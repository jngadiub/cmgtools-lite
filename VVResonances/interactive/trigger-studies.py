#nb, rescale TrimmedMass histos by factor 0.5 for 2016-RunC because of bug in the converter
import ROOT
from ROOT import *
import sys, time, os, math
from array import array
import CMS_lumi, tdrstyle
tdrstyle.setTDRStyle()
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)

CMS_lumi.writeExtraText = 1
CMS_lumi.extraText = "Preliminary"
CMS_lumi.lumi_sqrtS = "13 TeV" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)

iPeriod = 4

def getCanvas(name, lumi, iPos):

 CMS_lumi.lumi_13TeV = lumi

 if( iPos==0 ): CMS_lumi.relPosX = 0.12
 else: CMS_lumi.relPosX = 0.045
 
 H_ref = 600; 
 W_ref = 800; 
 W = W_ref
 H  = H_ref

 # references for T, B, L, R
 T = 0.08*H_ref
 B = 0.12*H_ref 
 L = 0.12*W_ref
 R = 0.04*W_ref

 canvas = ROOT.TCanvas(name,name,50,50,W,H)
 canvas.SetFillColor(0)
 canvas.SetBorderMode(0)
 canvas.SetFrameFillStyle(0)
 canvas.SetFrameBorderMode(0)
 canvas.SetLeftMargin( L/W )
 canvas.SetRightMargin( R/W )
 canvas.SetTopMargin( T/H )
 canvas.SetBottomMargin( B/H )
 canvas.SetTickx(0)
 canvas.SetTicky(0)
 
 return canvas

def getRunConfig(key):

  if 'Run2016B' in key: return '5.8 fb^{-1}','Run2016B','Run 2016B'
  if 'Run2016C' in key: return '2.6 fb^{-1}','Run2016C','Run 2016C'
  if 'Run2016D' in key: return '4.2 fb^{-1}','Run2016D','Run 2016D'
  if 'Run2016E' in key: return '4.0 fb^{-1}','Run2016E','Run 2016E'
  if 'Run2016F' in key: return '3.1 fb^{-1}','Run2016F','Run 2016F'
  if 'Run2016G' in key: return '7.6 fb^{-1}','Run2016G','Run 2016G'
  if 'Run2016H' in key: return '8.7 fb^{-1}','Run2016H','Run 2016H'
  
  if 'Run2017B' in key: return '4.8 fb^{-1}','Run2017B','Run 2017B'
  if 'Run2017C' in key: return '9.7 fb^{-1}','Run2017C','Run 2017C'
  if 'Run2017D' in key: return '4.3 fb^{-1}','Run2017D','Run 2017D'
  if 'Run2017E' in key: return '9.3 fb^{-1}','Run2017E','Run 2017E'
  if 'Run2017F' in key: return '13.5 fb^{-1}','Run2017F','Run 2017F'

  if 'Run2018A' in key: return '4.8 fb^{-1}','Run2018A','Run 2018A'
  if 'Run2018B' in key: return '9.7 fb^{-1}','Run2018B','Run 2018B'
  if 'Run2018C' in key: return '4.3 fb^{-1}','Run2018C','Run 2018C'
  if 'Run2018D' in key: return '9.3 fb^{-1}','Run2018D','Run 2018D'
  
  return 'n.a,n.a,n.a'

     
