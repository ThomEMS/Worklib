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
    
    def enlever_item(self, item):
        
        if item in self.conduits:
            self.conduits.remove(item)
        elif item in self.coudes:
            self.coudes.remove(item)
        self.calculer_perte_pression()

    def calculer_perte_pression(self):
        self.total_HL = sum(conduit.HL for conduit in self.conduits) + sum(coude.HL for coude in self.coudes)
    
    def __repr__(self):
        details = f"  Branche {self.name} (Perte totale = {self.total_HL:.2f} Pa)\n"
        for conduit in self.conduits:
            details += f"    - {conduit}\n"
        for coude in self.coudes:
            details += f"    - {coude}\n"
        return details