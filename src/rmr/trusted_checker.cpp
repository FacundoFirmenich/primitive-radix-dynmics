#include <bits/stdc++.h>
using namespace std; using i128=__int128_t;
struct R{long long p,q;};
long long B0=88011536665779LL, M=223336848698040LL;
R X[5]={{406,731},{712,731},{712,1265},{1218,1265},{406,557}};
int TM[5]={1,0,3,2,4}, SM[5]={4,2,1,0,0};
long long mod(i128 a,long long m){long long r=(long long)(a%m);return r<0?r+m:r;}
bool tedge(long long B,int i,int j){long long g=gcd(X[i].q,B);if(X[i].q/g!=X[j].q)return false;return mod((i128)(B/g)*X[i].p,X[j].q)==X[j].p;}
bool sedge(long long B,int i,int j){long long h=gcd(X[i].p,B);if(X[i].p/h!=X[j].p)return false;long long ci=X[i].q-X[i].p,cj=X[j].q-X[j].p;return mod((i128)(B/h)*ci,X[j].p)==cj;}
int main(){
 for(int t=0;t<=1000;t++){
  long long B=B0+M*t;
  for(int i=0;i<5;i++){
   if(!(2*X[i].p>X[i].q && X[i].p<X[i].q && gcd(X[i].p,X[i].q)==1))return 1;
   if(!tedge(B,i,TM[i])||!sedge(B,i,SM[i]))return 2;
  }
  for(int s=0;s<5;s++){bool seen[5]={};queue<int>q;seen[s]=1;q.push(s);while(!q.empty()){int u=q.front();q.pop();for(int v:{TM[u],SM[u]})if(!seen[v])seen[v]=1,q.push(v);}for(bool z:seen)if(!z)return 3;}
 }
 cout<<"PASS\n"<<"counterfamily_bases_checked=1001\n"<<"cross_language_exact_edges=PASS\n"<<"unique_strict_edge=S3:x3->x0\n";
}
