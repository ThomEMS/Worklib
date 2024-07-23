"""
# Feuille de fonctions d'ingénierie utiles 
# Auteur: Thomas Pelletier
# Date : 2024-05-13
"""
import numpy as np
import math
import itertools 

std_duct_in = []

# Ajout des tailles de 3 à 9.5 avec un pas de 0.5
std_duct_in.extend(np.arange(3, 10, 0.5))

# Ajout des tailles de 10 à 20 avec un pas de 1
std_duct_in.extend(range(10, 21))

# Ajout des tailles de 25 à 100 avec un pas de 5
std_duct_in.extend(range(25, 105, 5))


def pelec(V,I,f=1):
    """
    Puissance electrique consomme
    Variables : V, Tension d'alimentation; I, Courant consomme; f, facteur d'efficacite (default = 1)
    """
    p = V*I*f
    return p
    
def convert_unit(value, from_unit, to_unit):
    conversion_factors = {
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
    a = math.pi() * (diam_in/(2*12))**2 #aire de passage en ft^2
    vel = cfm/a #en ft/min
    return (vel,"ft/min")

def square_duct_diam_in(cfm,head_loss):
    cond_sizes = []
    rd_diam = round_duct_diam_in(cfm,head_loss)[0]
    for a, b in itertools.product(std_duct_in,std_duct_in):
        d = 1.30*(a*b)**0.625/(a+b)**0.25
        if d >= rd_diam and d <= rd_diam+1:
            if (a,b) and (b,a) not in cond_sizes:
                if max((a,b))/min((a,b)) <= 3:
                    cond_sizes.append((a,b))
    return cond_sizes

