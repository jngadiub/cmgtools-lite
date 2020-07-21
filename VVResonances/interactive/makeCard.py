from tools.DatacardTools import *
import sys,os
import ROOT
import json
ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")
from CMGTools.VVResonances.statistics.DataCardMaker import DataCardMaker
from optparse import OptionParser
import cuts


parser = OptionParser()
parser.add_option("-p","--period",dest="period",default="2016,2017",help="run period")
parser.add_option("--pseudodata",dest="pseudodata",help="make cards with real data or differen pseudodata sets: Vjets, ZprimeZH etc",default='')
parser.add_option("--signal",dest="signal",default="BulkGWW,BulkGZZ,ZprimeWW,ZprimeZH,WprimeWH,WprimeWZ",help="which signal do you want to run? options are BulkGWW, BulkGZZ, WprimeWZ, ZprimeWW, ZprimeZH")
parser.add_option("--outlabel",dest="outlabel",help="lebel for output workspaces for example sigonly_M4500",default='')
parser.add_option("-c","--category",dest="category",default="VV_HPLP,VV_HPHP,VH_HPLP,VH_HPHP,VH_LPHP",help="run period")
parser.add_option("--combo",dest="combo",default=True,help="If True inputs from the 3 years combined will be used")


(options,args) = parser.parse_args()

cmd='combineCards.py '



#### to create the preparatory WS for pseudodata with Vjets: pseudodata = "" & doVjets=True 
pseudodata = options.pseudodata

outlabel = options.outlabel


purities= options.category.split(",")

signals = options.signal.split(",")
print "signals ",signals
doVjets= True
sf_qcd=1.
if outlabel.find("sigonly")!=-1 or outlabel.find("qcdonly")!=-1: doVjets = False
if outlabel.find("sigonly")!=-1 or outlabel.find("Vjetsonly")!=-1: sf_qcd = 0.00001


# vtag uncertainty is added through the migrationunc.json file 
# all other uncertainties and SF from one place: defined in init_VV_VH.json imported via the class defined in cuts.py
ctx = cuts.cuts("init_VV_VH.json",options.period,"dijetbins_random")
#ctx17 = cuts.cuts("init_VV_VH.json","2017","dijetbins_random")
#ctx18 = cuts.cuts("init_VV_VH.json","2018","dijetbins_random")

lumi = ctx.lumi #{'2016':ctx16.lumi["2016"],'2017':ctx17.lumi["2017"], '2018':ctx18.lumi}
lumi_unc = ctx.lumi_unc #{'2016':ctx16.lumi_unc,'2017':ctx17.lumi_unc, '2018':ctx18.lumi_unc}

print "lumi ",lumi
print type(lumi)



# what are there scales?
#scales = {"2017" :[ctx17.W_HPmassscale,ctx17.W_LPmassscale], "2016":[ctx16.W_HPmassscale,ctx16.W_LPmassscale], "2018":[ctx18.W_HPmassscale,ctx18.W_LPmassscale]}
#scalesHiggs = {"2017" :[ctx17.H_HPmassscale,ctx17.H_LPmassscale], "2016":[ctx16.H_HPmassscale,ctx16.H_LPmassscale], "2018":[ctx18.H_HPmassscale,ctx18.H_LPmassscale]}

scales = {"2017" :[1,1], "2016":[1,1], "2018":[1,1], "Run2":[1,1]}
scalesHiggs = {"2017" :[1,1], "2016":[1,1], "2018":[1,1]}

#quick fix to add VH !!!
vtag_pt_dependence = ctx.vtag_pt_dependence #{"2016" : ctx.vtag_pt_dependence["2016"],"2017" : ctx.vtag_pt_dependence["2017"],"2018" : ctx.vtag_pt_dependence["2018"]}



datasets= options.period.split(",")
resultsDir = {year:'results_'+year for year in datasets}

if len(datasets) == 3 and options.combo == True:
  datasets = []
  datasets.append("Run2")
  resultsDir.update({"Run2" : "results_Run2"})
print "datasets ",datasets
print "result dir ",resultsDir






doCorrelation = True 
Tools = DatacardTools(scales,scalesHiggs,vtag_pt_dependence,lumi_unc,sf_qcd,pseudodata,outlabel,doCorrelation)


