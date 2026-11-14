using System;
using System.Collections.Generic;

public static class RgphiSquareSearch
{
    static int Gcd(int a, int b) {
        while (b != 0) { int r = a % b; a = b; b = r; }
        return Math.Abs(a);
    }

    static long Inv(long a, long m) {
        long t=0, next=1, r=m, step=a%m;
        while(step!=0) {
            long q=r/step;
            long old=t; t=next; next=old-q*next;
            old=r; r=step; step=old-q*step;
        }
        if(r!=1) throw new ArgumentException("Nonunit mod " + m);
        return (t%m+m)%m;
    }

    static int[][] Roots(int bound) {
        var smallest=new int[bound+1];
        for(int p=2;p<=bound;p++) if(smallest[p]==0) {
            for(int n=p;n<=bound;n+=p) if(smallest[n]==0) smallest[n]=p;
        }
        var roots=new int[bound+1][];
        roots[1]=new int[]{0};
        for(int n=2;n<=bound;n++) {
            int p=smallest[n], q=p, m=n/p;
            while(m%p==0) {q*=p; m/=p;}
            int[] local=q==2 ? new int[]{1} :
                p==2 && q>=8 ? new int[]{1,q-1,q/2+1,q/2-1} :
                new int[]{1,q-1};
            var values=new int[local.Length*roots[m].Length];
            int index=0;
            long e=Inv(m,q);
            foreach(int a in roots[m]) foreach(int b in local) {
                long k=(((b-a)*e)%q+q)%q;
                values[index++]=(int)(a+m*k);
            }
            roots[n]=values;
        }
        return roots;
    }

    static long Square(int x) {return (long)x*x;}

    public static string Search(int maximum, int kind) {
        var roots=Roots(6*maximum);
        long candidates=0;
        var output=new System.Text.StringBuilder();
        if(kind==606897) {
            for(int q=4;q<=maximum;q++) {
                if(q%3==0) continue;
                for(int e=5*q/6+1;e<q;e++) {
                    if(e%3==0 || Gcd(e,q)!=1) continue;
                    int c=3*e-q;
                    foreach(int u in roots[q]) {
                        int a=(int)((long)e*u%q);
                        if(a%3==0 || a==e || 2*a<=c || 2%Gcd(a,c)!=0) continue;
                        foreach(int v in roots[c]) {
                            int d=c+(int)(3L*q*v%c);
                            if(d>=2*a || d==c || d%3==0 || Gcd(d,a)!=1 || 2%Gcd(q,d)!=0) continue;
                            candidates++;
                            if((Square(q)-Square(d))%a!=0 || (Square(c)-Square(a))%d!=0) continue;
                            if((d-q)%Gcd(e,a)!=0 || (a-c)%Gcd(e,d)!=0) continue;
                            output.AppendLine(a+","+c+","+d+","+q+","+e);
                        }
                    }
                }
            }
        } else {
            int r=kind;
            for(int a=3;a<=maximum;a++) {
                if(a%r==0) continue;
                for(int e=a+1;e<2*a;e++) {
                    if(e%r==0 || Gcd(a,e)!=1) continue;
                    for(int shift=1; shift<=2; shift++) {
                        int j=r==2 ? (shift==1 ? 1:-1):shift;
                        int d=r*e-j*a;
                        if(d<=r*a || d>=4*a || d%r==0) continue;
                        foreach(int u in roots[d]) {
                            int c=(int)((long)r*a*u%d);
                            if(c%r==0 || d>=2*c || c>=2*a || (r-1)%Gcd(a,c)!=0) continue;
                            foreach(int v in roots[c]) {
                                int q=c+(int)((long)d*v%c);
                                if(q==c || q==e || q>=2*a || q%r==0 || Gcd(q,a)!=1 || (r-1)%Gcd(q,d)!=0) continue;
                                candidates++;
                                if((Square(c)-Square(a))%q!=0 || (Square(q)-Square(e))%a!=0) continue;
                                if((c-a)%Gcd(e,q)!=0 || (r*a-c)%Gcd(e,d)!=0 || (d-q)%Gcd(e,c)!=0) continue;
                                output.AppendLine(a+","+c+","+d+","+q+","+e);
                            }
                        }
                    }
                }
            }
        }
        return "Kind="+kind+" max="+maximum+" candidates="+candidates+"\n"+output.ToString();
    }
}
