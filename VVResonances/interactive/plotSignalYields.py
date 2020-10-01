#!/bin/env python
import ROOT
import json
import math
ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")
from time import sleep
import optparse, sys
from  CMGTools.VVResonances.plotting.CMS_lumi import *

# ROOT.gROOT.SetBatch(True)

path = "../plots/"

def getLegend(x1=0.70010112,y1=0.693362,x2=0.90202143,y2=0.829833):
  legend = ROOT.TLegend(x1,y1,x2,y2)
  legend.SetTextSize(0.032)
  legend.SetLineColor(0)
  legend.SetShadowColor(0)
  legend.SetLineStyle(1)
  legend.SetLineWidth(1)
  legend.SetFillColor(0)
  legend.SetFillStyle(0)
  legend.SetMargin(0.35)
  return legend
  
def getCanvasPaper(cname):
        ROOT.gStyle.SetOptStat(0)

        H_ref = 600
        W_ref = 600
        W = W_ref
        H  = H_ref
        iPeriod = 0
        # references for T, B, L, R
        T = 0.08*H_ref
        B = 0.15*H_ref
        L = 0.15*W_ref
        R = 0.04*W_ref
        canvas = ROOT.TCanvas(cname,cname,50,50,W,H)
        canvas.SetFillColor(0)
        canvas.SetBorderMode(0)
        canvas.SetFrameFillStyle(0)
        canvas.SetFrameBorderMode(0)
        canvas.SetLeftMargin( L/W )
        canvas.SetRightMargin( R/W )
        canvas.SetTopMargin( T/H )
        canvas.SetBottomMargin( B/H )
        canvas.SetTickx()
        canvas.SetTicky()
        legend = getLegend()

        pt = ROOT.TPaveText(0.1746231,0.6031469,0.5251256,0.7517483,"NDC")
        pt.SetTextFont(42)
        pt.SetTextSize(0.04)
        pt.SetTextAlign(12)
        pt.SetFillColor(0)
        pt.SetBorderSize(0)
        pt.SetFillStyle(0)

        return canvas, legend, pt
