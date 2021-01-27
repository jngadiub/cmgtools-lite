import json, sys, math, time
from array import array
import ROOT
from ROOT import *

if len(sys.argv) < 2:
 print "Please specify decay channel (WW or ZZ)"
 sys.exit()

channel = sys.argv[1]

print "********* Make Radion->%s cross section graphs***********"%channel

yTH = array('d',[])
yTHUp = array('d',[])
yTHDown = array('d',[])
yTHUncs = array('d',[])
masses = array('d',[])
massesUncs = array('d',[])

Fxsec = open('GF_NLO_13TeV_LR_3TeV_kl_35.txt','r')
Fbr = open('Decay_short_kl_35_arxiv1110.6452.txt','r')
brs = Fbr.readlines()

for i,l in enumerate(Fxsec.readlines()):

 if i<1 or i > len(brs)-1: continue
 if float(l.split('\t')[0]) != float(brs[i].split('\t')[0]): continue
 
 masses.append(float(l.split('\t')[0])/1000.)
 massesUncs.append(float(l.split('\t')[0])/1000.)
 
 if channel=='WW': br = float(brs[i].split('\t')[4])
 else: br = float(brs[i].split('\t')[3])
 sigma = float(l.split('\t')[1])
 uncUp = 1.0 + float(l.split('\t')[5])/100.
 uncDown = 1.0 - float(l.split('\t')[5])/100.
 
 
 yTH.append(math.log(sigma*br))
 yTHUp.append(math.log(uncUp*sigma*br))
 yTHDown.append(math.log(uncDown*sigma*br))
 print "mass",masses[-1],"th",yTH[-1],"down",yTHDown[-1],"up",yTHUp[-1]

Fxsec.close()
Fbr.close()
  
graphTHLog = ROOT.TGraph(len(masses),masses,yTH)
graphTHUPLog = ROOT.TGraph(len(masses),masses,yTHUp)
graphTHDOWNLog = ROOT.TGraph(len(masses),masses,yTHDown)

new_xsec = array('d',[])
new_xsecUp = array('d',[])
new_xsecDown = array('d',[])
for i in range(graphTHLog.GetN()):
 x = ROOT.Double(0.)
 y = ROOT.Double(0.)
 graphTHLog.GetPoint(i,x,y)
 new_xsec.append(y)
for i in range(graphTHUPLog.GetN()):
 x = ROOT.Double(0.)
 y = ROOT.Double(0.)
 graphTHUPLog.GetPoint(i,x,y)
 new_xsecUp.append(y) 
for i in range(graphTHDOWNLog.GetN()):
 x = ROOT.Double(0.)
 y = ROOT.Double(0.)
 graphTHDOWNLog.GetPoint(i,x,y)
 new_xsecDown.append(y)
    
new_masses = [3.5,4.0,4.5,5.0,5.5,6.0,6.5]
for m in new_masses:
 masses.append(m)
 massesUncs.append(m)
 new_xsec.append(graphTHLog.Eval(m))
 new_xsecUp.append(graphTHUPLog.Eval(m))
 new_xsecDown.append(graphTHDOWNLog.Eval(m))

graphTHLog = ROOT.TGraph(len(masses),masses,new_xsec)
graphTHUPLog = ROOT.TGraph(len(masses),masses,new_xsecUp)
graphTHDOWNLog = ROOT.TGraph(len(masses),masses,new_xsecDown)

for i,v in enumerate(new_xsec):
 new_xsec[i] = math.exp(new_xsec[i])
 new_xsecUp[i] = math.exp(new_xsecUp[i])
 new_xsecDown[i] = math.exp(new_xsecDown[i])
 yTHUncs.append(new_xsecUp[i])

for m in xrange(len(masses), 0, -1):

  massesUncs.append(masses[m-1])
  yTHUncs.append(new_xsecDown[m-1])

fout = ROOT.TFile.Open('Radion%s.root'%channel,'RECREATE') 
graphTH = ROOT.TGraph(len(masses),masses,new_xsec)
graphTH.SetName('gtheory')
graphTH.Write()
graphTHUP = ROOT.TGraph(len(masses),masses,new_xsecUp)
graphTHUP.SetName('gtheoryUP')
graphTHUP.Write()
graphTHDOWN = ROOT.TGraph(len(masses),masses,new_xsecDown)
graphTHDOWN.SetName('gtheoryDOWN')
graphTHDOWN.Write()
graphTHUncs = ROOT.TGraph(len(massesUncs),massesUncs,yTHUncs)
graphTHUncs.SetName('grshade')
graphTHUncs.Write()
fout.Close()





