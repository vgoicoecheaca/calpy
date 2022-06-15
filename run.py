import numpy as np
from manager import Manager
import warnings
warnings.filterwarnings("ignore")

m = Manager()

class Run():
    def __init__(self,fmc,fbg=None):  
        self.tree_mc,self.cut_stats_mc  = m.branches(m.config('run',"path",'str')+fmc,"dstree") 
        #self.tree_bg,self.cut_stats_bg  = None if fbg==None else m.branches(m.config('run',"path",'str')+fbg,"dstree") 
        self.neutron_yield = 100;

        # Apply cuts and store stats in dic for computing rates
        print(self.cut_stats_mc) 
        m.branches.cut_branches("depTPCtot>0")        
        print(self.cut_stats_mc)
 
    # Apply cuts and store stats in dic for computing rates
    #m.branches.cut_branches(self.branches["depTPCtot"]>0)
    #m.branches.

    # events with energy deposit 
    

    #m.branches.cut_branches((self.branches["s1npe_run"]>s1min) & (self.branches["s1npe_run"]<s1max))

    #nevts_edep                       = t1 ->GetEntries(cut_edep);
    #nevets_singles 			         = t1 ->GetEntries("depTPCtot>0 && nclus==1");
    #nevents_singles_NR               = t1->GetEntries("depTPCtot>0 && nclus_nucl==1 && nclus_elec==0"); 
    #nevents_nr_tpc_w_gamma           = t1->GetEntries("depTPCtot>0 && nclus_nucl>0 && v2nclus_elec>0 && depVeto2tot>4200 && depVeto2tot<4500"); 
    #nevents_nr_tpc_w_gamma_time      = t1->GetEntries("depTPCtot>0 && nclus_nucl>0 && v2nclus_elec>0 && v2cl_t[0]<2"); 
    #source_livetime                  = nevts_tot/neutron_yield;



    # implement an option for neutron vs gamma source and what's default by each of this options


    # def a proccess to check for the PSD 


    # def a process to check for XY reco





##### Run ####
fmc  = m.config('run','mc','str')
#fbg  = m.config('run',"bg","str")
tune = Run(fmc)