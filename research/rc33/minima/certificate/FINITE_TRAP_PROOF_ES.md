# Certificados finitos de supervivencia a toda cardinalidad

Autor: Facundo Firmenich. RGΦ RC3.3. Aritmética exacta sobre Q.

Sea H=(1/2,1), T(x)={Bx} y S=ΦTΦ⁻¹, Φ(x)=1/(1+x). Definimos

    K0=H, K(d+1)=H ∩ T⁻¹(Kd) ∩ S⁻¹(Kd).

Cada conjunto alto cerrado bajo ambas acciones, finito o infinito, está
contenido en todos los Kd, por inducción. Los Kd decrecen. Son uniones finitas
de intervalos abiertos con extremos racionales. Para I=(l,u), sus preimágenes
se obtienen, para k=0,…,B−1, de

    T⁻¹(I): ((k+l)/B, (k+u)/B),
    S⁻¹(I): (Bl/[1+(B−1+k)l], Bu/[1+(B−1+k)u]),

intersectando con H. Los extremos se conservan abiertos: intervalos que se
tocan no se fusionan, pues el punto de contacto puede estar excluido.

En cada intervalo de Kd, d≥1, ambas ramas son continuas y sus dígitos son
constantes. Formamos dos grafos de transiciones posibles: I→J si la imagen
de I bajo la acción correspondiente corta J. Se eliminan iterativamente los
vértices que no tienen sucesor superviviente por alguna de las dos acciones.
Ningún punto de un conjunto alto cerrado puede ocupar un vértice eliminado:
su sucesor por cada acción debe ocupar otro vértice superviviente.

**Criterio.** Si el núcleo del grafo queda vacío, no existe ningún conjunto alto
cerrado. Si en el núcleo una de las dos letras tiene exactamente un sucesor
por intervalo, existe a lo sumo un punto superviviente por intervalo.

Para T, dos puntos que siguieran el mismo itinerario tendrían diferencias
multiplicadas por Bⁿ, mientras sus imágenes permanecen en H. Su diferencia es
por tanto cero. Para S se aplica lo mismo a Φ⁻¹(x), donde la dinámica es T.
El itinerario de intervalos es finalmente periódico porque el grafo es finito
y la transición elegida es determinista. Los dígitos dan un punto racional
explícito: una cola periódica de período k tiene valor

    (a0 B^(k−1)+…+a(k−1))/(B^k−1),

y se antepone después el prefijo. En la carta de S se aplica Φ al resultado.
Se descartan candidatos fuera del intervalo que los generó. De los puntos
restantes se elimina sucesivamente todo aquel cuya imagen T o S no figure en
el conjunto. Queda exactamente el conjunto de puntos cuyos futuros bajo
cualquier palabra permanecen altos: la inclusión superior procede del criterio;
la inferior, del cierre directo comprobado.

Sus componentes fuertemente conexos terminales son todos los componentes altos
cerrados del sistema, sin imponer cardinalidad ni altura racional. Sus mapas
se evalúan exactamente para determinar si son permutaciones. Un certificado
que sólo termina por límite de tiempo, profundidad o memoria no prueba exclusión.

## Contraste computacional

El generador usa preimágenes de intervalos y poda de grafos. El verificador
separado reconstruye cada Kd mediante todos sus puntos de corte y evalúa T,S
en cada celda racional; también controla los extremos. Reconstruye los puntos
periódicos mediante una fórmula cerrada, calcula de nuevo el cierre y compara
los componentes. No importa funciones del generador. Es una implementación
separada de comprobación exacta, no una revisión externa por terceros.

Los datos fijos indican explícitamente las bases verificadas. La prueba aplica
a toda cardinalidad en cada una de esas bases, no a bases fuera del registro.
