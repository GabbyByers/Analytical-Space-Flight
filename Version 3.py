import os, pygame.gfxdraw, pygame, math, random, time
pygame.init()
DisplayX, DisplayY = 1440,900
win = pygame.display.set_mode((DisplayX, DisplayY))
pygame.display.set_caption("template")
White = (255,255,255)
Label_White = (150,150,150)
Debug_White = (200,200,200)
Black = (0,0,0)
Back_Drop = (0,0,26)
Gray = (150,150,150)
Orbit_Gray = (60,60,60)
Moon_Gray = (100,100,110)
Blue = (0,0,255)
Green = (0,200,0)
Red = (255,30,30)
Purple = (255,0,255)
Yellow = (255,255,0)
Brown = (139,69,19)
Gold = (255,215,0)
font = pygame.font.SysFont('courier', 20, False)
key_font = pygame.font.SysFont('courier', 16, False)
label_font = pygame.font.SysFont('courier', 20, False)

I have made an edit here

class angle:
    def __init__(self, radians):
        self.radians = radians

    def normalize(self):
        if self.radians < -pi:
            while self.radians < -pi:
                self.radians += 2*pi
        if self.radians > pi:
            while self.radians > pi:
                self.radians += -2*pi

    def degress(self):
        return math.degrees(self.radians)

class box:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

#System Variables
Toggle_Stars = True
Debug_Toggle = True
Label_Toggle = True
Vector_Toggle = True
pi = 3.141592653589793
G = 6.67408*10**-11
GlobalX,GlobalY = 0,0
Iterations = 200
Angular_Momentum,Angular_Impulse = 0,0.01
TimeWarp_Maximum = 9
TimeWarp_Value = 1
TimeWarp = 10**(TimeWarp_Value-1)
System_Scale = 1/20000
Sphere_Influence = "Earth"
Label_Size = 15
DeltaV_Consumed = 0

#Planets
Mass_Earth = 5.972     *10**24
Mass_Moon  = 7.34767309*10**22
Radius_Earth = 6.371 *10**6
Velocity_Moon = 1017.8
Radius_Moon  = 1.7374*10**6
Orbital_Radius_Moon = 384748000
Orbital_Period_Moon = 2360620
Sphere_Influence_Radius = 66100000

#Ship
Dist_Earth = 10000000
Dist_Moon = 0
Velocity = 6500
Engine_Impulse = 200

#Base Angles
Earth_TO_Ship = angle(1)
Moon_TO_Ship = angle(0)
Earth_TO_Moon = angle(-0.8)
Moon_TO_Earth = angle(0)
X_TO_Vel = angle(-0.5)
X_TO_Impulse = angle(-1)
True_Anomaly = angle(0)

#Derived Angles
Ship_TO_Earth = angle(0)
Ship_TO_Moon = angle(0)
EarthShip_TO_Vel = angle(0)
MoonShip_TO_Vel = angle(0)
Vel_TO_Impulse = angle(0)
Impulse_TO_Vel = angle(0)
X_TO_MoonVel = angle(0)
ShipVel_TO_MoonVel = angle(0)

#Navigation Window
RocketPolygon = [(9.5,-1),(5.5,-4),(2.5,-4),(1.5,-5),(0.5,-5),(-0.5,-4),(-3.5,-4),(-3.5,-2),(-5.5,-1),(-9.5,-2),(-9.5,2),(-5.5,1),(-3.5,2),(-3.5,4),(-0.5,4),(0.5,5),(1.5,5),(2.5,4),(5.5,4),(9.5,1)]
RocketScale = 10
Toggle_Navigation = box(20,20,30,30)
Navigation        = box(650,570,(2*Toggle_Navigation.x+Toggle_Navigation.width,300),(2*Toggle_Navigation.y+Toggle_Navigation.height,300))
Minus             = box(3,12,24,6)
Plus              = box(Minus.y,Minus.x,Minus.height,Minus.width)
MouseOver = "None"
MouseDown = "None"
Minimized = False

def panNavigation():
    if MouseDown == "Navigation":
        Navigation.x += Mouse_RelX
        Navigation.y += Mouse_RelY
        if Navigation.x < 0:
            Navigation.x = 0
        if Navigation.y < 0:
            Navigation.y = 0
        if Minimized:
            if Navigation.x + Navigation.width[0] > DisplayX:
                Navigation.x = DisplayX - Navigation.width[0]
            if Navigation.y + Navigation.height[0] > DisplayY:
                Navigation.y = DisplayY - Navigation.height[0]
        elif not Minimized:
            if Navigation.x + Navigation.width[1] > DisplayX:
                Navigation.x = DisplayX - Navigation.width[1]
            if Navigation.y + Navigation.height[1] > DisplayY:
                Navigation.y = DisplayY - Navigation.height[1]

