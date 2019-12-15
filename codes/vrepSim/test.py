from lib import *
import numpy as np
import matplotlib.pyplot as plt
import time,sys,vrep
import threading


# fig,ax=plt.subplots()

# for t in np.arange(0,.75,.02):
#   x=moveLeg([0,0,0],[2,0,0],t)
#   ax.plot(x[0],x[2],'ob')
# plt.show()


global Vxy,state
state = 0
Vxy = [0,0]

def parse(resp):    
    resp = str(resp)
    data = resp.split('''\\r\\n\\r\\n''')[1]
    data = data.split(";")
    x = data[0]
    y = data[1]
    return [int(x),int(y[:-1])]
def th1():
    # first of all import the socket library 
    import socket       

     
    global Vxy,clientID,connectionID,state
    # next create a socket object 
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)        
    print ("Socket successfully created")

    # reserve a port on your computer in our 
    # case it is 12345 but it can be anything 
    port = 12312      

    # Next bind to the port 
    # we have not typed any ip in the ip field 
    # instead we have inputted an empty string 
    # this makes the server listen to requests 
    # coming from other computers on the network 
    s.bind(('', port))       
    print ("socket binded to %s" %(port) )

    # put the socket into listening mode 
    s.listen(5)  
    print ("socket is listening")           

    # a forever loop until we interrupt it or 
    # an error occurs 
    while True: 

        if state==1:

            x._Thread_stop()
            c.close() 
            break
        # Establish connection with client.
        c, addr = s.accept() 
        c.settimeout(2)

        # send a thank you message to the client. 
        data =  c.recv(2048)
        Vxy = parse(data)
        # Close the connection with the client 
        c.close() 


x = threading.Thread(target=th1)
x.start()
#--------------------------V-REP Connection-------------------------------

vrep.simxFinish(-1) # just in case, close all opened connections
global clientID,connectionID
print ("Trying to connect......")
clientID=vrep.simxStart('127.0.0.1',9999,True,True,5000,5) # Connect to V-REP
connectionID=vrep.simxGetConnectionId(clientID)
if clientID!=-1:
    print ('Connected to remote API server')
else:
    print( "Could not connect")
    sys.exit("Error: could not connect")
    time.sleep(1)


#--------------------------Handles-------------------------------

eCode,Body=vrep.simxGetObjectHandle(clientID,'base',vrep.simx_opmode_oneshot_wait)
eCode,frForce=vrep.simxGetObjectHandle(clientID,'FR_force',vrep.simx_opmode_oneshot_wait)
eCode,dummy=vrep.simxGetObjectHandle(clientID,'Dummy',vrep.simx_opmode_oneshot_wait)


eCode,frRoll=vrep.simxGetObjectHandle(clientID,'FR_roll',vrep.simx_opmode_oneshot_wait)
eCode,frPitch=vrep.simxGetObjectHandle(clientID,'FR_pitch',vrep.simx_opmode_oneshot_wait)
eCode,frKnee=vrep.simxGetObjectHandle(clientID,'FR_knee',vrep.simx_opmode_oneshot_wait)
eCode,rrRoll=vrep.simxGetObjectHandle(clientID,'RR_roll',vrep.simx_opmode_oneshot_wait)
eCode,rrPitch=vrep.simxGetObjectHandle(clientID,'RR_pitch',vrep.simx_opmode_oneshot_wait)
eCode,rrKnee=vrep.simxGetObjectHandle(clientID,'RR_knee',vrep.simx_opmode_oneshot_wait)
eCode,rlRoll=vrep.simxGetObjectHandle(clientID,'RL_roll',vrep.simx_opmode_oneshot_wait)
eCode,rlPitch=vrep.simxGetObjectHandle(clientID,'RL_pitch',vrep.simx_opmode_oneshot_wait)
eCode,rlKnee=vrep.simxGetObjectHandle(clientID,'RL_knee',vrep.simx_opmode_oneshot_wait)
eCode,flRoll=vrep.simxGetObjectHandle(clientID,'FL_roll',vrep.simx_opmode_oneshot_wait)
eCode,flPitch=vrep.simxGetObjectHandle(clientID,'FL_pitch',vrep.simx_opmode_oneshot_wait)
eCode,flKnee=vrep.simxGetObjectHandle(clientID,'FL_knee',vrep.simx_opmode_oneshot_wait)

global jointHandles
jointHandles = [[frRoll,rrRoll,rlRoll,flRoll],[frPitch,rrPitch,rlPitch,flPitch],[frKnee,rrKnee,rlKnee,flKnee]]


global bodyDim,legLengths
bodyDim=[0.5,0.3]
bodyState = [0,0,0.2, 0,0,0]

LL=[0.0, 0.1,0.16]
legLengths=np.array([LL,LL,LL,LL]).T

toePos = initToePos(bodyDim,bodyState)
step = .07
radius = 2
T=1.0
delta = 0.01



