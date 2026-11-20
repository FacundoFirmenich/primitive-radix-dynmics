# Verificación Lean · dinámica radix–Möbius primitiva · RC3.3

Autor: **Facundo Firmenich**.

La entrega contiene una formalización parcial, ejecutable, con Lean 4.19.0 y
la revisión exacta de Mathlib indicada en `lake-manifest.json`. Las144
proposiciones auxiliares y principales pertenecen a 17 módulos. La cuenta de
proposiciones mide cobertura del desarrollo formal; no 144 descubrimientos.

```sh
lake build
python3 scripts/audit.py
```

El primer comando puede necesitar descargar dependencias. Si la caché oficial
no está disponible, Lake compila sus fuentes. El paquete conserva las fuentes,
las revisiones y el auditor; no incluye el compilador ni `.lake`.
Puede seleccionarse un Lake ya instalado con `--lake /ruta/a/lake`.

El auditor imprime las entradas exactas, recompila, enumera las hipótesis de
cada enunciado y consulta sus axiomas mediante `#print axioms` y `--trust=0`.
Siete parejas de control comprueban que Lean rechaza afirmaciones falsas y
acepta sus negaciones. Los archivos deliberadamente falsos se guardan aparte
y no se importan en la biblioteca. No se usan pruebas incompletas, axiomas
propios ni `native_decide`. Los únicos axiomas transitivos admitidos son los
estándar `propext`, `Classical.choice` y `Quot.sound`.

Se formalizaron los mapas racionales originales y su representación primitiva,
los defectos locales, el balance de ciclos, el levantamiento integral y su
identidad espectral, las dos familias infinitas de portadores de cinco estados,
sus 36 acciones de rango mínimo dos y la seguridad de la criba cuadrática.
La criba incluye sus ramas degeneradas y no presupone que el coeficiente de
la ecuación lineal sea siempre no nulo.

La exclusión general de cuatro estados sigue pendiente de formalización.
Tampoco se certifican aquí el agotamiento externo de índices, las 37
exclusiones, la unicidad global, los mínimos globales ni la existencia de 606897.
`COVERAGE.json` distingue todos esos alcances. La revisión semántica es una
autorrevisión explícita; la comprobación de los términos de prueba la realiza
el núcleo de Lean. El DOI anterior y su depósito permanecen inalterados.
