#python prefiring-uncs.py
#python prefiring-uncs.py --vbf
#python prefiring-uncs.py --ivbf
#python prefiring-uncs.py --ivbf --vbf
#python prefiring-uncs.py && python prefiring-uncs.py --vbf && python prefiring-uncs.py --ivbf && python prefiring-uncs.py --ivbf --vbf
import ROOT
from ROOT import *
import os, pickle, time, sys, optparse, json
from array import array
import numpy as np
import CMS_lumi, tdrstyle
tdrstyle.setTDRStyle()
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)
ROOT.gROOT.SetBatch(True)

def fit_graphs(uncsUp_all,masses,label):

 parameters = {}
 
 for s in uncsUp_all.keys():

  graph = ROOT.TGraph(len(masses),masses,uncsUp_all[s])
  graph.SetMarkerColor(ROOT.kBlack)
  graph.SetLineColor(ROOT.kBlack)
  graph.SetMarkerStyle(20)
	   
  func = ROOT.TF1("func_%s_%s"%(s,label),"[0]*x+[1]",1.2,8)
	
  c = ROOT.TCanvas("cfit_%s_%s"%(s,label),"cfit_%s"%s)
  c.cd()
  graph.Fit(func)
  graph.Draw('ALP')
  pt = ROOT.TPaveText(0.52,0.79,0.90,0.89,"NDC")
  pt.SetTextFont(62)
  pt.SetTextSize(0.04)
  pt.SetTextAlign(12)
  pt.SetFillColor(0)
  pt.SetBorderSize(0)
  pt.SetFillStyle(0)   
  pt.AddText(s)
  pt.AddText("y = %.3f*x + %.3f"%(func.GetParameter(0),func.GetParameter(1)))
  pt.Draw()
  
  c.SaveAs("cfit_%s_%s.pdf"%(s,label))

  parameters[s] = [func.GetParameter(0),func.GetParameter(1)]
 
 return parameters
 
def tree_draw(indir,infile,cut,add_weights,lumi):

	  if not os.path.isfile(indir+"/"+infile): return [None,None,None,None]
      
	  fpck=open(indir+"/"+infile.replace('.root','.pck'))
	  dpck=pickle.load(fpck)
	  weightinv = float(dpck['events'])
	
	  tf = ROOT.TFile.Open(indir+"/"+infile,'READ')
	  tree = tf.AnalysisTree
	  ROOT.gROOT.cd()

	  htempNW = ROOT.gROOT.FindObject("htempNW%s"%indir)
	  htemp = ROOT.gROOT.FindObject("htemp%s"%indir)
	  htempUp = ROOT.gROOT.FindObject("htempUp%s"%indir)
	  htempDown = ROOT.gROOT.FindObject("htempDown%s"%indir)
	  if htempNW: htemp.Delete()
	  if htemp: htemp.Delete()
	  if htempUp: htempUp.Delete()
	  if htempDown: htempDown.Delete()
  
	  #print "Draw histo for file",f
  
	  genWeight = 'genWeight'
	  if indir=='2017' or indir=='2018': genWeight = 'genWeight_LO'

	  tree.Draw("jj_LV_mass>>htempNW%s(1000,0,10000)"%indir, '(%s*xsec*puWeight*%.10f)*'%(add_weights,lumi*1./weightinv)+cut);
	  tree.Draw("jj_LV_mass>>htemp%s(1000,0,10000)"%indir, '(%s*xsec*puWeight*L1prefWeight*%.10f)*'%(add_weights,lumi*1./weightinv)+cut);
	  tree.Draw("jj_LV_mass>>htempUp%s(1000,0,10000)"%indir, '(%s*xsec*puWeight*L1prefWeightUp*%.10f)*'%(add_weights,lumi*1./weightinv)+cut);
	  tree.Draw("jj_LV_mass>>htempDown%s(1000,0,10000)"%indir, '(%s*xsec*puWeight*L1prefWeightDown*%.10f)*'%(add_weights,lumi*1./weightinv)+cut);

	  htempNW = ROOT.gROOT.FindObject("htempNW%s"%indir)
	  htemp = ROOT.gROOT.FindObject("htemp%s"%indir)
	  htempUp = ROOT.gROOT.FindObject("htempUp%s"%indir)
	  htempDown = ROOT.gROOT.FindObject("htempDown%s"%indir)
	  
	  tf.Close()
	  
	  return  [htempNW, htemp, htempUp, htempDown]
	  