'''
def getMVVPdf(j,MH,postfix=""):

        var = w.var(options.var)

        pdfName 	= "signal_%d%s" %(MH,postfix)
        Jmean 		= eval(j['MEAN'])
        Jsigma		= eval(j['SIGMA'])
        Jalpha1     = eval(j['ALPHA1'])
        Jalpha2     = eval(j['ALPHA2'])
        Jn1 		= eval(j['N1'])
        Jn2 		= eval(j['N2'])
        
        mean        = ROOT.RooRealVar("mean_%d%s"%(MH,postfix),"mean_%d%s"%(MH,postfix),Jmean)
        sigma       = ROOT.RooRealVar("sigma_%d%s"%(MH,postfix),"sigma_%d%s"%(MH,postfix),Jsigma)        
        alpha1      = ROOT.RooRealVar("alpha1_%d%s"%(MH,postfix),"alpha1_%d%s"%(MH,postfix),Jalpha1)
        alpha2      = ROOT.RooRealVar("alpha2_%d%s"%(MH,postfix),"alpha2_%d%s"%(MH,postfix),Jalpha2)
        n1          = ROOT.RooRealVar("n1_%d%s"%(MH,postfix),"n1_%d%s"%(MH,postfix),Jn1)
        n2          = ROOT.RooRealVar("n2_%d%s"%(MH,postfix),"n2_%d%s"%(MH,postfix),Jn2)
        

        alpha1.setConstant(ROOT.kTRUE)
        alpha2.setConstant(ROOT.kTRUE)
        n2.setConstant(ROOT.kTRUE)
        n1.setConstant(ROOT.kTRUE)
        mean.setConstant(ROOT.kTRUE)
        sigma.setConstant(ROOT.kTRUE)
                
        # gauss     = ROOT.RooGaussian("gauss_%d%s"%(MH,postfix), "gauss_%d%s"%(MH,postfix), var, mean, gsigma)
        # cb        = ROOT.RooCBShape("cb_%d%s"%(MH,postfix), "cb_%d%s"%(MH,postfix),var, mean, sigma, alpha, sign)
        # function = ROOT.RooAddPdf(pdfName, pdfName,gauss, cb, sigfrac)
        function = ROOT.RooDoubleCB(pdfName, pdfName,var, mean,sigma,alpha1,n1,alpha2,n2)
        getattr(w,'import')(function,ROOT.RooFit.Rename(pdfName))

def getMJPdf(j,MH,postfix=""):
 
        var = w.var(options.var)
	
        pdfName 	= "signal_%d%s" %(MH,postfix)
        Jmean 		= eval(j['mean'])
        Jsigma		= eval(j['sigma'])
        Jalpha 		= eval(j['alpha'])
        Jalpha2 	= eval(j['alpha2'])
        Jn 		= eval(j['n'])
        Jn2 		= eval(j['n2'])

        mean        = ROOT.RooRealVar("mean_%d%s"%(MH,postfix),"mean_%d%s"%(MH,postfix),Jmean)
        sigma       = ROOT.RooRealVar("sigma_%d%s"%(MH,postfix),"sigma_%d%s"%(MH,postfix),Jsigma)
        alpha       = ROOT.RooRealVar("alpha_%d%s"%(MH,postfix),"alpha_%d%s"%(MH,postfix),Jalpha)
        alpha2      = ROOT.RooRealVar("alpha2_%d%s"%(MH,postfix),"alpha2_%d%s"%(MH,postfix),Jalpha2)
        sign        = ROOT.RooRealVar("sign_%d%s"%(MH,postfix),"sign_%d%s"%(MH,postfix),Jn)
        sign2        = ROOT.RooRealVar("sign2_%d%s"%(MH,postfix),"sign2_%d%s"%(MH,postfix),Jn2)        

        alpha.setConstant(ROOT.kTRUE)
        sign.setConstant(ROOT.kTRUE)
        alpha2.setConstant(ROOT.kTRUE)
        sign2.setConstant(ROOT.kTRUE)
        mean.setConstant(ROOT.kTRUE)
        sigma.setConstant(ROOT.kTRUE)
        
	function = ROOT.RooDoubleCB(pdfName, pdfName, var, mean, sigma, alpha, sign,  alpha2, sign2)  
	getattr(w,'import')(function,ROOT.RooFit.Rename(pdfName))
'''		
parser = optparse.OptionParser()
parser.add_option("-f","--file",dest="file",default='JJ_BulkGWW_MVV.json',help="input file")
parser.add_option("-v","--var",dest="var",help="mVV or mJ",default='mVV')
parser.add_option("-l","--leg",dest="leg",help="l1 or l2",default='l1')
parser.add_option("-p","--period",dest="period",help="2016 or 2017 or 2018",default='2016')
parser.add_option("-c","--category",dest="category",help="VV_HPHP or VV_HPLP or VH_HPHP etc",default='VV_HPLP')
parser.add_option("-d","--directory",dest="directory",help="input directory",default='')
parser.add_option("-n","--name",dest="name",help="specify a label for the output file name",default='All')

postfix = "Jet 1 "
(options,args) = parser.parse_args()
if options.leg == "l2" !=-1: postfix = "Jet 2 "
purity  = options.category


