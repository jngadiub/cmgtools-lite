import os, pickle, time, sys, math
import ROOT

doSignalEffWW = False
doSignalEffZH = False
doMistagRate = False
doPunzi = False
doPlots = False

# map testing 
doExternalMap = True

doPlotsMJJ = False
doPlotsMJet = False
doPlotsPT = True

extraLabel = "nominalMap_noBkup"
mapDir = "testMapPt_nominalonly/"

######################

doPlotsCut = False
files = []
filesZH = []
filesWW = []
for f in os.listdir('2016trainingV2'):
 if 'QCD_Pt_' in f and '.root' in f: files.append(f)
 if 'Bulk' in f and '.root' in f: filesWW.append(f)
 if 'Zprime' in f and '.root' in f: filesZH.append(f)

print files
lumi = 35900.

minMVV = 1126.
maxMVV = 5500.
minMJ= 55.0
maxMJ= 215.0

catHtag = {}
catVtag = {}

'''
# For retuned DDT tau 21, use this                                                                                                                                                                                                                                             
cat['HP1'] = '(jj_l1_tau2/jj_l1_tau1+(0.080*TMath::Log((jj_l1_softDrop_mass*jj_l1_softDrop_mass)/jj_l1_pt)))<0.43'
cat['HP2'] = '(jj_l2_tau2/jj_l2_tau1+(0.080*TMath::Log((jj_l2_softDrop_mass*jj_l2_softDrop_mass)/jj_l2_pt)))<0.43'
cat['LP1'] = '(jj_l1_tau2/jj_l1_tau1+(0.080*TMath::Log((jj_l1_softDrop_mass*jj_l1_softDrop_mass)/jj_l1_pt)))>0.43&&(jj_l1_tau2/jj_l1_tau1+(0.080*TMath::Log((jj_l1_softDrop_mass*jj_l1_softDrop_mass)/jj_l1_pt)))<0.79'
cat['LP2'] = '(jj_l2_tau2/jj_l2_tau1+(0.080*TMath::Log((jj_l2_softDrop_mass*jj_l2_softDrop_mass)/jj_l2_pt)))>0.43&&(jj_l2_tau2/jj_l2_tau1+(0.080*TMath::Log((jj_l2_softDrop_mass*jj_l2_softDrop_mass)/jj_l2_pt)))<0.79'
'''

catVtag['HP1'] = '(jj_l1_DeepBoosted_WvsQCD>jj_l1_DeepBoosted_WvsQCD__0p05)'																						   
catVtag['HP2'] = '(jj_l2_DeepBoosted_WvsQCD>jj_l2_DeepBoosted_WvsQCD__0p05)'																						   
catVtag['LP1'] = '((jj_l1_DeepBoosted_WvsQCD<jj_l1_DeepBoosted_WvsQCD__0p05)&&(jj_l1_DeepBoosted_WvsQCD>jj_l1_DeepBoosted_WvsQCD__0p10))'     
catVtag['LP2'] = '((jj_l2_DeepBoosted_WvsQCD<jj_l2_DeepBoosted_WvsQCD__0p05)&&(jj_l2_DeepBoosted_WvsQCD>jj_l2_DeepBoosted_WvsQCD__0p10))'													   
catVtag['NP1'] = '(jj_l1_DeepBoosted_WvsQCD<jj_l1_DeepBoosted_WvsQCD__0p10)'																						   
catVtag['NP2'] = '(jj_l2_DeepBoosted_WvsQCD<jj_l2_DeepBoosted_WvsQCD__0p10)'

