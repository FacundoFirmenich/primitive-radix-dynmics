# Completamiento conjunto de coordenadas opuestas

Autor: Facundo Firmenich. RC3.3. Coeficientes exactos en Z y Q,
sin interpretación probabilística de los recuentos.

## Proposición

Fijemos r=2 o 3 y la cámara normal, o r=3 y la cámara reflejada. Las
condiciones del núcleo, en orden común (A,C,D,Q), son

    A | D²-r²Q²,   C | D²-Q²,
    D | C²-r²A²,   Q | C²-A².

Si se fijan D,Q, los valores posibles de A,C pertenecen a los conjuntos
de divisores positivos de |D²-r²Q²| y |D²-Q²|. Las dos condiciones
restantes se cumplen exactamente cuando coinciden las etiquetas

    h_A(A)=(r²A² mod D, A² mod Q),
    h_C(C)=(C² mod D, C² mod Q).

Si se fijan A,C, los valores posibles de D,Q dividen
|C²-r²A²| y |C²-A²|. Las otras dos condiciones equivalen a

    h_D(D)=(D² mod A, D² mod C),
    h_Q(Q)=(r²Q² mod A, Q² mod C).

La prueba es la definición de congruencia en cada coordenada. Las listas
de divisores son completas por sus factorizaciones certificadas. Los
numeradores no son cero en las cámaras utilizadas. Después de emparejar
las etiquetas se conservan las condiciones primitivas y las
intersecciones opuestas de módulos; sólo entonces se prueba E, el CRT y
las diez aristas.

Para la cámara reflejada, las cotas son

- D,Q fijados: Q<A<2D/3 y D<C<2Q.
- A,C fijados: 3A/2<D<C y C/2<Q<A.

Son restricciones propias de la cámara, no cortes de búsqueda añadidos.
Para la cámara normal se usan proyecciones que contienen la cámara
completa y se verifica después la desigualdad completa. Se retienen las
potencias primas enteras; el emparejamiento no presupone que las raíces
módulo potencias de dos sean sólo los signos uniformes.

## Por qué los cambios simultáneos pueden ser necesarios

El control construido
(A,C,D,Q)=(376,637,1265,731), r=3, pertenece a la cámara normal y cumple
las condiciones de coprimalidad. El portador conocido tiene
(406,712,1265,731).

Cambiar primero A produce gcd(406,637)=7, que no divide r-1=2.
Cambiar primero C produce gcd(376,712)=8, que tampoco divide dos.
Cambiar simultáneamente A,C alcanza el núcleo válido. Es un ejemplo
exacto de que los dos órdenes directos de cambios aislados fallan aunque
la modificación conjunta sea admisible. No demuestra que todos los
caminos más largos estén bloqueados ni que sea la causa de la ausencia
de testigos de 606897.

## Certificados y alcance

El generador conjunto se contrasta con una enumeración independiente de
enteros en 1536 contextos pequeños, y recupera los dos portadores
conocidos al ocultar cualquiera de sus dos parejas opuestas.

La instantánea PAIR_CONTEXTS_SNAPSHOT.jsonl fija 128058 contextos de la
cámara reflejada procedentes de 96127 vértices del explorador previo que
cumplían al menos dos condiciones cuadráticas. La ejecución agota sus
completamientos: 138985 parejas candidatas después de las puertas
individuales; seis coincidencias en un residuo, cuatro en el otro y
ninguna coincidencia conjunta. No aparece un núcleo cuadrático. Es una
exclusión de esas fibras explícitas, no una clasificación global ni una
prueba de generación completa de los candidatos originales.

El explorador posterior deduplica los contextos, conserva sus resultados
completos y los alimenta con nuevas salidas de los Tarasutras y del
explorador de una coordenada. Las realizaciones conocidas se registran
como controles, no como descubrimientos nuevos. Las factorizaciones no
certificadas se conservan como diferidas.
