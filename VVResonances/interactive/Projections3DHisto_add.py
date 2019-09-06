import os,sys,optparse,time
import ROOT as rt
rt.gROOT.ProcessLine(".x tdrstyle.cc")
import CMS_lumi
#setTDRStyle()
rt.gStyle.SetOptStat(0)
rt.gStyle.SetOptTitle(0)
rt.gROOT.SetBatch(True)
from time import sleep

# Run from command line with
# python Projections3DHisto_add.py --mc control-plots-HPLP-pythia-2016-rho-kernel-VH/JJ_2016_nonRes_VV_HPLP_altshape2.root,nonRes -k control-plots-HPLP-pythia-2016-rho-kernel-VH/JJ_2016_nonRes_3D_VV_HPLP.root,histo_madgraph --cm control-plots-VV_HPLP-madgraph-2018-rho-kernel/JJ_2018_nonRes_VV_HPLP_altshape2.root,nonRes --vh control-plots-VV_HPLP-madgraph-2018-rho-kernel/JJ_2018_nonRes_3D_VV_HPLP.root,histo_madgraph -o "VV_HPLP"

# python Projections3DHisto_add.py --mc control-plots-VH_HPLP-pythia-2016-rho-kernel/JJ_2016_nonRes_VH_HPLP_altshape2.root,nonRes -k control-plots-VH_HPLP-pythia-2016-rho-kernel/JJ_2016_nonRes_3D_VH_HPLP.root,histo_madgraph --cm control-plots-VH_HPLP-madgraph-2018-rho-kernel/JJ_2018_nonRes_VH_HPLP_altshape2.root,nonRes --vh control-plots-VH_HPLP-madgraph-2018-rho-kernel/JJ_2018_nonRes_3D_VH_HPLP.root,histo_madgraph -o "VH_HPLP"

#python Projections3DHisto.py --mc JJ_2016_nonRes_VV_HPLP.root,nonRes -k JJ_2016_nonRes_3D_VV_HPLP.root,histo -o control-plots-HPLP-pythia
#python Projections3DHisto.py --mc 2017/JJ_nonRes_HPLP.root,nonRes -k 2016/JJ_nonRes_3D_HPLP_2017_copy.root,histo -o control-plots-HPLP-pythia
#python Projections3DHisto.py --mc 2017/JJ_nonRes_HPHP.root,nonRes -k 2016/JJ_nonRes_3D_HPHP_2017_copy.root,histo -o control-plots-HPHP-pythia
#python Projections3DHisto.py --mc 2016/JJ_nonRes_LPLP_altshapeUp.root,nonRes -k 2016/JJ_nonRes_3D_LPLP_fixed.root,histo_altshapeUp -o control-plots-LPLPfixed-herwig
#python Projections3DHisto.py --mc 2016/JJ_nonRes_LPLP_altshapeUp.root,nonRes -k 2016/JJ_nonRes_3D_LPLP.root,histo_altshapeUp -o control-plots-LPLP-herwig
#python Projections3DHisto.py --mc 2016/JJ_nonRes_LPLP_altshapeUp.root,nonRes -k JJ_nonRes_3D_LPLP.root,histo -o control-plots-LPLPnew-herwig
#python Projections3DHisto.py --mc JJ_nonRes_LPLP_nominal.root,nonRes -k JJ_nonRes_3D_LPLP.root,histo -o control-plots-LPLP-pythia

def get_canvas(cname):

 #change the CMS_lumi variables (see CMS_lumi.py)
 CMS_lumi.lumi_7TeV = "4.8 fb^{-1}"
 CMS_lumi.lumi_8TeV = "18.3 fb^{-1}"
 CMS_lumi.writeExtraText = 1
 CMS_lumi.extraText = "Simulation"
 CMS_lumi.lumi_sqrtS = "13 TeV (2016)" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)

 iPos = 11
 if( iPos==0 ): CMS_lumi.relPosX = 0.12

 H_ref = 600 
 W_ref = 800 
 W = W_ref
 H  = H_ref

 iPeriod = 0

 # references for T, B, L, R
 T = 0.08*H_ref
 B = 0.12*H_ref 
 L = 0.12*W_ref
 R = 0.04*W_ref

 canvas = rt.TCanvas(cname,cname,50,50,W,H)
 canvas.SetFillColor(0)
 canvas.SetBorderMode(0)
 canvas.SetFrameFillStyle(0)
 canvas.SetFrameBorderMode(0)
 canvas.SetLeftMargin( L/W )
 canvas.SetRightMargin( R/W )
 canvas.SetTopMargin( T/H )
 canvas.SetBottomMargin( B/H )
 canvas.SetTickx(0)
 canvas.SetTicky(0)
 
 return canvas

