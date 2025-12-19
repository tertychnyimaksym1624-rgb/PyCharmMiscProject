from vpython import *
from random import *

kB = 1.38e-23
n = 10
T = 50
m = 6.65e-26
r0 = 3.4e-10
sigma = 119*kB
R = r0/2
lx = 1e-8
ly = 1e-8

t_global = 1e-9
dt = 1e-15

scale = 1/lx
scene1 = canvas(width=800, height=800, background=vector(0,0,0), center=vector(0.5,0.5,0.1), align='left')
cylinder(pos=vec(0, 0, 0), axis=vec(1, 0, 0,), radius=0.01, color=color.yellow)
cylinder(pos=vec(0, 0, 0), axis=vec(0, 1, 0,), radius=0.01, color=color.yellow)
cylinder(pos=vec(0, 1, 0), axis=vec(1, 0, 0,), radius=0.01, color=color.yellow)
cylinder(pos=vec(1, 0, 0), axis=vec(0, 1, 0,), radius=0.01, color=color.yellow)
graph(title="Енергії", xtitle="Ek,Ep,Egen", width=500, height=300, background=color.white, align="left", autoscale=True)
E_gen_graf = gcurve(label="загальна", color=color.yellow, width=2)
Ek_graf = gcurve( color=color.red, width=2)#label="кінетична",
Ep_graf = gcurve( color=color.green, width=2)#label="потенціальна",

x = []
y = []
vx = []
vy = []
fx = []
fy = []
ball = []


def init():
   for i in range(n):
       x.append(R + (lx - 2*R) * random())
       y.append(R + (ly - 2*R) * random())
       vx.append(sin(2*pi*random())*sqrt(2*kB*T/m)*sqrt(-log(random())))
       vy.append(sin(2*pi*random())*sqrt(2*kB*T/m)*sqrt(-log(random())))
       fx.append(0)
       fy.append(0)
       ball.append(sphere(pos=vector(x[i]*scale,y[i]*scale,0), radius = R*scale, color = vector(1-i/n,i/n,0), make_trail=False))


def p_func(r):
   return 4*sigma*(exp(12*log(r0/r))-exp(6*log(r0/r)))


def f_func(r):
   return 24*sigma/r*(2*exp(12*log(r0/r))-exp(6*log(r0/r)))


def GB_wall(coor,direct,i):
   if direct == 'x':
       if coor<0:
           coor = 2*0-coor
           vx[i] = - vx[i]
       if coor > lx:
           coor = 2 * lx - coor
           vx[i] = - vx[i]
   if direct == 'y':
       if coor<0:
           coor = 2*0-coor
           vy[i] = - vy[i]
       if coor > ly:
           coor = 2 * ly - coor
           vy[i] = - vy[i]
   return coor


def BC(coor,direct,i):
   if direct == 'x':
       if coor<0:
           coor += lx
       if coor > lx:
           coor -= lx
   if direct == 'y':
       if coor<0:
           coor += ly
       if coor > ly:
           coor -= ly
   return coor


init()
t = 0
while t < t_global:
   Ep = 0
   for i in range(0,n):
       fx[i] = 0
       fy[i] = 0
       for j in range(0, n):
           if i != j:
               r = sqrt((x[i]-x[j])**2+(y[i]-y[j])**2)
               f = f_func(r)
               fx[i] += f / r * (x[i] - x[j])
               fy[i] += f / r * (y[i] - y[j])
               Ep += p_func(r)/2
   Ek = 0
   for i in range(n):
       vx[i] = vx[i] + fx[i] / m * dt
       vy[i] = vy[i] + fy[i] / m * dt
       x[i] = BC(x[i] + vx[i] * dt,'x',i)
       y[i] = BC(y[i] + vy[i] * dt,'y',i)
       ball[i].pos = vector(x[i]*scale,y[i]*scale,0)
       Ek += m*(vx[i]**2/2+vy[i]**2/2)

   # norma = sqrt((2*n*2*kB*T/2 - Ep)/Ek)
   norma = sqrt(n*2*kB*T/2/Ek)
   for i in range(n):
       vx[i] *= norma
       vy[i] *= norma

   t = t+dt
   # Ek_graf.plot(t/dt, Ek/1.6e-19)
   Ep_graf.plot(t/dt, Ep/1.6e-19)
