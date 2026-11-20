# Puente algebraico Tzolk'in 260 × Yijing 384 yao

El producto `Z/260 × Z/384` se descompone en exactamente **cuatro órbitas temporales** bajo la traslación diagonal `(1,1)`. Cada órbita tiene `mcm(260,384) = 24.960` elementos. Es compatible un par `(k,j)` si y solo si `j-(k-1) ≡ 0 (mod 4)`. Entre los 99.840 pares hay 24.960 compatibles con la fase del anclaje de referencia; no se inventan fases para los otros 74.880.

Codificación explícita y **convencional** de los 384 yao: hexagrama abstracto `h ∈ [1,64]`, línea `ℓ ∈ [1,6]`, índice `j = 64(ℓ-1)+(h-1)`. Se trata de una *enumeración* reversible moderna, no de Rey Wen, Fu Xi, Jing Fang ni Na Jia. La interpretación tradicional de líneas y gobernantes permanece en el motor chino existente del repositorio. El único acoplamiento es aritmético, no histórico.

**Contrato RGΦ:** el portador racional sólo puede proyectarse mediante inversión modular cuando su denominador reducido es coprimo con el módulo. El nuevo puente no postula que el Yijing, las 52 celdas GAP o las cinco particiones calendarias sean congruencias dinámicas para `S_B`, ni restricciones de existencia sobre las cinco fracciones primitivas.

Reproducción de cuatro tests exhaustivos incluidos: `python -m unittest discover -s tests -p 'test_iching_loom_coupler.py' -v`. La prueba recorre **las 24.960 fases** y verifica la inversa exacta. No contiene Marte ni observaciones físicas supuestas.