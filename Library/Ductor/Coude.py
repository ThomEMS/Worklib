import fonctions as fn
class Coude:
    def __init__(self,p_name,p_mlc,p_diam,p_flow):
        self.mlc = p_mlc
        self.diam = p_diam
        self.cfm = p_flow
        self.name = p_name
        self.HL = self.calculate_headloss()

    def calculate_headloss(self):
        return fn.headloss_air_MLCoeff(self.mlc,self.diam,self.cfm)

    def set_diam(self,p_diam):
        self.diam = p_diam
        self.HL = self.calculate_headloss()

    def set_mlc(self,p_mlc):
        self.mlc = p_mlc
        self.HL = self.calculate_headloss()

    def set_cfm(self, p_cfm):
        self.cfm = p_cfm
        self.HL = self.calculate_headloss()

    def __repr__(self):
        return f"{self.name}(mlc={self.mlc}, diameter={self.diam}, cfm = {self.cfm}, HeadLoss = {self.HL})"


   

    