catHtag['HP1'] = '(jj_l1_DeepBoosted_ZHbbvsQCD>jj_l1_DeepBoosted_ZHbbvsQCD__0p02)' 
catHtag['HP2'] = '(jj_l2_DeepBoosted_ZHbbvsQCD>jj_l2_DeepBoosted_ZHbbvsQCD__0p02)' 
catHtag['LP1'] = '(jj_l1_DeepBoosted_ZHbbvsQCD<jj_l1_DeepBoosted_ZHbbvsQCD__0p02&&jj_l1_DeepBoosted_ZHbbvsQCD>jj_l1_DeepBoosted_ZHbbvsQCD__0p10)' 
catHtag['LP2'] = '(jj_l2_DeepBoosted_ZHbbvsQCD<jj_l2_DeepBoosted_ZHbbvsQCD__0p02&&jj_l2_DeepBoosted_ZHbbvsQCD>jj_l2_DeepBoosted_ZHbbvsQCD__0p10)'
catHtag['NP1'] = '(jj_l1_DeepBoosted_ZHbbvsQCD<jj_l1_DeepBoosted_ZHbbvsQCD__0p10)' 
catHtag['NP2'] = '(jj_l2_DeepBoosted_ZHbbvsQCD<jj_l2_DeepBoosted_ZHbbvsQCD__0p10)'

cuts={}
cuts['common'] = '((HLT_JJ)*(run>500) + (run<500))*(passed_METfilters&&passed_PVfilter&&njj>0&&jj_LV_mass>700&&abs(jj_l1_eta-jj_l2_eta)<1.3&&jj_l1_softDrop_mass>0.&&jj_l2_softDrop_mass>0.&&TMath::Log(jj_l1_softDrop_mass**2/jj_l1_softDrop_pt**2)<-1.8&&TMath::Log(jj_l2_softDrop_mass**2/jj_l2_softDrop_pt**2)<-1.8)'
#cuts['common'] = '((HLT_JJ)*(run>500) + (run<500))*(passed_METfilters&&passed_PVfilter&&njj>0&&puppijjmass(jj_l1_softDrop_pt,jj_l1_softDrop_eta,jj_l1_softDrop_phi,jj_l1_softDrop_mass,jj_l2_softDrop_pt,jj_l2_softDrop_eta,jj_l2_softDrop_phi,jj_l2_softDrop_mass)>700&&abs(jj_l1_softDrop_eta-jj_l2_softDrop_eta)<1.3&&jj_l1_softDrop_mass>0.&&jj_l2_softDrop_mass>0.&&TMath::Log(jj_l1_softDrop_mass**2/jj_l1_softDrop_pt**2)<-1.8&&TMath::Log(jj_l2_softDrop_mass**2/jj_l2_softDrop_pt**2)<-1.8)'                                                        
cuts['acceptance']= "(jj_LV_mass>{minMVV}&&jj_LV_mass<{maxMVV}&&jj_l1_softDrop_mass>{minMJ}&&jj_l1_softDrop_mass<{maxMJ}&&jj_l2_softDrop_mass>{minMJ}&&jj_l2_softDrop_mass<{maxMJ})".format(minMVV=minMVV,maxMVV=maxMVV,minMJ=minMJ,maxMJ=maxMJ)


catsAll = {}

#at least one H tag HP (+ one V/H tag HP)                                                                                                                                                                                                                                      
catsAll['VH_HPHP'] = '('+'&&'.join([catVtag['HP1'],catHtag['HP2']])+')'
catsAll['HV_HPHP'] = '('+'&&'.join([catHtag['HP1'],catVtag['HP2']])+')'
catsAll['HH_HPHP'] = '('+'&&'.join([catHtag['HP1'],catHtag['HP2']])+')'
cuts['VH_HPHP'] = '('+'||'.join([catsAll['VH_HPHP'],catsAll['HV_HPHP'],catsAll['HH_HPHP']])+')'

# two V tag HP                                                                                                                                                                                                                                                                 
cuts['VV_HPHP'] = '('+'!'+cuts['VH_HPHP']+'&&'+'(' +  '&&'.join([catVtag['HP1'],catVtag['HP2']]) + ')' + ')'


#at least one H-tag HP (+one V OR H-tag LP)                                                                                                                                                                                                                                    
catsAll['VH_LPHP'] = '('+'&&'.join([catVtag['LP1'],catHtag['HP2']])+')'
catsAll['HV_HPLP'] = '('+'&&'.join([catHtag['HP1'],catVtag['LP2']])+')'
catsAll['HH_HPLP'] = '('+'&&'.join([catHtag['HP1'],catHtag['LP2']])+')'
catsAll['HH_LPHP'] = '('+'&&'.join([catHtag['LP1'],catHtag['HP2']])+')'
cuts['VH_LPHP'] = '('+'('+'!'+cuts['VH_HPHP']+'&&!'+cuts['VV_HPHP']+')&&('+'||'.join([catsAll['VH_LPHP'],catsAll['HV_HPLP'],catsAll['HH_HPLP'],catsAll['HH_LPHP']])+')'+')'