inFileName = options.file
#massPoints = [1000,1200,1400,1600,1800,2000,2500,3000,3500,4000,4500]
massPoints = [1200,1400,1600,1800,2000,2500,3000,3500,4000,4500]
#massPoints = [1200,1400,1600,1800,2000,2200,2400,2600,2800,3000,3200,3400,3600,3800,4000,4200,4400,4600,4800,5000,5200]
varName = {'mVV':'M_{VV} (GeV)','mJ':'%ssoftdrop mass (GeV)'%postfix}
varBins = {'mVV':'[37,1000,5500]','mJ':'[80,55,215]'}
w=ROOT.RooWorkspace("w","w")
w.factory(options.var+varBins[options.var])
w.var(options.var).SetTitle(varName[options.var])
colors= []
colors.append(["#f9c677","#f9d077","#f9f577","#ffd300","#f9fe77","#f9fe64","#f9fe43","#f9fe17"]*3)
colors.append(["#fee0d2","#fcbba1","#fc9272","#ef3b2c","#ef3b2c","#cb181d","#a50f15","#67000d"]*3) 
colors.append(["#e5f5e0","#c7e9c0","#a1d99b","#41ab5d","#41ab5d","#238b45","#006d2c","#00441b"]*3) 
colors.append(["#02fefe","#02e5fe","#02d7fe","#4292c6","#02b5fe","#02a8fe","#0282fe","#0300fc"]*3)  
colors.append(["#e6a3e1","#d987e6","#ce5ce0","#822391","#8526bd","#9b20e3","#a87eed","#8649eb"]*3)  

def doSingle():
    with open(inFileName) as jsonFile:
      j = json.load(jsonFile)
    
      c1 = getCanvas()
      c1.Draw()
      leg = ROOT.TLegend(0.8, 0.2, 0.95, 0.8)
      frame = w.var(options.var).frame()   
      
      for i, MH in enumerate(massPoints):  # mind that MH is evaluated below
        if options.var == 'mVV': getMVVPdf(j,MH)
        else: getMJPdf(j,MH)
        w.pdf('signal_%d'%MH).plotOn(frame, ROOT.RooFit.LineColor(ROOT.TColor.GetColor(colors[0][i])),ROOT.RooFit.Name(str(MH)))#,ROOT.RooFit.Range(MH*0.8,1.2*MH))#ROOT.RooFit.Normalization(1, ROOT.RooAbsReal.RelativeExpected),
        leg.AddEntry(frame.findObject(str(MH)), "%d GeV" % MH, "L")
      frame.GetYaxis().SetTitle("A.U")
      frame.GetYaxis().SetNdivisions(4,5,0)
      frame.SetMaximum(0.1)
      if options.var == 'mVV':frame.SetMaximum(0.5)
      frame.Draw()
      # leg.Draw("same")
      model = "G_{B} #rightarrow WW"
      if options.file.find("ZZ")!=-1:
          model = "G_{B} #rightarrow ZZ"
      if options.file.find("WZ")!=-1:
          model = "W' #rightarrow WZ"
      if options.file.find("Zprime")!=-1:
          model = "Z' #rightarrow WW"
      if   options.file.find("HPHP")!=-1: purity = "HPHP"
      elif options.file.find("HPLP")!=-1: purity = "HPLP"
      else:purity = "HPLP+HPHP"
      c1.cd()
      pt =ROOT.TPaveText(0.81,0.82,0.84,0.89,"brNDC")
      pt.SetBorderSize(0)
      pt.SetTextAlign(12)
      pt.SetFillStyle(0)
      pt.SetTextFont(42)
      pt.SetTextSize(0.04)
      pt.AddText(model)
      # pt.AddText(purity)

      pt.Draw()
      cmslabel_sim(c1,'2016',11)
      c1.Update()
      
      c1.SaveAs(path+"signalShapes%s_%s.png" %(options.var, inFileName.rsplit(".", 1)[0]))
      c1.SaveAs(path+"signalShapes%s_%s.pdf" %(options.var, inFileName.rsplit(".", 1)[0]))
      c1.SaveAs(path+"signalShapes%s_%s.C" %(options.var, inFileName.rsplit(".", 1)[0]))
      c1.SaveAs(path+"signalShapes%s_%s.root" %(options.var, inFileName.rsplit(".", 1)[0]))
  
