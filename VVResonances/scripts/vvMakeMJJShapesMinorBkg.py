#!/usr/bin/env python
import ROOT
from array import array
from CMGTools.VVResonances.statistics.Fitter import Fitter
from math import log,exp,sqrt
import os, sys, re, optparse,pickle,shutil,json
import copy
import json
from CMGTools.VVResonances.plotting.tdrstyle import *
setTDRStyle()
from CMGTools.VVResonances.plotting.TreePlotter import TreePlotter
from CMGTools.VVResonances.plotting.MergedPlotter import MergedPlotter
sys.path.insert(0, "../interactive/")
import cuts

ROOT.gSystem.Load("libCMGToolsVVResonances")
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptFit(0)

parser = optparse.OptionParser()
parser.add_option("-o","--output",dest="output",help="Output",default='')
parser.add_option("-s","--samples",dest="samples",default='',help="Type of sample")
parser.add_option("-c","--cut",dest="cut",help="Cut to apply for yield in gen sample",default='')
parser.add_option("-p","--period",dest="period",help="data taking year ",default='2016')
parser.add_option("-b","--bins",dest="binsx",type=int,help="bins",default=1)
parser.add_option("-x","--minx",dest="minx",type=float,help="bins",default=0)
parser.add_option("-X","--maxx",dest="maxx",type=float,help="conditional bins split by comma",default=1)
parser.add_option("-w","--weights",dest="weights",help="additional weights",default='')
parser.add_option("--binsMVV",dest="binsMVV",help="use special binning",default="")
parser.add_option("-t","--triggerweight",dest="triggerW",action="store_true",help="Use trigger weights",default=False)
parser.add_option("--corrFactorW",dest="corrFactorW",type=float,help="add correction factor xsec",default=1.)
parser.add_option("--corrFactorZ",dest="corrFactorZ",type=float,help="add correction factor xsec",default=1.)


(options,args) = parser.parse_args()

def get_canvas(cname):
    

    H_ref = 600 
    W_ref = 600 
    W = W_ref
    H  = H_ref

    iPeriod = 0

    # references for T, B, L, R
    T = 0.08*H_ref
    B = 0.12*H_ref 
    L = 0.12*W_ref
    R = 0.04*W_ref

    canvas = ROOT.TCanvas(cname,cname,50,50,W,H)
    canvas.SetFillColor(0)
    canvas.SetBorderMode(0)
    canvas.SetFrameFillStyle(0)
    canvas.SetFrameBorderMode(0)
    canvas.SetLeftMargin( L/W )
    canvas.SetRightMargin( R/W )
    canvas.SetTopMargin( T/H )
    canvas.SetBottomMargin( B/H )
    canvas.SetTickx()
    canvas.SetTicky()
    
    return canvas

def getBinning(binsMVV,minx,maxx,bins):
    l=[]
    if binsMVV=="":
        for i in range(0,bins+1):
            l.append(minx + i* (maxx - minx)/bins)
    else:
        s = binsMVV.split(",")
        for w in s:
            l.append(int(w))
    return l


def doPlot(data,finalFit,sampleTypes,outlabel,mvv_nominal_w=None):
    c = get_canvas("c")
    c.SetLogy()
    data.SetMarkerColor(ROOT.kBlack)
    
    data.GetYaxis().SetTitleOffset(1.5)
    
    data.GetXaxis().SetTitle("m_{jj} (GeV)")
    data.GetYaxis().SetTitle("arbitrary scale")
    data.SetMarkerStyle(20)
    data.SetMaximum(1.2)
    data.SetMinimum(0.0000001)
    data.Draw("P")
    orig = data.GetFunction("expo")
    orig.SetLineWidth(2)
    if outlabel.find("noreweight")!=-1 :
        finalFit.SetLineColor(ROOT.kBlue)
        finalFit.SetLineWidth(2)
        finalFit.SetLineStyle(2)

        c3var = (orig.GetParameter(4)-finalFit.GetParameter(4))

        tmpu = orig.Clone()
        tmpu.SetParameter(4,orig.GetParameter(4)+c3var)
        tmpu.SetLineColor(ROOT.kGreen+2)
        tmpu.SetLineStyle(1)
        tmpu.Draw("fsame")

        tmpd = orig.Clone()
        tmpd.SetParameter(4,orig.GetParameter(4)-c3var)
        tmpd.SetLineColor(ROOT.kGreen+2)
        tmpd.SetLineStyle(1)
        tmpd.Draw("fsame")

        c3var2 = 2*(orig.GetParameter(4)-finalFit.GetParameter(4))

        tmpu2 = orig.Clone()
        tmpu2.SetParameter(4,orig.GetParameter(4)+c3var2)
        tmpu2.SetLineColor(ROOT.kGreen+2)
        tmpu2.SetLineStyle(2)
        tmpu2.Draw("fsame")

        tmpd2 = orig.Clone()
        tmpd2.SetParameter(4,orig.GetParameter(4)-c3var2)
        tmpd2.SetLineColor(ROOT.kGreen+2)
        tmpd2.SetLineStyle(2)
        tmpd2.Draw("fsame")

        c3var3 = 3*(orig.GetParameter(4)-finalFit.GetParameter(4))

        tmpu3 = orig.Clone()
        tmpu3.SetParameter(4,orig.GetParameter(4)+c3var3)
        tmpu3.SetLineColor(ROOT.kGreen+2)
        tmpu3.SetLineStyle(3)
        tmpu3.Draw("fsame")

        tmpd3 = orig.Clone()
        tmpd3.SetParameter(4,orig.GetParameter(4)-c3var3)
        tmpd3.SetLineColor(ROOT.kGreen+2)
        tmpd3.SetLineStyle(3)
        tmpd3.Draw("fsame")


    finalFit.Draw("fsame")

    '''
    tmp = orig.Clone()
    tmp.SetParameter(4,orig.GetParameter(4))
    tmp.SetLineColor(ROOT.kOrange)
    tmp.Draw("fsame")
    
    tmp2 = orig.Clone()
    tmp2.SetParameter(4,0.8*orig.GetParameter(4))
    tmp2.SetLineColor(ROOT.kOrange)
    tmp2.Draw("fsame")
    '''
    l = ROOT.TLegend(0.3809045,0.6063636,0.7622613,0.8220979)
    l.SetHeader(outlabel.split("_")[0])
    l.AddEntry(data,"simulation","lp")
    l.AddEntry(orig,"Fit","l")
    if outlabel.find("noreweight")!=-1 :
        l.AddEntry(tmpu,"Fit, c3 +/- unc","l")
        l.AddEntry(tmpu2,"Fit, c3 +/- 2unc","l")
        l.AddEntry(tmpu3,"Fit, c3 +/- 3unc","l")
    if mvv_nominal_w!=None:
        if mvv_nominal_w.Integral()!=0: mvv_nominal_w.Scale(1/mvv_nominal_w.Integral())
        mvv_nominal_w.Draw("same")
        mvv_nominal_w.SetMarkerStyle(10)
        mvv_nominal_w.SetMarkerColor(ROOT.kBlue)
        mvv_nominal_w.SetLineColor(ROOT.kBlue)
        #if options.samples.find("TT")!=-1:

        #else: l.AddEntry(mvv_nominal_w,"pT up variation", "lp")
    l.Draw("same")

    print "nominal chisquare ",orig.GetChisquare()/data.GetNbinsX()
    pt = ROOT.TPaveText(0.18,0.88,0.54,0.81,"NDC")
    pt.SetTextFont(42)
    pt.SetTextSize(0.03)
    pt.SetTextAlign(12)
    pt.SetFillColor(0)
    pt.SetBorderSize(0)
    pt.SetFillStyle(0)
    pt.AddText("Chi2/ndf = %.2f/%i = %.2f"%(orig.GetChisquare(),data.GetNbinsX(),orig.GetChisquare()/data.GetNbinsX()))
    pt.AddText("Prob = %.3f"%ROOT.TMath.Prob(orig.GetChisquare(),data.GetNbinsX()))
    pt.Draw("same")

    if outlabel.find("noreweight")!=-1 :
        l2 = ROOT.TLegend(0.15,0.3,0.35,0.4)
        l2.AddEntry(mvv_nominal_w,"t#bar{t} without p_T","lp")
        l2.AddEntry(finalFit,"Fit","l")
        #l2.AddEntry(tmpn,"Fit, c3 +/- 20%","l")
        l2.Draw("same")

        print "no pt reweight chisquare ",finalFit.GetChisquare()/data.GetNbinsX()
        pt2 = ROOT.TPaveText(0.18,0.28,0.54,0.2,"NDC")
        pt2.SetTextFont(42)
        pt2.SetTextSize(0.03)
        pt2.SetTextAlign(12)
        pt2.SetFillColor(0)
        pt2.SetBorderSize(0)
        pt2.SetFillStyle(0)
        pt2.AddText("Chi2/ndf = %.2f/%i = %.2f"%(finalFit.GetChisquare(),data.GetNbinsX(),finalFit.GetChisquare()/data.GetNbinsX()))
        pt2.AddText("Prob = %.3f"%ROOT.TMath.Prob(finalFit.GetChisquare(),data.GetNbinsX()))
        pt2.Draw("same")

    tmplabel = "nonRes"
    if sampleTypes[0].find("Jets")!=-1: tmplabel="Jets"
    if sampleTypes[0].find("TT")!=-1: tmplabel="TTbar"
    if options.output.find('VV_HPLP')!=-1: tmplabel+='VV_HPLP'
    if options.output.find('VV_HPHP')!=-1: tmplabel+='VV_HPHP'
    if options.output.find('VH_HPLP')!=-1: tmplabel+='VH_HPLP'
    if options.output.find('VH_HPHP')!=-1: tmplabel+='VH_HPHP'
    if options.output.find('VH_LPHP')!=-1: tmplabel+='VH_LPHP'
    if 'W' in sampleTypes: tmplabel="W"+tmplabel
    if 'Z' in sampleTypes: tmplabel="Z"+tmplabel
    text = ROOT.TLatex()
    text.DrawLatexNDC(0.13,0.92,"#font[62]{CMS} #font[52]{Simulation}")
    outputname="debug_mVV_shapes_"+tmplabel+"_"+outlabel+".pdf"
    c.SaveAs(outputname)
    print "for debugging save",outputname