for sig in signals:

  cmd ="combineCards.py"
  for dataset in datasets:
    print dataset
    cmd_combo="combineCards.py"
    for p in purities:

      ncontrib = 0
      print dataset," has lumi ",lumi[dataset]
      print type(lumi[dataset])
      
      cat='_'.join(['JJ',sig,p,'13TeV_'+dataset])
      card=DataCardMaker('',p,'13TeV_'+dataset,lumi[dataset],'JJ',cat)
      cmd=cmd+" "+cat.replace('_%s'%sig,'')+'=datacard_'+cat+'.txt '
      cmd_combo=cmd_combo+" "+cat.replace('_%s'%sig,'')+'=datacard_'+cat+'.txt '
      cardName='datacard_'+cat+'.txt '
      workspaceName='workspace_'+cat+outlabel+'.root'

      Tools.AddSignal(card,dataset,p,sig,resultsDir[dataset],ncontrib)
      ncontrib+=1

      if doVjets:
        print "##########################       including W/Z jets in datacard      ######################"
        rootFileMVV = resultsDir[dataset]+'/JJ_%s_WJets_MVV_'%dataset+p+'.root'    
        rootFileNorm = resultsDir[dataset]+'/JJ_%s_WJets_%s.root'%(dataset,p)
        print rootFileMVV," ",rootFileNorm
        Tools.AddWResBackground(card,dataset,p,rootFileMVV,rootFileNorm,resultsDir[dataset],ncontrib)
        ncontrib+=1
        print " W jets done, now do Z"         
        rootFileMVV = resultsDir[dataset]+'/JJ_%s_ZJets_MVV_'%dataset+p+'.root'
        rootFileNorm = resultsDir[dataset]+"/JJ_%s_ZJets_%s.root"%(dataset,p)
        Tools.AddZResBackground(card,dataset,p,rootFileMVV,rootFileNorm,resultsDir[dataset],ncontrib)
        ncontrib+=1

      #rootFile3DPDF = resultsDir[dataset]+'/JJ_2016_nonRes_3D_VV_HPLP.root'
      print "##########################       including QCD in datacard      ######################"
      #rootFile3DPDF = resultsDir[dataset]+'/JJ_%s_nonRes_3D_'%dataset+'NP.root'            
      rootFile3DPDF = resultsDir[dataset]+"/save_new_shapes_%s_pythia_"%dataset+p+"_3D.root"
      #rootFile3DPDF = resultsDir[dataset]+"/save_new_shapes_%s_pythia_"%dataset+"VVVH_all"+"_3D.root"
      print "rootFile3DPDF ",rootFile3DPDF
      rootFileNorm = resultsDir[dataset]+"/JJ_%s_nonRes_"%dataset+p+".root"   
      print "rootFileNorm ",rootFileNorm

      Tools.AddNonResBackground(card,dataset,p,rootFile3DPDF,rootFileNorm,ncontrib) 
      print "##########################       QCD added in datacard      ######################"


#      rootFileData = resultsDir[dataset]+"/JJ_%s_nonRes_3D_%s.root"%(dataset,p) #use this only to prepare workspace for making pseudo data with vjets
      rootFileData = resultsDir[dataset]+"/JJ_%s_nonRes_3D_NP.root"%(dataset) #use this only to prepare workspace for making pseudo data with vjets
      histName="histo"
      scaleData=lumi[dataset]

      #if you run on real data or pseudodata
#      rootFileData = resultsDir[dataset]+"/JJ_"+p+".root"
#      histName="data"
#      scaleData=1.0 

      if pseudodata=="noVjets":
        print "Using pseudodata without vjets"
        rootFileData = resultsDir[dataset]+"/JJ_PDnoVjets_"+p+".root"
        histName="datah"
        scaleData=1.0
      if pseudodata=="Vjets":
        print "Using pseudodata with vjets"
        rootFileData = resultsDir[dataset]+"/JJ_"+dataset+"_PDVjets_"+p+".root"
        histName="data"
        scaleData=1.0
      if pseudodata==sig:
       rootFileData = resultsDir[dataset]+"/pseudodata_sigOnly_"+dataset+"_"+sig+"_"+p+"_"+"M"+outlabel.split("_M")[1]+".root"
       histName="data_obs" 
       scaleData=1.0
      Tools.AddData(card,rootFileData,histName,scaleData)

      print "##########################       data/pseudodata added in datacard      ######################"  
       
      Tools.AddSigSystematics(card,sig,dataset,p,1)
      Tools.AddResBackgroundSystematics(card,p)
      Tools.AddNonResBackgroundSystematics(card,p)
      #Tools.AddTaggingSystematics(card,sig,dataset,p,resultsDir[dataset]+'/migrationunc.json')
      print "##########################       systematics added in datacard      ######################"  



        
      card.makeCard()
      t2wcmd = "text2workspace.py %s -o %s"%(cardName,workspaceName)
      print t2wcmd
      os.system(t2wcmd)
    del card

    print "#####################################"

    #make combined 
    if len(purities)>1:
      print "#######     going to combine purity categories: ",purities    
      combo_card = cardName.replace("VV_HPHP","").replace("VV_HPLP","").replace("VV_LPLP","").replace("VH_HPHP","").replace("VH_HPLP","").replace("VH_LPHP","").replace("VH_LPLP","")
      combo_workspace = workspaceName.replace("VV_HPHP","").replace("VV_HPLP","").replace("VV_LPLP","").replace("VH_HPHP","").replace("VH_HPLP","").replace("VH_LPHP","").replace("VH_LPLP","")
      os.system('rm %s'%combo_card)
      cmd_combo+=' >> %s'%combo_card
      print cmd_combo
      os.system(cmd_combo)
      t2wcmd = "text2workspace.py %s -o %s"%(combo_card,combo_workspace)
      print t2wcmd
      os.system(t2wcmd)
      print "#####################################"

  if len(datasets)>1:   
    #make combine 2016+2017 card
    print "more than one year, making combined cards"
    combo_card = 'datacard_'+cat.replace("_HPHP","").replace("_HPLP","").replace("_LPLP","").replace('_2016','').replace('_2017','')+'.txt'
    combo_workspace = 'workspace_'+cat.replace("_HPHP","").replace("_HPLP","").replace("_LPLP","").replace('_2016','').replace('_2017','')+'.root'
    os.system('rm %s'%combo_card)
    cmd+=' >> %s'%combo_card
    print cmd
    os.system(cmd)
    t2wcmd = "text2workspace.py %s -o %s"%(combo_card,combo_workspace)
    print t2wcmd
    os.system(t2wcmd)


