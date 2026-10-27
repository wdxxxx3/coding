// 【背景】
// 3D 检测网络会对同一个目标输出多个重叠的候选框，NMS（非极大值抑制）用来去重：
// 保留分数最高的框，删除与它重叠度（IoU）超过阈值的其他框，重复直到处理完。
// 这里的框是 BEV（鸟瞰图）下的轴对齐矩形，单位米。
//
// 【任务】
// 1. 讲清楚 IoU 和 NMS 各自在做什么。
// 2. 找出代码中的问题，按严重程度排序。
// 3. 这些问题在车上分别会表现成什么现象？

#include <algorithm>
#include <vector>

struct Box {
  float x1, y1, x2, y2;  // 左下角 (x1, y1) 与右上角 (x2, y2)
  float score;           // 置信度 [0, 1]
  int label;             // 0=车辆 1=行人 2=锥桶 ...
};

float IoU(const Box& a, const Box& b) {
  float w = std::min(a.x2, b.x2) - std::max(a.x1, b.x1);
  float h = std::min(a.y2, b.y2) - std::max(a.y1, b.y1);
  float inter = w * h;
  float area_a = (a.x2 - a.x1) * (a.y2 - a.y1);
  float area_b = (b.x2 - b.x1) * (b.y2 - b.y1);
  return inter / (area_a + area_b);
}

std::vector<Box> NMS(std::vector<Box> boxes, float iou_thresh) {
  std::sort(boxes.begin(), boxes.end(),
            [](const Box& a, const Box& b) { return a.score < b.score; });
  std::vector<Box> keep;
  while (!boxes.empty()) {
    Box best = boxes.front();
    keep.push_back(best);
    boxes.erase(boxes.begin());
    for (auto it = boxes.begin(); it != boxes.end(); ++it) {
      if (IoU(best, *it) > iou_thresh) {
        boxes.erase(it);
      }
    }
  }
  return keep;
}