def drawNavigation():
    if Minimized:
        pygame.draw.rect(win, Black, (Navigation.x,Navigation.y,Navigation.width[0],Navigation.height[0]))
        if MouseDown == "Navigation":
            pygame.draw.rect(win, Green, (Navigation.x,Navigation.y,Navigation.width[0],Navigation.height[0]), 1)
        elif not MouseDown == "Navigation":
            pygame.draw.rect(win, White, (Navigation.x,Navigation.y,Navigation.width[0],Navigation.height[0]), 1)
    elif not Minimized:
        pygame.draw.rect(win, Black, (Navigation.x,Navigation.y,Navigation.width[1],Navigation.height[1]))
        if MouseDown == "Navigation":
            pygame.draw.rect(win, Green, (Navigation.x,Navigation.y,Navigation.width[1],Navigation.height[1]), 1)
        elif not MouseDown == "Navigation":
            pygame.draw.rect(win, White, (Navigation.x,Navigation.y,Navigation.width[1],Navigation.height[1]), 1)
    pygame.draw.rect(win, White, (Toggle_Navigation.x+Navigation.x,Toggle_Navigation.y+Navigation.y,Toggle_Navigation.width,Toggle_Navigation.height), 1)
    pygame.draw.rect(win, White, (Toggle_Navigation.x+Navigation.x+Minus.x,Toggle_Navigation.y+Navigation.y+Minus.y,Minus.width,Minus.height))
    if Minimized:
        pygame.draw.rect(win, White, (Toggle_Navigation.x+Navigation.x+Plus.x,Toggle_Navigation.y+Navigation.y+Plus.y,Plus.width,Plus.height))

def drawRocket():
    if not Minimized:
        pygame.draw.lines(win, White, True, rotateScaleTranslateList(RocketPolygon), 1)
        if Accelerating:
            PlumePolygon = [(-10.5,-1.7),(-10.5,1.7)]
            x0 = -15 + (2*random.randrange(1000)/1000)
            PlumePolygon.append((x0,0))
            pygame.draw.lines(win, White, True, rotateScaleTranslateList(PlumePolygon), 1)

def drawRightPlume():
    if not Minimized:
        RCSPlume0 = [(0,-4.5)]
        RCSPlume1 = [(2,4.5)]
        x0 = -2.5 + (random.randrange(1000)/1000)
        y0 = -6 + (random.randrange(1000)/1000)
        RCSPlume0.append((x0,y0))
        x1 = 3.5 + (random.randrange(1000)/1000)
        y1 = 5 + (random.randrange(1000)/1000)
        RCSPlume1.append((x1,y1))
        pygame.draw.line(win, White, (rotateScaleTranslateList(RCSPlume0)[0]), (rotateScaleTranslateList(RCSPlume0)[1]), 1)
        pygame.draw.line(win, White, (rotateScaleTranslateList(RCSPlume1)[0]), (rotateScaleTranslateList(RCSPlume1)[1]), 1)

def drawLeftPlume():
    if not Minimized:
        RCSPlume0 = [(2,-4.5)]
        RCSPlume1 = [(0,4.5)]
        x0 = 3.5 + (random.randrange(1000)/1000)
        y0 = -6 + (random.randrange(1000)/1000)
        RCSPlume0.append((x0,y0))
        x1 = -2.5 + (random.randrange(1000)/1000)
        y1 = 5 + (random.randrange(1000)/1000)
        RCSPlume1.append((x1,y1))
        pygame.draw.line(win, White, (rotateScaleTranslateList(RCSPlume0)[0]), (rotateScaleTranslateList(RCSPlume0)[1]), 1)
        pygame.draw.line(win, White, (rotateScaleTranslateList(RCSPlume1)[0]), (rotateScaleTranslateList(RCSPlume1)[1]), 1)

def rotateScaleTranslateList(LIST):
    LIST0 = [(x*math.cos(X_TO_Impulse.radians)-y*math.sin(X_TO_Impulse.radians),(x*math.sin(X_TO_Impulse.radians)+y*math.cos(X_TO_Impulse.radians))) for (x,y) in LIST]
    LIST1 = [(Navigation.x+(Navigation.width[1]/2)+(x*RocketScale),Navigation.y+(Navigation.height[1]/2)+(y*RocketScale)) for (x,y) in LIST0]
    return LIST1

def determineMouseOver():
    global MouseOver
    MouseOver = "None"
    if Minimized:
        if (Navigation.x < MouseX < Navigation.x+Navigation.width[0]) and (Navigation.y < MouseY < Navigation.y+Navigation.height[0]):
            MouseOver = "Navigation"
    elif not Minimized:
        if (Navigation.x < MouseX < Navigation.x+Navigation.width[1]) and (Navigation.y < MouseY < Navigation.y+Navigation.height[1]):
            MouseOver = "Navigation"
    if (Navigation.x+Toggle_Navigation.x < MouseX < Navigation.x+Toggle_Navigation.x+Toggle_Navigation.width) and (Navigation.y+Toggle_Navigation.y < MouseY < Navigation.y+Toggle_Navigation.y+Toggle_Navigation.height):
        MouseOver = "Toggle Navigation"

