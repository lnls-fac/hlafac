#!/usr/bin/env python3

import numpy
import math
import matplotlib.pyplot as plt
import sirius
import pyaccel

accel=sirius.SI_V07.create_accelerator()
pyaccel.tracking.set6dtracking(accel)

fam_data=sirius.SI_V07.family_data
chs=fam_data['chs']['index']
cvs=fam_data['cvs']['index']
bpm=fam_data['bpm']['index']

def orbit(accel,bpm):
    orbit=pyaccel.tracking.findorbit6(accel,'open')
    orb=numpy.zeros((6,len(bpm)))
    j=0
    for i in range(numpy.size(orbit,1)):
        if i in bpm:
            orb[:,j]=orbit[:,i]
            j+=1
    x=orb[0,:]
    y=orb[2,:]
    r=numpy.concatenate((x,y))
    return x,y,r

def matriz_resposta(accel,chs,cvs,bpm,dk):
    M=numpy.zeros((2*len(bpm),(len(chs)+len(cvs))))
    i=0
    for ch in chs:
        k = accel[ch].hkick_polynom

        accel[ch].hkick_polynom = k + dk/2.0
        x1,y1,r1 = orbit(accel,bpm)

        accel[ch].hkick_polynom =  k - dk/2.0
        x2,y2,r2 = orbit(accel,bpm)

        delta_h=r1-r2
        M[:,i]=delta_h/dk

        accel[ch].hkick_polynom =  k
        i+=1
    for cv in cvs:
        k=accel[cv].vkick_polynom

        accel[cv].vkick_polynom = k + dk/2.0
        x3,y3,r3 = orbit(accel,bpm)

        accel[cv].vkick_polynom = k - dk/2.0
        x4,y4,r4 = orbit(accel,bpm)

        delta_v=r3-r4
        M[:,i]=delta_v/dk

        accel[cv].vkick_polynom = k
        i+=1
    return M

def inverter_matriz(M):
    U,s,V=numpy.linalg.svd(M,full_matrices=False)
    invS=numpy.zeros((numpy.size(s),numpy.size(s)))
    for i in range(numpy.size(s)):
        if s[i] < 10e-16:
            invS[i][i]=0
        else:
            invS[i][i]=1/s[i]
    Ut=numpy.transpose(U)
    Vt=numpy.transpose(V)
    invM=Vt.dot(invS.dot(Ut))
    return invM

def correcao(accel,invM,r_ref,chs,cvs,bpm):
    x_erro,y_erro,r_erro = orbit(accel,bpm)
    delta_a=(r_ref-r_erro)
    dk=invM.dot(delta_a)

    i=0
    for ch in chs:
        k = accel[ch].hkick_polynom
        accel[ch].hkick_polynom = k + dk[i]
        i+=1
    for cv in cvs:
        k = accel[cv].vkick_polynom
        accel[cv].vkick_polynom = k + dk[i]
        i+=1

    x_f,y_f,r_f = orbit(accel,bpm)
    delta_b = (r_ref-r_f)
    delta_b2 = [z**2 for z in delta_b]
    desvio = math.sqrt(sum(delta_b2)/len(delta_b))
    return x_f,y_f,r_f,desvio,dk

try:
    M=numpy.genfromtxt('M.txt')
    invM=inverter_matriz(M)
except:
    dkick=1e-6
    M=matriz_resposta(accel,chs,cvs,bpm,dkick)
    numpy.savetxt('M.txt', M, fmt='%-14.8f')
    invM=inverter_matriz(M)

x_ref,y_ref,r_ref = orbit(accel,bpm)

# #kick 1e-4 na primeira corretora horizontal
# accel[chs[0]].hkick_polynom = 1e-4
# x_erro,y_erro,r_erro = orbit(accel,bpm)

#kick 1e-4 na primeira corretora vertical
accel[cvs[0]].vkick_polynom = 1e-4
x_erro,y_erro,r_erro = orbit(accel,bpm)

for i in range(3):
    x_f,y_f,r_f,desvio,dk = correcao(accel,invM,r_ref,chs,cvs,bpm)
    print(desvio)

plt.subplot(2, 2, 1)
plt.plot(x_ref,'g')
plt.plot(x_erro,'r')
plt.title('Orbita referência (verde) e orbita com erro (vermelha)')
plt.xlabel('bpm')
plt.ylabel('x')

plt.subplot(2, 2, 2)
plt.plot(y_ref,'g')
plt.plot(y_erro,'r')
plt.title('Orbita referência (verde) e orbita com erro (vermelha)')
plt.xlabel('bpm')
plt.ylabel('y')

plt.subplot(2, 2, 3)
plt.plot(x_ref,'g')
plt.plot(x_f,'b')
plt.title('Orbita referência (verde) e orbita corrigida (azul)')
plt.xlabel('bpm')
plt.ylabel('x')


plt.subplot(2, 2, 4)
plt.plot(y_ref,'g')
plt.plot(y_f,'b')
plt.title('Orbita referência (verde) e orbita corrigida (azul)')
plt.xlabel('bpm')
plt.ylabel('y')

plt.show()
