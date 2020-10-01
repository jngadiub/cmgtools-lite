from functionsVV import *
from optparse import OptionParser
from cutsVVdeepW import cuts, HPSF16, HPSF17, LPSF16, LPSF17, dijetbins, HCALbinsMVVSignal, minMJ,maxMJ,binsMJ, minMVV, maxMVV, binsMVV, minMX, maxMX, catVtag, catHtag
## import cuts of the analysis from separate file

# python makeInputsVV.py -p 2016 --run "detector"
# python makeInputsVV.py -p 2016 --run "signorm" --signal "ZprimeWW" --batch False 
# python makeInputsVV.py -p 2016 --run "vjets" --batch False                                                                                                                                      
# python makeInputsVV.py -p 2016 --run "qcdtemplates"
# python makeInputsVV.py -p 2016 --run "qcdkernel"
# python makeInputsVV.py -p 2016 --run "qcdnorm"
# python makeInputsVV.py -p 2016 --run "data"
# python makeInputsVV.py -p 2016 --run "pseudoNOVJETS"
# python makeInputsVV.py -p 2016 --run "pseudoVJETS"                                                                                                                                                                                                                   

parser = OptionParser()
parser.add_option("-p","--period",dest="period",type="int",default=2016,help="run period")
parser.add_option("-s","--sorting",dest="sorting",help="b-tag or random sorting",default='random')
parser.add_option("-b","--binning",action="store_false",dest="binning",help="use dijet binning or not",default=True)
parser.add_option("--batch",action="store_false",dest="batch",help="submit to batch or not ",default=True)
parser.add_option("--trigg",action="store_true",dest="trigg",help="add trigger weights or not ",default=False)
parser.add_option("--run",dest="run",help="decide which parts of the code should be run right now possible optoins are: all : run everything, sigmvv: run signal mvv fit sigmj: run signal mj fit, signorm: run signal norm, vjets: run vjets , qcdtemplates: run qcd templates, qcdkernel: run qcd kernel, qcdnorm: run qcd merge and norm, detector: run detector fit , data : run the data or pseudodata scripts ",default="all")
parser.add_option("--signal",dest="signal",default="BGWW",help="which signal do you want to run? options are BulkGWW, BulkGZZ, WprimeWZ, ZprimeWW, ZprimeZH")


(options,args) = parser.parse_args()

print options

period = options.period
# NB to use the DDT decorrelation method, the ntuples in /eos/cms/store/cmst3/group/exovv/VVtuple/FullRun2VVVHNtuple/deepAK8V2/ should be used
samples= str(period)+"trainingV2/" #for V+jets we use 2017 samples also for 2016 because the 2016 ones are buggy

sorting = options.sorting

submitToBatch = options.batch #Set to true if you want to submit kernels + makeData to batch!
runParallel   = True #Set to true if you want to run all kernels in parallel! This will exit this script and you will have to run mergeKernelJobs when your jobs are done! 

dijetBinning = options.binning
useTriggerWeights = options.trigg

#scale factors to be updated!
HPSF = HPSF16
LPSF = LPSF16
if period == 2017:
    HPSF = HPSF17
    LPSF = LPSF17
    
addOption = ""
if useTriggerWeights: 
    addOption = "-t"
    
if dijetBinning:
    HCALbinsMVV  =" --binsMVV "
    HCALbinsMVV += ','.join(str(e) for e in dijetbins)
else:
    HCALbinsMVV=""
    HCALbinsMVVSignal=""

if period == 2018:
    lumi = 59690. #to be checked! https://twiki.cern.ch/twiki/bin/view/CMS/PdmV2018Analysis
if period == 2017:
    lumi = 41367.    
elif period == 2016:
    lumi = 35900.


#signal regions
if sorting == 'random':
 print "Use random sorting!"
 # two V tag HP                                                                                                                                                                                                                             
 cuts['VV_HPHP'] = '(' +  '&&'.join([catVtag['HP1'],catVtag['HP2']]) + ')'
 cuts['VV_HPLP'] = '(' + '('+  '&&'.join([catVtag['HP1'],catVtag['LP2']]) + ')' + '||' + '(' + '&&'.join([catVtag['HP2'],catVtag['LP1']]) + ')' + ')'

