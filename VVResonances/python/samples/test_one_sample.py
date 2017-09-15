from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
kreator = ComponentCreator()
signalSamples=[]

QstarToQW_2000=kreator.makeMCComponent("QstarToQW_2000", "/QstarToQW_M-2000_TuneCUETP8M2T4_13TeV-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v2/MINIAODSIM", "CMS", ".*root",1.0)
signalSamples.append(QstarToQW_2000)
