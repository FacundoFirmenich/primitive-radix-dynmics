import unittest
from arguelles.partition_scheduler import (
 assignment,partitions,iter_castle,verify_castle_plan,count_residue
)

class SchedulerExactTests(unittest.TestCase):
 def test_existing_excluded_Q_interval_2_20000_coverage_not_solver(self):
  cert=verify_castle_plan(2,20000)
  self.assertEqual(cert['expected_count'],19999)
  self.assertTrue(cert['coverage_exact'])
  self.assertEqual((cert['missing_count'],cert['overlap_count']), (0,0))
  self.assertEqual(sum(cert['lane_counts']),19999)
  self.assertEqual(sum(cert['portal_class_counts'].values()),19999)
  self.assertEqual(cert['solver_calls'],0)
 def test_next_unchecked_Q_interval_scheduler(self):
  r=verify_castle_plan(20001,22000)
  self.assertTrue(r['coverage_exact'])
  self.assertEqual(r['expected_count'],2000)
 def test_modular_exact_counts_exhaustive_small(self):
  for lo,hi in ((1,260),(42,777),(300,580),(5001,7000)):
   for r in range(260):
    self.assertEqual(count_residue(lo,hi,r),sum(q%260==r for q in range(lo,hi+1)))
 def test_roundtrip_assignment_yijing_and_castle(self):
  for q in (1,2,13,52,64,260,384,260*384,2087631):
   a=assignment(q)
   self.assertEqual((a['kin']-1)%260,q%260)
   self.assertEqual(a['phase_mod_24960'],q%24960)
   self.assertIn(q,list(iter_castle(q,q,a['castle'])))
 def test_all_castles_complete_on_one_cycle(self):
  for c in range(1,6):
   self.assertEqual(len(list(iter_castle(1,260,c))),52)
  self.assertEqual(partitions(1,260,'portal'),{'N':208,'P':52})
if __name__=='__main__':unittest.main()