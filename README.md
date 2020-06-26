# VV statistical analysis in 10X

Prepare the working directory with Higgs Combine Tools. Use the 10X release compatible with the [UHH framework](https://github.com/UHH2/UHH2). If you have that already installed you do
not need to check out the CMSSW release again.

```
mkdir VVAnalysisWith2DFit
mkdir CMGToolsForStat10X
cd CMGToolsForStat10X
export SCRAM_ARCH=slc6_amd64_gcc700
cmsrel CMSSW_10_2_10
cd CMSSW_10_2_10/src
cmsenv
git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
cd $CMSSW_BASE/src/HiggsAnalysis/CombinedLimit
git fetch origin
git checkout v8.0.0
scramv1 b clean && scramv1 b -j 8
```
NB: currently under test: https://github.com/IreneZoi/HiggsAnalysis-CombinedLimit.git branch my_102x with the commit https://github.com/IreneZoi/HiggsAnalysis-CombinedLimit/commit/157d5e0849eb3e03811ca638c00e8470903d958c to manage to have a workspace with all the needed categories

Fork cmgtools from https://github.com/Diboson3D/cmgtools-lite and checkout the VV statistical tools

```
cd ../..
export GITUSER=`git config user.github`
git clone https://github.com/${GITUSER}/cmgtools-lite CMGTools
cd CMGTools
git remote add Diboson3D https://github.com/Diboson3D/cmgtools-lite -b VV_VH
git fetch Diboson3D
git checkout -b VV_VH Diboson3D/VV_VH
scram b -j 8
cd VVResonances/interactive
```
NB to run on the 3 Run2 years some changes have been made and the soft link below should point to the folder cointaining the years subfolder

```
ln -s samples_location simboliklinkname

```

Current sample location with random sorting of jet1 and jet2

```
/eos/cms/store/cmst3/group/exovv/VVtuple/FullRun2VVVHNtuple/deepAK8V2/
```
Before running, initialiaze the basedir variable in makeInputs.py to your simboliklinkname

Make the 3D templates. Several options can be specified to produce QCD, V+Jets or signal templates, normalization etc.
 
```
 python makeInputs.py -p 2016 --run "signorm" --signal "ZprimeWW" --batch False 
 python makeInputs.py -p 2016 --run "sigmvv" --signal "ZprimeWW" --batch False 
 python makeInputs.py -p 2016 --run "sigmjet" --signal "ZprimeWW" --batch False 
 python makeInputs.py -p 2016 --run "vjets" --batch False                                                                                                                                      
 python makeInputs.py -p 2016 --run "qcdtemplates"
 python makeInputs.py -p 2016 --run "qcdkernel"
 python makeInputs.py -p 2016 --run "qcdnorm"
 python makeInputs.py -p 2016 --run "data"
 # python makeInputs.py -p 2016 --run "pseudo"
```

Run closure test of signal fits:

```
python plotSignalShapesFromJSON.py -f JJ_BulkGravWW_2016_MJl1_VV_HPLP.json -v mJ
python plotSignalShapesFromJSON.py -f JJ_BulkGravWW_2016_MJl2_VV_HPLP.json -v mJ -l "l2"
python plotSignalShapesFromJSON.py -f JJ_BulkGravWW_2016_MVV.json -v mVV
```

After producing the QCD background templetes, to improve the agreement between MC and template, it is necessary to fit the  HPLP MC with HPLP kernel ( with the option -p it is possible to select different projections: x for mjet1, y for mjet2 and z for mjj - use just one option at the time to avoid crashes! - e.g. -p z -x 65,105 -y 65,105 gives mjj projection in the mjet1&2 range 65,105).

The script expects to find the files in a directory called results_year.

```
./run_transferKernel.sh VV_HPLP VV_HPLP
```

The same script can be used to extrapolate the templates from a high statistics category to a low statistics one. In the analysis this is done to extrapolate from
HPLP to HPHP and from ggF/DY to VBF categories as follows:

```
./run_transferKernel.sh VV_HPLP VV_HPHP
./run_transferKernel.sh VV_HPLP VBF_VV_HPLP
```

The first argument is the input pdfs taken from the high statistics category; the second argument is the MC in the low statistics category to be fit.

Create datacard and workspaces: in order to call the 'addParametricYieldHVTBR' function the signal name BulkGVV or VprimeWV should be used

```
python makeCard.py
#text2workspace.py datacard_JJ_HPHP_13TeV.txt -o JJ_BulkGWW_HPHP_13TeV_workspace.root
#python runPostFit.py 
```

Run the limits with combine and make final plot

```
vvSubmitLimits.py workspace_JJ_BulkGVV_VV_13TeV_2016.root -s 100 -q "tomorrow" -m 1200 -M 4200 -C 1
find higgsCombineTest.AsymptoticLimits.* -size +1500c | xargs hadd Limits_BulkGVV_13TeV_2016.root
vvMakeLimitPlot.py Limits_BulkGVV_13TeV_2016.root -x 1200 -X 4200 -s BulkGVV  --hvt 2 --HVTworkspace workspace_JJ_BulkGVV_VV_13TeV_2016.root -p 2016 #(expected limits)
vvMakeLimitPlot.py Limits_BulkGWW_HPHP_13TeV.root -x 1200 -X 4200 -b 0 #(expected+observed limits)
```
Run post fit control plots

```
python runFitPlots_vjets_signal_oneyear_splitRes.py -n results_2016/workspace_JJ_BulkGVV_VV_13TeV_2016.root  -l sigonly -i results_2016/JJ_2016_nonRes_VV_HPLP.root -M 2000 -s
```

Get pulls of systematics for 1 mass points and produce a nice plot:

```
combine -M FitDiagnostics -m 1200 workspace.root
root -l PlotPulls.C
```

Further instructions on how to run the code can be found at:
https://docs.google.com/document/d/1hU84u27mY85UaAK5R11OHYctBMckDU6kX7IcorboZf8/edit?usp=sharing

