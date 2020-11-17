#!/usr/bin/env python 
# make tree containing genweight, other event weights, as well as is jet H/ V jet, what category is the event classified in, what V/Htag has each jet -> for each signal sample!
#use this as input for the migrationUncertainties.py script
import ROOT
import os, sys, re, optparse,pickle,shutil,json,time
from collections import defaultdict
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
from array import array
ROOT.gROOT.ProcessLine("struct rootint { Int_t ri;};")
from ROOT import rootint
ROOT.gROOT.ProcessLine("struct rootfloat { Float_t rf;};")
from ROOT import rootfloat
ROOT.gROOT.ProcessLine("struct rootlong { Long_t li;};")
from ROOT import rootlong

from rootpy.tree import CharArrayCol
sys.path.insert(0, "../interactive/")
import cuts
# python categorisation.py -y "2016" -s WJetsToQQ -d deepAK8V2/
# python categorisation.py -y "2016,2017,2018" -s WJetsToQQ -d deepAK8V2/
# python categorisation.py -y "2016" -s BulkGravToWW -d deepAK8V2/

parser = optparse.OptionParser()
parser.add_option("-y","--year",dest="year",default='2016',help="year of data taking")
parser.add_option("-s","--signal",dest="signal",help="signal to categorise",default='ZprimeToZh')
parser.add_option("-d","--directory",dest="directory",help="directory with signal samples",default='deepAK8V2/')

(options,args) = parser.parse_args()



def getSamplelist(directories,signal,minMX=1200.,maxMX=8000.):
    samples = {}
    dirs=directories.split(",")
    for directory in dirs:
        for filename in os.listdir(directory):
            if filename.find(signal)!=-1 and filename.find('root')!=-1:
                if filename.find("VBF")!=-1 and signal.find("VBF")==-1: continue  
                fnameParts=filename.split('.')
                fname=fnameParts[0]

                mass = float(fname.split('_')[-1])
                if mass < minMX or mass > maxMX: continue
                print fname 
                if fname not in samples:         
                    samples.update({fname : []}   )
                    samples[fname].append(directory+fname)
                else:
                    samples[fname].append(directory+fname)
                print 'found ',directory+fname,' mass',str(mass)


    complete_mass = {} #defaultdict(dict)
    for mass in samples.keys():
        print mass
        x = samples[mass]
        if len(x) < len(dirs):    
            print "!!!!    directories missing for mass", mass ," !!!!!!!! only ",x, "available "
        else:
            complete_mass.update({ mass: x})


    print " complete ",complete_mass

    return complete_mass



def getBkgSamplelist(directories,signal):
    samples = {}
    dirs=directories.split(",")
    for directory in dirs:
        for filename in os.listdir(directory):
            if filename.find(signal)!=-1 and filename.find('root')!=-1:
                if filename.find("VBF")!=-1 and signal.find("VBF")==-1: continue
                fnameParts=filename.split('.')
                fname=fnameParts[0]
                fpart=fnameParts[0].split("_")[0]
                if fpart not in samples:
                    samples.update({fpart : []}   )
                    samples[fpart].append(directory+fname)
                else:
                    samples[fpart].append(directory+fname)
                print 'found ',directory+fname

    print "samples ",samples
    return samples




