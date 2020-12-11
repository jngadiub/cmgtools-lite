#!/usr/bin/env python
import ROOT
from array import array
from CMGTools.VVResonances.statistics.Fitter import Fitter
from math import log,exp,sqrt
import os, sys, re, optparse,pickle,shutil,json
import copy
import json
from CMGTools.VVResonances.plotting.tdrstyle import *
setTDRStyle()
from CMGTools.VVResonances.plotting.TreePlotter import TreePlotter
from CMGTools.VVResonances.plotting.MergedPlotter import MergedPlotter
sys.path.insert(0, "../interactive/")
import cuts
ROOT.gSystem.Load("libCMGToolsVVResonances")
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptFit(0)
ROOT.v5.TFormula.SetMaxima(10000) #otherwise we get an error that the TFormula called by the TTree draw has too many operators when running on the CR

parser = optparse.OptionParser()
parser.add_option("-o","--output",dest="output",help="Output",default='')
parser.add_option("-p","--period",dest="period",help="run period",default=2016)
parser.add_option("-r","--res",dest="res",help="res",default='')
parser.add_option("-H","--resHisto",dest="resHisto",help="res",default='')
parser.add_option("-s","--samples",dest="samples",default='',help="Type of sample")
parser.add_option("-c","--cut",dest="cut",help="Cut to apply for yield in gen sample",default='')
parser.add_option("-v","--var",dest="var",help="variable for x",default='')
parser.add_option("-b","--bins",dest="binsx",type=int,help="bins",default=1)
parser.add_option("-x","--minx",dest="minx",type=float,help="bins",default=0)
parser.add_option("-X","--maxx",dest="maxx",type=float,help="conditional bins split by comma",default=1)
parser.add_option("-w","--weights",dest="weights",help="additional weights",default='')
parser.add_option("-u","--usegenmass",dest="usegenmass",action="store_true",help="use gen mass for det resolution",default=False)
parser.add_option("-e","--firstEv",dest="firstEv",type=int,help="first event",default=0)
parser.add_option("-E","--lastEv",dest="lastEv",type=int,help="last event",default=-1)
parser.add_option("--binsMVV",dest="binsMVV",help="use special binning",default="")
parser.add_option("-t","--triggerweight",dest="triggerW",action="store_true",help="Use trigger weights",default=False)
parser.add_option("--corrFactorW",dest="corrFactorW",type=float,help="add correction factor xsec",default=1.)
parser.add_option("--corrFactorZ",dest="corrFactorZ",type=float,help="add correction factor xsec",default=1.)

(options,args) = parser.parse_args()

tmplabel = options.output.split("_")[2]
if options.output.find("/")!=-1: tmplabel = (options.output.split("/")[1]).split("_")[2]
print " tmplabel ",tmplabel
ttlabel = tmplabel.replace("TTJets","")
print " ttlabel ",ttlabel

if options.output.find('VV_HPLP')!=-1: purity='VV_HPLP'
if options.output.find('VV_HPHP')!=-1: purity='VV_HPHP'
if options.output.find('VH_HPLP')!=-1: purity='VH_HPLP'
if options.output.find('VH_HPHP')!=-1: purity='VH_HPHP'
if options.output.find('VH_LPHP')!=-1: purity='VH_LPHP'
if options.output.find('NP')!=-1: purity='NP'
print "purity ",purity
def getBinning(binsMVV,minx,maxx,bins):
    l=[]
    if binsMVV=="":
        for i in range(0,bins+1):
            l.append(minx + i* (maxx - minx)/bins)
    else:
        s = binsMVV.split(",")
        for w in s:
            l.append(int(w))
    return l


def unequalScale(histo,name,alpha,power=1):
    newHistoU =copy.deepcopy(histo) 
    newHistoU.SetName(name+"Up")
    newHistoD =copy.deepcopy(histo) 
    newHistoD.SetName(name+"Down")
    for i in range(1,histo.GetNbinsX()+1):
        x= histo.GetXaxis().GetBinCenter(i)
        nominal=histo.GetBinContent(i)
        factor = 1+alpha*pow(x,power) 
        newHistoU.SetBinContent(i,nominal*factor)
        newHistoD.SetBinContent(i,nominal/factor)
    return newHistoU,newHistoD 
    
