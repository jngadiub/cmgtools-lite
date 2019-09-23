#!/bin/env python
import ROOT
import json
import math
ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")
from time import sleep
import optparse, sys
from  CMGTools.VVResonances.plotting.CMS_lumi import *

# ROOT.gROOT.SetBatch(True)

def getLegend(textsize=0.20,x1=0.5809045,y1=0.6363636,x2=0.9522613,y2=0.9020979):
  legend = ROOT.TLegend(x1,y1,x2,y2)
  legend.SetTextSize(textsize)
  legend.SetLineColor(0)
  legend.SetShadowColor(0)
  legend.SetLineStyle(1)
  legend.SetLineWidth(1)
  legend.SetFillColor(0)
  legend.SetFillStyle(0)
  legend.SetMargin(0.35)
  legend.SetTextFont(42)
  return legend
  
def getCanvasPaper(cname):
 ROOT.gStyle.SetOptStat(0)

 H_ref = 700 
 W_ref = 600 
 W = W_ref
 H  = H_ref
 iPeriod = 0
 # references for T, B, L, R
 if options.var =="mVV":
    T = 0.3*H_ref
    B = 0.35*H_ref 
    L = 0.10*W_ref
    R = 0.07*W_ref
 else:
    T = 0.08*H_ref
    B = 0.12*H_ref
    L = 0.14*W_ref
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
 #legend = getLegend()
 
 
 pt = ROOT.TPaveText(0.1746231,0.6031469,0.5251256,0.7517483,"NDC")
 pt.SetTextFont(42)
 pt.SetTextSize(0.04)
 pt.SetTextAlign(12)
 pt.SetFillColor(0)
 pt.SetBorderSize(0)
 pt.SetFillStyle(0)
 
 
 return canvas, pt

	
def getMVVPdf(w,j,MH,postfix=""):

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

def getMJPdf(w,j,MH,postfix="",jH=None):
        
        var = w.var(options.var)
	if postfix.find("H")==-1:
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
        else:
            if postfix =="H": postfix = ""
            pdfName 	= "signal_%d%s" %(MH,postfix)
            Jmean 		= eval(j['mean'])
            Jsigma		= eval(j['sigma'])
            Jalpha 		= eval(j['alpha'])
            Jalpha2 	= eval(j['alpha2'])
            Jn 		= eval(j['n'])
            Jn2 		= eval(j['n2'])
            
            JmeanH 		= eval(jH['meanH'])
            JsigmaH		= eval(jH['sigmaH'])
            JalphaH 		= eval(jH['alphaH'])
            Jalpha2H 	= eval(jH['alpha2H'])
            JnH 		= eval(jH['nH'])
            Jn2H 		= eval(jH['n2H'])
            
            

            mean        = ROOT.RooRealVar("mean_%d%s"%(MH,postfix),"mean_%d%s"%(MH,postfix),Jmean)
            sigma       = ROOT.RooRealVar("sigma_%d%s"%(MH,postfix),"sigma_%d%s"%(MH,postfix),Jsigma)
            alpha       = ROOT.RooRealVar("alpha_%d%s"%(MH,postfix),"alpha_%d%s"%(MH,postfix),Jalpha)
            alpha2      = ROOT.RooRealVar("alpha2_%d%s"%(MH,postfix),"alpha2_%d%s"%(MH,postfix),Jalpha2)
            sign        = ROOT.RooRealVar("sign_%d%s"%(MH,postfix),"sign_%d%s"%(MH,postfix),Jn)
            sign2        = ROOT.RooRealVar("sign2_%d%s"%(MH,postfix),"sign2_%d%s"%(MH,postfix),Jn2)
            
            meanH        = ROOT.RooRealVar("Hmean_%d%s"%(MH,postfix),"Hmean_%d%s"%(MH,postfix),JmeanH)
            sigmaH       = ROOT.RooRealVar("Hsigma_%d%s"%(MH,postfix),"Hsigma_%d%s"%(MH,postfix),JsigmaH)
            alphaH       = ROOT.RooRealVar("Halpha_%d%s"%(MH,postfix),"Halpha_%d%s"%(MH,postfix),JalphaH)
            alpha2H      = ROOT.RooRealVar("Halpha2_%d%s"%(MH,postfix),"Halpha2_%d%s"%(MH,postfix),Jalpha2H)
            signH        = ROOT.RooRealVar("Hsign_%d%s"%(MH,postfix),"Hsign_%d%s"%(MH,postfix),JnH)
            sign2H        = ROOT.RooRealVar("Hsign2_%d%s"%(MH,postfix),"Hsign2_%d%s"%(MH,postfix),Jn2H)
            
            ratio        = ROOT.RooRealVar("ratio_%d%s"%(MH,postfix),"ratio_%d%s"%(MH,postfix),0.5)

            alpha.setConstant(ROOT.kTRUE)
            sign.setConstant(ROOT.kTRUE)
            alpha2.setConstant(ROOT.kTRUE)
            sign2.setConstant(ROOT.kTRUE)
            mean.setConstant(ROOT.kTRUE)
            sigma.setConstant(ROOT.kTRUE)
            
            alphaH.setConstant(ROOT.kTRUE)
            signH.setConstant(ROOT.kTRUE)
            alpha2H.setConstant(ROOT.kTRUE)
            sign2H.setConstant(ROOT.kTRUE)
            meanH.setConstant(ROOT.kTRUE)
            sigmaH.setConstant(ROOT.kTRUE)
            
            function1 = ROOT.RooDoubleCB(pdfName+"1", pdfName+"1", var, mean, sigma, alpha, sign,  alpha2, sign2) 
            function2 = ROOT.RooDoubleCB(pdfName+"2", pdfName+"2", var, meanH, sigmaH, alphaH, signH,  alpha2H, sign2H)
            function =  ROOT.RooAddPdf(pdfName,pdfName,function1,function2,ratio)
            getattr(w,'import')(function,ROOT.RooFit.Rename(pdfName))
            
		