def userControls():
    global GlobalX, GlobalY, System_Scale, Angular_Momentum, Accelerating
    global Turning_Left, Turning_Right
    Turning_Left, Turning_Right = False, False
    Accelerating = False
    if MouseDown == "None":
        if MouseLeft:
            GlobalX += Mouse_RelX
            GlobalY += Mouse_RelY
        if MouseScroll:
            System_Scale = System_Scale * (1+Mouse_RelY/1000)
    if TimeWarp == 1 and (Vector_Toggle or not Minimized):
        if keys[pygame.K_a]:
            Angular_Momentum += -Angular_Impulse*SPF
            Turning_Left = True
        if keys[pygame.K_d]:
            Angular_Momentum += Angular_Impulse*SPF
            Turning_Right = True
        if keys[pygame.K_s]:
            if Angular_Momentum > 0:
                Angular_Momentum += -Angular_Impulse*SPF
                Turning_Left = True
            if Angular_Momentum < 0:
                Angular_Momentum += Angular_Impulse*SPF
                Turning_Right = True
            if abs(Angular_Momentum) < Angular_Impulse*SPF:
                Angular_Momentum = 0
        if keys[pygame.K_w]:
            Accelerating = True

def timeWarp():
    global TimeWarp
    for n in range(TimeWarp_Maximum):
        offset = n*25
        pygame.draw.polygon(win, White, [(10+offset,10),(10+offset,30),(29+offset,20)], 1)
    for n in range(TimeWarp_Value):
        offset = n*25
        pygame.draw.polygon(win, White, [(10+offset,10),(10+offset,30),(29+offset,20)])
    TimeWarp = 10**(TimeWarp_Value-1)
    text = font.render("x"+str(TimeWarp), 1, White)
    win.blit(text, (TimeWarp_Maximum*25+15, 10))

def pixelValues():
    global Pixel_Ship_X,Pixel_Ship_Y,Pixel_Vel_X,Pixel_Vel_Y,Pixel_Impulse_X,Pixel_Impulse_Y,Pixel_Radius_Sphere_Influence
    global Pixel_Earth_X,Pixel_Earth_Y,Pixel_Radius_Earth,Pixel_Moon_X,Pixel_Moon_Y,Pixel_Radius_Moon,Pixel_Orbital_Radius_Moon
    #Ship
    Pixel_Ship_X = DisplayX//2 + GlobalX
    Pixel_Ship_Y = DisplayY//2 + GlobalY
    #Earth
    Pixel_Earth_X = Pixel_Ship_X+math.cos(Ship_TO_Earth.radians)*Dist_Earth*System_Scale
    Pixel_Earth_Y = Pixel_Ship_Y+math.sin(Ship_TO_Earth.radians)*Dist_Earth*System_Scale
    Pixel_Radius_Earth = Radius_Earth*System_Scale
    if Pixel_Radius_Earth < 1:
        Pixel_Radius_Earth = 1
    #Moon
    Pixel_Moon_X = Pixel_Earth_X+math.cos(Earth_TO_Moon.radians)*Orbital_Radius_Moon*System_Scale
    Pixel_Moon_Y = Pixel_Earth_Y+math.sin(Earth_TO_Moon.radians)*Orbital_Radius_Moon*System_Scale
    Pixel_Radius_Moon = Radius_Moon*System_Scale
    Pixel_Radius_Sphere_Influence = Sphere_Influence_Radius*System_Scale
    if Pixel_Radius_Moon < 1:
        Pixel_Radius_Moon = 1
    Pixel_Orbital_Radius_Moon = Orbital_Radius_Moon*System_Scale
    #Debug
    Pixel_Vel_X = Pixel_Ship_X+math.cos(X_TO_Vel.radians)*Velocity*0.02
    Pixel_Vel_Y = Pixel_Ship_Y+math.sin(X_TO_Vel.radians)*Velocity*0.02
    Pixel_Impulse_X = Pixel_Vel_X + math.cos(X_TO_Impulse.radians)*40
    Pixel_Impulse_Y = Pixel_Vel_Y + math.sin(X_TO_Impulse.radians)*40

def drawPlanets():
    pygame.draw.circle(win, White, (round(Pixel_Ship_X),round(Pixel_Ship_Y)), 2)
    pygame.draw.circle(win, Blue, (round(Pixel_Earth_X),round(Pixel_Earth_Y)), round(Pixel_Radius_Earth))
    pygame.draw.circle(win, Orbit_Gray, (round(Pixel_Earth_X),round(Pixel_Earth_Y)), round(Pixel_Orbital_Radius_Moon), 1)
    pygame.draw.circle(win, Moon_Gray, (round(Pixel_Moon_X),round(Pixel_Moon_Y)), round(Pixel_Radius_Moon))
    pygame.draw.circle(win, Orbit_Gray, (round(Pixel_Moon_X),round(Pixel_Moon_Y)), round(Pixel_Radius_Sphere_Influence), 1)

def drawFPS():
    global FPS
    fps_t = font.render("FPS/UPS: "+str(round(FPS)), 1, White)
    win.blit(fps_t, (DisplayX-146,0))
    spf_t = font.render("Sec/Frame: "+str(round(SPF,5)), 1, White)
    win.blit(spf_t, (DisplayX-216,20))

def drawLabel(width, margin, center, name, offset):
    x = center[0]
    y = center[1]
    p1 = [(x-width,y-width+margin),(x-width,y-width),(x-width+margin,y-width)]
    p2 = [(x-width,y+width-margin),(x-width,y+width),(x-width+margin,y+width)]
    p3 = [(x+width-margin,y+width),(x+width,y+width),(x+width,y+width-margin)]
    p4 = [(x+width,y-width+margin),(x+width,y-width),(x+width-margin,y-width)]
    pygame.draw.lines(win, Label_White, False, p1, 1)
    pygame.draw.lines(win, Label_White, False, p2, 1)
    pygame.draw.lines(win, Label_White, False, p3, 1)
    pygame.draw.lines(win, Label_White, False, p4, 1)
    t1 = label_font.render(name, 1, White)
    win.blit(t1, (x+width+10+offset, y-width+5))