def mirror(histo,histoNominal,name):
    newHisto =copy.deepcopy(histoNominal) 
    newHisto.SetName(name)
    intNominal=histoNominal.Integral()
    intUp = histo.Integral()
    for i in range(1,histo.GetNbinsX()+1):
        up=histo.GetBinContent(i)/intUp
        nominal=histoNominal.GetBinContent(i)/intNominal
        newHisto.SetBinContent(i,histoNominal.GetBinContent(i)*nominal/up)
    return newHisto      

  
def smoothTail1D(proj,smooth=3000):
    if proj.Integral() == 0:
        print "histogram has zero integral "+proj.GetName()
        return 0
    scale = proj.Integral()
    proj.Scale(1.0/scale)
    
    
    beginFitX = 2100#1500
    if smooth < 2600 : beginFitX = 1200
    endX = smooth #2800
    #if options.output.find("HPHP")!=-1: 
        #beginFitX=1100
        #endX = 1500
    expo=ROOT.TF1("expo","[0]*(1-x/13000.)^[1]/(x/13000)^[2]",2000,8000)
    expo.SetParameters(0,16.,2.)
    expo.SetParLimits(2,1.,20.)
    proj.Fit(expo,"LLMR","",beginFitX,8000)
    beginsmooth = False
    print proj.GetNbinsX()+1
    for j in range(1,proj.GetNbinsX()+1):
        x=proj.GetXaxis().GetBinCenter(j)
        if x>beginFitX:
            if beginsmooth==False:
                if x< endX: #2100: 
                   if abs(proj.GetBinContent(j) - expo.Eval(x)) < 0.00009:# and abs(expo.Derivative(x)- (hist.GetBinContent(j):
                    print beginFitX
                    print "begin smoothing at " +str(x)
                    beginsmooth = True 
               #if abs(proj.GetBinContent(j) - expo.Eval(x)) < 0.00001:# and abs(expo.Derivative(x)- (hist.GetBinContent(j):
                   #print beginFitX
                   #print "begin smoothing at " +str(x)

                   #beginsmooth = True 
                else: beginsmooth = True
            if beginsmooth:
                proj.SetBinContent(j,expo.Eval(x))
    proj.Scale(scale)
    return 1

weights_ = options.weights.split(',')

random=ROOT.TRandom3(101082)

sampleTypes=options.samples.split(',')
#period = "2016"
#if options.samples.find("HT800")!=-1:
#    period = "2017"
period=options.period

stack = ROOT.THStack("stack","")
print "Creating datasets for samples: " ,sampleTypes
dataPlotters=[]
dataPlottersNW=[]

#folders=[]
print "args[0] ",args[0]
folder = args[0] #.split(',')
print "folder ",folder
print "split ",folder.split("/")
year=folder.split("/")[-2]
print "year ",year
print "now working with cuts "
ctx = cuts.cuts("init_VV_VH.json",year,"dijetbins_random")
print "lumi for year "+year+" = ",ctx.lumi[year]
luminosity = ctx.lumi[year]/ctx.lumi["Run2"]
#smoothstart=ctx.tt_smooth
smoothstart={ "" : { "NP": 3000., "VV_HPHP": 3000. , "VV_HPLP": 1800., "VH_HPHP": 3000., "VH_HPLP": 2000., "VH_LPHP": 3000. },
              "resT" : { "NP": 3000., "VV_HPHP": 3000. , "VV_HPLP": 1800., "VH_HPHP": 3000., "VH_HPLP": 2000., "VH_LPHP": 3000. },
              "resW": { "NP": 1800., "VV_HPHP": 1800. , "VV_HPLP": 1400., "VH_HPHP": 1400., "VH_HPLP": 1400., "VH_LPHP": 1200. },
              "resTnonresT": { "NP": 3000., "VV_HPHP": 1600. , "VV_HPLP": 1600., "VH_HPHP": 3000., "VH_HPLP": 3000., "VH_LPHP": 2200. },
              "resWnonresT": { "NP": 2000., "VV_HPHP": 1600. , "VV_HPLP": 1600., "VH_HPHP": 1800., "VH_HPLP": 2000., "VH_LPHP": 1800. },
              "resTresW" : { "NP": 3000., "VV_HPHP": 1800. , "VV_HPLP": 1800., "VH_HPHP": 1800., "VH_HPLP": 2800., "VH_LPHP": 2200. },
              "nonresT" : { "NP": 3000., "VV_HPHP": 1400. , "VV_HPLP": 1800., "VH_HPHP": 2000., "VH_HPLP": 1800., "VH_LPHP": 2000. }}