parser = optparse.OptionParser()
parser.add_option("-f","--file",dest="file",default='JJ_BulkGWW_2016_MVV.json',help="input file (JJ_{sig}_2016_MVV.json,JJ_{sig}_2016_MJrandom_VV_HPLP.json)")
parser.add_option("-v","--var",dest="var",help="mVV or mJ",default='mVV')
parser.add_option("-y","--year",dest="year",help="2016 or 2017 or 2018",default='2016')
parser.add_option("-c","--category",dest="category",help="VV_HPHP or VV_HPLP or VH_HPHP etc",default='VV_HPLP')
parser.add_option("-o","--outdir",dest="outdir",help="output directory",default='../plots/')
parser.add_option("-i","--indir",dest="indir",help="input directory",default='results_2016/')
parser.add_option("-n","--name",dest="name",help="you may specify an additional label for the output file",default='test')
parser.add_option("-l","--leg",dest="leg",help="mVV or mJ",default='l1')
parser.add_option("-p","--prelim",dest="prelim",help="with label preliminary or not",default=0)

(options,args) = parser.parse_args()

path = options.outdir

purity  = options.category

inFileName = options.file
massPoints = [1200,1400,1600,1800,2000,2500,3000,3500,4000,4500]
postfix = "Jet 1 "
if options.leg == "l2" !=-1: postfix = "Jet 2 "
varName = {'mVV':'Dijet invariant mass [GeV]','mJ':'%sJet mass [GeV]'%postfix}
varBins = {'mVV':'[37,1000,5500]','mJ':'[80,55,215]'}
#w=ROOT.RooWorkspace("w","w")
#w.factory(options.var+varBins[options.var])
#w.var(options.var).SetTitle(varName[options.var])
colors= []
#colors.append(["#f9c677","#f9d077","#f9f577","#ffd300","#f9fe77","#f9fe64","#f9fe43","#f9fe17"]*3)
#colors.append(["#fee0d2","#fcbba1","#fc9272","#ef3b2c","#ef3b2c","#cb181d","#a50f15","#67000d"]*3) 
#colors.append(["#e5f5e0","#c7e9c0","#a1d99b","#41ab5d","#41ab5d","#238b45","#006d2c","#00441b"]*3) 
#colors.append(["#02fefe","#02e5fe","#02d7fe","#4292c6","#02b5fe","#02a8fe","#0282fe","#0300fc"]*3)  
#colors.append(["#e6a3e1","#d987e6","#ce5ce0","#822391","#8526bd","#9b20e3","#a87eed","#8649eb"]*3)
colors.append(["#000080","#0000CD","#0000FF","#3D59AB","#4169E1","#4876FF","#6495ED","#1E90FF","#63B8FF","#87CEFA","#C6E2FF"]*3)   
colors.append(["#006400","#308014","#228B22","#32CD32","#00CD00","#00EE00","#00FF00","#7CCD7C","#7CFC00","#ADFF2F","#C0FF3E"]*3)   
colors.append(["#CD8500","#CD950C","#EE9A00","#EEAD0E","#FFA500","#FFB90F","#FFC125","#EEC900","#FFD700","#FFEC8B","#FFF68F"]*3) 
colors.append(["#8B2500","#CD3700","#EE4000","#FF4500","#CD4F39","#EE5C42","#EE6A50","#FF7256","#FA8072","#FFA07A","#EEB4B4"]*3)
colors.append(["#EE82EE","#FF00FF","#D02090","#C71585","#B03060 ","#DB7093","#FFB6C1","#FFC0CB"]*3)