else:
 print "Use b-tagging sorting"
 cuts['VH_HPHP'] = '('+  '&&'.join([catHtag['HP1'],catVtag['HP2']]) + ')'
 cuts['VH_HPLP'] = '('+  '&&'.join([catHtag['HP1'],catVtag['LP2']]) + ')'
 cuts['VH_LPHP'] = '('+  '&&'.join([catHtag['LP1'],catVtag['HP2']]) + ')'
 cuts['VH_LPLP'] = '('+  '&&'.join([catHtag['LP1'],catVtag['LP2']]) + ')'
 cuts['VH_all'] =  '('+  '||'.join([cuts['VH_HPHP'],cuts['VH_HPLP'],cuts['VH_LPHP'],cuts['VH_LPLP']]) + ')'
 cuts['VV_HPHP'] = '(' + '!' + cuts['VH_all'] + '&&' + '(' + '&&'.join([catVtag['HP1'],catVtag['HP2']]) + ')' + ')'
 cuts['VV_HPLP'] = '(' + '!' + cuts['VH_all'] + '&&' + '(' + '('+  '&&'.join([catVtag['HP1'],catVtag['LP2']]) + ')' + '||' + '(' + '&&'.join([catVtag['HP2'],catVtag['LP1']]) + ')' + ')' + ')'



#all categories
categories=['VV_HPLP','VV_HPHP'] #,'VBF_VV_HPHP','VBF_VV_HPLP']
#categories=['VH_HPHP','VH_HPLP','VH_LPHP','VV_HPHP','VV_HPLP'] #,'VBF_VV_HPHP','VBF_VV_HPLP']
#categories=['NP']

                                                                                                                                                                                   
#list of signal samples --> nb, radion and vbf samples to be added
BulkGravWWTemplate="BulkGravToWW_"
VBFBulkGravWWTemplate="VBF_BulkGravToWW_"
BulkGravZZTemplate="BulkGravToZZToZhadZhad_"
ZprimeWWTemplate= "ZprimeToWW_"
ZprimeZHTemplate="ZprimeToZhToZhadhbb_"
WprimeWZTemplate= "WprimeToWZToWhadZhad_"
WprimeWHTemplate="WprimeToWhToWhadhbb_"

# use arbitrary cross section 0.001 so limits converge better
BRZZ=1.*0.001*0.6991*0.6991
BRWW=1.*0.001 #ZprimeWW and GBulkWW are inclusive
BRZH=1.*0.001*0.6991*0.584
BRWZ=1.*0.001*0.6991*0.676
BRWH=1.*0.001*0.676*0.584

#data samples
dataTemplate="JetHT"

#background samples
#nonResTemplate="QCD_Pt-" #low stat herwig
#nonResTemplate="QCD_HT" #medium stat madgraph+pythia
nonResTemplate="QCD_Pt_" #high stat pythia8

#commentin TT for the moment, will need better shaping                                                                                                                                                                                       
#if(period == 2016):                                                                                                                                                                                                                         
#    TTemplate= "TT_Mtt-700to1000,TT_Mtt-1000toInf" #do we need a separate fit for ttbar?                                                                                                                                                    
#else:                                                                                                                                                                                                                                       
#    TTemplate= "TTToHadronic" #do we need a separate fit for ttbar?                                                                                                                                                                         
#WresTemplate= "WJetsToQQ_HT400to600,WJetsToQQ_HT600to800,WJetsToQQ_HT800toInf,"+str(TTemplate)                                                                                                                                              
WresTemplate= "WJetsToQQ_HT400to600,WJetsToQQ_HT600to800,WJetsToQQ_HT800toInf"
ZresTemplate= "ZJetsToQQ_HT400to600,ZJetsToQQ_HT600to800,ZJetsToQQ_HT800toInf"
#resTemplate= "ZJetsToQQ_HT400to600,ZJetsToQQ_HT600to800,ZJetsToQQ_HT800toInf,WJetsToQQ_HT400to600,WJetsToQQ_HT600to800,WJetsToQQ_HT800toInf,"+str(TTemplate)                                                                                
resTemplate= "ZJetsToQQ_HT400to600,ZJetsToQQ_HT600to800,ZJetsToQQ_HT800toInf,WJetsToQQ_HT400to600,WJetsToQQ_HT600to800,WJetsToQQ_HT800toInf"


