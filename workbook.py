"""
# Feuille de fonctions d'ingénierie utiles 
# Auteur: Thomas Pelletier
# Date : 2024-05-13
"""
import numpy as np


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

        # Force
        ("newton_mètres", "livres_pieds"): 0.737562,
        ("livres_pieds", "newton_mètres"): 1.35582,
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