def selectSignalTree(cs,sample):
    print sample 
    chain = ROOT.TChain('AnalysisTree')
    tmpname = "tmp_"+time.strftime("%Y%m%d-%H%M%S")
    outfile = ROOT.TFile(tmpname+'.root','RECREATE')
    for signal in sample:
        rfile = signal+".root"
        chain.Add(rfile)
        print " entries ",chain.GetEntries()

    bigtree = chain.CopyTree("1")
    finaltree = chain.CopyTree(cs['common']+'*'+cs['acceptance'])
    print 'overall entries in tree '+str(chain.GetEntries())
    print 'entries after analysis selections '+str(finaltree.GetEntries())
    signaltree_VH_HPHP = finaltree.CopyTree(cs['VH_HPHP'])
    signaltree_VV_HPHP = finaltree.CopyTree(cs['VV_HPHP'])#all other categories before are explicitly removed so that each event can only live in one category!!
    signaltree_VH_LPHP = finaltree.CopyTree(cs['VH_LPHP'])
    signaltree_VH_HPLP = finaltree.CopyTree(cs['VH_HPLP'])
    signaltree_VV_HPLP = finaltree.CopyTree(cs['VV_HPLP'])
    rest = finaltree.CopyTree('!('+cs['VV_HPLP']+')*!('+cs['VH_LPHP']+')*!('+cs['VH_HPLP']+')*!('+cs['VH_HPHP']+')*!('+cs['VV_HPHP']+')')
    print ' #event VH_HPHP '+str(signaltree_VH_HPHP.GetEntries())+' #event VV_HPHP '+str(signaltree_VV_HPHP.GetEntries())+' #event VH_LPHP '+str(signaltree_VH_LPHP.GetEntries())+' #event VH_LPHP '+str(signaltree_VH_LPHP.GetEntries())+' #event VV_HPLP '+str(signaltree_VV_HPLP.GetEntries())
    print '#event no category '+str(rest.GetEntries())
    sumcat = signaltree_VH_HPHP.GetEntries()+signaltree_VV_HPHP.GetEntries()+signaltree_VH_LPHP.GetEntries()+signaltree_VH_HPLP.GetEntries()+signaltree_VV_HPLP.GetEntries()
    print 'sum '+str(sumcat)
    print 'overall signal efficiency after selection cut '+str(finaltree.GetEntries()/float(chain.GetEntries()))
    print 'signal efficiency after category cuts '+str(sumcat/float(chain.GetEntries()))
    if finaltree.GetEntries() !=0 :
        print 'efficiency of all category cuts '+str(sumcat/float(finaltree.GetEntries()))
    else: 
        print ' no events left after preselection, presumably it is a low pt bin sample '
    signaltree_VH_HPHP.SetName('VH_HPHP')
    signaltree_VV_HPHP.SetName('VV_HPHP')
    signaltree_VH_LPHP.SetName('VH_LPHP')
    signaltree_VH_HPLP.SetName('VH_HPLP')
    signaltree_VV_HPLP.SetName('VV_HPLP')
    bigtree.SetName('all')
    finaltree.SetName('commonacceptance')
    signaltree_VH_HPHP.Write()
    signaltree_VV_HPHP.Write()
    signaltree_VH_LPHP.Write()
    signaltree_VH_HPLP.Write()
    signaltree_VV_HPLP.Write()
    finaltree.Write()
    bigtree.Write()
    outfile.Close()

    return tmpname


