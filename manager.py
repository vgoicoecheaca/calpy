from plotter import Plotter 
from config import Config
from branches import Branches

class Manager():
    def __init__(self,**kwargs):
        self.config   = Config()
        self.plotter  = Plotter(manager=self,**kwargs)
        self.branches = Branches(manager=self,**kwargs)