def doPlotRatio(data,finalFit,sampleTypes,outlabel,mvv_nominal_w=None):
    c = get_canvas("c")
    pad1 = ROOT.TPad("pad1","pad1",0,0.3,1,1)
    pad2 = ROOT.TPad("pad2","pad2",0,0,1,0.3);
    pad1.SetBottomMargin(0.00001);
    pad1.SetBorderMode(0);
    pad1.SetLogy();
    pad2.SetTopMargin(0.00001);
    pad2.SetBottomMargin(0.3);
    pad2.SetBorderMode(0);
    pad1.Draw();
    pad2.Draw();
    pad1.cd();

    data.SetMarkerColor(ROOT.kBlack)
    
    data.GetYaxis().SetTitleOffset(1.5)
    
    data.GetXaxis().SetTitle("m_{jj} (GeV)")
    data.GetYaxis().SetTitle("arbitrary scale")
    data.SetMarkerStyle(20)
    data.SetMaximum(1.2)
    data.SetMinimum(0.0000001)
    data.Draw("P")
    orig = data.GetFunction("expo")
    orig.SetLineWidth(2)
    if outlabel.find("noreweight")!=-1 :
        finalFit.SetLineColor(ROOT.kBlue)
        finalFit.SetLineWidth(2)
        finalFit.SetLineStyle(2)

        c3var = (orig.GetParameter(4)-finalFit.GetParameter(4))

        tmpu = orig.Clone()
        tmpu.SetParameter(4,orig.GetParameter(4)+c3var)
        tmpu.SetLineColor(ROOT.kGreen+2)
        tmpu.SetLineStyle(1)
        tmpu.Draw("fsame")

        tmpd = orig.Clone()
        tmpd.SetParameter(4,orig.GetParameter(4)-c3var)
        tmpd.SetLineColor(ROOT.kGreen+2)
        tmpd.SetLineStyle(1)
        tmpd.Draw("fsame")

        c3var2 = 2*(orig.GetParameter(4)-finalFit.GetParameter(4))

        tmpu2 = orig.Clone()
        tmpu2.SetParameter(4,orig.GetParameter(4)+c3var2)
        tmpu2.SetLineColor(ROOT.kGreen+2)
        tmpu2.SetLineStyle(2)
        tmpu2.Draw("fsame")

        tmpd2 = orig.Clone()
        tmpd2.SetParameter(4,orig.GetParameter(4)-c3var2)
        tmpd2.SetLineColor(ROOT.kGreen+2)
        tmpd2.SetLineStyle(2)
        tmpd2.Draw("fsame")

        c3var3 = 3*(orig.GetParameter(4)-finalFit.GetParameter(4))

        tmpu3 = orig.Clone()
        tmpu3.SetParameter(4,orig.GetParameter(4)+c3var3)
        tmpu3.SetLineColor(ROOT.kGreen+2)
        tmpu3.SetLineStyle(3)
        tmpu3.Draw("fsame")

        tmpd3 = orig.Clone()
        tmpd3.SetParameter(4,orig.GetParameter(4)-c3var3)
        tmpd3.SetLineColor(ROOT.kGreen+2)
        tmpd3.SetLineStyle(3)
        tmpd3.Draw("fsame")


    finalFit.Draw("fsame")

    '''
    tmp = orig.Clone()
    tmp.SetParameter(4,orig.GetParameter(4))
    tmp.SetLineColor(ROOT.kOrange)
    tmp.Draw("fsame")
    
    tmp2 = orig.Clone()
    tmp2.SetParameter(4,0.8*orig.GetParameter(4))
    tmp2.SetLineColor(ROOT.kOrange)
    tmp2.Draw("fsame")
    '''
    l = ROOT.TLegend(0.3809045,0.6063636,0.7622613,0.8220979)
    l.SetHeader(outlabel.split("_")[0])
    l.AddEntry(data,"simulation","lp")
    l.AddEntry(orig,"Fit","l")
    if outlabel.find("noreweight")!=-1 :
        l.AddEntry(tmpu,"Fit, c3 +/- unc","l")
        l.AddEntry(tmpu2,"Fit, c3 +/- 2unc","l")
        l.AddEntry(tmpu3,"Fit, c3 +/- 3unc","l")
    if mvv_nominal_w!=None:
        if mvv_nominal_w.Integral()!=0: mvv_nominal_w.Scale(1/mvv_nominal_w.Integral())
        mvv_nominal_w.Draw("same")
        mvv_nominal_w.SetMarkerStyle(4)
        mvv_nominal_w.SetMarkerColor(ROOT.kBlue)
        mvv_nominal_w.SetLineColor(ROOT.kBlue)
        #if options.samples.find("TT")!=-1:

        #else: l.AddEntry(mvv_nominal_w,"pT up variation", "lp")
    l.Draw("same")

    print "nominal chisquare ",orig.GetChisquare()/data.GetNbinsX()
    pt = ROOT.TPaveText(0.18,0.88,0.54,0.81,"NDC")
    pt.SetTextFont(42)
    pt.SetTextSize(0.03)
    pt.SetTextAlign(12)
    pt.SetFillColor(0)
    pt.SetBorderSize(0)
    pt.SetFillStyle(0)
    pt.AddText("Chi2/ndf = %.2f/%i = %.2f"%(orig.GetChisquare(),data.GetNbinsX(),orig.GetChisquare()/data.GetNbinsX()))
    pt.AddText("Prob = %.3f"%ROOT.TMath.Prob(orig.GetChisquare(),data.GetNbinsX()))
    pt.Draw("same")

    if outlabel.find("noreweight")!=-1 :
        l2 = ROOT.TLegend(0.15,0.3,0.35,0.4)
        l2.AddEntry(mvv_nominal_w,"t#bar{t} without p_T","lp")
        l2.AddEntry(finalFit,"Fit","l")
        #l2.AddEntry(tmpn,"Fit, c3 +/- 20%","l")
        l2.Draw("same")

        print "no pt reweight chisquare ",finalFit.GetChisquare()/data.GetNbinsX()
        pt2 = ROOT.TPaveText(0.18,0.28,0.54,0.2,"NDC")
        pt2.SetTextFont(42)
        pt2.SetTextSize(0.03)
        pt2.SetTextAlign(12)
        pt2.SetFillColor(0)
        pt2.SetBorderSize(0)
        pt2.SetFillStyle(0)
        pt2.AddText("Chi2/ndf = %.2f/%i = %.2f"%(finalFit.GetChisquare(),data.GetNbinsX(),finalFit.GetChisquare()/data.GetNbinsX()))
        pt2.AddText("Prob = %.3f"%ROOT.TMath.Prob(finalFit.GetChisquare(),data.GetNbinsX()))
        pt2.Draw("same")

    tmplabel = "nonRes"
    if sampleTypes[0].find("Jets")!=-1: tmplabel="Jets"
    if sampleTypes[0].find("TT")!=-1: tmplabel="TTbar"
    if options.output.find('VV_HPLP')!=-1: tmplabel+='VV_HPLP'
    if options.output.find('VV_HPHP')!=-1: tmplabel+='VV_HPHP'
    if options.output.find('VH_HPLP')!=-1: tmplabel+='VH_HPLP'
    if options.output.find('VH_HPHP')!=-1: tmplabel+='VH_HPHP'
    if options.output.find('VH_LPHP')!=-1: tmplabel+='VH_LPHP'
    if 'W' in sampleTypes: tmplabel="W"+tmplabel
    if 'Z' in sampleTypes: tmplabel="Z"+tmplabel
    text = ROOT.TLatex()
    text.DrawLatexNDC(0.13,0.92,"#font[62]{CMS} #font[52]{Simulation}")


    pad2.cd()
    r = ROOT.TH1F()
    data.Copy(r)
    r.GetYaxis().SetTitle("(data-fit)/#sigma_{stat}")
    r.GetYaxis().SetLabelFont(63);
    r.GetYaxis().SetLabelSize(16);
    r.GetXaxis().SetLabelFont(63);
    r.GetXaxis().SetLabelSize(16);

    r.GetYaxis().SetTitleFont(63);
    r.GetYaxis().SetTitleOffset(2.);
    r.GetYaxis().SetTitleSize(16);
    r.GetXaxis().SetTitleFont(63);
    r.GetXaxis().SetTitleSize(16);
    r.GetXaxis().SetTitleOffset(3);

    for i in range(0,data.GetNbinsX()+1):
        diff=data.GetBinContent(i+1)-orig.Eval(data.GetBinCenter(i+1))
        if data.GetBinError(i+1)!=0:
            diff=diff/data.GetBinError(i+1)
        r.SetBinContent(i+1,diff)
        if data.GetBinContent(i+1)==0: r.SetBinContent(i+1,0)
    r.SetMarkerStyle(10)
    r.SetMarkerColor(ROOT.kBlack)
    r.SetLineColor(ROOT.kBlack)
    r.SetMaximum(2)
    r.SetMinimum(-2)
    r.Draw("p")
    li = ROOT.TLine(data.GetXaxis().GetXmin(),0,data.GetXaxis().GetXmax(),0)
    li.SetLineStyle(2)
    li.SetLineColor(ROOT.kRed)
    li.Draw("same")

    if outlabel.find("noreweight")!=-1 :
        rw = ROOT.TH1F()
        data.Copy(rw)
        for i in range(0,data.GetNbinsX()):
            diff=data.GetBinContent(i+1)-finalFit.Eval(data.GetBinCenter(i+1))
            if data.GetBinError(i+1)!=0:
                diff=diff/data.GetBinError(i+1)
            rw.SetBinContent(i+1,diff)
            if data.GetBinContent(i+1)==0: rw.SetBinContent(i+1,0)
        rw.SetMarkerStyle(4)
        rw.SetMarkerColor(ROOT.kBlue)
        rw.SetLineColor(ROOT.kBlue)
        rw.Draw("psame")
    c.cd()
    outputname="debug_mVV_shapes_"+tmplabel+"_"+outlabel+".pdf"
    c.SaveAs(outputname)
    print "for debugging save",outputname