def calculateSF(self,event,ctx,year,jet,SF=1,eff_vtag=[1,1],eff_htag=[1,1],mistag_top=[1,1],TTruth1=0,TTruth2=0,tag1="",tag2=""):
    VTruth = event.jj_l1_mergedVTruth
    HTruth = event.jj_l1_mergedHTruth
    ZbbTruth = event.jj_l1_mergedZbbTruth
    TTruth = TTruth1
    jetTag = tag1
    if jet == 2:
        VTruth = event.jj_l2_mergedVTruth
        HTruth = event.jj_l2_mergedHTruth
        ZbbTruth = event.jj_l2_mergedZbbTruth
        TTruth = TTruth2
        jetTag = tag2

    jetTruth = ""
    '''
    print " jet ",jet
    print " VTruth ",VTruth
    print " HTruth ",HTruth
    print " ZbbTruth ",ZbbTruth
    print " TTruth ",TTruth
    print " jetTag ",jetTag
    '''
    if VTruth ==1 :
        jetTruth = "V"
    elif  HTruth ==1 or ZbbTruth ==1 :
        jetTruth = "H"
    elif TTruth == 1:
        jetTruth = "top"
    #print " jetTruth ",jetTruth
    if (jetTruth=='H' or jetTruth=='V'):
        #print " jetTruth H or V"
        if jetTag == 'HPHtag':
            #print "jetTag== HPHtag"
            SF *= ctx.HPSF_htag[year]
            eff_htag[0] *= (ctx.HPSF_htag[year]+ctx.H_tag_unc_HP[year])
            eff_htag[1] *= (ctx.HPSF_htag[year]-ctx.H_tag_unc_HP[year])
            #print "********************      SF ",SF
            #print "eff_htag[0] ",eff_htag[0]
        elif jetTag == 'LPHtag':
            #print "LPHtag "
            SF *= ctx.LPSF_htag[year]
            eff_htag[0] *= (ctx.LPSF_htag[year]+ctx.H_tag_unc_LP[year])
            eff_htag[1] *= (ctx.LPSF_htag[year]-ctx.H_tag_unc_LP[year])
            #print "********************      SF ",SF
            #print "eff_htag[0] ",eff_htag[0]
        elif jetTag == 'HPVtag':
            #print "jetTag== HPVtag"
            SF *= ctx.HPSF_vtag[year]
            eff_vtag[0] *= (ctx.HPSF_vtag[year]+ctx.W_tag_unc_HP[year])
            eff_vtag[1] *= (ctx.HPSF_vtag[year]-ctx.W_tag_unc_HP[year])
            #print "********************      SF ",SF
            #print "eff_wtag[0] ",eff_vtag[0]
        elif jetTag == 'LPVtag':
            #print "LPVtag "
            SF *= ctx.LPSF_vtag[year]
            eff_vtag[0] *= (ctx.LPSF_vtag[year]+ctx.W_tag_unc_LP[year])
            eff_vtag[1] *= (ctx.LPSF_vtag[year]-ctx.W_tag_unc_LP[year])
            #print "********************      SF ",SF
            #print "eff_wtag[0] ",eff_vtag[0]
        #else:
            #print " jetTag is ",jetTag
    elif jetTruth=='top' :
        #print " this is a top!"
        if jetTag == 'HPHtag':
            #print "jetTag== HPHtag"
            SF *= ctx.HPSF_toptag[year]
            mistag_top[0] *= (ctx.HPSF_toptag[year]+ctx.TOP_tag_unc_HP[year])
            mistag_top[1] *= (ctx.HPSF_toptag[year]-ctx.TOP_tag_unc_HP[year])
            #print "********************      SF ",SF
            #print "mistag_top[0] ",mistag_top[0]
        elif jetTag == 'LPHtag':
            SF *= ctx.LPSF_toptag[year]
            mistag_top[0] *= (ctx.LPSF_toptag[year]+ctx.TOP_tag_unc_LP[year])
            mistag_top[1] *= (ctx.LPSF_toptag[year]-ctx.TOP_tag_unc_LP[year])
    #else:
        #print "***********************       this jet do not contain V, H and top     **************************"
    #print "SF ",SF
    #print " mistag_top ",mistag_top
    #print "eff_vtag ",eff_vtag
    return SF,eff_vtag,eff_htag,mistag_top