def runVrep(clientID,jointHandles,ang):
    """
    ang=  [ frRoll,  rrRoll,  rlRoll,  flRoll
            frPitch, rrPitch, rlPitch, flPitch
            frKnee,  rrKnee,  rlKnee,  flKnee ]
    
    jointHandles= [ frRoll,  rrRoll,  rlRoll,  flRoll
                   frPitch, rrPitch, rlPitch, flPitch
                   frKnee,  rrKnee,  rlKnee,  flKnee ]
    """


    [[frRoll,rrRoll,rlRoll,flRoll],[frPitch,rrPitch,rlPitch,flPitch],[frKnee,rrKnee,rlKnee,flKnee],] = jointHandles


    vrep.simxPauseCommunication(clientID,1)
    vrep.simxSetJointTargetPosition(clientID, frRoll, ang[0,0], vrep.simx_opmode_oneshot)
    vrep.simxSetJointTargetPosition(clientID, frPitch, ang[1,0], vrep.simx_opmode_oneshot)
    vrep.simxSetJointTargetPosition(clientID, frKnee, ang[2,0], vrep.simx_opmode_oneshot)
    vrep.simxSetJointTargetPosition(clientID, rrRoll, ang[0,1], vrep.simx_opmode_oneshot)
    vrep.simxSetJointTargetPosition(clientID, rrPitch, ang[1,1], vrep.simx_opmode_oneshot)
    vrep.simxSetJointTargetPosition(clientID, rrKnee, ang[2,1], vrep.simx_opmode_oneshot)
    vrep.simxSetJointTargetPosition(clientID, rlRoll, ang[0,2], vrep.simx_opmode_oneshot)
    vrep.simxSetJointTargetPosition(clientID, rlPitch, ang[1,2], vrep.simx_opmode_oneshot)
    vrep.simxSetJointTargetPosition(clientID, rlKnee, ang[2,2], vrep.simx_opmode_oneshot)
    vrep.simxSetJointTargetPosition(clientID, flRoll, ang[0,3], vrep.simx_opmode_oneshot)
    vrep.simxSetJointTargetPosition(clientID, flPitch, ang[1,3], vrep.simx_opmode_oneshot)
    vrep.simxSetJointTargetPosition(clientID, flKnee, ang[2,3], vrep.simx_opmode_oneshot)
    vrep.simxPauseCommunication(clientID,0)


'''
def gait(bodyState,initialToePos,step,radius,T,delta):

    finalToePos = np.zeros((3,4))
    finalToePos[:,0] = secondPoint(initialToePos[:,0],bodyDim,step,radius,isLeft=0, isFront=1, direction=1 )
    finalToePos[:,1] = secondPoint(initialToePos[:,1],bodyDim,step,radius,isLeft=0, isFront=0, direction=-1 )
    finalToePos[:,2] = secondPoint(initialToePos[:,2],bodyDim,step,radius,isLeft=1, isFront=0, direction=1 )
    finalToePos[:,3] = secondPoint(initialToePos[:,3],bodyDim,step,radius,isLeft=1, isFront=1, direction=-1 )


    tempToePos = initialToePos.copy()

    for t in np.arange(0,1,delta):


        tempToePos[:,0] = moveLeg(initialToePos[:,0], finalToePos[:,0],t,direction=1)
        tempToePos[:,1] = moveLeg(initialToePos[:,1],finalToePos[:,1],t,direction=-1)
        tempToePos[:,2] = moveLeg(initialToePos[:,2], finalToePos[:,2],t,direction=1)
        tempToePos[:,3] = moveLeg(initialToePos[:,3],finalToePos[:,3],t,direction=-1)

        ang = jointAngles(bodyState,tempToePos,bodyDim,legLengths)
        runVrep(clientID,jointHandles,ang)
        time.sleep(T*delta)

        print tempToePos
'''


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
beta = np.ones(4)*0.5
# phi = [0,0.75,0.25,0.5]
phi = [0,0.5,0,0.5]
i=0
while True:
    norm_t = limit(t/T,1.0001)
    # vel=np.array([-1,1,0])*.05
    vel = np.array([Vxy[0],Vxy[1],0])*.0005
    print(Vxy,vel)
    omega=np.array([0,0,1])*0
    i+=.07

    # if i%50 >25:
    #     vel = np.array([0,1,0])*0.0 + 0*np.sin(i)*.7
    #     omega = np.array([0,0,-1])*0.0

    toePos = gait(bodyDim,bodyState,toePos,vel,omega,T,beta,phi,norm_t,delta_t)
    ang = jointAngles(bodyState,toePos,bodyDim,legLengths)
    runVrep(clientID,jointHandles,ang)

    t += delta_t
    time.sleep(delta_t*.3)

    cid=vrep.simxGetConnectionId(clientID)
    if not cid==connectionID:
        state=1
        print ('connectionID :',cid)
        print ('server is not connected: main thread')
        x.kill()
        break

# gait(bodyState,initialToePos,step,radius,T,delta)         
# "2/4/19"