parser = optparse.OptionParser()
parser.add_option("--mc","--mc",dest="mc",help="File with mc events and histo name (separated by comma)",default='JJ_nonRes_HPHP_nominal.root,nonRes')
parser.add_option("-k","--kernel",dest="kernel",help="File with kernel and histo name (separated by comma)",default='JJ_nonRes_3D_HPHP.root,histo')
parser.add_option("--cm",dest="cm",help="File to compare with mc events and histo name (separated by comma)",default='JJ_nonRes_HPHP_nominal.root,nonRes')
parser.add_option("--vh",dest="vh",help="File to compare with kernel and histo name (separated by comma)",default='JJ_nonRes_3D_HPHP.root,histo')
parser.add_option("-o","--outdir",dest="outdir",help="Output directory for plots",default='')
parser.add_option("-l","--label",dest="label",help="MC type label (Pythia8, Herwig, Madgraph, Powheg)",default='Pythia8')
(options,args) = parser.parse_args()

#void Projections3DHisto(std::string dataFile, std::string hdataName, std::string fitFile, std::string hfitName, std::string outDirName){

os.system('rm -rf %s'%options.outdir)
os.system('mkdir %s'%options.outdir)

lumi2018 = 59690. #to be checked! https://twiki.cern.ch/twiki/bin/view/CMS/PdmV2018Analysis                                                                                                                                                                                  
lumi2017 = 41367.
lumi2016 = 35900.



#2016 file
kfile,kname = options.kernel.split(',')
print "kfile "+str(kfile)
fin = rt.TFile.Open(kfile,"READ")
print "kname "+str(kname)
hin = fin.Get(kname)
hin.Scale(1./hin.Integral())
#2018 file
kfile2,kname2 = options.vh.split(',')
print "kfile2 "+str(kfile2)
fin2 = rt.TFile.Open(kfile2,"READ")
print "kname2 "+str(kname2)
hin2 = fin2.Get(kname2)
hin2.Scale(1./hin2.Integral())
hin_tot = hin.Clone()
hin_tot.Scale(lumi2016)
hin2.Scale(lumi2018)
#hin_tot.Add(hin2,1./lumi2018)
if hin_tot.Add(hin2) : #,1./lumi2018)
 print "success"
hin_tot.SaveAs("JJ_2016and2018_nonRes_3D_"+options.outdir+"_histo_madgraph.root")



MCfile,MCname = options.mc.split(',')
finMC = rt.TFile.Open(MCfile,"READ")
hinMC = finMC.Get(MCname)
hinMC.Scale(1./hinMC.Integral())

MCfile2,MCname2 = options.cm.split(',')
finMC2 = rt.TFile.Open(MCfile2,"READ")
hinMC2 = finMC2.Get(MCname2)
hinMC2.Scale(1./hinMC2.Integral())

hinMC_tot = hinMC.Clone()
hinMC_tot.Scale(lumi2016)
hinMC2.Scale(lumi2018)
hinMC_tot.Add(hinMC2)
hinMC_tot.SaveAs("JJ_2016and2018_nonRes_"+options.outdir+"_altshape2.root")


binsx = hin.GetNbinsX()
xmin = hin.GetXaxis().GetXmin()
xmax = hin.GetXaxis().GetXmax()
print "xmin",xmin,"xmax",xmax,"binsx",binsx

binsy = hin.GetNbinsY()
ymin = hin.GetYaxis().GetXmin()
ymax = hin.GetYaxis().GetXmax()
print "ymin",ymin,"ymax",ymax,"binsy",binsy

binsz = hin.GetNbinsZ()
zmin = hin.GetZaxis().GetXmin()
zmax = hin.GetZaxis().GetXmax()
print "zmin",zmin,"zmax",zmax,"binsz",binsz

