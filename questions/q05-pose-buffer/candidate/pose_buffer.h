// 【背景】
// 激光雷达转一圈约 100 ms，这期间车在动（高速时 100 ms 走 2.5 m）。
// "运动补偿"需要查询每个激光点采样时刻的车辆位姿，把所有点统一到同一时刻。
// PoseBuffer 由定位线程以 100 Hz 调用 Push()，由点云处理线程调用 Query()。
//
// 【任务】
// 1. 讲清楚 Query 的逻辑，特别是二分查找部分是否正确。
// 2. 这段代码有哪些问题？哪些会导致点云"重影"或"拖尾"？
// 3. 你会怎么修，怎么验证？

#include <deque>
#include <mutex>

struct Pose {
  double t;     // 秒
  double x, y;  // 米
  double yaw;   // 弧度 [-pi, pi]
};

class PoseBuffer {
 public:
  void Push(const Pose& p) {
    std::lock_guard<std::mutex> lock(mu_);
    buf_.push_back(p);
    if (buf_.size() > kMaxSize) buf_.pop_front();
  }

  bool Query(double t, Pose* out) {
    if (buf_.empty()) return false;
    std::lock_guard<std::mutex> lock(mu_);
    if (t <= buf_.front().t) { *out = buf_.front(); return true; }
    if (t >= buf_.back().t) { *out = buf_.back(); return true; }

    size_t lo = 0, hi = buf_.size() - 1;
    while (lo < hi) {
      size_t mid = (lo + hi) / 2;
      if (buf_[mid].t < t) lo = mid + 1; else hi = mid;
    }
    const Pose& a = buf_[lo - 1];
    const Pose& b = buf_[lo];
    double r = (t - a.t) / (b.t - a.t);
    out->t = t;
    out->x = a.x + r * (b.x - a.x);
    out->y = a.y + r * (b.y - a.y);
    out->yaw = a.yaw + r * (b.yaw - a.yaw);
    return true;
  }

 private:
  static constexpr size_t kMaxSize = 200;
  std::deque<Pose> buf_;
  std::mutex mu_;
};