def doSingle():
    w=ROOT.RooWorkspace("w","w")
    w.factory(options.var+varBins[options.var])
    w.var(options.var).SetTitle(varName[options.var])
    with open(inFileName) as jsonFile:
      j = json.load(jsonFile)
    
      c1 = getCanvasPaper("c1")[0]
      c1.Draw()
      leg = ROOT.TLegend(0.8, 0.2, 0.95, 0.8)
      frame = w.var(options.var).frame()   
      
      for i, MH in enumerate(massPoints):  # mind that MH is evaluated below
        if options.var == 'mVV': getMVVPdf(w,j,MH)
        else: 
            if inFileName.find("H")==-1:
                getMJPdf(w,j,MH)
            if inFileName.find("Vjet")!=-1:
                with open(inFileName.replace("Vjet","Hjet")) as jsonFileH:
                    jH = json.load(jsonFileH)
                getMJPdf(j,MH,"H",jH)
            if inFileName.find("Hjet")!=-1:
                with open(inFileName.replace("Hjet","Vjet")) as jsonFileV:
                    jV = json.load(jsonFileV)
                getMJPdf(w,jV,MH,"H",j)
                
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
  

def doAll(category,jsons,legs):
    w=ROOT.RooWorkspace("w","w")
    w.factory(options.var+varBins[options.var])
    w.var(options.var).SetTitle(varName[options.var])
    #legs = ["G_{bulk} #rightarrow ZZ","W' #rightarrow WZ","G_{bulk} #rightarrow WW","Z'#rightarrow WW","Z' #rightarrow ZH"]
    c1,pt = getCanvasPaper("c1")

    c1.Draw()
    if options.var == 'mVV':
        c1.Divide(1,5,0.0,0.0)
    leg = []
    frame = []  
    #frame.SetTitle("")
    for ii,f in enumerate(jsons):
        if options.var == 'mVV':
            c1.cd(ii)
            if ii==len(jsons)-1:
                leg.append(getLegend(0.15))
            else:
                leg.append(getLegend())
            frame.append( w.var(options.var).frame() ) 
        else:
            if ii ==0:
                leg.append(getLegend(0.05,0.46))
                frame.append( w.var(options.var).frame() ) 
        if options.var=='mJ':
            frame[-1].SetAxisRange(55,150)
        frame[-1].SetTitle("")
        name = f.split("_")[1]
        with open(options.indir+f) as jsonFile:
          j = json.load(jsonFile)
          for i, MH in enumerate(massPoints):  # mind that MH is evaluated below

            print " i "+str(i)+" MH "+str(MH)+" j "+str(j)+" name " +str(name)
            if options.var == 'mVV': getMVVPdf(w,j,MH,name)

            else: 
                if f.find("ZH")==-1:
                    print "no H boson in sample "
                    getMJPdf(w,j,MH,name)
                if f.find("Vjet")!=-1:
                    with open(f.replace("Vjet","Hjet")) as jsonFileH:
                        jH = json.load(jsonFileH)
                    getMJPdf(j,MH,name,jH)
                if f.find("Hjet")!=-1:
                    with open(f.replace("Hjet","Vjet")) as jsonFileV:
                        jV = json.load(jsonFileV)
                    getMJPdf(w,jV,MH,name,j)
  
  
            w.pdf('signal_%d%s'%(MH,name)).plotOn(frame[-1], ROOT.RooFit.LineColor(ROOT.TColor.GetColor(colors[ii][i])),ROOT.RooFit.Name(str(MH)+name))#,ROOT.RooFit.Range(MH*0.8,1.2*MH))#ROOT.RooFit.Normalization(1, ROOT.RooAbsReal.RelativeExpected),
      
    if options.var == 'mVV': 
        for ii,f in enumerate(jsons):
            print len(jsons)
            print ii
            print "json "+str(jsons[len(jsons)-ii-1])
            name = jsons[ii].split("_")[1]
            leg[ii].AddEntry(frame[ii].findObject(str(2000)+name), legs[ii], "L")
    else:
        for ii,f in enumerate(jsons):
            name = jsons[len(jsons)-ii-1].split("_")[1]
            leg[-1].AddEntry(frame[0].findObject(str(2000)+name),legs[len(jsons)-ii-1],"L")

    '''
    <<<<<<<<<<<<<<<<<<<<<<<<
    for ii,f in enumerate(jsons):
        print len(jsons)
        print ii
        print "json "+str(jsons[len(jsons)-ii-1])
        name = jsons[len(jsons)-ii-1].split("_")[1]
        leg.AddEntry(frame.findObject(str(1800)+name), legs[len(jsons)-ii-1], "L")
    frame.GetYaxis().SetTitle("a.u.")
    frame.GetYaxis().SetTitleOffset(1.3)
    frame.GetYaxis().SetNdivisions(4,5,0)
    frame.GetXaxis().SetNdivisions(3,5,0)
    frame.SetMaximum(0.17)
    frame.GetXaxis().SetTitleSize(0.055)
    frame.GetYaxis().SetTitleSize(0.055)
    frame.GetYaxis().SetLabelSize(0.05)
    frame.GetXaxis().SetLabelSize(0.05)
    if options.var == 'mVV':
      frame.SetMaximum(0.3)
      frame.GetXaxis().SetTitle("Dijet invariant mass [GeV]")
    frame.Draw()
    leg.Draw("same")
    =======
    '''
    for i in range(1,len(frame)+1):
        c1.cd(i)
        c1.cd(i).SetTickx()
        c1.cd(i).SetTicky()
      
      
        frame[i-1].GetYaxis().SetTitle("a. u.")
        frame[i-1].GetYaxis().SetTitleOffset(1.18)
        frame[i-1].GetXaxis().SetTitleOffset(0.9)
        frame[i-1].GetYaxis().SetNdivisions(6,5,1)
        frame[i-1].GetXaxis().SetNdivisions(6,5,1)
        frame[i-1].SetMaximum(0.17)
        if options.var == 'mVV':
            frame[i-1].SetMaximum(0.45)
            frame[i-1].GetYaxis().SetNdivisions(0,5,0,False)
            frame[i-1].GetYaxis().SetTitleOffset(0.25)
            frame[i-1].GetXaxis().SetTitleSize(0.20)
            frame[i-1].GetYaxis().SetTitleSize(0.20)
            frame[i-1].GetYaxis().SetLabelSize(0.20)
            frame[i-1].GetXaxis().SetLabelSize(0.20)
            #frame[i-1].Draw()
            frame[i-1].GetXaxis().SetTickLength(0.1)
            frame[-1].GetYaxis().SetLabelSize(0.14) 
            frame[-1].GetXaxis().SetLabelSize(0.14)
            frame[-1].GetXaxis().SetTitleSize(0.14)
            frame[-1].GetYaxis().SetTitleSize(0.14)
            frame[-1].GetYaxis().SetTitleOffset(0.35)
            frame[-1].GetXaxis().SetTitleOffset(1.05)
            frame[-1].GetXaxis().SetLabelOffset(0.05)
            frame[-1].GetXaxis().SetTickLength(0.08)
        else:    
            
            frame[i-1].GetXaxis().SetTitleSize(0.06)
            frame[i-1].GetYaxis().SetTitleSize(0.06)
            frame[i-1].GetYaxis().SetLabelSize(0.05)
            frame[i-1].GetXaxis().SetLabelSize(0.05)
                
        frame[i-1].Draw()
        leg[i-1].Draw("same")
    
    
    pt2 = ROOT.TPaveText(0.16,0.62,0.63,0.76,"NDC")
    pt2.SetTextFont(42)
    pt2.SetTextSize(0.04)
    pt2.SetTextAlign(12)
    pt2.SetFillColor(0)
    pt2.SetBorderSize(0)
    pt2.SetFillStyle(0)

    if options.var == 'mJ': pt2.AddText(category)
    pt2.Draw()
    if options.var =="mVV": category = "Vall"
    if options.prelim=="1":
        cmslabel_sim_prelim(c1,'sim',11)
        c1.Update()
        c1.SaveAs(path+"signalShapes_%s_%s_%s_All_%s_prelim.png"  %(options.var,category,options.period,options.name))
        c1.SaveAs(path+"signalShapes_%s_%s_%s_All_%s_prelim.pdf"  %(options.var,category,options.period,options.name))
        c1.SaveAs(path+"signalShapes_%s_%s_%s_All_%s_prelim.C"    %(options.var,category,options.period,options.name))
        c1.SaveAs(path+"signalShapes_%s_%s_%s_All_%s_prelim.root" %(options.var,category,options.period,options.name))
    else:
        cmslabel_sim(c1,'sim',11)
        c1.Update()
        
        c1.SaveAs(path+"signalShapes_%s_%s_%s_All_%s.png"  %(options.var,category,options.period,options.name))
        c1.SaveAs(path+"signalShapes_%s_%s_%s_All_%s.pdf"  %(options.var,category,options.period,options.name))
        c1.SaveAs(path+"signalShapes_%s_%s_%s_All_%s.C"    %(options.var,category,options.period,options.name))
        c1.SaveAs(path+"signalShapes_%s_%s_%s_All_%s.root" %(options.var,category,options.period,options.name))
    
      
if __name__ == '__main__':
    #doSingle()
    legs = ["G_{bulk} #rightarrow ZZ","W' #rightarrow WZ","G_{bulk} #rightarrow WW","Z'#rightarrow WW","Z' #rightarrow ZH"]
    signals = ["BulkGZZ","WprimeWZ","BulkGWW","ZprimeWW"]
    categories = ["VV_HPLP"]#,"VV_HPHP","VH_HPLP","VH_HPHP"]
    jsons=[]
    for category in categories:
        for s in signals:
            if options.var =="mJ":
                jsons.append("JJ_"+s+"_2016_MJrandom_"+category+".json")
            else: jsons.append("JJ_"+s+"_2016_MVV.json")
        if options.var=="mJ":
            jsons.append("JJ_Hjet_ZprimeZH_2016_MJrandom_"+category+".json")
        else:
            jsons.append("JJ_j1ZprimeZH_2016_MVV.json")
        doAll(category,jsons,legs)
