#include <algorithm>
#include <array>
#include <chrono>
#include <iostream>
#include <numeric>
#include <vector>
using namespace std;
long long pairs_n=0,D_n=0,C_n=0,P_n=0,E_n=0,Croot_n=0,Proot_n=0,crt_n=0;
int inv(int a,int n){a%=n;for(int i=1;i<n;i++)if((a*i)%n==1)return i;return n==1?0:-1;}
vector<int> divisors(int n){vector<int> r;for(int i=1;i*i<=n;i++)if(n%i==0){r.push_back(i);if(i*i!=n)r.push_back(n/i);}return r;}
bool compatible(vector<pair<int,int>> cs){for(int i=0;i<(int)cs.size();i++)for(int j=0;j<i;j++)if((cs[i].first-cs[j].first)%gcd(cs[i].second,cs[j].second))return false;return true;}
int main(int argc,char**argv){int cap=argc>1?stoi(argv[1]):500;if(cap<1||cap>5000){cerr<<"Certified implementation range is 1<=Qmax<=5000\n";return 2;}auto start=chrono::steady_clock::now();
cout<<"CONFIG before computation: exact integer hexagon; Q<= "<<cap<<"; d=4,5,6,7; states P/(dQ),A/Q,A/D,C/D,C/E,P/E; all primitive and high; CRT includes strict residue modulo dQ\n"<<flush;
vector<vector<int>> roots(2*cap+1);for(int m=2;m<=2*cap;m++)for(int i=1;i<m;i++)if((i*i)%m==1)roots[m].push_back(i);
for(int d=4;d<=7;d++)for(int Q=1;Q<=cap;Q++)for(int A=Q/2+1;A<Q;A++)if(gcd(A,Q)==1){pairs_n++;
 for(int rt:roots[A]){int D=A+(Q*rt)%A;if(!(A<D&&D<2*A))continue;D_n++;
  for(int rc:roots[D]){int C=(A*rc)%D;if(!(D<2*C&&C<D))continue;C_n++;
   if(gcd(d,Q)!=1)continue;
   for(int k=-3;k<=3;k++){if(k==0||2*abs(k)>=d)continue;int P=d*A+k*Q;
    if(!(d*Q<2*P&&P<d*Q&&P<2*C))continue;if(gcd(P,d*Q)!=1)continue;P_n++;
    for(int E:divisors(P*P-C*C)){if(!(P<E&&E<2*C))continue;E_n++;
     if((E*E-D*D)%C)continue;Croot_n++;
     if((E*E-d*d*Q*Q)%P)continue;Proot_n++;
     vector<pair<int,int>> cs={{1,Q},{(d*A*inv(P,d*Q))%(d*Q),d*Q},{(C*inv(A,D))%D,D},{(D*inv(Q,A))%A,A},{(P*inv(C,E))%E,E},{(E*inv(D,C))%C,C},{(E*inv(d*Q,P))%P,P}};
     cerr<<"PRE_CRT "<<d<<" "<<Q<<" "<<A<<" "<<D<<" "<<C<<" "<<E<<" "<<P<<"\n";
     if(compatible(cs)){crt_n++;cerr<<"REALIZATION "<<d<<" "<<Q<<" "<<A<<" "<<D<<" "<<C<<" "<<E<<" "<<P<<"\n";}
    }
   }
  }
 }
}
double sec=chrono::duration<double>(chrono::steady_clock::now()-start).count();
cout<<"{\"Q_max\":"<<cap<<",\"primitive_Q_A_pairs\":"<<pairs_n<<",\"first_cycle_D_candidates\":"<<D_n<<",\"second_cycle_C_candidates\":"<<C_n<<",\"high_primitive_P_candidates\":"<<P_n<<",\"E_divisors_in_chamber\":"<<E_n<<",\"E_also_root_mod_C\":"<<Croot_n<<",\"E_also_root_mod_P\":"<<Proot_n<<",\"CRT_compatible\":"<<crt_n<<",\"seconds\":"<<sec<<"}\n";
return 0;}
