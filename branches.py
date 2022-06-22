import ROOT as R
import numpy as np

class Branches():
    def __init__(self,manager):
        self.manager              = manager
        self.cut_stats            = {}

    def __call__(self,file,tree):                   
        self.file = self.read_file(file)
        self.tree = self.read_tree(self.file,tree)

        return self.tree, self.cut_stats
    
    def read_file(self,file): return R.TFile(file,"read")

    def read_tree(self,file,tree): return file.Get(tree)

    def add_branch(self,name,func):       
        self.tree.SetAlias(name,func)

    def cut_branches(self,cut,label):           
        self.cut_stats[label] = self.tree.GetEntries(cut)

    def get_xys(self,files,tree):
        xys = {}
        for file in files:
            f = self.read_file(file)            
            t = self.read_tree(f,tree)
            xys[file] = [t["cl_x"],t["cl_y"]]
        return xys