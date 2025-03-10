import matplotlib.pyplot as plt
import numpy as np 
from Library import workbook as wb


def main():


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
    cl_45 = 0.2



    # Number of air duct component in the system
    n_t_ = 1
    n_90_ = 6
    n_45_ = 2
    n_entre = 1
    n_sortie = 1
    n_grille = 1

    #Dimensions duct circulaire
    d = 4*25.4 # mm

    #Lenght of duct section
    l_asp = 11 #m
    l_retour = 7 #m

    """
    # Duct definition
    # According to structure : 
    # [[Diameter1(mm),Lenght1(m)],[Diameter2,Lenght2],[...]]
    """
    duct = np.array([[d,l_asp],[d,l_retour]])

    """
    # Air duct component for minor loss definition
    # According to structure : 
    # [[MinorLossCoefficient(adim.),NumberOfItemsInSys(un.),DiameterOfComponent(mm)],[...]],[...]]
    """
    mlc = np.array([[cl_90,n_90_,d],
                    [cl_t,n_t_,d],
                    [cl_entre,n_entre,d],
                    [cl_45,n_45_,d],
                    [cl_sortie,n_sortie,d],
                    [cl_grille,n_grille,d]
                    ])


    # System curve calculation see workbook for function details
    curve = wb.sys_curve(0,125,5,mlc,duct)

    #plot curve using matplotlib
    #Fig 1 using standard axis to see full system curve
    fig, ax = plt.subplots()
    plt.title("M24-083 Courbe système - Salle de conduite")
    plt.xlabel("Débit (CFM)")
    plt.ylabel("P.S. (po. H20)")
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

if __name__ == "__main__":
    main()