def doPlotCRatio(data,finalFit,sampleTypes,outlabel,mvv_nominal_w=None):
    c = get_canvas("c")
    pad1 = ROOT.TPad("pad1","pad1",0,0.3,1,1)
    pad2 = ROOT.TPad("pad2","pad2",0,0,1,0.3);
    pad1.SetBottomMargin(0.00001);
    pad1.SetBorderMode(0);
    pad1.SetLogy();
    pad2.SetTopMargin(0.00001);
    pad2.SetBottomMargin(0.3);
    pad2.SetBorderMode(0);
    pad1.Draw();
    pad2.Draw();
    pad1.cd();

    data.SetMarkerColor(ROOT.kBlack)
    
    data.GetYaxis().SetTitleOffset(1.5)
    
    data.GetXaxis().SetTitle("m_{jj} (GeV)")
    data.GetYaxis().SetTitle("arbitrary scale")
    data.SetMarkerStyle(20)
    data.SetMaximum(1.2)
    data.SetMinimum(0.0000001)
    data.Draw("P")
    orig = data.GetFunction("expo")
    orig.SetLineWidth(3)
    if outlabel.find("noreweight")!=-1 :
        fw = mvv_nominal_w.GetFunction("expo")
        fw.SetLineColor(ROOT.kBlue)
        fw.SetLineStyle(2)
        fw.SetLineWidth(2)
        finalFit.SetLineColor(ROOT.kBlue)
        finalFit.SetLineWidth(2)
        finalFit.SetLineStyle(2)
        
        c3var = (orig.GetParameter(4)-finalFit.GetParameter(4))

        tmpu = orig.Clone()
        tmpu.SetParameter(4,orig.GetParameter(4)+c3var)
        tmpu.SetLineColor(ROOT.kGreen+2)
        tmpu.SetLineStyle(1)
        tmpu.Draw("fsame")

        tmpd = orig.Clone()
        tmpd.SetParameter(4,orig.GetParameter(4)-c3var)
        tmpd.SetLineColor(ROOT.kGreen+2)
        tmpd.SetLineStyle(1)
        tmpd.Draw("fsame")

        c2var = (orig.GetParameter(2)-finalFit.GetParameter(2))

        tmpu2 = orig.Clone()
        tmpu2.SetParameter(2,orig.GetParameter(2)+c2var)
        tmpu2.SetLineColor(ROOT.kGreen+2)
        tmpu2.SetLineStyle(2)
        tmpu2.Draw("fsame")

        tmpd2 = orig.Clone()
        tmpd2.SetParameter(2,orig.GetParameter(2)-c2var)
        tmpd2.SetLineColor(ROOT.kGreen+2)
        tmpd2.SetLineStyle(2)
        tmpd2.Draw("fsame")

        c1var = (orig.GetParameter(1)-finalFit.GetParameter(1))

        tmpu3 = orig.Clone()
        tmpu3.SetParameter(1,orig.GetParameter(1)+c1var)
        tmpu3.SetLineColor(ROOT.kGreen+2)
        tmpu3.SetLineStyle(3)
        tmpu3.Draw("fsame")

        tmpd3 = orig.Clone()
        tmpd3.SetParameter(1,orig.GetParameter(1)-c1var)
        tmpd3.SetLineColor(ROOT.kGreen+2)
        tmpd3.SetLineStyle(3)
        tmpd3.Draw("fsame")
        
        #vary all
        tmpuc = orig.Clone()
        tmpuc.SetParameter(1,orig.GetParameter(1)+c1var)
        tmpuc.SetParameter(2,orig.GetParameter(2)+c2var)
        tmpuc.SetParameter(4,orig.GetParameter(4)+c3var)
        tmpuc.SetLineColor(ROOT.kOrange)
        tmpuc.SetLineStyle(2)
        tmpuc.Draw("fsame")

        tmpdc = orig.Clone()
        tmpdc.SetParameter(1,orig.GetParameter(1)-c1var)
        tmpdc.SetParameter(2,orig.GetParameter(2)-c2var)
        tmpdc.SetParameter(4,orig.GetParameter(4)-c3var)
        tmpdc.SetLineColor(ROOT.kOrange)
        tmpdc.SetLineStyle(2)
        tmpdc.Draw("fsame")


    finalFit.Draw("fsame")

    '''
    tmp = orig.Clone()
    tmp.SetParameter(4,orig.GetParameter(4))
    tmp.SetLineColor(ROOT.kOrange)
    tmp.Draw("fsame")
    
    tmp2 = orig.Clone()
    tmp2.SetParameter(4,0.8*orig.GetParameter(4))
    tmp2.SetLineColor(ROOT.kOrange)
    tmp2.Draw("fsame")
    '''
    l = ROOT.TLegend(0.3809045,0.6063636,0.7622613,0.8220979)
    l.SetHeader(outlabel.split("_")[0])
    l.AddEntry(data,"simulation","lp")
    l.AddEntry(orig,"Fit","l")
    if outlabel.find("noreweight")!=-1 :
        l.AddEntry(tmpu,"Fit, c3 +/- unc","l")
        l.AddEntry(tmpu2,"Fit, c2 +/- unc","l")
        l.AddEntry(tmpu3,"Fit, c1 +/- unc","l")
        l.AddEntry(tmpuc,"Fit, c1,c2,c3 +/- unc","l")
    if mvv_nominal_w!=None:
        if mvv_nominal_w.Integral()!=0: mvv_nominal_w.Scale(1/mvv_nominal_w.Integral())
        mvv_nominal_w.Draw("same")
        mvv_nominal_w.SetMarkerStyle(4)
        mvv_nominal_w.SetMarkerColor(ROOT.kBlue)
        mvv_nominal_w.SetLineColor(ROOT.kBlue)
        #if options.samples.find("TT")!=-1:

        #else: l.AddEntry(mvv_nominal_w,"pT up variation", "lp")
    l.Draw("same")

    print "nominal chisquare ",orig.GetChisquare()/data.GetNbinsX()
    pt = ROOT.TPaveText(0.18,0.88,0.54,0.81,"NDC")
    pt.SetTextFont(42)
    pt.SetTextSize(0.03)
    pt.SetTextAlign(12)
    pt.SetFillColor(0)
    pt.SetBorderSize(0)
    pt.SetFillStyle(0)
    pt.AddText("Chi2/ndf = %.2f/%i = %.2f"%(orig.GetChisquare(),data.GetNbinsX(),orig.GetChisquare()/data.GetNbinsX()))
    pt.AddText("Prob = %.3f"%ROOT.TMath.Prob(orig.GetChisquare(),data.GetNbinsX()))
    pt.Draw("same")

    if outlabel.find("noreweight")!=-1 :
        l2 = ROOT.TLegend(0.15,0.3,0.35,0.4)
        l2.AddEntry(mvv_nominal_w,"t#bar{t} without p_T","lp")
        l2.AddEntry(finalFit,"Fit","l")
        #l2.AddEntry(tmpn,"Fit, c3 +/- 20%","l")
        l2.Draw("same")

        print "no pt reweight chisquare ",finalFit.GetChisquare()/data.GetNbinsX()
        pt2 = ROOT.TPaveText(0.18,0.28,0.54,0.2,"NDC")
        pt2.SetTextFont(42)
        pt2.SetTextSize(0.03)
        pt2.SetTextAlign(12)
        pt2.SetFillColor(0)
        pt2.SetBorderSize(0)
        pt2.SetFillStyle(0)
        pt2.AddText("Chi2/ndf = %.2f/%i = %.2f"%(finalFit.GetChisquare(),data.GetNbinsX(),finalFit.GetChisquare()/data.GetNbinsX()))
        pt2.AddText("Prob = %.3f"%ROOT.TMath.Prob(finalFit.GetChisquare(),data.GetNbinsX()))
        pt2.Draw("same")

    tmplabel = "nonRes"
    if sampleTypes[0].find("Jets")!=-1: tmplabel="Jets"
    if sampleTypes[0].find("TT")!=-1: tmplabel="TTbar"
    if options.output.find('VV_HPLP')!=-1: tmplabel+='VV_HPLP'
    if options.output.find('VV_HPHP')!=-1: tmplabel+='VV_HPHP'
    if options.output.find('VH_HPLP')!=-1: tmplabel+='VH_HPLP'
    if options.output.find('VH_HPHP')!=-1: tmplabel+='VH_HPHP'
    if options.output.find('VH_LPHP')!=-1: tmplabel+='VH_LPHP'
    if 'W' in sampleTypes: tmplabel="W"+tmplabel
    if 'Z' in sampleTypes: tmplabel="Z"+tmplabel
    text = ROOT.TLatex()
    text.DrawLatexNDC(0.13,0.92,"#font[62]{CMS} #font[52]{Simulation}")
    orig.Draw("same")

    pad2.cd()
    r = ROOT.TH1F()
    data.Copy(r)
    r.GetYaxis().SetTitle("(data-fit)/#sigma_{stat}")
    r.GetYaxis().SetLabelFont(63);
    r.GetYaxis().SetLabelSize(16);
    r.GetXaxis().SetLabelFont(63);
    r.GetXaxis().SetLabelSize(16);

    r.GetYaxis().SetTitleFont(63);
    r.GetYaxis().SetTitleOffset(2.);
    r.GetYaxis().SetTitleSize(16);
    r.GetXaxis().SetTitleFont(63);
    r.GetXaxis().SetTitleSize(16);
    r.GetXaxis().SetTitleOffset(3);

    for i in range(0,data.GetNbinsX()+1):
        diff=data.GetBinContent(i+1)-orig.Eval(data.GetBinCenter(i+1))
        if data.GetBinError(i+1)!=0:
            diff=diff/data.GetBinError(i+1)
        r.SetBinContent(i+1,diff)
        if data.GetBinContent(i+1)==0: r.SetBinContent(i+1,0)
    r.SetMarkerStyle(10)
    r.SetMarkerColor(ROOT.kBlack)
    r.SetLineColor(ROOT.kBlack)
    r.SetMaximum(2)
    r.SetMinimum(-2)
    r.Draw("p")
    li = ROOT.TLine(data.GetXaxis().GetXmin(),0,data.GetXaxis().GetXmax(),0)
    li.SetLineStyle(2)
    li.SetLineColor(ROOT.kRed)
    li.Draw("same")

    if outlabel.find("noreweight")!=-1 :
        rw = ROOT.TH1F()
        data.Copy(rw)
        for i in range(0,data.GetNbinsX()):
            diff=data.GetBinContent(i+1)-finalFit.Eval(data.GetBinCenter(i+1))
            if data.GetBinError(i+1)!=0:
                diff=diff/data.GetBinError(i+1)
            rw.SetBinContent(i+1,diff)
            if data.GetBinContent(i+1)==0: rw.SetBinContent(i+1,0)
        rw.SetMarkerStyle(4)
        rw.SetMarkerColor(ROOT.kBlue)
        rw.SetLineColor(ROOT.kBlue)
        rw.Draw("psame")
    c.cd()

    outputname="debug_mVV_shapes_"+tmplabel+"_"+outlabel+".pdf"
    c.SaveAs(outputname)
    print "for debugging save",outputname