def drawKey(string, vert_offset):
    text = key_font.render(string, 1, White)
    win.blit(text, (10,802+(vert_offset*15)))

def drawDebug():
    t0  = font.render("--- Stats For Nerds ---", 1, White)
    t1  = font.render("Velocity: "+str(round(Velocity,5)), 1, White)
    t2  = font.render("Apoapsis: "+str(round(Apoapsis,5)), 1, White)
    t3  = font.render("Periapsis: "+str(round(Periapsis,5)), 1, White)
    t4  = font.render("Semi Major Axis: "+str(round(Semi_Major_Axis,5)), 1, White)
    t5  = font.render("Semi Minor Axis: "+str(round(Semi_Minor_Axis,5)), 1, White)
    t6  = font.render("Distance To Earth: "+str(round(Dist_Earth,3)), 1, White)
    t7  = font.render("Distance To Moon: "+str(round(Dist_Moon,3)), 1, White)
    t8  = font.render("Eccentricity: "+str(round(Eccentricity,5)), 1, White)
    t9  = font.render("True Anomaly: "+str(round(True_Anomaly.radians,5)), 1, White)
    t10 = font.render("Global X: "+str(round(GlobalX,5)), 1, White)
    t11 = font.render("Global Y: "+str(round(GlobalY,5)), 1, White)
    t12 = font.render("EarthShip_TO_Vel(Y): "+str(round(EarthShip_TO_Vel.radians,5)), 1, White)
    t13 = font.render("Earth_TO_Ship: "+str(round(Earth_TO_Ship.radians,5)), 1, White)
    t14 = font.render("Moon_TO_Ship: "+str(round(Moon_TO_Ship.radians,5)), 1, White)
    t15 = font.render("Ship_TO_Earth: "+str(round(Ship_TO_Earth.radians,5)), 1, White)
    t16 = font.render("Ship_TO_Moon: "+str(round(Ship_TO_Moon.radians,5)), 1, White)
    t17 = font.render("Earth_TO_Moon: "+str(round(Earth_TO_Moon.radians,5)), 1, White)
    t18 = font.render("Moon_TO_Earth: "+str(round(Moon_TO_Earth.radians,5)), 1, White)
    t19 = font.render("X_TO_Impulse: "+str(round(X_TO_Impulse.radians,5)), 1, White)
    t20 = font.render("Vel_TO_Impulse: "+str(round(Vel_TO_Impulse.radians,5)), 1, White)
    t21 = font.render("Impulse_TO_Vel: "+str(round(Impulse_TO_Vel.radians,5)), 1, White)
    t22 = font.render("Delta V Used: "+str(round(DeltaV_Consumed, 3)), 1, White)
    
    x = 1000
    y = 150
    win.blit(t0,  (x, y+30*0))
    win.blit(t1,  (x, y+30*1))
    win.blit(t2,  (x, y+30*2))
    win.blit(t3,  (x, y+30*3))
    win.blit(t4,  (x, y+30*4))
    win.blit(t5,  (x, y+30*5))
    win.blit(t6,  (x, y+30*6))
    win.blit(t7,  (x, y+30*7))
    win.blit(t8,  (x, y+30*8))
    win.blit(t9,  (x, y+30*9))
    win.blit(t10, (x, y+30*10))
    win.blit(t11, (x, y+30*11))
    win.blit(t12, (x, y+30*12))
    win.blit(t13, (x, y+30*13))
    win.blit(t14, (x, y+30*14))
    win.blit(t15, (x, y+30*15))
    win.blit(t16, (x, y+30*16))
    win.blit(t17, (x, y+30*17))
    win.blit(t18, (x, y+30*18))
    win.blit(t19, (x, y+30*19))
    win.blit(t20, (x, y+30*20))
    win.blit(t21, (x, y+30*21))
    win.blit(t22, (x, y+30*22))
    
def drawVectors():
    pygame.draw.line(win, Red, (Pixel_Vel_X,Pixel_Vel_Y), (Pixel_Impulse_X,Pixel_Impulse_Y), 1)
    if Sphere_Influence == "Earth":
        pygame.draw.line(win, Debug_White, (Pixel_Earth_X, Pixel_Earth_Y), (Pixel_Ship_X, Pixel_Ship_Y), 1)
    if Sphere_Influence == "Moon":
        pygame.draw.line(win, Debug_White, (Pixel_Moon_X, Pixel_Moon_Y), (Pixel_Ship_X, Pixel_Ship_Y), 1)
    pygame.draw.line(win, Debug_White, (Pixel_Ship_X,Pixel_Ship_Y), (Pixel_Vel_X,Pixel_Vel_Y), 1)