def plotAllTriggersPeriodByPeriod(all_effs,var,bins):

 os.system('mkdir trigger-studies/plotAllTriggersPeriodByPeriod')
  
 for k,effs in all_effs.iteritems():

  pt = ROOT.TPaveText(0.6378446,0.2264808,0.9974937,0.489547,"NDC")
  pt.SetTextFont(42)
  pt.SetTextSize(0.04)
  pt.SetTextAlign(12)
  pt.SetFillColor(0)
  pt.SetBorderSize(0)
  pt.SetFillStyle(0)
    
  line = TLine(bins[0],1.0,bins[len(bins)-1],1.0)
  line.SetLineColor(ROOT.kBlack)
  line.SetLineStyle(2)

  leg = ROOT.TLegend(0.15,0.73,0.82,0.895)
  leg.SetNColumns(2)
  leg.SetBorderSize(0)
  leg.SetTextSize(0.02961672)
  leg.SetTextFont(42)
  leg.SetLineColor(1)
  leg.SetLineStyle(1)
  leg.SetLineWidth(1)
  leg.SetFillColor(0)
  leg.SetFillStyle(0)
  leg.SetMargin(0.1)
  leg.SetColumnSeparation(0.2)
  
  lumi, year, text = getRunConfig(k)
  c = getCanvas('c_%s_plotAllTriggersPeriodByPeriod%s'%(var,year),lumi,0)
  c.cd()
  frame = c.DrawFrame(bins[0],0,bins[len(bins)-1],1.4)
  frame.GetYaxis().SetTitleOffset(0.9)
  frame.GetYaxis().SetTitle('Efficiency')
  frame.GetXaxis().SetTitle('Dijet invariant mass [GeV]')
  if var == 'mjet': frame.GetXaxis().SetTitle('Jet mass [GeV]')
  for i,e in enumerate(effs):
   name = e.GetName().replace('_den_clone','')
   if 'PFJet' in name and not "Trim": 
    e.SetMarkerColor(ROOT.kBlue+i)
    e.SetLineColor(ROOT.kBlue+i)
   elif "Trim" in name: 
    e.SetMarkerColor(ROOT.kOrange+i*2)
    e.SetLineColor(ROOT.kOrange+i*2)  
   else: 
    e.SetMarkerColor(ROOT.kTeal+i)
    e.SetLineColor(ROOT.kTeal+i)  
   e.Draw('same') 
   if name.split('HLT_')[-1] != 'JJ' and name.split('HLT_')[-1] != 'TrimmedMass': leg.AddEntry(e,name.split('HLT_')[-1],'LP')
   elif name.split('HLT_')[-1] == 'TrimmedMass': leg.AddEntry(e,'All substructure triggers','LP')
   else: leg.AddEntry(e,'All','LP')
  
  leg.Draw()
  line.Draw()
  text = pt.AddText(text)
  text.SetTextFont(62)
  pt.AddText("")
  if var=='mjj':
   pt.AddText("p_{T} > 200 GeV")
   pt.AddText("|#eta| < 2.4")
   pt.AddText("|#Delta#eta_{jj}| < 1.3")
   pt.AddText("m_{jet} > 55 GeV")
  else:
   pt.AddText("p_{T} > 600 GeV") 
   pt.AddText("|#eta| < 2.4")
   pt.AddText("|#Delta#eta_{jj}| < 1.3")
  pt.Draw()
  CMS_lumi.CMS_lumi(c, iPeriod, 0)
  c.cd()
  c.Update()
  c.RedrawAxis()
  frame = c.GetFrame()
  frame.Draw()
  c.SaveAs('trigger-studies/plotAllTriggersPeriodByPeriod/c_%s_plotAllTriggersPeriodByPeriod%s.png'%(var,year)) 
  c.SaveAs('trigger-studies/plotAllTriggersPeriodByPeriod/c_%s_plotAllTriggersPeriodByPeriod%s.pdf'%(var,year)) 
  c.SaveAs('trigger-studies/plotAllTriggersPeriodByPeriod/c_%s_plotAllTriggersPeriodByPeriod%s.root'%(var,year)) 

  
def plotAllTriggersForOneYear(h_total,h_passed,year,lumi,bins=[],var='mjj'):

 os.system('mkdir trigger-studies/plotAllTriggersForOneYear')
 
 effs_dummy = []
 
 for k,v in h_total.iteritems():
   print "Computing efficiency for",k,"passed =",h_passed[k].GetEntries(),"total =",v.GetEntries()
   eff = ROOT.TEfficiency(h_passed[k],v) 
   eff.SetName(k)
   effs_dummy.append(eff)
   
 c = getCanvas('c_%s_plotAllTriggersForOneYear%s'%(var,year),lumi,0)
 c.cd()
 frame = c.DrawFrame(bins[0],0,bins[len(bins)-1],1.4)
 frame.GetYaxis().SetTitleOffset(0.9)
 frame.GetYaxis().SetTitle('Efficiency')
 frame.GetXaxis().SetTitle('Dijet invariant mass [GeV]')
 if var == 'mjet': frame.GetXaxis().SetTitle('Jet mass [GeV]')
 leg = ROOT.TLegend(0.15,0.73,0.82,0.895)
 leg.SetNColumns(2)
 leg.SetBorderSize(0)
 leg.SetTextSize(0.02961672)
 leg.SetTextFont(42)
 leg.SetLineColor(1)
 leg.SetLineStyle(1)
 leg.SetLineWidth(1)
 leg.SetFillColor(0)
 leg.SetFillStyle(0)
 leg.SetMargin(0.1)
 leg.SetColumnSeparation(0.2)
 for i,e in enumerate(effs_dummy):
  e.SetMarkerColor(ROOT.kOrange+i)
  e.SetLineColor(ROOT.kOrange+i)
  e.Draw('same') 
  if e.GetName().split('HLT_')[-1] != 'JJ' and e.GetName().split('HLT_')[-1] != 'TrimmedMass': leg.AddEntry(e,e.GetName().split('HLT_')[-1],'LP')
  elif e.GetName().split('HLT_')[-1] == 'TrimmedMass': leg.AddEntry(e,'All substructure triggers','LP')
  else: leg.AddEntry(e,'All','LP')
  
 leg.Draw() 
 line = TLine(bins[0],1.0,bins[len(bins)-1],1.0)
 line.SetLineColor(ROOT.kBlack)
 line.SetLineStyle(2)
 line.Draw()
 
 CMS_lumi.CMS_lumi(c, iPeriod, 0)
 c.cd()
 c.Update()
 c.RedrawAxis()
 frame = c.GetFrame()
 frame.Draw()

 c.SaveAs('trigger-studies/plotAllTriggersForOneYear/c_%s_plotAllTriggersForOneYear%s.pdf'%(var,year))  
 c.SaveAs('trigger-studies/plotAllTriggersForOneYear/c_%s_plotAllTriggersForOneYear%s.png'%(var,year)) 
 c.SaveAs('trigger-studies/plotAllTriggersForOneYear/c_%s_plotAllTriggersForOneYear%s.root'%(var,year)) 

 for i,e in enumerate(effs_dummy):
  c = getCanvas('c_%s_plotAllTriggersForOneYear%s_%s'%(var,year,e.GetName().split('HLT_')[-1]),lumi,0)
  c.cd()
  frame = c.DrawFrame(bins[0],0,bins[len(bins)-1],1.4)
  frame.GetYaxis().SetTitleOffset(0.9)
  frame.GetYaxis().SetTitle('Efficiency')
  frame.GetXaxis().SetTitle('Dijet invariant mass [GeV]')
  if var == 'mjet': frame.GetXaxis().SetTitle('Jet mass [GeV]')
  e.SetMarkerColor(ROOT.kOrange+i)
  e.SetLineColor(ROOT.kOrange+i)  
  e.Draw('same') 
  line.Draw()
  CMS_lumi.CMS_lumi(c, iPeriod, 0)
  c.cd()
  c.Update()
  c.RedrawAxis()
  frame = c.GetFrame()
  frame.Draw()
  c.SaveAs('trigger-studies/plotAllTriggersForOneYear/c_%s_plotAllTriggersForOneYear%s_%s.pdf'%(var,year,e.GetName().split('HLT_')[-1])) 
  c.SaveAs('trigger-studies/plotAllTriggersForOneYear/c_%s_plotAllTriggersForOneYear%s_%s.png'%(var,year,e.GetName().split('HLT_')[-1])) 
  c.SaveAs('trigger-studies/plotAllTriggersForOneYear/c_%s_plotAllTriggersForOneYear%s_%s.root'%(var,year,e.GetName().split('HLT_')[-1])) 
      
