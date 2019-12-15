import numpy as np



def multiplyMat(a = []):
    temp = np.diag([1,1,1,1])
    for n in range(len(a)):
        temp = temp.dot(a[n])
    return temp


def traMatrix(rotation,translation,isInverse=False):
    "transformationMatrix: traMatrix(rotation,translation,isInverse=False(default))"  # traMatrix.__doc__
    [a,b,c] = rotation

    T = np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0],[translation[0],translation[1],translation[2],1]],dtype=np.float16).T
    Tx = np.array([[1,0,0,0],[0,np.cos(a),np.sin(a),0],[0,-np.sin(a),np.cos(a),0],[0,0,0,1]],dtype=np.float16).T
    Ty = np.array([[np.cos(b),0,-np.sin(b),0],[0,1,0,0],[np.sin(b),0,np.cos(b),0],[0,0,0,1]],dtype=np.float16).T
    Tz = np.array([[np.cos(c),np.sin(c),0,0],[-np.sin(c),np.cos(c),0,0],[0,0,1,0],[0,0,0,1]],dtype=np.float16).T
    
    transformation=multiplyMat([T,Tz,Ty,Tx])

    if isInverse: #transformation=npla.inv(transformation)
        rm=transformation[0:3,0:3].T
        tra=-rm.dot(transformation[0:3,3])
        invMat=np.append(np.append(rm.T,[tra],axis=0).T,[[0,0,0,1]],axis=0)
        transformation=invMat
    return transformation


def jointAngles(bodyState,toePos,bodyDim,legLengths):
    "bodyState and toePos in world frame, legLengths is 3x4 matrix"

    def angles(L,V,S):
        "angles(linkLength,Vector,originShift)"
        [x,y,z] = [-(V[2]-S[2]),-(V[0]-S[0]),(V[1]-S[1])];
        [l1,l2,l3] = [L[0],L[1],L[2]]
        z = z-l1

        th1 = np.arctan2(y,x)

        r = np.sqrt(x**2+y**2)
        R = np.sqrt(r**2+z**2)
        a1 = np.arctan2(z,r)

        var1 = ((R**2)+(l2**2)-(l3**2))/(2*R*l2)
        var2 = ((l2**2)+(l3**2)-(R**2))/(2*l2*l3)

        if abs(var1)>1: var1=var1/abs(var1)
        if abs(var2)>1: var2=var2/abs(var2)
        a2 = np.arccos(var1)
        a3 = np.arccos(var2)

        th2 = a1-a2
        th3 = np.pi-a3
        return [th1,th2,th3]

    orien = bodyState[3:6]
    pos = bodyState[0:3]
    l,w = bodyDim

    world2body = traMatrix(orien,pos,isInverse=True)

    ToePosinWorld = np.append(toePos,[[1,1,1,1]],axis=0)
    ToePosinBody = world2body.dot(ToePosinWorld)

    frToePosinBody = ToePosinBody[0:3,0]
    rrToePosinBody = ToePosinBody[0:3,1]
    rlToePosinBody = ToePosinBody[0:3,2]
    flToePosinBody = ToePosinBody[0:3,3]

    frA = angles(legLengths[:,0],frToePosinBody,[w/2,l/2,0])
    rrA = angles(legLengths[:,1],rrToePosinBody,[w/2,-l/2,0])
    rlA = angles(legLengths[:,2],rlToePosinBody,[-w/2,-l/2,0])
    flA = angles(legLengths[:,3],flToePosinBody,[-w/2,l/2,0])

    return np.array(np.mat([frA,rrA,rlA,flA]).T,dtype=np.float16)


# def secondPoint(firstPoint,bodyDim,step,radius,isLeft ,isFront ,onGround ):
#     l,w = bodyDim
#     r = radius
#     th1 = np.arctan(0.5*l/(r-0.5*w))
#     th2 = np.arctan(0.5*l/(r+0.5*w))
    
#     temp = np.zeros(3)
#     temp[0] = firstPoint[0] - (-onGround)*(2*isFront-1)*step*np.sin( th1*(isLeft) + th2*(1-isLeft) )
#     temp[1] = firstPoint[1] + (-onGround)*step*np.cos( th1*(isLeft) + th2*(1-isLeft) )
#     temp[2] = firstPoint[2]

#     point = temp
#     return point

def secondPoint(bodyDim,step,vel,omega,leg):
	l,w = bodyDim
	if leg == 'FR':
		l,w = l,w
	elif leg == 'RR':
		l,w = -l,w
	elif leg == 'RL':
		l,w = -l,-w
	elif leg == 'FL':
		l,w = l,-w
	step = .06
	shoulderPos = np.array([w/2.0, l/2.0, 0])
	V = vel + np.cross(omega,shoulderPos)
	mag_V = np.sqrt(sum(i**2 for i in V))
	if mag_V==0:
		nextPos = shoulderPos
	else:
		nextPos = shoulderPos + step*V/mag_V
	return nextPos


def liftedLeg(bodyDim,SP,vel,omega,T,beta,t,delta_t,leg):
    
    step = 0.4*np.sqrt(sum(i**2 for i in (vel + np.cross(omega,SP))))
    temp = np.array(SP).copy()
    
    V = (vel + np.cross(omega,[SP[0],SP[1],0]))*(beta/(1-beta))
   
    temp[2] = step*np.sin(t*np.pi/(1-beta))

    t = delta_t/(1-beta-t)*T
    finalPos = secondPoint(bodyDim,step,vel,omega,leg)
    temp[0:2] = (1-t)*SP[0:2] + t*finalPos[0:2]

    # temp[0] = SP[0]+V[0]*delta_t
    # temp[1] = SP[1]+V[1]*delta_t
    # temp[2] = 0.6*step*np.sin(t*np.pi/(1-beta))

    nextPos = temp
    # print nextPos,leg
    return nextPos

def groundLeg(SP,vel,omega,delta_t):
    nextPoint =SP.copy()
    nextPoint=SP - vel*delta_t - np.cross(omega,SP)*delta_t
    return nextPoint

def limit(a,a_max):
    temp = a-a_max*int(a/a_max)
    return round(temp,5)


def moveLeg(bodyDim,SP,vel,omega,T,beta,phi,t,delta_t,leg):

    if (t>=limit(phi+beta , 1)) and (t<limit(phi+beta+(1-beta),1.00001)):
        t = limit(t,1-beta)
        nextPos = liftedLeg(bodyDim,SP,vel,omega,T,beta,t,delta_t,leg)
    else:
        nextPos = groundLeg(SP,vel,omega,delta_t)

    return nextPos
    

def initToePos(bodyDim, bodyState):
    [l,w]=bodyDim
    orien=bodyState[3:6]
    pos=bodyState[0:3]
    r=np.sqrt(w**2+l**2)/2.0
    alpha=np.arctan(l/w)

    frToePos=[pos[0]+w*0.5,pos[1]+l*0.5,0]
    rrToePos=[pos[0]+w*0.5,pos[1]-l*0.5,0]
    rlToePos=[pos[0]-w*0.5,pos[1]-l*0.5,0]
    flToePos=[pos[0]-w*0.5,pos[1]+l*0.5,0]
    toePos=np.array([frToePos,rrToePos,rlToePos,flToePos],dtype=np.float16).T

    
    return toePos


