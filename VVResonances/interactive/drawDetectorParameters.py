from ROOT import TFile, TCanvas, TPaveText, TLegend, gDirectory, TH1F,gROOT,gStyle, TLatex,TF1
import sys,copy
import tdrstyle
tdrstyle.setTDRStyle()
from  CMGTools.VVResonances.plotting.CMS_lumi import *

from time import sleep
gROOT.SetBatch(True)
# infile = sys.argv[1]                                                                                                                                                                                                                        
# f = TFile(infile,"READ")                                                                                                                                                                                                                    

path = sys.argv[1]
cols = [46,30]
colors = ["#4292c6","#41ab5d","#ef3b2c","#ffd300","#D02090","#fdae61","#abd9e9","#2c7bb6"]
mstyle = [8,24,22,26,32]                                                                                                                                                                                                                     
#linestyle=[1,2,1,2,3]                                                                                                                                                                                                                        
markerstyle = [1,4,8,10,20,25]
linestyle = [1,2,3,4,5,6,7,8,9]
#mstyle = [8,4]

def beautify(h1,color,linestyle=1,markerstyle=8):
    h1.SetLineColor(color)
    h1.SetMarkerColor(color)
    # h1.SetFillColor(color)                                                                                                                                                                                                                  
    h1.SetLineWidth(3)
    h1.SetLineStyle(linestyle)
    h1.SetMarkerStyle(markerstyle)

def getLegend(x1=0.5809045,y1=0.6363636,x2=0.9522613,y2=0.9020979):
  legend = TLegend(x1,y1,x2,y2)
  legend.SetTextSize(0.04)
  legend.SetLineColor(0)
  legend.SetShadowColor(0)
  legend.SetLineStyle(1)
  legend.SetLineWidth(1)
  legend.SetFillColor(0)
  legend.SetFillStyle(0)
  legend.SetMargin(0.35)
  legend.SetTextFont(42)
  return legend

def getPavetext():
  addInfo = TPaveText(0.3010112,0.2066292,0.4202143,0.3523546,"NDC")
  addInfo.SetFillColor(0)
  addInfo.SetLineColor(0)
  addInfo.SetFillStyle(0)
  addInfo.SetBorderSize(0)
  addInfo.SetTextFont(42)
  addInfo.SetTextSize(0.040)
  addInfo.SetTextAlign(12)
  return addInfo

def getCanvas(w=800,h=600):

 H_ref = 600
 W_ref = 600
 W = W_ref
 H  = H_ref

 iPeriod = 0

 # references for T, B, L, R                                                                                                                                                                                                                  
 T = 0.08*H_ref
 B = 0.12*H_ref
 L = 0.15*W_ref
 R = 0.04*W_ref
 cname = "c"
 canvas = TCanvas(cname,cname,50,50,W,H)
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

 return canvas






def doDetPar(leg,years):
    print years
    gStyle.SetOptFit(0)
    
    files=[]
    for i,s in enumerate(years):
        inputDir = "det"+s+"_"+leg
        files.append(TFile(inputDir+"/JJ_"+s+"_nonRes_detectorResponse.root","READ"))
    
    variables = ["scalexHisto","scaleyHisto","resxHisto","resyHisto"] 
    titles = ["M_{VV} scale","M_{jet} scale","M_{VV} resolution","M_{jet} resolution"]
    for j,var in enumerate(variables):
       datas=[]
       c = getCanvas()
       l = getLegend()#0.7788945,0.723362,0.9974874,0.879833)                                                                                                                                                                                 

       gStyle.SetOptStat(0)
       gStyle.SetOptTitle(0)
       for i,f in enumerate(files):
           print f
           g = f.Get(var)
           print g
           print colors[i]
           print mstyle[i]
           print i 
           beautify(g ,rt.TColor.GetColor(colors[i]),1,mstyle[i])
#           datas.append(g)
           l.AddEntry(g,years[i],"LP")

           g.GetXaxis().SetTitle("Gen p_{T} [GeV]")
           g.GetYaxis().SetTitle(titles[j])
           
           g.GetYaxis().SetNdivisions(4,5,0)
           g.GetXaxis().SetNdivisions(5,5,0)
           g.GetYaxis().SetTitleOffset(1.05)
           g.GetXaxis().SetTitleOffset(0.9)
           g.GetXaxis().SetRangeUser(200, 5000.)
           g.GetXaxis().SetLabelSize(0.05)
           g.GetXaxis().SetTitleSize(0.06)
           g.GetYaxis().SetLabelSize(0.05)
           g.GetYaxis().SetTitleSize(0.06)
           if var == "scalexHisto": g.GetYaxis().SetRangeUser(0.9,1.1);
           if var == "scaleyHisto": g.GetYaxis().SetRangeUser(0.9,1.1);
           if var == "resxHisto": g.GetYaxis().SetRangeUser(0,0.15)
           if var == "resyHisto": g.GetYaxis().SetRangeUser(0,0.15)
           #if(i==0): g.Draw("EP")
           g.Draw("EPsame")
           g.GetXaxis().SetRangeUser(200., 5000.)
       l.Draw("same")
       if prelim.find("prelim")!=-1:
           cmslabel_sim_prelim(c,'sim',11)
       else:
           cmslabel_sim(c,'sim',11)
       pt = getPavetext()
       c.Update()
       c.SaveAs(path+"DetPar_"+var+"_"+leg+prelim+".png")
       c.SaveAs(path+"DetPar_"+var+"_"+leg+prelim+".pdf")
       c.SaveAs(path+"DetPar_"+var+"_"+leg+prelim+".C")



if __name__ == '__main__':
  prelim = ""
  years = ["2016","2017","Run2"]
  doDetPar("l1",years)