def makeLegacyPlots(h_passed_2016,h_passed_2017,h_passed_2017noRunB,h_passed_2018,h_tot_2016,h_tot_2017,h_tot_2017noRunB,h_tot_2018,key,var='mjj',bins=[]):

 os.system('mkdir trigger-studies/legacyPlots')
 eff_2016 = 0
 eff_2017 = 0
 eff_2017noRunB = 0
 eff_2018 = 0
 eff_tot = 0
 h_tot_ALL = 0
 h_passed_ALL = 0
 if h_tot_2016 and h_tot_2017 and h_tot_2018:
  h_tot_ALL = h_tot_2016[key].Clone('h_tot_ALL')
  h_tot_ALL.Add(h_tot_2017[key])
  h_tot_ALL.Add(h_tot_2018[key])
  h_passed_ALL = h_passed_2016[key].Clone('h_passed_ALL')
  h_passed_ALL.Add(h_passed_2017[key])
  h_passed_ALL.Add(h_passed_2018[key])
  
 try:
  eff_2016 = ROOT.TGraphAsymmErrors()
  eff_2016.Divide(h_passed_2016[key],h_tot_2016[key],"cl=0.683 b(1,1) mode")
  #eff_2016 = ROOT.TEfficiency(h_passed_2016[key],h_tot_2016[key])
  eff_2016.SetLineColor(ROOT.kTeal+3)
  eff_2016.SetMarkerColor(ROOT.kTeal+3)
  eff_2016.SetMarkerStyle(24)
  if var=='mjj':
   h_passed_2016[key].Divide(h_tot_2016[key])
   myfit, eff_ = doFit(eff_2016,h_passed_2016[key],2000.)
 except:
  print "key",key,"not found for 2016"  
  
 try:
  #eff_2017 = ROOT.TEfficiency(h_passed_2017[key],h_tot_2017[key])
  eff_2017 = ROOT.TGraphAsymmErrors()
  eff_2017.Divide(h_passed_2017[key],h_tot_2017[key],"cl=0.683 b(1,1) mode")
  print "******* Final numbers for 2017",key,h_passed_2017[key].Integral(),h_tot_2017[key].Integral()
  eff_2017.SetLineColor(42)
  eff_2017.SetMarkerColor(42)
  eff_2017.SetMarkerStyle(21)
  if var=='mjj':
   h_passed_2017[key].Divide(h_tot_2017[key])
   myfit, eff_ = doFit(eff_2017,h_passed_2017[key],2000.)
 except:
  print "key",key,"not found for 2017" 

 try:
  #eff_2017noRunB = ROOT.TEfficiency(h_passed_2017noRunB[key],h_tot_2017noRunB[key])
  eff_2017noRunB = ROOT.TGraphAsymmErrors()
  eff_2017noRunB.Divide(h_passed_2017noRunB[key],h_tot_2017noRunB[key],"cl=0.683 b(1,1) mode")
  print "******* Final numbers for 2017 noB",key,h_passed_2017noRunB[key].Integral(),h_tot_2017noRunB[key].Integral()
  eff_2017noRunB.SetLineColor(42)
  eff_2017noRunB.SetMarkerColor(42)
  eff_2017noRunB.SetMarkerStyle(25)
  if var=='mjj':
   h_passed_2017noRunB[key].Divide(h_tot_2017noRunB[key])
   myfit, eff_ = doFit(eff_2017noRunB,h_passed_2017noRunB[key],2000.)
 except:
  print "key",key,"not found for 2017noRunB" 
  
 try:
  eff_2018 = ROOT.TGraphAsymmErrors()
  eff_2018.Divide(h_passed_2018[key],h_tot_2018[key],"cl=0.683 b(1,1) mode")
  #eff_2018 = ROOT.TEfficiency(h_passed_2018[key],h_tot_2018[key])
  eff_2018.SetLineColor(ROOT.kTeal+3)
  eff_2018.SetMarkerColor(ROOT.kTeal+3)
  eff_2018.SetMarkerStyle(20)
  if var=='mjj':
   h_passed_2018[key].Divide(h_tot_2018[key])
   myfit, eff_ = doFit(eff_2018,h_passed_2018[key],2000.)
 except:
  print "key",key,"not found for 2018" 

 try:
  eff_ALL = ROOT.TGraphAsymmErrors()
  eff_ALL.Divide(h_passed_ALL,h_tot_ALL,"cl=0.683 b(1,1) mode")
  #eff_ALL = ROOT.TEfficiency(h_passed_ALL[key],h_tot_ALL[key])
  eff_ALL.SetLineColor(ROOT.kBlack)
  eff_ALL.SetMarkerColor(ROOT.kBlack)
  eff_ALL.SetMarkerStyle(20)
  if var=='mjj':
   h_passed_ALL.Divide(h_tot_ALL)
   myfit, eff_ = doFit(eff_ALL,h_passed_ALL,2000.)
 except:
  print "NO ALL EFFICIENCY COMPUTED!"
 
 c = getCanvas('c_%s_makeLegacyPlots'%(var),'137.2 fb^{-1}',11)
 c.cd()
 frame = c.DrawFrame(bins[0],0,bins[len(bins)-1],1.4)
 frame.GetYaxis().SetTitleOffset(0.9)
 frame.GetYaxis().SetTitle('Efficiency')
 frame.GetXaxis().SetTitle('Dijet invariant mass [GeV]')
 if var == 'mjet': frame.GetXaxis().SetTitle('Jet mass [GeV]')

 leg = ROOT.TLegend(0.55,0.72,0.77,0.9)
 leg.SetBorderSize(0)
 leg.SetTextSize(0.03961672)
 leg.SetTextFont(42)
 leg.SetLineColor(1)
 leg.SetLineStyle(1)
 leg.SetLineWidth(1)
 leg.SetFillColor(0)
 leg.SetFillStyle(0)

 pt = ROOT.TPaveText(0.6,0.2264808,0.9,0.489547,"NDC")
 pt.SetTextFont(42)
 pt.SetTextSize(0.04)
 pt.SetTextAlign(12)
 pt.SetFillColor(0)
 pt.SetBorderSize(0)
 pt.SetFillStyle(0)
       
 if eff_2016:
  eff_2016.Draw('MPsame')
  leg.AddEntry(eff_2016,'2016 (35.9 fb^{-1})','LP')
 if eff_2017:
  eff_2017.Draw('MPsame')
  leg.AddEntry(eff_2017,'2017 (full, 41.5 fb^{-1})','LP')
 if eff_2017noRunB:
  eff_2017noRunB.Draw('MPsame')
  leg.AddEntry(eff_2017noRunB,'2017 (later periods, 36.7 fb^{-1})','LP')
 if eff_2018:
  eff_2018.Draw('MPsame')  
  leg.AddEntry(eff_2018,'2018 (59.7 fb^{-1})','LP')
 if eff_ALL:
  eff_ALL.Draw('MPsame') 
  leg.AddEntry(eff_ALL,'All periods','LP')

 leg.Draw()
 line = TLine(bins[0],1.0,bins[len(bins)-1],1.0)
 line.SetLineColor(ROOT.kBlack)
 line.SetLineStyle(2)
 line.Draw()

 if var=='mjj':
  pt.AddText("p_{T} > 200 GeV")
  pt.AddText("|#eta| < 2.4")
  pt.AddText("|#Delta#eta_{jj}| < 1.3")
  pt.AddText("m_{jet} > 55 GeV")
 else:
  pt.AddText("p_{T} > 600 GeV") 
  pt.AddText("|#eta| < 2.4")
  pt.AddText("|#Delta#eta_{jj}| < 1.3")
   
 pt.Draw()   
 CMS_lumi.CMS_lumi(c, iPeriod, 11)
 c.cd()
 c.Update()
 c.RedrawAxis()
 frame = c.GetFrame()
 frame.Draw()

 c.SaveAs('trigger-studies/legacyPlots/c_%s_makeLegacyPlots.pdf'%(var))    
 c.SaveAs('trigger-studies/legacyPlots/c_%s_makeLegacyPlots.png'%(var))   
 c.SaveAs('trigger-studies/legacyPlots/c_%s_makeLegacyPlots.root'%(var))   

