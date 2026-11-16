"""Map already extracted static observations. CPU-only; requires pycolmap/NumPy."""
from pathlib import Path
import json,sys,time

def main(folder):
    import numpy as np,pycolmap
    root=Path(folder).resolve();prepared=root/'prepared';rows=json.loads((prepared/'frames.json').read_text())
    review=json.loads((root/'project.json').read_text()).get('sourceReview',{})
    if not review.get('passed'):raise ValueError('Review source continuity in the app before mapping')
    target=root/'mapping';target.mkdir(exist_ok=False);start=time.monotonic()
    reader=pycolmap.ImageReaderOptions();reader.camera_model='SIMPLE_PINHOLE'
    ex=pycolmap.FeatureExtractionOptions();ex.num_threads=4;ex.max_image_size=640;ex.use_gpu=False
    match=pycolmap.FeatureMatchingOptions();match.num_threads=4;match.use_gpu=False
    pycolmap.extract_features(target/'database.db',prepared/'images',camera_mode=pycolmap.CameraMode.SINGLE,reader_options=reader,extraction_options=ex,device=pycolmap.Device.cpu)
    seq=pycolmap.SequentialPairingOptions();seq.overlap=12;seq.quadratic_overlap=True;seq.loop_detection=False
    pycolmap.match_sequential(target/'database.db',matching_options=match,pairing_options=seq,device=pycolmap.Device.cpu)
    opt=pycolmap.IncrementalPipelineOptions();opt.num_threads=4;opt.random_seed=12345;opt.max_runtime_seconds=600;opt.mapper.init_min_tri_angle=4;opt.triangulation.ignore_two_view_tracks=False
    opt.ba_refine_principal_point=False;opt.ba_refine_extra_params=False
    models=pycolmap.incremental_mapping(target/'database.db',prepared/'images',target/'sparse',options=opt)
    if not models:raise ValueError('Camera recovery failed: capture overlapping stationary textured surfaces with more camera translation')
    key,model=max(models.items(),key=lambda x:x[1].num_reg_images());report=dict(registered=model.num_reg_images(),frames=len(rows),points=model.num_points3D(),medianError=float(np.median([p.error for p in model.points3D.values()])),seconds=time.monotonic()-start,pycolmapVersion=pycolmap.__version__)
    report['passed']=report['registered']==len(rows) and report['points']>=400 and report['medianError']<=2
    (target/'map-initial-result.json').write_text(json.dumps(report,indent=2)+'\n')
    if not report['passed']:raise ValueError('Camera map failed coverage/error gate. Failed map is retained; use a new upload.')
    assert len(model.cameras)==1
    poses={im.name:dict(file=im.name,cameraToWorld=im.cam_from_world().inverse().matrix().tolist()) for im in model.images.values()}
    package=dict(K=next(iter(model.cameras.values())).calibration_matrix().tolist(),poses=[poses[r['file']] for r in rows])
    (target/'map-cameras.json').write_text(json.dumps(package,indent=2)+'\n')
    index={r['file']:r['index'] for r in rows};points=[(pid,p) for pid,p in model.points3D.items() if len(p.track.elements)>=4 and p.error<=2]
    valid=np.zeros((len(rows),len(points)),bool);tracks=np.zeros((*valid.shape,2),np.float32)
    for j,(_,p) in enumerate(points):
        for e in p.track.elements:
            im=model.image(e.image_id);i=index[im.name];valid[i,j]=True;tracks[i,j]=im.point2D(e.point2D_idx).xy
    remaining=set(range(len(points)));chosen=[];coverage=np.zeros(len(rows),int)
    while remaining and len(chosen)<4000:
        deficit=np.maximum(160-coverage,0)
        if not deficit.any():break
        candidates=sorted(remaining);j=candidates[int(np.argmax(valid[:,candidates].T@deficit))];chosen.append(j);remaining.remove(j);coverage+=valid[:,j]
    chosen+=sorted(remaining,key=lambda j:(-int(valid[:,j].sum()),points[j][0]))[:4000-len(chosen)]
    report.update(selectedTracks=len(chosen),minimumObserved=int(valid[:,chosen].sum(1).min()) if chosen else 0)
    report['passed'] &= report['minimumObserved']>=64
    np.savez_compressed(target/'map-tracks.npz',tracks=tracks[:,chosen],valid=valid[:,chosen],mapWorld=np.array([points[j][1].xyz for j in chosen]))
    (target/'map-result.json').write_text(json.dumps(report,indent=2)+'\n')
    if not report['passed']:raise ValueError('Insufficient observed static anchors per frame. Retry a suitable new capture.')
    print(json.dumps(report))
if __name__=='__main__':main(sys.argv[1])
