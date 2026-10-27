import numpy as np
def run(new, cutin=False, seed=0):
    rng=np.random.default_rng(seed)
    x=np.array([60.,0.]); P=np.eye(2)*100; Q=np.eye(2)*0.5; last=0.0; neg=0; minP=1e9
    def pred(t):
        nonlocal x,P,last,neg,minP
        dt=t-last
        if not new and dt<=0: return
        if dt<0: neg+=1
        F=np.array([[1,dt],[0,1]]); x=F@x; P=F@P@F.T+Q*dt; last=t; minP=min(minP,np.linalg.eigvalsh(P).min())
    H=np.array([1.,0.]); log=[]
    true_d=60.0; rejected=0
    for k in range(1,1001):          # 20 s, 20 ms planner tick
        now=k*0.02
        true_d = 60.0 if not (cutin and now>=10) else 30.0  # car cuts in at 30 m
        if k%2==0 and k>1:            # radar at 25Hz-ish, sample 50ms old
            ts=now-0.05; z=true_d+rng.normal(0,0.5); var=0.25
            if not new and ts< last-0.2: pass
            else:
                pred(ts); y=z-H@x
                if new and abs(y)>5: rejected+=1
                else:
                    S=H@P@H+var; K=P@H/S; x=x+K*y
                    if new: P=(np.eye(2)-np.outer(K,H))@P
                    else:
                        IKH=np.eye(2)-np.outer(K,H); P=IKH@P@IKH.T+np.outer(K,K)*var
        pred(now); log.append(x[0])
    return neg, minP, rejected, log[-1]
for new in (False,True):
    for cut in (False,True):
        print("new" if new else "old", "cutin" if cut else "steady", "neg_dt=%d minEig=%.4f rejected=%d final_d=%.1f"%run(new,cut))
