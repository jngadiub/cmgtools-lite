#!/bin/env python                                                                                                                                                                                                                                                               
import ROOT
import json
import math
from time import sleep
import optparse, sys

parser = optparse.OptionParser()


parser.add_option("-c","--cut",dest="cut",help="0p05 or 0p10 etc",default='0p05')
parser.add_option("-i","--indir",dest="indir",help="input directory",default='')
parser.add_option("-o","--outdir",dest="outdir",help="output directory",default='')
parser.add_option("-t","--tagger",dest="tagger",help="W or ZH",default='W')
(options,args) = parser.parse_args()
c = options.cut 


# first rebin pseudodata
mapfile = "myDeepBoostedMap_"+c+"rho.root"
print mapfile
r_file = ROOT.TFile(str(options.indir)+mapfile,"READ")
print r_file
mapname = "DeepBoosted_WvsQCD_v_rho_v_pT_scaled_yx"  #DeepBoosted_WvsQCD_v_rho_v_pT_yx"
if options.tagger=="ZH": mapname = "DeepBoosted_ZHbbvsQCD_v_rho_v_pT_sclaed_yx" #"DeepBoosted_ZHbbvsQCD_v_rho_v_pT_yx"
cutmap = r_file.Get(mapname)
print cutmap
#print data.GetXaxis().GetNbins()

cutmap.SetName(mapname+"_"+c)


r_file_out = ROOT.TFile(str(options.outdir)+mapfile,"RECREATE")
cutmap.Write(mapname+"_"+c)

print r_file_out