def getParametrization(FinalFit):
    #string = str(FinalFit.GetParameter(0))+"*(1-x/13000.)^"+str(FinalFit.GetParameter(1))+"/(x/13000)^"+str(FinalFit.GetParameter(2))
    #return string
    result = {}
    result["N0"] = FinalFit.GetParameter(0)
    result["c1"] = FinalFit.GetParameter(1)
    result["c2"] = FinalFit.GetParameter(2)
    result["N1"] = FinalFit.GetParameter(3)
    result["c3"] = FinalFit.GetParameter(4)
    return result

def unequalScale(histo,name,alpha,power=1):
    newHistoU =copy.deepcopy(histo) 
    newHistoU.SetName(name+"Up")
    newHistoD =copy.deepcopy(histo) 
    newHistoD.SetName(name+"Down")
    for i in range(1,histo.GetNbinsX()+1):
        x= histo.GetXaxis().GetBinCenter(i)
        nominal=histo.GetBinContent(i)
        factor = 1+alpha*pow(x,power) 
        newHistoU.SetBinContent(i,nominal*factor)
        newHistoD.SetBinContent(i,nominal/factor)
    return newHistoU,newHistoD
    
  
def doFit(proj,label="",fixPars=None):
    if proj.Integral() == 0:
        print "histogram has zero integral "+proj.GetName()
        return 0
    scale = proj.Integral()
    proj.Scale(1.0/scale)
    
    
    beginFitX = options.minx
    endX =  options.maxx
    #expo=ROOT.TF1("expo","[0]*(1-x/13000.)^[1]/(x/13000)^[2]",1000,8000)
    #expo=ROOT.TF1("expo","[0]*(e^(-[1]*x/13000.))*(1-TMath::Erf(x/13000.-[2]))",1000,8000)
    #expo=ROOT.TF1("expo","[0]*e^(-[1]*(x -1125.)/13000.-[2]/((x-1125.)/13000.)+[3]*(x -1125.)/13000.*(x -1125.)/13000.+[4]*(x -1125.)/13000.*(x -1125.)/13000.*(x -1125.)/13000.)",1000,8000)
    print label
    if label == "Wjets": 
        expo=ROOT.TF1("expo","[0]*e^(-[1]*(x -1126.)/13000.-[2]/((x-1126.)/13000.))+ [3]*e^(-[4]*(x -1126.)/13000.)",1000,8000)
        expo.SetParLimits(4,65.,200.)
    expo=ROOT.TF1("expo","[0]*e^(-[1]*(x -1125.)/13000.-[2]/((x-1125.)/13000.))+ [3]*e^(-[4]*(x -1125.)/13000.)",1000,8000)
    print expo
    if fixPars!=None:
        print " fixPars = ",fixPars
        expo.SetParLimits(4,0.,1000.)
        for key in fixPars.keys():
            p = fixPars[key]
            if key=="N0": expo.SetParameter(0,p); expo.SetParLimits(0,p-p/10000.,2.); 
            if key=="c1": expo.SetParameter(1,p); expo.SetParLimits(1,0.,p*3); 
            if key=="c2": expo.SetParameter(2,p); expo.SetParLimits(2,p-p/10000.,1.); 
            if key=="N1": expo.SetParameter(3,p); expo.SetParLimits(3,p-p/10000.,2.); 
            ##if key=="c3": expo.SetParLimits(4,fixPars[key],fixPars[key])
    #expo=ROOT.TF1("expo","[0]*e^(-[1]*x)*(1/x)",1000,8000)
    
    print " expo ",expo
    print " N0 ",expo.GetParameter(0)
    print " N1 ",expo.GetParameter(3)
    print " c1 ",expo.GetParameter(1)
    print " c2 ",expo.GetParameter(2)
    print " c3 ",expo.GetParameter(4)


    print " 1st fit "
    proj.Fit(expo,"LLMR","",beginFitX,endX)
    print " expo ",expo
    print " N0 ",expo.GetParameter(0)
    print " N1 ",expo.GetParameter(3)
    print " c1 ",expo.GetParameter(1)
    print " c2 ",expo.GetParameter(2)
    print " c3 ",expo.GetParameter(4)
    print expo.GetChisquare(),proj.GetNbinsX(),expo.GetChisquare()/proj.GetNbinsX()
    #p0 = expo.GetParameter(0)
    #p1 = expo.GetParameter(1)
    #expo=ROOT.TF1("expo","[0]*(e^(-[1]*x))*(1+TMath::Erf(x-[2]))",1000,8000) #*(1+TMath::Erf(x-[2]))
    #expo.SetParameters(0,p0)
    #expo.SetParameters(1,p1)
    #expo.SetParLimits(2,0,1000)
    #expo.SetParLimits(3,-50,110)
    #expo=ROOT.TF1("expo","expo(2)",1000,8000)
    #expo.SetParameters(0,16.,2.)
    print " 2nd fit "
    proj.Fit(expo,"LLMR","",beginFitX,endX)
    print " expo ",expo
    print " N0 ",expo.GetParameter(0)
    print " N1 ",expo.GetParameter(3)
    print " c1 ",expo.GetParameter(1)
    print " c2 ",expo.GetParameter(2)
    print " c3 ",expo.GetParameter(4)

    print expo.GetChisquare(),proj.GetNbinsX(),expo.GetChisquare()/proj.GetNbinsX()

    print " 3rd fit "
    proj.Fit(expo,"LLMR","",beginFitX,endX)
    print " expo ",expo
    print " N0 ",expo.GetParameter(0)
    print " N1 ",expo.GetParameter(3)
    print " c1 ",expo.GetParameter(1)
    print " c2 ",expo.GetParameter(2)
    print " c3 ",expo.GetParameter(4)

    print expo.GetChisquare(),proj.GetNbinsX(),expo.GetChisquare()/proj.GetNbinsX()

    return expo




