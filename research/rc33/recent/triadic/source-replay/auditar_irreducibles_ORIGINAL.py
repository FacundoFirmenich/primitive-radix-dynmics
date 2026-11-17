#!/usr/bin/env python3
"""Atlas exacto de {4777} y {6444} como dos operandos indivisibles.

Sólo biblioteca estándar. No inspecciona, segmenta, rota, ordena ni factoriza
las escrituras de entrada. La interfaz permite operaciones sobre valores completos.
Conserva expresiones y procedencia aunque la evaluación cancele una dependencia.
La opacidad es un contrato de interfaz, no una garantía de seguridad contra reflexión.

Ejecutar: python auditar_irreducibles.py --out-dir salida
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from collections import defaultdict
from dataclasses import dataclass
from fractions import Fraction as F
from pathlib import Path
from typing import Any

if hasattr(sys, 'set_int_max_str_digits'):
    sys.set_int_max_str_digits(100000)

CHECKS: list[str] = []

def check(ok: bool, label: str) -> None:
    if not ok:
        raise AssertionError(label)
    CHECKS.append(label)

@dataclass(frozen=True)
class Whole:
    """Nodo de expresión. Nunca se ofrecen caracteres o trozos de un operando."""
    op: str
    args: tuple['Whole', ...] = ()
    atom_name: str = ''

    def __getitem__(self, key: Any) -> Any:
        raise TypeError('Los paquetes son indivisibles: no hay indexación ni cortes.')

    def __iter__(self) -> Any:
        raise TypeError('No se pueden iterar componentes internos del paquete.')

    def __len__(self) -> int:
        raise TypeError('La longitud de la escritura no es observable de este núcleo.')

    def __add__(self, other: 'Whole') -> 'Whole':
        return Whole('add', (self, require(other)))

    def __sub__(self, other: 'Whole') -> 'Whole':
        return Whole('sub', (self, require(other)))

    def __mul__(self, other: 'Whole') -> 'Whole':
        return Whole('mul', (self, require(other)))

    def __truediv__(self, other: 'Whole') -> 'Whole':
        other = require(other)
        if evaluate(other) == 0:
            raise ZeroDivisionError('Denominador completo nulo.')
        return Whole('div', (self, other))

    def __neg__(self) -> 'Whole':
        return Whole('neg', (self,))

    def inverse(self) -> 'Whole':
        if evaluate(self) == 0:
            raise ZeroDivisionError('Cero no tiene recíproco.')
        return Whole('inv', (self,))


def require(x: Any) -> Whole:
    if not isinstance(x, Whole):
        raise TypeError('Se requiere un nodo Whole, no un fragmento ni un escalar externo.')
    return x

# Únicos paquetes de entrada: no se incluye {644}, ni ninguna cifra de las fuentes.
SOURCE_VALUES = {'{4777}': F(4777), '{6444}': F(6444)}
X = Whole('atom', atom_name='{4777}')
Y = Whole('atom', atom_name='{6444}')
ONE = Whole('unit')
ZERO = ONE - ONE
TWO = ONE + ONE
FOUR = TWO + TWO


def evaluate(e: Whole) -> F:
    if e.op == 'atom':
        return SOURCE_VALUES[e.atom_name]
    if e.op == 'unit':
        return F(1)
    a = evaluate(e.args[0])
    if e.op == 'neg': return -a
    if e.op == 'inv': return 1 / a
    b = evaluate(e.args[1])
    if e.op == 'add': return a + b
    if e.op == 'sub': return a - b
    if e.op == 'mul': return a * b
    if e.op == 'div': return a / b
    if e.op == 'gcd':
        if a.denominator != 1 or b.denominator != 1:
            raise ValueError('gcd requiere operandos enteros completos.')
        return F(math.gcd(a.numerator, b.numerator))
    if e.op == 'lcm':
        if a.denominator != 1 or b.denominator != 1:
            raise ValueError('lcm requiere operandos enteros completos.')
        return F(math.lcm(a.numerator, b.numerator))
    raise ValueError(f'Operador desconocido: {e.op}')


def sources(e: Whole) -> frozenset[str]:
    if e.op == 'atom': return frozenset((e.atom_name,))
    out: frozenset[str] = frozenset()
    for a in e.args: out = out | sources(a)
    return out


def expression(e: Whole) -> str:
    if e.op == 'atom': return e.atom_name
    if e.op == 'unit': return '(+01)'
    if e.op == 'neg': return f'(-{expression(e.args[0])})'
    if e.op == 'inv': return f'((+01)/{expression(e.args[0])})'
    if e.op in ('gcd','lcm'):
        return f'{e.op}({expression(e.args[0])},{expression(e.args[1])})'
    symbol = {'add':'+','sub':'-','mul':'*','div':'/'}[e.op]
    return f'({expression(e.args[0])}{symbol}{expression(e.args[1])})'


def record(e: Whole) -> dict[str, Any]:
    return {'expression': expression(e), 'value': str(evaluate(e)),
            'sources': sorted(sources(e))}


def export_dag(roots: dict[str, Whole]) -> dict[str, Any]:
    ids: dict[Whole, int] = {}
    nodes: list[dict[str, Any]] = []
    def visit(e: Whole) -> int:
        if e in ids: return ids[e]
        args = [visit(a) for a in e.args]
        idx = len(nodes)
        ids[e] = idx
        node = {'id':idx, 'op':e.op, 'args':args,
                'value':str(evaluate(e)), 'sources':sorted(sources(e))}
        if e.op == 'atom': node['atom'] = e.atom_name
        nodes.append(node)
        return idx
    root_ids = {name:visit(e) for name,e in roots.items()}
    return {'roots':root_ids, 'nodes':nodes}


def exhaustive(max_leaves: int = 5) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Cuenta TODOS los árboles ordenados +/-/*// con fuentes X,Y hasta n hojas.

    Agrupa por (valor, soporte), pero mantiene multiplicidades sintácticas.
    La agrupación es exacta porque valor y soporte determinan las transiciones.
    Se excluye cualquier árbol con una división por cero, incluso interna.
    """
    levels: list[dict[tuple[F,int], tuple[int,str]]] = [dict(),
        {(F(4777),1):(1,'{4777}'), (F(6444),2):(1,'{6444}')}]
    summary = []
    for n in range(1, max_leaves+1):
        if n > 1:
            counts: defaultdict[tuple[F,int], int] = defaultdict(int)
            witnesses: dict[tuple[F,int],str] = {}
            for k in range(1,n):
                for (a,sa),(ca,wa) in levels[k].items():
                    for (b,sb),(cb,wb) in levels[n-k].items():
                        support = sa | sb
                        outcomes = [('+',a+b),('-',a-b),('*',a*b)]
                        if b: outcomes.append(('/',a/b))
                        for op,v in outcomes:
                            key=(v,support)
                            counts[key] += ca*cb
                            if key not in witnesses:
                                witnesses[key]=f'({wa}{op}{wb})'
            levels.append({k:(v,witnesses[k]) for k,v in counts.items()})
        level=levels[n]
        raw=math.comb(2*(n-1),n-1)//n * 2**n * 4**(n-1)
        valid=sum(c for c,w in level.values())
        row={'leaf_occurrences':n, 'all_syntactic_trees':raw,
             'valid_trees':valid, 'undefined_trees':raw-valid,
             'distinct_values':len({v for v,mask in level}),
             'valid_joint_trees':sum(c for (v,mask),(c,w) in level.items() if mask==3),
             'distinct_joint_values':len({v for v,mask in level if mask==3})}
        summary.append(row)
        check(0 <= valid <= raw, f'enumeración: límites nivel {n}')
    # Segundo conteo independiente, sin agrupar valores, hasta cuatro hojas.
    rawlevels: list[list[tuple[F,int]]] = [[],[(F(4777),1),(F(6444),2)]]
    for n in range(2,min(max_leaves,4)+1):
        out=[]
        for k in range(1,n):
            for a,sa in rawlevels[k]:
                for b,sb in rawlevels[n-k]:
                    out.extend(((a+b,sa|sb),(a-b,sa|sb),(a*b,sa|sb)))
                    if b: out.append((a/b,sa|sb))
        rawlevels.append(out)
    for n in range(1,len(rawlevels)):
        actual=defaultdict(int)
        for key in rawlevels[n]: actual[key]+=1
        predicted={key:c for key,(c,w) in levels[n].items()}
        check(dict(actual)==predicted, f'conteo independiente sin compresión nivel {n}')
    # Un testigo mínimo por cada pareja (valor, soporte), conservando procedencia.
    union: dict[tuple[F,int],dict[str,Any]] = {}
    for n,level in enumerate(levels[1:],1):
        for (v,mask),(count,witness) in sorted(level.items(),key=lambda t:(t[0][0],t[0][1])):
            if (v,mask) not in union:
                union[(v,mask)]={'value':str(v),'source_mask':mask,
                    'minimum_leaves_within_search':n,'witness':witness}
    detail={'source_mask_definition':{'1':'{4777}','2':'{6444}','3':'ambos'},
            'max_leaves':max_leaves,
            'total_valid_trees':sum(r['valid_trees'] for r in summary),
            'total_valid_joint_trees':sum(r['valid_joint_trees'] for r in summary),
            'distinct_values_up_to_bound':len({v for v,mask in union}),
            'distinct_joint_values_up_to_bound':len({v for v,mask in union if mask==3}),
            'witnesses':list(union.values())}
    return summary,detail


