"""Optional output work only; optimization and numerical gates remain unchanged."""
from pathlib import Path
import hashlib,json
B=Path('/workspace/revisit')
def patch():
    receipt=B/'output/core-source-patch.json'
    if receipt.exists():return
    records=[]
    def replace(name,old,new):
        p=B/'mosca'/name;s=p.read_text();assert s.count(old)==1,(name,old)
        before=hashlib.sha256(p.read_bytes()).hexdigest();p.write_text(s.replace(old,new))
        records.append(dict(file=name,before=before,after=hashlib.sha256(p.read_bytes()).hexdigest()))
    replace('lib_mosca/photo_recon.py', '        # viz\n        fig = plt.figure(figsize=(30, 8))',
        '        # Required checkpoints above are complete; videos/plots are optional.\n        if os.environ.get("CORE_DIAGNOSTICS", "0") != "1":\n            return\n        # viz\n        fig = plt.figure(figsize=(30, 8))')
    replace('mosca_reconstruct.py', '    # update the bundle cam\n    rgb, dep, alp = photo_solver.render_all(cams, s_model=s_model)',
        '    # Static fixed-camera export renders each frame separately downstream.\n    if os.environ.get("CORE_STATIC", "0") == "1" and os.environ.get("CORE_DIAGNOSTICS", "0") != "1":\n        return\n    # update the bundle cam\n    rgb, dep, alp = photo_solver.render_all(cams, s_model=s_model)')
    replace('lib_prior/epi_error/epi_analysis.py',
        '    epi_global_list = load_epi_error(global_epi_dir)\n    viz_epi_error_folder(epi_global_list, osp.join(working_dir, "epi_error.mp4"))',
        '    if os.environ.get("CORE_DIAGNOSTICS", "0") == "1":\n        epi_global_list = load_epi_error(global_epi_dir)\n        viz_epi_error_folder(epi_global_list, osp.join(working_dir, "epi_error.mp4"))')
    replace('mosca_reconstruct.py', '    viz_mosca_curves_before_optim(curve_xyz, curve_rgb, curve_mask, cams, log_path)',
        '    if os.environ.get("CORE_DIAGNOSTICS", "0") == "1":\n        viz_mosca_curves_before_optim(curve_xyz, curve_rgb, curve_mask, cams, log_path)')
    old = '    viz_list = viz_list_of_colored_points_in_cam_frame(\n        [cams.trans_pts_to_cam(t, it).cpu() for t, it in enumerate(scaffold._node_xyz)],\n        node_rgb,\n        zoom_out_factor=1.0,\n    )\n    imageio.mimsave(osp.join(log_path, "cam_curve_optimized.gif"), viz_list, loop=1000)'
    replace('mosca_reconstruct.py',old,'    if os.environ.get("CORE_DIAGNOSTICS", "0") == "1":\n'+'\n'.join('    '+line for line in old.split('\n')))
    receipt.write_text(json.dumps(dict(optionalDiagnosticsOnly=True,changes=records),indent=2)+'\n')
if __name__=='__main__':patch()