'''
hx = []
hy = []
hz = []
hxMC = []
hyMC = []
hzMC = []

hx2 = []
hy2 = []
hz2 = []
hxMC2 = []
hyMC2 = []
hzMC2 = []

zbinMin = 1 #,1,hin.GetZaxis().FindBin(1530)+1,hin.GetZaxis().FindBin(2546)+1]
zbinMax = binsz #,hin.GetZaxis().FindBin(1530),hin.GetZaxis().FindBin(2546),binsz]
colors = 1 #,99,9,8,94]
scale = 1. #,0.8,3.0,30.]

print "Plotting mJ projections",zbinMin,zbinMax
pname = "px"
hin.RebinX(2)
hx =  hin.ProjectionX(pname,1,binsy,zbinMin,zbinMax) 
pname = "py"
hin.RebinY(2)
hy = hin.ProjectionY(pname,1,binsx,zbinMin,zbinMax) 
pname = "px_MC"
hinMC.RebinX(2)
hxMC =  hinMC.ProjectionX(pname,1,binsy,zbinMin,zbinMax) 
pname = "py_MC"
hinMC.RebinY(2)
hyMC = hinMC.ProjectionY(pname,1,binsx,zbinMin,zbinMax) 

print "Plotting mJ2 projections",zbinMin,zbinMax
pname = "px2"
hin2.RebinX(2)
hx2 =  hin2.ProjectionX(pname,1,binsy,zbinMin,zbinMax) 
pname = "py2"
hin2.RebinY(2)
hy2 = hin2.ProjectionY(pname,1,binsx,zbinMin,zbinMax) 
pname = "px_MC2"
hinMC2.RebinX(2)
hxMC2 =  hinMC2.ProjectionX(pname,1,binsy,zbinMin,zbinMax) 
pname = "py_MC2"
hinMC2.RebinY(2)
hyMC2 = hinMC2.ProjectionY(pname,1,binsx,zbinMin,zbinMax) 

hx.SetLineColor(colors)
hx.SetMarkerColor(colors)
hy.SetLineColor(colors)
hy.SetMarkerColor(colors)
hxMC.SetLineColor(colors)
hxMC.SetMarkerColor(colors)
hxMC.SetMarkerStyle(20)
hxMC.SetMarkerSize(0.5)
hyMC.SetLineColor(colors)
hyMC.SetMarkerColor(colors) 
hyMC.SetMarkerStyle(20)
hyMC.SetMarkerSize(0.5)
 
hx.SetMinimum(0)
hx.SetMaximum(0.05)
hy.SetMinimum(0)
hy.SetMaximum(0.05)

hx2.SetLineColor(colors)
hx2.SetLineStyle(2)
hx2.SetMarkerColor(colors)
hy2.SetLineColor(colors)
hy2.SetLineStyle(2)
hy2.SetMarkerColor(colors)
hxMC2.SetLineColor(colors)
hxMC2.SetLineStyle(2)
hxMC2.SetMarkerColor(colors)
hxMC2.SetMarkerStyle(25)
hxMC2.SetMarkerSize(0.5)
hyMC2.SetLineColor(colors)
hyMC2.SetLineStyle(2)
hyMC2.SetMarkerColor(colors) 
hyMC2.SetMarkerStyle(25)
hyMC2.SetMarkerSize(0.5)
 
hx2.SetMinimum(0)
hx2.SetMaximum(0.05)
hy2.SetMinimum(0)
hy2.SetMaximum(0.05)

#leg = rt.TLegend(0.6,0.6,0.85,0.8)
leg = rt.TLegend(0.51,0.60,0.76,0.85)
leg.SetBorderSize(0)
leg.SetTextSize(0.035)
leg.AddEntry(hxMC,"Simulation (%s) VV "%options.label,"LP")
leg.AddEntry(hx,"Template VV","L")
leg.AddEntry(hxMC2,"Simulation (%s) VH "%options.label,"LP")
leg.AddEntry(hx2,"Template VH","L")
 
cx = get_canvas("cx")
cx.cd()
hx.Draw("HISTsame")
hxMC.Draw("PEsame")
hx2.Draw("HISTsame")
hxMC2.Draw("PEsame")
hx.GetXaxis().SetTitle("m_{jet1} (proj. x) [GeV]")
leg.Draw()

CMS_lumi.CMS_lumi(cx, 0, 11)
cx.cd()
cx.Update()
cx.RedrawAxis()
frame = cx.GetFrame()
frame.Draw()
cx.SaveAs(options.outdir+"/cx.png","pdf")

cy = get_canvas("cy")
cy.cd()
hy.GetXaxis().SetTitle("m_{jet2} (proj. y) [GeV]")
hy.GetXaxis().SetTitleSize(hx.GetXaxis().GetTitleSize())
hy.GetXaxis().SetTitleOffset(hx.GetXaxis().GetTitleOffset())
hy.Draw("HISTsame")
hyMC.Draw("PEsame")
hy2.Draw("HISTsame")
hyMC2.Draw("PEsame")
leg.Draw()

CMS_lumi.CMS_lumi(cy, 0, 11)
cy.cd()
cy.Update()
cy.RedrawAxis()
frame = cy.GetFrame()
frame.Draw()
cy.SaveAs(options.outdir+"/cy.png","pdf")


#############

#xbinMin[5] = {1,hin.GetXaxis().FindBin(55),hin.GetXaxis().FindBin(70),hin.GetXaxis().FindBin(100),hin.GetXaxis().FindBin(150)}
#xbinMax[5] = {binsx,hin.GetXaxis().FindBin(70),hin.GetXaxis().FindBin(100),hin.GetXaxis().FindBin(150),binsx}
xbinMin = 1 #,hin.GetXaxis().FindBin(55),hin.GetXaxis().FindBin(73)+1,hin.GetXaxis().FindBin(103)+1,hin.GetXaxis().FindBin(167)+1]
xbinMax = binsx #,hin.GetXaxis().FindBin(73),hin.GetXaxis().FindBin(103),hin.GetXaxis().FindBin(167),binsx]
#ybinMin = hin.GetXaxis().FindBin(55)
#ybinMax = hin.GetXaxis().FindBin(73)
#float scalez[5] = {1.,1.,0.1,0.01,0.001}
scalez = 1. #,1.,0.1,0.01,0.001]

print "Plotting mJJ projections",xbinMin,xbinMax
pname = "pz"
hz =  hin.ProjectionZ(pname,xbinMin,xbinMax,xbinMin,xbinMax)
pname = "pzMC"
hzMC = hinMC.ProjectionZ(pname,xbinMin,xbinMax,xbinMin,xbinMax)

print "Plotting mJJ 2 projections",xbinMin,xbinMax
pname = "pz2"
hz2 =  hin2.ProjectionZ(pname,xbinMin,xbinMax,xbinMin,xbinMax)
pname = "pzMC2"
hzMC2 = hinMC2.ProjectionZ(pname,xbinMin,xbinMax,xbinMin,xbinMax)

hz.SetLineColor(colors)
hz.SetMarkerColor(colors)
hzMC.SetLineColor(colors)
hzMC.SetMarkerColor(colors)
hzMC.SetMarkerStyle(20)
hzMC.SetMarkerSize(0.5)

hz2.SetLineColor(colors)
hz2.SetLineStyle(2)
hz2.SetMarkerColor(colors)
hzMC2.SetLineColor(colors)
hzMC2.SetLineStyle(2)
hzMC2.SetMarkerColor(colors)
hzMC2.SetMarkerStyle(22)
hzMC2.SetMarkerSize(0.5)

#leg2 = rt.TLegend(0.6,0.6,0.85,0.85)
leg2 = rt.TLegend(0.51,0.65,0.76,0.90)
leg2.SetBorderSize(0)
leg2.SetTextSize(0.035)
leg2.AddEntry(hzMC,"Simulation (%s) VV "%options.label,"LP")
leg2.AddEntry(hz,"Template VV ","L")
leg2.AddEntry(hzMC2,"Simulation (%s) VH "%options.label,"LP")
leg2.AddEntry(hz2,"Template VH ","L")

cz = get_canvas("cz")
cz.SetLogy()
cz.cd()
hz.SetMinimum(1E-11)
hz.SetMaximum(50.0)
hz2.SetMinimum(1E-11)
hz2.SetMaximum(50.0)
hz.Draw("HISTsame")
hzMC.Draw("PEsame")
hz2.Draw("HISTsame")
hzMC2.Draw("PEsame")
hz.GetXaxis().SetTitle("m_{jj} (proj. z) [GeV]")
leg2.Draw()

CMS_lumi.CMS_lumi(cz, 0, 11)
cz.cd()
cz.Update()
cz.RedrawAxis()
frame = cz.GetFrame()
frame.Draw()
cz.SaveAs(options.outdir+"/cz.png","pdf")




'''
#xbinMin = [hin.GetXaxis().FindBin(173)+1]
#xbinMax = [binsx]