if dijetBinning:
    minMVV = float(dijetbins[0])
    maxMVV = float(dijetbins[-1])
    binsMVV= len(dijetbins)-1
      

#do not change the order here, add at the end instead
parameters = [cuts,minMVV,maxMVV,minMX,maxMX,binsMVV,HCALbinsMVV,samples,categories,minMJ,maxMJ,binsMJ,lumi,submitToBatch]   
f = AllFunctions(parameters)


#parser.add_option("--signal",dest="signal",default="BGWW",help="which signal do you want to run? options are BGWW, BGZZ, WprimeWZ, ZprimeWW, ZprimeZH")
if options.run.find("all")!=-1 or options.run.find("sig")!=-1:
    if options.signal.find("ZprimeZH")!=-1:
        signal_inuse="ZprimeZH"
        signaltemplate_inuse=ZprimeZHTemplate
        xsec_inuse=BRZH
    elif options.signal.find("BGWW")!=-1 and not 'VBF' in options.signal:
        signal_inuse="BulkGWW"
        signaltemplate_inuse=BulkGravWWTemplate
        xsec_inuse=BRWW
    elif options.signal.find("VBFBGWW")!=-1:
        signal_inuse="VBF_BulkGWW"
        signaltemplate_inuse=VBFBulkGravWWTemplate
        xsec_inuse=BRWW
    elif options.signal.find("BGZZ")!=-1:
        signal_inuse="BulkGZZ"
        signaltemplate_inuse=BulkGravZZTemplate
        xsec_inuse=BRZZ
    elif options.signal.find("ZprimeWW")!=-1:
        signal_inuse="ZprimeWW"
        signaltemplate_inuse=ZprimeWWTemplate
        xsec_inuse=BRWW
    elif options.signal.find("WprimeWZ")!=-1:
        signal_inuse="WprimeWZ"
        signaltemplate_inuse=WprimeWZTemplate
        xsec_inuse=BRWZ
    elif options.signal.find("WprimeWH")!=-1:
        signal_inuse="WprimeWH"
        signaltemplate_inuse=WprimeWHTemplate
        xsec_inuse=BRWH
    else:
        print "signal "+str(options.signal)+" not found!"
        sys.exit()


