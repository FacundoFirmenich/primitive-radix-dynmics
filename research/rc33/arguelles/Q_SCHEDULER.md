# RGΦ RC3.3 · Planificador MAYAB sin pérdidas sobre el parámetro Q

**Propósito:** dividir campañas aritméticas reales en bloques paralelizables con certificado de cobertura y sin convertir los castillos, GAP o hexagramas en criterios diofánticos.

- Los **cinco castillos de 52** son exactamente los cinco bloques de clases de restos de `Q mod 260`. La asignación es `kin=1+(Q mod260)`, `castle=1+floor((kin-1)/52)`.
- Para cada resto `r`, el primer `Q >= lo` congruente es `lo+(r-lo)%260`, y el número de elementos hasta `hi` se calcula por cociente entero. Al distribuir 260 restos una sola vez, los cinco carriles son disjuntos y cubren cualquier intervalo entero finito.
- La categorización de los **52 portal kin** frente a los 208 restantes es una partición puramente instrumental, nunca un criterio de aceptación/rechazo de portadores primitivos.
- Cada `Q` tiene además una fase conjunta de los relojes 260/384, recuperable mediante CRT y codificada con el índice 384-yao convencionado; no afecta a las diez transiciones aritméticas de RGΦ.

**Comprobación de cobertura** (`reports/RC33_LOSSLESS_Q_SCHEDULER.json`):

| Rango de Q | Total | Castillo 1 | 2 | 3 | 4 | 5 | GAP / no GAP | Solver nuevo |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| 2–20.000 | 19.999 | 4.002 | 4.004 | 4.004 | 4.004 | 3.985 | 4.002 / 15.997 | No; sólo replay del plan |
| 20.001–22.000 | 2.000 | 416 | 416 | 416 | 369 | 383 | 401 / 1.599 | No; plan prospectivo |

**Estado:** 20 pruebas Python locales aprobadas, incluyendo exhaustividad de conteos de restos y disjunción de los cinco carriles. No existe en este módulo prueba nueva de no existencia global para 606897/r3 ni extensión de la exclusión del solver más allá de Q=20.000. Lo que el programa certifica es el plan, no la realización del trabajo futuro.

Reproducir:
```bash
python -m unittest discover -s tests -p test_partition_scheduler.py -v
python -c "from arguelles.partition_scheduler import verify_castle_plan; assert verify_castle_plan(20001,22000)['coverage_exact']"
```