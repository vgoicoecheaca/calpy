import ROOT as R

class Aux():
    def __init__(self,manager):
        self.m = manager 

    def fit_peak_with_gaus(self,h,min,max):
        g = R.TF1("g","gaus",min,max)     
        h.Fit("g","R+")
        return  g.GetParameters()
