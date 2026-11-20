# Argüelles · El factor maya → RGΦ RC3.3

**Estado:** instrumental exacto (19 contratos internos, 11 tests), no claim de cierre global. Python ≥3.10, biblioteca estándar. **No contiene Marte.**

## Archivos

- `arguelles/loom_bridge.py`: figura de 52 Kin, 13 cuartetos, 60 intervalos; cinco castillos, ondas, armónicas, cromáticas; dualidad 261; CRT 260/64; cuadrado 8×8 de Benjamin Franklin; observación racional modular con ABSTAIN; ciclos finitos de multiplicación por base; números armónicos de El factor maya.
- `tests/test_loom_bridge.py`: once tests independientes; exhaustivos en 260 kins y rangos finitos declarados.
- `reports/LOOM_RC33_AUDIT.json`: certificado reproducible con la matriz y 13 cuartetos.

```bash
python -m unittest discover -s tests -v
python -m arguelles.audit --output reports/LOOM_RC33_AUDIT.json
```

## Anclaje en los tres repositorios

- **Radix principal:** `FacundoFirmenich/primitive-radix-mobius-dynamics`, `research/rc33` y `RESEARCH_STATUS.md`. Pauta de publicación: NO agregar artículo, suplemento, manuscritos ni PDF completo.
- **Kwantorithmics:** `FacundoFirmenich/Kwantorithmics_mayab_iching`, rama `Ulalito's-Island`, contiene ya A01..A28, motor chino de 64 hexagramas/384 yao y 7 bloques `606897/r3` hasta Q=20.000. El presente módulo B01..B19 añade propiedades *específicas* de El factor maya/Argüelles, no reemplaza las A01..A28.
- **Tarasutra:** `FacundoFirmenich/Tarasutra-cuantorithmics`, preservando T1/T2/LOGITS, datasets y hashes; se usa únicamente el testigo ya verificado en el repositorio principal.

## Gate matrix a 20-XI-2026

| Frontera | Apoyo de este módulo | Cierre global |
| --- | --- | --- |
| `606897/factor 3` | CRT, observadores parciales, auditorías de candidatos | NO |
| Unicidad de dos orientaciones realizadas | ensayo de nuevas huellas observacionales, preservación de testigo | NO |
| Base mínima con 5 estados | relojes finitos como ordenadores de exploración, nunca como filtro necesario no probado | NO |
| Base mínima cualquier cardinalidad | ninguna exclusión nueva; conservar cota certificada ≥54 | NO |
| Seis estados | extensión de etiquetas/fibras para test de arquitecturas | NO |

**Restricción de soundness:** ni ser un portal GAP ni el castillo ni el número de Franklin es condición necesaria de una solución diofántica RGΦ. El observador modular `p/q mod m` **ABSTAIN** si `gcd(q,m) ≠ 1`. Un sensor que no distingue dos estados no demuestra identidad aritmética. Si una partición de calendario no es congruencia para `T,S`, no se puede cocientar el monoide sin un testigo adicional. Toda exclusión requiere condición aritmética demostrada desde RC3.3.

## Procedencia y fronteras históricas

1. José Argüelles, *The Mayan Factor: Path Beyond Technology* (Bear & Company, 1987), cap. 4 y apéndices; libro en inglés: `https://files.spiritmaji.com/books/Jose%20Arguelles/The%20Mayan%20Factor%20Arguelles.pdf`; castellano: `https://maestrosdelsaber.com/wp-content/uploads/ftp-files/Culturas%20antiguas%20America/Mayas/Ame%20Arguelles%2C%20Jose%20-%20El%20factor%20maya%2C%20Mas%20alla%20de%20la%20tecnologia.pdf`.
2. Portal kin de 52 posiciones: `https://tzolkin.io/info/encantamento-do-sonho/portal-ativacao-galactica`. El esquema GAP/portal y la numerología de Argüelles **no** son testimonio de prácticas calendáricas mayas prehispánicas.
3. Franklin 8×8: `https://mathworld.wolfram.com/FranklinMagicSquare.html`, con aclaración de que el cuadrado es *semimágico* y sus diagonales rectas no son ambas 260.
4. Hunab Ku: N. Cruz Cortés, *Estudios de Cultura Maya* 53 (2019), DOI `10.19130/iifl.ecm.2019.53.960`. La cuestión historiográfica del teónimo es independiente del centro o eje matemático de la matriz.

Licencia y autoría del código nuevo: conservar las licencias y autoría definidas por el titular del repositorio destino; no se transcribe el texto ni el arte protegido del libro.