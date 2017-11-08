from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
kreator = ComponentCreator()
QCDbackgroundSamples=[] 

QCD_Pt_15to7000 = kreator.makeMCComponent("QCD_Pt-15to7000","/QCD_Pt-15to7000_TuneCUETHS1_FlatP6_13TeV_herwigpp/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM","CMS",".*root",2.022100000e+09)
QCDbackgroundSamples.append(QCD_Pt_15to7000)

QCD_Pt_170to300       = kreator.makeMCComponent("QCD_Pt_170to300"      , "/QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM"       , "CMS", ".*root", 117276)
QCD_Pt_170to300_ext   = kreator.makeMCComponent("QCD_Pt_170to300_ext"  , "/QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM"  , "CMS", ".*root", 117276)
QCD_Pt_300to470       = kreator.makeMCComponent("QCD_Pt_300to470"      , "/QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM"       , "CMS", ".*root", 7823)
QCD_Pt_300to470_ext   = kreator.makeMCComponent("QCD_Pt_300to470_ext"  , "/QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM"  , "CMS", ".*root", 7823)
QCDbackgroundSamples.append(QCD_Pt_170to300)
QCDbackgroundSamples.append(QCD_Pt_170to300_ext)
QCDbackgroundSamples.append(QCD_Pt_300to470)
QCDbackgroundSamples.append(QCD_Pt_300to470_ext)

QCD_Pt_470to600       = kreator.makeMCComponent("QCD_Pt_470to600"      , "/QCD_Pt_470to600_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM"       , "CMS", ".*root", 648.2)
QCD_Pt_470to600_ext   = kreator.makeMCComponent("QCD_Pt_470to600_ext"  , "/QCD_Pt_470to600_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_backup_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root", 648.2)
QCD_Pt_600to800       = kreator.makeMCComponent("QCD_Pt_600to800"      , "/QCD_Pt_600to800_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM"       , "CMS", ".*root", 186.9)
QCD_Pt_600to800_ext   = kreator.makeMCComponent("QCD_Pt_600to800_ext"  , "/QCD_Pt_600to800_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM"  , "CMS", ".*root", 186.9)
QCD_Pt_600to800_ext2  = kreator.makeMCComponent("QCD_Pt_600to800_ext2" , "/QCD_Pt_600to800_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_backup_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root", 186.9)
QCDbackgroundSamples.append(QCD_Pt_470to600)
QCDbackgroundSamples.append(QCD_Pt_470to600_ext) #ok
QCDbackgroundSamples.append(QCD_Pt_600to800) #ok
QCDbackgroundSamples.append(QCD_Pt_600to800_ext) 
QCDbackgroundSamples.append(QCD_Pt_600to800_ext2) #ok

QCD_Pt_800to1000      = kreator.makeMCComponent("QCD_Pt_800to1000"     , "/QCD_Pt_800to1000_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM"      , "CMS", ".*root", 32.293)
QCD_Pt_800to1000_ext  = kreator.makeMCComponent("QCD_Pt_800to1000_ext" , "/QCD_Pt_800to1000_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM" , "CMS", ".*root", 32.293)
QCD_Pt_1000to1400     = kreator.makeMCComponent("QCD_Pt_1000to1400"    , "/QCD_Pt_1000to1400_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM"     , "CMS", ".*root", 9.4183)
QCD_Pt_1000to1400_ext = kreator.makeMCComponent("QCD_Pt_1000to1400_ext", "/QCD_Pt_1000to1400_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM", "CMS", ".*root", 9.4183)
QCDbackgroundSamples.append(QCD_Pt_800to1000)
QCDbackgroundSamples.append(QCD_Pt_800to1000_ext)
QCDbackgroundSamples.append(QCD_Pt_1000to1400)
QCDbackgroundSamples.append(QCD_Pt_1000to1400_ext)

QCD_Pt_1400to1800     = kreator.makeMCComponent("QCD_Pt_1400to1800"    , "/QCD_Pt_1400to1800_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM"     , "CMS", ".*root", 0.84265)
QCD_Pt_1400to1800_ext = kreator.makeMCComponent("QCD_Pt_1400to1800_ext", "/QCD_Pt_1400to1800_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM", "CMS", ".*root", 0.84265)
QCD_Pt_1800to2400     = kreator.makeMCComponent("QCD_Pt_1800to2400"    , "/QCD_Pt_1800to2400_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM"     , "CMS", ".*root", 0.114943)
QCD_Pt_1800to2400_ext = kreator.makeMCComponent("QCD_Pt_1800to2400_ext", "/QCD_Pt_1800to2400_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM", "CMS", ".*root", 0.114943)
QCDbackgroundSamples.append(QCD_Pt_1400to1800)
QCDbackgroundSamples.append(QCD_Pt_1400to1800_ext)
QCDbackgroundSamples.append(QCD_Pt_1800to2400)
QCDbackgroundSamples.append(QCD_Pt_1800to2400_ext)

QCD_Pt_2400to3200     = kreator.makeMCComponent("QCD_Pt_2400to3200"    , "/QCD_Pt_2400to3200_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM"     , "CMS", ".*root", 0.00682981)
QCD_Pt_2400to3200_ext = kreator.makeMCComponent("QCD_Pt_2400to3200_ext", "/QCD_Pt_2400to3200_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM", "CMS", ".*root", 0.00682981)
QCD_Pt_3200toInf      = kreator.makeMCComponent("QCD_Pt_3200toInf"     , "/QCD_Pt_3200toInf_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v3/MINIAODSIM"      , "CMS", ".*root", 0.000165445)
QCDbackgroundSamples.append(QCD_Pt_2400to3200)
QCDbackgroundSamples.append(QCD_Pt_2400to3200_ext)
QCDbackgroundSamples.append(QCD_Pt_3200toInf)
