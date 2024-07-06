"""
# Feuille de fonctions d'ingénierie utiles 
# Autheur: Thomas Pelletier
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
    # Define conversion factors
    conversion_factors = {
        # Volume
        'litres_to_gallons': 0.264172,
        'gallons_to_litres': 3.78541,
        'mètres_cubes_to_pieds_cubes': 35.3147,
        'pieds_cubes_to_mètres_cubes': 0.0283168,

        # Torque
        'newton_mètres_to_livres_pieds': 0.737562,
        'livres_pieds_to_newton_mètres': 1.35582,

        # Energy
        'joules_to_btu': 0.000947817,
        'btu_to_joules': 1055.06,
        'joules_to_calories': 0.239006,
        'calories_to_joules': 4.184,
        'joules_to_kwh': 2.77778e-7,
        'kwh_to_joules': 3.6e6,
    }

    # Define key for conversion
    key = f'{from_unit}_to_{to_unit}'
    
    if key not in conversion_factors:
        raise ValueError(f"Conversion from {from_unit} to {to_unit} not supported.")

    # Perform the conversion
    converted_value = value * conversion_factors[key]
    return converted_value