class myTree:
    
    run = rootint()
    lumi = rootint()
    puWeight  = rootfloat()
    genWeight = rootfloat()
    xsec      = rootfloat()
    evt       = rootlong()

    sf  = rootfloat()
    CMS_eff_vtag_sf_up = rootfloat()
    CMS_eff_vtag_sf_down = rootfloat()
    CMS_eff_htag_sf_up = rootfloat()
    CMS_eff_htag_sf_down = rootfloat()
    CMS_mistag_top_sf_up = rootfloat()
    CMS_mistag_top_sf_down = rootfloat()
    
    jj_l1_mergedVTruth           = rootint()
    jj_l2_mergedVTruth           = rootint()
    
    jj_l1_mergedHTruth           = rootint()
    jj_l2_mergedHTruth           = rootint()
    
    jj_l1_mergedTopTruth           = rootint()
    jj_l2_mergedTopTruth           = rootint()

    jj_l1_mergedZbbTruth           = rootint()
    jj_l2_mergedZbbTruth           = rootint()
    
    jj_l1_jetTag           = bytearray(6)
    jj_l2_jetTag           = bytearray(6)
    
    category               =  bytearray(7)
    newTree = None
    File = None
    
    def __init__(self, treename,outfile):
        self.File = outfile
        self.File.cd()
    #ROOT.gROOT.ProcessLine("struct string { TString s;};")
    #from ROOT import string
        self.newTree = ROOT.TTree(treename,treename)

        self.newTree.Branch("SF",self.sf,"SF/F")
        self.newTree.Branch("CMS_eff_vtag_sf_up",self.CMS_eff_vtag_sf_up,"CMS_eff_vtag_sf_up/F")
        self.newTree.Branch("CMS_eff_vtag_sf_down",self.CMS_eff_vtag_sf_down,"CMS_eff_vtag_sf_down/F")
        self.newTree.Branch("CMS_eff_htag_sf_up",self.CMS_eff_htag_sf_up,"CMS_eff_htag_sf_up/F")
        self.newTree.Branch("CMS_eff_htag_sf_down",self.CMS_eff_htag_sf_down,"CMS_eff_htag_sf_down/F")
        self.newTree.Branch("CMS_mistag_top_sf_up",self.CMS_mistag_top_sf_up,"CMS_mistag_top_sf_up/F")
        self.newTree.Branch("CMS_mistag_top_sf_down",self.CMS_mistag_top_sf_down,"CMS_mistag_top_sf_down/F")

        self.newTree.Branch("run",self.run,"run/i")
        self.newTree.Branch("lumi",self.lumi,"lumi/i")
        self.newTree.Branch("evt",self.evt,"evt/l")
        self.newTree.Branch("xsec",(self.xsec),"xsec/F")        
        self.newTree.Branch("puWeight",(self.puWeight),"puWeight/F")                 
        self.newTree.Branch("genWeight",(self.genWeight),"genWeight/F")
   
        self.newTree.Branch("jj_l1_mergedVTruth",self.jj_l1_mergedVTruth,"jj_l1_mergedVTruth/i")
        self.newTree.Branch("jj_l2_mergedVTruth",self.jj_l2_mergedVTruth,"jj_l2_mergedVTruth/i")
        self.newTree.Branch("jj_l1_mergedHTruth",self.jj_l1_mergedHTruth,"jj_l1_mergedHTruth/i")
        self.newTree.Branch("jj_l2_mergedHTruth",self.jj_l2_mergedHTruth,"jj_l2_mergedHTruth/i")
        self.newTree.Branch("jj_l1_mergedTopTruth",self.jj_l1_mergedTopTruth,"jj_l1_mergedTopTruth/i")
        self.newTree.Branch("jj_l2_mergedTopTruth",self.jj_l2_mergedTopTruth,"jj_l2_mergedTopTruth/i")
        self.newTree.Branch("jj_l1_mergedZbbTruth",self.jj_l1_mergedZbbTruth,"jj_l1_mergedZbbTruth/i")
        self.newTree.Branch("jj_l2_mergedZbbTruth",self.jj_l2_mergedZbbTruth,"jj_l2_mergedZbbTruth/i")
   
        self.newTree.Branch("jj_l1_jetTag",self.jj_l1_jetTag,"jj_l1_jetTag[6]/C")
        self.newTree.Branch("jj_l2_jetTag",self.jj_l2_jetTag,"jj_l2_jetTag[6]/C")
     
        self.newTree.Branch("category",self.category,"category[7]/C")
        
    def setOutputTreeBranchValues(self,cat,ctx,tmpname,year):
        print " setOutputTreeBranchValues ",cat
        rf = ROOT.TFile(tmpname+'.root','READ')
        cattree = rf.Get(cat)
        print " cat "+cat+" "+str(cattree.GetEntries())


        ZHbb_branch_l1 = cattree.GetBranch(ctx.varl1Htag)
        ZHbb_leaf_l1 = ZHbb_branch_l1.GetLeaf(ctx.varl1Htag)
        W_branch_l1 = cattree.GetBranch(ctx.varl1Wtag)
        W_leaf_l1 = W_branch_l1.GetLeaf(ctx.varl1Wtag)
        ZHbb_branch_l2 = cattree.GetBranch(ctx.varl2Htag)
        ZHbb_leaf_l2 = ZHbb_branch_l2.GetLeaf(ctx.varl2Htag)
        W_branch_l2 = cattree.GetBranch(ctx.varl2Wtag)
        W_leaf_l2 = W_branch_l2.GetLeaf(ctx.varl2Wtag)
        
        
        WPHP_ZHbb_branch_l1 = cattree.GetBranch(ctx.WPHPl1Htag)
        WPHP_ZHbb_leaf_l1 = WPHP_ZHbb_branch_l1.GetLeaf(ctx.WPHPl1Htag)
        WPHP_W_branch_l1 = cattree.GetBranch(ctx.WPHPl1Wtag)
        WPHP_W_leaf_l1 = WPHP_W_branch_l1.GetLeaf(ctx.WPHPl1Wtag)
        
        WPHP_ZHbb_branch_l2 = cattree.GetBranch(ctx.WPHPl2Htag)
        WPHP_ZHbb_leaf_l2 = WPHP_ZHbb_branch_l2.GetLeaf(ctx.WPHPl2Htag)
        WPHP_W_branch_l2 = cattree.GetBranch(ctx.WPHPl2Wtag)
        WPHP_W_leaf_l2 = WPHP_W_branch_l2.GetLeaf(ctx.WPHPl2Wtag)
        
        
        WPLP_ZHbb_branch_l1 = cattree.GetBranch(ctx.WPLPl1Htag)
        WPLP_ZHbb_leaf_l1 = WPLP_ZHbb_branch_l1.GetLeaf(ctx.WPLPl1Htag)
        WPLP_W_branch_l1 = cattree.GetBranch(ctx.WPLPl1Wtag)
        WPLP_W_leaf_l1 = WPLP_W_branch_l1.GetLeaf(ctx.WPLPl1Wtag)
        
        WPLP_ZHbb_branch_l2 = cattree.GetBranch(ctx.WPLPl2Htag)
        WPLP_ZHbb_leaf_l2 = WPLP_ZHbb_branch_l2.GetLeaf(ctx.WPLPl2Htag)
        WPLP_W_branch_l2 = cattree.GetBranch(ctx.WPLPl2Wtag)
        WPLP_W_leaf_l2 = WPLP_W_branch_l2.GetLeaf(ctx.WPLPl2Wtag)

        
        for event in cattree:
            self.puWeight.rf       = event.puWeight 
            self.genWeight.rf      = event.genWeight
            self.xsec.rf           = event.xsec     
            self.evt.rl            = event.evt                  
            self.lumi.ri           = event.lumi
            self.run.ri = event.run 
            
            self.jj_l1_mergedVTruth.ri = event.jj_l1_mergedVTruth
            self.jj_l2_mergedVTruth.ri = event.jj_l2_mergedVTruth
            self.jj_l1_mergedHTruth.ri = event.jj_l1_mergedHTruth
            self.jj_l2_mergedHTruth.ri = event.jj_l2_mergedHTruth
            try:
                self.jj_l1_mergedTopTruth.ri = event.jj_l1_mergedTopTruth
                self.jj_l2_mergedTopTruth.ri = event.jj_l2_mergedTopTruth
            except:
                self.jj_l1_mergedTopTruth.ri = 0
                self.jj_l2_mergedTopTruth.ri = 0

            self.jj_l1_mergedZbbTruth.ri = event.jj_l1_mergedZbbTruth
            self.jj_l2_mergedZbbTruth.ri = event.jj_l2_mergedZbbTruth
            if cat !='all':
                self.category[:7] = cat
            else: self.category[:7] = "0"
            # this depends now on the actual cuts in the analysis!!
            if ZHbb_leaf_l1.GetValue() > WPHP_ZHbb_leaf_l1.GetValue():
                self.jj_l1_jetTag[:6] = 'HPHtag'
            elif W_leaf_l1.GetValue() > WPHP_W_leaf_l1.GetValue():
                self.jj_l1_jetTag[:6] = 'HPVtag'
            elif ZHbb_leaf_l1.GetValue() > WPLP_ZHbb_leaf_l1.GetValue():
                self.jj_l1_jetTag[:6] = 'LPHtag'
            elif W_leaf_l1.GetValue() > WPLP_W_leaf_l1.GetValue():
                self.jj_l1_jetTag[:6] = 'LPVtag'
            else:
                self.jj_l1_jetTag[:6] = 'Notag'
                
            #print   WPLP_W_leaf_l1.GetValue()  
            if ZHbb_leaf_l2.GetValue() > WPHP_ZHbb_leaf_l2.GetValue():
                self.jj_l2_jetTag[:6] = 'HPHtag'
            elif W_leaf_l2.GetValue() > WPHP_W_leaf_l2.GetValue():
                self.jj_l2_jetTag[:6] = 'HPVtag'
            elif ZHbb_leaf_l2.GetValue() > WPLP_ZHbb_leaf_l2.GetValue():
                self.jj_l2_jetTag[:6] = 'LPHtag'
            elif W_leaf_l2.GetValue() > WPLP_W_leaf_l2.GetValue():
                self.jj_l2_jetTag[:6] = 'LPVtag'
            else:
                self.jj_l2_jetTag[:6] = 'Notag'

            tag1=self.jj_l1_jetTag[:6]
            tag2=self.jj_l2_jetTag[:6]

            SF = 1.0
            CMS_eff_vtag_sf = [1.0,1.0] #for up and down variations                                                                                                                                                               
            CMS_eff_htag_sf = [1.0,1.0]
            CMS_mistag_top_sf = [1.0,1.0]
            jet = 1
            SF,CMS_eff_vtag_sf,CMS_eff_htag_sf,CMS_mistag_top_sf = calculateSF(self,event,ctx,year,jet,SF,CMS_eff_vtag_sf,CMS_eff_htag_sf,CMS_mistag_top_sf,self.jj_l1_mergedTopTruth,self.jj_l2_mergedTopTruth,tag1,tag2)
            jet = 2
            SF,CMS_eff_vtag_sf,CMS_eff_htag_sf,CMS_mistag_top_sf = calculateSF(self,event,ctx,year,jet,SF,CMS_eff_vtag_sf,CMS_eff_htag_sf,CMS_mistag_top_sf,self.jj_l1_mergedTopTruth,self.jj_l2_mergedTopTruth,tag1,tag2)
            #print " final SF ",SF
            #print
            self.sf.rf = SF
            self.CMS_eff_vtag_sf_up.rf = CMS_eff_vtag_sf[0]
            self.CMS_eff_vtag_sf_down.rf = CMS_eff_vtag_sf[1]
            self.CMS_eff_htag_sf_up.rf = CMS_eff_htag_sf[0]
            self.CMS_eff_htag_sf_down.rf = CMS_eff_htag_sf[1]
            self.CMS_mistag_top_sf_up.rf = CMS_mistag_top_sf[0]
            self.CMS_mistag_top_sf_down.rf = CMS_mistag_top_sf[1]


            #print self.jj_l1_jetTag
            self.newTree.Fill()
        print 'number of events in this category '+str(self.newTree.GetEntries())

    def test(self):
        for event in self.newTree:
            print event.jj_l1_mergedVTruth
            print event.jj_l1_mergedTopTruth
            print event.jj_l2_mergedTopTruth
    def write(self,name=""):
        self.File.cd()
        self.newTree.Write(name)

