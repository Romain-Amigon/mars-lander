
import sys
import math
import random as rd
import time
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.cm as cm

# Save the Planet.
# Use less Fossil Fuel.


l_chrom=80
Npop=200
TIME=0.08
#To run your python code, you must construct a class Program with a constructor and a function runTurn
class Program:
    #The constructor takes in an argument land, which is a list of [x, y] of every ground point
    def __init__(self, land):
        self.obj = ((0,0),(0,0))
        prex,prey=-1,-1
        self.ground=[]
        for land_x, land_y in land:
            # land_x: X coordinate of a surface point. (0 to 6999)
            # land_y: Y coordinate of a surface point. By linking all the points together in a sequential fashion, you form the surface of Mars.
            self.ground.append((land_x,land_y))
            
            if land_y==prey:
                self.obj=((prex,prey),(land_x,land_y))
            prex=land_x
            prey=land_y
    
    
    	#The function runTurn takes in an argument with the seven integers read at each game turn
    	#It must return a vector of two integers [angle, power], printing these values will do nothing
    def runTurn(self, inputValues):
        x, y, hs, vs, f, r, p = inputValues
        state=State(x,y,hs,vs,f,-r,p,self.obj,self.ground)
        
        ((a,b),(na,nb))=self.obj
        
        if vs:t=round((y-b)/vs)
        else: t=999999
        if abs(hs)>40:
            print("vitesse eleve")
            return(35*hs/abs(hs),4)
        
        if a<x<na and( 0<=hs*t<na-x or hs*t<x-a):
            print('JDIJSC0NSC')
            if vs<-35:return [0,4]
            else:return[0,3]
            
        if y<b+50:
            print("basse altitude")
            return(0,4)
    
        
        chrom=Evolution(state)
        print([chrom.chromosome[0].angle, chrom.chromosome[0].power])
        plt.show()
        # R P. R is the desired rotation angle. P is the desired thrust power.
        return  [-chrom.chromosome[0].angle, chrom.chromosome[0].power]
    


class State:

    def __init__(self,x,y,h_speed,v_speed,fuel,rotate,power,obj,ground):
        self.x=x
        self.y=y
        self.h_speed=h_speed
        self.v_speed=v_speed
        self.fuel=fuel
        self.rotate=rotate
        self.power=power
        self.obj=obj
        self.ground=ground
        self.mort=False
    
    def change(self,x,y,h_speed,v_speed,fuel,rotate,power):
        self.x=x
        self.y=y
        self.h_speed=h_speed
        self.v_speed=v_speed
        self.fuel=fuel
        self.rotate=rotate
        self.power=power

    def var(self):
        return [self.x,self.y, self.h_speed, self.v_speed, self.fuel, self.rotate, self.power,self.obj,self.ground]
    
    def copy(self):
        return State(self.x,self.y,self.h_speed,self.v_speed,self.fuel,self.rotate,self.power,self.obj,self.ground)
    
class Gene():
    def __init__(self,  power,angle,score=0):
        self.power=power
        self.angle=angle
        self.score=score

