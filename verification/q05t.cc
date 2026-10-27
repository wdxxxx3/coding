#include <cstdio>
#include "../questions/q05-pose-buffer/candidate/pose_buffer.h"
int main(){ PoseBuffer b; for(int i=0;i<10;i++) b.Push({i*0.01, i*0.25, 0, (i<5? 3.13: -3.13)});
  Pose p; for(double t: {0.035,0.045,0.055,0.5}){ b.Query(t,&p); printf("t=%.3f x=%.3f yaw=%.3f\n",t,p.x,p.yaw);} }
