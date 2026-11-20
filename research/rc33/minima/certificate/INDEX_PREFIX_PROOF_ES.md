# Recorrido exacto de índices: unicidad y coste de base

Autor: Facundo Firmenich. RGΦ RC3.3.

Se conserva la reducción ya demostrada a un número finito de planos y de
niveles enteros K,J para cada índice λ. El programa fija por escrito cada
plano y las cajas completas de niveles. Su geometría no añade cortes de altura.
Una unidad estricta r impide índices con gcd(r,λ)>1, porque λ divide E.

En un plano, sean

    u(s²−1)+vsq+wq²=Kq,
    P(1−s²)+hq+zq²=Jsq,
    U=Pw+uz, V=uh−PK, W=uJ−Pv.

La eliminación da Ws=Uq+V. Sus coeficientes cuadráticos son

    α=uU²+vUW+wW²,
    β=2uUV+vVW−KW²,
    γ=u(V²−W²).

La identidad exacta del nuevo instrumento es

    β²−4αγ = W² Z,
    Z=(v²−4uw)V²−2K(2uU+vW)V+K²W²+4uα.

Con W≠0, una raíz racional obliga a que Z sea un cuadrado entero. Con W=0,
q=−V/U y Z es también el numerador del discriminante de la cuadrática restante,
con denominador cuadrado U². Se mantiene este caso, así como las cuadráticas
degeneradas de grado uno, en el reconstructor racional.

El motor C++/GMP recorre toda la caja, rechaza exclusivamente restos no cuadrados
módulo 16,7,11,13,17,19,23 y calcula las raíces enteras exactas de los restantes.
Cada pareja superviviente pasa al reconstructor racional, que comprueba cámara,
primitividad, cuatro condiciones cuadráticas, índice real, quinta coordenada,
CRT y las diez aristas con sus defectos.

La identidad se verificó simbólicamente; el filtro se contrastó en 44.100 pares
con coeficientes de ambos signos frente a enteros Python sin esa criba. Dos
controles de nueve parejas recuperan los portadores conocidos de índices 557
y 140383. El registro 1..3 coincide al reiniciar después de 2 y al ejecutarlo
sin interrupción, salvo las fechas de terminación. La referencia racional previa
se reejecuta por separado para contrastar los primeros estratos.

El certificado fijo 1..12 agota 117093402 pares de niveles y no deja candidatos
del sistema necesario. Abarca todas las alturas dentro de las cinco cámaras
clasificadas. No afirma unicidad global ni mínimo de base: ambos exigirían
cubrir el dominio restante pertinente.

El explorador conserva dos objetivos. Un portador nuevo del mismo tipo ataca
unicidad incluso si su base es enorme. Para el mínimo a cinco estados se compara
la menor base de su fibra con B*=88011536665779. Sus cotas de altura e índice
sólo restringen este segundo objetivo. No se aplican a la búsqueda de unicidad.