def doAll():
    files = ["JJ_BulkGZZ_"+str(options.period)+"_"+str(purity)+"_yield.root","JJ_WprimeWZ_"+str(options.period)+"_"+str(purity)+"_yield.root","JJ_BulkGWW_"+str(options.period)+"_"+str(purity)+"_yield.root","JJ_ZprimeWW_"+str(options.period)+"_"+str(purity)+"_yield.root","JJ_ZprimeZH_"+str(options.period)+"_"+str(purity)+"_yield.root"]
    legs = ["G_{bulk} #rightarrow ZZ","W' #rightarrow WZ","G_{bulk} #rightarrow WW","Z'#rightarrow WW","Z'#rightarrow ZH"]
    c1,leg,pt = getCanvasPaper("c1")
    c1.Draw()
    gr=[]
    #leg = getLegend()
    for ii,f in enumerate(files):
      print f
      name = f.split("_")[1]
      r_file = ROOT.TFile(str(options.directory)+f,"READ")
      gr = r_file.Get("yield")
      print " get number of points ", gr.GetN()
      for i in range(gr.GetN()) :
        print gr.GetY()[i]
        gr.GetY()[i] *= 1000
        print gr.GetY()[i]

      gr.SetLineColor(ROOT.TColor.GetColor(colors[ii][3]))
      gr.SetLineStyle(2)
      gr.SetLineWidth(2)
      gr.SetMarkerColor(ROOT.TColor.GetColor(colors[ii][3]))
      gr.SetMarkerStyle(24)
      gr.GetYaxis().SetTitle("a.u.")
      gr.GetXaxis().SetTitle("m_{X} [GeV]")
      gr.GetYaxis().SetTitleOffset(1.3)
      gr.GetYaxis().SetNdivisions(4,5,0)
      gr.GetXaxis().SetNdivisions(3,5,0)
      gr.SetMinimum(0.)
      gr.SetMaximum(0.225)
      gr.GetXaxis().SetTitleSize(0.055)
      gr.GetYaxis().SetTitleSize(0.055)
      gr.GetYaxis().SetLabelSize(0.05)
      gr.GetXaxis().SetLabelSize(0.05)
      ff = gr.GetFunction("func")
      if ff != None:
        gr.Fit(ff)
        ff.SetLineColor(0) 
        ff.SetLineWidth(0)
      #ff1000.Draw("same")
      leg.AddEntry(gr, legs[ii], "L")
      #    if options.var == 'mVV':gr.SetMaximum(0.45)
      if ii == 0 :gr_gzz = gr #gr.Draw("AP")        
      elif ii == 1 :gr_w = gr #gr.Draw("AP")        
      if ii == 2 :gr_z = gr #gr.Draw("AP")        
      if ii == 3 :gr_gww = gr #gr.Draw("AP")        
      if ii == 4 :gr_zh = gr #gr.Draw("AP")        



    gr_gzz.Draw("APL")
    gr_w.Draw("PL")
    gr_z.Draw("PL")
    gr_gww.Draw("PL")
    gr_zh.Draw("PL")
    leg.Draw("same")
 
    
    pt2 = ROOT.TPaveText(0.16,0.62,0.63,0.76,"NDC")
    pt2.SetTextFont(42)
    pt2.SetTextSize(0.04)
    pt2.SetTextAlign(12)
    pt2.SetFillColor(0)
    pt2.SetBorderSize(0)
    pt2.SetFillStyle(0)
    pt2.AddText(str(purity)+" category")
    pt2.Draw()


    name = path+"signalYelds_%s_%s_%s_%s"  %(options.var,options.period,purity,options.name)
    c1.SaveAs(name+".png")
    c1.SaveAs(name+".pdf" )
    c1.SaveAs(name+".C"   )
    c1.SaveAs(name+".root")
    
    # sleep(1000)
                
if __name__ == '__main__':
#    doSingle() #NB: some fix would be needed here!
    doAll()