def simulateImpulse():
    global Velocity, DeltaV_Consumed
    dV = Engine_Impulse*SPF
    DeltaV_Consumed += dV
    New_Velocity = math.sqrt(Velocity**2+dV**2+-2*Velocity*dV*math.cos(Impulse_TO_Vel.radians))
    arccos_arg = (Velocity**2+New_Velocity**2-dV**2)/(2*Velocity*New_Velocity)
    if arccos_arg < 1:
        Increment_X_TO_Vel = math.acos(arccos_arg)
    else:
        Increment_X_TO_Vel = 0
    if Vel_TO_Impulse.radians < 0:
        X_TO_Vel.radians += -Increment_X_TO_Vel
    if Vel_TO_Impulse.radians > 0:
        X_TO_Vel.radians += Increment_X_TO_Vel
    X_TO_Vel.normalize()
    Velocity = New_Velocity

def rotatePoints(x,y,a):
    x1 = x*math.cos(a)-y*math.sin(a)
    y1 = x*math.sin(a)+y*math.cos(a)
    return x1,y1

def derivedAngles():
    #Universal
    X_TO_Impulse.radians += Angular_Momentum*TimeWarp
    X_TO_Impulse.normalize()
    
    Vel_TO_Impulse.radians = X_TO_Impulse.radians - X_TO_Vel.radians
    Vel_TO_Impulse.normalize()

    Impulse_TO_Vel.radians = pi - Vel_TO_Impulse.radians
    Impulse_TO_Vel.normalize()

    #Conditional
    global Dist_Moon, Dist_Earth
    if Sphere_Influence == "Earth":
        x1 = Dist_Earth*math.cos(Earth_TO_Ship.radians)
        y1 = Dist_Earth*math.sin(Earth_TO_Ship.radians)
        x0 = Orbital_Radius_Moon*math.cos(Earth_TO_Moon.radians)
        y0 = Orbital_Radius_Moon*math.sin(Earth_TO_Moon.radians)
        Moon_TO_Ship.radians = math.atan2(y1-y0,x1-x0)
        Gamma = Earth_TO_Ship.radians - Earth_TO_Moon.radians
        Dist_Moon = math.sqrt(Dist_Earth**2+Orbital_Radius_Moon**2+-2*Dist_Earth*Orbital_Radius_Moon*math.cos(Gamma))
        
    if Sphere_Influence == "Moon":
        x1 = Dist_Moon*math.cos(Moon_TO_Ship.radians)
        y1 = Dist_Moon*math.sin(Moon_TO_Ship.radians)
        x0 = Orbital_Radius_Moon*math.cos(Moon_TO_Earth.radians)
        y0 = Orbital_Radius_Moon*math.sin(Moon_TO_Earth.radians)
        Earth_TO_Ship.radians = math.atan2(y1-y0,x1-x0)
        Gamma = Moon_TO_Ship.radians - Moon_TO_Earth.radians
        Dist_Earth = math.sqrt(Dist_Moon**2+Orbital_Radius_Moon**2+-2*Dist_Moon*Orbital_Radius_Moon*math.cos(Gamma))

    #Ship To Planet
    Ship_TO_Earth.radians = Earth_TO_Ship.radians + pi
    Ship_TO_Moon.radians = Moon_TO_Ship.radians + pi
    Ship_TO_Earth.normalize()
    Ship_TO_Moon.normalize()

    #Flight Path Angle
    EarthShip_TO_Vel.radians = X_TO_Vel.radians - Earth_TO_Ship.radians
    MoonShip_TO_Vel.radians = X_TO_Vel.radians - Moon_TO_Ship.radians
    EarthShip_TO_Vel.normalize()
    MoonShip_TO_Vel.normalize()

def calculateOrbit():
    global Apoapsis, Periapsis, Semi_Major_Axis, Semi_Minor_Axis, Eccentricity
    if Sphere_Influence == "Earth":
        #Constants
        C  = (2*G*Mass_Earth)/(Dist_Earth*Velocity**2)
        C0 = (Dist_Earth*Velocity**2)/(G*Mass_Earth)
        #Eccentricity
        Eccentricity = math.sqrt((C0-1)**2*math.sin(EarthShip_TO_Vel.radians)**2+math.cos(EarthShip_TO_Vel.radians)**2)
        #Apoapsis and Periapsis
        Radicand = C**2+-4*(1-C)*(-math.sin(EarthShip_TO_Vel.radians)**2)
        r1 = ((-C+math.sqrt(Radicand))/(2*(1-C)))*Dist_Earth
        r2 = ((-C-math.sqrt(Radicand))/(2*(1-C)))*Dist_Earth
        if Eccentricity < 1:
            Apoapsis  = max(r1,r2)
            Periapsis = min(r1,r2)
        if Eccentricity >= 1:
            Apoapsis  = min(r1,r2)
            Periapsis = max(r1,r2)
        #Semi Major and Minor Axis
        Semi_Major_Axis = 1/((2/Dist_Earth)-(Velocity**2/(G*Mass_Earth)))
        if Eccentricity < 1:
            Semi_Minor_Axis = math.sqrt(Semi_Major_Axis**2-(Semi_Major_Axis-Periapsis)**2)
        #True Anomaly
        Rise = C0*math.sin(EarthShip_TO_Vel.radians)*math.cos(EarthShip_TO_Vel.radians)
        Run  = C0*math.sin(EarthShip_TO_Vel.radians)**2-1
        True_Anomaly.radians = math.atan2(Rise,Run)
        True_Anomaly.normalize()

    elif Sphere_Influence == "Moon":
        #Constants
        C  = (2*G*Mass_Moon)/(Dist_Moon*Velocity**2)
        C0 = (Dist_Moon*Velocity**2)/(G*Mass_Moon)
        #Eccentricity
        Eccentricity = math.sqrt((C0-1)**2*math.sin(MoonShip_TO_Vel.radians)**2+math.cos(MoonShip_TO_Vel.radians)**2)
        #Apoapsis and Periapsis
        Radicand = C**2+-4*(1-C)*(-math.sin(MoonShip_TO_Vel.radians)**2)
        r1 = ((-C+math.sqrt(Radicand))/(2*(1-C)))*Dist_Moon
        r2 = ((-C-math.sqrt(Radicand))/(2*(1-C)))*Dist_Moon
        if Eccentricity < 1:
            Apoapsis  = max(r1,r2)
            Periapsis = min(r1,r2)
        if Eccentricity >= 1:
            Apoapsis  = min(r1,r2)
            Periapsis = max(r1,r2)
        #Semi Major and Minor Axis
        Semi_Major_Axis = 1/((2/Dist_Moon)-(Velocity**2/(G*Mass_Moon)))
        if Eccentricity < 1:
            Semi_Minor_Axis = math.sqrt(Semi_Major_Axis**2-(Semi_Major_Axis-Periapsis)**2)
        #True Anomaly
        Rise = C0*math.sin(MoonShip_TO_Vel.radians)*math.cos(MoonShip_TO_Vel.radians)
        Run  = C0*math.sin(MoonShip_TO_Vel.radians)**2-1
        True_Anomaly.radians = math.atan2(Rise,Run)
        True_Anomaly.normalize()

