import ROOT
from ROOT import *
import time, sys
from array import array

def getListOfBinsLowEdge(hist,dim):
    axis =0
    N = 0
    if dim =="x":
        axis= hist.GetXaxis()
        N = hist.GetNbinsX()
    if dim =="y":
        axis = hist.GetYaxis()
        N = hist.GetNbinsY()
    if dim =="z":
        axis = hist.GetZaxis()
        N = hist.GetNbinsZ()
    if axis==0:
        return {}
    
    mmin = axis.GetXmin()
    mmax = axis.GetXmax()
    r =[]
    for i in range(1,N+2):
        #v = mmin + i * (mmax-mmin)/float(N)
        r.append(axis.GetBinLowEdge(i))
    return r
    
#f = ROOT.TFile.Open('/afs/cern.ch/user/t/thaarres/public/results_2016_tt/workspace_JJ_ZprimeZH_VH_HPHP_13TeV_2016ZprimeZH_NoConditional.root','READ')
f = ROOT.TFile.Open('workspace_JJ_ZprimeZH_VH_HPHP_13TeV_2016ZprimeZH.root','READ')
#f = ROOT.TFile.Open('test_workspace.root','READ')
ws = f.w

modelTTjets = ws.pdf('shapeBkg_TTJets_JJ_VH_HPHP_13TeV_2016')
#argsPdf  = modelTTjets.getComponents()
#argsPdf.Print("v")
#argsPdf['TTJets_mjetRes_l2_JJ_VH_HPHP_13TeV_2016'].Print("v")
#sys.exit()

MJ1= ws.var("MJ1");
MJ2= ws.var("MJ2");
MJJ= ws.var("MJJ");
args = ROOT.RooArgSet(MJ1,MJ2,MJJ)

print "n_exp_binJJ_VH_HPHP_13TeV_2016_proc_TTJets"
o_norm_ttjets = ws.obj("n_exp_binJJ_VH_HPHP_13TeV_2016_proc_TTJets")

nEventsTT = o_norm_ttjets.getVal()
print "Expected tt+jets events: ",nEventsTT
modelTTjets.Print('v')

#ttjets = modelTTjets.generate(args,int(nEventsTT*10), ROOT.RooFit.ConditionalObservables( ROOT.RooArgSet(ws.var("MJJ")) ) )
ttjets = modelTTjets.generate(args,int(nEventsTT*10))
print "NOW GET OBSERVABLES"
test = modelTTjets.getObservables(ttjets)
test.Print("v")

'''
xframe = MJ1.frame()
ttjets.plotOn(xframe)
modelTTjets.plotOn(xframe)
 
canv = ROOT.TCanvas()
canv.cd()
xframe.Draw()
time.sleep(1000)    
'''

finmc = ROOT.TFile.Open("results_2016_tt/JJ_2016_nonRes_VH_HPHP.root",'READ')
hmcin = finmc.Get('nonRes')
xbins = array("f",getListOfBinsLowEdge(hmcin,"x"))
zbins = array("f",getListOfBinsLowEdge(hmcin,"z"))
binsz = hmcin.GetNbinsZ()
binsy = hmcin.GetNbinsY()
binsx = hmcin.GetNbinsX()
  
hout_ttjets = ROOT.TH3F('ttjets','ttjets',len(xbins)-1,xbins,len(xbins)-1,xbins,len(zbins)-1,zbins)
  
if ttjets!=None:
 #print signal.sumEntries()
 for i in range(0,int(ttjets.sumEntries())):
  a = ttjets.get(i)
  it = a.createIterator()
  var = it.Next()
  x=[]
  while var:
      x.append(var.getVal())
      var = it.Next()
  #print x
  hout_ttjets.Fill(x[0],x[1],x[2])  

print "Integral",hout_ttjets.Integral()

x_projs = []
zbinMin = [1    ,1                             ,hmcin.GetZaxis().FindBin(1235)+1,hmcin.GetZaxis().FindBin(1344)+1,hmcin.GetZaxis().FindBin(1454)+1]
zbinMax = [binsz,hmcin.GetZaxis().FindBin(1235),hmcin.GetZaxis().FindBin(1344)  ,hmcin.GetZaxis().FindBin(1454)  ,binsz]

