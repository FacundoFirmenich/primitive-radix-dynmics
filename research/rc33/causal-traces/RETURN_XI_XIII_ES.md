# Retorno RGΦ → Fronteras XI–XIII

17 de noviembre de2026. Fuente: maths-4777, commit a859725a3ef7c9e5890e48e7929340072752ecee. Revisión asistida en esta sesión; no revisión externa independiente.

Se contrastaron las pruebas y se reprodujeron independientemente2.097.151 reconstrucciones binarias,265.720 historias ternarias, los determinantes, el aniquilador entero16x16 y el certificado Apéry–CRT de4.777 residuos. Nueve archivos de prueba/código/resultados conservan sus SHA-256 publicados. No se atribuye aquí ejecución a las suites Python ni a los laboratorios en navegador.

**Aporte de retorno: seleccionar las sondas dentro del lenguaje admisible.** En RGΦ, las ramas dependen del estado y se componen por la izquierda. En toda la familia CRT conocida, cuatro sondas de longitud máxima dos reconstruyen el levantamiento2x2: vacía,T,S,TT desde los estados0–3; vacía,T,S,TS desde el estado4. RESULTS.md contiene los determinantes simbólicos y los inversores.

**Obstrucción al uso exclusivo de retornos.** Todos los ciclos basados en un racional comparten una dirección invariante. Sus trazas ven sólo dos caracteres diagonales. El Hankel de retornos tiene rango a lo sumo dos, exactamente dos en el testigo. TT y SS desde406/731 producen matrices distintas que ninguna traza de continuación cerrada distingue. Una T abierta sí lo hace.

**Nueva frontera finita cuantificada.** El Hankel de la serie de puntos fijos del monoide de36 transformaciones tiene rango11: menor de determinante−576 y factorización entera de la tabla completa. Todas sus consultas futuras por trazas distinguen30 acciones; dos grupos de cuatro acciones permanecen indistinguibles. Se separan así racional, levantamiento matricial, acción global sobre el conjunto finito e historia.

**Contrato esencial:** las sondas observan el levantamiento acumulado mediante registro causal u oráculo equivalente. No se deducen del racional final aislado. Dos antecedentes fusionados en un mismo estado siguen siendo indistinguibles mediante estados futuros solamente. Esto no sustituye el registrador óptimo anterior ni anula su cota.

El destino editorial es el companion junto a observabilidad y palabras, con certificados en el suplemento y un enlace breve en el main. El ejemplo aditivo de Frobenius y las cifras8888 se conservan como investigación y retorno: no imponen una nueva restricción sobre la realización diofántica. Las tríadas8888 y7444 son experimentos distintos.

El cierre global de RGΦ todavía requiere acotar o reducir uniformemente el índice de completación; la mínima base a cardinalidad arbitraria necesita además un control de cardinalidad. Las sondas y el rango11 no proporcionan por sí solos esa cota.

Reproducción: Node18+; make causal-trace-verify. Los PDF/HTML privados no pudieron reconstruirse: el entorno estaba indisponible. Las inserciones están pendientes y no se presentan como compiladas.
