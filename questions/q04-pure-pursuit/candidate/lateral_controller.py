# 【背景】
# 这是一个横向控制器：输入车辆当前位姿和速度，以及规划给出的参考路径，
# 输出前轮转角（弧度，左转为正）。车辆为牵引车，轴距 4.0 m。
# 坐标系 ENU，yaw 为车头朝向，逆时针为正。
# path 是规划模块每个周期下发的路径点，点间距约 0.5 m，起点通常在车辆后方 10~20 m。
#
# 【任务】
# 1. 先不看注释以外的提示，说说这是什么控制算法？背后的几何关系是什么？
# 2. (x, y) 应该是车上哪个点的坐标？为什么？
# 3. 这段代码上车会有什么问题？

import math

WHEELBASE = 4.0
MAX_STEER = math.radians(30)


class Controller:
    def __init__(self, path):
        self.path = path  # [(x, y), ...]
        self.k = 0.8
        self.ld_min = 1.0

    def find_target(self, x, y, v):
        ld = max(self.k * v, self.ld_min)
        for px, py in self.path:
            if math.hypot(px - x, py - y) >= ld:
                return px, py, ld
        return self.path[-1][0], self.path[-1][1], ld

    def control(self, x, y, yaw, v):
        tx, ty, ld = self.find_target(x, y, v)
        alpha = math.atan2(ty - y, tx - x) - yaw
        delta = math.atan2(2.0 * WHEELBASE * math.sin(alpha), ld)
        return delta