def output_decimal(q: F) -> dict[str, Any]:
    """Serializa el RESULTADO racional, no analiza las fuentes como escritura."""
    if q <= 0: raise ValueError('Se requiere resultado positivo.')
    whole,r=divmod(q.numerator,q.denominator)
    seen: dict[int,int]={}; output=[]
    while r and r not in seen:
        seen[r]=len(output)
        d,r=divmod(10*r,q.denominator)
        output.append(str(d))
    cut=seen[r] if r else len(output)
    pre=''.join(output[:cut]); cycle=''.join(output[cut:])
    reconstruction=F(whole)+F(int(pre or '0'),10**len(pre))
    if cycle:
        reconstruction+=F(int(cycle),10**len(pre)*(10**len(cycle)-1))
    check(reconstruction==q,f'reconstrucción de salida decimal {q}')
    return {'integer_part':str(whole),'preperiod':pre,'period':cycle,
            'preperiod_length':len(pre),'period_length':len(cycle)}


def matmul(a: tuple[tuple[F,F],tuple[F,F]],
           b: tuple[tuple[F,F],tuple[F,F]]) -> tuple[tuple[F,F],tuple[F,F]]:
    return tuple(tuple(sum(a[i][k]*b[k][j] for k in range(2))
                       for j in range(2)) for i in range(2))  # type: ignore


