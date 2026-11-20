#include <gmpxx.h>
#include <iostream>
#include <vector>
#include <string>
#include <cstdint>
#include <stdexcept>
using Z=mpz_class;
static_assert(sizeof(long)>=8,"64-bit long required");
int md(const Z&x,int p){Z a=x%p;if(a<0)a+=p;return a.get_si();}
int main(){
 Z u,v,w,P,h,z; long kl,ku,jl,ju;
 if(!(std::cin>>u>>v>>w>>P>>h>>z>>kl>>ku>>jl>>ju))return 2;
 Z U=P*w+u*z; if(U==0)throw std::runtime_error("unhandled U=0");
 std::vector<int> mods={16,7,11,13,17,19,23};
 std::vector<std::vector<unsigned char>> masks;
 for(int p:mods){std::vector<unsigned char> sq(p),tab(p*p);for(int t=0;t<p;t++)sq[t*t%p]=1;
  int uu=md(u,p),vv=md(v,p),ww=md(w,p),pp=md(P,p),hh=md(h,p),UU=md(U,p);
  for(int k=0;k<p;k++)for(int j=0;j<p;j++){
   long V=(uu*hh-pp*k)%p,W=(uu*j-pp*vv)%p;
   long a=(1LL*k*k+4LL*uu*ww)%p,b=(-2LL*k*vv*V+4LL*uu*vv*UU)%p;
   long c=((1LL*vv*vv-4LL*uu*ww)*V*V-4LL*uu*k*UU*V+4LL*uu*uu*UU*UU)%p;
   long q=(a*W*W+b*W+c)%p;if(q<0)q+=p;tab[k*p+j]=sq[q];
  }masks.push_back(tab);
 }
 unsigned long pairs=0,filtered=0,exact=0,hits=0;
 for(long k=kl;k<ku;k++){
  Z V=u*h-P*k;
  Z a=Z(k)*k+4*u*w,b=-2*Z(k)*v*V+4*u*v*U;
  Z c=(v*v-4*u*w)*V*V-4*u*k*U*V+4*u*u*U*U;
  std::vector<int> kr;for(int p:mods){long t=k%p;if(t<0)t+=p;kr.push_back(t);}
  for(long j=jl;j<ju;j++){
   ++pairs;bool pass=true;
   for(size_t t=0;t<mods.size();t++){int p=mods[t];long jr=j%p;if(jr<0)jr+=p;if(!masks[t][kr[t]*p+jr]){pass=false;break;}}
   if(!pass){++filtered;continue;}
   ++exact;Z W=u*j-P*v;Z q=a*W*W+b*W+c;if(q<0)continue;
   Z rt;mpz_sqrt(rt.get_mpz_t(),q.get_mpz_t());if(rt*rt==q){++hits;std::cout<<"H "<<k<<" "<<j<<"\n";}
  }
 }
 std::cout<<"C "<<pairs<<" "<<filtered<<" "<<exact<<" "<<hits<<"\n";
}