if __name__=='__main__':
    if options.directory.find(options.year)== -1: print 'ATTENTION: are you sure you are using the right directory for '+options.year+' data?'    
    period = options.year
    ctx  = cuts.cuts("init_VV_VH.json",period,"random_dijetbins")
    samples=""
    basedir=options.directory
    filePeriod=options.year

    if options.year.find(",")!=-1:
        period = options.year.split(',')
        filePeriod="Run2"

        for year in period:
            print year
            if year==period[-1]: samples+=basedir+"/"
            else: samples+=basedir+"/,"
    else: 
        samples=basedir+"/"
    outfile = ROOT.TFile('migrationunc/'+options.signal+'_'+filePeriod+'.root','RECREATE')

    samplelist= getBkgSamplelist(samples,options.signal)
    print " samplelist ", samplelist

    for sample in samplelist.keys():
        print sample
        print 'init new tree'
        outtree = myTree(sample,outfile)
        outtreeAll = myTree(sample,outfile)
        print 'select common cuts signal tree' 
        tmpfilename = selectSignalTree(ctx.cuts,samplelist[sample])
        print " tmpfilename ",tmpfilename
        outtree.setOutputTreeBranchValues('VH_HPHP',ctx,tmpfilename,filePeriod)
        outtree.setOutputTreeBranchValues('VV_HPHP',ctx,tmpfilename,filePeriod)
        outtree.setOutputTreeBranchValues('VH_LPHP',ctx,tmpfilename,filePeriod)
        outtree.setOutputTreeBranchValues('VH_HPLP',ctx,tmpfilename,filePeriod)
        outtree.setOutputTreeBranchValues('VV_HPLP',ctx,tmpfilename,filePeriod)
        outfile.cd()
        outtree.write('signalregion')
        outtreeAll.setOutputTreeBranchValues('all',ctx,tmpfilename,filePeriod)
        outfile.cd()
        outtreeAll.write('all')
        
        os.system("rm "+tmpfilename+".root")
        
