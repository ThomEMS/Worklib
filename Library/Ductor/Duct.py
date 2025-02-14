import math

MtoFT = 1/0.3048

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



class Duct :

    def __init__(self,p_lenght,p_cfm, p_form = "round", p_TargetHL = 0.08):
        self.len = p_lenght
        self.cfm = p_cfm
        self.form = p_form
        if self.form == "round":
            self.diam = math.ceil(((self.cfm**1.9 * 0.109136)/p_TargetHL)**(1/5.02)) #tiré de la feuille de calcul engeneering toolbox pour le equal friction method
            self.cond_sizes = [self.diam]
        elif self.form == "square":
            cond_sizes = []
            self.diam = math.ceil(((self.cfm**1.9 * 0.109136)/p_TargetHL)**(1/5.02))
            for a, b in std_duct_rect_inches:
                d = 1.30*(a*b)**0.625/(a+b)**0.25
                if d >= self.diam and d <= self.diam+2:
                    if (a,b) and (b,a) not in cond_sizes:
                        if max((a,b))/min((a,b)) <= 2:
                            cond_sizes.append((a,b))
            self.cond_sizes=cond_sizes
        self.headloss = (self.len*MtoFT)*p_TargetHL/100
    
    def reqCfm(self):
        s = f"{self.cfm} cfm"
        return s  
    
    def reqLen(self):
        s = f"{self.len} m"
        return s  

    def reqDiam(self):
        s = f"{self.diam} in."
        return s  
    
l1 = Duct(26.00, 1200,"square")
print(l1.headloss, l1.cond_sizes)