def plot_graphs(indir,ctx,add_weights,signals,label,ymax):

	cut_vv='*'.join([ctx.cuts['common_VV'],ctx.cuts['acceptance']])
	cut_vbf='*'.join([ctx.cuts['common_VBF'],ctx.cuts['acceptance']])

	colors = [15,12,40,9,42,46,8,30]
	styles = [20,24,21,25,22,26,23,32]


	uncs = {}

	for s in signals:

	 uncs[s] = {}
 
	 cut = cut_vv
	 if isvbf_channel: cut = cut_vbf
 
	 print s
 
	 dir_loop = indir
	 if indir == 'Run2': dir_loop = '2016'
	 for f in os.listdir(dir_loop):
 
	  if not 'root' in f: continue
	  if not s in f: continue
	  if not 'VBF' in s and 'VBF' in f: continue
  
	  mass = float(f.replace('.root','').split('_')[-1])

	  if indir!='Run2': histos = tree_draw(indir,f,cut,add_weights,1)
	  else:
	   histos = tree_draw('2016',f,cut,add_weights,ctx.lumi['2016'])
	   histos_17 = tree_draw('2017',f,cut,add_weights,ctx.lumi['2017'])
	   histos_18 = tree_draw('2018',f,cut,add_weights,ctx.lumi['2018'])
	   if histos_17[0] == None or histos_18[0] == None:
	    print "Breaking the loop!!",f
	    break
	   histoUp16 = histos[2].Clone("histoUp16")
	   histoUp16.Add(histos_17[1])
	   histoUp16.Add(histos_18[1])
	   histoUp17 = histos_17[2].Clone("histoUp17")
	   histoUp17.Add(histos[1])
	   histoUp17.Add(histos_18[1])
	   for i,h in enumerate(histos):
	    h.Add(histos_17[i])
	    h.Add(histos_18[i])	                 
	  nw = histos[0].Integral()
	  centr = histos[1].Integral()
	  up = histos[2].Integral()
	  #down = histos[3].Integral()
	  up17 = centr
	  if indir=='Run2':
	   up = histoUp16.Integral()
	   up17 = histoUp17.Integral()	  
	
	  if centr!=0: uncs[s][mass] = [centr/nw,(centr-up)/centr,(centr-up17)/centr]
	
	graphs_eff = {}
	graphs_uncUp = {}
	graphs_uncUp17 = {}
	effs_all = {}
	uncsUp_all = {}
	uncsUp17_all = {}
	i = 0
	for s,v in uncs.iteritems():
 
	  print s
   
	  masses = array('d',[])
	  effs = array('d',[])
	  uncsUp = array('d',[])
	  uncsUp17 = array('d',[])
	  
	  for m,u in sorted(v.items(), key=lambda item: item[0]): #v.iteritems():
	   if m < 1200: continue
	   print "   *",m,u[0],u[1],u[2]
	   masses.append(float(m)/1000.)
	   effs.append((1-u[0])*100.)
	   uncsUp.append(u[1]*100.)
	   uncsUp17.append(u[2]*100.)
  
	  graphs_eff[s] = ROOT.TGraph(len(masses),masses,effs)
	  graphs_eff[s].SetName("graphEff_%s"%s)
	  graphs_eff[s].SetMarkerColor(colors[i])
	  graphs_eff[s].SetLineColor(colors[i])
	  graphs_eff[s].SetMarkerStyle(styles[i])
	  graphs_uncUp[s] = ROOT.TGraph(len(masses),masses,uncsUp)
	  graphs_uncUp[s].SetName("graphUncUp_%s"%s)
	  graphs_uncUp[s].SetMarkerColor(colors[i])
	  graphs_uncUp[s].SetMarkerStyle(styles[i])
	  graphs_uncUp[s].SetLineColor(colors[i])
	  graphs_uncUp17[s] = ROOT.TGraph(len(masses),masses,uncsUp17)
	  graphs_uncUp17[s].SetName("graphUncUp17_%s"%s)
	  graphs_uncUp17[s].SetMarkerColor(colors[i])
	  graphs_uncUp17[s].SetMarkerStyle(styles[i])
	  graphs_uncUp17[s].SetLineColor(colors[i])
	
	  effs_all[s] = effs
	  uncsUp_all[s] =uncsUp
	  uncsUp17_all[s] =uncsUp17
	  i+=1
	    
	leg = ROOT.TLegend(0.52,0.59,0.90,0.89) #0.58,0.96
	leg.SetTextSize(0.04)
	leg.SetBorderSize(0)
	leg.SetLineColor(1)
	leg.SetLineStyle(1)
	leg.SetLineWidth(1)
	leg.SetFillColor(0)
	leg.SetFillStyle(0)
	leg.SetTextFont(42)

	pt = ROOT.TPaveText(0.2,0.8,0.5,0.9,"NDC")
	pt.SetTextFont(62)
	pt.SetTextSize(0.04)
	pt.SetTextAlign(12)
	pt.SetFillColor(0)
	pt.SetBorderSize(0)
	pt.SetFillStyle(0)   
	if isvbf_channel: pt.AddText("VBF selections")
	else: pt.AddText("ggF/DY selections")
	pt.AddText(indir)
   
	mg_eff = ROOT.TMultiGraph("mg_eff","mg_eff")
	mg_uncUp = ROOT.TMultiGraph("mg_uncUp","mg_uncUp")
	mg_uncUp17 = ROOT.TMultiGraph("mg_uncUp17","mg_uncUp17")
  
	for s in graphs_eff.keys():
 
	 mg_eff.Add(graphs_eff[s])  
	 mg_uncUp.Add(graphs_uncUp[s])   
	 mg_uncUp17.Add(graphs_uncUp17[s])     

	 leg.AddEntry(graphs_eff[s],s,'LP')   

	c_eff = ROOT.TCanvas("c_eff","c_eff")
	c_eff.cd()
	mg_eff.Draw("ALP")
	mg_eff.SetMinimum(0)
	mg_eff.SetMaximum(ymax[0])
	mg_eff.GetXaxis().SetTitle('m_{X} [TeV]')
	mg_eff.GetYaxis().SetTitle('Prefiring impact [%]')
	leg.Draw()
	pt.Draw()
	c_eff.SaveAs("prefiring-impact-%s.pdf"%label)
 
	c_uncUp = ROOT.TCanvas("c_uncUp","c_uncUp")
	c_uncUp.cd()
	mg_uncUp.Draw("ALP")
	mg_uncUp.SetMinimum(0)
	mg_uncUp.SetMaximum(ymax[1]) 
	mg_uncUp.GetXaxis().SetTitle('m_{X} [TeV]')
	mg_uncUp.GetYaxis().SetTitle('Prefiring uncertainty [%]')
	if indir=='Run2': mg_uncUp.GetYaxis().SetTitle('2016 Prefiring uncertainty [%]')
	leg.Draw()
	pt.Draw()
	c_uncUp.SaveAs("prefiring-uncs-%s.pdf"%label)

	if indir=='Run2':
	 c_uncUp17 = ROOT.TCanvas("c_uncUp17","c_uncUp17")
	 c_uncUp17.cd()
	 mg_uncUp17.Draw("ALP")
	 mg_uncUp17.SetMinimum(0)
	 mg_uncUp17.SetMaximum(ymax[1]) 
	 mg_uncUp17.GetXaxis().SetTitle('m_{X} [TeV]')
	 mg_uncUp17.GetYaxis().SetTitle('2017 Prefiring uncertainty [%]')
	 leg.Draw()
	 pt.Draw()
	 c_uncUp17.SaveAs("prefiring-uncs17-%s.pdf"%label)
	
	return effs_all,uncsUp_all,uncsUp17_all,masses