class Chromosome:
    def __init__(self,l_chrom=l_chrom):
        self.chromosome=[]
        """
        r=rd.random()
        if r<0.2:
            angle=
        elif r>0.8:
            angle=-45
        elif r<0.4:
            angle=-25
        elif r>0.6:
            angle=-25
        else: angle=0
        """
        angle=rd.randint(-30,30)
        power=0
        for i in range(l_chrom):

            angle=angle+rd.randint(-15,15)
            p4 = max(0.7,i / (l_chrom - 1)  )        # de 0 au début à 1 à la fin
            p3 = 1 - p4   -0.1
            
            r=rd.random() 
            
            if r<p3:power=max(0,power-1)
            elif r< p4: power=min(4,power+1) 
            power = rd.choices([3, 4], weights=[p3, p4])[0]
            self.chromosome.append(Gene(power, angle))
        
        self.score=0

    def croisement(self, chrom):
        
        """
        # Poids pour favoriser le parent le mieux noté
        if self.score + chrom.score == 0:
            r = 0.5
        else:
            r = self.score / (self.score + chrom.score)
    
        child = Chromosome(len(self.chromosome))
        for i in range(len(self.chromosome)):
            if rd.random() < 0.2:  # mutation
                # gène totalement nouveau
                child.chromosome[i] = Gene(
                    rd.randint(1, 4),
                    self.chromosome[i].angle + rd.randint(-15, 15)
                )
            else:
                # choisir un parent selon r
                if rd.random() < r:
                    parent_gene = self.chromosome[i]
                else:
                    parent_gene = chrom.chromosome[i]
                # *** nouvelle instance ***
                child.chromosome[i] = Gene(parent_gene.power, parent_gene.angle)
        return child

        
        """
        #print(self.score,chrom.score)
        #if self.score+chrom.score==0:r=rd.random()
        #else :r = self.score/(self.score+chrom.score) #rd.random()
        r=rd.random()
        child = Chromosome(len(self.chromosome))
        for i in range(len(self.chromosome)):
            g1 = self.chromosome[i]
            """
            if rd.random() < 0.1:  # mutation
                child.chromosome[i] = Gene(
                    rd.randint(1,4),
                    g1.angle + rd.randint(-15,15)
                )
            """
            if rd.random() > 0.2:
                g2 = chrom.chromosome[i]
                child.chromosome[i] = Gene(
                    max(0, min(4, round(r*g1.power + (1-r)*g2.power +0.5))),
                    round(r*g1.angle + (1-r)*g2.angle)
                )
        return child
        
    
    def newt_iter(self):
        self.chromosome= self.chromosome[1:]+[Gene(rd.randint(0,4),self.chromosome[-1].angle+rd.randint(-15,15))]
        return self
        


def has_landed(state):
    x, y, h_speed, v_speed, fuel, rotate, power, obj, ground = state.var()
    (a, b), (na, nb) = obj
    return (a <= x <= na) and (y <= b) and (abs(h_speed) <= 20) and (abs(v_speed) <= 40) and (rotate == 0)

def J(state): 
    x, y, h_speed, v_speed, fuel, rotate, power,obj,ground=state.var() 
    score=20-abs(v_speed+20) +math.log(max(1,y+50))
    score=0
    
 
    a,b=obj[0] 
    na,nb=obj[1] 
    if a<x<na:
        
        score+=1400
        if y<b:
            score-=b-y
        
        
        if abs(h_speed)<18:
            score+=2800
            
            score+=10*(100+ 38 - abs(v_speed) )
            """
            if rotate==0:
                score+=900
                
                if abs(v_speed)<38 :
                    score+=1000
                
                else :score+=100+ 38 -2* abs(v_speed) 
            
            else : score +=271-3*abs(rotate)
            """
        
        else : score+= 500+18 - abs(h_speed)
            
                    
        """
        if abs(v_speed)<41 and abs(h_speed)<21:
            score+=300
            score+=180-abs(rotate)
        
        else : 
            if abs(v_speed)>40: score+=100+ 41 - abs(v_speed) 
            if abs(h_speed)>20 : score+= 100+21 - abs(h_speed)
        """
        
        
    else : score+=700-min( abs(a-x), abs(x-na) )/10 #•100*math.exp( -(min( abs(a-x), abs(x-na) )/500)**2) 
      #print(score, x)
    return score





