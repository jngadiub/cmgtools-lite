#!/usr/bin/env python

import ROOT
from array import array
from CMGTools.VVResonances.plotting.TreePlotter import TreePlotter
from CMGTools.VVResonances.plotting.MergedPlotter import MergedPlotter
from CMGTools.VVResonances.plotting.StackPlotter import StackPlotter
from CMGTools.VVResonances.statistics.Fitter import Fitter
from math import log
import os, sys, re, optparse,pickle,shutil,json
ROOT.gROOT.SetBatch(True)



parser = optparse.OptionParser()
parser.add_option("-s","--sample",dest="sample",default='',help="Type of sample")
parser.add_option("-c","--cut",dest="cut",help="Cut to apply for shape",default='')
parser.add_option("-o","--output",dest="output",help="Output JSON",default='')
parser.add_option("-m","--min",dest="mini",type=float,help="min MJJ",default=40)
parser.add_option("-M","--max",dest="maxi",type=float,help="max MJJ",default=160)
parser.add_option("--store",dest="store",type=str,help="store fitted parameters in this file",default="")
parser.add_option("--corrFactorW",dest="corrFactorW",type=str,help="add correction factor xsec",default=1.)
parser.add_option("--corrFactorZ",dest="corrFactorZ",type=str,help="add correction factor xsec",default=1.)
parser.add_option("-f","--fix",dest="fixPars",help="Fixed parameters",default="")


(options,args) = parser.parse_args()
samples={}

label = options.output.split(".root")[0]
t  = label.split("_")
el=""
for words in t:
    if words.find("HP")!=-1 or words.find("LP")!=-1:
        continue
    el+=words+"_"
label = el


for filename in os.listdir(args[0]):
    if not (filename.find(options.sample)!=-1):
        continue

    fnameParts=filename.split('.')
    fname=fnameParts[0]
    ext=fnameParts[1]
    if ext.find("root") ==-1:
        continue
    
    name = fname.split('_')[0]
    
    samples[name] = fname

    print 'found',filename

sigmas=[]
print samples
params={}
NRes = [0,0]
NnonRes= [0,0]
legs=["l1","l2"]
for leg in legs:
    plotters=[]
    for name in samples.keys():
        print leg
        print 'fitting resonant contribution: ' 
        print "append "+samples[name]
        plotters.append(TreePlotter(args[0]+'/'+samples[name]+'.root','tree'))
        plotters[-1].setupFromFile(args[0]+'/'+fname+'.pck')
        plotters[-1].addCorrectionFactor('xsec','tree')
        plotters[-1].addCorrectionFactor('genWeight','tree')
        plotters[-1].addCorrectionFactor('puWeight','tree')
        
    for p in plotters:
        corr = options.corrFactorW
        if name.find("Z")!=-1:
            corr = options.corrFactorZ
        sigmas.append(p.tree.GetMaximum("xsec")/p.weightinv)
        p.addCorrectionFactor(1.0/sigmas[-1]*float(corr),'flat')    
        
    plotter=MergedPlotter(plotters)        
    fitter=Fitter(['x'])
    fitter.jetResonanceVjets('model','x')

    if options.fixPars!="":
        fixedPars =options.fixPars.split(',')
        print fixedPars
        for par in fixedPars:
            parVal = par.split(':')
            fitter.w.var(parVal[0]).setVal(float(parVal[1]))
            fitter.w.var(parVal[0]).setConstant(1)

    histo = plotter.drawTH1("jj_"+leg+"_softDrop_mass",options.cut+"*(jj_"+leg+"_mergedVTruth==1)","1",80,options.mini,options.maxi)
    if leg.find("l1")!=-1:
        NRes[0] += histo.Integral()
    else:
        NRes[1] += histo.Integral()
    fitter.importBinnedData(histo,['x'],'data')
    fitter.fit('model','data',[ROOT.RooFit.SumW2Error(0)])
    fitter.fit('model','data',[ROOT.RooFit.SumW2Error(0),ROOT.RooFit.Minos(1)])
    fitter.projection("model","data","x","debugJ"+leg+"_"+options.output+"_Res.png")
    params[label+"_Res_"+leg]={"mean": {"val": fitter.w.var("mean").getVal(), "err": fitter.w.var("mean").getError()}, "sigma": {"val": fitter.w.var("sigma").getVal(), "err": fitter.w.var("sigma").getError()}, "alpha":{ "val": fitter.w.var("alpha").getVal(), "err": fitter.w.var("alpha")},"alpha2":{"val": fitter.w.var("alpha2").getVal(),"err": fitter.w.var("alpha2").getError()},"n":{ "val": fitter.w.var("n").getVal(), "err": fitter.w.var("n").getError()},"n2": {"val": fitter.w.var("n2").getVal(), "err": fitter.w.var("n2").getError()}}
     
    plotters=[] 
    for name in samples.keys(): 
        print 'calculate non-resonant contribution: ' 
        plotters.append(TreePlotter(args[0]+'/'+samples[name]+'.root','tree'))
        plotters[-1].setupFromFile(args[0]+'/'+fname+'.pck')
        plotters[-1].addCorrectionFactor('xsec','tree')
        plotters[-1].addCorrectionFactor('genWeight','tree')
        plotters[-1].addCorrectionFactor('puWeight','tree')
    
    for p in plotters:
        corr = options.corrFactorW
        if name.find("Z")!=-1:
            corr = options.corrFactorZ
        sigmas.append(p.tree.GetMaximum("xsec")/p.weightinv)
        p.addCorrectionFactor(1.0/sigmas[-1]*float(corr),'flat') 
            

    plotter=MergedPlotter(plotters)
    histo = plotter.drawTH1("jj_"+leg+"_softDrop_mass",options.cut+"*(jj_"+leg+"_mergedVTruth==0)","1",80,options.mini,options.maxi)
    if leg.find("l1")!=-1:
        NnonRes[0] += histo.Integral()
    else:
        NnonRes[1] += histo.Integral()
   
    
    
    
    