for i in range(len(zbinMin)):

 pname = "px_%i"%i
 x_projs.append( hout_ttjets.ProjectionX(pname,1,binsy,zbinMin[i],zbinMax[i]) )
 
colors = [ROOT.kBlack,ROOT.kRed,ROOT.kBlue,210,ROOT.kOrange] 
for i,h in enumerate(x_projs):
 h.SetLineColor(colors[i])
 h.SetLineWidth(2)
 #h.Scale(1./h.Integral())

leg = ROOT.TLegend(0.51,0.60,0.76,0.85)
leg.SetBorderSize(0)
leg.SetTextSize(0.035)
leg.AddEntry(x_projs[0],"Inclusive","L")
for i in range(1,5):
 leg.AddEntry(x_projs[i],"%.1f < m_{jj} < %.1f TeV"%( hmcin.GetZaxis().GetBinLowEdge(zbinMin[i])/1000.,hmcin.GetZaxis().GetBinUpEdge(zbinMax[i])/1000.),"L" )
 
for h in x_projs:
 h.Draw("HISTsame")

leg.Draw()
#x_projs[0].Draw("PE")
time.sleep(1000)  
# import ROOT
# from ROOT import *
# import time
# from array import array
# def getListOfBinsLowEdge(hist,dim):
#     axis =0
#     N = 0
#     if dim =="x":
#         axis= hist.GetXaxis()
#         N = hist.GetNbinsX()
#     if dim =="y":
#         axis = hist.GetYaxis()
#         N = hist.GetNbinsY()
#     if dim =="z":
#         axis = hist.GetZaxis()
#         N = hist.GetNbinsZ()
#     if axis==0:
#         return {}
#
#     mmin = axis.GetXmin()
#     mmax = axis.GetXmax()
#     r =[]
#     for i in range(1,N+2):
#         #v = mmin + i * (mmax-mmin)/float(N)
#         r.append(axis.GetBinLowEdge(i))
#     return r
#
# f = ROOT.TFile.Open('workspace_JJ_ZprimeZH_VV_HPHP_13TeV_2016ZprimeZH.root','READ')
# ws = f.w
#
# modelTTjets = ws.pdf('shapeBkg_TTJets_JJ_VV_HPHP_13TeV_2016')
#
# MJ1= ws.var("MJ1");
# MJ2= ws.var("MJ2");
# MJJ= ws.var("MJJ");
# args = ROOT.RooArgSet(MJ1,MJ2,MJJ)
#
# print "n_exp_binJJ_VV_HPHP_13TeV_2016_proc_TTJets"
# o_norm_ttjets = ws.obj("n_exp_binJJ_VV_HPHP_13TeV_2016_proc_TTJets")
#
# nEventsTT = o_norm_ttjets.getVal()
# print "Expected tt+jets events: ",nEventsTT
# modelTTjets.Print('v')
#
# ttjets = modelTTjets.generate(args,int(nEventsTT*10))
#
# finmc = ROOT.TFile.Open("results_2016_tt/JJ_2016_nonRes_VV_HPHP.root",'READ')
# hmcin = finmc.Get('nonRes')
# xbins = array("f",getListOfBinsLowEdge(hmcin,"x"))
# zbins = array("f",getListOfBinsLowEdge(hmcin,"z"))
#
# hout_ttjets = ROOT.TH3F('ttjets','ttjets',len(xbins)-1,xbins,len(xbins)-1,xbins,len(zbins)-1,zbins)
# if ttjets!=None:
#  #print signal.sumEntries()
#  for i in range(0,int(ttjets.sumEntries())):
#   a = ttjets.get(i)
#   it = a.createIterator()
#   var = it.Next()
#   x=[]
#   while var:
#       x.append(var.getVal())
#       var = it.Next()
#   #print x
#   hout_ttjets.Fill(x[0],x[1],x[2])
#
# print "Integral",hout_ttjets.Integral()
# x_proj = hout_ttjets.ProjectionX()
# x_proj.Draw("PE")
# time.sleep(1000)