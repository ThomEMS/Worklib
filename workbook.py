"""
# Feuille de fonctions d'ingénierie utiles 
# Auteur: Thomas Pelletier
# Date : 2024-05-13
"""
import numpy as np
import math
import itertools 


# Dimensions des conduits
widths = [100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850]
heights = [200, 250, 300, 400, 500, 600, 800, 1000, 1200, 1400, 1600, 1800, 2000]


# Liste des combinaisons largeur x hauteur où la combinaison de grosseur est 1
std_duct_rect = []
# Liste des combinaisons largeur x hauteur où la combinaison de grosseur est 1, en pouces
std_duct_rect_inches = []

def mm_to_inches(mm):
    inches = mm / 25.4
    return round(inches * 4) / 4

# Parcourir le tableau et ajouter les combinaisons à la liste
for i, height in enumerate(widths):
    for j, width in enumerate(widths):
        if height/width >= 2/3 and height/width <= 1:
            std_duct_rect.append((width, height))
            width_inches = mm_to_inches(width)
            height_inches = mm_to_inches(height)
            std_duct_rect_inches.append((width_inches, height_inches))


def pelec(V,I,f=1):
    """
    Puissance electrique consomme
    Variables : V, Tension d'alimentation; I, Courant consomme; f, facteur d'efficacite (default = 1)
    """
    p = V*I*f
    return p
    
def convert_unit(value, from_unit, to_unit):
    conversion_factors = {
        #Aire
        ("mètres_carrés","pieds_carrés"):10.76391042,
        # Volume
        ("litres", "millilitres"): 1000,
        ("millilitres", "litres"): 0.001,
        ("litres", "gallons"): 0.264172,
        ("gallons", "litres"): 3.78541,
        ("mètres_cubes", "gallons"): 264.172,
        ("gallons", "mètre_cubes"): 1/264.172,
        ("mètres_cubes", "pieds_cubes"): 35.3147,
        ("pieds_cubes", "mètres_cubes"): 0.0283168,

        # Longueur
        ("mètres", "millimètres"): 1000,
        ("millimètres", "mètres"): 0.001,
        ("mètres", "centimètres"): 100,
        ("centimètres", "mètres"): 0.01,
        ("mètres", "pieds"): 3.28084,
        ("pieds", "mètres"): 0.3048,
        ("kilomètres", "miles"): 0.621371,
        ("miles", "kilomètres"): 1.60934,
        ("millimètres","pouces"): 1/25.4,
        ("pouces","millimètres"): 25.4,

        # Poids/Masse
        ("kilogrammes", "grammes"): 1000,
        ("grammes", "kilogrammes"): 0.001,
        ("kilogrammes", "livres"): 2.20462,
        ("livres", "kilogrammes"): 0.453592,
        ("grammes", "onces"): 0.035274,
        ("onces", "grammes"): 28.3495,

        # Énergie
        ("joules", "BTU"): 0.000947817,
        ("BTU", "joules"): 1055.06,
        ("calories", "joules"): 4.184,
        ("joules", "calories"): 0.239006,
        ("kwh", "joules"): 3600000,
        ("joules", "kwh"): 2.77778e-7,

        # couple
        ("newton_mètres", "livres_pieds"): 0.737562,
        ("livres_pieds", "newton_mètres"): 1.35582,

        # débits volumique
        ("litres_par_seconde", "millilitres_par_seconde"): 1000,
        ("millilitres_par_seconde", "litres_par_seconde"): 0.001,
        ("litres_par_seconde", "gallons_par_minute"): 15.8503,
        ("gallons_par_minute", "litres_par_seconde"): 0.0630902,
        ("mètres_cubes_par_seconde", "litres_par_seconde"): 1000,
        ("litres_par_seconde", "mètres_cubes_par_seconde"): 0.001,
        ("mètres_cubes_par_seconde", "pieds_cubes_par_seconde"): 35.3147,
        ("pieds_cubes_par_seconde", "mètres_cubes_par_seconde"): 0.0283168,
        ("litres_par_seconde", "pieds_cubes_par_seconde"): 0.0353147,
        ("pieds_cubes_par_seconde", "litres_par_seconde"): 28.3168,
        ("litres_par_seconde", "litres_par_minute"): 60,
        ("litres_par_minute", "litres_par_seconde"): 1/60,
        ("litres_par_minute", "mètres_cubes_par_heure"): 0.06,
        ("mètres_cubes_par_heure", "litres_par_minute"): 16.6667,
        ("mètres_cubes_par_heure", "litres_par_seconde"): 0.277778,
        ("litres_par_seconde", "mètres_cubes_par_heure"): 3.6,
        ("litres_par_minute", "gallons_par_minute"): 0.264172,
        ("gallons_par_minute", "litres_par_minute"): 3.78541,
        ("mètres_cubes_par_heure", "pieds_cubes_par_seconde"): 0.0098096,
        ("pieds_cubes_par_seconde", "mètres_cubes_par_heure"): 101.941,
        ("mètres_cubes_par_heure", "gallons_par_minute"): 4.40287,
        ("gallons_par_minute", "mètres_cubes_par_heure"): 0.227124,
        #Débits massique
        ("kilogrammes_par_seconde", "grammes_par_seconde"): 1000,
        ("grammes_par_seconde", "kilogrammes_par_seconde"): 0.001,
        ("kilogrammes_par_seconde", "tonnes_par_seconde"): 0.001,
        ("tonnes_par_seconde", "kilogrammes_par_seconde"): 1000,
        ("kilogrammes_par_seconde", "livres_par_seconde"): 2.20462,
        ("livres_par_seconde", "kilogrammes_par_seconde"): 0.453592,
        ("tonnes_par_seconde", "livres_par_seconde"): 2204.62,
        ("livres_par_seconde", "tonnes_par_seconde"): 0.000453592,
        ("grammes_par_seconde", "livres_par_seconde"): 0.00220462,
        ("livres_par_seconde", "grammes_par_seconde"): 453.592,
        ("tonnes_par_heure", "livres_par_heure"): 2204.62,
        ("livres_par_heure", "tonnes_par_heure"): 0.000453592,
        ("kilogrammes_par_heure", "livres_par_heure"): 2.20462,
        ("livres_par_heure", "kilogrammes_par_heure"): 0.453592
    }
    
    # Température conversion requires different handling
    if from_unit == "celsius" and to_unit == "fahrenheit":
        return (value * 9/5) + 32
    elif from_unit == "fahrenheit" and to_unit == "celsius":
        return (value - 32) * 5/9

    try:
        factor = conversion_factors[(from_unit, to_unit)]
        return value * factor
    except KeyError:
        raise ValueError(f"Conversion de {from_unit} à {to_unit} non supportée.")