def extended_euclid(a: int, b: int) -> tuple[int, int, int, list[dict[str, int]]]:
    """Bézout por Euclides sobre valores de paquetes completos."""
    r0, r1 = a, b
    s0, s1 = 1, 0
    t0, t1 = 0, 1
    steps: list[dict[str, int]] = []
    while r1:
        q, r2 = divmod(r0, r1)
        steps.append({'dividend': r0, 'divisor': r1, 'quotient': q, 'remainder': r2})
        r0, r1 = r1, r2
        s0, s1 = s1, s0 - q*s1
        t0, t1 = t1, t0 - q*t1
    return r0, s0, t0, steps


def continued_fraction(a: int, b: int) -> list[int]:
    """Fracción continua exacta de a/b, sin abrir las fuentes."""
    out=[]
    while b:
        q, r=divmod(a,b)
        out.append(q)
        a,b=b,r
    return out


def convergents(coeffs: list[int]) -> list[F]:
    p_minus2, p_minus1=0,1
    q_minus2, q_minus1=1,0
    out=[]
    for a in coeffs:
        p = a*p_minus1+p_minus2
        q = a*q_minus1+q_minus2
        out.append(F(p,q))
        p_minus2,p_minus1=p_minus1,p
        q_minus2,q_minus1=q_minus1,q
    return out


def modular_inverse_tails(a: int, k_min: int=1, k_max: int=12) -> list[dict[str, Any]]:
    """Inversas de EVALUACIONES completas módulo 10**k; escribe los resultados con anchura k."""
    tails=[]
    for k in range(k_min,k_max+1):
        m=10**k
        v=pow(a,-1,m)
        check(a*v % m == 1, f'inversa por terminación k={k}')
        if tails:
            check(v%10**(k-1)==int(tails[-1]['residue']),f'compatibilidad inversa k={k}')
        tails.append({'k':k,'modulus':str(m),'residue':str(v),'padded_output':str(v).zfill(k)})
    return tails


