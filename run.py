import numpy as np
from manager import Manager
import warnings
warnings.filterwarnings("ignore")

m = Manager()

class Run():
    def __init__(self,fmc,fbg=None):  
        self.branches = m.branches(m.config('run',"path",'str')+fmc,"mc") 
        

##### Run ####
fmc  = m.config('run','mc','str')
#fbg  = m.config('run',"bg","str")
tune = Run(fmc)