def prefiring_background(indir,sample,ctx,add_weights):

 cut_vv='*'.join([ctx.cuts['common_VV'],ctx.cuts['acceptance']])
 cut_vbf='*'.join([ctx.cuts['common_VBF'],ctx.cuts['acceptance']])
 cut = cut_vv
 if isvbf_channel: cut = cut_vbf

 histos = []
 FIRST = True
 
 for f in os.listdir(indir):
 
  if not sample in f: continue
  if not 'root' in f: continue
  
  print f
  
  histosTmp = tree_draw(indir,f,cut,add_weights,ctx.lumi[indir])
  if FIRST:
   for h in histosTmp:
    histos.append(h.Clone(sample+"_"+h.GetName()))
    FIRST = False
  else:
   for h in range(len(histos)):
    histos[h].Add(histosTmp[h])

 return histos
	       
parser = optparse.OptionParser()
parser.add_option("--vbf","--vbf",dest="doVBF",action="store_true", help="Run VBF selections",default=False)
parser.add_option("--ivbf","--ivbf",dest="isVBF",action="store_true", help="Use VBF signals",default=False)
(options,args) = parser.parse_args()
 
isvbf_channel=options.doVBF
isvbf_signal=options.isVBF

import cuts
ctx  = cuts.cuts("init_VV_VH.json","2016,2017,2018","dijetbins_random",True)

