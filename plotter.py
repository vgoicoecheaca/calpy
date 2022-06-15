import matplotlib.pyplot as plt
from branches import Branches
import numpy as np
from cmocean.cm import dense
import matplotlib as mpl
from scipy.interpolate import interp1d
import ROOT as R
from array import array

plt.style.use('mystyle.mlstyle')

class Plotter():
    def __init__(self,manager):
        self.m = manager

    def get_branches(self,branches): 
        self.branches = branches