#at least one V-tag HP (+ one H-tag LP)                                                                                                                                                                                                                                        
catsAll['VH_HPLP'] = '('+'&&'.join([catVtag['HP1'],catHtag['LP2']])+')'
catsAll['HV_LPHP'] = '('+'&&'.join([catHtag['LP1'],catVtag['HP2']])+')'
cuts['VH_HPLP'] = '('+'('+'!'+cuts['VH_LPHP']+'&&!'+cuts['VH_HPHP']+'&&!'+cuts['VV_HPHP']+')&&('+'||'.join([catsAll['VH_HPLP'],catsAll['HV_LPHP']])+')'+')'


cuts['VH_LPLP'] = '('+'('+ '&&'.join([catVtag['LP1'],catHtag['LP2']]) + ')'+ '||' +'(' + '&&'.join([catVtag['LP2'],catHtag['LP1']]) + ')' + '||' + '(' + '&&'.join([catVtag['LP2'],catHtag['LP1']]) + ')' +'||' + '(' + '&&'.join([catHtag['LP2'],catHtag['LP1']]) + ')' + ')'

cuts['VH_all'] =  '('+  '||'.join([cuts['VH_HPHP'],cuts['VH_LPHP'],cuts['VH_HPLP']]) + ')'

cuts['VV_HPLP'] = '(' +'('+'!'+cuts['VH_LPHP']+'&&!'+cuts['VH_HPHP']+'&&!'+cuts['VV_HPHP']+'&&!'+cuts['VH_HPLP']+') &&' + '(' + '('+  '&&'.join([catVtag['HP1'],catVtag['LP2']]) + ')' + '||' + '(' + '&&'.join([catVtag['HP2'],catVtag['LP1']]) + ')' + ')' + ')'

################### test external maps ################

if doExternalMap:
 inputDir='2016trainingV2/noBkup/' 
 #percMin = ['no'] #,'0p02','0p05','0p10','0p10']
 #percMax = ['no'] #,'0p05','0p10','0p20','0p15']
 percMin = ['0p05'] #,'0p02','0p05','0p10','0p10']
 percMax = ['0p05'] #,'0p05','0p10','0p20','0p15']
  
 for i,p in enumerate(percMin):
 

  if doPlotsMJet:
   label = 'W_mjet1_cuts_rhosd_testoldmap_'+p+'_'+percMax[i]
   hmass = ROOT.TH1F("hmass_%s"%label,"hmass_%s"%label,40,55,215)
  if doPlotsMJJ:
   label = 'W_mjj_cuts_rhosd_testloosemap_'+p+'_'+percMax[i] 
   hmass = ROOT.TH1F("hmass_%s"%label,"hmass_%s"%label,100,1000,6000)
  if doPlotsPT:
   label = 'W_pt1sd_cuts_rhosd_testloosemap_'+p+'_'+percMax[i]
   hmass = ROOT.TH1F("hpt1sd_1j_%s"%label,"hpt1sd_1j_%s"%label,100,200,4000)
#  hmass = ROOT.TH1F("hpt1sd_1j_%s"%label,"hpt1sd_1j_%s"%label,50,20,1500)

  print hmass
  
  print "Making histos for ",label
  if p != 'no':
   mapn= mapDir+"/myDeepBoostedMap_"+p+"rho.root"
   print mapn
   mapf = ROOT.TFile.Open(mapn,'READ')
   print mapf
   mapname =  "DeepBoosted_WvsQCD_v_rho_v_pT_yx"  #"DeepBoosted_WvsQCD_v_rho_v_pT_scaled_0p95_map_dijet" #"DeepBoosted_WvsQCD_v_rho_v_pT_scaled_yx" #"DeepBoosted_WvsQCD_v_rho_v_pT_yx"
   map_WvsQCD = mapf.Get(mapname) 
   print type( map_WvsQCD )
   print "entries in  map_WvsQCD ",map_WvsQCD.GetEntries()
   ROOT.gROOT.GetListOfSpecials().Add(map_WvsQCD);
  
  for f in files:
   print "   * File:",f
   tf = ROOT.TFile.Open(inputDir+f,'READ')
   tree = tf.AnalysisTree   
   fpck=open(inputDir+f.replace('.root','.pck'))
   dpck=pickle.load(fpck)
   weightinv = float(dpck['events'])
   htmp0 = ROOT.gROOT.FindObject('htmp0')
   if htmp0: htmp0.Delete()
   
   if p != 'no': 
    cutTagger = '(jj_l1_DeepBoosted_WvsQCD>getWcut(jj_l1_softDrop_pt,jj_l1_softDrop_mass))'   #,ROOT.gROOT.FindObject(map_WvsQCD)))' #.format(perc=p)
