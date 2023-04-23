
import numpy as np

def torward_vector(sp, ep, maxspeed=3):
    twd = [e-s for s,e in zip(sp,ep)]
    print(twd)
    twdnorm = 0
    for t in twd: twdnorm += t**2
    for i in range(3): twd[i]=twd[i]/twdnorm*maxspeed
    print(twd)


# sp = np.array([10, 20, 30])
# ep = np.array([100, 200, 300])
# vec = ep - sp

# vecnorm = vec/np.linalg.norm(vec)
sp = (2,3,4)
ep=(30,40,50)
x = torward_vector(sp, ep)