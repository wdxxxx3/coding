#include <cstdio>
#include "../questions/q09-voxel/candidate/voxel_filter.cc"
int main(){
  auto o = VoxelDownsample({{0.05f,100.05f,0.05f,1},{0.15f,0.05f,0.05f,1}}, 0.1f);
  for(auto&p:o) printf("collision -> %zu pts: (%.2f, %.2f, %.2f)\n", o.size(), p.x,p.y,p.z);
  o = VoxelDownsample({{-0.3f,0,0,1},{0.3f,0,0,1}}, 0.5f);
  printf("trunc toward zero -> %zu pts\n", o.size());
  o = VoxelDownsample({{230.f,0,0,1}}, 0.1f);
}
