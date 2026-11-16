from pathlib import Path
import json,csv
from fractions import Fraction
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
ROOT=Path(__file__).resolve().parents[2]; OUT=ROOT/'outputs/figures'; OUT.mkdir(parents=True,exist_ok=True)
plt.rcParams.update({'font.size':10,'font.family':'DejaVu Sans','axes.linewidth':0.8,'figure.dpi':160,'savefig.dpi':240})

def save(fig,name):
    for ax in fig.axes:
        for patch in ax.patches:
            patch.set_edgecolor('#315FA7')
            if patch.get_fill(): patch.set_facecolor('#D4DEF2')
        for line in ax.lines: line.set_color('#315FA7')
        for spine in ax.spines.values(): spine.set_edgecolor('#9BAED0')
    for ext in ('svg','png','pdf'): fig.savefig(OUT/f'{name}.{ext}',bbox_inches='tight',transparent=False)
    for p in OUT.glob(name+'.svg'):
        p.write_text('\n'.join(line.rstrip() for line in p.read_text().splitlines())+'\n')
    plt.close(fig)

def box(ax,xy,w,h,text,lw=1.4):
    r=FancyBboxPatch(xy,w,h,boxstyle='round,pad=0.02,rounding_size=0.04',fill=False,lw=lw);ax.add_patch(r);ax.text(xy[0]+w/2,xy[1]+h/2,text,ha='center',va='center');return r

def arrow(ax,a,b,text=''):
    ax.add_patch(FancyArrowPatch(a,b,arrowstyle='-|>',mutation_scale=13,lw=1.2));
    if text: ax.text((a[0]+b[0])/2,(a[1]+b[1])/2+0.035,text,ha='center',va='bottom',fontsize=9)

def fig_object():
    fig,ax=plt.subplots(figsize=(10.5,3.6));ax.set_xlim(0,1);ax.set_ylim(0,1);ax.axis('off')
    box(ax,(.03,.31),.18,.36,'Reduced rational\n$x=p/q$')
    box(ax,(.29,.31),.20,.36,'Primitive ray\n$(p,q)$')
    box(ax,(.57,.31),.19,.36,'Branch matrix\n$M_k$, $\\det M_k=B$')
    box(ax,(.83,.31),.14,.36,"Normalize\n$M_k v = \\delta v'$")
    arrow(ax,(.21,.49),(.29,.49),'lift');arrow(ax,(.49,.49),(.57,.49),'choose branch');arrow(ax,(.76,.49),(.83,.49),'content')
    ax.text(.5,.88,'Primitive projective radix–Möbius dynamics',ha='center',fontsize=15,weight='bold')
    ax.text(.5,.12,r'$\delta_T=\gcd(q,B)$   ·   $\delta_S=\gcd(p,B)$   ·   content is retained as a multiplicative cocycle',ha='center')
    save(fig,'fig01_object_architecture')

def fig_threshold():
    fig,ax=plt.subplots(figsize=(9,4)); ns=[2,3,4,5]; vals=[1,1,1,0]; ax.bar(ns,vals,width=.62);ax.set_xticks(ns);ax.set_ylim(0,1.22);ax.set_yticks([0,1],['nonpermutation exists','permutation rigid']);ax.set_xlabel('cardinality of finite high closed SCC');ax.set_title('Sharp rigidity threshold')
    for n,v in zip(ns,vals): ax.text(n,v+.055 if v else .055,'rigid' if v else 'exact breakdown',ha='center',weight='bold')
    ax.axvline(4.5,ls='--',lw=1);ax.text(4.53,1.12,r'$n_{min}^{nonperm}=5$',ha='left')
    save(fig,'fig02_sharp_threshold')

