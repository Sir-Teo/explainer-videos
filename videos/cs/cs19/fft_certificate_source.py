"""Independent native integer-convolution reference, compiled outside benchmark timing."""

SOURCE = r'''
// Independent exact modular convolution certificate; excluded from NumPy timings.
#include <algorithm>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <vector>
using u32=std::uint32_t; using u64=std::uint64_t;
u32 power(u32 x,u32 k,u32 p){u64 r=1;for(;k;k>>=1,x=u64(x)*x%p)if(k&1)r=r*x%p;return r;}
void ntt(std::vector<u32>& a,u32 p,bool inverse){
 const std::size_t n=a.size();
 if(!n || (n&(n-1)) || (p-1)%n)throw std::runtime_error("unsupported radix or modulus");
 for(std::size_t i=1,j=0;i<n;i++){std::size_t b=n>>1;for(;j&b;b>>=1)j^=b;j^=b;if(i<j)std::swap(a[i],a[j]);}
 for(std::size_t len=2;len<=n;len<<=1){u32 root=power(3,(p-1)/len,p);if(inverse)root=power(root,p-2,p);
  for(std::size_t i=0;i<n;i+=len){u64 w=1;for(std::size_t j=0;j<len/2;j++){
   u32 u=a[i+j],v=u64(a[i+j+len/2])*w%p;
   a[i+j]=(u64(u)+v)%p;a[i+j+len/2]=(u64(u)+p-v)%p;w=w*root%p;
  }}
 }
 if(inverse){u32 inv=power(n,p-2,p);for(auto& x:a)x=u64(x)*inv%p;}
}
int main(int argc,char** argv){try{
 if(argc!=3)throw std::runtime_error("expected input/output paths");
 std::ifstream in(argv[1],std::ios::binary);u64 na=0,nb=0,n=0;
 in.read(reinterpret_cast<char*>(&na),8);in.read(reinterpret_cast<char*>(&nb),8);in.read(reinterpret_cast<char*>(&n),8);
 if(!in || !na || !nb || n<na+nb-1 || n>(1u<<23))throw std::runtime_error("invalid lengths");
 std::vector<u32> x(na),y(nb);in.read(reinterpret_cast<char*>(x.data()),na*4);in.read(reinterpret_cast<char*>(y.data()),nb*4);
 if(!in)throw std::runtime_error("truncated input");std::ofstream out(argv[2],std::ios::binary);
 for(u32 p:{998244353u,469762049u}){
  std::vector<u32>a(n),b(n);std::copy(x.begin(),x.end(),a.begin());std::copy(y.begin(),y.end(),b.begin());
  if(*std::max_element(x.begin(),x.end())>=p || *std::max_element(y.begin(),y.end())>=p)throw std::runtime_error("coefficient outside residue range");
  ntt(a,p,false);ntt(b,p,false);for(std::size_t i=0;i<n;i++)a[i]=u64(a[i])*b[i]%p;ntt(a,p,true);
  out.write(reinterpret_cast<char*>(a.data()),n*4);
 }
 if(!out)throw std::runtime_error("write failure");
 return 0;
}catch(const std::exception& e){std::cerr<<e.what()<<'\n';return 1;}}
'''
