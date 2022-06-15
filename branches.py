import ROOT as R
import numpy as np

class Branches():
    def __init__(self,manager):
        self.manager        = manager
        self.cut_stats      = {}

    def __call__(self,file,tree):                   
        self.file = R.TFile(file,"read")
        self.tree = self.file.Get(tree)
    
        return self.tree, self.cut_stats
        
    def add_branch(self,name,func):       
        self.tree.SetAlias(name,func)

    def cut_branches(self,cut):           
        self.tree = self.tree(cut)
        self.cut_stats[cut] = self.tree.GetEntreis(cut)