"""Apply minimal recorded baseline repairs and opt-in shared-query adapter."""
from pathlib import Path
import hashlib,json,shutil,zipfile
B=Path('/workspace/revisit');R=B/'mosca'
def replace(p,old,new):
 s=p.read_text()
 assert old in s,(p,old[:80])
 p.write_text(s.replace(old,new,1))
def main():
 p=R/'mosca_precompute.py'
 replace(p,'        dep_mode=getattr(', '        metric3d_depth_version=getattr(pre_cfg, "metric3d_depth_version", "small"),\n        cotrakcer_version="3", cotracker_online_flag=True,\n        dep_mode=getattr(')
 p=R/'lib_prior/depth_models/metric3d_wrapper.py'
 replace(p,'model = torch.hub.load("yvanyin/metric3d", f"metric3d_vit_{version}", pretrain=True)', '''model = torch.hub.load('/workspace/revisit/sources/metric3d', f'metric3d_vit_{version}', source='local', pretrain=False)
    weights = torch.load(f'/workspace/revisit/weights/metric_depth_vit_{version}_800k.pth', map_location='cpu')['model_state_dict']
    result = model.load_state_dict(weights, strict=False)
    assert set(result.missing_keys) <= {'depth_model.encoder.mask_token'} and not result.unexpected_keys, str(result)
    model.checkpoint_loading_receipt = {'missingKeys': result.missing_keys, 'unexpectedKeys': result.unexpected_keys, 'allowedMissing': 'Unused zero-initialized DINO training mask token; unmasked inference only'}''')
 p=R/'mosca_evaluate.py'
 s=p.read_text().replace('imageio.imsave(osp.join(saved_dir, "fps_eval_samples.jpg"), viz)','imageio.imsave(osp.join(saved_dir, "fps_eval_samples.jpg"), (np.clip(viz, 0, 1)*255).astype(np.uint8))');p.write_text(s)
 p=R/'lib_mosca/camera.py'
 if p.read_text().strip()=='../lib_moca/camera.py':p.write_text((R/'lib_moca/camera.py').read_text())
 # Hash checks precede trusted torch checkpoint loads.
 records=json.loads((B/'weights/manifest.json').read_text())
 for row in records:
  p=B/'weights'/row['file'];assert hashlib.sha256(p.read_bytes()).hexdigest()==row['sha256'],p
 dst=R/'weights/tapnet/bootstapir_checkpoint_v2.pt';dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(B/'weights/bootstapir_checkpoint_v2.pt',dst)
 with zipfile.ZipFile(B/'weights/raft-models.zip') as z:
  names=[n for n in z.namelist() if n.endswith('raft-things.pth')];assert len(names)==1
  p=R/'weights/raft_models/raft-things.pth';p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(z.read(names[0]));assert hashlib.sha256(p.read_bytes()).hexdigest()=='fcfa4125d6418f4de95d84aec20a3c5f4e205101715a79f193243c186ac9a7e1'
 p=R/'lib_prior/tracking/cotracker_wrapper.py'
 s=p.read_text();start=s.index('    if online_flag:',s.index('def get_cotracker'));end=s.index('    cotracker.eval()',start)
 s=s[:start]+'''    assert online_flag and str(cotrakcer_version)=='3'
    cotracker=torch.hub.load('/workspace/revisit/sources/cotracker','cotracker3_online',source='local',pretrained=False)
    cotracker.model.load_state_dict(torch.load('/workspace/revisit/weights/scaled_online.pth',map_location='cpu'),strict=True)
    cotracker=cotracker.to(device)
'''+s[end:]
 start=s.index('    T = video_pt_cpu.shape[1]',s.index('def __online_inference_one_pass__'));end=s.index('\n\n@torch.no_grad()',start)
 s=s[:start]+'''    from tracker_adapter import online_pass
    return online_pass(video_pt_cpu,queries_cpu,model,device,add_support_grid)
'''+s[end:]
 # Keep all sampled query records, fixing upstream's last-chunk-only metadata.
 s=s.replace('    start_t = time.time()','    all_queries = []\n    start_t = time.time()',1).replace('        viz_list = viz_queries','        all_queries.append(queries)\n        viz_list = viz_queries',1).replace('queries=queries.numpy(),','queries=torch.cat(all_queries,1).numpy(),')
 p.write_text(s)
 (B/'output/patch-manifest.json').write_text(json.dumps({str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [R/'mosca_precompute.py',R/'lib_prior/depth_models/metric3d_wrapper.py',R/'lib_prior/tracking/cotracker_wrapper.py',R/'mosca_evaluate.py',R/'lib_mosca/camera.py']},indent=2))
 print('Pinned loaders and historical source repairs installed',flush=True)
if __name__=='__main__':main()
