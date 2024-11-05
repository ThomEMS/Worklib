"""
# Feuille de calcul, courbe du système 
# Auteur: Thomas Pelletier, CPI 6064480
# Date : 2024-10-17
"""
import numpy as np
import matplotlib.pyplot as plt
import workbook as wb


"""
# Minor loss coefficient for system parameters
# Source : The Engineering ToolBox (2003). Air Duct Components - Minor Dynamic Loss Coefficients.
# 
"""
cl_90 = 0.5 #90deg bend r/D < 1
cl_t = 0.3 #T, flow to branch
cl_entre = 0.35
cl_sortie = 1
cl_catalyst = 6698.91 
cl_demist = 31.98 


# Number of air duct component in the system
n_t_75 = 1
n_90_75 = 5
n_entre = 1
n_sortie = 1
n_t_100 = 1
n_90_100 = 2
n_demist = 1
n_catalyst = 1 

# Diameter of round duct section
d_asp = 75 #mm
d_exh = 100 #mm

#Lenght of duct section
l_asp = 25 #m
l_exh = 4 #m

"""
# Duct definition
# According to structure : 
# [[Diameter1(mm),Lenght1(m)],[Diameter2,Lenght2],[...]]
"""
duct = np.array([[d_asp,l_asp],
                 [d_exh,l_exh]])

"""
# Air duct component for minor loss definition
# According to structure : 
# [[MinorLossCoefficient(adim.),NumberOfItemsInSys(un.),DiameterOfComponent(mm)],[...]],[...]]
"""
mlc = np.array([[cl_90,n_90_75,d_asp],
                [cl_t,n_t_75,d_asp],
                [cl_entre,n_entre,d_asp],
                [cl_sortie,n_sortie,d_exh],
                [cl_90,n_90_100,d_exh],
                [cl_t,n_t_100,d_exh],
                [cl_catalyst,n_catalyst,300],
                [cl_demist,n_demist,150]])


# System curve calculation see workbook for function details
curve = wb.sys_curve(0,750,10,mlc,duct)

# Blower fan 
cfm_blwer = np.array([0,100,150,160,200,240,250,270,290,300,360,400,430,450,500,520,550,590,600,610,650,700,720])
sp_blwer = np.array([24.5,24.5,24.8,24.9,25,25.2,25.3,25.5,25.6,25.6,25.8,26,26,25.9,25.8,25.7,25.5,25.2,25.15,25,24.4,23.6,23.2])



#plot curve using matplotlib
#Fig 1 using standard axis to see full system curve
fig, ax = plt.subplots()
plt.title("U24-177 Courbe système - Dégazage d'ozone")
plt.xlabel("Débit (CFM)")
plt.ylabel("S.P. (inH20)")
plt.minorticks_on()
plt.grid(color= '0.8', linestyle='-', linewidth=0.5, which="both")
ax.plot(curve[0], (curve[1]/249)+3,label="Courbe Système",color = "#30638E")
ax.plot(cfm_blwer,sp_blwer,label="Courbe Soufflante - HP-4C",color = "#D1495B")

ax.spines["right"].set_visible(False)
ax.spines["top"].set_visible(False)

ax.yaxis.set_ticks_position("left")
ax.xaxis.set_ticks_position("bottom")
ax.spines["bottom"].set_bounds(0, 750)
ax.set_ylim([0, 610])

ax.legend(frameon = False)

#Fig 1 using standard axis to see full system curve
fig2, ax2 = plt.subplots()
plt.title("U24-177 Courbe système - Dégazage d'ozone")
plt.xlabel("Débit (CFM)")
plt.ylabel("S.P. (inH20)")
plt.minorticks_on()
plt.grid(color= '0.8', linestyle='-', linewidth=0.5, which="both")
ax2.set_ylim([0, 60])
ax2.plot(curve[0], (curve[1]/249)+3,label="Courbe Système", color = "#30638E")
ax2.plot(cfm_blwer,sp_blwer,label="Courbe Soufflante - HP-4C", color = "#D1495B")
ax2.spines["right"].set_visible(False)
ax2.spines["top"].set_visible(False)

ax2.yaxis.set_ticks_position("left")
ax2.xaxis.set_ticks_position("bottom")
ax.spines["bottom"].set_bounds(0, 750) 

ax2.legend(frameon = False)
ax.set_xlim([0, 750])
ax2.set_xlim([0, 750])

plt.show()


