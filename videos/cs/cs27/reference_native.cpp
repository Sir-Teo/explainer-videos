// Independent finite references: subset DP, modular CRT, exhaustive bit operations.
#include <algorithm>
#include <cmath>
#include <cstdint>
#include <iostream>
#include <numeric>
#include <string>
#include <vector>
#include <gmpxx.h>
using cpp_int=mpz_class;
using I=long;
I mul(I a,I b,I p){return (__int128)a*b%p;}
I power(I a,I n,I p){I r=1;for(;n;n>>=1,a=mul(a,a,p))if(n&1)r=mul(r,a,p);return r;}
bool prime(I n){if(n<2)return false;for(I d=2;d*d<=n;++d)if(n%d==0)return false;return true;}
I modular(std::vector<std::vector<I>> a,I p){
 int n=a.size();I d=1;
 for(auto &r:a)for(auto &v:r)v=(v%p+p)%p;
 for(int j=0;j<n;++j){
  int pivot=j;while(pivot<n&&!a[pivot][j])++pivot;if(pivot==n)return 0;
  if(pivot!=j){std::swap(a[pivot],a[j]);d=(p-d)%p;}
  I v=a[j][j];d=mul(d,v,p);I inv=power(v,p-2,p);
  for(int i=j+1;i<n;++i){I f=mul(a[i][j],inv,p);for(int c=j;c<n;++c)a[i][c]=(a[i][c]-mul(f,a[j][c],p)+p)%p;}
 }
 return d;
}
unsigned __int128 mask(const std::string &s){unsigned __int128 x=0;for(char c:s)x=x*10+c-'0';return x;}
int main(){
 std::string op; if(!(std::cin>>op))return 2;
 if(op=="ov"){
  int n,m;std::cin>>n>>m;std::vector<unsigned __int128>a(n),b(m);std::string s;
  for(auto &x:a){std::cin>>s;x=mask(s);}for(auto &x:b){std::cin>>s;x=mask(s);}
  std::uint64_t checked=0;for(int i=0;i<n;++i)for(int j=0;j<m;++j){++checked;if(!(a[i]&b[j])){std::cout<<1<<' '<<i<<' '<<j<<' '<<checked<<'\n';return 0;}}
  std::cout<<0<<" -1 -1 "<<checked<<'\n';return 0;
 }
 if(op=="pit_batch"){
  int trials;std::cin>>trials;
  for(int t=0;t<trials;++t){
   int n,wrong;I p;std::cin>>n>>p>>wrong;std::vector<I>xs(n);for(auto &x:xs)std::cin>>x;
   std::vector<std::vector<I>>a(n,std::vector<I>(n));
   for(int i=0;i<n;++i){I v=1;for(int j=0;j<n;++j){a[i][j]=v;v=mul(v,xs[i],p);}}
   I lhs=modular(a,p),rhs=1;for(int j=0;j<n;++j)for(int i=0;i<j;++i)rhs=mul(rhs,(wrong&&i==0&&j==1?(xs[j]+xs[i])%p:(xs[j]-xs[i]+p)%p),p);
   std::cout<<lhs<<' '<<rhs<<' '<<(lhs==rhs)<<'\n';
  }
  return 0;
 }
 if(op=="blr4"){
  constexpr int N=16;int parity[N][N];for(int a=0;a<N;++a)for(int x=0;x<N;++x)parity[a][x]=__builtin_parity((unsigned)(a&x));
  for(unsigned f=0;f<(1u<<N);++f){
   int distance=N,bad=0;for(int a=0;a<N;++a){int d=0;for(int x=0;x<N;++x)d+=((f>>x)&1u)!=parity[a][x];distance=std::min(distance,d);}
   for(int x=0;x<N;++x)for(int y=0;y<N;++y)bad+=(((f>>x)^(f>>y)^(f>>(x^y)))&1u);
   std::cout<<f<<' '<<distance<<' '<<bad<<'\n';
  }
  return 0;
 }
 if(op=="satcount"){
  int n,m;std::cin>>n>>m;if(n<0||n>25)return 3;std::vector<std::vector<int>>clauses(m);
  for(auto &c:clauses){int k;std::cin>>k;c.resize(k);for(auto &l:c)std::cin>>l;}
  std::uint64_t count=0;for(std::uint64_t x=0;x<(1ull<<n);++x){bool good=true;for(auto &c:clauses){bool sat=false;for(int l:c)sat|=bool(x>>(std::abs(l)-1)&1)==(l>0);if(!sat){good=false;break;}}count+=good;}
  std::cout<<count<<'\n';return 0;
 }
 int n;std::cin>>n;if(n<0||n>250)return 3;std::vector<std::vector<I>>a(n,std::vector<I>(n));for(auto&r:a)for(auto&v:r)std::cin>>v;
 if(op=="permanent"){
  if(n>22)return 3;std::vector<cpp_int>dp(1ull<<n);dp[0]=1;
  for(unsigned s=0;s<(1u<<n);++s){int row=__builtin_popcount(s);if(row==n)continue;for(int j=0;j<n;++j)if(!(s>>j&1)&&a[row][j])dp[s|(1u<<j)]+=dp[s]*a[row][j];}
  std::cout<<dp.back()<<'\n';return 0;
 }
 if(op=="determinant"){
  cpp_int bound=1;for(auto&r:a){cpp_int norm=0;for(auto v:r)norm+=cpp_int(v)*v;cpp_int root;mpz_sqrt(root.get_mpz_t(),norm.get_mpz_t());if(root*root<norm)++root;bound*=root;}
  if(bound==0){std::cout<<"0 0\n";return 0;}
  cpp_int x=0,M=1;int primes=0;I p=1000000007;
  while(M<=2*bound){while(!prime(p))p-=2;cpp_int xres=x%p,mres=M%p;I r=modular(a,p),xm=xres.get_si(),mm=mres.get_si();I t=mul((r-xm+p)%p,power(mm,p-2,p),p);x+=M*t;M*=p;++primes;p-=2;}
  if(x>M/2)x-=M;
  std::cout<<x<<' '<<primes<<'\n';return 0;
 }
 if(op=="detmod") {I p;std::cin>>p;std::cout<<modular(a,p)<<'\n';return 0;}
 return 4;
}
