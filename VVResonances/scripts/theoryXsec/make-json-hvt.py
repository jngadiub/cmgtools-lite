import json, sys
from array import array
import ROOT
import pandas as pd

def get_theo_map(sqrts,model=""):

   V_mass = array('d',[])

   brs = {}
   index = {}

   mapping = ["M0","M+","BRWW","BRZh","BRWZ","BRWh","CX+(pb)","CX0(pb)","CX-(pb)"]

   for m in xrange(0,len(mapping)):
      if mapping[m] != "M0" and mapping[m] != "M+":
   	 brs[mapping[m]] = array('d',[])
   	 #print mapping[m]

   f = open('xsect_HVT%s_%sTeV.txt'%(model,sqrts),'r')
   for line in f:
      brDict = line.split(",")
      for d in xrange(0,len(brDict)):
   	 if brDict[d].find('\n') != -1:
   	    brDict[d] = brDict[d].split('\n')[0]
   	 for m in xrange(0,len(mapping)):
   	    if brDict[d] == mapping[m]:
   	       index[mapping[m]] = d
   	       print "%s %i" %(mapping[m],d)
	    
   f.close()

   f = open('xsect_HVT%s_%sTeV.txt'%(model,sqrts),'r')
   for line in f:
      if line.find('M0') != -1: continue
      brDict = line.split(",")  	    
      V_mass.append(float(brDict[index['M0']]))
      for m in xrange(0,len(mapping)):
   	 if mapping[m] != "M0" and mapping[m] != "M+":
   	    brs[mapping[m]].append(float(brDict[index[mapping[m]]]))

   f.close()

   return [brs,V_mass]


thMap13 = get_theo_map("13","B")
xsecMap13 = thMap13[0]
mass = thMap13[1]

fdict = {}
for k,m in enumerate(mass):
 fdict[str(int(m))] = {}
 for i,v in xsecMap13.iteritems():
  fdict[str(int(m))][i] = v[k]

f=open("HVTB.json","w")
json.dump(fdict,f)
f.close()

yTH = array('d',[])
x = array('d',[])
for i,m in enumerate(mass):
  x.append(m/1000.)
  yTH.append(fdict[str(int(m))]['CX0(pb)']*fdict[str(int(m))]['BRZh'])


fout = ROOT.TFile.Open('ZprimeZH.root','RECREATE') 
graphTH = ROOT.TGraph(len(x),x,yTH)
graphTH.SetName('gtheory')
graphTH.Write()  
fout.Close()

yTH = array('d',[])
for i,m in enumerate(mass):
  yTH.append(fdict[str(int(m))]['CX0(pb)']*fdict[str(int(m))]['BRWW'])


fout = ROOT.TFile.Open('ZprimeWW.root','RECREATE') 
graphTH = ROOT.TGraph(len(x),x,yTH)
graphTH.SetName('gtheory')
graphTH.Write()  
fout.Close()

yTH = array('d',[])
for i,m in enumerate(mass):
  yTH.append( (fdict[str(int(m))]['CX+(pb)']+fdict[str(int(m))]['CX-(pb)'])*fdict[str(int(m))]['BRWZ'])
  

fout = ROOT.TFile.Open('WprimeWZ.root','RECREATE') 
graphTH = ROOT.TGraph(len(x),x,yTH)
graphTH.SetName('gtheory')
graphTH.Write()  
fout.Close()

yTH = array('d',[])
for i,m in enumerate(mass):
  yTH.append( (fdict[str(int(m))]['CX+(pb)']+fdict[str(int(m))]['CX-(pb)'])*fdict[str(int(m))]['BRWh'])
  

fout = ROOT.TFile.Open('WprimeWH.root','RECREATE') 
graphTH = ROOT.TGraph(len(x),x,yTH)
graphTH.SetName('gtheory')
graphTH.Write()  
fout.Close()

df = pd.read_csv('HVTC.csv') 

mass = df['M'].values
xsec_zpr = df['Zprime_cH1'].values
br_zpr_ww = df['BrZprimeToWW'].values
br_zpr_zh = df['BrZprimeToZH'].values
xsec_wpr = df['Wprime_cH1'].values
br_wpr_wz = df['BrWprimeToWZ'].values
br_wpr_wh = df['BrWprimeToWH'].values

fdict = {}
for i,m in enumerate(mass):
 fdict[str(int(m))] = {}
 fdict[str(int(m))]['Zprime_cH1'] = xsec_zpr[i]
 fdict[str(int(m))]['BRWW'] = br_zpr_ww[i]
 fdict[str(int(m))]['BRZh'] = br_zpr_zh[i]
 fdict[str(int(m))]['Wprime_cH1'] = xsec_wpr[i]
 fdict[str(int(m))]['BRWh'] = br_wpr_wh[i]
 fdict[str(int(m))]['BRWZ'] = br_wpr_wz[i]
 
f=open("HVTC.json","w")
json.dump(fdict,f)
f.close() 

yTH = array('d',[])
x = array('d',[])
for i,m in enumerate(mass):
  x.append(m/1000.)
  yTH.append(fdict[str(int(m))]['Zprime_cH1']*fdict[str(int(m))]['BRZh'])


fout = ROOT.TFile.Open('HVTC_ZprimeZH.root','RECREATE') 
graphTH = ROOT.TGraph(len(x),x,yTH)
graphTH.SetName('gtheory')
graphTH.Write()  
fout.Close()

yTH = array('d',[])
for i,m in enumerate(mass):
  yTH.append(fdict[str(int(m))]['Zprime_cH1']*fdict[str(int(m))]['BRWW'])


fout = ROOT.TFile.Open('HVTC_ZprimeWW.root','RECREATE') 
graphTH = ROOT.TGraph(len(x),x,yTH)
graphTH.SetName('gtheory')
graphTH.Write()  
fout.Close()

yTH = array('d',[])
for i,m in enumerate(mass):
  yTH.append(fdict[str(int(m))]['Wprime_cH1']*fdict[str(int(m))]['BRWZ'])


fout = ROOT.TFile.Open('HVTC_WprimeWZ.root','RECREATE') 
graphTH = ROOT.TGraph(len(x),x,yTH)
graphTH.SetName('gtheory')
graphTH.Write()  
fout.Close()

yTH = array('d',[])
for i,m in enumerate(mass):
  yTH.append(fdict[str(int(m))]['Wprime_cH1']*fdict[str(int(m))]['BRWh'])


fout = ROOT.TFile.Open('HVTC_WprimeWH.root','RECREATE') 
graphTH = ROOT.TGraph(len(x),x,yTH)
graphTH.SetName('gtheory')
graphTH.Write()  
fout.Close()
