#!/usr/bin/env bash
# 重新验证题目中埋的问题。需要 python3 + numpy、g++（C++17）。
# C++ 测试预期会报 ASan/UBSan 错误，这正是题目里埋的 bug。
set -u
cd "$(dirname "$0")" && mkdir -p build
PYTHONDONTWRITEBYTECODE=1 python3 verify_python.py
python3 q03_kf_sim.py
for t in q02t q05t q09t; do
  echo "== $t"
  g++ -std=c++17 -g -fsanitize=address,undefined "$t.cc" -o "build/$t" && "./build/$t" 2>&1 | grep -E "ERROR|runtime error|->|t=|kept|IoU" | head -5
done
