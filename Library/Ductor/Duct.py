import fonctions as fn
class Duct:
    def __init__(self, p_name, p_length, p_diameter, p_cfm = 0):
        self.name = p_name
        self.length = p_length  # Length of the duct in m
        self.diameter = p_diameter  # Diameter of the duct in mm
        self.cfm = p_cfm # Predicted flow in system branch default 0
        self.HL = self.calculate_headloss() #branch default (nominal HL)
    
    def calculate_headloss(self):
        # Example placeholder function for computing HL
        # Replace with your real formula or function call.
        return fn.pressure_loss(self.diameter,self.length,self.cfm) 
        
    def set_diam(self,p_diam):
        self.diameter = p_diam
        self.HL = self.calculate_headloss()

    def set_length(self,p_length):
        self.length = p_length
        self.HL = self.calculate_headloss()

    def set_cfm(self, p_cfm):
        self.cfm = p_cfm
        self.HL = self.calculate_headloss()

    def __repr__(self):
        return (f"Conduit: {self.name}, "
                f"L={self.length}m, D={self.diameter}mm, CFM={self.cfm}, HL={self.HL:.2f}")




   