#   cutTagger = '(jj_l1_DeepBoosted_WvsQCD>getWcut(jj_l1_softDrop_pt,jj_l1_softDrop_mass))'   #,ROOT.gROOT.FindObject(map_WvsQCD)))' #.format(perc=p)
#   cutTagger = '(jj_l1_DeepBoosted_WvsQCD>getWcut(jj_l1_softDrop_pt,jj_l1_softDrop_mass)&&jj_l2_DeepBoosted_WvsQCD>getWcut(jj_l2_softDrop_pt,jj_l2_softDrop_mass))'   #,ROOT.gROOT.FindObject(map_WvsQCD)))' #.format(perc=p)
#   cutTagger = '(jj_l1_DeepBoosted_WvsQCD>jj_l1_DeepBoosted_WvsQCD__{perc})'.format(perc=p)
#   if i!= 0: cutTagger = '((jj_l1_DeepBoosted_WvsQCD<jj_l1_DeepBoosted_WvsQCD__{percMin})&&(jj_l1_DeepBoosted_WvsQCD>jj_l1_DeepBoosted_WvsQCD__{percMax})&&(jj_l2_DeepBoosted_WvsQCD<jj_l2_DeepBoosted_WvsQCD__{percMin})&&(jj_l2_DeepBoosted_WvsQCD>jj_l2_DeepBoosted_WvsQCD__{percMax}))'.format(percMin=p,percMax=percMax[i])
   #cutTagger = '(jj_l1_DeepBoosted_ZHbbvsQCD>jj_l1_DeepBoosted_ZHbbvsQCD__{perc}&&jj_l2_DeepBoosted_ZHbbvsQCD>jj_l2_DeepBoosted_ZHbbvsQCD__{perc})'.format(perc=p)
   #if i!= 0: cutTagger = '((jj_l1_DeepBoosted_ZHbbvsQCD<jj_l1_DeepBoosted_ZHbbvsQCD__{percMin})&&(jj_l1_DeepBoosted_ZHbbvsQCD>jj_l1_DeepBoosted_ZHbbvsQCD__{percMax})&&(jj_l2_DeepBoosted_ZHbbvsQCD<jj_l2_DeepBoosted_ZHbbvsQCD__{percMin})&&(jj_l2_DeepBoosted_ZHbbvsQCD>jj_l2_DeepBoosted_ZHbbvsQCD__{percMax}))'.format(percMin=p,percMax=percMax[i])
   cut = "*".join([cuts['common'],cuts['acceptance']])   
   if p != 'no': cut = "*".join([cuts['common'],cuts['acceptance'],cutTagger])   
   
   print " before ROOT.gROOT.Macro(myfunctions.C+) "
   ROOT.gROOT.Macro("myfunctions.C")
   print "after"
   if doPlotsMJJ:
    tree.Draw('jj_LV_mass>>htmp0(100,1000,6000)','(genWeight*xsec*puWeight*%.20f)*'%(lumi/weightinv)+cut,"goff")
    #   tree.Draw('puppijjmass(jj_l1_softDrop_pt,jj_l1_softDrop_eta,jj_l1_softDrop_phi,jj_l1_softDrop_mass,jj_l2_softDrop_pt,jj_l2_softDrop_eta,jj_l2_softDrop_phi,jj_l2_softDrop_mass)>>htmp0(100,1000,6000)','(genWeight*xsec*puWeight*%.20f)*'%(lumi/weightinv)+cut,"goff")
   if doPlotsPT:
    #   tree.Draw('jj_l1_softDrop_pt>>htmp0(50,20,1500)','(genWeight*xsec*puWeight*%.20f)*'%(lumi/weightinv)+cut,"goff")
    tree.Draw('jj_l1_softDrop_pt>>htmp0(100,200,4000)','(genWeight*xsec*puWeight*%.20f)*'%(lumi/weightinv)+cut,"goff")
   if doPlotsMJet:
    tree.Draw('jj_l1_softDrop_mass>>htmp0(40,55,215)','(genWeight*xsec*puWeight*%.20f)*'%(lumi/weightinv)+cut,"goff")

   htmp0 = ROOT.gROOT.FindObject('htmp0')
   print label,hmass
   if htmp0:
    hmass.Add(htmp0)
  
  hmass.SaveAs('h_%s_%s.root'%(label,extraLabel))  


