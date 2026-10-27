# 【背景】
# 这是一段早期的 ACC（自适应巡航）跟车逻辑，作者已离职，没有文档和单测。
# 每 50 ms 调用一次 calc()，返回期望加速度（m/s^2），交给下游纵向控制执行。
# 现在要把它接入重卡项目（满载 49 t），需要先重构再扩展。
#
# 【任务】（本题不需要写代码，请口述）
# 1. 尽量还原作者的意图：每个分支在处理什么场景？每个参数可能是什么单位？
# 2. 重构之前，你会先做什么？
# 3. 你会怎么拆分这段代码？各部分的接口长什么样？
# 4. 重构过程中你发现了哪些问题？哪些必须先和作者/产品确认？

last_acc = 0
flag = 0


def calc(d, v, v2, s, t):
    global last_acc, flag
    # d: 与前车距离, v: 自车速度, v2: 前车速度, s: 设定速度, t: 时间
    if d < 0 or d > 200:
        a = (s - v) * 0.3
    else:
        safe = v * 3.6 * 2 + 10
        if d < safe:
            if v2 < v:
                a = -((v - v2) ** 2) / (2 * (d - 5))
                if a < -5:
                    a = -5
                flag = 1
            else:
                a = (d - safe) * 0.05
        else:
            if flag == 1 and t - last_t < 2:
                a = 0
            else:
                flag = 0
                a = min((s - v) * 0.3, (d - safe) * 0.1)
    if a - last_acc > 0.2:
        a = last_acc + 0.2
    last_acc = a
    return a
