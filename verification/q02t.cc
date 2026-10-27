#include <cstdio>
#include "../questions/q02-bev-nms/candidate/nms.cc"
int main(){ setvbuf(stdout, nullptr, _IONBF, 0);
  Box a{0,0,2,2,0.9f,0}, b{3,3,5,5,0.8f,0}, c{0,0,2,2,0.7f,0};
  printf("IoU disjoint diag=%.3f identical=%.3f\n", IoU(a,b), IoU(a,c));
  std::vector<Box> v{a,c,{0.1f,0,2.1f,2,0.95f,0},{10,10,12,12,0.3f,0}};
  auto k = NMS(v, 0.3f);
  printf("kept %zu, first score %.2f\n", k.size(), k[0].score);
}