def traverseOrbit():
    global Velocity, Dist_Earth, Dist_Moon
    #The Moon Orbits The Earth
    dV = Velocity_Moon*SPF*TimeWarp
    Increment_Earth_TO_Moon = math.atan(dV/Orbital_Radius_Moon)
    Earth_TO_Moon.radians -= Increment_Earth_TO_Moon
    Moon_TO_Earth.radians = Earth_TO_Moon.radians + pi
    Earth_TO_Moon.normalize()
    Moon_TO_Earth.normalize()

    if Sphere_Influence == "Earth":
        #Increment True Anomaly
        dV = Velocity*SPF*TimeWarp
        Proj_Dist_Earth = math.sqrt(Dist_Earth**2+dV**2+-2*Dist_Earth*dV*math.cos(pi-EarthShip_TO_Vel.radians))
        arccos_arg = (Dist_Earth**2+Proj_Dist_Earth**2-dV**2)/(2*Dist_Earth*Proj_Dist_Earth)
        if 0 < arccos_arg < 1:
            Increment_True_Anomaly = math.acos(arccos_arg)
        elif arccos_arg < 0:
            Increment_True_Anomaly = 1
        else:
            Increment_True_Anomaly = 0
        if EarthShip_TO_Vel.radians < 0:
            True_Anomaly.radians  += -Increment_True_Anomaly
            Earth_TO_Ship.radians += -Increment_True_Anomaly
        if EarthShip_TO_Vel.radians > 0:
            True_Anomaly.radians  += Increment_True_Anomaly
            Earth_TO_Ship.radians += Increment_True_Anomaly
        Earth_TO_Ship.normalize()
        True_Anomaly.normalize()
        #Re-Calulcate R,V,Y
        Dist_Earth = (Semi_Major_Axis*(1-Eccentricity**2))/(1+Eccentricity*math.cos(True_Anomaly.radians))
        Velocity = math.sqrt(G*Mass_Earth*((2/Dist_Earth)-(1/Semi_Major_Axis)))
        Phi = math.atan2(Eccentricity*math.sin(True_Anomaly.radians),1+Eccentricity*math.cos(True_Anomaly.radians))
        if EarthShip_TO_Vel.radians < 0:
            X_TO_Vel.radians = Earth_TO_Ship.radians - (pi/2) - Phi
        if EarthShip_TO_Vel.radians > 0:
            X_TO_Vel.radians = Earth_TO_Ship.radians + (pi/2) - Phi
        X_TO_Vel.normalize()
        
    if Sphere_Influence == "Moon":
        #Increment True Anomaly
        dV = Velocity*SPF*TimeWarp
        Proj_Dist_Moon = math.sqrt(Dist_Moon**2+dV**2+-2*Dist_Moon*dV*math.cos(pi-MoonShip_TO_Vel.radians))
        arccos_arg = (Dist_Moon**2+Proj_Dist_Moon**2-dV**2)/(2*Dist_Moon*Proj_Dist_Moon)
        if 0 < arccos_arg < 1:
            Increment_True_Anomaly = math.acos(arccos_arg)
        elif arccos_arg < 0:
            Increment_True_Anomaly = 1
        else:
            Increment_True_Anomaly = 0
        if MoonShip_TO_Vel.radians < 0:
            True_Anomaly.radians += -Increment_True_Anomaly
            Moon_TO_Ship.radians += -Increment_True_Anomaly
        if MoonShip_TO_Vel.radians > 0:
            True_Anomaly.radians += Increment_True_Anomaly
            Moon_TO_Ship.radians += Increment_True_Anomaly
        Moon_TO_Ship.normalize()
        True_Anomaly.normalize()
        #Re-Calulcate R,V,Y
        Dist_Moon = (Semi_Major_Axis*(1-Eccentricity**2))/(1+Eccentricity*math.cos(True_Anomaly.radians))
        Velocity = math.sqrt(G*Mass_Moon*((2/Dist_Moon)-(1/Semi_Major_Axis)))
        Phi = math.atan2(Eccentricity*math.sin(True_Anomaly.radians),1+Eccentricity*math.cos(True_Anomaly.radians))
        if MoonShip_TO_Vel.radians < 0:
            X_TO_Vel.radians = Moon_TO_Ship.radians - (pi/2) - Phi
        if MoonShip_TO_Vel.radians > 0:
            X_TO_Vel.radians = Moon_TO_Ship.radians + (pi/2) - Phi
        X_TO_Vel.normalize()