def doC3Fit(proj,finalFit,label="",fixPars=None):
    if proj.Integral() == 0:
        print "histogram has zero integral "+proj.GetName()
        return 0
    scale = proj.Integral()
    proj.Scale(1.0/scale)
    
    
    beginFitX = options.minx
    endX =  options.maxx
    #expo=ROOT.TF1("expo","[0]*(1-x/13000.)^[1]/(x/13000)^[2]",1000,8000)
    #expo=ROOT.TF1("expo","[0]*(e^(-[1]*x/13000.))*(1-TMath::Erf(x/13000.-[2]))",1000,8000)
    #expo=ROOT.TF1("expo","[0]*e^(-[1]*(x -1125.)/13000.-[2]/((x-1125.)/13000.)+[3]*(x -1125.)/13000.*(x -1125.)/13000.+[4]*(x -1125.)/13000.*(x -1125.)/13000.*(x -1125.)/13000.)",1000,8000)
    print label
    if label == "Wjets": 
        expo=ROOT.TF1("expo","[0]*e^(-[1]*(x -1126.)/13000.-[2]/((x-1126.)/13000.))+ [3]*e^(-[4]*(x -1126.)/13000.)",1000,8000)
        expo.SetParLimits(4,65.,200.)
    expo=ROOT.TF1("expo","[0]*e^(-[1]*(x -1125.)/13000.-[2]/((x-1125.)/13000.))+ [3]*e^(-[4]*(x -1125.)/13000.)",1000,8000)
    print expo
    expo.SetParLimits(4,0.,1000.)
    print "N0 final fit ",finalFit.GetParameter(0)
    expo.FixParameter(0,finalFit.GetParameter(0)) #,finalFit.GetParameter(0));
    expo.FixParameter(1,finalFit.GetParameter(1)) #,finalFit.GetParameter(1));
    expo.FixParameter(2,finalFit.GetParameter(2)) #,finalFit.GetParameter(2));
    expo.FixParameter(3,finalFit.GetParameter(3)) #,finalFit.GetParameter(3));
    ##if key=="c3": expo.SetParLimits(4,fixPars[key],fixPars[key])
    #expo=ROOT.TF1("expo","[0]*e^(-[1]*x)*(1/x)",1000,8000)
    
    print " expo ",expo 
    print " N0 ",expo.GetParameter(0)
    print " N1 ",expo.GetParameter(3)
    print " c1 ",expo.GetParameter(1)
    print " c2 ",expo.GetParameter(2)
    print " c3 ",expo.GetParameter(4)


    print " 1st fit "
    proj.Fit(expo,"LLMR","",beginFitX,endX)
    print " expo ",expo
    print " N0 ",expo.GetParameter(0)
    print " N1 ",expo.GetParameter(3)
    print " c1 ",expo.GetParameter(1)
    print " c2 ",expo.GetParameter(2)
    print " c3 ",expo.GetParameter(4)
    print expo.GetChisquare(),proj.GetNbinsX(),expo.GetChisquare()/proj.GetNbinsX()
    #p0 = expo.GetParameter(0)
    #p1 = expo.GetParameter(1)
    #expo=ROOT.TF1("expo","[0]*(e^(-[1]*x))*(1+TMath::Erf(x-[2]))",1000,8000) #*(1+TMath::Erf(x-[2]))
    #expo.SetParameters(0,p0)
    #expo.SetParameters(1,p1)
    #expo.SetParLimits(2,0,1000)
    #expo.SetParLimits(3,-50,110)
    #expo=ROOT.TF1("expo","expo(2)",1000,8000)
    #expo.SetParameters(0,16.,2.)
    print " 2nd fit "
    proj.Fit(expo,"LLMR","",beginFitX,endX)
    print " expo ",expo
    print " N0 ",expo.GetParameter(0)
    print " N1 ",expo.GetParameter(3)
    print " c1 ",expo.GetParameter(1)
    print " c2 ",expo.GetParameter(2)
    print " c3 ",expo.GetParameter(4)

    print expo.GetChisquare(),proj.GetNbinsX(),expo.GetChisquare()/proj.GetNbinsX()

    print " 3rd fit "
    proj.Fit(expo,"LLMR","",beginFitX,endX)
    print " expo ",expo
    print " N0 ",expo.GetParameter(0)
    print " N1 ",expo.GetParameter(3)
    print " c1 ",expo.GetParameter(1)
    print " c2 ",expo.GetParameter(2)
    print " c3 ",expo.GetParameter(4)

    print expo.GetChisquare(),proj.GetNbinsX(),expo.GetChisquare()/proj.GetNbinsX()

    return expo