print "smooth start",smoothstart 
if options.output.find("Run2") ==-1: luminosity = 1
for filename in os.listdir(folder):
    for sampleType in sampleTypes:
        if filename.find(sampleType)!=-1:
            fnameParts=filename.split('.')
            fname=fnameParts[0]
            ext=fnameParts[1]
            if ext.find("root") ==-1: continue
            dataPlotters.append(TreePlotter(folder+'/'+fname+'.root','AnalysisTree'))
            dataPlotters[-1].setupFromFile(folder+'/'+fname+'.pck')
            dataPlotters[-1].addCorrectionFactor('xsec','tree')
            dataPlotters[-1].addCorrectionFactor('genWeight','tree')
            dataPlotters[-1].addCorrectionFactor('puWeight','tree')
            dataPlotters[-1].addCorrectionFactor(luminosity,'flat')
            if options.triggerW:
                dataPlotters[-1].addCorrectionFactor('triggerWeight','tree')
                print "Using trigger weights from tree"
            for w in weights_:
                if w != '': dataPlotters[-1].addCorrectionFactor(w,'branch')
            corrFactor = 1
            dataPlotters[-1].addCorrectionFactor(corrFactor,'flat') 
            if filename.find("TT")!=-1:
                #we consider ttbar with reweight applyied as nominal!
                dataPlotters[-1].addCorrectionFactor('TopPTWeight','tree')
            dataPlotters[-1].filename=fname

            dataPlottersNW.append(TreePlotter(folder+'/'+fname+'.root','AnalysisTree'))
            dataPlottersNW[-1].addCorrectionFactor('puWeight','tree')
            dataPlottersNW[-1].addCorrectionFactor('genWeight','tree')
            dataPlottersNW[-1].addCorrectionFactor(corrFactor,'flat')
            for w in weights_: 
                if w != '': dataPlottersNW[-1].addCorrectionFactor(w,'branch')
            if options.triggerW: dataPlottersNW[-1].addCorrectionFactor('triggerWeight','tree')
            dataPlottersNW[-1].addCorrectionFactor(corrFactor,'flat')
            dataPlottersNW[-1].addCorrectionFactor(luminosity,'flat') 
            dataPlottersNW[-1].filename=fname


data=MergedPlotter(dataPlotters)
fcorr=ROOT.TFile(options.res)

scale = fcorr.Get("scale"+options.resHisto+"Histo")
res   = fcorr.Get("res"  +options.resHisto+"Histo")

binning = getBinning(options.binsMVV,options.minx,options.maxx,options.binsx)
print binning



histogram_nominal = ROOT.TH1F("histo_nominal","histo_nominal",options.binsx,array('f',binning))
histogram_nominal.Sumw2()
histogram_noreweight = ROOT.TH1F("histo_noreweight","histo_noreweight",options.binsx,array('f',binning))
histogram_noreweight.Sumw2()

mvv_nominal = ROOT.TH1F("mvv_nominal","mvv_nominal",options.binsx,array('f',binning))
mvv_nominal.Sumw2()

