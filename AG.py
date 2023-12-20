import random as rd

import numpy as np

def pop(n):
    Pop= []

    for k in range(n):
        G=[]
        a=0
        
        for i in range(80):
            
            a=rd.randint(-15,15)+a
            b=rd.randint(0,4)
            
            if abs(a)>30:
                a=80*a/(abs(a))
            
            if i>25 :
                a=rd.randint(-15,15)
                
                
            
            
            
            G.append((a,b))
            #♣G.append((0,4))
            
        Pop.append(G)
            
        
    return Pop



def score(i,Reuss,x1,x2,h):
    s=0
    
    Pos=i[1]
    if Pos in Reuss :
        s+=1000000
    
    
    x,y,vy,vx,teta=Pos[-1]
    
    a= ( (x-x1)**2 )**0.5
    b= ( (x-x2)**2  )**0.5
    
    d= min(a,b)
    
    
    if y<h-200:
        
        s-=10000
    #s+=100/(abs(teta)+0.5)
    
    if x>=x1 and x<=x2 and y>h:
        s+=100/(abs(teta)+0.1)
        
        if vx<20 and teta==0:
            s+=10000000
        if vy>-40:
            s+=10000
        else:
            s+= 10
        
    
    
        
    
    s+= 10000/(d +100)   
    return s
    
    
def mutation(S):
    X=[]
    somme=0
    total=0
    A=[]
    b=1
    for i in S:
        somme+= i[1]
    
    for i in S:
        c=round((i[1]*100)/somme)
        A.append( ( i[0], [b,total+c] ) )
        
        b=c+total
        total+=b

    
    
    
    for i in range(len(S)):
        
        
        Pop=[(rd.randint(-15,15),rd.randint(2,4)) for k in range(80)]
        
        for j in range(80) :
            
            x=rd.randint(1,100)
            
            for k in A:
                
                if k[1][0]<=x and k[1][1]>x:
                    Pop[j] = k[0][ j ]
                    break
              
        
        X.append(Pop)
            
        
    
    
    return X
            

        