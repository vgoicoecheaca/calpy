from multiprocessing import managers
import sys
import awkward as ak
import uproot as ur
import numpy as np

class Branches():
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __init__(self,manager):
        self.m              = manager
        self.branches_mc    = manager.config("branches","mc","str").split(",") 
        self.branches       = {}
        self.nevents        = manager.config("run","nevents","int")
        
    def __repr__(self) -> str:
        return self.branches.keys()

    def __call__(self,file,mode):    
        self.mode = mode   
        if mode =="mc":
            branches_names = self.branches_mc
        for branch in branches_names:
            print("Reading file, branch",file,branch)
            self.branches[branch] = self.read_branch(file,branch) 

        self.change_branch(self.branches_mc,[branch+"_mc" for branch in self.branches_mc])

        return self.branches

    def add_branch(self,branch,data):
        self.branches[branch] = data

    def read_branch(self,fname,branch):       
        return ur.open(fname)["dstree"][branch].array(library="np")[:self.nevents]

    def cut_branches(self,cut,data="run"):
        for key in self.branches.keys():
            if data in key:
                self.branches[key] = self.branches[key][cut]

    def change_branch(self,olds, news):
        for i in range(len(olds)):
            self.branches[news[i]] = self.branches[olds[i]]
            del self.branches[olds[i]]