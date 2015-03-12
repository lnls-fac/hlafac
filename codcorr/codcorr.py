import numpy as np
import matplotlib.pyplot as plt

def orbita_inicial(bpms):
    x=np.random.randn(bpms)*10e-6
    y=np.random.randn(bpms)*10e-6
    r= np.concatenate((x,y),axis=1)
    return x,y,r

def matriz_resposta(hcm,vcm,bpms):
    M=np.random.randn(2*bpms,hcm+vcm)
    return M

def inverter_matriz(M):
    U,s,V=np.linalg.svd(M,full_matrices=False)
    invS=np.zeros((np.size(s),np.size(s)))
    for i in range(np.size(s)):
        if s[i] < 10e-15:
            invS[i][i]=0
        else:
            invS[i][i]=1/s[i]
    Ut=np.transpose(U)
    invM=V.dot(invS.dot(Ut))
    return invM

def orbita_referencia(bpms):
    x=np.zeros(bpms)
    y=np.zeros(bpms)
    r= np.concatenate((x,y),axis=1)
    print x,y,r

def db(r_i,r_r,invM):
    delta=r_r-r_i
    delta=np.transpose(delta)
    db=invM.dot(delta)

#[x,y,r]=orbita_inicial(100)
#plt.plot(x)
#plt.show()
print matriz_resposta(2,5,3)