def round_duct_diam_in(air_flow_CFM,head_loss_100ft):
    #Retourne le diamètre de conduits nécessaire eb pouces 
    diam = ((air_flow_CFM**1.9 * 0.109136)/head_loss_100ft)**(1/5.02) #tiré de la feuille de calcul engeneering toolbox pour le equal friction method
    return (diam, math.ceil(diam))

def round_duct_vel(cfm,diam_in):
    #retourne la vélocité pour un diam circulaire donnée
    a = math.pi() * (diam_in/(2*12))**2 #aire de passage en ft^2
    vel = cfm/a #en ft/min
    return (vel,"ft/min")

def square_duct_diam_in(cfm,head_loss):
    cond_sizes = []
    rd_diam = round_duct_diam_in(cfm,head_loss)[0]
    for a, b in std_duct_rect_inches:
        d = 1.30*(a*b)**0.625/(a+b)**0.25
        if d >= rd_diam and d <= rd_diam+2:
            if (a,b) and (b,a) not in cond_sizes:
                if max((a,b))/min((a,b)) <= 2:
                    cond_sizes.append((a,b))
    return cond_sizes

def square_duct_diam_mm(cfm,head_loss):
    cond_sizes = []
    rd_diam = convert_unit((round_duct_diam_in(cfm,head_loss)[0]),"pouces","millimètres")
    for a, b in std_duct_rect:
        d = 1.30*(a*b)**0.625/(a+b)**0.25
        if d >= rd_diam and d <= rd_diam + 50:
            if (a,b) and (b,a) not in cond_sizes:
                if max((a,b))/min((a,b)) <= 3:
                    cond_sizes.append((a,b))
    return cond_sizes


def square_duct_vel(cfm,dim):
    #retourne la vélocité pour les dimension rectengulaire données (a,b) en pouce
    a = (dim(0)/12)*(dim(1)/12) #aire de passage en ft^2
    vel = cfm/a #en ft/min
    return (vel,"ft/min")


def headloss_air_duct(cfm,diam,length):
    #  lenght unit: m
    HL_100ft = 0.109136*(cfm**1.9)/((convert_unit(diam,"millimètres","pouces"))**5.02)
    HL_tot = (HL_100ft*convert_unit(length,"mètres","pieds")/100)*249
    return HL_tot #Pa

def duct_vel(diam, cfm):
    #diam unit: mm
    area = (math.pi*(diam/1000)**2)/4 #m^2
    vel = cfm/convert_unit(area,"mètres_carrés","pieds_carrés") #pieds minutes
    
    return vel

def headloss_air_MLCoeff(K,diam, cfm):
    dP = (K*1.2*(duct_vel(diam,cfm)*0.00508)**2)/2
    return dP #Pa

def sys_curve(Cfm_min,Cfm_max,step,MLC,duct):
    #duct: [diam, length],[diam,lenght]]      MLC: [[Cl_elbow, N_elbow, diam], [Cl_tee, N_tee, diam]]
    sp_Y = np.empty(int((Cfm_max-Cfm_min)/step)+1)
    cfm_X = np.empty(int((Cfm_max-Cfm_min)/step)+1)
    j = 0
    for cfm in range (Cfm_min,Cfm_max+step,step):
        
        Hl=0
        n_duct = np.shape(duct)[0]
        for i in range(0,n_duct):
            Hl = Hl + headloss_air_duct(cfm,duct[i,0],duct[i,1])

        n_mlc = np.shape(MLC)[0]
        for i in range(0,n_mlc):
            Hl = Hl + MLC[i,1]*headloss_air_MLCoeff(MLC[i,0],MLC[i,2],cfm)
        
        sp_Y[j]=Hl
        cfm_X[j]=cfm
        j = j +1 
    return (cfm_X,sp_Y)

