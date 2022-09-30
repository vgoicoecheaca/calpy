from manager import Manager
m = Manager()
class Run():
    def __init__(self,fmc,fbg=None):  
        self.tree_mc, self.cut_stats_mc  = m.branches(fmc,"dstree") 
        self.source_type                 = m.config("source","type","str")
        #self.bg_hist                    = m.branches.get_bg("gamma_bg_tpc.root")  #as of now bg only in all edeps mode:
        #self.tree_bg,self.cut_stats_bg  = None if fbg==None else m.branches(m.config('run',"path",'str')+fbg,"dstree") 
        self.cut_stats_mc["nevents"]    = self.tree_mc.GetEntries()
        self.activity                   = m.config("source","activity","int")
        self.scaleF                     = self.activity/self.cut_stats_mc["nevents"]
        
        # read the cuts from file        
        self.cuts = m.cuts.sec("cuts")
        self.cuts_description = m.cuts.sec("description")  
        self.cut_plots       = [self.cuts[cut] for cut in m.cuts("plots","general","str").split(",")]
        self.cut_plot_gammas = [self.cuts[cut] for cut in m.cuts("plots","gammas","str").split(",")]
        self.cut_bg          = [self.cuts[cut] for cut in m.cuts("plots","bg","str").split(",")]
        if self.source_type == "g": self.cut_plots = [self.cuts[cut] for cut in ["edep","er_ss"]]

        # Apply cuts and store stats in dic for computing rates
        for label,cut in self.cuts.items():
            print(cut)
            m.branches.cut_branches(cut,label)

        ####################
        #### Plotting ###### 
        ####################
        '''Plotting: the energy_spectra function will automatically add gamma bg provided in the same directory
                     only for the depTPCtot>0 cut and a cut containing nclus_elec==1 for single scatter gammas.
                     Other bg statistics not implemented yet.
                     Keep the depTPCtot as the first cut for bg addition to work (modify this eventually)'''

        m.plotter.get_branches(self.tree_mc)                
        # double scatters
        m.plotter.hist("nclus",0,15,["depTPCtot>0","depTPCtot>0 && nclus_elec>0","depTPCtot>0 && nclus_nucl>0"],10,"nclus")
        m.plotter.hist("dep_time",0,8,["depTPCtot>0","depTPCtot>0 && nclus_elec>0","depTPCtot>0 && nclus_nucl>0"],200,"dep_time")

        #hist(self,var,mn,mx,cuts,bins,name,scale=None):
        exit()

        #m.plotter.doke_plot(fields=[200,150,100],energy=[1117],source=["co60"],min=[1170*8 - 1000],max=[1170*8+1000])
 
        # plot bg only
        m.plotter.plot_bg(name="test_bg",nbins=200,cuts=self.cut_bg,min=0,max=3000,res=True,scale=self.scaleF)

        #spectrum before bg
        m.plotter.energy_spectra(nbins=200,min=0,max=12000 if self.source_type=="n" else 3000,res=True,scale=self.scaleF,name="ene",   cuts=self.cut_plots)
        m.plotter.energy_spectra(nbins=100,min=0,max=200,                                     res=True,scale=self.scaleF,name="lowene",cuts=self.cut_plots,range=[1,2e-4])

        if self.source_type == "n":
            m.plotter.energy_spectra(nbins=200,min=0,max=12000,res=True,scale=self.scaleF,name="gammas",cuts=self.cut_plot_gammas)

        # spectrum after bg 
        m.plotter.energy_spectra(nbins=200,min=0,max=3000,bg=True,res=True,scale=self.scaleF,name="enebg",   cuts=self.cut_bg,range=[10,2e-4])
        m.plotter.energy_spectra(nbins=100,min=0,max=200, bg=True,res=True,scale=self.scaleF,name="lowenebg",cuts=self.cut_bg,range=[10,2e-4]) 

        if self.source_type == "n":
            m.plotter.energy_spectra(nbins=200,min=0,max=12000,res=True,scale=self.scaleF,name="gammas",cuts=self.cut_plot_gammas)

        # before bg
        #m.plotter.spatial_distribution(var="xy",nbins=100,min=-200,max=200,s = self.source_type,title="xy",scale=self.scaleF, cuts=self.cut_bg)
        #m.plotter.spatial_distribution(var="xz",nbins=100,min=-200,max=200,s = self.source_type,title="xz",scale=self.scaleF, cuts=self.cut_bg)
        #with  
        #m.plotter.spatial_distribution(var="xy",nbins=100,min=-200,max=200,s = self.source_type,bg=True,title="xybg",scale=self.scaleF, cuts=self.cut_bg)
        #m.plotter.spatial_distribution(var="xz",nbins=100,min=-200,max=200,s = self.source_type,bg=True,title="xzbg",scale=self.scaleF, cuts=self.cut_bg)

        ## def a process to check for XY reco
        #if self.source_type == "g":
        #    m.plotter.xy_resolution()        

        # check PSD for neutron sources 
        if self.source_type=="n":
            m.plotter.psd()

        # check for LY uniformities given current optical model (DS50 based) for distributed sources (Kr83m, Rn220)
        if self.source_type == "d":
            m.plotter.ly_map(bins=50,peak_ene=41,lymin=0,lymax=500)

        #Print stats
        str_len = 25                                                                          # to make output uniform
        print("//////////////////////////////////////")
        print("////////// Cuts Description //////////////")
        print("//////////////////////////////////////")
        for i, name in enumerate(self.cuts_description.keys()):
             print(name+(str_len-len(name))*" ",self.cuts_description[name])
        print("//////////////////////////////////////")
        print("////////// Events/decay //////////////")
        print("//////////////////////////////////////")
        for i, name in enumerate(self.cut_stats_mc.keys()):
            print(name+(str_len-len(name))*" ","{:.2e}".format(self.cut_stats_mc[name]/self.cut_stats_mc["nevents"]))
        print("/////////////////////////////////////// ")
        print("//////// Rates in [Events/sec]///////// ")
        print("/////////////////////////////////////// ")
        for i, name in enumerate(self.cut_stats_mc.keys()):
            print(name,(str_len-len(name))*" ","{:.2e}".format(self.cut_stats_mc[name]*(self.activity/self.cut_stats_mc["nevents"])))

    # implement an option for neutron vs gamma source and what's default by each of this options

    # def a proccess to check for the PSD 
    #m.plotter.psd()

##### Run ####
#if one file
path = m.config('ene',"path",'str')
fmc  = path + m.config('ene','mc','str')
#if several files
tune = Run(fmc)
