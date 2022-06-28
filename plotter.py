from re import I
from branches import Branches
from array import array
import numpy as np
import ROOT as R

class Plotter():
    def __init__(self,manager):
        self.m = manager
        self.fbg  = R.TFile(self.m.config('ene','bg','str'))
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
                if "bg" in pars.keys() and pars["bg"]:
                    h_res[i], bg_str  = self.add_bg(h_res[i],pars["cuts"][i],low=False if pars["max"]>300 else True) 
                    #h_res[i].Add(self.h_bg[bg_str]) 
                    if "range" in pars.keys():
                        self.h_bg[bg_str].SetAxisRange(pars["range"][1],pars["range"][0],"Y")
                    self.h_bg[bg_str].Draw("HIST same")
                if "range" in pars.keys():
                    h_res[i].SetAxisRange(pars["range"][1],pars["range"][0],"Y")
                h_res[i].Draw("HIST same") 
            cr.SetLogy()
            cr.Update()
            cr.SaveAs("plots/"+pars["name"]+"_res.pdf")

    def spatial_distribution(self,**pars):   
        cs = R.TCanvas()
        #cs.SetLogz()
        h  =  R.TH2F("h","",pars["nbins"],pars["min"],pars["max"],pars["nbins"],pars["min"],pars["max"]) 
        var  = "cl_y:cl_x" if pars["var"] == "xy" else "cl_z:cl_x" 
        bg_str = pars["var"]+"sbg" if "nclus" in pars["cuts"] else pars["var"]+"bg"
        h.GetXaxis().SetTitle("X [cm]")
        h.GetYaxis().SetTitle("Y [cm]")
        h.GetZaxis().SetTitle("Rate [Events/sec]")
        if pars["var"] =="xz":
            h.GetYaxis().SetTitle("Z [cm]")
            h.GetYaxis().SetRangeUser(-185,185)
        self.tree.Draw(var+">>h",pars["cuts"],"COLZ")
        R.gStyle.SetPadRightMargin(0.16)
        h.Scale(50/h.Integral() if pars["s"] == "n" else pars["scale"] )                                            #cheap fix, come back to this 
        if "bg" in pars.keys() and pars["bg"]:
            bg_str = pars["var"]+"sbg" if "nclus_elec==1" in pars["cuts"] else pars["var"]+"bg"
            integral = self.h_bg[bg_str].Integral()
            self.h_bg[bg_str].Scale( (43/integral) if "s" in bg_str else 84/integral)                                                   # there was a bug, total bg rate should be 84Hz for all deposits and 43 for single scatters, roughly
            h.Add(self.h_bg[bg_str])
        print("After adding", h.Integral())
        cs.Update()
        cs.SaveAs("plots/"+pars["title"]+".pdf")

    def doke_plot(self,**pars):
        '''S2/E vs S1/E or g2 vs g1 for different fiel configurations
            peak dependent, 
            field dependent
            should be scatter plot'''
        c = R.TCanvas()
        texs,gs = [],[]
        for n,field in enumerate(pars["fields"]):
            xs,ys,xs_err,ys_err = [],[],[],[]
            # get the data from the self.m.branches  
            # create fake data for development
            cent,dev  = 1170, 800 
            minf,maxf = 1170*8 - 800, 1170*8 + 800
            s1, s2 = R.TH1F("s1","",400,minf,maxf),R.TH1F("s2","",4000,minf*20,maxf*20)
            for i in range(100000):
                s1.Fill(np.random.normal(cent*8,dev,1)[0])
                s2.Fill(np.random.normal(cent*20,dev*20,1)[0]) # end of fake data 

            for i,energy in enumerate(pars["energy"]): 
                fit_s1 = self.m.aux.fit_peak_with_gaus(s1,minf,maxf)
                fit_s2 = self.m.aux.fit_peak_with_gaus(s2,minf*20,maxf*20) # remember this is an approximation
                c.SaveAs("test"+str(i)+".pdf")
                print("HERE", fit_s1[1])
                xs.append(fit_s1[1]/energy)
                ys.append(fit_s2[1]/energy)
                xs_err.append(fit_s1[2]/energy)
                ys_err.append(fit_s2[2]/energy)
                texs.append(R.TLatex(xs[i]*1.1,ys[i]*1.1,str(field)+" kV/cm"))
                texs[n+i].SetTextColor(n+1)
                texs[n+i].Draw()
            print(xs)
            gs.append(R.TGraphErrors(len(xs),array("f",xs),array("f",ys),array("f",xs_err),array("f",ys_err)))
            gs[n].GetYaxis().SetRangeUser(0,100)
            gs[n].GetXaxis().SetRangeUser(0,10)
            gs[n].SetMarkerColor(n+1)
            gs[n].GetXaxis().SetTitle("g1 [photon/keV]")
            gs[n].GetYaxis().SetTitle("g2 [PE/kev]")
            gs[n].Draw("PA")
        c.SaveAs("plots/doke.pdf")

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
      
    def xy_resolution(self,**pars):
        c = R.TCanvas() 
        hs = R.TH2F("h","",100,-200,200,100,-200,200)   
        pos = self.m.config("xy","pos","str").split()
        h = R.TH2F("h","",100,-200,200,100,-200,200)
        pos = [int(p) for p in pos]
        pm = 20 
        #fs = [R.TF2("g"+str(i),"gaus",pos[i]-pm,pos[i]+pm,0-pm,0+pm) for i in range(len(pos))]
        if "show" in pars.keys():
            h.SetContour(10)
            h.SetFillColor(45)
            hs.GetXaxis().SetTitle("X [cm]")
            hs.GetYaxis().SetTitle("Y [cm]")
            self.tree.Draw("cl_y:cl_x>>h","depTPCtot>0","LEGO2Z")
        #hs.Draw("LEGO2Z")
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

        return g,g2,g3


    def add_bg(self,h,cut,low=False):
        bg_str = "lowbg" if low else "enebg"
        h.Add(self.h_bg[bg_str[:3]+"s"+bg_str[3:] if "nclus_elec==1" in cut else bg_str])
        self.h_bg[bg_str].SetLineColor(24 if "nclus_elec==1" in cut else 20)
        self.h_bg[bg_str].SetLineStyle(0)
        self.h_bg[bg_str].SetFillColorAlpha(24 if "nclus_elec==1" in cut else 20,0.1)
        self.h_bg[bg_str].GetYaxis().SetTitle("Rate [Events/sec]")
        return h , bg_str
