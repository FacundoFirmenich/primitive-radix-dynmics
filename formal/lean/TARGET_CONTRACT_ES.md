# Contrato de formalización Lean — RGΦ RC3.3

Autor: Facundo Firmenich. Inicio: 20 de noviembre de 2026.
Base pública: f7aaf02942757fd8b60ec4283b75448aa3a7c088.

El objetivo es obtener pruebas verificadas por Lean 4, con Mathlib fijada por
revisión, de resultados de los manuscritos actuales. Una prueba de un lema
auxiliar no se presentará como formalización de todo el artículo.

## Condiciones de aceptación

- Definiciones explícitas de los mapas racionales, del intervalo alto y de las
  hipótesis de primitividad, cierre y conectividad utilizadas.
- Pruebas completas, sin `sorry`, `admit`, axiomas locales ni descarga de una
  obligación matemática en un fichero JSON o un resultado Python.
- No usar `native_decide`: el cálculo de casos concretos debe producir términos
  comprobables por el núcleo de Lean.
- Auditar las dependencias axiomáticas de los teoremas públicos y registrar las
  versiones, entradas, comandos, salidas y hashes efectivos.
- Distinguir los axiomas lógicos habituales de Lean/Mathlib de un axioma que
  afirmase el resultado que se quiere demostrar.
- Confrontar cada resultado con el enunciado del manuscrito, incluyendo sus
  cuantificadores, cuerpos de coeficientes y condiciones de no anulación.

## Rutas del primer bloque

1. **Aritmética primitiva.** Formalizar las identidades de mcd de ambas ramas,
   el levantamiento integral y las identidades matriciales del cociclo.
   El primer control es que la primitividad y los extremos abiertos se usan
   realmente y no se sustituyen por hipótesis que ya contengan la conclusión.
2. **Ciclos.** Formalizar el balance telescópico para caminos y ciclos y sus
   consecuencias elementales. La obligación es enlazar las dos coordenadas y
   las etiquetas; no basta con asumir la identidad de balance.
3. **Realización.** Comprobar dentro de Lean las diez aristas de los portadores
   conocidos, sus cinco estados altos y distintos y la conectividad. Vincular
   los mapas efectivos con el autómata, en vez de certificar únicamente el grafo
   abstracto. La no inyectividad debe quedar demostrada sobre esos mismos mapas.

Las rutas de búsqueda aritmética ya activas no se modifican. Las preguntas
globales de existencia, unicidad y mínimos conservan su estado abierto.

## Frontera explícita

El teorema de exclusión de cuatro estados, las 37 exclusiones simbólicas, los
certificados de 52 bases, los 117093402 pares del prefijo de índice y los
resultados espectrales/observacionales del artículo complementario sólo podrán
marcarse como formalizados cuando tengan su propia prueba Lean completa.
La compilación de archivos auxiliares no cierra esas obligaciones.