fixParsSig={"ZprimeZH":{
    "VV_HPLP": {"fixPars":"mean:91.5,n:1.83,n2:4.22,sigmaH:10.7,nH:130", "pol":"mean:pol0,sigma:pol5,alpha:pol5,n:pol0,alpha2:pol5,n2:pol0,meanH:pol4,sigmaH:pol0,alphaH:pol2,nH:pol3,alpha2H:pol3,n2H:pol4"}, 
    "VH_all": {"fixPars":"mean:91.5,n2:4.22,n:128,alphaH:0.51,nH:127","pol":"mean:pol0,sigma:pol5,alpha:pol5,n:pol0,alpha2:pol5,n2:pol0,meanH:pol5,sigmaH:pol7,alphaH:pol0,nH:pol3,alpha2H:pol3,n2H:pol4"}, 
    "VH_HPLP": {"fixPars":"mean:90.5,sigmaH:10,n:5,nH:5", "pol":"mean:pol0,sigma:pol5,alpha:pol5,n:pol0,alpha2:pol5,n2:pol3,meanH:pol5,sigmaH:pol6,alphaH:pol3,nH:pol3,alpha2H:pol5,n2H:pol4"},
    "VH_LPHP": {"fixPars":"mean:90.5,sigmaH:10,n:5,nH:5", "pol":"mean:pol0,sigma:pol5,alpha:pol5,n:pol0,alpha2:pol5,n2:pol3,meanH:pol5,sigmaH:pol6,alphaH:pol3,nH:pol3,alpha2H:pol5,n2H:pol4"},#irene
    "VV_HPHP": {"fixPars":"mean:90.9,alpha:1.1,n:1.83,n2:4.22,alphaH:0.5,nH:120", "pol":"mean:pol0,sigma:pol5,alpha:pol5,n:pol0,alpha2:pol5,n2:pol0,meanH:pol4,sigmaH:pol2,alphaH:pol0,nH:pol3,alpha2H:pol4,n2H:pol4"}, 
    "VH_HPHP": {"fixPars":"n:4.2,nH:132", "pol":"mean:pol3,sigma:pol5,alpha:pol5,n:pol0,alpha2:pol3,n2:pol3,meanH:pol5,sigmaH:pol6,alphaH:pol2,nH:pol0,alpha2H:pol3,n2H:pol4"},"NP":{"fixPars":"nH:129,n:2.4","pol":"mean:pol5,sigma:pol5,alpha:pol5,n:pol0,alpha2:pol3,n2:pol3,meanH:pol5,sigmaH:pol6,alphaH:pol2,nH:pol0,alpha2H:pol3,n2H:pol4"}},
"BulkGWW":{ "VV_HPLP": {"fixPars":"alpha:1.125,n:2,n2:2","pol":"mean:pol4,sigma:pol3,alpha:pol3,n:pol0,alpha2:pol3,n2:pol3"},
            "VV_HPHP": {"fixPars":"alpha:1.08,n:6,n2:2", "pol":"mean:pol5,sigma:pol5,alpha:pol0,n:pol0,alpha2:pol5,n2:pol0"},
            "VH_HPLP": {"fixPars":"alpha:1.125,n:2,n2:2","pol":"mean:pol4,sigma:pol3,alpha:pol3,n:pol0,alpha2:pol3,n2:pol3"},
            "VH_HPHP": {"fixPars":"n:60,alpha:0.76", "pol":"mean:pol5,sigma:pol6,alpha:pol0,n:pol0,alpha2:pol5,n2:pol5"},
            "VH_LPHP": {"fixPars":"alpha:1.125,n:2,n2:2","pol":"mean:pol4,sigma:pol3,alpha:pol3,n:pol0,alpha2:pol3,n2:pol3"},"NP":{"fixPars":"n:5","pol":"mean:pol4,sigma:pol4,alpha:pol5,n:pol0,alpha2:pol3,n2:pol3"}}, #VH_LPHP irene
"BulkGZZ":{"VV_HPLP":{"fixPars":"alpha:1.024,n:3.25","pol":"mean:pol4,sigma:pol3,alpha:pol0,n:pol0,alpha2:pol3,n2:pol4"},
           "VV_HPHP":{"fixPars":"n2:4.8,n:2.8","pol":"mean:pol5,sigma:pol5,alpha:pol5,n:pol0,alpha2:pol3,n2:pol0"},
           "VH_HPLP":{"fixPars":"alpha:1.024,n:3.25","pol":"mean:pol4,sigma:pol3,alpha:pol0,n:pol0,alpha2:pol3,n2:pol4"},
           "VH_HPHP":{"fixPars":"n:64","pol":"mean:pol3,sigma:pol5,alpha:pol5,n:pol0,alpha2:pol3,n2:pol3"},"NP":{"fixPars":"n:3.6,alpha:1","pol":"mean:pol5,sigma:pol6,alpha:pol7,n:pol0,alpha2:pol5,n2:pol4"}},
"ZprimeWW":{"VV_HPLP": {"fixPars":"alpha:1.125","pol":"mean:pol5,sigma:pol5,alpha:pol0,n:pol3,alpha2:pol3,n2:pol3"},
            "VV_HPHP": {"fixPars":"alpha:1.083,n:3.5,n2:2.3","pol":"mean:pol5,sigma:pol4,alpha:pol0,n:pol0,alpha2:pol5,n2:pol0"},
            "VH_HPLP": {"fixPars":"n:5","pol":"mean:pol5,sigma:pol5,alpha:pol5,n:pol0,alpha2:pol5,n2:pol3"},
            "VH_HPHP": {"fixPars":"n:1.2,alpha:1.22", "pol":"mean:pol6,sigma:pol4,alpha:pol0,n:pol0,alpha2:pol5,n2:pol3"},"NP":{"fixPars":"n:14","pol":"mean:pol4,sigma:pol3,alpha:pol3,n:pol0,alpha2:pol3,n2:pol3"}},
"WprimeWZ":{"VV_HPLP":{"fixPars":"n:2.3","pol":"mean:pol3,sigma:pol3,alpha:pol3,n:pol0,alpha2:pol3,n2:pol1"},
            "VV_HPHP":{"fixPars":"n:2,n2:2,alpha:1.505", "pol":"mean:pol3,sigma:pol3,alpha:pol3,n:pol0,alpha2:pol3,n2:pol1"},
            "VH_HPLP":{"fixPars":"n:2.3","pol":"mean:pol3,sigma:pol3,alpha:pol3,n:pol0,alpha2:pol3,n2:pol1"},
            "VH_HPHP":{"fixPars":"n:0.24,alpha:1.6", "pol":"mean:pol3,sigma:pol5,alpha:pol3,n:pol0,alpha2:pol3,n2:pol3"},"NP":{"fixPars":"n:2.6,alpha:1.4","pol":"mean:pol5,sigma:pol5,alpha:pol0,n:pol0,alpha2:pol4,n2:pol7"}}, 
"WprimeWH":{
    "VV_HPLP": {"fixPars":"mean:91.5,n:1.83,n2:4.22,sigmaH:10.7,nH:130", "pol":"mean:pol0,sigma:pol5,alpha:pol5,n:pol0,alpha2:pol5,n2:pol0,meanH:pol4,sigmaH:pol0,alphaH:pol2,nH:pol3,alpha2H:pol3,n2H:pol4"}, 
    "VH_all": {"fixPars":"mean:91.5,n2:4.22,n:128,alphaH:0.51,nH:127","pol":"mean:pol0,sigma:pol5,alpha:pol5,n:pol0,alpha2:pol5,n2:pol0,meanH:pol5,sigmaH:pol7,alphaH:pol0,nH:pol3,alpha2H:pol3,n2H:pol4"}, 
    "VH_HPLP": {"fixPars":"mean:90.5,sigmaH:10,n:5,nH:5", "pol":"mean:pol0,sigma:pol5,alpha:pol5,n:pol0,alpha2:pol5,n2:pol3,meanH:pol5,sigmaH:pol6,alphaH:pol3,nH:pol3,alpha2H:pol5,n2H:pol4"},
    "VH_LPHP": {"fixPars":"mean:90.5,sigmaH:10,n:5,nH:5", "pol":"mean:pol0,sigma:pol5,alpha:pol5,n:pol0,alpha2:pol5,n2:pol3,meanH:pol5,sigmaH:pol6,alphaH:pol3,nH:pol3,alpha2H:pol5,n2H:pol4"},#irene
    "VV_HPHP": {"fixPars":"mean:90.9,alpha:1.1,n:1.83,n2:4.22,alphaH:0.5,nH:120", "pol":"mean:pol0,sigma:pol5,alpha:pol5,n:pol0,alpha2:pol5,n2:pol0,meanH:pol4,sigmaH:pol2,alphaH:pol0,nH:pol3,alpha2H:pol4,n2H:pol4"}, 
    "VH_HPHP": {"fixPars":"n:4.2,nH:132", "pol":"mean:pol3,sigma:pol5,alpha:pol5,n:pol0,alpha2:pol3,n2:pol3,meanH:pol5,sigmaH:pol6,alphaH:pol2,nH:pol0,alpha2H:pol3,n2H:pol4"},"NP":{"fixPars":"nH:129,n:2.4,alphaH:0.6,alpha:1.14","pol":"mean:pol5,sigma:pol5,alpha:pol0,n:pol0,alpha2:pol3,n2:pol3,meanH:pol5,sigmaH:pol6,alphaH:pol0,nH:pol0,alpha2H:pol3,n2H:pol4"}}}



