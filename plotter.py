from branches import Branches
import numpy as np
import ROOT as R

class Plotter():
    def __init__(self,manager):
        self.m = manager
        self.fbg  = R.TFile(self.m.config('run','bg','str'))
        self.h_bg      = {}
        self.bg_labels = ["enebg","enesbg","lowbg","lowsbg","xybg","xysbg","xzbg","xzsbg"]
        for i,label in enumerate(self.bg_labels):
            self.h_bg[label] = self.fbg.Get(label)

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
        c.SaveAs("plots/"+pars["name"]+".pdf")
        if "res" in pars.keys() and pars["res"]:
            cr   = R.TCanvas("cr", "cr", 0, 0, 700, 500)
            h_res = self.apply_energy_res(hs,pars["nbins"],pars["min"],pars["max"])  
            for i in range(len(pars["cuts"])):
                h_res[i].Scale(pars["scale"] if "scale" in pars.keys() else 1)
                h_res[i].GetYaxis().SetTitle("Rate [s^{-1}]")
                h_res[i].GetXaxis().SetTitle("Energy [keV]")
                bg_str = "enebg" if pars["max"]>300 else "lowbg"
                if i == 0 or "nclus_elec==1" in pars["cuts"][i]:
                    #h_res[i].Add(self.h_bg[bg_str[:3]+"s"+bg_str[3:] if "nclus_elec==1" in pars["cuts"][i] else bg_str])
                    h_res[i].Add(self.h_bg[bg_str[:3]+"s"+bg_str[3:] if i!=0 else bg_str])
                h_res[i].Draw("HIST" if i==0 else "HIST same") 
                if "bg" in pars.keys() and pars["bg"]:
                    self.h_bg[bg_str].SetLineColor(2)
                    self.h_bg[bg_str].Draw("HIST same") 
            cr.SetLogy()
            cr.Update()
            cr.SaveAs("plots/"+pars["name"]+"_res.pdf")

    def spatial_distribution(self,**pars):   
        cs = R.TCanvas("cs","cs",0,0,700,550)
        h  =  R.TH2F("h",pars["nbins"],pars["min"],pars["max"],pars["nbins"],pars["min"],pars["max"])
        var  = "dep_y/100:dep_x/100" if pars["var"] == "xy" else "dep_z/100:dep_x/100"
        cs.SetLogy()
        cs.SetFillColor(10)
        bg_str = pars["var"]+"sbg" if "nclus" in pars["cuts"] else pars["var"]+"bg"
        h.Add(self.h_bg[bg_str])
        self.tree.Draw(var,pars["cuts"],"COLZ")
        if var =="xz":
            h.GetYaxis().SetRangeUser(-1.85,1.85)
        cs.Update()
        cs.SaveAs("plots/"+pars["title"]+".pdf")

    def doke_plot(self):
        '''S2/E vs S1/E or g2 vs g1 for different fiel configurations'''

    def psd(self):
        '''PSD plot: f90 vs S1,test with other file for now (ReD)''' 
        '''Shaded region?BG?'''
        #fd = R.TF2("f2","xygaus + xygaus(5) + xylandau(10)",0,1000,0,1); #generate fake data
        c = R.TCanvas()
        f = R.TF2("f","xygaus(5) + xylandau(8)",0,1000,0,1)
        f.SetParameters(150,1231,1000,12,800, 3600,22,123,1,800)
        fd = R.TH2F("h","xygaus(5) + xylandau(8)",100,0,1000,100,0,1)
        fd.FillRandom("f",40000)
        fd.Draw("COLZ")
        g1,g2,g3 = self.neutron_psd()
        g1.Draw("l")
        g2.Draw("l")
        g3.Draw("f")
        fd.GetXaxis().SetTitle("S1 [PE]")
        fd.GetYaxis().SetTitle("f90")
        c.SaveAs("plots/psd.pdf") 
      
    def xy_resolution(self,files):
        #R.gStyle.SetPalette(57)
        c = R.TCanvas() 
        hs = R.TH2F("h","",100,-200,200,100,-200,200)   
        pos = [-100,0,100]
        pm = 20 
        fs = [R.TF2("g"+str(i),"gaus",pos[i]-pm,pos[i]+pm,0-pm,0+pm) for i in range(len(pos))]
        for i,p in enumerate(pos):
            for n in range(100000):
                hs.Fill(np.random.normal(p, 15, 1)[0],np.random.normal(0, 15, 1)[0])
            print(fs[i])
            fs[i].SetContour(20)
            hs.SetContour(20)
            #hs.Fit("g"+str(i),"R" if i==0 else "R+")
        #hs.Fit('gaus')
        #hs.SetContour(10)
        #hs.SetFillColor(45)
        #hs.GetXaxis().SetTitle("X [cm]")
        #hs.GetYaxis().SetTitle("Y [cm]")
        hs.Draw("LEGO2Z")
        c.SaveAs("plots/res.pdf")
        #self.m.branches.get_xys(files)
        #for i, p in enumerate(pos):
        #compare the mc with reconstructed???
    
    def neutron_psd(self):
        x = [0,10,20,100,200,300,400,500,800,1000]
        ymin = [1,0.95,0.92,0.85,0.75,0.7,0.7,0.7,0.7,0.7]
        ymax = [1 for i in range(len(x))]

        g = R.TGraph(len(x))
        g.SetLineColor(6)
        for i in range(len(x)):
            g.SetPoint(i,x[i],ymin[i])

        g2 = R.TGraph(len(x))
        g2.SetLineColor(6)
        for i in range(len(x)):
            g2.SetPoint(i,x[i],ymax[i])

        g3 = R.TGraph(100)
        g3.SetFillStyle(3013)
        g3.SetFillColor(6)
        for i in range(len(x)):
            g3.SetPoint(i,x[i],ymax[i])
            g3.SetPoint(10+i,x[len(x)-i-1],ymin[len(x)-i-1])

        l1 = R.TGraph(3)        
        l1.SetLineColor(2)
        l2 = R.TGraph(3)
        l2.SetLineColor(2)

        return g,g2,g3,l1,l2