"""Standard-library local extraction; exact source PTS, no GPU allocation."""
from pathlib import Path
import hashlib,json,subprocess,sys

def prepare(folder):
    root=Path(folder);cfg=json.loads((root/'config.json').read_text());source=root/'source.video'
    raw=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','frame=best_effort_timestamp_time','-of','json',str(source)],timeout=60))
    pts=[float(f['best_effort_timestamp_time']) for f in raw['frames']]
    assert pts and all(pts[i]<=pts[i+1] for i in range(len(pts)-1)),'Non-monotonic source timestamps'
    n=round(cfg['durationSeconds']*cfg['fps']);selected=[]
    for j in range(n):
        t=cfg['startSeconds']+j/cfg['fps'];i=min(range(len(pts)),key=lambda i:abs(pts[i]-t));selected.append(i)
    assert len(set(selected))==n,'Input has too few distinct observations at 12 Hz'
    frames=root/'prepared'/'images';frames.mkdir(parents=True,exist_ok=False)
    # A balanced expression avoids FFmpeg5 expression recursion limits at360
    # selected states; a left-associated360-term sum can fail parsing.
    def combine(terms):
        if len(terms)==1:return terms[0]
        middle=len(terms)//2
        return '('+combine(terms[:middle])+'+'+combine(terms[middle:])+')'
    select=combine([f'eq(n\\,{i})' for i in selected])
    command=['ffmpeg','-hide_banner','-loglevel','error','-filter_threads','1','-threads','2','-i',str(source),'-vf',f'select={select},scale=640:360,setsar=1','-fps_mode','vfr','-threads','1','-start_number','0',str(frames/'%05d.png')]
    completed=subprocess.run(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,timeout=240)
    if completed.returncode:raise RuntimeError('Frame extraction failed: '+completed.stderr[-1800:])
    files=sorted(frames.glob('*.png'));assert len(files)==n,'Extraction count mismatch'
    rows=[dict(index=j,file=f.name,sourceFrame=i,sourceSeconds=pts[i],eventSeconds=pts[i]-pts[selected[0]],sha256=hashlib.sha256(f.read_bytes()).hexdigest(),split='map') for j,(i,f) in enumerate(zip(selected,files))]
    (root/'prepared/frames.json').write_text(json.dumps(rows,indent=2)+'\n')
    report=dict(observations=n,firstSourceSeconds=rows[0]['sourceSeconds'],lastSourceSeconds=rows[-1]['sourceSeconds'],width=640,height=360,fps=12,clock='actual source presentation timestamps; nearest unique frame',previewFiles=[files[round((n-1)*i/5)].name for i in range(6)],cameraMappingPassed=False,reconstructionCreated=False)
    (root/'prepared/report.json').write_text(json.dumps(report,indent=2)+'\n');return report
if __name__=='__main__':print(json.dumps(prepare(sys.argv[1])))