fixParsSigMVV={"ZprimeZH":{"fixPars":"ALPHA2:2.42,N1:126.5", "pol":"MEAN:pol1,SIGMA:pol1,N1:pol0,ALPHA1:pol5,N2:pol3,ALPHA2:pol0,corr_mean:pol1,corr_sigma:pol1"},
               "WprimeWH":{"fixPars":"ALPHA2:2.42,N1:126.5", "pol":"MEAN:pol1,SIGMA:pol1,N1:pol0,ALPHA1:pol5,N2:pol3,ALPHA2:pol0,corr_mean:pol1,corr_sigma:pol1"},#irene
               "WprimeWZ":{"fixPars":"N1:7,N2:4","pol": "MEAN:pol1,SIGMA:pol3,N1:pol0,ALPHA1:pol7,N2:pol0,ALPHA2:pol5,corr_mean:pol1,corr_sigma:pol1"},
               "BulkGWW":{"fixPars":"N1:1.61364,N2:4.6012","pol":"MEAN:pol1,SIGMA:pol6,ALPHA1:pol5,N1:pol0,ALPHA2:pol4,N2:pol0"},
               "BulkGZZ":{"fixPars":"N1:1.61364,N2:4.6012","pol":"MEAN:pol1,SIGMA:pol6,ALPHA1:pol5,N1:pol0,ALPHA2:pol4,N2:pol0"},
               "ZprimeWW":{"fixPars":"N1:1.61364,N2:4.6012","pol":"MEAN:pol1,SIGMA:pol6,ALPHA1:pol5,N1:pol0,ALPHA2:pol4,N2:pol0"}}