if doPlotsCut:
 inputDir='2016trainingV2/' #OldDDTMaps/

 percMin = ['no'] #,'0p02','0p05','0p10','0p10']
 percMax = ['no'] #,'0p05','0p10','0p20','0p15']
 #percMin = ['0p10'] #,'0p02','0p05','0p10','0p10']
 #percMax = ['0p10'] #,'0p05','0p10','0p20','0p15']
 #percMin = ['0p10','0p02','0p05','0p10','0p10']
 #percMax = ['0p10','0p05','0p10','0p20','0p15']
 #percMin = ['0p50','0p02','0p05','0p10']
 #percMax = ['0p50','0p05','0p10','0p20']
  
# hmass = {}
 for i,p in enumerate(percMin):
 
  #ROOT.gDirectory.cd()
  
  label = 'W_cutpt_'+p+'_'+percMax[i]
  hmass = ROOT.TH2F("hcut_%s"%label,"hcut_%s"%label,100,200,4000,300,-1.5,1)
#  hmass = ROOT.TH1F("hcut_%s"%label,"hcut_%s"%label,100,0,1)
#  hmass[label] = ROOT.TH1F("hmass_%s"%label,"hmass_%s"%label,40,55,215)
  print hmass
  
  #if i!=0: continue
  
  print "Making histos for ",label
 
  for f in files:
   print "   * File:",f
   tf = ROOT.TFile.Open(inputDir+f,'READ')
   tree = tf.AnalysisTree   
   fpck=open(inputDir+f.replace('.root','.pck'))
   dpck=pickle.load(fpck)
   weightinv = float(dpck['events'])
   htmp2D = ROOT.gROOT.FindObject('htmp2D')
   if htmp2D: htmp2D.Delete()
   #cutTagger = '(jj_l1_DeepBoosted_WvsQCD>jj_l1_DeepBoosted_WvsQCD__{perc}&&jj_l2_DeepBoosted_WvsQCD>jj_l2_DeepBoosted_WvsQCD__{perc})'.format(perc=p)
   #if i!= 0: cutTagger = '((jj_l1_DeepBoosted_WvsQCD<jj_l1_DeepBoosted_WvsQCD__{percMin})&&(jj_l1_DeepBoosted_WvsQCD>jj_l1_DeepBoosted_WvsQCD__{percMax})&&(jj_l2_DeepBoosted_WvsQCD<jj_l2_DeepBoosted_WvsQCD__{percMin})&&(jj_l2_DeepBoosted_WvsQCD>jj_l2_DeepBoosted_WvsQCD__{percMax}))'.format(percMin=p,percMax=percMax[i])
   #cutTagger = '(jj_l1_DeepBoosted_ZHbbvsQCD>jj_l1_DeepBoosted_ZHbbvsQCD__{perc}&&jj_l2_DeepBoosted_ZHbbvsQCD>jj_l2_DeepBoosted_ZHbbvsQCD__{perc})'.format(perc=p)
   #if i!= 0: cutTagger = '((jj_l1_DeepBoosted_ZHbbvsQCD<jj_l1_DeepBoosted_ZHbbvsQCD__{percMin})&&(jj_l1_DeepBoosted_ZHbbvsQCD>jj_l1_DeepBoosted_ZHbbvsQCD__{percMax})&&(jj_l2_DeepBoosted_ZHbbvsQCD<jj_l2_DeepBoosted_ZHbbvsQCD__{percMin})&&(jj_l2_DeepBoosted_ZHbbvsQCD>jj_l2_DeepBoosted_ZHbbvsQCD__{percMax}))'.format(percMin=p,percMax=percMax[i])
   #cutTagger = '(jj_l1_softDrop_pt>490&&jj_l1_softDrop_pt<510)'
   #cut = "*".join([cuts['common'],cuts['acceptance'],cutTagger])   
   cut = "*".join([cuts['common'],cuts['acceptance']])   
   print " before ROOT.gROOT.Macro(myfunctions.C+) "
   ROOT.gROOT.Macro("myfunctions.C")
   print "after"
   
