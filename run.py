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
        
        # defining here the cuts for later use along with a label
        self.cut_labels                 = {
                "depTPCtot>0":"edep",      
                "depTPCtot>0 && nclus==1":"edep single",        
                "depTPCtot>0 && nclus==1 && nclus_nucl==1 && nclus_elec==0":"NR SS",
                "depTPCtot>0 && nclus_nucl>0 && nclus_elec>0":"NR and ER",        
                "depTPCtot>0 && nclus_nucl>0 && nclus_elec>0 && isFV30==1":"NR and ER FV",
                "depTPCtot>0 && nclus_nucl==0 && nclus_elec>0":"ER",        
                "depTPCtot>0 && nclus==1 && nclus_nucl==1 && nclus_elec==0 && isFV30==1":"NR SS in FV",        
                "depTPCtot>0 && nclus==1 && nclus_nucl==1 && nclus_elec==0 && isFV30==1 && v2nclus==0":"Pure NR SS in FV",        
                "depTPCtot>0 && nclus==1 && nclus_nucl==1 && nclus_elec==0 && v2nclus_elec>0 && depVeto2tot>4200 && depVeto2tot<4500 ":"NR SS in FV (AmBe)",        
                "depTPCtot>0 && nclus==1 && nclus_nucl==1 && nclus_elec==0 && isFV30==1 && v2nclus>0 && depVeto2tot>4200 && depVeto2tot<4500":"NR SS in FV (AmBe)",        
                "depTPCtot>0 && nclus==1 && nclus_nucl==0 && nclus_elec==1 && isFV30==1":"ER SS in FV",       
                "depTPCtot>0 && nclus_nucl==2 && nclus_elec==0 && isFV30==1":"NR DS in FV",        
                "depTPCtot>0 && nclus_nucl==2 && nclus_elec==0 && isFV30==1":"NR DS in FV",        
                "depTPCtot>0 && nclus_nucl==1 && nclus==1 && v2nclus_elec>0 && isFV30==1":"NR SS in FV with ER in Veto",
                        }
        self.cut_labels = {label:cut for cut,label in self.cut_labels.items()}                    # switch between cuts and labels (lazy after it was already written)

        # Apply cuts and store stats in dic for computing rates
        for label,cut in self.cut_labels.items():
            m.branches.cut_branches(cut,label)

        # Plotting
        m.plotter.get_branches(self.tree_mc)                
        self.cut_plots = ["depTPCtot>0",
                        "depTPCtot>0 && nclus_nucl==1 && nclus_elec==0 && nclus==1",
                        "depTPCtot>0 && nclus_elec==1 && nclus==1",
                        "depTPCtot>0 && nclus_nucl==1 && nclus_elec==0 && nclus==1 && isFV30==1"]
        self.cut_plot_gammas = ["depTPCtot>0",
                        "depTPCtot>0 && nclus_nucl==0 && nclus_elec>0",
                        "depTPCtot>0 && nclus_nucl>0 && nclus_elec>0",
                        "depTPCtot>0 && nclus_elec==1 && nclus==1 && isFV30==1"]
        if self.source_type == "g":
            self.cut_plots = ["depTPCtot>0", "depTPCtot>0 && nclus_elec==1"]

        #m.plotter.doke_plot(fields=[200,150,100],energy=[1117],source=["co60"],min=[1170*8 - 1000],max=[1170*8+1000])
    
        '''Plotting: the energy_spectra function will automatically add gamma bg provided in the same directory
                    only for the depTPCtot>0 cut and a cut containing nclus_elec==1 for single scatter gammas.
                    Other bg statistics not implemented yet.
                    Keep the depTPCtot as the first cut for bg addition to work (modify this eventually)'''
        #spectrum before bg
        #m.plotter.energy_spectra(nbins=200,min=0,max=12000 if self.source_type=="n" else 2500,res=True,scale=self.scaleF,name="ene",   cuts=self.cut_plots)
        #m.plotter.energy_spectra(nbins=100,min=0,max=200,                                     res=True,scale=self.scaleF,name="lowene",cuts=self.cut_plots,range=[1,2e-4])

        #if self.source_type == "n":
        #    m.plotter.energy_spectra(nbins=200,min=0,max=12000,res=True,scale=self.scaleF,name="gammas",cuts=self.cut_plot_gammas)

        ## spectrum after bg 
        #m.plotter.energy_spectra(nbins=200,min=0,max=12000                                   ,bg=True,res=True,scale=self.scaleF,name="enebg",   cuts=["depTPCtot>1","depTPCtot>1 && nclus_elec==1 && nclus==1"])
        #m.plotter.energy_spectra(nbins=100,min=0,max=200,                                     bg=True,res=True,scale=self.scaleF,name="lowenebg",cuts=["depTPCtot>1","depTPCtot>1 && nclus_elec==1 && nclus==1"])

        #if self.source_type == "n":
        #    m.plotter.energy_spectra(nbins=200,min=0,max=12000,res=True,scale=self.scaleF,name="gammas",cuts=self.cut_plot_gammas)

        # before bg
        m.plotter.spatial_distribution(var="xy",nbins=100,min=-200,max=200,s = "g",title="xy",scale=self.scaleF, cuts="depTPCtot>0 && nclus_elec>0 && nclus_nucl==0")
        m.plotter.spatial_distribution(var="xz",nbins=100,min=-200,max=200,s = "g",title="xz",scale=self.scaleF, cuts="depTPCtot>0 && nclus_elec>0 && nclus_nucl==0")
        m.plotter.spatial_distribution(var="xy",nbins=100,min=-200,max=200,s = "g",bg=True,title="xybg",scale=self.scaleF, cuts="depTPCtot>0 && nclus_elec>0 && nclus_nucl==0")
        m.plotter.spatial_distribution(var="xz",nbins=100,min=-200,max=200,s = "g",bg=True,title="xzbg",scale=self.scaleF, cuts="depTPCtot>0 && nclus_elec>0 && nclus_nucl==0")

        # def a process to check for XY reco
        # m.plotter.xy_resolution()        

        #Print stats
        str_len = 20                                                                          # to make output uniform
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