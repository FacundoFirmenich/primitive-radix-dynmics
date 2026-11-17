# Retorno RGΦ → FST16

17 de noviembre de2026 · Revisión asistida de esta sesión, no revisión externa independiente.

La isometría es correcta para etiquetas admisibles: C=K0 es8mod9 y, por tanto, unidad módulo3. La prueba LTE da exactamente v3(v_j-v_k)=v3(j-k); las permutaciones de todos los cocientes finitos proporcionan la extensión biyectiva sobre Z3. La inversa analítica usa el logaritmo en1+9Z3 y un denominador de valoración dos.

**Precisión que conviene añadir al canon:** observar el valor v_j módulo3^t equivale a observar K_j módulo3^(t+2), no módulo3^t. Es el mismo desplazamiento de dos niveles que exige el factor nueve del teorema previo del módulo efectivo. El motor verifica ambos canales por separado.

**Generalización con una excepción estructural:** para borrar un primo p!=3, poner q=p^ord9(p), s=v3(q-1). Entonces v3(v_j-v_k)=s-2+v3(j-k). Sólo s=2 da una isometría sobre todo Z3. Si s>2, la imagen es un coset de3^(s-2)Z3. Los primos109 y163 dan desplazamientos1 y2. Por tanto, la extensión a todos los primos debe declarar ese parámetro y la condición de compatibilidad del coset.

La reconstrucción independiente, con h=C=8, longitud10000, prefijo/sufijo88 y rango3000, obtiene3944,986,110,2,1 candidatos al añadir los módulos9,729,2187. La clase final es3000mod8748 y la elevación ternaria hace21 pruebas. Sin sufijo,3^8 basta uniformemente. El DFA que empieza por88 acepta3944 de3945 candidatos y visita21 nodos. Los parámetros omitidos en el mensaje se han reconstruido explícitamente; no se presenta este cálculo como recuperación del JSON original.

Se añadieron pruebas exactas de15.840 pares de valoración,10.920 valores residuales,1.620 inversiones,15.450 consultas conjuntas,6.240 casos DFA y6.612 cotas de anchura, entre otros controles. La poda utiliza una pila y no impone un límite de recursión Python a palabras largas. La prueba vale para cualquier DFA completo; no garantiza coste sublineal para todos ellos.

El código nuevo se apoya en el FST14 preservado y su adaptador declarado. No recibimos el ZIP/PDF/motores/atlas FST15/16 ni sus15/12/12 suites. No se atribuyen esas ejecuciones a este turno. El programa independiente, los parámetros y sus hashes acompañan este anexo.

En RGΦ el resultado se incorpora al apéndice de observación del companion y al contrato de evidencias del suplemento. Es una mejora exacta del inversor de palabras; todavía no establece una parametrización exponencial del índice diofántico de los portadores. La cota uniforme de ese índice sigue siendo una obligación distinta.

Reproducir: make fst16-check en A1, o python replay.py --output /tmp/fst16-return en el módulo portátil. Los resultados actuales y la reconstrucción de los seis documentos constan en el recibo final de la entrega.
