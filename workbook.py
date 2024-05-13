###
# Feuille de fonctions d'ingénierie utiles 
# Autheur: Thomas Pelletier
# Date : 2024-05-13
###
import numpy as np

def pelec(V,I,f=1):
    ##
    # Puissance electrique consomme
    # Variables : V, Tension d'alimentation; I, Courant consomme; f, facteur d'efficacite (default = 1)
    ##
    p = V*I*f
    return p