'''
hin_PTUp = fin.Get("histo_PTUp")
hin_PTUp.Scale(1./hin_PTUp.Integral())
hin_PTDown = fin.Get("histo_PTDown")
hin_PTDown.Scale(1./hin_PTDown.Integral())
hin_OPTUp = fin.Get("histo_OPTUp")
hin_OPTUp.Scale(1./hin_OPTUp.Integral())
hin_OPTDown = fin.Get("histo_OPTDown")
hin_OPTDown.Scale(1./hin_OPTDown.Integral())
hin_altshapeUp = fin.Get("histo_altshapeUp")
hin_altshapeUp.Scale(1./hin_altshapeUp.Integral())
hin_altshapeDown = fin.Get("histo_altshapeDown")
hin_altshapeDown.Scale(1./hin_altshapeDown.Integral())
hin_altshape2Up = fin.Get("histo_altshape2Up")
hin_altshape2Up.Scale(1./hin_altshape2Up.Integral())
hin_altshape2Down = fin.Get("histo_altshape2Down")
hin_altshape2Down.Scale(1./hin_altshape2Down.Integral())
#hin_altshape3Up = fin.Get("histo_altshape3Up")
#hin_altshape3Up.Scale(1./hin_altshape3Up.Integral())
#hin_altshape3Down = fin.Get("histo_altshape3Down")
#hin_altshape3Down.Scale(1./hin_altshape3Down.Integral())
hin_OPT3Up = fin.histo_OPT3Up
hin_OPT3Up.Scale(1./hin_OPT3Up.Integral())
hin_OPT3Down = fin.histo_OPT3Down
hin_OPT3Down.Scale(1./hin_OPT3Down.Integral())

hz_PTUp = hin_PTUp.ProjectionZ("pz_PTUp",xbinMin[0],xbinMax[0],xbinMin[0],xbinMax[0])
hz_PTUp.SetLineColor(rt.kMagenta)
hz_PTUp.Scale(1./hz_PTUp.Integral())
hz_PTDown = hin_PTDown.ProjectionZ("pz_PTDown",xbinMin[0],xbinMax[0],xbinMin[0],xbinMax[0])
hz_PTDown.SetLineColor(rt.kMagenta)
hz_PTDown.Scale(1./hz_PTDown.Integral())
hz_OPTUp = hin_OPTUp.ProjectionZ("pz_OPTUp",xbinMin[0],xbinMax[0],xbinMin[0],xbinMax[0])
hz_OPTUp.SetLineColor(210)
hz_OPTUp.Scale(1./hz_OPTUp.Integral())
hz_OPTDown = hin_OPTDown.ProjectionZ("pz_OPTDown",xbinMin[0],xbinMax[0],xbinMin[0],xbinMax[0])
hz_OPTDown.SetLineColor(210)
hz_OPTDown.Scale(1./hz_OPTDown.Integral())
hz_altshapeUp = hin_altshapeUp.ProjectionZ("pz_altshapeUp",xbinMin[0],xbinMax[0],xbinMin[0],xbinMax[0])
hz_altshapeUp.SetLineColor(rt.kBlue)
hz_altshapeUp.Scale(1./hz_altshapeUp.Integral())
hz_altshapeDown = hin_altshapeDown.ProjectionZ("pz_altshapeDown",xbinMin[0],xbinMax[0],xbinMin[0],xbinMax[0])
hz_altshapeDown.SetLineColor(rt.kBlue)
hz_altshapeDown.Scale(1./hz_altshapeDown.Integral())
hz_altshape2Up = hin_altshape2Up.ProjectionZ("pz_altshape2Up",xbinMin[0],xbinMax[0],xbinMin[0],xbinMax[0])
hz_altshape2Up.SetLineColor(rt.kRed)
hz_altshape2Up.Scale(1./hz_altshape2Up.Integral())
hz_altshape2Down = hin_altshape2Down.ProjectionZ("pz_altshape2Down",xbinMin[0],xbinMax[0],xbinMin[0],xbinMax[0])
hz_altshape2Down.SetLineColor(rt.kRed)
hz_altshape2Down.Scale(1./hz_altshape2Down.Integral())
#hz_altshape3Up = hin_altshape3Up.ProjectionZ("pz_altshape3Up",xbinMin[0],xbinMax[0],xbinMin[0],xbinMax[0])
#hz_altshape3Up.SetLineColor(rt.kOrange+1)
#hz_altshape3Down = hin_altshape3Down.ProjectionZ("pz_altshape3Down",xbinMin[0],xbinMax[0],xbinMin[0],xbinMax[0])
#hz_altshape3Down.SetLineColor(rt.kOrange+1)
hz_OPT3Up = hin_OPT3Up.ProjectionZ("pz_OPT3Up",xbinMin[0],xbinMax[0],xbinMin[0],xbinMax[0])
hz_OPT3Up.SetLineColor(rt.kViolet-6)
hz_OPT3Up.Scale(1./hz_OPT3Up.Integral())
hz_OPT3Down = hin_OPT3Down.ProjectionZ("pz_OPT3Down",xbinMin[0],xbinMax[0],xbinMin[0],xbinMax[0])
hz_OPT3Down.SetLineColor(rt.kViolet-6)
hz_OPT3Down.Scale(1./hz_OPT3Down.Integral())

hzMC[0].Scale(1./hzMC[0].Integral())
hz[0].Scale(1./hz[0].Integral())

#leg3 = rt.TLegend(0.6,0.55,0.95,0.8)
leg3 = rt.TLegend(0.53,0.55,0.78,0.89)
leg3.SetBorderSize(0)
leg3.SetTextSize(0.035)
leg3.AddEntry(hzMC[0],"Simulation (%s)"%(options.label),"LP")
leg3.AddEntry(hz[0],"Template","L")

leg3.AddEntry(hz_PTUp,"#propto m_{jj} up/down","L")
leg3.AddEntry(hz_OPTUp,"#propto 1/m_{jj} up/down","L")
leg3.AddEntry(hz_altshapeUp,"HERWIG up/down","L")
leg3.AddEntry(hz_altshape2Up,"MADGRAPH+PYTHIA up/down","L")
#leg3.AddEntry(hz_altshape3Up,"POWHEG up/down","L")
leg3.AddEntry(hz_OPT3Up,"m_{jj} turn-on up/down","L")

czSyst = get_canvas("czSyst")
czSyst.cd()
czSyst.SetLogy()

#hz[4].SetLineColor(rt.kBlack)
#hz[4].Scale(1./0.001)
hz[0].SetMinimum(1E-06)
hz[0].SetMaximum(10.0)
hz[0].Draw("HIST")
hz_PTUp.Draw("HISTsame")
hz_PTDown.Draw("HISTsame") 
hz_OPTUp.Draw("HISTsame")
hz_OPTDown.Draw("HISTsame")
hz_altshapeUp.Draw("HISTsame")
hz_altshapeDown.Draw("HISTsame")
hz_altshape2Up.Draw("HISTsame")
hz_altshape2Down.Draw("HISTsame")
#hz_altshape3Up.Draw("HISTsame")
#hz_altshape3Down.Draw("HISTsame")
#hzMC[4].SetLineColor(rt.kBlack)
#hzMC[4].SetMarkerColor(rt.kBlack)
#hzMC[4].Scale(1./0.001)
hz_OPT3Up.Draw("HISTsame")
hz_OPT3Down.Draw("HISTsame")
hzMC[0].Draw("same")
leg3.Draw()

CMS_lumi.CMS_lumi(czSyst, 0, 11)
czSyst.cd()
czSyst.Update()
czSyst.RedrawAxis()
frame = czSyst.GetFrame()
frame.Draw()
czSyst.SaveAs(options.outdir+"/czSyst.png","pdf")
# sleep(10000)
hx_PTUp = hin_PTUp.ProjectionX("px_PTUp",1,binsy,zbinMin[0],zbinMax[0])
hx_PTUp.SetLineColor(rt.kMagenta)
hx_PTUp.Scale(1./hx_PTUp.Integral())
hx_PTDown = hin_PTDown.ProjectionX("px_PTDown",1,binsy,zbinMin[0],zbinMax[0])
hx_PTDown.SetLineColor(rt.kMagenta)
hx_PTDown.Scale(1./hx_PTDown.Integral())
hx_OPTUp = hin_OPTUp.ProjectionX("px_OPTUp",1,binsy,zbinMin[0],zbinMax[0])
hx_OPTUp.SetLineColor(210)
hx_OPTUp.Scale(1./hx_OPTUp.Integral())
hx_OPTDown = hin_OPTDown.ProjectionX("px_OPTDown",1,binsy,zbinMin[0],zbinMax[0])
hx_OPTDown.SetLineColor(210)
hx_OPTDown.Scale(1./hx_OPTDown.Integral())
hx_altshapeUp = hin_altshapeUp.ProjectionX("px_altshapeUp",1,binsy,zbinMin[0],zbinMax[0])
hx_altshapeUp.SetLineColor(rt.kBlue)
hx_altshapeUp.Scale(1./hx_altshapeUp.Integral())
hx_altshapeDown = hin_altshapeDown.ProjectionX("px_altshapeDown",1,binsy,zbinMin[0],zbinMax[0])
hx_altshapeDown.SetLineColor(rt.kBlue)
hx_altshapeDown.Scale(1./hx_altshapeDown.Integral())
hx_altshape2Up = hin_altshape2Up.ProjectionX("px_altshape2Up",1,binsy,zbinMin[0],zbinMax[0])
hx_altshape2Up.SetLineColor(rt.kRed)
hx_altshape2Up.Scale(1./hx_altshape2Up.Integral())
hx_altshape2Down = hin_altshape2Down.ProjectionX("px_altshape2Down",1,binsy,zbinMin[0],zbinMax[0])
hx_altshape2Down.SetLineColor(rt.kRed)
hx_altshape2Down.Scale(1./hx_altshape2Down.Integral())
#hx_altshape3Up = hin_altshape3Up.ProjectionX("px_altshape3Up",1,binsy,zbinMin[0],zbinMax[0])
#hx_altshape3Up.SetLineColor(rt.kOrange+1)
#hx_altshape3Down = hin_altshape3Down.ProjectionX("px_altshape3Down",1,binsy,zbinMin[0],zbinMax[0])
#hx_altshape3Down.SetLineColor(rt.kOrange+1)
hx_OPT3Up = hin_OPT3Up.ProjectionX("px_OPT3Up",1,binsy,zbinMin[0],zbinMax[0])
hx_OPT3Up.SetLineColor(rt.kViolet-6)
hx_OPT3Up.Scale(1./hx_OPT3Up.Integral())
hx_OPT3Down = hin_OPT3Down.ProjectionX("px_OPT3Down",1,binsy,zbinMin[0],zbinMax[0])
hx_OPT3Down.SetLineColor(rt.kViolet-6)
hx_OPT3Down.Scale(1./hx_OPT3Down.Integral())


hxMC[0].Scale(1./hxMC[0].Integral())
hx[0].Scale(1./hx[0].Integral())
#leg3 = rt.TLegend(0.6,0.55,0.95,0.8)
leg3 = rt.TLegend(0.53,0.50,0.78,0.84)
leg3.SetBorderSize(0)
leg3.SetTextSize(0.035)
leg3.AddEntry(hxMC[0],"Simulation (%s)"%(options.label),"LP")
leg3.AddEntry(hx[0],"Template","L")
leg3.AddEntry(hx_PTUp,"#propto m_{jj} up/down","L")
leg3.AddEntry(hx_OPTUp,"#propto 1/m_{jj} up/down","L")
leg3.AddEntry(hx_altshapeUp,"HERWIG up/down","L")
leg3.AddEntry(hx_altshape2Up,"MADGRAPH+PYTHIA up/down","L")
#leg3.AddEntry(hx_altshape3Up,"POWHEG up/down","L")
leg3.AddEntry(hx_OPT3Up,"m_{jj} turn-on up/down","L")

cxSyst = get_canvas("cxSyst")
cxSyst.cd()

hx[0].SetMinimum(0)
hx[0].SetMaximum(0.04)
hx[0].Draw("HIST")
hx_PTUp.Draw("HISTsame")
hx_PTDown.Draw("HISTsame") 
hx_OPTUp.Draw("HISTsame")
hx_OPTDown.Draw("HISTsame")
hx_altshapeUp.Draw("HISTsame")
hx_altshapeDown.Draw("HISTsame")
hx_altshape2Up.Draw("HISTsame")
hx_altshape2Down.Draw("HISTsame")
#hx_altshape3Up.Draw("HISTsame")
#hx_altshape3Down.Draw("HISTsame")
hx_OPT3Up.Draw("HISTsame")
hx_OPT3Down.Draw("HISTsame")
hxMC[0].Draw("same")
leg3.Draw()

CMS_lumi.CMS_lumi(cxSyst, 0, 11)
cxSyst.cd()
cxSyst.Update()
cxSyst.RedrawAxis()
frame = cxSyst.GetFrame()
frame.Draw()
cxSyst.SaveAs(options.outdir+"/cxSyst.png","pdf")


hy_PTUp = hin_PTUp.ProjectionY("py_PTUp",1,binsy,zbinMin[0],zbinMax[0])
hy_PTUp.SetLineColor(rt.kMagenta)
hy_PTUp.Scale(1./hy_PTUp.Integral())
hy_PTDown = hin_PTDown.ProjectionY("py_PTDown",1,binsy,zbinMin[0],zbinMax[0])
hy_PTDown.SetLineColor(rt.kMagenta)
hy_PTDown.Scale(1./hy_PTDown.Integral())
hy_OPTUp = hin_OPTUp.ProjectionY("py_OPTUp",1,binsy,zbinMin[0],zbinMax[0])
hy_OPTUp.SetLineColor(210)
hy_OPTUp.Scale(1./hy_OPTUp.Integral())
hy_OPTDown = hin_OPTDown.ProjectionY("py_OPTDown",1,binsy,zbinMin[0],zbinMax[0])
hy_OPTDown.SetLineColor(210)
hy_OPTDown.Scale(1./hy_OPTDown.Integral())
hy_altshapeUp = hin_altshapeUp.ProjectionY("py_altshapeUp",1,binsy,zbinMin[0],zbinMax[0])
hy_altshapeUp.SetLineColor(rt.kBlue)
hy_altshapeUp.Scale(1./hy_altshapeUp.Integral())
hy_altshapeDown = hin_altshapeDown.ProjectionY("py_altshapeDown",1,binsy,zbinMin[0],zbinMax[0])
hy_altshapeDown.SetLineColor(rt.kBlue)
hy_altshapeDown.Scale(1./hy_altshapeDown.Integral())
hy_altshape2Up = hin_altshape2Up.ProjectionY("py_altshape2Up",1,binsy,zbinMin[0],zbinMax[0])
hy_altshape2Up.SetLineColor(rt.kRed)
hy_altshape2Up.Scale(1./hy_altshape2Up.Integral())
hy_altshape2Down = hin_altshape2Down.ProjectionY("py_altshape2Down",1,binsy,zbinMin[0],zbinMax[0])
hy_altshape2Down.SetLineColor(rt.kRed)
hy_altshape2Down.Scale(1./hy_altshape2Down.Integral())
#hy_altshape3Up = hin_altshape3Up.ProjectionY("py_altshape3Up",1,binsy,zbinMin[0],zbinMax[0])
#hy_altshape3Up.SetLineColor(rt.kOrange+1)
#hy_altshape3Down = hin_altshape3Down.ProjectionY("py_altshape3Down",1,binsy,zbinMin[0],zbinMax[0])
#hy_altshape3Down.SetLineColor(rt.kOrange+1)
hy_OPT3Up = hin_OPT3Up.ProjectionY("py_OPT3Up",xbinMin[0],xbinMax[0],zbinMin[0],zbinMax[0])
hy_OPT3Up.SetLineColor(rt.kViolet-6)
hy_OPT3Up.Scale(1./hy_OPT3Up.Integral())
hy_OPT3Down = hin_OPT3Down.ProjectionY("py_OPT3Down",xbinMin[0],xbinMax[0],zbinMin[0],zbinMax[0])
hy_OPT3Down.SetLineColor(rt.kViolet-6)
hy_OPT3Down.Scale(1./hy_OPT3Down.Integral())

hyMC[0].Scale(1./hyMC[0].Integral())
hy[0].Scale(1./hy[0].Integral())
#leg3 = rt.TLegend(0.6,0.55,0.95,0.8)
leg3 = rt.TLegend(0.53,0.50,0.78,0.84)
leg3.SetBorderSize(0)
leg3.SetTextSize(0.035)
leg3.AddEntry(hyMC[0],"Simulation (%s)"%(options.label),"LP")
leg3.AddEntry(hy[0],"Template","L")
leg3.AddEntry(hy_PTUp,"#propto m_{jj} up/down","L")
leg3.AddEntry(hy_OPTUp,"#propto 1/m_{jj} up/down","L")
leg3.AddEntry(hy_altshapeUp,"HERWIG up/down","L")
leg3.AddEntry(hy_altshape2Up,"MADGRAPH+PYTHIA up/down","L")
#leg3.AddEntry(hy_altshape3Up,"POWHEG up/down","L")
leg3.AddEntry(hy_OPT3Up,"m_{jj} turn-on up/down","L")



cySyst = get_canvas("cySyst")
cySyst.cd()

hy[0].SetMinimum(0)
hy[0].SetMaximum(0.04)
hy[0].Draw("HIST")

hy_PTUp.Draw("HISTsame")
hy_PTDown.Draw("HISTsame") 
hy_OPTUp.Draw("HISTsame")
hy_OPTDown.Draw("HISTsame")
hy_altshapeUp.Draw("HISTsame")
hy_altshapeDown.Draw("HISTsame")
hy_altshape2Up.Draw("HISTsame")
hy_altshape2Down.Draw("HISTsame")
#hy_altshape3Up.Draw("HISTsame")
#hy_altshape3Down.Draw("HISTsame")
hy_OPT3Up.Draw("HISTsame")
hy_OPT3Down.Draw("HISTsame")
hyMC[0].Draw("same")

leg3.Draw()

CMS_lumi.CMS_lumi(cySyst, 0, 11)
cySyst.cd()
cySyst.Update()
cySyst.RedrawAxis()
frame = cySyst.GetFrame()
frame.Draw()
cySyst.SaveAs(options.outdir+"/cySyst.png","pdf")
'''


'''
TCanvas* cxz = new TCanvas("cxz","cxz")
cxz.cd()
TH2F* hxz = (TH2F*)hin.Project3D("zx")
hxz.Draw("COLZ")

cxz.SaveAs(TString(outDirName)+TString("/")+TString("cxz.png"),"pdf")

TCanvas* cyz = new TCanvas("cyz","cyz")
cyz.cd()
TH2F* hyz = (TH2F*)hin.Project3D("zy")
hyz.Draw("COLZ")

cyz.SaveAs(TString(outDirName)+TString("/")+TString("cyz.png"),"pdf")

}

'''