#   tree.Draw('jj_LV_mass>>htmp2D(100,1000,6000)','(genWeight*xsec*puWeight*%.20f)*'%(lumi/weightinv)+cut)
#   tree.Draw('puppijjmass(jj_l1_softDrop_pt,jj_l1_softDrop_eta,jj_l1_softDrop_phi,jj_l1_softDrop_mass,jj_l2_softDrop_pt,jj_l2_softDrop_eta,jj_l2_softDrop_phi,jj_l2_softDrop_mass)>>htmp2D(100,1000,6000)','(genWeight*xsec*puWeight*%.20f)*'%(lumi/weightinv)+cut,"goff")
   tree.Draw('jj_l1_DeepBoosted_WvsQCD__0p10:jj_l1_softDrop_pt>>htmp2D(100,200,4000,300,-1.5,1)','(genWeight*xsec*puWeight*%.20f)*'%(lumi/weightinv)+cut,"goff")

   htmp2D = ROOT.gROOT.FindObject('htmp2D')
   print label,hmass
#   print label,hmass[label]
   if htmp2D:
    hmass.Add(htmp2D)
    #hmass[label].Add(htmp2D)
   
  hmass.SaveAs('h_%s.root'%label) 
#  hmass[label].SaveAs('h_%s.root'%label) 




if doPlots:
 inputDir='2016trainingV2/' #OldDDTMaps/
# percMin = ['no'] #,'0p02','0p05','0p10','0p10']
# percMax = ['no'] #,'0p05','0p10','0p20','0p15']
 percMin = ['0p50'] #,'0p02','0p05','0p10','0p10']
 percMax = ['0p50'] #,'0p05','0p10','0p20','0p15']
 #percMin = ['0p10','0p02','0p05','0p10','0p10']
 #percMax = ['0p10','0p05','0p10','0p20','0p15']
 #percMin = ['0p50','0p02','0p05','0p10']
 #percMax = ['0p50','0p05','0p10','0p20']
  
# hmass = {}
 for i,p in enumerate(percMin):
 
  #ROOT.gDirectory.cd()
  
  label = 'W_'+p+'_'+percMax[i]
  hmass = ROOT.TH1F("hmass_%s"%label,"hmass_%s"%label,40,55,215)