maxEvents = -1
#ok lets populate!
for plotter,plotterNW in zip(dataPlotters,dataPlottersNW):
 '''
 if plotter.filename.find("Jets") != -1 or plotter.filename.find("TT") !=-1:
   print "Preparing nominal histogram for "
   print "filename: ", plotter.filename, " preparing central values histo"
   histI2=plotter.drawTH1Binned('jj_LV_mass',options.cut,"1",array('f',binning))
   canv = ROOT.TCanvas("c1","c1",800,600)
   dataset=plotterNW.makeDataSet('jj_gen_partialMass,jj_l1_gen_pt,jj_l1_gen_softDrop_mass',options.cut,options.firstEv,options.lastEv)

   histTMP=ROOT.TH1F("histoTMP","histo",options.binsx,array('f',binning))
   if not(options.usegenmass):
    datamaker=ROOT.cmg.GaussianSumTemplateMaker1D(dataset,options.var,'jj_l1_gen_pt',scale,res,histTMP)
   else: datamaker=ROOT.cmg.GaussianSumTemplateMaker1D(dataset,options.var,'jj_l1_gen_softDrop_mass',scale,res,histTMP)

   if histTMP.Integral()>0:
    histTMP.Scale(histI2.Integral()/histTMP.Integral())
    histogram_nominal.Add(histTMP)
    mvv_nominal.Add(histI2)

   histI2.Delete()
   histTMP.Delete()
 '''


 #Nominal histogram Pythia8
 c=0
 if plotter.filename.find(sampleTypes[0].replace('.root','')) != -1 : #and plotter.filename.find("Jets") == -1 and plotter.filename.find("TT") ==-1: 
   print "Preparing histograms for sampletype " ,sampleTypes[0]
   print "filename: ", plotter.filename
   histI2=plotter.drawTH1Binned('jj_LV_mass',options.cut,"1",array('f',binning))
   histI2nw=plotterNW.drawTH1Binned('jj_LV_mass',options.cut,"1",array('f',binning))
   canv = ROOT.TCanvas("c1","c1",800,600)
   dataset=plotter.makeDataSet('jj_gen_partialMass,jj_l1_gen_pt,jj_l1_gen_softDrop_mass',options.cut,options.firstEv,options.lastEv)
   datasetNW=plotterNW.makeDataSet('jj_gen_partialMass,jj_l1_gen_pt,jj_l1_gen_softDrop_mass',options.cut,options.firstEv,options.lastEv)

   histTMP=ROOT.TH1F("histoTMP","histo",options.binsx,array('f',binning))
   histTMPnw=ROOT.TH1F("histoTMPnw","histo",options.binsx,array('f',binning))
   if not(options.usegenmass):
    datamaker=ROOT.cmg.GaussianSumTemplateMaker1D(dataset,options.var,'jj_l1_gen_pt',scale,res,histTMP)
    datamaker2=ROOT.cmg.GaussianSumTemplateMaker1D(datasetNW,options.var,'jj_l1_gen_pt',scale,res,histTMPnw)
   else: 
       datamaker=ROOT.cmg.GaussianSumTemplateMaker1D(dataset,options.var,'jj_l1_gen_softDrop_mass',scale,res,histTMP)
       datamaker2=ROOT.cmg.GaussianSumTemplateMaker1D(datasetNW,options.var,'jj_l1_gen_softDrop_mass',scale,res,histTMPnw)

   if histTMP.Integral()>0:
    histTMP.Scale(histI2.Integral()/histTMP.Integral())
    histogram_nominal.Add(histTMP)
    mvv_nominal.Add(histI2)
   if histTMPnw.Integral()>0:
    histTMPnw.Scale(histI2nw.Integral()/histTMPnw.Integral())
    histogram_noreweight.Add(histTMPnw)


   histI2.Delete()
   histTMP.Delete()
   histI2nw.Delete()
   histTMPnw.Delete()


 if len(sampleTypes)<2: continue
 elif plotter.filename.find(sampleTypes[1].replace('.root','')) != -1 : #and plotter.filename.find("Jets") == -1 and plotter.filename.find("TT") ==-1: #alternative shape Herwig
   print "Preparing histograms for sampletype " ,sampleTypes[1]
   print "filename: ", plotter.filename
   histI2=plotter.drawTH1Binned('jj_LV_mass',options.cut,"1",array('f',binning))
   histI2nw=plotterNW.drawTH1Binned('jj_LV_mass',options.cut,"1",array('f',binning))
   canv = ROOT.TCanvas("c1","c1",800,600)
   dataset=plotter.makeDataSet('jj_gen_partialMass,jj_l1_gen_pt,jj_l1_gen_softDrop_mass',options.cut,options.firstEv,options.lastEv)
   datasetNW=plotterNW.makeDataSet('jj_gen_partialMass,jj_l1_gen_pt,jj_l1_gen_softDrop_mass',options.cut,options.firstEv,options.lastEv)

   histTMP=ROOT.TH1F("histoTMP","histo",options.binsx,array('f',binning))
   histTMPnw=ROOT.TH1F("histoTMPnw","histo",options.binsx,array('f',binning))
   if not(options.usegenmass):
    datamaker=ROOT.cmg.GaussianSumTemplateMaker1D(dataset,options.var,'jj_l1_gen_pt',scale,res,histTMP)
    datamaker2=ROOT.cmg.GaussianSumTemplateMaker1D(datasetNW,options.var,'jj_l1_gen_pt',scale,res,histTMPnw)
   else:
       datamaker=ROOT.cmg.GaussianSumTemplateMaker1D(dataset,options.var,'jj_l1_gen_softDrop_mass',scale,res,histTMP)
       datamaker2=ROOT.cmg.GaussianSumTemplateMaker1D(datasetNW,options.var,'jj_l1_gen_softDrop_mass',scale,res,histTMPnw)

   if histTMP.Integral()>0:
    histTMP.Scale(histI2.Integral()/histTMP.Integral())
    histogram_nominal.Add(histTMP)
    mvv_nominal.Add(histI2)
   if histTMPnw.Integral()>0:
    histTMPnw.Scale(histI2nw.Integral()/histTMPnw.Integral())
    histogram_noreweight.Add(histTMPnw)

   histI2.Delete()
   histTMP.Delete()
   histI2nw.Delete()
   histTMPnw.Delete()



 if len(sampleTypes)<3: continue
 elif plotter.filename.find(sampleTypes[2].replace('.root','')) != -1 : #and plotter.filename.find("Jets") == -1 and plotter.filename.find("TT") ==-1: #alternative shape Pythia8+Madgraph (not used for syst but only for cross checks)
   print "Preparing histogram for sampletype " ,sampleTypes[2]
   print "filename: ", plotter.filename
   histI2=plotter.drawTH1Binned('jj_LV_mass',options.cut,"1",array('f',binning))
   histI2nw=plotterNW.drawTH1Binned('jj_LV_mass',options.cut,"1",array('f',binning))
   canv = ROOT.TCanvas("c1","c1",800,600)
   dataset=plotter.makeDataSet('jj_gen_partialMass,jj_l1_gen_pt,jj_l1_gen_softDrop_mass',options.cut,options.firstEv,options.lastEv)
   datasetNW=plotterNW.makeDataSet('jj_gen_partialMass,jj_l1_gen_pt,jj_l1_gen_softDrop_mass',options.cut,options.firstEv,options.lastEv)

   histTMP=ROOT.TH1F("histoTMP","histo",options.binsx,array('f',binning))
   histTMPnw=ROOT.TH1F("histoTMPnw","histo",options.binsx,array('f',binning))
   if not(options.usegenmass):
    datamaker=ROOT.cmg.GaussianSumTemplateMaker1D(dataset,options.var,'jj_l1_gen_pt',scale,res,histTMP)
    datamaker2=ROOT.cmg.GaussianSumTemplateMaker1D(datasetNW,options.var,'jj_l1_gen_pt',scale,res,histTMPnw)
   else:
       datamaker=ROOT.cmg.GaussianSumTemplateMaker1D(dataset,options.var,'jj_l1_gen_softDrop_mass',scale,res,histTMP)
       datamaker2=ROOT.cmg.GaussianSumTemplateMaker1D(datasetNW,options.var,'jj_l1_gen_softDrop_mass',scale,res,histTMPnw)

   if histTMP.Integral()>0:
    histTMP.Scale(histI2.Integral()/histTMP.Integral())
    histogram_nominal.Add(histTMP)
    mvv_nominal.Add(histI2)
   if histTMPnw.Integral()>0:
    histTMPnw.Scale(histI2nw.Integral()/histTMPnw.Integral())
    histogram_noreweight.Add(histTMPnw)

   histI2.Delete()
   histTMP.Delete()
   histI2nw.Delete()
   histTMPnw.Delete()


