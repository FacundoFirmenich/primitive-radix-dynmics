from fractions import Fraction
from rmr.core import T,S,defects
B=88011536665779
states=[Fraction(406,731),Fraction(712,731),Fraction(712,1265),Fraction(1218,1265),Fraction(406,557)]
def test_maps():
    assert [states.index(T(x,B)) for x in states]==[1,0,3,2,4]
    assert [states.index(S(x,B)) for x in states]==[4,2,1,0,0]
def test_strict_edge():
    assert [(i,defects(x,B)) for i,x in enumerate(states)]==[(0,(1,1)),(1,(1,1)),(2,(1,1)),(3,(1,3)),(4,(1,1))]
