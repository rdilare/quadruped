from lib import *
import numpy as np
import time
from serial import Serial
s = Serial("COM5",115200,timeout=0.1)
# import pyfirmata as pf

# board = pf.Arduino('COM5')
# pin1 = board.get_pin('d:51:s')  # setting up pin as servo
# pin2 = board.get_pin('d:52:s')
# pin3 = board.get_pin('d:53:s')
# pin4 = board.get_pin('d:48:s')
# pin5 = board.get_pin('d:49:s')
# pin6 = board.get_pin('d:47:s')
# pin7 = board.get_pin('d:23:s')
# pin8 = board.get_pin('d:24:s')
# pin9 = board.get_pin('d:25:s')
# pin10 = board.get_pin('d:27:s')
# pin11 = board.get_pin('d:28:s')
# pin12 = board.get_pin('d:29:s')


bodyDim=[0.5, 0.36]
bodyState = [0, 0, 0.28, 0, 0, 0]

LL=[0.095, 0.095,0.23]
legLengths=np.array([LL,LL,LL,LL]).T

toePos = initToePos(bodyDim,bodyState)
step = .07
radius = 2
T=1.0
delta = 0.01


def runBot(ang,t):
	ang = ang*180/np.pi

	ang[0,0] = 90 + ang[0,0]
	ang[1,0] = 90 - ang[1,0] - 10
	ang[2,0] = 180 - ang[2,0] - 10

	ang[0,1] = 90 + ang[0,1]
	ang[1,1] = 90 - ang[1,1] -10
	ang[2,1] =180 - ang[2,1] - 5

	ang[0,2] = 90 - ang[0,2]
	ang[1,2] = 90 + ang[1,2] 
	ang[2,2] = 0 + ang[2,2]

	ang[0,3] = 90 - ang[0,3]
	ang[1,3] = 90 + ang[1,3] + 10
	ang[2,3] = 180 - ang[2,3] - 10
	ang = np.array(ang,dtype=np.int16)
	# a = int(90 - 30*np.sin(t*2.5))
	# b = int(90 - 30*np.sin(t*2.5))
	# c = int(90 + 30*np.sin(t*2.5))
	# d = int(90 - 30*np.sin(t*2.5))

	call = s.readline()
	print (call)
	if b"ok" in call:

		x = bytearray("{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11};".format(ang[0,0],ang[1,0],ang[2,0],ang[0,1],ang[1,1],ang[2,1],ang[0,2],ang[1,2],ang[2,2],ang[0,3],ang[1,3],ang[2,3]),"UTF8")
		# x = bytearray("90,135,{0},90,135,{1},90,45,{2},90,45,{3};".format(a,b,c,d),"UTF8")
	# x = bytearray(input("> "),"UTF8")
	# pin1.write(ang[0,0])
	# pin2.write(ang[1,0])
	# pin3.write(ang[2,0])
	# pin4.write(ang[0,1])
	# pin5.write(ang[1,1])
	# pin6.write(ang[2,1])
	# pin7.write(ang[0,2])
	# pin8.write(ang[1,2])
	# pin9.write(ang[2,2])
	# pin10.write(ang[0,3])
	# pin11.write(ang[1,3])
	# pin12.write(ang[2,3])
		print(x)
		s.write(x)

def gait(bodyDim,bodyState,initialToePos,vel,omega,T,beta,phi,t,delta_t):

	tempToePos = np.zeros((3,4))
	tempToePos[:,0] = moveLeg(bodyDim,initialToePos[:,0], vel,omega,T,beta[0],phi[0],t,delta_t,leg = 'FR')
	tempToePos[:,1] = moveLeg(bodyDim,initialToePos[:,1], vel,omega,T,beta[1],phi[1],t,delta_t,leg = 'RR')
	tempToePos[:,2] = moveLeg(bodyDim,initialToePos[:,2], vel,omega,T,beta[2],phi[2],t,delta_t,leg = 'RL')
	tempToePos[:,3] = moveLeg(bodyDim,initialToePos[:,3], vel,omega,T,beta[3],phi[3],t,delta_t,leg = 'FL')

	return tempToePos

T = 2.0
t = 0.0
delta_t = 0.04

#---------------------Crawl-------------------
# beta = np.ones(4)*0.5
# phi = [0,0.75,0.25,0.5]

#---------------------Trot-----------------
beta = np.ones(4)*0.5
phi = [0,0.5,0,0.5]
i=0
while True:
	norm_t = limit(t/T,1.0001)
	vel=np.array([0,1,0])*.07
	omega=np.array([0,0,1])*0
	i+=.07
	# bodyState[2] = .24 + .05*np.sin(t)
	# bodyState[4] =  .1*np.sin(t)

	# if i%50 >25:
	# 	vel = np.array([0,1,0])*0.1 + 0*np.sin(i)*.7
	# 	omega = np.array([0,0,-1])*0.2

	toePos = gait(bodyDim,bodyState,toePos,vel,omega,T,beta,phi,norm_t,delta_t)
	ang = jointAngles(bodyState,toePos,bodyDim,legLengths)
	runBot(ang,t)

	t += delta_t
	time.sleep(delta_t*0.3)

# gait(bodyState,initialToePos,step,radius,T,delta)			
# "2/4/19"