def drawEllipse():
    raw = []
    for n in range(Iterations):
        angle = 2*pi*(n/Iterations)
        x = math.cos(angle)*Semi_Major_Axis
        y = math.sin(angle)*Semi_Minor_Axis
        raw.append((x,y))
    if Sphere_Influence == "Earth":
        focus   = [(x-Semi_Major_Axis+Periapsis,y)           for (x,y) in raw]
        scale   = [(x*System_Scale,y*System_Scale)           for (x,y) in focus]
        rotate  = [(rotatePoints(x,y,Earth_TO_Ship.radians)) for (x,y) in scale]
        anomaly = [(rotatePoints(x,y,-True_Anomaly.radians)) for (x,y) in rotate]
        trans = [(x+Pixel_Earth_X,y+Pixel_Earth_Y)           for (x,y) in anomaly]
    if Sphere_Influence == "Moon":
        focus   = [(x-Semi_Major_Axis+Periapsis,y)           for (x,y) in raw]
        scale   = [(x*System_Scale,y*System_Scale)           for (x,y) in focus]
        rotate  = [(rotatePoints(x,y,Moon_TO_Ship.radians))  for (x,y) in scale]
        anomaly = [(rotatePoints(x,y,-True_Anomaly.radians)) for (x,y) in rotate]
        trans = [(x+Pixel_Moon_X,y+Pixel_Moon_Y)             for (x,y) in anomaly]
    pygame.draw.lines(win, Orbit_Gray, True, trans)

def drawHyperbola():
    a = Periapsis/(Eccentricity - 1)
    c = a*Eccentricity
    b = math.sqrt(c**2-a**2)
    raw = []
    if Sphere_Influence == "Earth":
        Vertical_Range = 500000000
        for n in range(Iterations):
            y = (-Vertical_Range/2)+(n/Iterations)*Vertical_Range
            x = -math.sqrt(a**2+((a**2*y**2)/b**2))
            raw.append((x,y))
        focus   = [(x-Semi_Major_Axis+Periapsis,y)           for (x,y) in raw]
        scale   = [(x*System_Scale,y*System_Scale)           for (x,y) in focus]
        rotate  = [(rotatePoints(x,y,Earth_TO_Ship.radians)) for (x,y) in scale]
        anomaly = [(rotatePoints(x,y,-True_Anomaly.radians)) for (x,y) in rotate]
        trans = [(round(x+Pixel_Earth_X),round(y+Pixel_Earth_Y))           for (x,y) in anomaly]
    if Sphere_Influence == "Moon":
        Vertical_Range = 100000000
        for n in range(Iterations):
            y = (-Vertical_Range/2)+(n/Iterations)*Vertical_Range
            x = -math.sqrt(a**2+((a**2*y**2)/b**2))
            raw.append((x,y))
        focus   = [(x-Semi_Major_Axis+Periapsis,y)           for (x,y) in raw]
        scale   = [(x*System_Scale,y*System_Scale)           for (x,y) in focus]
        rotate  = [(rotatePoints(x,y,Moon_TO_Ship.radians))  for (x,y) in scale]
        anomaly = [(rotatePoints(x,y,-True_Anomaly.radians)) for (x,y) in rotate]
        trans = [(round(x+Pixel_Moon_X),round(y+Pixel_Moon_Y))             for (x,y) in anomaly]
    pygame.draw.lines(win, Orbit_Gray, False, trans)

def checkSphereInfluence():
    global Sphere_Influence
    if (Dist_Moon < Sphere_Influence_Radius) and (Sphere_Influence == "Earth"):
        Sphere_Influence = "Moon"
        correctRelativeVelocity("sub")
        derivedAngles()
        calculateOrbit()
    elif (Dist_Moon > Sphere_Influence_Radius) and (Sphere_Influence == "Moon"):
        Sphere_Influence = "Earth"
        correctRelativeVelocity("add")
        derivedAngles()
        calculateOrbit()