def doCFit(proj,finalFit,label="",fixPars=None):
    if proj.Integral() == 0:
        print "histogram has zero integral "+proj.GetName()
        return 0
    scale = proj.Integral()
    proj.Scale(1.0/scale)
    
    
    beginFitX = options.minx
    endX =  options.maxx
    print label
    if label == "Wjets": 
        expo=ROOT.TF1("expo","[0]*e^(-[1]*(x -1126.)/13000.-[2]/((x-1126.)/13000.))+ [3]*e^(-[4]*(x -1126.)/13000.)",1000,8000)
        expo.SetParLimits(4,65.,200.)
    expo=ROOT.TF1("expo","[0]*e^(-[1]*(x -1125.)/13000.-[2]/((x-1125.)/13000.))+ [3]*e^(-[4]*(x -1125.)/13000.)",1000,8000)
    print expo
    expo.SetParLimits(4,0.5*expo.GetParameter(4),1.5*expo.GetParameter(4)) 
    expo.SetParLimits(1,0.5*expo.GetParameter(1),1.5*expo.GetParameter(1))
    #expo.SetParameter(1,100.)
    expo.SetParLimits(2,0.5*expo.GetParameter(2),1.5*expo.GetParameter(2))

    print "N0 final fit ",finalFit.GetParameter(0)
    expo.FixParameter(0,finalFit.GetParameter(0)) #,finalFit.GetParameter(0));
    #expo.FixParameter(1,finalFit.GetParameter(1)) #,finalFit.GetParameter(1));
    #expo.FixParameter(2,finalFit.GetParameter(2)) #,finalFit.GetParameter(2));
    expo.FixParameter(3,finalFit.GetParameter(3)) #,finalFit.GetParameter(3));
    #expo.FixParameter(4,finalFit.GetParameter(4)) #,finalFit.GetParameter(3));
    ##if key=="c3": expo.SetParLimits(4,fixPars[key],fixPars[key])
    #expo=ROOT.TF1("expo","[0]*e^(-[1]*x)*(1/x)",1000,8000)
    
    print " expo ",expo 
    print " N0 ",expo.GetParameter(0)
    print " N1 ",expo.GetParameter(3)
    print " c1 ",expo.GetParameter(1)
    print " c2 ",expo.GetParameter(2)
    print " c3 ",expo.GetParameter(4)


    print " 1st fit "
    proj.Fit(expo,"LLMR","",beginFitX,endX)
    print " expo ",expo
    print " N0 ",expo.GetParameter(0)
    print " N1 ",expo.GetParameter(3)
    print " c1 ",expo.GetParameter(1)
    print " c2 ",expo.GetParameter(2)
    print " c3 ",expo.GetParameter(4)
    print expo.GetChisquare(),proj.GetNbinsX(),expo.GetChisquare()/proj.GetNbinsX()
    #p0 = expo.GetParameter(0)
    #p1 = expo.GetParameter(1)
    #expo=ROOT.TF1("expo","[0]*(e^(-[1]*x))*(1+TMath::Erf(x-[2]))",1000,8000) #*(1+TMath::Erf(x-[2]))
    #expo.SetParameters(0,p0)
    #expo.SetParameters(1,p1)
    #expo.SetParLimits(2,0,1000)
    #expo.SetParLimits(3,-50,110)
    #expo=ROOT.TF1("expo","expo(2)",1000,8000)
    #expo.SetParameters(0,16.,2.)
    print " 2nd fit "
    proj.Fit(expo,"LLMR","",beginFitX,endX)
    print " expo ",expo
    print " N0 ",expo.GetParameter(0)
    print " N1 ",expo.GetParameter(3)
    print " c1 ",expo.GetParameter(1)
    print " c2 ",expo.GetParameter(2)
    print " c3 ",expo.GetParameter(4)

    print expo.GetChisquare(),proj.GetNbinsX(),expo.GetChisquare()/proj.GetNbinsX()

    print " 3rd fit "
    proj.Fit(expo,"LLMR","",beginFitX,endX)
    print " expo ",expo
    print " N0 ",expo.GetParameter(0)
    print " N1 ",expo.GetParameter(3)
    print " c1 ",expo.GetParameter(1)
    print " c2 ",expo.GetParameter(2)
    print " c3 ",expo.GetParameter(4)

    print expo.GetChisquare(),proj.GetNbinsX(),expo.GetChisquare()/proj.GetNbinsX()

    return expo

