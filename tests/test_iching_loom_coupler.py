import unittest
from arguelles.iching_loom_coupler import (
 yao_index,inverse_yao_index,join_kin_yao,split_joint_phase,coupling_invariants
)
class IChingLoomExactTests(unittest.TestCase):
 def test_full_384_yao_bijection(self):
  seen=set()
  for h in range(1,65):
   for line in range(1,7):
    j=yao_index(h,line);seen.add(j)
    self.assertEqual(inverse_yao_index(j),(h,line))
  self.assertEqual(seen,set(range(384)))
 def test_full_24960_joint_bijection(self):
  phases=set()
  for t in range(24960):
   x=split_joint_phase(t)
   self.assertEqual(x['phase'],t)
   phases.add((x['kin'],x['hexagram'],x['line']))
  self.assertEqual(len(phases),24960)
 def test_incompatible_noninvented(self):
  self.assertIsNone(join_kin_yao(1,2,1)['phase'])
  self.assertEqual(join_kin_yao(1,1,1)['phase'],0)
  t=join_kin_yao(1,5,1)['phase']
  self.assertIsNotNone(t)
  self.assertEqual(t%260,0)
  self.assertEqual(t%384,4)
 def test_invariants(self):
  r=coupling_invariants()
  self.assertEqual((r['gcd'],r['lcm'],r['classes']),(4,24960,4))
if __name__=='__main__':unittest.main()