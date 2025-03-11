class System:
    def __init__(self, name):
        self.name = name
        self.branches = []
    
    def ajouter_branche(self, branche):
        self.branches.append(branche)
    
    def calculer_pressions_statiques(self):
        pressions = {}
        for branche in self.branches:
            branche.calculer_perte_pression()
            pressions[branche.name] = branche.total_HL
        return pressions
    
    def __repr__(self):
        details = f"Système {self.name}:\n"
        for branche in self.branches:
            details += str(branche)  # This will now include conduits and coudes!
        return details