histosTT_2016 = prefiring_background('2016','TT_Mtt',ctx,'TopPTWeight*genWeight')
histosTT_2017 = prefiring_background('2017','TT_Mtt',ctx,'TopPTWeight*genWeight')
histosTT_2018 = prefiring_background('2018','TT_Mtt',ctx,'TopPTWeight*genWeight')
histosTT_Run2 = [] 
for h in histosTT_2016: histosTT_Run2.append(h.Clone(h.GetName().replace('16','Run2')))
for i,h in enumerate(histosTT_2017): histosTT_Run2[i].Add(h)
for i,h in enumerate(histosTT_2018): histosTT_Run2[i].Add(h)
histosTT_Run2_UncUp16 = histosTT_2016[2].Clone('TT_Run2_UncUp16')
histosTT_Run2_UncUp16.Add(histosTT_2017[1])
histosTT_Run2_UncUp16.Add(histosTT_2018[1])
histosTT_Run2_UncUp17 = histosTT_2017[2].Clone('TT_Run2_UncUp17')
histosTT_Run2_UncUp17.Add(histosTT_2016[1])
histosTT_Run2_UncUp17.Add(histosTT_2018[1])

histosWJets_2016 = prefiring_background('2016','WJetsToQQ',ctx,'kfactor*genWeight')
histosWJets_2017 = prefiring_background('2017','WJetsToQQ',ctx,'kfactor*genWeight')
histosWJets_2018 = prefiring_background('2018','WJetsToQQ',ctx,'kfactor*genWeight')
histosWJets_Run2 = [] 
for h in histosWJets_2016: histosWJets_Run2.append(h.Clone(h.GetName().replace('16','Run2')))
for i,h in enumerate(histosWJets_2017): histosWJets_Run2[i].Add(h)
for i,h in enumerate(histosWJets_2018): histosWJets_Run2[i].Add(h)
histosWJets_Run2_UncUp16 = histosWJets_2016[2].Clone('WJets_Run2_UncUp16')
histosWJets_Run2_UncUp16.Add(histosWJets_2017[1])
histosWJets_Run2_UncUp16.Add(histosWJets_2018[1])
histosWJets_Run2_UncUp17 = histosWJets_2017[2].Clone('WJets_Run2_UncUp17')
histosWJets_Run2_UncUp17.Add(histosWJets_2016[1])
histosWJets_Run2_UncUp17.Add(histosWJets_2018[1])