if options.run.find("all")!=-1 or options.run.find("sig")!=-1:
    print "run signal"
    if options.run.find("all")!=-1 or options.run.find("mj")!=-1:
        print "mj fit for signal "
        if sorting == "random":
            if signal_inuse.find("H")!=-1: 
                f.makeSignalShapesMJ("JJ_Vjet_"+str(signal_inuse)+"_"+str(period),signaltemplate_inuse,'random', fixParsSig[signal_inuse],"jj_random_mergedVTruth==1")
                f.makeSignalShapesMJ("JJ_Hjet_"+str(signal_inuse)+"_"+str(period),signaltemplate_inuse,'random',fixParsSig[signal_inuse],"jj_random_mergedHTruth==1")
            else:
                f.makeSignalShapesMJ("JJ_"+str(signal_inuse)+"_"+str(period),signaltemplate_inuse,'random',fixParsSig[signal_inuse.replace('VBF_','')]) 
        else:
            if signal_inuse.find("H")!=-1: 
                f.makeSignalShapesMJ("JJ_Vjet_"+str(signal_inuse)+"_"+str(period),signaltemplate_inuse,'l1',fixParsSig[signal_inuse],"jj_l1_mergedVTruth==1")
                f.makeSignalShapesMJ("JJ_Vjet_"+str(signal_inuse)+"_"+str(period),signaltemplate_inuse,'l2',fixParsSig[signal_inuse],"jj_l2_mergedVTruth==1")
                f.makeSignalShapesMJ("JJ_Hjet_"+str(signal_inuse)+"_"+str(period),signaltemplate_inuse,'l1',fixParsSig[signal_inuse],"jj_l1_mergedHTruth==1")
                f.makeSignalShapesMJ("JJ_Hjet_"+str(signal_inuse)+"_"+str(period),signaltemplate_inuse,'l2',fixParsSig[signal_inuse],"jj_l2_mergedHTruth==1")
            else:
                f.makeSignalShapesMJ("JJ_"+str(signal_inuse)+"_"+str(period),signaltemplate_inuse,'l1',fixParsSig[signal_inuse])
                f.makeSignalShapesMJ("JJ_"+str(signal_inuse)+"_"+str(period),signaltemplate_inuse,'l2',fixParsSig[signal_inuse])
    if options.run.find("all")!=-1 or options.run.find("mvv")!=-1:
        print "mjj fit for signal ",signal_inuse
        if signal_inuse.find("H")!=-1:
            f.makeSignalShapesMVV("JJ_"+str(signal_inuse)+"_"+str(period),signaltemplate_inuse,fixParsSigMVV[signal_inuse],"( jj_l1_softDrop_mass <= 150 && jj_l1_softDrop_mass > 105 && jj_l2_softDrop_mass <= 105 && jj_l2_softDrop_mass > 65) || (jj_l2_softDrop_mass <= 150 && jj_l2_softDrop_mass > 105 && jj_l1_softDrop_mass <= 105 && jj_l1_softDrop_mass > 65) ")
        elif signal_inuse.find("WZ")!=-1:
            f.makeSignalShapesMVV("JJ_"+str(signal_inuse)+"_"+str(period),signaltemplate_inuse,fixParsSigMVV[signal_inuse],"(jj_l1_softDrop_mass <= 105 && jj_l1_softDrop_mass > 85 && jj_l2_softDrop_mass <= 85 && jj_l2_softDrop_mass >= 65) || (jj_l2_softDrop_mass <= 105 && jj_l2_softDrop_mass > 85 && jj_l1_softDrop_mass <= 85 && jj_l1_softDrop_mass >= 65)")
        else:
            f.makeSignalShapesMVV("JJ_"+str(signal_inuse)+"_"+str(period),signaltemplate_inuse,fixParsSigMVV[signal_inuse.replace('VBF_','')])
    

    if options.run.find("all")!=-1 or options.run.find("norm")!=-1:
        print "fit signal norm "
        f.makeSignalYields("JJ_"+str(signal_inuse)+"_"+str(period),signaltemplate_inuse,xsec_inuse,{'VH_HPHP':HPSF*HPSF,'VH_HPLP':HPSF*LPSF,'VH_LPHP':HPSF*LPSF,'VH_LPLP':LPSF*LPSF,'VV_HPHP':HPSF*HPSF,'VV_HPLP':HPSF*LPSF,'VH_all':HPSF*HPSF+HPSF*LPSF})


