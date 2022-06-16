from binascii import hexlify
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
        h_res      = [R.TH1F("h"+str(i)+"res","",bins,min,max) for i in range(len(hs))]
        for i in range(len(h_res)):
            h_res[i].SetLineColor(1+i)
            h_res[i].SetLineWidth(2)
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
            cr.Update()
            h_res = self.apply_energy_res(hs,pars["nbins"],pars["min"],pars["max"])  
            for i in range(len(pars["cuts"])):
                h_res[i].Scale(pars["scale"] if "scale" in pars.keys() else 1)
                h_res[i].GetYaxis().SetTitle("Rate [s^{-1}]")
                h_res[i].GetXaxis().SetTitle("Energy [keV]")
                h_res[i].Draw("HIST" if i==0 else "HIST same") 
            cr.SetLogy()
            cr.Update()
            cr.SaveAs("plots/"+pars["name"]+"_res.pdf")

    def spatial_distribution(self,**pars):   
        cs = R.TCanvas("cs","cs",0,0,700,550)
        h  =  R.TH2F("h",pars["nbins"],pars["min"],pars["max"],pars["nbins"],pars["min"],pars["max"])
        var  = "dep_y/100:dep_x/100" if pars["var"] == "xy" else "dep_z/100:dep_x/100"
        cs.SetLogy()
        cs.SetFillColor(10)
        self.tree.Draw(var,pars["cuts"],"COLZ")
        if var =="xz":
            h.GetYaxis().SetRangeUser(-1.85,1.85)
        cs.Update()
        cs.SaveAs("plots/"+pars["title"]+".pdf")

    def psd(self):
        print("hello there psd")
    
    def xy_resolution(self):
        print("Heljo there XY Res")