#  hmass[label] = ROOT.TH1F("hmass_%s"%label,"hmass_%s"%label,40,55,215)
  print hmass
  
  #if i!=0: continue
  
  print "Making histos for ",label
 
  for f in files:
   print "   * File:",f
   tf = ROOT.TFile.Open(inputDir+f,'READ')
   tree = tf.AnalysisTree   
   fpck=open(inputDir+f.replace('.root','.pck'))
   dpck=pickle.load(fpck)
   weightinv = float(dpck['events'])
   htmp = ROOT.gROOT.FindObject('htmp')
   if htmp: htmp.Delete()
   cutTagger = '(jj_l1_DeepBoosted_WvsQCD>jj_l1_DeepBoosted_WvsQCD__{perc}&&jj_l2_DeepBoosted_WvsQCD>jj_l2_DeepBoosted_WvsQCD__{perc})'.format(perc=p)
   if i!= 0: cutTagger = '((jj_l1_DeepBoosted_WvsQCD<jj_l1_DeepBoosted_WvsQCD__{percMin})&&(jj_l1_DeepBoosted_WvsQCD>jj_l1_DeepBoosted_WvsQCD__{percMax})&&(jj_l2_DeepBoosted_WvsQCD<jj_l2_DeepBoosted_WvsQCD__{percMin})&&(jj_l2_DeepBoosted_WvsQCD>jj_l2_DeepBoosted_WvsQCD__{percMax}))'.format(percMin=p,percMax=percMax[i])
   #cutTagger = '(jj_l1_DeepBoosted_ZHbbvsQCD>jj_l1_DeepBoosted_ZHbbvsQCD__{perc}&&jj_l2_DeepBoosted_ZHbbvsQCD>jj_l2_DeepBoosted_ZHbbvsQCD__{perc})'.format(perc=p)
   #if i!= 0: cutTagger = '((jj_l1_DeepBoosted_ZHbbvsQCD<jj_l1_DeepBoosted_ZHbbvsQCD__{percMin})&&(jj_l1_DeepBoosted_ZHbbvsQCD>jj_l1_DeepBoosted_ZHbbvsQCD__{percMax})&&(jj_l2_DeepBoosted_ZHbbvsQCD<jj_l2_DeepBoosted_ZHbbvsQCD__{percMin})&&(jj_l2_DeepBoosted_ZHbbvsQCD>jj_l2_DeepBoosted_ZHbbvsQCD__{percMax}))'.format(percMin=p,percMax=percMax[i])
   ROOT.gROOT.Macro("myfunctions.C")
   cut = "*".join([cuts['common'],cuts['acceptance'],cutTagger])   
   #cut = "*".join([cuts['common'],cuts['acceptance']])   
#   tree.Draw('jj_l1_softDrop_mass>>htmp(40,55,215)','(genWeight*xsec*puWeight*%.20f)*'%(lumi/weightinv)+cut,"goff")
   tree.Draw('jj_l2_softDrop_mass>>htmp(40,55,215)','(genWeight*xsec*puWeight*%.20f)*'%(lumi/weightinv)+cut,"goff")
#jj_LV_mass
   htmp = ROOT.gROOT.FindObject('htmp')
   print label,hmass
#   print label,hmass[label]
   if htmp:
    hmass.Add(htmp)
    #hmass[label].Add(htmp)
   
  hmass.SaveAs('h_%s.root'%label) 
#  hmass[label].SaveAs('h_%s.root'%label) 

##################### FOR SIGNAL EFF ###################
print ""
num = {}
if doSignalEffWW or doSignalEffZH:

 files_sig = filesZH
 if doSignalEffWW: files_sig = filesWW
 
 for f in files_sig:
 
  numALL = 0
  
  tf = ROOT.TFile.Open('2016trainingV2/'+f,'READ')
  tree = tf.AnalysisTree

  cut = "*".join([cuts['common'],cuts['acceptance']])
  den = float(tree.GetEntries(cut))
 
  cut = "*".join([cuts['VH_HPHP'],cuts['common'],cuts['acceptance']])
  num['VH_HPHP'] = float(tree.GetEntries(cut))

  cut = "*".join([cuts['VH_LPHP'],cuts['common'],cuts['acceptance']])
  num['VH_LPHP'] = float(tree.GetEntries(cut))

  cut = "*".join([cuts['VH_HPLP'],cuts['common'],cuts['acceptance']])
  #num['VH_HPLP'] = float(tree.GetEntries(cut))
 
  cut = "*".join([cuts['VH_all'],cuts['common'],cuts['acceptance']])
  num['VH_all'] = float(tree.GetEntries(cut))

  cut = "*".join(['('+cuts['VV_HPHP']+'||'+cuts['VH_HPLP']+')',cuts['common'],cuts['acceptance']]) #if I add VH_HPLP to VV_HPHP how much background I am picking up?
  num['VV_HPHP'] = float(tree.GetEntries(cut))

  cut = "*".join([cuts['VV_HPLP'],cuts['common'],cuts['acceptance']])
  num['VV_HPLP'] = float(tree.GetEntries(cut))

  cut = "*".join([cuts['VV_HPHP_noVeto'],cuts['common'],cuts['acceptance']])
  #num['VV_HPHP_noVeto'] = float(tree.GetEntries(cut))
      
  print "File:",f
  for k in num.keys():
   print "    -",k,num[k]/den
   if not 'all' in k: numALL+=num[k]

  print "--> Total eff (cross check):",numALL/den
  print ""



