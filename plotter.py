from re import I
from branches import Branches
import matplotlib as mpl
import ROOT as R

class Plotter():
    def __init__(self,manager):
        self.m = manager

    def get_branches(self,branches): 
        self.tree = branches

    def apply_energy_res(self,hs,bins,min,max):
        f1_smear   = R.TF1("f1_smear",  "gaus");
        f1_res     = R.TF1("f1_res",   "0.0073 + 0.418/sqrt(x)", min, max);
        h_res      = [hs[i].Clone("h"+str(i)+"res") for i in range(len(hs))]
        for i in range(len(hs)):
            h_res[i].Reset()
            for n in range(1,bins):
                bincenter       = int(hs[i].GetBinCenter(n))
                bincontent      = int(hs[i].GetBinContent(n))
                binres          = f1_res.Eval(bincenter)
                f1_smear.SetParameters(1, bincenter, bincenter*binres)
                h_res[i].FillRandom("f1_smear", bincontent)
        
        return h_res

    def energy_spectra(self,**pars):
        c   = R.TCanvas("c", "c", 0, 0, 700, 500)
        hs  = [R.TH1F("h"+str(i),"",pars["nbins"],pars["min"],pars["max"]) for i in range(len(pars["cuts"]))]
        for i in range(len(pars["cuts"])):
            hs[i].SetLineColor(i+1)
            hs[i].SetLineWidth(2)  
            self.tree.Draw("depTPCtot>>"+"h"+str(i),pars["cuts"][i],"hist" if i==0 else "hist same") 
        c.SetLogy()
        c.Update()
        if "name" in pars.keys():
            c.SaveAs("plots/"+pars["name"]+".pdf")
        if "res" in pars.keys() and pars["res"]:
            cr   = R.TCanvas("cr", "cr", 0, 0, 700, 500)
            h_res = self.apply_energy_res(hs,pars["nbins"],pars["min"],pars["max"])
            for i in range(len(pars["cuts"])):
                h_res[i].GetXaxis().SetTitle("Energy [keV]")
                self.tree.Draw("depTPCtot>>"+"h"+str(i)+"res",pars["cuts"][i],"hist" if i==0 else "hist same") 
            cr.SetLogy()
            cr.Update()
            cr.SaveAs("plots/"+pars["name"]+"_res.pdf")

    def spatial_distribution(self):   
        print("Hell there")

    def psd(self):
        print("hello there psd")
    
    def xy_resolution(self):
        print("Hello there XY Res")