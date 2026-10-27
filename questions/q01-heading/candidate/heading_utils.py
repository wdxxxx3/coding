# 【背景】
# 自动驾驶中常用"航向角 heading"表示车头朝向：以东为 x 轴、北为 y 轴（ENU 坐标系），
# heading 是车头方向与 x 轴的夹角，逆时针为正，单位弧度，取值范围 [-pi, pi]。
# 下面是规控模块中处理航向角的一组工具函数，已经在线上使用。
#
# 【任务】
# 1. 请边读边说：每个函数在做什么、输入输出是什么。
# 2. 你认为这段代码有哪些问题？请按严重程度排序。
# 3. 选最严重的一个，说说它在车上会造成什么后果，以及怎么修。

import math
import numpy as np


def compute_headings(xs, ys):
    """根据轨迹点序列计算每个点的航向角（弧度）。"""
    headings = []
    for i in range(len(xs) - 1):
        dx = xs[i + 1] - xs[i]
        dy = ys[i + 1] - ys[i]
        headings.append(math.atan2(dx, dy))
    headings.append(headings[-1])
    return headings


def heading_error(target, current):
    """目标航向与当前航向的偏差，用于横向控制。"""
    return target - current


def smooth_headings(headings, window=5):
    """对航向角做滑动平均，抑制定位噪声。"""
    smoothed = []
    half = window // 2
    for i in range(len(headings)):
        lo = max(0, i - half)
        hi = min(len(headings), i + half + 1)
        smoothed.append(sum(headings[lo:hi]) / (hi - lo))
    return smoothed


def heading_rate(headings, dt):
    """航向角变化率（rad/s）。"""
    return [(headings[i + 1] - headings[i]) / dt for i in range(len(headings) - 1)]
