from branches import Branches
import matplotlib as mpl
import ROOT as R
class Plotter():
    def __init__(self,manager):
        self.m = manager

    def get_branches(self,branches): 
        self.tree = branches

    def energy_spectra(self,**pars):
        c = R.TCanvas("c", "c", 0, 0, 700, 500)
        hs = [R.TH1F("h"+str(i),"",pars["nbins"],pars["min"],pars["max"]) for i in range(len(pars["cuts"]))]
        for i in range(len(pars["cuts"])):
            hs[i].SetLineColor(i+1)
            hs[i].SetLineWidth(2)
            # do energy resolution stuff from helper
            self.tree.Draw("depTPCtot>>"+"h"+str(i),pars["cuts"][i],"hist" if i==0 else "hist same")
        c.SetLogy()
        c.Update()
        c.SaveAs("test.pdf")