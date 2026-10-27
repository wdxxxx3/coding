# 【背景】
# 约定：T_a_b 是 4x4 齐次变换矩阵，把 b 坐标系下的点变换到 a 坐标系：p_a = T_a_b @ p_b
# 例如 T_vehicle_lidar 是激光雷达外参（lidar -> vehicle），T_world_vehicle 是定位结果（vehicle -> world）。
#
# 【任务】
# 1. 逐个函数说明它在做什么，并判断是否正确。
# 2. 如果你来给这个文件写单元测试，你会怎么设计？
#    （提示问题：只做 "lidar->world->lidar 来回转一圈等于原值" 的测试够不够？）

import numpy as np


def make_T(R, t):
    T = np.eye(4)
    T[:3, :3] = R
    T[:3, 3] = t
    return T


def inv_T(T):
    Ti = np.eye(4)
    Ti[:3, :3] = T[:3, :3].T
    Ti[:3, 3] = -T[:3, 3]
    return Ti


def transform_points(T, pts):
    """pts: (N, 3) 数组，返回变换后的 (N, 3)。"""
    homo = np.hstack([pts, np.ones((pts.shape[0], 1))])
    return (homo @ T)[:, :3]


def lidar_to_world(pts_lidar, T_vehicle_lidar, T_world_vehicle):
    T_world_lidar = T_vehicle_lidar @ T_world_vehicle
    return transform_points(T_world_lidar, pts_lidar)


def world_to_lidar(pts_world, T_vehicle_lidar, T_world_vehicle):
    T_lidar_world = inv_T(T_world_vehicle @ T_vehicle_lidar)
    return transform_points(T_lidar_world, pts_world)