def correctRelativeVelocity(toggle):
    global Velocity
    X_TO_MoonVel.radians = Earth_TO_Moon.radians + pi/2
    if toggle == "sub":
        ShipVel_TO_MoonVel.radians = X_TO_MoonVel.radians - X_TO_Vel.radians
    if toggle == "add":
        ShipVel_TO_MoonVel.radians = X_TO_MoonVel.radians - X_TO_Vel.radians + pi
    ShipVel_TO_MoonVel.normalize()
    Gamma = pi - ShipVel_TO_MoonVel.radians
    New_Velocity = math.sqrt(Velocity**2+Velocity_Moon**2+-2*Velocity*Velocity_Moon*math.cos(Gamma))
    Delta_X_TO_Vel = math.acos((Velocity**2+New_Velocity**2-Velocity_Moon**2)/(2*Velocity*New_Velocity))
    if ShipVel_TO_MoonVel.radians < 0:
        X_TO_Vel.radians -= Delta_X_TO_Vel
    elif ShipVel_TO_MoonVel.radians > 0:
        X_TO_Vel.radians += Delta_X_TO_Vel
    Velocity = New_Velocity

Star_Population = 200
def initializeStars():
    global Stars
    Stars = []
    for n in range(Star_Population):
        x = random.randrange(DisplayX)
        y = random.randrange(DisplayY)
        colour = (200,200,200)
        Stars.append((x,y,colour))

def drawStars():
    for n in range(len(Stars)):
        pygame.gfxdraw.pixel(win, Stars[n][0], Stars[n][1], Stars[n][2])

#Initialize
run = True
FPS = 500
SPF = 1/FPS
derivedAngles()
calculateOrbit()
initializeStars()
start_time = time.time()
Time_Between_FPS_Updates = 1
FPS_counter = 0
while run == True:
    win.fill(Back_Drop)
    MouseX, MouseY = pygame.mouse.get_pos()
    MouseLeft, MouseScroll, MouseRight = pygame.mouse.get_pressed()
    Mouse_RelX, Mouse_RelY = pygame.mouse.get_rel()
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        #Navigation
        if event.type == pygame.MOUSEBUTTONDOWN:
            if MouseOver == "Toggle Navigation" or MouseOver == "Navigation":
                MouseDown = "Navigation"
        if event.type == pygame.MOUSEBUTTONUP:
            MouseDown = "None"
        if event.type == pygame.MOUSEBUTTONDOWN:
            if MouseOver == "Toggle Navigation":
                if Minimized:
                    Minimized = False
                elif not Minimized:
                    Minimized = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKQUOTE:
                GlobalX = 0
                GlobalY = 0
            if event.key == pygame.K_COMMA:
                TimeWarp_Value -= 1
                if TimeWarp_Value < 1:
                    TimeWarp_Value = 1
            if event.key == pygame.K_PERIOD:
                TimeWarp_Value += 1
                if TimeWarp_Value > TimeWarp_Maximum:
                    TimeWarp_Value = TimeWarp_Maximum
            if event.key == pygame.K_l:
                if Label_Toggle:
                    Label_Toggle = False
                elif not Label_Toggle:
                    Label_Toggle = True
            if event.key == pygame.K_k:
                if Debug_Toggle:
                    Debug_Toggle = False
                elif not Debug_Toggle:
                    Debug_Toggle = True
            if event.key == pygame.K_j:
                if Vector_Toggle:
                    Vector_Toggle = False
                elif not Vector_Toggle:
                    Vector_Toggle = True
            if event.key == pygame.K_h:
                if Toggle_Stars:
                    Toggle_Stars = False
                elif not Toggle_Stars:
                    Toggle_Stars = True

    #Calculate
    checkSphereInfluence()
    derivedAngles()
    determineMouseOver()
    userControls()
    if Accelerating:
        simulateImpulse()
        derivedAngles()
        calculateOrbit()
    traverseOrbit()
    derivedAngles()

    #Draw
    if Toggle_Stars:
        drawStars()
    pixelValues()
    if Eccentricity < 1:
        drawEllipse()
    if Eccentricity >= 1:
        drawHyperbola()
    drawPlanets()
    if Debug_Toggle:
        drawDebug()
    if Vector_Toggle:
        drawVectors()
    if Label_Toggle:
        drawLabel(Label_Size, 5, (Pixel_Ship_X,  Pixel_Ship_Y),  "Spaceship", 0)
        drawLabel(Label_Size, 5, (Pixel_Earth_X, Pixel_Earth_Y), "Earth", 0 if Label_Size > Pixel_Radius_Earth else Pixel_Radius_Earth-Label_Size)
        drawLabel(Label_Size, 5, (Pixel_Moon_X,  Pixel_Moon_Y),  "The Moon", 0 if Label_Size > Pixel_Radius_Moon else Pixel_Radius_Moon-Label_Size)
    timeWarp()
    drawFPS()
    drawKey("Control Spaceship With W A S D",0)
    drawKey("Press 'L' to Toggle Labels",1)
    drawKey("Press 'K' to Toggle Vectors",2)
    drawKey("Press 'J' to Toggle Debug Information",3)
    drawKey("Press 'H' to Toggle Stars",4)
    drawKey("Press '`' to Reset Position of The Spaceship On Screen",5)

    #Navigation
    panNavigation()
    drawNavigation()
    if Turning_Left:
        drawLeftPlume()
    if Turning_Right:
        drawRightPlume()
    drawRocket()

    pygame.display.update()
    FPS_counter += 1
    if time.time()-start_time > Time_Between_FPS_Updates:
        FPS = FPS_counter/(time.time()-start_time)
        SPF = 1/FPS
        FPS_counter = 0
        start_time = time.time()
pygame.quit()




















