#!/bin/env python                                                                                                                                                                                                                                                               
import ROOT
import json
import math
from time import sleep
import optparse, sys

parser = optparse.OptionParser()


parser.add_option("-c","--category",dest="category",help="VV_HPHP or VV_HPLP or VH_HPHP etc",default='VV_HPLP')
parser.add_option("-i","--indir",dest="indir",help="input directory",default='')
parser.add_option("-o","--outdir",dest="outdir",help="output directory",default='')
parser.add_option("-b","--binning",dest="binning",help="rebinning factor",type="int",default=1)
(options,args) = parser.parse_args()
purity = options.category
rebin= options.binning


# first rebin pseudodata
pseudo = "JJ_PD_"+str(purity)+".root"

r_file = ROOT.TFile(str(options.indir)+pseudo,"READ")
data = r_file.Get("data")
nonRes = r_file.Get("nonRes")

#print data.GetXaxis().GetNbins()

data.RebinX(rebin)

#print data.GetXaxis().GetNbins()

data.RebinY(rebin)

nonRes.RebinX(rebin)
nonRes.RebinY(rebin)


r_file_out = ROOT.TFile(str(options.outdir)+pseudo,"RECREATE")
data.Write()
nonRes.Write("nonRes")




# then rebin also templates
generators = ["pythia","madgraph","herwig"]
for gen in generators:
    print "gen"
    templ = "save_new_shapes_2016_"+gen+"_"+str(purity)+"_3D.root"
    f_templ = ROOT.TFile(str(options.indir)+templ,"READ")
    fout_templ = ROOT.TFile(str(options.outdir)+templ,"RECREATE")
    for key in f_templ.GetListOfKeys():
        print key.GetName()
        kname = key.GetName()
        hist = f_templ.Get(kname)
        #print hist.GetEntries()
        #print hist.GetXaxis().GetNbins()
        hist.RebinX(rebin)
        hist.RebinY(rebin)
        #print hist.GetXaxis().GetNbins()
        hist.Write()
