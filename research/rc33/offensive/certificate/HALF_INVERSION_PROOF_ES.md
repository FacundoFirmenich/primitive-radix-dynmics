# Inversión media, bit de rama y transferencia entre las dos formas

Autor: Facundo Firmenich. RC3.3. Continuación de 20 de noviembre de 2026.
Revisión: autorrevisión matemática; no revisión externa independiente.
La existencia de 606897/factor 3 sigue abierta.

## Identidades y condición necesaria y suficiente

Todo es adimensional. Sean B>=2 entero, H=(1/2,1),
T_B(x)={Bx}, S_B(x)=1/(1+{B(1/x-1)}) y
Psi(x)=1/(2x). Psi es una involución de H sobre H.
Pongamos epsilon_B(x)=floor(B/x) mod 2.

Para todo x en H se tiene exactamente

    T_B(Psi(x)) = Psi(S_B(x)) - (1-epsilon_B(x))/2.

Si además T_B(x) pertenece a H, entonces

    S_B(Psi(x)) = Psi(T_B(x)).

Prueba: escribir B/x=m+u, m entero y 0<=u<1. Entonces
{B/(2x)}=(epsilon_B(x)+u)/2 y Psi(S_B(x))=(1+u)/2.
Para la segunda identidad, {B(2x-1)}={2Bx}; cuando {Bx}>1/2,
1+{2Bx}=2{Bx}.

En consecuencia, si F es un componente alto, Psi(F) es cerrado bajo ambos
mapas exactamente cuando epsilon_B(x)=1 para todos sus estados. Cuando se
cumple, se intercambian T y S y se conserva la conectividad fuerte. Si
epsilon_B(x)=0, la imagen T_B(Psi(x)) cae en (0,1/2): la falta de cierre
consiste en un desplazamiento exacto de media unidad.

## Contenido y paridad de denominadores

Supongamos B impar y que F es fuertemente conexo. Si Psi(F) es también
cerrado, los denominadores reducidos de F tienen todos la misma paridad.

Para verlo, K=[[0,1],[2,0]] lleva el vector primitivo v_x=(p,q) a
t_x v_(Psi(x)), donde t_x=gcd(q,2) es 1 o 2. Cuando las dos identidades
son ramas genuinas de T y S, K conjuga sus matrices y los defectos cumplen

    delta'_e = delta_e t_destino/t_origen.

Todos los defectos son impares porque B es impar. Un cambio de t=2 a t=1
haría no entero al defecto nuevo. La conectividad fuerte impide coexistir
a ambas clases. Si t es constante, los defectos se conservan exactamente.

**Denominadores pares.** Si un componente alto finito tiene todos sus
denominadores pares, su base es impar: una base par eliminaría
sucesivamente los factores dos de cualquier denominador bajo iteraciones
de T, contradiciendo el cierre. Sus numeradores son impares. Para una
rama S con dígito b=floor(B(q-p)/p), el denominador antes de reducir es
Bq-(B-1+b)p; como el denominador de llegada es par y el defecto es impar,
b es par. Así epsilon_B=B+b es impar en todos los estados. Por tanto
Psi siempre produce otro componente alto con los generadores
intercambiados y los mismos defectos.

**Coordenadas ambas impares.** A base impar, si todos los numeradores y
denominadores reducidos son impares, la misma ecuación de la rama S
obliga a que b sea par. También en este caso Psi es admisible y conserva
los defectos.

La condición no se omite: con B=41, F={3/4,3/5} es un componente
permutacional de dos estados, pero Psi(F)={2/3,5/6} tiene imágenes bajo T
iguales a 1/3 y 1/6, fuera de H.

## La quinta coordenada determina una obstrucción de rama

En la forma normal de 119772 usamos
(A/Q,C/Q,C/D,rA/D,A/E), D=rE-jA, y los mapas
T=(1,0,3,2,4), S=(4,2,1,0,0). Denotemos por b_3,b_4 los dígitos de S
en las fuentes 3 y 4. La arista estricta y la ordinaria dan

    BD-rA(B-1+b_3)=rQ,
    BE-A(B-1+b_4)=Q.

Restar r veces la segunda igualdad a la primera demuestra

    r(b_4-b_3)=jB.

En r=3, j=1, la base es B=3 mod 6 por la obstrucción de paridad ya
probada para D=3E-A. Luego b_4-b_3=B/3 es impar. Los dos bits de rama
correspondientes son opuestos y Psi no puede intercambiar los generadores
en todo el componente. Es una obstrucción al cambio de carta, no a la
existencia del portador original.

En j=2 desaparece esta obstrucción concreta, porque 2B/3 es par. Esto es
necesario, pero no garantiza por sí solo todos los bits epsilon=1.

## Transferencia constructiva al frente 606897

Si una realización normal con r=3 pasa el criterio de Psi, necesariamente
pertenece a j=2. Hay dos transformaciones de sus coordenadas comunes:

- Si Q,D,E son pares: (A,C,D,Q,E) -> (A,C,D/2,Q/2,E/2).
- Si Q,D,E son impares: (A,C,D,Q,E) -> (2A,2C,D,Q,E).

En cada caso la nueva relación es D'=3E'-A', la cámara es
3A'/2<D'<C'<2Q'<2A' y las cinco fracciones son
(Q'/A',Q'/C',D'/C',D'/(3A'),E'/A'). Las letras quedan intercambiadas y
el único defecto tres pasa a T desde la fuente 3: es la orientación
606897. La implementación vuelve a comprobar el CRT y las diez aristas.

En particular, una realización normal de factor tres con todas las
coordenadas A,C,D,Q,E impares proporciona una realización de 606897:
su rama es j=2 por paridad y se elige una base impar de su fibra CRT,
cuyo módulo es impar. El criterio anterior hace admisible a Psi.
Toda realización normal de factor tres en una base par tiene esas
coordenadas impares, porque sus defectos 1 o 3 son impares. Por ello,
cualquier tal realización en base par también produciría un testigo de
606897 en una base impar de su misma fibra original.

Esto es una reducción de existencia y una nueva ruta de búsqueda. No se
afirma que se haya encontrado una realización en esa subrama.

## Decidir todos los levantamientos de base

Para una tupla ya realizada en B=b0 mod L, L es múltiplo de todos sus
numeradores. Los bits epsilon tienen período 2L en B. Basta examinar b0 y
b0+L, con representantes >=2. Las bases admisibles para Psi son ninguna
clase, una clase módulo 2L, o toda la clase original módulo L. No hay
búsqueda no acotada de bases en este paso.

## Controles

test_duality.py verifica las identidades con 8400 pares racional/base y
4095 instancias de la identidad restringida al intervalo alto. Incluye
componentes positivos {3/4} en base 13 y {5/8,7/8} en base 211, su dual,
y el control negativo mixto de base 41. Los dos portadores conocidos se
conservan como realizaciones; fallan únicamente el ensayo de cambio de
carta. No hay un control positivo no permutacional j=2 porque esa
existencia es precisamente la ruta todavía abierta.