if options.run.find("all")!=-1 or options.run.find("detector")!=-1:
    print "make Detector response"
    f.makeDetectorResponse("nonRes","JJ_"+str(period),nonResTemplate,cuts['nonres'])

if options.run.find("all")!=-1 or options.run.find("qcd")!=-1:
    print "Make nonresonant QCD templates and normalization"
    if runParallel and submitToBatch:
        if options.run.find("all")!=-1 or options.run.find("templates")!=-1:
            wait = False
            f.makeBackgroundShapesMVVKernel("nonRes","JJ_"+str(period),nonResTemplate,cuts['nonres'],"1D",wait)
            f.makeBackgroundShapesMVVConditional("nonRes","JJ_"+str(period),nonResTemplate,'l1',cuts['nonres'],"2Dl1",wait)
            f.makeBackgroundShapesMVVConditional("nonRes","JJ_"+str(period),nonResTemplate,'l2',cuts['nonres'],"2Dl2",wait)
            print "Exiting system! When all jobs are finished, please run mergeKernelJobs below"
            sys.exit()
        elif options.run.find("all")!=-1 or options.run.find("kernel")!=-1:
            f.mergeKernelJobs("nonRes","JJ_"+str(period))
	    f.mergeBackgroundShapes("nonRes","JJ_"+str(period))
    else:
        if options.run.find("all")!=-1 or options.run.find("templates")!=-1:
            wait = True
            f.makeBackgroundShapesMVVKernel("nonRes","JJ_"+str(period),nonResTemplate,cuts['nonres'],"1D",wait)
            f.makeBackgroundShapesMVVConditional("nonRes","JJ_"+str(period),nonResTemplate,'l1',cuts['nonres'],"2Dl1",wait)
            f.makeBackgroundShapesMVVConditional("nonRes","JJ_"+str(period),nonResTemplate,'l2',cuts['nonres'],"2Dl2",wait)
            f.mergeBackgroundShapes("nonRes","JJ_"+str(period))
    if options.run.find("all")!=-1 or options.run.find("norm")!=-1:
        f.makeNormalizations("nonRes","JJ_"+str(period),nonResTemplate,0,cuts['nonres'],"nRes")