print "********* Make VBF Radion->%s cross section graphs***********"%channel

yTH = array('d',[])
yTHUp = array('d',[])
yTHDown = array('d',[])
yTHUncs = array('d',[])
masses = array('d',[])
massesUncs = array('d',[])

Fxsec = open('VBF_HXSWG2016_13TeV_LR_3TeV.txt','r')
Fbr = open('Decay_short_kl_35_arxiv1110.6452.txt','r')

for i,l in enumerate(Fxsec.readlines()):

 if i<1: continue
 
 Fbr = open('Decay_short_kl_35_arxiv1110.6452.txt','r')
 for j,ll in enumerate(Fbr.readlines()):
 
  if j<1: continue
  
  if float(l.split('\t')[0]) != float(ll.split('\t')[0]): continue
 
  masses.append(float(l.split('\t')[0])/1000.)
  massesUncs.append(float(l.split('\t')[0])/1000.)
 
  if channel=='WW': br = float(ll.split('\t')[4])
  else: br = float(ll.split('\t')[3])
  sigma = float(l.split('\t')[1])
  uncUp = 1.0 + float(l.split('\t')[5])/100.
  uncDown = 1.0 + float(l.split('\t')[6])/100.
 
 
  yTH.append(math.log(sigma*br))
  yTHUp.append(math.log(uncUp*sigma*br))
  yTHDown.append(math.log(uncDown*sigma*br))
  print "mass",masses[-1],"th",yTH[-1],"down",yTHDown[-1],"up",yTHUp[-1]
  
 Fbr.close()
 
Fxsec.close()
Fbr.close()
  
graphTHLog = ROOT.TGraph(len(masses),masses,yTH)
graphTHUPLog = ROOT.TGraph(len(masses),masses,yTHUp)
graphTHDOWNLog = ROOT.TGraph(len(masses),masses,yTHDown)

new_xsec = array('d',[])
new_xsecUp = array('d',[])
new_xsecDown = array('d',[])
for i in range(graphTHLog.GetN()):
 x = ROOT.Double(0.)
 y = ROOT.Double(0.)
 graphTHLog.GetPoint(i,x,y)
 new_xsec.append(y)
for i in range(graphTHUPLog.GetN()):
 x = ROOT.Double(0.)
 y = ROOT.Double(0.)
 graphTHUPLog.GetPoint(i,x,y)
 new_xsecUp.append(y) 
for i in range(graphTHDOWNLog.GetN()):
 x = ROOT.Double(0.)
 y = ROOT.Double(0.)
 graphTHDOWNLog.GetPoint(i,x,y)
 new_xsecDown.append(y)
    
new_masses = [3.5,4.0,4.5,5.0,5.5,6.0,6.5]
for m in new_masses:
 masses.append(m)
 massesUncs.append(m)
 new_xsec.append(graphTHLog.Eval(m))
 new_xsecUp.append(graphTHUPLog.Eval(m))
 new_xsecDown.append(graphTHDOWNLog.Eval(m))

graphTHLog = ROOT.TGraph(len(masses),masses,new_xsec)
graphTHUPLog = ROOT.TGraph(len(masses),masses,new_xsecUp)
graphTHDOWNLog = ROOT.TGraph(len(masses),masses,new_xsecDown)

for i,v in enumerate(new_xsec):
 new_xsec[i] = math.exp(new_xsec[i])
 new_xsecUp[i] = math.exp(new_xsecUp[i])
 new_xsecDown[i] = math.exp(new_xsecDown[i])
 yTHUncs.append(new_xsecUp[i])

for m in xrange(len(masses), 0, -1):

  massesUncs.append(masses[m-1])
  yTHUncs.append(new_xsecDown[m-1])

fout = ROOT.TFile.Open('VBF_Radion%s.root'%channel,'RECREATE') 
graphTH = ROOT.TGraph(len(masses),masses,new_xsec)
graphTH.SetName('gtheory')
graphTH.Write()
graphTHUP = ROOT.TGraph(len(masses),masses,new_xsecUp)
graphTHUP.SetName('gtheoryUP')
graphTHUP.Write()
graphTHDOWN = ROOT.TGraph(len(masses),masses,new_xsecDown)
graphTHDOWN.SetName('gtheoryDOWN')
graphTHDOWN.Write()
graphTHUncs = ROOT.TGraph(len(massesUncs),massesUncs,yTHUncs)
graphTHUncs.SetName('grshade')
graphTHUncs.Write()
fout.Close()