weights_ = options.weights.split(',')

random=ROOT.TRandom3(101082)

sampleTypes=options.samples.split(',')



print "Creating datasets for samples: " ,sampleTypes
list_dataPlotters = []
list_dataPlottersNW=[]

folders = str(args[0]).split(",")
for folder in folders:
    for filename in os.listdir(folder):
        for sampleType in sampleTypes:
            if filename.find(sampleType)!=-1:
                if filename.find(".")==-1: continue
                fnameParts=filename.split('.')
                fname=fnameParts[0]
                ext=fnameParts[1]
                if ext.find("root") ==-1: continue
                year=folder.split("/")[-2]
                print "year ",year
                ctx = cuts.cuts("init_VV_VH.json",year,"dijetbins_random")
                luminosity=   ctx.lumi[year]/ctx.lumi["Run2"]
                if options.output.find("Run2") ==-1: luminosity = 1
                print " fraction of lumi ",luminosity
                list_dataPlotters.append(TreePlotter(folder+'/'+fname+'.root','AnalysisTree'))
                list_dataPlotters[-1].setupFromFile(folder+'/'+fname+'.pck')
                list_dataPlotters[-1].addCorrectionFactor('xsec','tree')
                list_dataPlotters[-1].addCorrectionFactor(luminosity,'flat')
                list_dataPlotters[-1].addCorrectionFactor('genWeight','tree')
                list_dataPlotters[-1].addCorrectionFactor('puWeight','tree')
                if fname.find("QCD_Pt_") !=-1 or fname.find("QCD_HT") !=-1:
                    print "going to apply spikekiller for ",fname
                    list_dataPlotters[-1].addCorrectionFactor('b_spikekiller','tree')
                if filename.find("TT")!=-1:
                    #we consider ttbar with reweight applyied as nominal!
                    list_dataPlotters[-1].addCorrectionFactor('TopPTWeight','tree')
                if options.triggerW:
                    list_dataPlotters[-1].addCorrectionFactor('triggerWeight','tree')
                    print "Using trigger weights from tree"
                for w in weights_:
                    if w != '': list_dataPlotters[-1].addCorrectionFactor(w,'branch')
                corrFactor = 1
                if filename.find('Z') != -1:
                    corrFactor = options.corrFactorZ
                    print "add correction factor for Z+jets sample"
                if filename.find('W') != -1:
                    corrFactor = options.corrFactorW
                    print "add correction factor for W+jets sample"
                list_dataPlotters[-1].addCorrectionFactor(corrFactor,'flat')
                list_dataPlotters[-1].filename=fname

                list_dataPlottersNW.append(TreePlotter(folder+'/'+fname+'.root','AnalysisTree'))
                list_dataPlottersNW[-1].addCorrectionFactor('puWeight','tree')
                list_dataPlottersNW[-1].addCorrectionFactor('genWeight','tree')
                list_dataPlottersNW[-1].addCorrectionFactor(luminosity,'flat')
                if fname.find("QCD_Pt_") !=-1 or fname.find("QCD_HT") !=-1:
                    print "going to apply spikekiller for ",fname
                    list_dataPlottersNW[-1].addCorrectionFactor('b_spikekiller','tree')
                if options.triggerW: list_dataPlottersNW[-1].addCorrectionFactor('triggerWeight','tree')
                list_dataPlottersNW[-1].addCorrectionFactor(corrFactor,'flat')
                for w in weights_:
                    if w != '': list_dataPlottersNW[-1].addCorrectionFactor(w,'branch')
                if options.triggerW: list_dataPlottersNW[-1].addCorrectionFactor('triggerWeight','tree')
                # for different background -> add reweighting of pT spectrum
                #if filename.find("Jets")!=-1:
                #list_dataPlottersNW[-1].addCorrectionFactor("(1+ 0.00027272727*pow(jj_l1_gen_pt, 1) )*(1 + 0.00027272727 * pow(jj_l2_gen_pt, 1))","branch")
                #list_dataPlottersNW[-1].addCorrectionFactor("sqrt((1.05*pow(jj_l1_gen_pt, 1) )*(1.05 * pow(jj_l2_gen_pt, 1)))","branch")
                #list_dataPlottersNW[-1].addCorrectionFactor("(1+ pow(5500*jj_l1_gen_pt, 2) )*(1 + pow(5500*jj_l2_gen_pt, 2))","branch")
                list_dataPlottersNW[-1].addCorrectionFactor(corrFactor,'flat')
                list_dataPlottersNW[-1].filename=fname
      


