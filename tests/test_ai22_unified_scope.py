"""Pure synthetic metadata regressions; no models, caches, rasterization or results."""
import ast
import math
from pathlib import Path
import unittest
p=Path(__file__).with_name('s12_unified.py')
if not p.exists():p=Path(__file__).resolve().parents[1]/'videos/ai/ai22/s12_unified.py'
node=next(n for n in ast.parse(p.read_text()).body if isinstance(n,ast.FunctionDef) and n.name=='unified_split_scope')
ns={'math':math}
exec(compile(ast.Module(body=[node],type_ignores=[]),str(p),'exec'),ns)
scope=ns['unified_split_scope']
class SplitScope(unittest.TestCase):
 def fixture(self):
  u={'pairs':[['A','A-bold'],['B','B-bold'],['C','C-bold']], 'held':[['B','B-bold']], 'seeds':[4,9], 'guide':1.5,'curve':[[[50,1]],[[50,1]]]}
  for k in ['name_acc','fam_acc','draw_acc','edit_rmse','copy_rmse','edit_ink','true_ink','edit_letter']:u[k]=[.2,.3]
  return u
 def test_different_catalog_and_seed_counts_are_data_driven(self):
  self.assertEqual(scope(self.fixture()),dict(pair_count=3,train_pairs=2,held_pairs=1,seed_count=2,cross_task_exposure='unverified'))
 def test_self_declared_exposure_is_never_verification(self):
  u=self.fixture();u.update(exposure_verified=True,verified_edit_exposure={'accepted':True,'source_excluded':True,'targets_in_base_training':True,'sha256':'a'*64})
  self.assertEqual(scope(u)['cross_task_exposure'],'unverified')
 def test_missing_or_ambiguous_split_fails_closed(self):
  variants=[{},{'held':[]},{'held':[['Z','Z-bold']]},{'pairs':[['A','A-bold'],['A','A-bold']]},{'held':[['B','B-bold'],['B','B-bold']]},{'pairs':[['A']]},{'seeds':[4,4]}]
  for changed in variants:
   u=self.fixture()
   if not changed:del u['pairs']
   else:u.update(changed)
   with self.subTest(changed=changed),self.assertRaises(ValueError):scope(u)
 def test_character_or_mapping_containers_are_not_pair_or_seed_lists(self):
  for changed in [dict(pairs=['AB','CD'],held=['AB']),dict(seeds='01'),dict(pairs={'AB':'CD'}),dict(held='AB'),dict(seeds={0:'a',1:'b'}),dict(seeds=[False,1]),dict(pairs=[b'AB',b'CD'],held=[b'AB'])]:
   u=self.fixture();u.update(changed)
   with self.subTest(changed=changed),self.assertRaises(ValueError):scope(u)
 def test_seed_metrics_and_curve_counts_must_match(self):
  for k in ['name_acc','edit_rmse','edit_ink','curve']:
   u=self.fixture();u[k]=[u[k][0]]
   with self.subTest(field=k),self.assertRaises(ValueError):scope(u)
 def test_nonfinite_metric_or_guidance_fails_closed(self):
  for value in [float('nan'),float('inf'),-float('inf')]:
   for k in ['guide','edit_rmse']:
    u=self.fixture()
    if k=='guide':u[k]=value
    else:u[k][0]=value
    with self.subTest(field=k,value=value),self.assertRaises(ValueError):scope(u)
if __name__=='__main__':unittest.main()