#################### FOR PUNZI ################

whichCat='VH_LPHP'
files_sig = filesWW
#files_sig = filesZH
masses = [3000]
#masses = [1200,2500,4000]

if doPunzi:

 eff = 0.
 num = 0.
 den = 0.
 
 hrate = {}
 effSig = {}
 for m in masses:
  hrate[m] = ROOT.TH1F('hrate_M%i'%m,'hrate_M%i'%m,3,0,3)

 for f in files:

  fpck=open('2016trainingV2/'+f.replace('.root','.pck'))
  dpck=pickle.load(fpck)
  weightinv = float(dpck['events'])
 
  tf = ROOT.TFile.Open('2016trainingV2/'+f,'READ')
  tree = tf.AnalysisTree
     
  fout = ROOT.TFile.Open('ftmp22222.root','RECREATE')   
  fout.cd()
  
  cut = "*".join([cuts['common'],cuts['acceptance']])
  reduced = tree.CopyTree(cut,"")
  reduced.Write("reduced")
  
  for m in masses:
   
   mjjcut = '(jj_LV_mass>%f&&jj_LV_mass<%f)'%(m-m*0.15,m+m*0.15)
   pden = float(reduced.GetEntries(mjjcut))
   den += float(reduced.GetEntries(mjjcut))
 
   htmp = ROOT.gROOT.FindObject('htmp')
   if htmp: htmp.Delete()

   cut = "*".join([cuts[whichCat],mjjcut])  
   reduced.Draw('njj>>htmp(3,0,3)','(genWeight*xsec*puWeight*%.20f)*'%(lumi/weightinv)+cut)
   htmp = ROOT.gROOT.FindObject('htmp')
   hrate[m].Add(htmp)
  
   pnum = float(reduced.GetEntries(cut))
   num += float(reduced.GetEntries(cut))
   
   peff = 0
   if pden!=0: peff=pnum/pden

   print "Mass:",m,"File:",f,"Partial rate:",hrate[m].Integral(),"Partial Den:",pden,"Partial Num:",pnum,"Partial Bkg Eff:",peff,
   
   #now calculate signal eff for Punzi
   for fs in files_sig:
    mass = float(fs.split('_')[-1].replace('.root',''))
    if mass!=m: continue
    
    tfSig = ROOT.TFile.Open('2016trainingV2/'+fs,'READ')
    treeSig = tfSig.AnalysisTree

    cut = "*".join([cuts['common'],cuts['acceptance'],mjjcut])    
    denSig = float(treeSig.GetEntries(cut))
    
    cut = "*".join([cuts['common'],cuts['acceptance'],mjjcut,cuts[whichCat]])  
    numSig = float(treeSig.GetEntries(cut))    
   
    effSig[m] = numSig/denSig
    print "Signal Eff:",numSig/denSig,"Partial Punzi:",(effSig[m])/(1+math.sqrt(hrate[m].Integral()))
  
  fout.Close()

 for m in masses:
  print "----> Final Punzi for mass",m," - cat.",whichCat,":",effSig[m]/(1+math.sqrt(hrate[m].Integral())),"Final Back eff:",num/den




#################### FOR MISTAG RATE ################
whichCat='VH_LPHP'
if doMistagRate:

 eff = 0.
 num = 0.
 den = 0.

 for f in files:

  tf = ROOT.TFile.Open('2016trainingV2/'+f,'READ')
  tree = tf.AnalysisTree
     
  cut = "*".join([cuts['common'],cuts['acceptance']])
  pden = float(tree.GetEntries(cut))
  den += float(tree.GetEntries(cut))

  cut = "*".join([cuts[whichCat],cuts['common'],cuts['acceptance']]) 
  pnum = float(tree.GetEntries(cut))
  num += float(tree.GetEntries(cut))    

  print "File:",f,"Partial Num:",pnum,"Partial Den:",pden,"Partial Eff:",pnum/pden
 print "----> Final mistag rate for cat.",whichCat,":",num/den




