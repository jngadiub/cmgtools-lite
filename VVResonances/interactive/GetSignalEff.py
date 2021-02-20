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
parser.add_option("-o","--output",dest="output",help="outname",default='_test')
parser.add_option("-i","--inputdir",dest="inputdir",help="directory where the input files are stored",default="results_Run2")
parser.add_option("-p","--period",dest="period",help="2016 or 2017 or 2016,2017,2018",default="2016,2017,2018")
parser.add_option("-c","--categories",dest="categories",help="VV_HPHP etc",default="VH_HPHP,VV_HPHP,VH_LPHP,VH_HPLP,VV_HPLP")
parser.add_option("-v","--vbf",dest="vbf",action="store_true",help="make vbf?",default=False)

(options,args) = parser.parse_args()

def getEff(inputdir,category,signal,period,mass):
    rootname=inputdir+"/JJ_"+signal+"_"+period+"_"+category+"_yield.root" 
    r_file = ROOT.TFile(rootname,"READ")
    gr = r_file.Get("yield")
    ff = gr.GetFunction("func")
    eff = ff.Eval(mass)*1000.
    print "eff ",eff
    return eff


def tablePreambole(txtfile,m):
    txtfile.write("\\begin{tabular}{lcccccccccc}\n")
    txtfile.write("\hline\n")
    txtfile.write("Category & $\MJOT$ & $\MJTO$ tagging & \multicolumn{6}{c}{Signal efficiency at $m= %d \TeV$\\\\ \n"%m)
    txtfile.write("&  & \multicolumn{2}{c}{$\Radion$}  & \multicolumn{2}{c}{$\PWpr$} & \multicolumn{2}{c}{$\PZpr$} & \multicolumn{2}{c}{$\BulkG$}\\\\ \n")
    txtfile.write("&  & $\PW{}\PW{}$ & $\PZ{}\PZ{}$ & $\PW{}\PZ{}$ & $\PW{}\PH{}$ & $\PW{}\PW{}$ & $\PZ{}\PH{}$ & $\PW{}\PW{}$ & $\PZ{}\PZ{}$\\\\ \n")
    txtfile.write("\hline\n")

def tableClosing(txtfile,caption):
    txtfile.write("\hline\n")
    txtfile.write("\end{tabular}\n")

if __name__ == "__main__":
    signals = ["RadionWW","RadionZZ","WprimeWZ","WprimeWH","ZprimeWW","ZprimeZH","BulkGWW","BulkGZZ"]
    name = options.output
    if options.period.find(",")!=-1 and len(options.period.split(",")) == 3: 
        year = "Run2"
    else: year = options.period
    catdef = {"VH_HPHP":"10\% \DeepWZqq{} & 2\% \DeepZHbb{}",
              "VH_HPHPbis":"2\% \DeepZHbb{} & 2\% \DeepZHbb{}",
              "VV_HPHP":"10\% \DeepWZqq{} & 10\% \DeepWZqq{}",
              "VH_LPHP":"20\% \DeepWZqq{} & 2\% \DeepZHbb{}",
              "VH_LPHPbis":"10\% \DeepZHbb{} & 2\% \DeepZHbb{}",
              "VH_HPLP":"10\% \DeepWZqq{} & 10\% \DeepZHbb{}",
              "VV_HPLP":"10\% \DeepWZqq{} & 20\% \DeepWZqq{}"}

    category = options.categories.split(",")
    print category

    mass = 4000.
    masstable = str(mass/1000.)
    text_file = open("SignalEfficiency_"+year+options.output+".txt", "w")
    tablePreambole(text_file,mass)
 
    #    txtfile.write("&  & \multicolumn{2}{c}{$\Radion$}  & \multicolumn{2}{c}{$\PWpr$} & \multicolumn{2}{c}{$\PZpr$} & \multicolumn{2}{c}{$\BulkG$}\\\\ \n")
    #    txtfile.write("&  & $\PW{}\PW{}$ & $\PZ{}\PZ{}$ & $\PW{}\PZ{}$ & $\PW{}\PH{}$ & $\PW{}\PW{}$ & $\PZ{}\PH{}$ & $\PW{}\PW{}$ & $\PZ{}\PZ{}$\\\\ \n")
    
    #    VH HPHP DY/gg & 10\% \DeepWZqq{} + 2\% \DeepZHbb{} & \% & \% & \% & \% & \% & \% & \% & \% \\
    #    VV HPHP DY/gg & 10\% \DeepWZqq{} + 10\% \DeepWZqq{} & \% & \% & \% & \% & \% & \% & \% & \% \\
    #    VH LPHP DY/gg & 20\% \DeepWZqq{} + 2\% \DeepZHbb{} & \% & \% & \% & \% & \% & \% & \% & \% \\
    #    VH HPLP DY/gg & 10\% \DeepWZqq{} + 10\% \DeepZHbb{} & \% & \% & \% & \% & \% & \% & \% & \% \\
    #    VV HPLP DY/gg & 10\% \DeepWZqq{} + 20\% \DeepWZqq{} & \% & \% & \% & \% & \% & \% & \% & \% \\

    production = ["gg/DY"]
    if options.vbf == True:
        production = ["VBF","gg/DY"]

    eff = {}
    for prod in production:
        print " production ",prod
        for c in category:
            print " cat ",c
            eff[c]={}
            if prod == "VBF":
                string=c.split("_")[0]+" "+c.split("_")[1]+" VBF & "+catdef[c]
                if c == "VH_HPHP" or c == "VH_LPHP": 
                    string = "\multirow{2}{*}{{"+c.split("_")[0]+" "+c.split("_")[1]+" VBF}}& "+catdef[c]
                    empty = " & "+catdef[c+"bis"]
                for sig in signals:
                    vbfsig = "VBF_"+sig
                    eff[c][vbfsig] = getEff(options.inputdir,c,vbfsig,year,mass)
                    if c == "VH_HPHP" or c == "VH_LPHP":
                        string=string+" &\multirow{2}{*}{{ %0.3f}} "%eff[c][vbfsig]
                        empty = empty+" & "
                    else:
                        string=string+" & %0.3f "%eff[c][vbfsig]
                string=string+"\\\\ \n"
                print " vbfstring ",string
                if c == "VH_HPHP" or c == "VH_LPHP": empty=empty+"\\\\ \n"
            else:
                string=c.split("_")[0]+" "+c.split("_")[1]+" DY/gg & "+catdef[c]
                if c == "VH_HPHP" or c == "VH_LPHP": 
                    empty = " & "+catdef[c+"bis"]
                    string = "\multirow{2}{*}{{"+c.split("_")[0]+" "+c.split("_")[1]+" DY/gg}}& "+catdef[c]
                for sig in signals:
                    print "signal ",sig
                    eff[c][sig] = getEff(options.inputdir,c,sig,year,mass)
                    if c == "VH_HPHP" or c == "VH_LPHP":  
                        string=string+"& \multirow{2}{*}{{ %0.3f }}"%eff[c][sig]
                        empty = empty+" & "
                    else:
                        string=string+" & %0.3f "%eff[c][sig]
                string=string+"\\\\ \n"
                if c == "VH_HPHP" or c == "VH_LPHP": empty=empty+"\\\\ \n"
                print "ggstring ",string



            text_file.write(string)
            if c == "VH_HPHP" or c == "VH_LPHP": text_file.write(empty)
        #text_file.write("\hline\n")

    tableClosing(text_file,name)
    text_file.close()

