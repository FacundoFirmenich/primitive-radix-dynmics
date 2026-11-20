import unittest
from fractions import Fraction
from arguelles.loom_bridge import (
 PORTALS, coordinates, kin_at, quartets, portal_grid, full_audit,
 generalized_crt, phase_bridge, finite_radix_orbit, rational_residue,
 witness_modular_readings, reciprocal_certificate, franklin_certificate,
 harmonics_1366560
)
class LoomExactTests(unittest.TestCase):
 def test_all_19_certificates(self):
  audit=full_audit()
  self.assertTrue(audit['pass'], {k:v for k,v in audit['checks'].items() if not v})
  self.assertEqual(len(audit['checks']),19)
 def test_grid_roundtrip_260(self):
  for k in range(1,261):self.assertEqual(kin_at(*coordinates(k)), k)
 def test_portal_grid_52_and_mystic_column(self):
  mat=portal_grid()
  self.assertEqual(len(mat),20)
  self.assertEqual([len(x) for x in mat],[13]*20)
  self.assertEqual(sum(row.count('#') for row in mat),52)
  self.assertTrue(all(row[6]=='.' for row in mat))
 def test_13_quartets_disjoint_cover(self):
  blocks=quartets()
  self.assertEqual(len(blocks),13)
  self.assertEqual({k for b in blocks for k in b},set(PORTALS))
  self.assertEqual(sum(len(b) for b in blocks),52)
 def test_all_260_occult(self):
  self.assertTrue(all(reciprocal_certificate(k)['same_portal_membership'] for k in range(1,261)))
 def test_generalized_crt_non_coprime(self):
  self.assertEqual(generalized_crt(1,260,1,64), (1,4160))
  self.assertIsNone(generalized_crt(1,260,2,64))
  self.assertEqual(phase_bridge((260,64))['orbit_classes'],4)
  self.assertEqual(phase_bridge((260,365))['orbit_classes'],5)
 def test_rational_abstain_primitive(self):
  self.assertIsNone(rational_residue(1,13,260))
  self.assertEqual(rational_residue(4,3,64),44)
  self.assertEqual(rational_residue(2,4,5),3)
 def test_radix_orbit_exact(self):
  for m in range(2,50):
   for B in (2,3,5,20):
    for seed in (0,1,m-1):
     x=finite_radix_orbit(m,B,seed)
     seq=x['trace']; pre=x['preperiod'];period=x['period']
     self.assertEqual((B*seq[-1])%m,seq[pre])
     self.assertEqual(len(seq),pre+period)
 def test_real_rc33_witness_observation(self):
  A,C,D,Q,E=1089859,1627375,3121631,2087631,2105745
  xs=[Fraction(A,Q),Fraction(C,Q),Fraction(C,D),Fraction(2*A,D),Fraction(A,E)]
  obs=witness_modular_readings(xs,(2,4,8,16,32,64,260))
  self.assertEqual([obs[m]['rank'] for m in (2,4,8,16,32)], [2,3,4,4,5])
  self.assertEqual(obs[260]['defined'],2)
  self.assertEqual(len(obs[260]['abstentions']),3)
  self.assertEqual(obs[64]['rank'],5)
 def test_franklin_not_ordinary_magic_diagonals(self):
  s=franklin_certificate()
  self.assertEqual(s['ordinary_diagonal_sums'],(228,292))
  self.assertEqual(set(s['toroidal_2x2_sums']),{130})
 def test_1366560_exact_no_mars(self):
  a=harmonics_1366560()
  self.assertEqual(a['exact_quotients'][260],5256)
  self.assertEqual(a['exact_quotients'][584],2340)
  self.assertEqual(a['exact_quotients'][360],3796)
  self.assertEqual(a['exact_quotients'][365],3744)
  self.assertEqual(a['exact_quotients'][18980],72)
  self.assertEqual(a['exact_quotients'][37960],36)
  self.assertNotIn(780,a['exact_quotients'])
if __name__=='__main__':unittest.main()