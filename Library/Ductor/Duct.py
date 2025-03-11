import fonctions as fn
class Duct:
    def __init__(self, p_length, p_diameter, p_cfm = 0):
        self.length = p_length  # Length of the duct in m
        self.diameter = p_diameter  # Diameter of the duct in mm
        self.cfm = p_cfm # Predicted flow in system branch default 0
        self.HL = fn.pressure_loss(self.diameter,self.length,self.cfm) #branch default (nominal HL)
        
        
    def set_diam(self,p_diam):
        self.diameter = p_diam

    def set_length(self,p_length):
        self.length = p_length

    def set_cfm(self, p_cfm):
        self.cfm = p_cfm

    def __repr__(self):
        return f"Duct(length={self.length}, diameter={self.diameter}, cfm = {self.cfm}, HeadLoss = {self.HL})"





   