if options.run.find("all")!=-1 or options.run.find("vjets")!=-1:    
    print "for V+jets"
    print "first we fit"
    f.fitVJets("JJ_WJets",resTemplate,1.,1.)
    print "and then we make kernels"
    print " did you run Detector response  for this period? otherwise the kernels steps will not work!"
    print "first kernel W"
    f.makeBackgroundShapesMVVKernel("WJets","JJ_"+str(period),WresTemplate,cuts['nonres'],"1D",0,1.,1.)
    print "then kernel Z"
    f.makeBackgroundShapesMVVKernel("ZJets","JJ_"+str(period),ZresTemplate,cuts['nonres'],"1D",0,1.,1.)
    print "then norm W"
    f.makeNormalizations("WJets","JJ_"+str(period),WresTemplate,0,cuts['nonres'],"nRes","",HPSF,LPSF)
    print "then norm Z"
    f.makeNormalizations("ZJets","JJ_"+str(period),ZresTemplate,0,cuts['nonres'],"nRes","",HPSF,LPSF)
    f.makeNormalizations("TTJets","JJ_"+str(period),TTemplate,0,cuts['nonres'],"nRes","") # ... so we do not need this


if options.run.find("all")!=-1 or options.run.find("data")!=-1:
    print " Do data "
    f.makeNormalizations("data","JJ_"+str(period),dataTemplate,1,'1',"normD") #run on data. Currently run on pseudodata only (below)
if options.run.find("all")!=-1 or options.run.find("pseudoNOVJETS")!=-1:
    print " Do pseudodata without vjets"
    from modules.submitJobs import makePseudoData
    for p in categories: makePseudoData("JJ_"+str(period)+"_nonRes_%s.root"%p,"save_new_shapes_"+str(period)+"_pythia_%s_3D.root"%p,"pythia","JJ_PDnoVjets_%s.root"%p,lumi)
if options.run.find("all")!=-1 or options.run.find("pseudoVJETS")!=-1:
    print " Do pseudodata with vjets: DID YOU PRODUCE THE WORKSPACE BEFORE???"
    from modules.submitJobs import makePseudoDataVjets
    for p in categories: makePseudoDataVjets("debugSensitivityBulkGWW/VVinclu/JJ_"+str(period)+"_nonRes_%s.root"%p,"debugSensitivityBulkGWW/VVinclu/save_new_shapes_"+str(period)+"_pythia_%s_3D.root"%p,"pythia","JJ_PDVjets_%s.root"%p,lumi,"results_2016_VVinclu_deepAK8WDDT_noCutTemplates/workspace_JJ_BulkGWW_"+p+"_13TeV_"+str(period)+"_scheme2_VVinclu_deepAK8WDDT_VjetsPrep.root",period,p)
#    for p in categories: makePseudoDataVjets("results_"+str(period)+"/JJ_"+str(period)+"_nonRes_%s.root"%p,"results_"+str(period)+"/save_new_shapes_"+str(period)+"_pythia_%s_3D.root"%p,"pythia","JJ_PDVjets_%s.root"%p,lumi,"results_"+str(period)+"/workspace_JJ_BulkGWW_"+p+"_13TeV_"+str(period)+"_VV_VH_scheme2_deepAK8_W_0p05_0p10_ZHbb_0p05_0p10_DDT_defaultMaps2016_fullStats_prepVjets.root",period,p)


print " ########## I did everything I could! ###### "