def Evolution(state, Npop=Npop):
    pop =[Chromosome() for _ in range(Npop)]

    start=time.time()

    while time.time()-start<TIME:
        ## SIMULATION
        total=0
        
        Coord=[]
        
        for chrom in pop:

            new_state=state.copy()
            C=[]
            for gene in chrom.chromosome:

                new_x, new_y, new_h_speed, new_v_speed, new_fuel, new_rotate, new_power = next_position(new_state,gene.angle,gene.power)
                C.append((new_x,new_y))
                if mort(new_state,new_x,new_y):
                    new_state=State(new_x, new_y, new_h_speed, new_v_speed, new_fuel, new_rotate, new_power, state.obj,state.ground)
                    score=max(0,J(new_state)-200)
                    
                    break

                new_state=State(new_x, new_y, new_h_speed, new_v_speed, new_fuel, new_rotate, new_power, state.obj,state.ground)
                
                if has_landed(new_state):
                    print("AAAAAAAAAAAAAA", file=sys.stderr, flush=True)
                    pause(1)
                    return chrom
                
                score=J(new_state)
                
            chrom.score=score
            Coord.append(C)
            total+=chrom.score
        
        for i in range(len(state.ground)-1):
            plt.plot([state.ground[i][0],state.ground[i+1][0]],[state.ground[i][1],state.ground[i+1][1]], color='red')
        
        
        
        ## SELECTION

        if total==0:continue

        
        Sort= sorted(pop, key=lambda x:-x.score)
        #print([i.score for i in Sort])

        l=int(Npop/20)
        
        new_pop=[]
        
        for i in range(l):
            new_pop.append(Sort[i].newt_iter())
        
        for i in range(l, Npop-l):
            p1 = tournament(pop,int(Npop/10))
            p2 = tournament(pop,int(Npop/10))
            #print(p1.score, p2.score)
            new_pop.append(p1.croisement(p2))
            #print(i,len(Sort),Npop, file=sys.stderr, flush=True)
            #○new_pop.append(Sort[i].croisement(rd.choice(Sort)))
        
        
        for i in range(l):
            new_pop.append(Chromosome())
        
        """
        for i in range(l-1, Npop-1):
            #print(i,len(Sort),Npop, file=sys.stderr, flush=True)
            new_pop.append(Sort[i].croisement(Sort[i+1]))
        """
        pop=new_pop
    
    rep=Sort[0]
    
    scores = [chrom.score for chrom in pop]
    if scores:  # éviter division par zéro
        norm = mcolors.Normalize(vmin=min(scores), vmax=max(scores))
        cmap = cm.RdYlGn   # ou 'viridis', 'cool', etc.
    
        for chrom, traj in zip(pop, Coord):
            xs = [p[0] for p in traj]
            ys = [p[1] for p in traj]
    
            # couleur en fonction du score, normalisée entre 0 et 1
            color = cmap(norm(chrom.score))
            plt.plot(xs, ys, color=color, alpha=0.5)        
        
    
    C=[]
    new_state=state.copy()
    for gene in rep.chromosome:

        new_x, new_y, new_h_speed, new_v_speed, new_fuel, new_rotate, new_power = next_position(new_state,gene.power,gene.angle)
        C.append((new_x,new_y))
        if mort(new_state,new_x,new_y):
            new_state=State(new_x, new_y, new_h_speed, new_v_speed, new_fuel, new_rotate, new_power, state.obj,state.ground)
            score=max(0,J(new_state)-200)
            
            break
        new_state=State(new_x, new_y, new_h_speed, new_v_speed, new_fuel, new_rotate, new_power, state.obj,state.ground)

    xs = [p[0] for p in C]
    ys = [p[1] for p in C]


    plt.plot(xs, ys,'bo',color='green' , alpha=0.5) 
    #plt.figure()
    plt.pause(0.01)  # mettre à jour le graphique
    return rep


    


def tournament(pop, k=3):
    return max(rd.sample(pop, k), key=lambda c: c.score)

        


def next_position(state:State, new_rotate, new_power):
    """
    Calcule la prochaine position et l'état du vaisseau après un tour.
    
    Entrées :
        x (float) : position horizontale (m)
        y (float) : position verticale (m)
        h_speed (float) : vitesse horizontale (m/s)
        v_speed (float) : vitesse verticale (m/s)
        fuel (int) : carburant restant (litres)
        rotate (int) : angle actuel (degrés, -90 à 90)
        power (int) : puissance actuelle (0 à 4)
        new_rotate (int) : nouvel angle souhaité (degrés, -90 à 90)
        new_power (int) : nouvelle puissance souhaitée (0 à 4)
    
    Sortie :
        tuple (new_x, new_y, new_h_speed, new_v_speed, new_fuel, new_rotate, new_power)
        - new_x, new_y : nouvelle position (m)
        - new_h_speed, new_v_speed : nouvelles vitesses (m/s)
        - new_fuel : carburant restant (litres)
        - new_rotate : angle appliqué (degrés)
        - new_power : puissance appliquée
    """
    x, y, h_speed, v_speed, fuel, rotate, power,obj,ground=state.var()
    # Constantes
    GRAVITY = -3.711  # Gravité de Mars (m/s², négative car vers le bas)
    MAX_ROTATE_CHANGE = 15  # Changement max d'angle par tour
    MAX_POWER_CHANGE = 1  # Changement max de puissance par tour
    
    # Appliquer les contraintes sur la rotation et la puissance
    new_rotate = max(min(new_rotate, rotate + MAX_ROTATE_CHANGE), rotate - MAX_ROTATE_CHANGE)
    new_rotate = max(min(new_rotate, 90), -90)
    
    new_power = max(min(new_power, power + MAX_POWER_CHANGE), power - MAX_POWER_CHANGE)
    new_power = max(min(new_power, 4), 0)
    
    # Si plus de carburant, forcer la puissance à 0
    if fuel <= 0:
        new_power = 0
    
    # Calcul de l'accélération due à la poussée
    thrust = new_power  # Poussée en m/s²
    angle_rad = math.radians(new_rotate)  # Convertir l'angle en radians
    ax = thrust * math.sin(angle_rad)  # Accélération horizontale
    ay = thrust * math.cos(angle_rad) + GRAVITY  # Accélération verticale (avec gravité)
    
    # Mise à jour des vitesses (v = v0 + a * t, t = 1s)
    new_h_speed = h_speed + ax
    new_v_speed = v_speed + ay
    
    # Mise à jour de la position (x = x0 + v * t, t = 1s)
    new_x = x + h_speed + ax/2
    new_y = y + v_speed + ay/2
    
    # Mise à jour du carburant
    new_fuel = fuel - new_power if fuel > 0 else 0
    
    # S'assurer que la position reste dans les limites
    #new_x = max(0, min(new_x, 6999))
    #new_y = max(0, min(new_y, 2999))
    
    return (new_x, new_y, new_h_speed, new_v_speed, new_fuel, new_rotate, new_power)