print 'fitting MVV: ' 
plotters=[]
for name in samples.keys():    
    plotters.append(TreePlotter(args[0]+'/'+samples[name]+'.root','tree') )
    plotters[-1].setupFromFile(args[0]+'/'+fname+'.pck')
    plotters[-1].addCorrectionFactor('xsec','tree')
    plotters[-1].addCorrectionFactor('genWeight','tree')
    plotters[-1].addCorrectionFactor('puWeight','tree')
for p in plotters:
    corr = options.corrFactorW
    if name.find("Z")!=-1:
        corr = options.corrFactorZ
    sigmas.append(p.tree.GetMaximum("xsec")/p.weightinv)
    p.addCorrectionFactor(1.0/sigmas[-1]*float(corr),'flat')    
   
plotter=MergedPlotter(plotters)        
fitter=Fitter(['MVV'])
fitter.qcd('model','MVV',True)

if options.fixPars!="":
    fixedPars =options.fixPars.split(',')
    for par in fixedPars:
        if par!="c_0" and par!="c_1" and par!="c_2":
            continue
        parVal = par.split(':')
        fitter.w.var(parVal[0]).setVal(float(parVal[1]))
        fitter.w.var(parVal[0]).setConstant(1)

histo = plotter.drawTH1("jj_LV_mass",options.cut+"*(jj_"+leg+"_mergedVTruth==1)","1",36,1000,5000)
c = ROOT.TCanvas("c",'C',400,400)
histo.Draw("hist")
c.SaveAs("test.pdf")
fitter.importBinnedData(histo,['MVV'],'data')
fitter.fit('model','data',[ROOT.RooFit.SumW2Error(0)])
fitter.fit('model','data',[ROOT.RooFit.SumW2Error(0),ROOT.RooFit.Minos(1)])
fitter.projection("model","data",'MVV',"debugMVV_"+options.output+".png")
params[label+"_MVV"]={"p0": {"val":fitter.w.var("c_0").getVal(), "err":fitter.w.var("c_0").getError() }, "p1":{ "val": fitter.w.var("c_1").getVal(), "err": fitter.w.var("c_1").getError()}, "p2":{ "val":  fitter.w.var("c_2").getVal(), "err": fitter.w.var("c_2").getError()}}
    
  
  
        
if options.store!="":
    f=open(options.store,"w")
    for par in params:
        f.write(str(par)+ " = " +str(params[par])+"\n")
    print NRes
    print NnonRes
    f.write(label+"_ratio_l1 = "+str(NRes[0]/(NRes[0]+NnonRes[0]))+"\n")
    f.write(label+"_ratio_l2 = "+str(NRes[1]/(NRes[1]+NnonRes[1]))+"\n")
