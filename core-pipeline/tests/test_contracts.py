import importlib.util,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def module(name):
 spec=importlib.util.spec_from_file_location(name,ROOT/'worker'/f'{name}.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
c=module('contracts')
class StageContracts(unittest.TestCase):
 def test_geometry_review_prevents_appearance(self):
  receipts={k:dict(exitCode=0) for k in ['prepare','bundle','dense']}
  with self.assertRaisesRegex(AssertionError,'Geometry review'):c.check_stage('photo',receipts,priors_review=True)
  c.check_stage('photo',receipts,priors_review=True,geometry_review=True)
 def test_failed_stage_is_not_success(self):
  with self.assertRaisesRegex(AssertionError,'prepare'):c.check_stage('bundle',{'prepare':dict(exitCode=1)},priors_review=True)
 def test_dynamic_requires_actual_motion_and_foreground_review(self):
  receipts={k:dict(exitCode=0) for k in ['prepare','bundle','dense','motion','foreground']}
  with self.assertRaisesRegex(AssertionError,'Motion review'):c.check_stage('photo',receipts,True,True,'dynamic')
  with self.assertRaisesRegex(AssertionError,'Foreground review'):c.check_stage('photo',receipts,True,True,'dynamic',True)
  c.check_stage('photo',receipts,True,True,'dynamic',True,True)
class CameraContracts(unittest.TestCase):
 def setUp(self):
  self.c=module('camera_contract');import numpy as np;self.np=np
 def test_named_pose_order_and_shared_scale(self):
  a=self.np.eye(4);b=self.np.eye(4);b[:3,3]=[1,2,3]
  result=self.c.build_contract([dict(file='a'),dict(file='b')],[dict(file='b',cameraToWorld=b.tolist()),dict(file='a',cameraToWorld=a.tolist())],[[400,0,320],[0,400,180],[0,0,1]],2)
  self.assertEqual(result['cameraToWorld'][1][0][3],2)
  self.assertEqual(result['cameraToWorld'][1][2][3],6)
  self.assertEqual(result['nativePrincipalPointRatio'],[.5,.5])
 def test_improper_pose_or_missing_identity_is_rejected(self):
  a=self.np.eye(4);a[0,0]=-1
  with self.assertRaises(ValueError):self.c.homogeneous(a)
  with self.assertRaises(ValueError):self.c.build_contract([dict(file='a')],[],[[400,0,320],[0,400,180],[0,0,1]])
if __name__=='__main__':unittest.main()