histosZJets_2016 = prefiring_background('2016','ZJetsToQQ',ctx,'kfactor*genWeight')
histosZJets_2017 = prefiring_background('2017','ZJetsToQQ',ctx,'kfactor*genWeight')
histosZJets_2018 = prefiring_background('2018','ZJetsToQQ',ctx,'kfactor*genWeight')
histosZJets_Run2 = [] 
for h in histosZJets_2016: histosZJets_Run2.append(h.Clone(h.GetName().replace('16','Run2')))
for i,h in enumerate(histosZJets_2017): histosZJets_Run2[i].Add(h)
for i,h in enumerate(histosZJets_2018): histosZJets_Run2[i].Add(h)
histosZJets_Run2_UncUp16 = histosZJets_2016[2].Clone('ZJets_Run2_UncUp16')
histosZJets_Run2_UncUp16.Add(histosZJets_2017[1])
histosZJets_Run2_UncUp16.Add(histosZJets_2018[1])
histosZJets_Run2_UncUp17 = histosZJets_2017[2].Clone('ZJets_Run2_UncUp17')
histosZJets_Run2_UncUp17.Add(histosZJets_2016[1])
histosZJets_Run2_UncUp17.Add(histosZJets_2018[1])

signals_ = []
if isvbf_signal: signals_ = ['VBF_BulkGravToWW','VBF_BulkGravToZZ','VBF_RadionToWW','VBF_RadionToZZ','VBF_ZprimeToWW','VBF_ZprimeToZh','VBF_WprimeToWZ','VBF_WprimeToWh']
else: signals_ = ['BulkGravToWW','BulkGravToZZ','RadionToWW','RadionToZZ','ZprimeToWW','ZprimeToZh','WprimeToWZ','WprimeToWh']

ymax_ = [0,0]
doFit = False
if not isvbf_signal and not isvbf_channel:
 label = 'nonVBF-2016-nonVBFsignals'
 ymax_ = [5,1]
if not isvbf_signal and isvbf_channel:
 label = 'VBF-2016-nonVBFsignals'
 ymax_ = [15,5]
if not isvbf_channel and isvbf_signal:
 label = 'nonVBF-2016-VBFsignals'
 ymax_ = [5,2]
 doFit=True
if isvbf_channel and isvbf_signal:
 label = 'VBF-2016-VBFsignals'
 ymax_ = [15,5]
 doFit=True
 
effs_2016, uncs_2016, uncs_Run2_17, masses = plot_graphs('2016',ctx,'genWeight',signals_,label,ymax_) 

label = label.replace('2016','2017')
if not isvbf_signal and not isvbf_channel: ymax_ = [6,1.5]
if not isvbf_signal and isvbf_channel: ymax_ = [25,6]
if not isvbf_channel and isvbf_signal: ymax_ = [10,2]
if isvbf_channel and isvbf_signal: ymax_ = [20,5]
effs_2017, uncs_2017, uncs_Run2_17, masses = plot_graphs('2017',ctx,'genWeight_LO',signals_,label,ymax_) 

label = label.replace('2017','Run2')
if not isvbf_signal and not isvbf_channel: ymax_ = [4,1]
if not isvbf_signal and isvbf_channel: ymax_ = [15,3]
if not isvbf_channel and isvbf_signal: ymax_ = [5,1]
if isvbf_channel and isvbf_signal: ymax_ = [15,1]
effs_Run2, uncs_Run2, uncs_Run2_17, masses = plot_graphs('Run2',ctx,'genWeight_LO',signals_,label,ymax_) 

if doFit:
 parameters_16 = fit_graphs(uncs_Run2,masses,label)
 parameters_17 = fit_graphs(uncs_Run2_17,masses,label)
 
outfile = open('table_prefiring_%s.txt'%(label),'w')
sig_for_table = {'BulkGravToWW':'$\Grav\\to\Wo\Wo$','BulkGravToZZ':'$\Grav\\to\Zo\Zo$',
                 'RadionToWW':'Radion$\\to\Wo\Wo$','RadionToZZ':'Radion$\\to\Zo\Zo$',
                 'ZprimeToWW':'$\Zpr\\to\Wo\Wo$','ZprimeToZh':'$\Zpr\\to\Zo\Ho$',
                 'WprimeToWZ':'$\Wpr\\to\Wo\Zo$','WprimeToWh':'$\Wpr\\to\Wo\Ho$'}
