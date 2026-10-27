# 【背景】
# Frenet 坐标：用"沿参考线走了多远 s"和"偏离参考线多远 l"来描述位置，规划和预测模块大量使用。
# 同事用 AI 生成了下面的函数和单测，单测全部通过。PR 描述写着："AI 生成，已通过单测验证"。
# 这个函数会被用于：对感知输出的每个障碍物（每帧约 50 个），计算其相对本车道中心线的 (s, l)。
# 参考线是高速道路中心线，点间距约 1 m，长度约 2 km。
#
# 【任务】
# 1. 你会同意合入吗？请像真实 Code Review 一样给出意见。
# 2. 这个单测有什么问题？你会补充哪些测试？
# 3. 如果让你用 AI 修改这段代码，你会怎么描述需求？怎么确认 AI 改对了？

import math


def cartesian_to_frenet(x, y, ref_path):
    """
    将笛卡尔坐标 (x, y) 转换为相对参考线的 Frenet 坐标 (s, l)。
    ref_path: [(x0, y0), (x1, y1), ...]
    返回 s: 沿参考线的弧长；l: 横向偏移（沿行驶方向，左正右负）
    """
    # 找最近的参考点
    min_dist = float("inf")
    idx = 0
    for i, (px, py) in enumerate(ref_path):
        d = math.hypot(x - px, y - py)
        if d < min_dist:
            min_dist = d
            idx = i

    # 计算到最近点的累积弧长
    s = 0.0
    for i in range(idx):
        s += math.hypot(ref_path[i + 1][0] - ref_path[i][0],
                        ref_path[i + 1][1] - ref_path[i][1])

    # 用最近点与下一个点确定切向
    if idx == len(ref_path) - 1:
        idx -= 1
    x0, y0 = ref_path[idx]
    x1, y1 = ref_path[idx + 1]
    tx, ty = x1 - x0, y1 - y0
    norm = math.hypot(tx, ty)
    tx, ty = tx / norm, ty / norm

    # 投影
    dx, dy = x - x0, y - y0
    s += dx * tx + dy * ty
    l = dx * ty - dy * tx
    return s, l


def test_straight_line():
    path = [(float(i), 0.0) for i in range(100)]
    s, l = cartesian_to_frenet(10.3, 2.0, path)
    assert abs(s - 10.3) < 1e-6
    assert abs(abs(l) - 2.0) < 1e-6


def test_offset_right():
    path = [(float(i), 0.0) for i in range(100)]
    s, l = cartesian_to_frenet(50.0, -1.5, path)
    assert abs(s - 50.0) < 1e-6
    assert abs(abs(l) - 1.5) < 1e-6
