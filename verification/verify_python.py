import sys, math, importlib.util, numpy as np
def load(p, n):
    s = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
import os
Q = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "questions") + "/"
h = load(Q+"q01-heading/candidate/heading_utils.py", "h")
print("Q01 east heading (expect 0):", h.compute_headings([0,1],[0,0])[0])
print("Q01 err 179 vs -179 deg:", math.degrees(h.heading_error(math.radians(179), math.radians(-179))))
print("Q01 smooth:", h.smooth_headings([3.10, 3.14, -3.14, -3.10], window=5))
print("Q01 dup pts:", h.compute_headings([0,1,1,2],[0,0,0,0]))
try: h.compute_headings([0],[0])
except Exception as e: print("Q01 single pt:", type(e).__name__)

t = load(Q+"q07-transform/candidate/transforms.py", "t")
c, s_ = math.cos(math.pi/2), math.sin(math.pi/2)
R = np.array([[c,-s_,0],[s_,c,0],[0,0,1]])
T1 = t.make_T(R, [1,2,0]); T2 = t.make_T(np.eye(3), [10,0,0])
p = np.array([[1.0,0,0]])
print("Q07 transform_points (expect [1,3,0]):", t.transform_points(T1, p))
print("Q07 inv_T ok?", np.allclose(t.inv_T(T1), np.linalg.inv(T1)))
# round trip
w = t.lidar_to_world(p, T1, T2); back = t.world_to_lidar(w, T1, T2)
print("Q07 roundtrip:", back, " correct world:", (T2 @ T1 @ np.array([1,0,0,1]))[:3], " got:", w)
# round trip with only translation tests
Tt = t.make_T(np.eye(3),[1,2,3])
print("Q07 pure translation transform:", t.transform_points(Tt, p))

f = load(Q+"q10-ai-frenet/candidate/frenet.py", "f")
f.test_straight_line(); f.test_offset_right(); print("Q10 tests pass")
path = [(float(i), 0.0) for i in range(100)]
print("Q10 left point l (expect +2):", f.cartesian_to_frenet(10.3, 2.0, path))
print("Q10 end point s (expect 99.5):", f.cartesian_to_frenet(99.5, 0.0, path))
# curve: circle radius 50, point outside
R0=50; cp=[(R0*math.cos(a), R0*math.sin(a)) for a in np.arange(0, math.pi, 1.0/R0)]
print("Q10 circle, point at angle 0.5 rad, r=52 (expect s=25, l=-2):", f.cartesian_to_frenet(52*math.cos(0.5), 52*math.sin(0.5), cp))
# U-shaped path: hairpin closest point on other branch
up = [(float(i),0.0) for i in range(50)] + [(49+3.5*math.sin(a), 3.5-3.5*math.cos(a)) for a in np.linspace(0.1,math.pi,12)] + [(float(49-i),7.0) for i in range(1,50)]
print("Q10 U path, obj at (20,3.6):", f.cartesian_to_frenet(20,3.6,up))
try: f.cartesian_to_frenet(1,1,[(0,0),(0,0),(1,0)])
except Exception as e: print("Q10 dup point:", type(e).__name__)

a = load(Q+"q08-acc-refactor/candidate/acc.py", "a")
print("Q08 d=3 v=20 v2=10:", [round(a.calc(3, 20, 10, 25, 0.05*k),2) for k in range(5)])
a.last_acc=0; a.flag=0
a.calc(50, 20, 10, 25, 0)
try: print(a.calc(250, 20, 10, 25, 1))
except Exception as e: print("Q08 after brake, lead lost:", type(e).__name__)
a.flag=0
a.calc(50,20,10,25,0)
try: print("Q08 flag=1 then d>safe:", a.calc(190, 20, 25, 25, 1))
except Exception as e: print("Q08 flag=1 then d>=safe:", type(e).__name__, e)
try: a.calc(5, 20, 10, 25, 0)
except Exception as e: print("Q08 d=5:", type(e).__name__)
print("Q08 safe at 25m/s:", 25*3.6*2+10)

pp = load(Q+"q04-pure-pursuit/candidate/lateral_controller.py", "pp")
# path: straight 20m behind then left curve R=60
pts=[(x*0.5-20,0.0) for x in range(41)]
Rc=60; pts += [(Rc*math.sin(th), Rc-Rc*math.cos(th)) for th in np.arange(0.5/Rc, 1.2, 0.5/Rc)]
c = pp.Controller(pts)
x,y,yaw,v = 0.0,0.0,0.0,20.0
maxdev=0
for k in range(200):
    d = c.control(x,y,yaw,v)
    x += v*math.cos(yaw)*0.02; y += v*math.sin(yaw)*0.02; yaw += v/4.0*math.tan(d)*0.02
    dev = min(math.hypot(x-px,y-py) for px,py in pts); maxdev=max(maxdev,dev)
print("Q04 target:", c.find_target(x,y,v), "pos", round(x,1), round(y,1), "max deviation m:", round(maxdev,2))
