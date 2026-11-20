# Auditoría semántica de la formalización · RC3.3

Autor: Facundo Firmenich. Fecha:20 de noviembre de2026.

**Dictamen principal: demostrado tal como está enunciado en las seis tarjetas
LEAN1–LEAN6, con el alcance literal de COVERAGE.json.** La formalización del
teorema completo del umbral sigue incompleta: falta la exclusión general de
cuatro estados. Este dictamen semántico es una autorrevisión; el núcleo de Lean
comprueba por separado los términos de prueba.

## Objetos y correspondencia

`Definitions.lean` define sobre Q exactamente T_B(x)=Bx−floor(Bx),
Phi(x)=1/(1+x), PhiInv(x)=(1−x)/x y S_B=Phi∘T_B∘PhiInv.
`High` exige1/2<x<1. Los inversos de carta incorporan las condiciones de no
anulación necesarias; no se afirma una inversa global donde un denominador
se anula. `FractionBridge.lean` prueba las fórmulas con resto y reducción;
`CanonicalRepresentation.lean` demuestra que todo racional alto tiene las
coordenadas primitivas usadas y que las transiciones se transportan exactamente.
No se sustituye una trayectoria racional por un grafo sin comprobar ese enlace.

`HighComponent` exige B>=2, pertenencia de todos los estados al intervalo,
cierre simultáneo y accesibilidad entre todos los pares por palabras. En las
realizaciones se demuestra además cardinalidad cinco y no inyectividad de S
sobre el propio conjunto. La clausura hace que los caminos intermedios
permanezcan en él. No se confunde no inyectividad global de S con la restricción.

## Dependencias esenciales

1. Definición racional -> fórmulas primitivas -> identidades de mcd -> defectos.
2. Conservación de numerador/denominador -> telescopado -> balance de dos cartas.
3. Cociente alto menor que dos -> presupuesto por número de letras -> exclusión
   de ciclos estrictos de longitud<= 3 y de la palabra T^a S^b mostrada.
4. Matrices de rama con dígitos enteros reales -> levantamiento de cada arista ->
   producto cronológico M_(n-1)...M_0 -> vector propio integral y espectro.
5. Diez aristas exactas y cinco fracciones distintas -> componente; divisibilidad
   del período por todas las coordenadas -> familias B0+tM para todo t>=0.
6. Tabla de 36 códigos distintos + palabras generadoras + cierre por ambas letras
   -> clasificación de palabras de cualquier longitud -> rango mínimo dos.
   El enlace fiel devuelve este resultado a los dos portadores racionales.
7. Las dos cónicas originales y q!=0 -> relación lineal -> cuadrática ->
   discriminante W²Z -> cuadratura entera de Z -> seguridad del rechazo modular.
   W=0,U!=0 se trata mediante la otra cuadrática; W=U=0 fuerzaV=0 y Z=0.

Las hojas externas son resultados formales de la revisión fijada de Mathlib,
no referencias bibliográficas asumidas como axiomas. La tabla finita se propone
como dato y se demuestra con `decide`; no se acepta la salida de Python como
premisa ni se emplea `native_decide`.

## Obligaciones y veredicto local

| Obligación | Estado | Evidencia |
| --- | --- | --- |
| Dominio alto y extremos abiertos | pasada | equivalencia con coordenadas; dos controles negativos |
| División natural sin truncar indebidamente | pasada | condición p<=q explícita en la carta S |
| Primitividad en las leyes de defecto | pasada | hipótesis explícita; contraejemplo al retirarla |
| Orden de composición | pasada | definiciones cronológicas y lema de concatenación |
| Todas las palabras del monoide | pasada | inducción desde el cierre, generación de cada entrada |
| Ambas familias infinitas | pasada | cuantificador t:Nat; mapas racionales y defectos |
| Casos degenerados del filtro | pasada | partición W=0/U=0; guardia al cancelar cuadrados |
| Axiomas transitivos | pasada si AUDIT.json=PASS | sólo los tres axiomas estándar registrados |
| Agotamiento de una búsqueda externa | fuera de alcance | no se importa ningún contador de ejecución |
| Exclusión de cuatro estados | no abordada por completo | falta el paso global del grafo y su congruencia excepcional |
| Mínimos o unicidad global | fuera de alcance | preguntas abiertas; no se añaden supuestos que las cierren |

## Control adversarial y límites

El auditor rechaza siete mutaciones falsas y prueba sus negaciones con los
mismos imports. Comprueba una base desplazada, retirada de primitividad,
sustracción natural fuera del dominio, cancelación de un factor cuadrado nulo,
ambos extremos del intervalo y truncado de la tabla del monoide. Los archivos
falsos quedan sólo en la carpeta de pruebas negativas.

`records/current/statements.log` contiene los tipos completos, con todos sus
cuantificadores. `axioms.log` conserva las dependencias transitivas.
`AUDIT.json` registra comandos, códigos de salida, revisiones de dependencias
sin cambios rastreados y hashes de las fuentes y objetos del proyecto. Las
etiquetas PASS se apoyan en esos registros, no sustituyen su reproducción.

El filtro demostrado es condición necesaria, no suficiente para una realización.
La periodicidad de las dos familias es suficiente; no se formaliza aquí que el
período sea mínimo ni la necesidad completa del sistema CRT. La cota por letras
no se presenta como la cota más fina por bloques del artículo. Un ciclo corto
no equivale a un componente con pocos estados sin el argumento adicional del
grafo. Estos límites impiden atribuir a este bloque la prueba formal completa
del umbral, de la clasificación o de los censos.

Siguiente obligación prioritaria: formalizar la reducción de un componente
no permutacional de hasta cuatro estados al ciclo alternante, y la obstrucción
congruencial que impide completarlo. El objetivo se añadirá como nuevo módulo
sólo cuando su demostración pase sin axiomas adicionales.