if isvbf_signal:
 sig_for_table = {'VBF_BulkGravToWW':'$\Grav\\to\Wo\Wo$','VBF_BulkGravToZZ':'$\Grav\\to\Zo\Zo$',
                 'VBF_RadionToWW':'Radion$\\to\Wo\Wo$','VBF_RadionToZZ':'Radion$\\to\Zo\Zo$',
                 'VBF_ZprimeToWW':'$\Zpr\\to\Wo\Wo$','VBF_ZprimeToZh':'$\Zpr\\to\Zo\Ho$',
                 'VBF_WprimeToWZ':'$\Wpr\\to\Wo\Zo$','VBF_WprimeToWh':'$\Wpr\\to\Wo\Ho$'}
                               
for s in effs_2016.keys():

  myarr16 = np.array(effs_2016[s])
  myarr2_16 = np.array(uncs_2016[s])
  myarr17 = np.array(effs_2017[s])
  myarr2_17 = np.array(uncs_2017[s])
  line = ''
  if not isvbf_signal: line = "%s & %.1f (%.1f) & %.1f (%.1f)\n"%(sig_for_table[s],np.amax(myarr16),np.amax(myarr17),np.amax(myarr2_16),np.amax(myarr2_17))
  else: line = "%s & %.1f--%.1f (%.1f-%.1f) & %.1f--%.1f (%.1f--%.1f)\n"%(sig_for_table[s],np.amin(myarr16),np.amax(myarr16),np.amin(myarr17),np.amax(myarr17),np.amin(myarr2_16),np.amax(myarr2_16),np.amin(myarr2_17),np.amax(myarr2_17))
  print line.replace('\n','')
  outfile.write(line)

nw16 = histosTT_2016[0].Integral()
centr16 = histosTT_2016[1].Integral()
up16 = histosTT_2016[2].Integral()
nw17 = histosTT_2017[0].Integral()
centr17 = histosTT_2017[1].Integral()
up17 = histosTT_2017[2].Integral()
line = "%s & %.1f (%.1f) & %.1f (%.1f)\n"%('$\\ttbar$',(1.0-centr16/nw16)*100.,(1.0-centr17/nw17)*100.,(centr16-up16)*100./centr16,(centr17-up17)*100./centr17)
print line.replace('\n','')
outfile.write(line)

nw16 = histosWJets_2016[0].Integral()
centr16 = histosWJets_2016[1].Integral()
up16 = histosWJets_2016[2].Integral()
nw17 = histosWJets_2017[0].Integral()
centr17 = histosWJets_2017[1].Integral()
up17 = histosWJets_2017[2].Integral()
line = "%s & %.1f (%.1f) & %.1f (%.1f)\n"%('W+jets',(1.0-centr16/nw16)*100.,(1.0-centr17/nw17)*100.,(centr16-up16)*100./centr16,(centr17-up17)*100./centr17)
print line.replace('\n','')
outfile.write(line)

nw16 = histosZJets_2016[0].Integral()
centr16 = histosZJets_2016[1].Integral()
up16 = histosZJets_2016[2].Integral()
nw17 = histosZJets_2017[0].Integral()
centr17 = histosZJets_2017[1].Integral()
up17 = histosZJets_2017[2].Integral()
line = "%s & %.1f (%.1f) & %.1f (%.1f)\n"%('Z+jets',(1.0-centr16/nw16)*100.,(1.0-centr17/nw17)*100.,(centr16-up16)*100./centr16,(centr17-up17)*100./centr17)
print line.replace('\n','')
outfile.write(line)

outfile.write("--------------------------------\n")
outfile.write("Full Run 2\n")
outfile.write("--------------------------------\n")
print("--------------------------------\n")
print("Full Run 2\n")
print("--------------------------------\n")

final_uncs = {}

for s in effs_Run2.keys(): final_uncs[s] = {}
for s in effs_Run2.keys():
 final_uncs[s]['2016'] = ''
 final_uncs[s]['2017'] = ''
final_uncs['TT']={}
final_uncs['TT']['2016'] = ''
final_uncs['TT']['2017'] = ''
final_uncs['WJets'] = {}
final_uncs['WJets']['2016'] = ''
final_uncs['WJets']['2017'] = ''
final_uncs['ZJets'] = {}
final_uncs['ZJets']['2016'] = ''
final_uncs['ZJets']['2017'] = ''

