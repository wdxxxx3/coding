// 【背景】
// 激光点云一帧几十万个点，下游处理前常做"体素下采样"：
// 把空间划分成边长为 voxel 的小立方体，同一个立方体里的点用它们的质心代替。
// 输入点云在车体坐标系下（原点在车上），重卡前向感知距离要求 >= 250 m，常用 voxel = 0.1~0.2 m。
//
// 【任务】
// 1. 讲清楚这段代码的流程。grid[key] 第一次访问时 cell 里的值是什么？
// 2. 找出问题。哪些问题会"凭空造出障碍物"？哪些会"让障碍物消失或变形"？
// 3. 你会怎么改 key 的设计？

#include <cmath>
#include <unordered_map>
#include <vector>

struct Point { float x, y, z, intensity; };

std::vector<Point> VoxelDownsample(const std::vector<Point>& cloud, float voxel) {
  std::unordered_map<int, std::pair<Point, int>> grid;
  for (const auto& p : cloud) {
    int ix = static_cast<int>(p.x / voxel);
    int iy = static_cast<int>(p.y / voxel);
    int iz = static_cast<int>(p.z / voxel);
    int key = ix * 1000000 + iy * 1000 + iz;
    auto& cell = grid[key];
    cell.first.x += p.x;
    cell.first.y += p.y;
    cell.first.z += p.z;
    cell.first.intensity += p.intensity;
    cell.second += 1;
  }
  std::vector<Point> out;
  for (auto& kv : grid) {
    Point c = kv.second.first;
    int n = kv.second.second;
    out.push_back({c.x / n, c.y / n, c.z / n, c.intensity / n});
  }
  return out;
}
