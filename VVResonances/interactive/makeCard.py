from tools.DatacardTools import *
import sys,os
import ROOT
ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")
from CMGTools.VVResonances.statistics.DataCardMaker import DataCardMaker
cmd='combineCards.py '

sf_qcd = 1.0
pseudodata = ""
outlabel = ""

datasets=['2016']#,'2017']
resultsDir = {'2016':'results_2016','2017':'results_2017'}

lumi = {'2016':35900,'2017':41367}
lumi_unc = {'2016':1.025,'2017':1.023}

scales = {"2017" :[0.983,1.08], "2016":[1.014,1.086]}

vtag_unc = {'VV_HPHP':{},'VV_HPLP':{},'VV_LPLP':{}}
vtag_unc['VV_HPHP'] = {'2016':'1.232/0.792','2017':'1.269/0.763'}
vtag_unc['VV_HPLP'] = {'2016':'0.882/1.12','2017':'0.866/1.136'}    
vtag_unc['VV_LPLP'] = {'2016':'1.063','2017':'1.043'}

vtag_pt_dependence = {'VV_HPHP':'((1+0.06*log(MH/2/300))*(1+0.06*log(MH/2/300)))','VV_HPLP':'((1+0.06*log(MH/2/300))*(1+0.07*log(MH/2/300)))'}
  
purities= ['VV_HPLP']
#purities= ['VV_HPLP','VV_HPHP']
#signals = ["BulkGWW", "BulkGZZ","ZprimeWW","WprimeWZ","VprimeWV","'ZprimeZH'"]
signals = ["BulkGWW"]

Tools = DatacardTools(scales,vtag_pt_dependence,lumi_unc,vtag_unc,sf_qcd,pseudodata,outlabel)

for sig in signals:
  cmd ="combineCards.py"
  for dataset in datasets:
    cmd_combo="combineCards.py"
    for p in purities:

      ncontrib = 0
      
      cat='_'.join(['JJ',sig,p,'13TeV_'+dataset])
      card=DataCardMaker('',p,'13TeV_'+dataset,lumi[dataset],'JJ',cat)
      cmd=cmd+" "+cat.replace('_%s'%sig,'')+'=datacard_'+cat+'.txt '
      cmd_combo=cmd_combo+" "+cat.replace('_%s'%sig,'')+'=datacard_'+cat+'.txt '
      cardName='datacard_'+cat+'.txt'
      workspaceName='workspace_'+cat+outlabel+'.root'
            
      Tools.AddSignal(card,dataset,p,sig,resultsDir[dataset],ncontrib)                
      ncontrib+=1

      rootFileMVV = resultsDir[dataset]+'/JJ_%s_WJets_MVV_'%dataset+p+'.root' 
      rootFileNorm = resultsDir[dataset]+'/JJ_%s_WJets_%s.root'%(dataset,p)
      Tools.AddWResBackground(card,dataset,p,rootFileMVV,rootFileNorm,resultsDir[dataset],ncontrib)
      ncontrib+=1
      
      rootFileMVV = resultsDir[dataset]+'/JJ_%s_ZJets_MVV_'%dataset+p+'.root'
      rootFileNorm = resultsDir[dataset]+"/JJ_%s_ZJets_%s.root"%(dataset,p)
      Tools.AddZResBackground(card,dataset,p,rootFileMVV,rootFileNorm,resultsDir[dataset],ncontrib)
      ncontrib+=1
      
      rootFile3DPDF = resultsDir[dataset]+'/JJ_2016_nonRes_3D_VV_HPLP.root'
      #rootFile3DPDF = resultsDir[dataset]+"/save_new_shapes_pythia_"+p+"_3D.root"
      rootFileNorm = resultsDir[dataset]+"/JJ_%s_nonRes_"%dataset+p+".root"   
      Tools.AddNonResBackground(card,dataset,p,rootFile3DPDF,rootFileNorm,ncontrib) 

      #rootFileData = resultsDir[dataset]+"/JJ_"+p+".root"
      #histName="data"
      #scaleData=1.0 #f you ru on real data
      rootFileData = "results_2016/JJ_2016_nonRes_VV_HPLP.root"   
      histName="nonRes"
      scaleData=lumi[dataset] #if you run on MC for transfer-kernel
      if pseudodata=="ZprimeZH":
       rootFileData = resultsDir[dataset]+"/JJ_ZprimeZH_VH_all_M2000.root"
       histName="data_obs"
       scaleData=1.0
      if pseudodata=="WprimeWZ":
       rootFileData = resultsDir[dataset]+"/JJ_WprimeWZ_VV_HPLP_M2000.root" 
       histName="data_obs"    
       scaleData=1.0
      Tools.AddData(card,rootFileData,histName,scaleData)
      
      Tools.AddSigSystematics(card,sig,dataset,p,1)
      Tools.AddResBackgroundSystematics(card,p)
      Tools.AddNonResBackgroundSystematics(card,p)
        
      card.makeCard()
      
      t2wcmd = "text2workspace.py %s -o %s"%(cardName,workspaceName)
      print t2wcmd
      os.system(t2wcmd)
    del card
    #make combined HPHP+HPLP card   
    combo_card = 'datacard_'+cat.replace("_HPHP","").replace("_HPLP","").replace("_LPLP","")+'.txt'
    combo_workspace = 'workspace_'+cat.replace("_HPHP","").replace("_HPLP","").replace("_LPLP","")+pseudodata+'.root'
    os.system('rm %s'%combo_card)
    cmd_combo+=' >> %s'%combo_card
    print cmd_combo
    os.system(cmd_combo)
    t2wcmd = "text2workspace.py %s -o %s"%(combo_card,combo_workspace)
    print t2wcmd
    os.system(t2wcmd)
  
  #make combine 2016+2017 card
  combo_card = 'datacard_'+cat.replace("_HPHP","").replace("_HPLP","").replace("_LPLP","").replace('_2016','').replace('_2017','')+'.txt'
  combo_workspace = 'workspace_'+cat.replace("_HPHP","").replace("_HPLP","").replace("_LPLP","").replace('_2016','').replace('_2017','')+pseudodata+'.root'
  os.system('rm %s'%combo_card)
  cmd+=' >> %s'%combo_card
  print cmd

  
  
  os.system(cmd)
  t2wcmd = "text2workspace.py %s -o %s"%(combo_card,combo_workspace)
  print t2wcmd
  os.system(t2wcmd)
  
  
  