print " ********** ALL DONE, now save in output file ", options.output
f=ROOT.TFile(options.output,"RECREATE")
f.cd()
scale = histogram_nominal.Integral()
scale2 = mvv_nominal.Integral()
finalHistograms={histogram_nominal.GetName(): histogram_nominal,
                 histogram_noreweight.GetName(): histogram_noreweight,
                 mvv_nominal.GetName(): mvv_nominal
}
print ttlabel
print purity
smooth = smoothstart[ttlabel][purity]
print " smooth ",smooth
for hist in finalHistograms.itervalues():
 # hist.Write(hist.GetName()+"_raw")
 if (options.output).find("Jets")!=-1 and hist.GetName().find("hist")!=-1:
     print "smooth tails of 1D histogram for vjets background of histo "+hist.GetName()
     if hist.Integral() > 0:
        smoothTail1D(hist,smooth)
        if hist.GetName().find("hist_nominal")!=-1:
            hist.Scale(scale)
        #if hist.GetName().find("mvv_nominal")!=-1:
        #    hist.Scale(scale2)

 hist.Write(hist.GetName())
 finalHistograms[hist.GetName()]=hist

#################################
if histogram_nominal.Integral()!=0 and histogram_noreweight.Integral()!=0: 
    c = ROOT.TCanvas("c","C",600,400)
    c.SetRightMargin(0.11)
    c.SetLeftMargin(0.11)
    c.SetTopMargin(0.11)
    finalHistograms["histo_nominal"].SetLineColor(ROOT.kBlue)
    #finalHistograms["histo_nominal"].Scale(scale)
    finalHistograms["histo_nominal"].GetYaxis().SetTitle("arbitrary scale")
    finalHistograms["histo_nominal"].GetYaxis().SetTitleOffset(1.5)
    finalHistograms["histo_nominal"].GetXaxis().SetTitle("dijet mass")
    finalHistograms["histo_nominal"].SetMinimum(0.0000000000001)
    sf = finalHistograms["histo_nominal"].Integral()
    histogram_noreweight     .Scale(sf/histogram_noreweight.Integral())
    finalHistograms["histo_nominal"].Draw("hist")
    histogram_noreweight.SetLineColor(ROOT.kRed)
    histogram_noreweight.SetLineWidth(2)
    histogram_noreweight.Draw("histsame")
    text = ROOT.TLatex()
    text.DrawLatexNDC(0.13,0.92,"#font[62]{CMS} #font[52]{Simulation}")
    data = finalHistograms["mvv_nominal"]
    data.Scale(sf/data.Integral())
    data.SetMarkerColor(ROOT.kBlack)
    data.SetMarkerStyle(7)
    data.Draw("same")
    c.SetLogy()


    l = ROOT.TLegend(0.17,0.2,0.6,0.33)
    l.AddEntry(data,"simulation","lp")
    l.AddEntry(finalHistograms["histo_nominal"],"template","l")
    l.AddEntry(histogram_noreweight,"no pt reweigh","l")
    l.Draw("same")

    

    #if options.output.find("/")!=-1: tmplabel = (options.output.split("/")[1]).split("_")[2]
    label=options.output.split("_")[1]
    print "label ",label
    tmplabel += label+"_"+purity
    c.SaveAs("debug_mVV_kernels_"+tmplabel+".pdf")
    print "for debugging save","debug_mVV_kernels_"+tmplabel+".pdf"

    ########################################################


f.Close()



