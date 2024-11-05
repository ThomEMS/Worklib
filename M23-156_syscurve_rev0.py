"""
# Feuille de calcul, courbe du système 
# Auteur: Thomas Pelletier, CPI 6064480
# Date : 2024-10-28
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
cl_grille = 3



# Number of air duct component in the system
n_t_ = 1
n_90_ = 1
n_entre = 1
n_sortie = 1
n_grille = 1

#Dimensions duct rectangulaire
a = 375
b = 375
# Diameter of round duct section
d_eq = 1.3 *(a*b)**0.625 / (a+b)**(0.25)#equivalent diam

#Lenght of duct section
l_asp = 6 #m


"""
# Duct definition
# According to structure : 
# [[Diameter1(mm),Lenght1(m)],[Diameter2,Lenght2],[...]]
"""
duct = np.array([[d_eq,l_asp]])

"""
# Air duct component for minor loss definition
# According to structure : 
# [[MinorLossCoefficient(adim.),NumberOfItemsInSys(un.),DiameterOfComponent(mm)],[...]],[...]]
"""
mlc = np.array([[cl_90,n_90_,d_eq],
                [cl_t,n_t_,d_eq],
                [cl_entre,n_entre,d_eq],
                [cl_sortie,n_sortie,d_eq],
                [cl_grille,n_grille,d_eq]
                ])


# System curve calculation see workbook for function details
curve = wb.sys_curve(0,900,10,mlc,duct)

#plot curve using matplotlib
#Fig 1 using standard axis to see full system curve
fig, ax = plt.subplots()
plt.title("U24-177 Courbe système - Dégazage d'ozone")
plt.xlabel("Débit (CFM)")
plt.ylabel("S.P. (inH20)")
plt.minorticks_on()
plt.grid(color= '0.8', linestyle='-', linewidth=0.5, which="both")
ax.plot(curve[0], (curve[1]/249),label="Courbe Système",color = "#30638E")

ax.spines["right"].set_visible(False)
ax.spines["top"].set_visible(False)

ax.yaxis.set_ticks_position("left")
ax.xaxis.set_ticks_position("bottom")
ax.spines["bottom"].set_bounds(0, 900)


ax.legend(frameon = False)

plt.show()


