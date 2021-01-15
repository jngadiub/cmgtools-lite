import ROOT
import json
import math
import types
from array import array

def getLegend(x1=0.5809045,y1=0.6363636,x2=0.9522613,y2=0.9020979):
  legend = ROOT.TLegend(x1,y1,x2,y2)
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
  addInfo = ROOT.TPaveText(0.3010112,0.2066292,0.4202143,0.3523546,"NDC")
  addInfo.SetFillColor(0)
  addInfo.SetLineColor(0)
  addInfo.SetFillStyle(0)
  addInfo.SetBorderSize(0)
  addInfo.SetTextFont(42)
  addInfo.SetTextSize(0.040)
  addInfo.SetTextAlign(12)
  return addInfo



def fitSF(SF,SFerr,year,tagger,WP):
    

    canvas = ROOT.TCanvas("c","c",500,500)
    canvas.SetFillColor(0)
    canvas.SetBorderMode(0)
    canvas.SetFrameFillStyle(0)
    canvas.SetFrameBorderMode(0)
    canvas.SetTickx()
    canvas.SetTicky()
    l = getLegend()#0.7788945,0.723362,0.9974874,0.879833)
    ptt = getPavetext()
    ptt.AddText(tagger+" "+WP+" "+year)
    n=3
    pta, SFa = array( 'd' ), array( 'd' )
    pterra, SFerra = array( 'd' ), array( 'd' )
    pt = {"ZHbb":[350.,550.,700,],"W":[235.,350.,600.]}
    pterr = [0.,0.,0.]
    #SF=[1.053,1.013,1.034]
    #SFerr = [0.053,0.036,0.031]
    for i in range( n ):
        pta.append(pt[tagger][i])
        SFa.append(SF[i])
        print " pt ",pta[i]
        print " SF ",SFa[i]
        pterra.append(pterr[i])
        SFerra.append(SFerr[i])

    gr = ROOT.TGraphErrors( n, pta, SFa, pterra, SFerra )
    gr.SetTitle("" )
    gr.SetMarkerColor( 4 )
    gr.SetMarkerStyle( 21 )
    gr.GetXaxis().SetTitle( 'pt [GeV]' )
    gr.GetXaxis().SetLimits(200.,3000.)
    gr.GetYaxis().SetTitle( 'SF' )
    gr.GetYaxis().SetRangeUser(0.,2.)
    gr.Draw( 'ACP' )
    fit1 = ROOT.TF1("fit1","pol1",200.,3000.)
    gr.Fit("fit1") #,"R",200.,3000.)
    fit1.Draw("same")
    slope = fit1.GetParameter(1)
    intercept = fit1.GetParameter(0)
    l.AddEntry(fit1,"pol1","l")
    #print " at 2 TeV SF = ",fit.Eval(2000.)
    fit0 = ROOT.TF1("fit0","pol0",200.,3000.)
    fit0.SetLineStyle(2)
    gr.Fit("fit0") #,"R",200.,3000.)
    fit0.Draw("same")
    l.AddEntry(fit0,"pol0","l")
    l.Draw()
    ptt.Draw()
    
    canvas.Update()
    name = tagger+"SFvsPT_"+year+"_"+WP
    canvas.SaveAs(name+".pdf")
    return [slope,intercept]

years=["2016","2017","2018"]
tagger=["W","ZHbb"]
purity=["HP","LP"]

SF={"W":{"HP":
         {"2016":[0.904,0.948,1.000],
          "2017":[0.890,0.844,0.873],
          "2018":[0.835,0.873,0.840],
          "Run2":[0,0,0]},
         "LP":
         {"2016":[1.090,0.995,1.055],
          "2017":[1.205,1.258,1.301],
          "2018":[1.058,1.009,1.164],
          "Run2":[0,0,0]}},
    "ZHbb":{"HP":
            {"2016":[1.027,1.014,1.049],
             "2017":[0.963,1.021,0.998],
             "2018":[0.998,1.045,1.079],
             "Run2":[0,0,0]},
            "LP":
            {"2016":[0.959,1.020,0.981],
             "2017":[1.226,1.136,1.066],
             "2018":[1.106,0.966,1.053],
             "Run2":[0,0,0]}}}

SFerr={"W":{"HP":
            {"2016":[0.038,0.039,0.066],
             "2017":[0.030,0.033,0.054],
             "2018":[0.031,0.033,0.045],
          "Run2":[0,0,0]},
            "LP":
            {"2016":[0.090,0.094,0.145],
             "2017":[0.093,0.114,0.165],
             "2018":[0.062,0.084,0.113],
             "Run2":[0,0,0]}},
       "ZHbb":{"HP":
               {"2016":[0.062,0.061,0.040],
                "2017":[0.079,0.059,0.035],
                "2018":[0.063,0.059,0.099],
                "Run2":[0,0,0]},
               "LP":
               {"2016":[0.072,0.043,0.026],
                "2017":[0.153,0.061,0.046],
                "2018":[0.147,0.164,0.069],
                "Run2":[0,0,0]}}}
lumi={"2016" : 35920.0,
    "2017" : 41530.0,
    "2018" : 59740.0,
    "Run2": 137190.0}

n = 3

for tag in tagger:
  for WP in purity:
    for year in years:
      print "******** "+tag+" "+WP+" "+year
           
#      fitSF(SF[tag][WP][year],SFerr[tag][WP][year],year,tag,WP)
      for i in range(n):
        SF[tag][WP]["Run2"][i]=SF[tag][WP]["Run2"][i]+SF[tag][WP][year][i]*lumi[year]/lumi["Run2"]
        SFerr[tag][WP]["Run2"][i]=SFerr[tag][WP]["Run2"][i]+SFerr[tag][WP][year][i]*lumi[year]/lumi["Run2"]

file2write=open("SFfit_Run2.txt",'w')
for tag in tagger:
  for WP in purity:
      print "******** "+tag+" "+WP+" Run2 "
      file2write.write(tag+" "+WP+" Run2 \n")
      slope,intercepts = fitSF(SF[tag][WP]["Run2"],SFerr[tag][WP]["Run2"],"Run2",tag,WP)
      file2write.write("slope "+str(slope)+" ; intercepts "+str(intercepts)+"\n")
file2write.close()