binning = getBinning(options.binsMVV,options.minx,options.maxx,options.binsx)
print binning


#distribution of mjet from simulation --> use to validate kernel
mvv_nominal=ROOT.TH1F("mvv_nominal","mvv_nominal",len(array('f',binning))-1,array('f',binning))
mvv_nominal_w=ROOT.TH1F("mvv_nominal_w","mvv_nominal_w",len(array('f',binning))-1,array('f',binning))
mvv_nominal.Sumw2()



maxEvents = -1
#ok lets populate!

#Nominal histogram Pythia:
#here pick the right plotters!
print list_dataPlotters
print list_dataPlottersNW
if len(list_dataPlotters) > 0:
    for plotter in list_dataPlotters:
        print "make shapes for Vjets or TTbar"
        histI2=plotter.drawTH1Binned('jj_LV_mass',options.cut,"1",array('f',binning))
        print "data Integral "+str(histI2.Integral())
        mvv_nominal.Add(histI2)
#if options.samples.find("TT")!=-1:
if len(list_dataPlottersNW) > 0:
    for plotter in list_dataPlottersNW:
        print "make weighted shape for TTbar"
        histI2=plotter.drawTH1Binned('jj_LV_mass',options.cut,"1",array('f',binning))
        print "data Integral "+str(histI2.Integral())
        mvv_nominal_w.Add(histI2)
            
print " ********** Done making hist now do the fit ******************"

fixPars = {"N0":0,"N1":0,"c1":100,"c2":0}
finalFit = doFit(mvv_nominal,((options.output).split("_")[2]).split(".")[0],fixPars)


print "************************ do debugging plots *******************"

doPlotRatio(mvv_nominal,finalFit,sampleTypes,((options.output).split("_")[2]).split(".")[0]+"_"+((options.output).split("_")[1]).split(".")[0],mvv_nominal_w)

print " **************************** write fit to json ***************"
print " open json file ",options.output
f=open(options.output,"w")
parametrization = getParametrization(finalFit)
json.dump(parametrization,f)
#f.close()

if options.samples.find("TT")!=-1: 
    print " ********** Making fit without reweight  ******************"

    #noreweightFit = doFit(mvv_nominal_w,((options.output).split("_")[2]).split(".")[0])
    #noreweightFit = doC3Fit(mvv_nominal_w,finalFit,((options.output).split("_")[2]).split(".")[0])
    noreweightFit = doCFit(mvv_nominal_w,finalFit,((options.output).split("_")[2]).split(".")[0])


    print "************************ do plots *******************"

    doPlotCRatio(mvv_nominal,noreweightFit,sampleTypes,((options.output).split("_")[2]).split(".")[0]+"_"+((options.output).split("_")[1]).split(".")[0]+"_noreweight",mvv_nominal_w)

    print " **************************** write fit to json ***************"
    jsonname="noreweight_"+options.output
    print " open json file ",jsonname
    f=open(jsonname,"w")
    parametrization = getParametrization(noreweightFit)
    json.dump(parametrization,f)


#print " ********** Make PT reweighted histograms ********************"
#alpha=1.5/float(options.maxx)
#histogram_pt_down,histogram_pt_up=unequalScale(mvv_nominal,"mvv_PT",alpha)

#alpha=1.5*float(options.minx)
#histogram_opt_down,histogram_opt_up=unequalScale(mvv_nominal,"mvv_OPT",alpha)

#alpha=float(options.maxx)*float(options.maxx)
#histogram_pt2_down,histogram_pt2_up=unequalScale(mvv_nominal,"mvv_PT2",alpha,2)

#alpha=float(options.minx)*float(options.minx)
#histogram_opt2_down,histogram_opt2_up=unequalScale(mvv_nominal,"mvv_OPT2",alpha,2)

#print " ************************* try final fit on reweighted histos BUT this time only c2 is floating ************"


#Fit = doFit(histogram_pt_down,((options.output).split("_")[-1]).split(".")[0]+"_pt_down",parametrization)
#doPlot(histogram_pt_down,Fit,sampleTypes,((options.output).split("_")[-1]).split(".")[0]+"_pt_down")
#Fit = doFit(histogram_pt_up,((options.output).split("_")[-1]).split(".")[0]+"_pt_up",parametrization)
#doPlot(histogram_pt_up,Fit,sampleTypes,((options.output).split("_")[-1]).split(".")[0]+"_pt_up")
#Fit = doFit(histogram_opt_down,((options.output).split("_")[-1]).split(".")[0]+"_opt_down",parametrization)
#doPlot(histogram_opt_down,Fit,sampleTypes,((options.output).split("_")[-1]).split(".")[0]+"_opt_down")
#Fit = doFit(histogram_opt_up,((options.output).split("_")[-1]).split(".")[0]+"_opt_up",parametrization)
#doPlot(histogram_opt_up,Fit,sampleTypes,((options.output).split("_")[-1]).split(".")[0]+"_opt_up")
#Fit = doFit(histogram_pt2_down,((options.output).split("_")[-1]).split(".")[0]+"_pt2_down",parametrization)
#doPlot(histogram_pt2_down,Fit,sampleTypes,((options.output).split("_")[-1]).split(".")[0]+"_pt2_down")
#Fit = doFit(histogram_pt2_up,((options.output).split("_")[-1]).split(".")[0]+"_pt2_up",parametrization)
#doPlot(histogram_pt2_up,Fit,sampleTypes,((options.output).split("_")[-1]).split(".")[0]+"_pt2_up")

#Fit = doFit(histogram_opt2_down,((options.output).split("_")[-1]).split(".")[0]+"_opt2_down",parametrization)
#doPlot(histogram_opt2_down,Fit,sampleTypes,((options.output).split("_")[-1]).split(".")[0]+"_opt2_down")
#Fit = doFit(histogram_opt2_up,((options.output).split("_")[-1]).split(".")[0]+"_opt2_up",parametrization)
#doPlot(histogram_opt2_up,Fit,sampleTypes,((options.output).split("_")[-1]).split(".")[0]+"_opt2_up")