def fig_counter():
    rows=list(csv.DictReader((ROOT/'certificates/STATES_AND_ACTIONS.csv').open())); Tm=[int(r['T_target']) for r in rows]; Sm=[int(r['S_target']) for r in rows]
    pos={0:(0,1),1:(1,1.25),2:(2,1),3:(2,.1),4:(.4,.05)}
    fig,ax=plt.subplots(figsize=(8.5,5.3));ax.set_aspect('equal');ax.axis('off');ax.set_xlim(-.4,2.5);ax.set_ylim(-.35,1.65)
    for i,r in enumerate(rows):
        x,y=pos[i];ax.add_patch(Circle((x,y),.12,fill=False,lw=2));ax.text(x,y+.01,f'$x_{i}$',ha='center',va='center',weight='bold');ax.text(x,y-.20,r['state'],ha='center',fontsize=9)
    for gen,m,rad in [('T',Tm,.18),('S',Sm,-.18)]:
        for i,j in enumerate(m):
            a=pos[i];b=pos[j]
            if i==j:
                ax.add_patch(FancyArrowPatch((a[0]+.07,a[1]+.09),(a[0]-.07,a[1]+.09),connectionstyle='arc3,rad=.8',arrowstyle='-|>',mutation_scale=12,lw=1.2))
                ax.text(a[0],a[1]+.29,gen,ha='center',fontsize=8)
            else:
                lw=2.8 if (gen=='S' and i==3 and j==0) else 1.1
                con='arc3,rad='+str(rad if i<j else -rad)
                ax.add_patch(FancyArrowPatch(a,b,connectionstyle=con,arrowstyle='-|>',mutation_scale=12,lw=lw,shrinkA=13,shrinkB=13))
                mx=(a[0]+b[0])/2;my=(a[1]+b[1])/2; lab='$S_3$' if (gen=='S' and i==3 and j==0) else gen
                ax.text(mx,my+(.10 if gen=='T' else -.10),lab,ha='center',fontsize=8,weight='bold' if '3' in lab else 'normal')
    ax.set_title('Exact five-state counterfamily: one strict content-loss edge',fontsize=14,weight='bold')
    ax.text(1,-.3,r'$B_t=88{,}011{,}536{,}665{,}779+t\,223{,}336{,}848{,}698{,}040$',ha='center')
    save(fig,'fig03_counterfamily_graph')

def fig_spectral():
    fig,ax=plt.subplots(figsize=(10,3.8));ax.axis('off');ax.set_xlim(0,1);ax.set_ylim(0,1)
    box(ax,(.04,.33),.18,.34,'primitive state\n$v_0$');box(ax,(.31,.33),.24,.34,'periodic word\n$w=g_m\\cdots g_1$');box(ax,(.64,.33),.30,.34,r'$M_w v_0=\Delta_w v_0$'+'\n'+r'$\det M_w=B^m$')
    arrow(ax,(.22,.50),(.31,.50),'iterate');arrow(ax,(.55,.50),(.64,.50),'multiply')
    ax.text(.5,.83,'Cycle spectrum from the content cocycle',ha='center',fontsize=14,weight='bold')
    ax.text(.5,.13,r'$\operatorname{tr}(M_w)=\Delta_w+B^m/\Delta_w$   ⇒   $\operatorname{tr}(M_w)^2-4B^m$ is a perfect square',ha='center')
    save(fig,'fig04_spectral_cycle')

def fig_abstract():
    fig,ax=plt.subplots(figsize=(13,5.2));ax.axis('off');ax.set_xlim(0,1);ax.set_ylim(0,1)
    ax.text(.5,.93,'Radix–Möbius Rigidity',ha='center',fontsize=19,weight='bold');ax.text(.5,.86,'primitive projective lift · content cocycle · sharp 4→5 threshold',ha='center',fontsize=11)
    box(ax,(.04,.36),.19,.30,r'$x=p/q$'+'\nradix–Möbius state');box(ax,(.29,.36),.20,.30,'primitive lattice ray\ncontent $\\delta$ retained');box(ax,(.55,.36),.18,.30,'cycle budget\n+ spectrum');box(ax,(.79,.36),.17,.30,'finite high SCCs')
    arrow(ax,(.23,.51),(.29,.51));arrow(ax,(.49,.51),(.55,.51));arrow(ax,(.73,.51),(.79,.51))
    ax.text(.26,.16,'n = 2, 3, 4',ha='center',fontsize=13,weight='bold');ax.text(.26,.09,'permutation rigid',ha='center')
    ax.text(.74,.16,'n = 5',ha='center',fontsize=13,weight='bold');ax.text(.74,.09,'exact nonpermutation family',ha='center')
    ax.annotate('',xy=(.62,.13),xytext=(.38,.13),arrowprops=dict(arrowstyle='-|>',lw=2));ax.text(.5,.19,r'sharp threshold $n_{min}=5$',ha='center',fontsize=11)
    save(fig,'graphical_abstract')

def main():
    fig_object();fig_threshold();fig_counter();fig_spectral();fig_abstract();print('figures=5 formats=svg,png,pdf PASS')
if __name__=='__main__': main()
