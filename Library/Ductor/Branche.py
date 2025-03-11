class Branche:
    def __init__(self, name):
        self.name = name
        self.conduits = []
        self.coudes = []
        self.total_HL = 0
    
    def ajouter_conduit(self, conduit):
        self.conduits.append(conduit)
        self.calculer_perte_pression()
    
    def ajouter_coude(self, coude):
        self.coudes.append(coude)
        self.calculer_perte_pression()
    
    def calculer_perte_pression(self):
        self.total_HL = sum(conduit.HL for conduit in self.conduits) + sum(coude.HL for coude in self.coudes)
    
    def __repr__(self):
        return f"Branche {self.name}: Perte de pression totale = {self.total_HL:.2f} Pa"