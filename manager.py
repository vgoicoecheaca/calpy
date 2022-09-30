from plotter import Plotter 
from config import Config
from branches import Branches
from aux import Aux

class Manager():
    def __init__(self,**kwargs):
        self.config   = Config("config.ini")
        self.cuts     = Config("cuts.ini")
        self.plotter  = Plotter(manager=self,**kwargs)
        self.branches = Branches(manager=self,**kwargs)
        self.aux      = Aux(manager=self,**kwargs)