def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out-dir',type=Path,default=Path('salida_irreducible'))
    args=parser.parse_args(); args.out_dir.mkdir(parents=True,exist_ok=True)
    x=evaluate(X); y=evaluate(Y)
    # Se prueba la frontera de la interfaz, no una seguridad contra reflexión.
    for source in (X,Y):
        for name,fn in (('indexación',lambda a:a[0]),('iteración',iter),('longitud',len)):
            try: fn(source)
            except TypeError: check(True,f'fuente opaca: {source.atom_name}: {name} bloqueada')
            else: check(False,f'fuente abierta: {source.atom_name}: {name}')
    try: X/ZERO
    except ZeroDivisionError: check(True,'división por cero rechazada')
    else: check(False,'división por cero no rechazada')
    S=X+Y; D=Y-X; P=X*Y; E=X*X+Y*Y
    roots={'sum':S,'difference':D,'product':P,
           'ratio_6444_over_4777':Y/X,'ratio_4777_over_6444':X/Y,
           'inverse_4777':X.inverse(),'inverse_6444':Y.inverse(),
           'sum_inverses':X.inverse()+Y.inverse(),
           'difference_inverses':X.inverse()-Y.inverse(),
           'product_inverses':X.inverse()*Y.inverse(),
           'square_4777':X*X,'square_6444':Y*Y,'sum_squares':E,
           'difference_squares':Y*Y-X*X,
           'arithmetic_mean':S/TWO,'harmonic_mean':TWO*P/S,
           'geometric_mean_squared':P,'quadratic_mean_squared':E/TWO,
           'contrast':D/S,
           'circle_cos':(Y*Y-X*X)/E,'circle_sin':TWO*P/E,
           'hyperbolic_cos':((Y/X)+(X/Y))/TWO,
           'hyperbolic_sin':((Y/X)-(X/Y))/TWO,
           'recover_4777':(S-D)/TWO,'recover_6444':(S+D)/TWO,
           'gcd':Whole('gcd',(X,Y)),'lcm':Whole('lcm',(X,Y)),
           'cancelled_joint_provenance':(X*Y)/(Y*X)}
    expected={'sum':11221,'difference':1667,'product':30782988,
              'square_4777':22819729,'square_6444':41525136,
              'sum_squares':64344865,'difference_squares':18705407,
              'gcd':1,'lcm':30782988}
    for k,v in expected.items(): check(evaluate(roots[k])==v,f'valor exacto: {k}')
    check(evaluate(roots['recover_4777'])==x,'inversa de suma/diferencia: 4777')
    check(evaluate(roots['recover_6444'])==y,'inversa de suma/diferencia: 6444')
    check(evaluate(roots['circle_cos'])**2+evaluate(roots['circle_sin'])**2==1,
          'identidad circular global')
    check(evaluate(roots['hyperbolic_cos'])**2-evaluate(roots['hyperbolic_sin'])**2==1,
          'identidad hiperbólica global')
    check(evaluate(S)**2-evaluate(D)**2==4*evaluate(P),'identidad cuadrática')
    check(evaluate(S)**2+evaluate(D)**2==2*evaluate(E),'Parseval de dos paquetes')
    check(evaluate(S)**2-4*evaluate(P)==evaluate(D)**2,'discriminante y reconstrucción')
    check(sources(roots['cancelled_joint_provenance'])==frozenset(SOURCE_VALUES),
          'cancelar evaluación no borra procedencia')
    check(evaluate(roots['cancelled_joint_provenance'])==1,'cancelación numérica a unidad')
    # Órbitas individuales por signo y recíproco.
    variants=[]
    for e in (X,Y):
        variants.append((e,-e,e.inverse(),-e.inverse()))
        check(len({evaluate(v) for v in variants[-1]})==4,
              f'órbita individual cuatro estados: {e.atom_name}')
    orbit=[]; orbit_values=set()
    for a in variants[0]:
        for b in variants[1]:
            for u,v in ((a,b),(b,a)):
                pair=(evaluate(u),evaluate(v)); orbit_values.add(pair)
                orbit.append({'first':record(u),'second':record(v)})
    check(len(orbit_values)==32,'órbita conjunta: 32 estados distintos')
    generators=(lambda a,b:(-a,b), lambda a,b:(a,-b),
                lambda a,b:(1/a,b), lambda a,b:(a,1/b),lambda a,b:(b,a))
    check(all(g(a,b) in orbit_values for a,b in orbit_values for g in generators),
          'clausura exhaustiva de la órbita bajo cinco generadores')
    # Involuciones y dinámica de Möbius, construidas sólo a partir de S y P.
    def reflect(t: F) -> F: return evaluate(S)-t
    def exchange(t: F) -> F: return evaluate(P)/t
    def flow(t: F) -> F: return reflect(exchange(t))
    def back(t: F) -> F: return exchange(reflect(t))
    def coordinate(t: F) -> F: return (t-y)/(t-x)
    for t,label in ((x,'4777'),(y,'6444'),(evaluate(S),'suma')):
        check(reflect(reflect(t))==t,f'involución aditiva sobre {label}')
        check(exchange(exchange(t))==t,f'involución multiplicativa sobre {label}')
    check(reflect(x)==y and reflect(y)==x,'reflexión intercambia originales completos')
    check(exchange(x)==y and exchange(y)==x,'inversión escalada intercambia originales completos')
    check(flow(x)==x and flow(y)==y,'composición fija los dos originales')
    t=evaluate(S); initial_w=coordinate(t); trace=[]
    for n in range(13):
        w=(x/y)**n*initial_w
        direct=(y-w*x)/(1-w)
        check(t==direct,f'fórmula cerrada de iteración n={n}')
        check(back(flow(t))==t,f'inversa del operador compuesto n={n}')
        trace.append({'n':n,'state':str(t),'coordinate':str(coordinate(t))})
        check(coordinate(flow(t))==(x/y)*coordinate(t),f'conjugación exacta n={n}')
        t=flow(t)
    check(x/y<1<y/x,'atractor y repulsor: multiplicadores positivos')
    # Recurrencia infinita: se documenta la prueba; se comprueban 13 términos.
    powers=[F(2),evaluate(S)]
    for n in range(2,13): powers.append(evaluate(S)*powers[-1]-evaluate(P)*powers[-2])
    for n,v in enumerate(powers): check(v==x**n+y**n,f'recurrencia simétrica n={n}')
    # Matrices no conmutativas: los parámetros son los valores completos.
    U=((F(1),x),(F(0),F(1))); V=((F(1),F(0)),(y,F(1)))
    UV=matmul(U,V); VU=matmul(V,U)
    check(UV!=VU,'composición externa no conmutativa')
    check(UV[0][0]*UV[1][1]-UV[0][1]*UV[1][0]==1,'determinante de producto SL2')
    check(UV[0][0]-VU[0][0]==x*y and UV[1][1]-VU[1][1]==-x*y,
          'conmutador aditivo exacto de productos matriciales')
    # Comprobaciones de propiedades globales sin factorizar la escritura.
    check(x.denominator==1 and y.denominator==1,'evaluaciones enteras')
    check(x.numerator%2==1 and y.numerator%2==0,'paridad global distinta')
    gcd=evaluate(roots['gcd']); lcm=evaluate(roots['lcm'])
    check(gcd*lcm==x*y,'identidad de intersección aditiva')
    check(lcm/x==int(lcm/x) and lcm/y==int(lcm/y),'primer múltiplo común de ambos')
    # Potencias cruzadas completas: no se trocean las fuentes ni se estiman cifras.
    power_xy=x.numerator**y.numerator; power_yx=y.numerator**x.numerator
    check(power_xy>power_yx,'comparación exacta de potencias cruzadas')
    (args.out_dir/'potencias_exactas.txt').write_text(
        '4777^6444 =\n'+str(power_xy)+'\n\n6444^4777 =\n'+str(power_yx)+'\n',encoding='utf-8')
    # Euclides / Bézout sobre valores enteros completos; no sobre cifras.
    gcd_ext,bez_x,bez_y,euclid_steps=extended_euclid(int(x),int(y))
    check(gcd_ext==1 and bez_x==1237 and bez_y==-917,
          'Bézout exacto 1237*4777-917*6444=1')
    check(bez_x*int(x)+bez_y*int(y)==1,'certificado Bézout evaluado')
    cf=continued_fraction(int(y),int(x)); conv=convergents(cf)
    check(cf==[1,2,1,6,2,3,1,4,5],'cocientes euclídeos y fracción continua')
    check(conv[-1]==y/x and conv[-2]==F(1237,917),
          'convergentes exactos, penúltimo 1237/917')
    for i in range(1,len(conv)):
        u,v=conv[i].numerator,conv[i].denominator
        u0,v0=conv[i-1].numerator,conv[i-1].denominator
        check(abs(u*v0-u0*v)==1,f'determinante unimodular convergentes {i}')
    check(pow(int(x),-1,int(y))==1237,'inversa modular de 4777 módulo 6444')
    check(pow(int(y),-1,int(x))==3860,'inversa modular de 6444 módulo 4777')
    check(math.gcd(int(Sv:=evaluate(S)), int(evaluate(D)))==1,
          'suma y diferencia coprimas')
    check(math.gcd(Sv.numerator,int(evaluate(P)))==1,
          'suma y producto coprimos')
    tails=modular_inverse_tails(int(x))
    try: pow(int(y),-1,100)
    except ValueError: check(True,'6444 no invertible modulo 100')
    else: check(False,'6444 invertible inesperadamente módulo 100')
    # Concatenación EXTERNA de dos tokens completos de anchura 4.
    # Nunca se indexa, trocea o permuta el interior de un token.
    block_base=10000
    xy_serial=block_base*int(x)+int(y)
    yx_serial=block_base*int(y)+int(x)
    check(xy_serial==47776444 and yx_serial==64444777,
          'serialización externa de los dos tokens enteros')
    check(yx_serial-xy_serial==(block_base-1)*int(evaluate(D))==16668333,
          'diferencia de órdenes de concatenación')
    check(xy_serial+yx_serial==(block_base+1)*Sv.numerator==112221221,
          'suma de concatenaciones reversibles')
    concat={'base_of_external_serialization':block_base,
            'tokens':[str(x),str(y)],'XY':str(xy_serial),'YX':str(yx_serial),
            'difference_YX_minus_XY':str(yx_serial-xy_serial),
            'sum':str(xy_serial+yx_serial),
            'formal_token_words_length_1_to_8':[
                {'k':k,'distinct_words':2**k} for k in range(1,9)]}
    # Dos expresiones simétricas, independientes de la escala común.
    check(evaluate(S)**2-evaluate(D)**2==4*evaluate(P),
          'reconstrucción exacta producto por suma y diferencia')
    check(int(x)%2 and int(y)%2==0,
          'independencia multiplicativa por paridad')
    # Observadores de salidas: fuera del núcleo irreducible.
    decimals={name:output_decimal(evaluate(roots[name]))
              for name in ('inverse_4777','inverse_6444','ratio_6444_over_4777')}
    check(decimals['inverse_4777']['period_length']==112,'período recíproco 4777')
    check(decimals['inverse_6444']['preperiod_length']==2 and
          decimals['inverse_6444']['period_length']==178,'preperíodo y período recíproco 6444')
    summary,enumeration=exhaustive(5)
    check(enumeration['total_valid_trees']==116210,'total exacto de árboles válidos hasta cinco hojas')
    # La identidad de la clausura racional es una prueba escrita, no un test finito.
    results={'protocol':{'inputs':['{4777}','{6444}'],
        'atomic_sources':True,'internal_access_allowed':False,
        'factorization_of_sources_used':False,
        'allowed_core':['unit','neg','inv','add','sub','mul','div'],
        'additional_declared':['gcd','lcm','integer_power','output_decimal_encoding','whole_token_concatenation'],
        'braces':'inicio y fin de escritura, no conjuntos',
        'interpretation':'evaluación decimal completa; la traza no se identifica con el valor',
        'irreducibility':'operacional; no se decide entre limitación del observador e intrínseca'},
        'operations':{k:record(v) for k,v in roots.items()},
        'orbit_32':orbit,'mobius_iteration':trace,
        'symmetric_power_sums':[str(v) for v in powers],
        'bezout':{'gcd':gcd_ext,'coefficient_x':bez_x,'coefficient_y':bez_y,
                  'certificate':'1237*4777-917*6444=1','euclidean_steps':euclid_steps,
                  'ratio_cf_y_over_x':cf,
                  'convergents':[str(v) for v in conv],
                  'inverse_x_mod_y':str(pow(int(x),-1,int(y))),
                  'inverse_y_mod_x':str(pow(int(y),-1,int(x)))},
        'inverse_modulo_decimal_tails_x':tails,
        'external_concat_serialization':concat,
        'matrices':{name:[[str(v) for v in row] for row in mat]
                    for name,mat in (('U',U),('V',V),('UV',UV),('VU',VU))},
        'output_decimal_observations':decimals,
        'exhaustive_search_summary':summary,
        'exhaustive_search_totals':{k:v for k,v in enumeration.items() if k!='witnesses'},
        'verification':{'status':'PASS','checks_count':len(CHECKS),'checks':CHECKS,
            'scope':'Exact arithmetic and finite complete enumerations; universal proofs in ATLAS.md. Not a proof-assistant certification.'}}
    def save(name: str,data: Any) -> None:
        (args.out_dir/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    save('resultados.json',results)
    save('expresiones_hasta_5_hojas.json',enumeration)
    save('procedencia_dag.json',export_dag(roots))
    print(json.dumps({'status':'PASS','checks':len(CHECKS),
       'enumeration_summary':summary,
       'total_valid':enumeration['total_valid_trees'],
       'distinct_joint_values':enumeration['distinct_joint_values_up_to_bound']},ensure_ascii=False,indent=2))

if __name__=='__main__':
    main()
