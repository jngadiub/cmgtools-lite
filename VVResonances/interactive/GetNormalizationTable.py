#!/usr/bin/env python                                                                                                                                                                   
import ROOT
from array import array
import os, sys, re, optparse,pickle,shutil,json, copy
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
ROOT.v5.TFormula.SetMaxima(10000) #otherwise we get an error that the TFormula called by the TTree draw has too many operators when running on the CR
from  CMGTools.VVResonances.plotting.CMS_lumi import *
#sys.path.insert(0, "../interactive/")
import cuts

parser = optparse.OptionParser()
parser.add_option("-o","--output",dest="output",help="outname",default='')
parser.add_option("-i","--inputdir",dest="inputdir",help="directory where the input files are stored",default="results_Run2")
parser.add_option("-p","--period",dest="period",help="2016 or 2017 or 2016,2017,2018",default="2016,2017,2018")
parser.add_option("-c","--categories",dest="categories",help="VV_HPHP etc",default="VH_HPHP,VV_HPHP,VH_LPHP,VH_HPLP,VV_HPLP")
parser.add_option("-v","--vbf",dest="vbf",help="make vbf?",default=False)

(options,args) = parser.parse_args()

def loadJson(inputdir,category,filename,period):
    jsonname=inputdir+"/"+filename+"_"+period+"_"+category+".json" 
    with open(jsonname) as jsonFile:
        print " opened json file ",jsonname
        j = json.load(jsonFile)
    print j
    return j


def tablePreambole(txtfile,caption):
    txtfile.write("\\begin{table}[b]\n")
    txtfile.write("\\topcaption{%s yield and background yields extracted from the background-only fit together with post-fit uncertainties.}\n" %caption)
    txtfile.write("\centering\n")
    txtfile.write("\\begin{tabular}{lccccccc}\n")
    txtfile.write("\hline\n")
    txtfile.write("Background  & QCD & \PW{}+jets & \PZ{}+jets & \\ttbar{} & other & Total & Data\\\\ \n")
    txtfile.write("\hline\n")

def tableClosing(txtfile,caption):
    txtfile.write("\hline\n")
    txtfile.write("\end{tabular}\n")
    txtfile.write("\label{tab:ObsEvents}\n")
    txtfile.write("\end{table}\n")



if __name__ == "__main__":
    contrib =["resT","resW","nonresT","resTnonresT","resWnonresT","resTresW"]
    mappdf = {"resT":"TTJetsTop","resW":"TTJetsW","nonresT":"TTJetsNonRes","resTnonresT":"TTJetsTNonResT","resWnonresT":"TTJetsWNonResT","resTresW":"TTJetsResWResT"}
    bkg = ["nonRes","TTJets","Wjets","Zjets"]
    eventstype=["Expected","Observed"]
    if options.period.find(",")!=-1 and len(options.period.split(",")) == 3: 
        year = "Run2"
    else: year = options.period


    category = options.categories.split(",")
    print category

    events = {}
    for evt in eventstype:
        print " processing ",evt
        events[evt] = {}
        text_file = open(evt+"_"+year+options.output+".txt", "w")
        tablePreambole(text_file,evt)
 

        exp = {}
        for c in category:
            print " cat ",c
            exp[c] = loadJson(options.inputdir,c,evt,year)
            print " non res ",exp[c]["nonRes"]
            if options.vbf == True:
                vbfc="VBF_"+c
                exp[vbfc] = loadJson(options.inputdir,vbfc,evt,year)
                totalTT=0
                for con in contrib:
                    if evt == "Expected":
                        totalTT=totalTT+int(round(exp[vbfc][mappdf[con]]))
                    else:
                        totalTT=totalTT+int(round(exp[vbfc][con]))
                exp[vbfc]["TTJets"]=totalTT
                total = 0
                for b in bkg:
                    total=total+int(round(exp[vbfc][b]))
                text_file.write(" %s %s %s & %.0f & %.0f & %.0f & %.0f & %.0f & %.0f & %.0f \\\\ \n"%(vbfc.split("_")[1],vbfc.split("_")[2],vbfc.split("_")[3],exp[vbfc]["nonRes"],exp[vbfc]["Wjets"],exp[vbfc]["Zjets"],totalTT,0,total,exp[vbfc]["data"]))
                text_file.write("\hline\n")
                # end of VBF part

            totalTT=0
            for con in contrib:
                if evt == "Expected":
                    totalTT=totalTT+int(round(exp[c][mappdf[con]]))
                else:
                    totalTT=totalTT+int(round(exp[c][con]))
                exp[c]["TTJets"]=totalTT
            total =0
            for b in bkg:
                total=total+int(round(exp[c][b]))
            text_file.write(" %s %s %s & %.0f & %.0f & %.0f & %.0f & %.0f & %.0f & %.0f \\\\ \n"%(c.split("_")[0],c.split("_")[1],"DY/gg",exp[c]["nonRes"],exp[c]["Wjets"],exp[c]["Zjets"],totalTT,0,total,exp[c]["data"]))
        tableClosing(text_file,evt)
        text_file.close()

