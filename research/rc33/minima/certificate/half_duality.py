"""Half inversion, its exact parity gate, and verified r3 transfers."""
from fractions import Fraction as F
from fibre_arithmetic import complete


def T(x, base):
    return base*x - (base*x).__floor__()


def S(x, base):
    return 1/(1+T(1/x-1, base))


def psi(x):
    return 1/(2*x)


def dual_base_fibre(states, residue, period):
    """Complete dual-admissible base subfibre for a known carrier base fibre.

    The caller supplies a valid original base fibre. The period must contain
    every reduced numerator, which makes the parity gate periodic modulo 2L.
    """
    states = tuple(map(F, states))
    if period <= 0 or any(period % x.numerator for x in states):
        raise ValueError('Period does not support the declared parity argument')
    tests = []
    for lift in (0, 1):
        b = residue + lift*period
        if b < 2:
            b += ((2-b+2*period-1)//(2*period))*(2*period)
        eps = [(b/x).__floor__() % 2 for x in states]
        tests.append(dict(lift=lift, base=b, epsilon=eps, admissible=all(eps)))
    good = [x for x in tests if x['admissible']]
    if len(good) == 2:
        fibres = [(residue % period, period)]
    elif good:
        fibres = [(good[0]['base'] % (2*period), 2*period)]
    else:
        fibres = []
    return dict(tests=tests, fibres=fibres)


def transfer_r3(orientation, core, E, residue, period):
    """Return only ten-edge-verified dual carriers of the opposite orientation."""
    A, C, D, Q = map(int, core)
    if orientation == 'normal':
        raw = ((A,Q),(C,Q),(C,D),(3*A,D),(A,E))
        target_orientation = 'reflected'
    else:
        raw = ((Q,A),(Q,C),(D,C),(D,3*A),(E,A))
        target_orientation = 'normal'
    states = tuple(F(p,q) for p,q in raw)
    gate = dual_base_fibre(states, residue, period)
    if not gate['fibres']:
        return dict(gate=gate, transfers=[])
    parities = {x.denominator % 2 for x in states}
    assert len(parities) == 1, 'Odd-content strong carriers cannot mix denominator parity under this duality'
    even = parities == {0}
    if orientation == 'normal':
        target = (A,C,D//2,Q//2) if even else (2*A,2*C,D,Q)
        expected_E = E//2 if even else E
        assert D == 3*E-2*A, 'The j=1 branch cannot pass the dual parity gate'
    else:
        target = (A//2,C//2,D,Q) if even else (A,C,2*D,2*Q)
        expected_E = E if even else 2*E
    hits = complete(3, target, target_orientation)
    hits = [h for h in hits if h['E'] == expected_E]
    assert hits, 'Duality must produce an actual opposite carrier'
    target_states = tuple(psi(x) for x in states)
    for test in gate['tests']:
        if not test['admissible']:
            continue
        b = test['base']
        for x in states:
            assert S(psi(x), b) == psi(T(x, b))
            assert T(psi(x), b) == psi(S(x, b))
        assert any((b-h['base']) % h['period'] == 0 for h in hits)
    return dict(gate=gate, target_orientation=target_orientation,
                target_states=list(map(str,target_states)), transfers=hits)