def segments_intersect(x1, y1, x2, y2, a1, b1, a2, b2):
    """
    Vérifie si les segments [(x1, y1), (x2, y2)] et [(a1, b1), (a2, b2)] se croisent.
    Retourne True si les segments se croisent à l'intérieur, False sinon.
    
    Args:
        x1, y1: Coordonnées du premier point du premier segment
        x2, y2: Coordonnées du second point du premier segment
        a1, b1: Coordonnées du premier point du second segment
        a2, b2: Coordonnées du second point du second segment
    
    Returns:
        bool: True si les segments se croisent, False sinon
    """
    def orientation(p1x, p1y, p2x, p2y, p3x, p3y):
        """Calcule l'orientation du triplet (p1, p2, p3).
        Retourne:
            0 si colinéaire,
            > 0 si sens horaire,
            < 0 si sens antihoraire.
        """
        val = (p2y - p1y) * (p3x - p2x) - (p2x - p1x) * (p3y - p2y)
        if val == 0:
            return 0  # Colinéaire
        return 1 if val > 0 else -1  # Horaire ou antihoraire

    def on_segment(px, py, qx, qy, rx, ry):
        """Vérifie si le point r est sur le segment [p, q]."""
        return (min(px, qx) <= rx <= max(px, qx) and
                min(py, qy) <= ry <= max(py, qy))

    # Calculer les orientations
    o1 = orientation(x1, y1, x2, y2, a1, b1)
    o2 = orientation(x1, y1, x2, y2, a2, b2)
    o3 = orientation(a1, b1, a2, b2, x1, y1)
    o4 = orientation(a1, b1, a2, b2, x2, y2)

    # Cas général : les segments se croisent si les orientations diffèrent
    if o1 != o2 and o3 != o4:
        return True

    # Cas particuliers : points colinéaires
    # Vérifier si un point d'un segment est sur l'autre segment
    if o1 == 0 and on_segment(x1, y1, x2, y2, a1, b1):
        return True
    if o2 == 0 and on_segment(x1, y1, x2, y2, a2, b2):
        return True
    if o3 == 0 and on_segment(a1, b1, a2, b2, x1, y1):
        return True
    if o4 == 0 and on_segment(a1, b1, a2, b2, x2, y2):
        return True

    return False

def mort(state,newx,newy):
    x, y, h_speed, v_speed, fuel, rotate, power,obj,ground=state.var()
    if newx>7000 or newx<0: return True

    for i in range(len(ground)-1):
        a,b=ground[i]
        na,nb=ground[i+1]

        if segments_intersect(x,y,newx,newy,a,b,na,nb):
            if rotate!=0: return True
            if abs(v_speed)>40 : return True
            if abs(h_speed)>20 : return True
            if not(a <= newx <= na) : return True
    return False



def c(x):
    a=4000
    na=5500
    return 100*math.exp( -(min( abs(a-x), abs(x-na) )/500)**2) 