def plotTrigger(histoName,trigList):

    for t in trigList:
     if t in histoName:
      return True
    
    return False

def sigmoid(x,p):
  
    max_eff = 1.
    try:
        return max_eff/(1+math.exp(-p[1]*(x[0]-p[0])))
    except:
        print "Overflow error for p[1] = %f p[0] =%f x[0] =%f "%(p[1],p[0],x[0])
        print "e^X, X = " ,-p[1]*(x[0]-p[0])
        return max_eff/(1+math.exp(-1.04140e-02*(x[0]-800)))
        # if -p[1]*(x[0]-p[0])< 0.: return 1
#         else: return 0
    # return max_eff/(p[1]+math.exp(-p[0]*x[0]))
    # return sigmoid
    # k == 1/sigma*Ethres, x0 = EThreshold

def doFit(eff,histtmp,end):
  fit_x3 = ROOT.TF1(histtmp.GetName()+"_fit", sigmoid, 0., 2000., 2)
  fit_x3.SetParameters(1.0,0.01)
  start = histtmp.GetBinCenter(histtmp.FindFirstBinAbove(0.75))
  
  print "Starting point = %s" %start
  st = eff.Fit(fit_x3, "+S","",start,end)
  status = st.Status()
  fit = eff.GetFunction(histtmp.GetName()+"_fit")
  mass = fit.GetX(0.9900, start, end, 1.E-10, 100, False)
  print "99 percent efficient at mass:"
  print mass
  print "######"
  ROOT.gStyle.SetOptStat(0)
  del fit_x3
  return fit, mass
           