for s in effs_Run2.keys():

  myarr16 = np.array(effs_Run2[s])
  myarr2_16 = np.array(uncs_Run2[s])
  myarr2_17 = np.array(uncs_Run2_17[s])
  line = ''
  if not doFit: line = "%s & %.1f & %.1f & %.1f\n"%(sig_for_table[s],np.amax(myarr16),np.amax(myarr2_16),np.amax(myarr2_17))
  else: line = "%s & %.1f--%.1f & %.1f--%.1f & %.1f--%.1f\n"%(sig_for_table[s],np.amin(myarr16),np.amax(myarr16),np.amin(myarr2_16),np.amax(myarr2_16),np.amin(myarr2_17),np.amax(myarr2_17))
  print line.replace('\n','')
  outfile.write(line)

  if not doFit:
   final_uncs[s]['2016'] = "(1.+%.8f)+0*MH"%(np.amax(myarr2_16)/100.)
   final_uncs[s]['2017'] = "(1.+%.8f)+0*MH"%(np.amax(myarr2_17)/100.)
  else:
   final_uncs[s]['2016'] = "(1.+%.8f*MH/1000.+%.8f)"%(parameters_16[s][0]/100.,parameters_16[s][1]/100.)
   final_uncs[s]['2017'] = "(1.+%.8f*MH/1000.+%.8f)"%(parameters_17[s][0]/100.,parameters_17[s][1]/100.)

nwRun2 = histosTT_Run2[0].Integral()
centrRun2 = histosTT_Run2[1].Integral()
up16 = histosTT_Run2_UncUp16.Integral()
up17 = histosTT_Run2_UncUp17.Integral()
final_uncs['TT']['2016'] = 1.0+(centrRun2-up16)/centrRun2
final_uncs['TT']['2017'] = 1.0+(centrRun2-up17)/centrRun2
line = "%s & %.1f & %.1f & %.1f\n"%('$\\ttbar$',(1.0-centrRun2/nwRun2)*100.,(centrRun2-up16)*100./centrRun2,(centrRun2-up17)*100./centrRun2)
print line.replace('\n','')
outfile.write(line)
  
nwRun2 = histosWJets_Run2[0].Integral()
centrRun2 = histosWJets_Run2[1].Integral()
up16 = histosWJets_Run2_UncUp16.Integral()
up17 = histosWJets_Run2_UncUp17.Integral()
final_uncs['WJets']['2016'] = 1.0+(centrRun2-up16)/centrRun2
final_uncs['WJets']['2017'] = 1.0+(centrRun2-up17)/centrRun2
line = "%s & %.1f & %.1f & %.1f\n"%('W+jets',(1.0-centrRun2/nwRun2)*100.,(centrRun2-up16)*100./centrRun2,(centrRun2-up17)*100./centrRun2)
print line.replace('\n','')
outfile.write(line)
   
nwRun2 = histosZJets_Run2[0].Integral()
centrRun2 = histosZJets_Run2[1].Integral()
up16 = histosZJets_Run2_UncUp16.Integral()
up17 = histosZJets_Run2_UncUp17.Integral()
final_uncs['ZJets']['2016'] = 1.0+(centrRun2-up16)/centrRun2
final_uncs['ZJets']['2017'] = 1.0+(centrRun2-up17)/centrRun2
line = "%s & %.1f & %.1f & %.1f\n"%('Z+jets',(1.0-centrRun2/nwRun2)*100.,(centrRun2-up16)*100./centrRun2,(centrRun2-up17)*100./centrRun2)
print line.replace('\n','')
outfile.write(line)

outfile.close()

print final_uncs
with open('prefiring_uncs_%s.json'%(label), "w") as jsfile: json.dump(final_uncs, jsfile) 

#final_uncs['TT']['2016']
#final_uncs['WJets']['2016']
#final_uncs['ZJets']['2016']
#final_uncs['TT']['2017']
#final_uncs['WJets']['2017']
#final_uncs['ZJets']['2017']
