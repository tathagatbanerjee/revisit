"""Apply a hash-checked, opt-in correction to a freshly extracted worker source."""
from pathlib import Path
import hashlib,json
EXPECTED='a34d26489f87c6aa48c746eee0ea9c86be0fab7629d020546b96af0e92a0e28d'
def patch(path):
 before=path.read_text();assert hashlib.sha256(path.read_bytes()).hexdigest()==EXPECTED
 after=before
 # The pinned file's import layout is retained; add the independent helper only.
 after='from ba_depth_validity import guard, safe_depth_inputs\n'+after
 marker='        uv_target = homo_list[None, tgt_inds].expand('
 inserted='''        # Only physically visible positive-depth pairs enter flow/depth ratios.
        target_depth_for_guard = scaled_depth_list[None, tgt_inds].expand(
            len(uv_src_to_every_frame), -1, -1)
        raw_visible_pairs = s_track_valid_mask[:, None] * s_track_valid_mask[None, tgt_inds]
        cross_time_mask, positive_depth_pairs = guard().mask(
            point_ref_to_every_frame[..., -1], scaled_depth_list[:, None],
            target_depth_for_guard, raw_visible_pairs, cross_time_mask, tgt_inds, step)

'''
 assert after.count(marker)==1;after=after.replace(marker,inserted+marker,1)
 marker='        warped_depth = point_ref_to_every_frame[..., -1]'
 assert after.count(marker)==1;after=after.replace(marker,marker+'\n        warped_depth, dep_target = safe_depth_inputs(warped_depth, dep_target, positive_depth_pairs)',1)
 marker='        loss.backward()';assert after.count(marker)==1
 after=after.replace(marker,'''        guard().losses(step, flow=uv_loss, depth=dep_loss, correction=dep_corr_loss,
                       cameraRotation=cam_rot_loss, cameraTranslation=cam_trans_loss, total=loss)
'''+marker,1)
 path.write_text(after)
 return {'beforeSha256':EXPECTED,'afterSha256':hashlib.sha256(path.read_bytes()).hexdigest(),'change':'Positive camera/source/target depth mask for flow and depth, safe ratio inputs, support/coverage guards and separated loss diagnostics; weights and initialization unchanged'}
if __name__=='__main__':
 base=Path('/workspace/revisit');config=json.loads((base/'depth-correction.json').read_text());assert hashlib.sha256((base/'ba_depth_validity.py').read_bytes()).hexdigest()==config['helperSha256'];assert hashlib.sha256(Path(__file__).read_bytes()).hexdigest()==config['patcherSha256'];receipt=patch(base/'mosca/lib_moca/bundle.py');(base/'output/depth-validity-patch.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt))