if __name__ == '__main__':

 binsy = [0,3,6,10,16,23,31,40,50,61,74,88,103,119,137,156,176,197,220,244,270,296,325,354,386,419,453,489,526,565,606,649,693,740,788,838,890,944,1000,1058,1118,1181,1246,1313,1383,1455,1530,1607,1687,1770,1856,1945,2037,2132,2231,2332,2438,2546,2659,2775,2895,3019,3147,3279,3416,3558,3704,3854,4010,4171,4337,4509,4686,4869,5058,5253,5455,5663,5877,6099,6328,6564,7000]

 files = ['/eos/cms/store/cmst3/group/exovv/VVtuple/FullRun2VVVHNtuple/2016_new/JetHT_Run2016B_17Jul2018.root','/eos/cms/store/cmst3/group/exovv/VVtuple/FullRun2VVVHNtuple/2016_new/JetHT_Run2016C_17Jul2018.root',
          '/eos/cms/store/cmst3/group/exovv/VVtuple/FullRun2VVVHNtuple/2016_new/JetHT_Run2016D_17Jul2018.root','/eos/cms/store/cmst3/group/exovv/VVtuple/FullRun2VVVHNtuple/2016_new/JetHT_Run2016E_17Jul2018.root',
	  '/eos/cms/store/cmst3/group/exovv/VVtuple/FullRun2VVVHNtuple/2016_new/JetHT_Run2016F_17Jul2018.root','/eos/cms/store/cmst3/group/exovv/VVtuple/FullRun2VVVHNtuple/2016_new/JetHT_Run2016G_17Jul2018.root',
	  '/eos/cms/store/cmst3/group/exovv/VVtuple/FullRun2VVVHNtuple/2016_new/JetHT_Run2016H_17Jul2018.root',
	  '/eos/cms/store/cmst3/group/exovv/VVtuple/FullRun2VVVHNtuple/2017/JetHT_Run2017B_31Mar2018.root', '/eos/cms/store/cmst3/group/exovv/VVtuple/FullRun2VVVHNtuple/2017/JetHT_Run2017C_31Mar2018.root',
	  '/eos/cms/store/cmst3/group/exovv/VVtuple/FullRun2VVVHNtuple/2017/JetHT_Run2017D_31Mar2018.root', '/eos/cms/store/cmst3/group/exovv/VVtuple/FullRun2VVVHNtuple/2017/JetHT_Run2017E_31Mar2018.root',
	  '/eos/cms/store/cmst3/group/exovv/VVtuple/FullRun2VVVHNtuple/2017/JetHT_Run2017F_31Mar2018.root',
          '/eos/cms/store/cmst3/group/exovv/VVtuple/FullRun2VVVHNtuple/2018/JetHT_Run2018A_17Sep2018.root','/eos/cms/store/cmst3/group/exovv/VVtuple/FullRun2VVVHNtuple/2018/JetHT_Run2018B_17Sep2018.root',
	  '/eos/cms/store/cmst3/group/exovv/VVtuple/FullRun2VVVHNtuple/2018/JetHT_Run2018C_17Sep2018.root','/eos/cms/store/cmst3/group/exovv/VVtuple/FullRun2VVVHNtuple/2018/JetHT_Run2018D_17Sep2018_part1.root',
	  '/eos/cms/store/cmst3/group/exovv/VVtuple/FullRun2VVVHNtuple/2018/JetHT_Run2018D_17Sep2018_part2.root','/eos/cms/store/cmst3/group/exovv/VVtuple/FullRun2VVVHNtuple/2018/JetHT_Run2018D_17Sep2018_part3.root'  
 ]

 files = ['/eos/cms/store/cmst3/group/exovv/VVtuple/FullRun2VVVHNtuple/2016_new/SingleMuon_Run2016B_17Jul2018.root', '/eos/cms/store/cmst3/group/exovv/VVtuple/FullRun2VVVHNtuple/2016_new/SingleMuon_Run2016C_17Jul2018.root',
          '/eos/cms/store/cmst3/group/exovv/VVtuple/FullRun2VVVHNtuple/2016_new/SingleMuon_Run2016D_17Jul2018.root', '/eos/cms/store/cmst3/group/exovv/VVtuple/FullRun2VVVHNtuple/2016_new/SingleMuon_Run2016E_17Jul2018.root',
	  '/eos/cms/store/cmst3/group/exovv/VVtuple/FullRun2VVVHNtuple/2016_new/SingleMuon_Run2016F_17Jul2018.root', '/eos/cms/store/cmst3/group/exovv/VVtuple/FullRun2VVVHNtuple/2016_new/SingleMuon_Run2016G_17Jul2018.root',
	  '/eos/cms/store/cmst3/group/exovv/VVtuple/FullRun2VVVHNtuple/2016_new/SingleMuon_Run2016H_17Jul2018.root',
	  '/eos/cms/store/cmst3/group/exovv/VVtuple/FullRun2VVVHNtuple/2017/SingleMuon_Run2017B_31Mar2018.root', '/eos/cms/store/cmst3/group/exovv/VVtuple/FullRun2VVVHNtuple/2017/SingleMuon_Run2017C_31Mar2018.root',
	  '/eos/cms/store/cmst3/group/exovv/VVtuple/FullRun2VVVHNtuple/2017/SingleMuon_Run2017D_31Mar2018.root', '/eos/cms/store/cmst3/group/exovv/VVtuple/FullRun2VVVHNtuple/2017/SingleMuon_Run2017E_31Mar2018.root',
	  '/eos/cms/store/cmst3/group/exovv/VVtuple/FullRun2VVVHNtuple/2017/SingleMuon_Run2017F_31Mar2018.root',
	  '/eos/cms/store/cmst3/group/exovv/VVtuple/FullRun2VVVHNtuple/2018/SingleMuon_Run2018A_17Sep2018.root', '/eos/cms/store/cmst3/group/exovv/VVtuple/FullRun2VVVHNtuple/2018/SingleMuon_Run2018B_17Sep2018.root', 
	  '/eos/cms/store/cmst3/group/exovv/VVtuple/FullRun2VVVHNtuple/2018/SingleMuon_Run2018C_17Sep2018.root', '/eos/cms/store/cmst3/group/exovv/VVtuple/FullRun2VVVHNtuple/2018/SingleMuon_Run2018D_22Jan2019.root', 
 ]
 trigNames16 = ["HLT_PFHT800",
                "HLT_PFJet450",
		"HLT_PFHT650_WideJetMJJ900DEtaJJ1p5",
		"HLT_AK8PFJet360_TrimMass30","HLT_AK8PFHT700_TrimR0p1PT0p03Mass50",
		"HLT_JJ","HLT_TrimmedMass"]	

 trigNames16H = ["HLT_PFHT900",
                 "HLT_PFJet450",
		 "HLT_AK8PFJet450",
		 "HLT_PFHT650_WideJetMJJ900DEtaJJ1p5",
		 "HLT_AK8PFJet360_TrimMass30","HLT_AK8PFHT700_TrimR0p1PT0p03Mass50",
		 "HLT_JJ","HLT_TrimmedMass"]
				   
 trigNames17 = ["HLT_PFHT1050",
                "HLT_AK8PFJet500",
		"HLT_AK8PFJet360_TrimMass30",
		"HLT_AK8PFHT750_TrimMass50",
		"HLT_JJ","HLT_TrimmedMass"]


 trigNames17F = ["HLT_PFHT1050",
                "HLT_AK8PFJet500",
		"HLT_AK8PFJet400_TrimMass30",
		"HLT_AK8PFHT800_TrimMass50",
		"HLT_JJ","HLT_TrimmedMass"]
		
 trigNames17B = ["HLT_PFHT1050" ,"HLT_AK8PFJet500", "HLT_JJ", "HLT_TrimmedMass"]

 trigNames18 = ["HLT_PFHT1050" ,
                "HLT_AK8PFJet500",
		"HLT_AK8PFJet400_TrimMass30",
		"HLT_AK8PFHT800_TrimMass50",
		"HLT_JJ","HLT_TrimmedMass"]

 all_triggers = trigNames16+trigNames16H+trigNames17+trigNames17B+trigNames18
 all_triggers = list(dict.fromkeys(all_triggers))
 print(all_triggers) 
		        		  		  
 #efficiencies of all triggers period by period
 effs_mjj = {}
 effs_mjet = {}

 #efficiencies of all triggers for the full year
 htot_passed_mjj_2016 = {}
 htot_total_mjj_2016 = {}
 htot_passed_mjet_2016 = {}
 htot_total_mjet_2016 = {}
 htot_passed_mjj_2017 = {}
 htot_total_mjj_2017 = {}
 htot_passed_mjet_2017 = {}
 htot_total_mjet_2017 = {}
 htot_passed_mjj_2017noRunB = {}
 htot_total_mjj_2017noRunB = {}
 htot_passed_mjet_2017noRunB = {}
 htot_total_mjet_2017noRunB = {}
 htot_passed_mjj_2018 = {}
 htot_total_mjj_2018 = {}
 htot_passed_mjet_2018 = {}
 htot_total_mjet_2018 = {}
 
 dummy = ROOT.TFile.Open('dummy.root','RECREATE')
 
 for f in files:
  
  effs_mjj[f.replace('.root','')] = []
  effs_mjet[f.replace('.root','')] = []
 
  tf = ROOT.TFile.Open(f)
  td = tf.Get('Trigger')
 
  for trig in all_triggers:
 
   hname = 'mjj_'+trig
   plotTrigger_ = False   
   if 'Run2016' in f and not 'Run2016H' in f: plotTrigger_ = plotTrigger(hname,trigNames16)
   if 'Run2016H' in f: plotTrigger_ = plotTrigger(hname,trigNames16H)
   if 'Run2017B' in f: plotTrigger_ = plotTrigger(hname,trigNames17B)
   if 'Run2017F' in f or 'Run2017E' in f: plotTrigger_ = plotTrigger(hname,trigNames17F)
   if 'Run2017' in f and not 'Run2017B' in f and not 'Run2017F' in f and not 'Run2017E' in f: plotTrigger_ = plotTrigger(hname,trigNames17)
   if 'Run2018' in f: plotTrigger_ = plotTrigger(hname,trigNames18)
         
   if not plotTrigger_: continue   
    
   dummy.cd()
   if not hname in htot_total_mjj_2016.keys() and 'Run2016' in f: 
    #print "Addind new 2016 mjj histo:",hname
    htot_total_mjj_2016[hname] = ROOT.TH1F('htot_total_'+hname+'_2016','htot_total_'+hname+'_2016',len(binsy)-1,array('f',binsy))
    htot_passed_mjj_2016[hname] = ROOT.TH1F('htot_passed_'+hname+'_2016','htot_passed_'+hname+'_2016',len(binsy)-1,array('f',binsy))
   if not hname in htot_total_mjj_2017.keys() and 'Run2017' in f: 
    #print "Addind new 2017 mjj histo:",hname
    htot_total_mjj_2017[hname] = ROOT.TH1F('htot_total_'+hname+'_2017','htot_total_'+hname+'_2017',len(binsy)-1,array('f',binsy))
    htot_passed_mjj_2017[hname] = ROOT.TH1F('htot_passed_'+hname+'_2017','htot_passed_'+hname+'_2017',len(binsy)-1,array('f',binsy))
   if not hname in htot_total_mjj_2017noRunB.keys() and 'Run2017' in f and not 'Run2017B' in f: 
    #print "Addind new 2017noRunB mjj histo:",hname
    htot_total_mjj_2017noRunB[hname] = ROOT.TH1F('htot_total_'+hname+'_2017noRunB','htot_total_'+hname+'_2017noRunB',len(binsy)-1,array('f',binsy))
    htot_passed_mjj_2017noRunB[hname] = ROOT.TH1F('htot_passed_'+hname+'_2017noRunB','htot_passed_'+hname+'_2017noRunB',len(binsy)-1,array('f',binsy))
   if not hname in htot_total_mjj_2018.keys() and 'Run2018' in f: 
    #print "Addind new 2018 mjj histo:",hname
    htot_total_mjj_2018[hname] = ROOT.TH1F('htot_total_'+hname+'_2018','htot_total_'+hname+'_2018',len(binsy)-1,array('f',binsy))
    htot_passed_mjj_2018[hname] = ROOT.TH1F('htot_passed_'+hname+'_2018','htot_passed_'+hname+'_2018',len(binsy)-1,array('f',binsy))

   histo_num = td.Get(hname+"_num")
   histo_den = td.Get(hname+"_den")
   if histo_num and histo_den:
      
    if 'Run2016' in f:
     htot_total_mjj_2016[hname].Add(histo_den)   
     htot_passed_mjj_2016[hname].Add(histo_num)   
    if 'Run2017' in f:
     htot_total_mjj_2017[hname].Add(histo_den)   
     htot_passed_mjj_2017[hname].Add(histo_num)   
    if 'Run2017' in f and not 'Run2017B' in f:
     htot_total_mjj_2017noRunB[hname].Add(histo_den)   
     htot_passed_mjj_2017noRunB[hname].Add(histo_num)  
    if 'Run2018' in f:
     htot_total_mjj_2018[hname].Add(histo_den)    
     htot_passed_mjj_2018[hname].Add(histo_num)   
   
    if hname == 'mjj_HLT_JJ': print "Computing efficiency for period",f,"histo",hname,"passed = ",histo_num.GetEntries(),"total =",histo_den.GetEntries()
    if histo_den.GetEntries() != 0: effs_mjj[f.replace('.root','')].append( ROOT.TEfficiency(histo_num,histo_den) )

    histo_num.Delete()
    histo_den.Delete()
      
   hname = 'mjet1_'+trig
   if not hname in htot_total_mjet_2016.keys() and 'Run2016' in f:   
    #print "Addind new 2016 mjet histo:",hname
    htot_total_mjet_2016[hname] = ROOT.TH1F('htot_total_'+hname+'_2016','htot_total_'+hname+'_2016',50,0,250)
    htot_passed_mjet_2016[hname] = ROOT.TH1F('htot_passed_'+hname+'_2016','htot_passed_'+hname+'_2016',50,0,250)
   if not hname in htot_total_mjet_2017.keys() and 'Run2017' in f:
    #print "Addind new 2017 mjet histo:",hname
    htot_total_mjet_2017[hname] = ROOT.TH1F('htot_total_'+hname+'_2017','htot_total_'+hname+'_2017',50,0,250)
    htot_passed_mjet_2017[hname] = ROOT.TH1F('htot_passed_'+hname+'_2017','htot_passed_'+hname+'_2017',50,0,250)
   if not hname in htot_total_mjet_2017noRunB.keys() and 'Run2017' in f and not 'Run2017B' in f: 
    #print "Addind new 2017noRunB mjet histo:",hname
    htot_total_mjet_2017noRunB[hname] = ROOT.TH1F('htot_total_'+hname+'_2017noRunB','htot_total_'+hname+'_2017noRunB',50,0,250)
    htot_passed_mjet_2017noRunB[hname] = ROOT.TH1F('htot_passed_'+hname+'_2017noRunB','htot_passed_'+hname+'_2017noRunB',50,0,250)
   if not hname in htot_total_mjet_2018.keys() and 'Run2018' in f: 
    #print "Addind new 2018 mjet histo:",hname
    htot_total_mjet_2018[hname] = ROOT.TH1F('htot_total_'+hname+'_2018','htot_total_'+hname+'_2018',50,0,250)
    htot_passed_mjet_2018[hname] = ROOT.TH1F('htot_passed_'+hname+'_2018','htot_passed_'+hname+'_2018',50,0,250)
   
   histo_num = td.Get(hname+"_num")
   histo_den = td.Get(hname+"_den")
   if histo_num and histo_den:
    if 'Run2016' in f:
     htot_total_mjet_2016[hname].Add(histo_den)   
     htot_passed_mjet_2016[hname].Add(histo_num)   
    if 'Run2017' in f:
     htot_total_mjet_2017[hname].Add(histo_den)   
     htot_passed_mjet_2017[hname].Add(histo_num)   
    if 'Run2017' in f and not 'Run2017B' in f:
     htot_total_mjet_2017noRunB[hname].Add(histo_den)   
     htot_passed_mjet_2017noRunB[hname].Add(histo_num)  
    if 'Run2018' in f:
     htot_total_mjet_2018[hname].Add(histo_den)    
     htot_passed_mjet_2018[hname].Add(histo_num)  
    
    if hname == 'mjet1_HLT_TrimmedMass':  print "Computing efficiency for period",f,"histo",hname,"passed = ",histo_num.GetEntries(),"total =",histo_den.GetEntries()
    if histo_den.GetEntries() != 0: effs_mjet[f.replace('.root','')].append( ROOT.TEfficiency(histo_num,histo_den) )
      
  tf.Close()
 
 print "****************************************************"
 plotAllTriggersForOneYear(htot_total_mjj_2016,htot_passed_mjj_2016,'2016','35.9 fb^{-1}',[489,2546],'mjj')
 plotAllTriggersForOneYear(htot_total_mjet_2016,htot_passed_mjet_2016,'2016','35.9 fb^{-1}',[0,250],'mjet')
 plotAllTriggersForOneYear(htot_total_mjj_2017,htot_passed_mjj_2017,'2017','41.5 fb^{-1}',[489,2546],'mjj')
 plotAllTriggersForOneYear(htot_total_mjet_2017,htot_passed_mjet_2017,'2017','41.5 fb^{-1}',[0,250],'mjet')
 plotAllTriggersForOneYear(htot_total_mjj_2018,htot_passed_mjj_2018,'2018','59.7 fb^{-1}',[489,2546],'mjj')
 plotAllTriggersForOneYear(htot_total_mjet_2018,htot_passed_mjet_2018,'2018','59.7 fb^{-1}',[0,250],'mjet')
  
 makeLegacyPlots(htot_passed_mjj_2016,htot_passed_mjj_2017,htot_passed_mjj_2017noRunB,htot_passed_mjj_2018,
                 htot_total_mjj_2016,htot_total_mjj_2017,htot_total_mjj_2017noRunB,htot_total_mjj_2018,'mjj_HLT_JJ','mjj',[489,2546])

 makeLegacyPlots(htot_passed_mjet_2016,htot_passed_mjet_2017,htot_passed_mjet_2017noRunB,htot_passed_mjet_2018,
                 htot_total_mjet_2016,htot_total_mjet_2017,htot_total_mjet_2017noRunB,htot_total_mjet_2018,'mjet1_HLT_TrimmedMass','mjet',[0,250])

		 
 plotAllTriggersPeriodByPeriod(effs_mjj,'mjj',[489,2546])
 plotAllTriggersPeriodByPeriod(effs_mjet,'mjet',[0,250])

 os.system('rm dummy.root')
