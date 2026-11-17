"""Export the exact approved standalone SVG sources and bilingual HTML viewers."""
from pathlib import Path
import shutil
import cairosvg

R=Path(__file__).resolve().parents[2]
assets=R/'research/rc33/recent/figure-assets'
out=R/'outputs/figures';out.mkdir(exist_ok=True,parents=True)
for p in sorted(assets.glob('*.svg')):shutil.copy2(p,out/p.name)
for ext in ['svg','png','pdf']:
    target=out/('graphical_abstract.'+ext);source=assets/'rc33_visual_EN.svg'
    if ext=='svg':shutil.copy2(source,target)
    elif ext=='png':cairosvg.svg2png(url=str(source),write_to=str(target),scale=1.8,background_color='#ffffff')
    else:cairosvg.svg2pdf(url=str(source),write_to=str(target),background_color='#ffffff')
for lang in ['EN','ES']:
    cairosvg.svg2png(url=str(assets/f'rc33_visual_{lang}.svg'),write_to=str(out/f'rc33_visual_{lang}.png'),scale=1.8,background_color='#ffffff')
    title='RGΦ RC3.3 — '+('Mapas y registros' if lang=='ES' else 'Maps and records')
    status_label='Estado de la investigación' if lang=='ES' else 'Research status'
    dependencies_label='Dependencias interactivas' if lang=='ES' else 'Interactive dependencies'
    captions=['Resumen visual','Mapa epistémico','Fase conjunta'] if lang=='ES' else ['Visual abstract','Epistemic map','Joint phase']
    items=''.join(f'<section><h2>{c}</h2><img alt="{c}" src="../figures/rc33_{n}_{lang}.svg"></section>' for n,c in zip(['visual','epistemic','coupled'],captions))
    page=f'<!doctype html><html lang="{lang.lower()}"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title><style>body{{max-width:1060px;margin:2rem auto;padding:0 1rem;background:#fafbfe;color:#16345e;font:17px/1.5 Georgia,serif}}h1,h2{{text-align:center}}a{{color:#315fa7}}section{{margin:2rem 0;padding:1.2rem;background:#f0f4fa;border:1px solid #829bc3;border-radius:10px}}img{{display:block;max-width:100%;height:auto;margin:auto}}</style><h1>{title}</h1><p><a href="../../RESEARCH_STATUS.md">{status_label}</a> · <a href="epistemic_graph.html">{dependencies_label}</a> · <a href="rc33_epistemic_{"ES" if lang=="EN" else "EN"}.html">{"Castellano" if lang=="EN" else "English"}</a></p>{items}</html>'
    (R/'outputs/interactive'/f'rc33_epistemic_{lang}.html').write_text(page)
print('PASS: canonical standalone figures and two bilingual HTML viewers')
