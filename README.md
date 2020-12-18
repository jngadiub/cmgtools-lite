# VV statistical analysis in 10X

Further information on each part of the 3D fit code can be found at:
https://docs.google.com/document/d/1hU84u27mY85UaAK5R11OHYctBMckDU6kX7IcorboZf8/edit?usp=sharing

### Setup ###

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
Before running, initialiaze the `basedir` variable in `makeInputs.py` to your `simboliklinkname`

### Make inclusive control plots with data ###

Control plots to check data versus MC agreement with just preselections applied can be made for several variables with the script `make-control-plots-submit.py` where the list of
observables can be found and/or modified.

To plot one variable (ex: the jet 1 mass) for one year (ex: 2016) run:

```
python make-control-plots.py -y 2016 -v jj_l1_softDrop_mass

```

A folder called `control-plots-2016` will contain the plot in several formats. This takes about 1 hour to run (all year data and MC including all QCD samples flavour). If it
was done once and you just want to change in the script the plotting style or legends you can use the option `-H` and it will load the histograms from saved root files.

To plot all variables listed in the script for one year (ex: 2016) it is better to parallelize sending one condor job per each observable as:

```
python make-control-plots.py -y 2016 -s

```

By default, the non-VBF preselections and plots are run. To make plots with the VBF selections to also obtain control plots of VBF jets observables in addition, you have to add option `--vbf`.

When running over multiple years simultaneously the year label is added to the output folders. If additional labels are needed (for instance when running simultaneously VBF
and non VBF for the same year) an additional label can be added with `-l`.

# Make inputs to 3D fit #

The `makeInputs.py` script allows to create all the simulation templates, normalizations and data inputs. To run on a single year use `-p "year"`, to run on more years separate them with a coma. Except for signals, when running on Run2, use the batch submission and the option `--sendjobs False` to merge the batch jobs. In the script it is possible to select on which analysis category to run. 

## 1. Make the normalizations ##
 * QCD (in batch it will automatically produce pythia, madgraph and herwig)
 
 `python makeInputs.py -p 2016 --run "qcdnorm"`
 
  * V+jets: 
  
   make SF (need a directory called `migrationunc`, it is long and not set up for batch): 
   
   `python makeInputs.py -p 2016 --run "vjetsSF"`
  
   make normalization: `python makeInputs.py -p 2016 --run "vjetsnorm"`
  
   make migration uncertainty file: `python makeInputs.py -p 2016 --run "vjetsMU"`
  
  * ttbar: 
  
   make SF (need a directory called `migrationunc`, it is long and not set up for batch): `python makeInputs.py -p 2016 --run "ttSF"`
  
   make normalization: `python makeInputs.py -p 2016 --run "ttnorm"`
  
   make migration uncertainty file: `python makeInputs.py -p 2016 --run "ttMU"`

  * signals ("ZprimeZH" "WprimeWH" "ZprimeWW" "BGWW" "BGZZ"  "WprimeWZ" + the same for VBF ):

   make SF (need a directory called `migrationunc`, it is long and not set up for batch): `python makeInputs.py -p 2016 --run "sigSF" --signal "BGWW"`
  
   make normalization: `python makeInputs.py -p 2016 --run "signorm" --signal "BGWW"`
  
   make migration uncertainty file: `python makeInputs.py -p 2016 --run "sigMU" --signal "BGWW"`
  
  * data:
  `python makeInputs.py -p 2016 --run "data"` 


## 2. Make the 3D templates. ##
 * QCD (tipically for NP category, in batch it will automatically produce pythia, madgraph and herwig):
 ```
 python makeInputs.py -p 2016 --run "qcdtemplates"
 ```
 when all jobs are over:
 ```
 python makeInputs.py -p 2016 --run "qcdkernel"
 ```
 Once also QCD normalizations files a produced, a further step should be carried out to improve the agreement between MC and templates. The MC (normalization) for a certain category can be fit with the `NP` high statistics kernels (or a different category)( with the option -p it is possible to select different projections: x for mjet1, y for mjet2 and z for mjj - use just one option at the time to avoid crashes! - e.g. -p z -x 65,105 -y 65,105 gives mjj projection in the mjet1&2 range 65,105).

The script expects to find the files in a directory called results_year. The first argument is the input pdfs taken from the high statistics category; the second argument is the MC in the low statistics category to be fit.

```
./run_transferKernel.sh NP VV_HPLP year year 
./run_transferKernel.sh NP VV_HPLP Run2 "2016,2017,2018"
```

* V+jets:
 
 jet mass shapes: `python makeInputs.py -p 2016 --run "vjetsfits" --batch False`
 
 dijet mass templates:  `python makeInputs.py -p "2016,2017,2018"  --run "vjetskernel"`
 
 * ttbar
 
 jet mass shapes: `python makeInputs.py -p 2016 --run "ttfits" --batch False`
 
 dijet mass templates: `python makeInputs.py -p "2016,2017,2018"  --run "tttemplates"`
 
 * signals ("ZprimeZH" "WprimeWH" "ZprimeWW" "BGWW" "BGZZ"  "WprimeWZ" + the same for VBF )
 
 jet mass shapes: `python makeInputs.py -p 2016 --run "sigmjet" --signal "BGWW" --batch False` 
 
 dijet mass templates: `python makeInputs.py -p 2016 --run "sigmvv" --signal "BGWW" --batch False`
 

## 3. Closure tests, datacards and workspaces ###

**NB: usually all script excpet the inputs to be in a `results_period` directory**
* A special treatment is need to obtain the correct ttbar normalization that will be given as input to the postifits and limits with all workspaces

Produce pseudodata with ttbar only, make a workspace and run postfits-> this will produce a json file with the ttbar normalizations. The postfit should be run on one category at the time.
```
python makeInputs.py -p 2016 --run "pseudoTT" 
python makeCard.py -p "2016,2017,2018" --signal "BulkGWW" -c "VH_HPLP" --outlabel "_ttbar" --pseudodata "ttbar"
source makeTTbarFits.sh VH_HPLP # python runFitPlots_vjets_signal_bigcombo_splitRes.py -n results_${period}/workspace_JJ_BulkGWW_${c}_13TeV_${period}_ttbar.root  -i  results_${period}/JJ_${period}_nonRes_${c}.root -M 2000  -o ${outputdir} --channel ${c} -l ${c} --doVjets --addTop --doFit --pseudo 
```
* produce pseudodata with all backgrounds
```
python makeCard.py -p "2016,2017,2018" --signal "BulkGWW" -c "VH_HPLP,VH_LPHP,VH_HPHP,VV_HPHP,VV_HPLP" --outlabel "_PrepPseudo" --pseudodata "PrepPseudo"
python makeInputs.py -p 2016 --run "pseudoALL"
```
* before preparing workspaces with all categories, to reduce the size of the workspace, some distributions need to be rebinned `source rebinPseudodataAndTemplates.sh`. This script expect the templates, qcd   normalizations and data and pseudodata to be in `results_period/pseudo80/` and will put the output in  `results_period/pseudo40/`. Once files are created, they should be copied in`results_period/` for the next step.

* prepare workspace and run postfits on pseudodata
```
python makeInputs.py -p 2016 --run "pseudoALL"
python makeCard.py -p "2016,2017,2018" --signal "BulkGWW" -c "VH_HPLP,VH_LPHP,VH_HPHP,VV_HPHP,VV_HPLP" --outlabel "_pseudodata" --pseudodata "True"
source makePseudoFits.sh results_Run2 label #label can be any string to identify the outputs #python runFitPlots_vjets_signal_bigcombo_splitRes.py -n ${inputdir}/workspace_JJ_BulkGWW_VVVH_13TeV_${period}_pseudodata.root  -i  ${inputdir}/JJ_${period}_nonRes_${c}.root -M 2000  -o ${outputdir} --channel ${c} -l ${c} --doVjets --addTop --doFit --pseudo
```
* prepare workspace and run postfits on data
```
python makeCard.py -p "2016,2017,2018" --signal "BulkGWW" -c "VH_HPLP,VH_LPHP,VH_HPHP,VV_HPHP,VV_HPLP" --outlabel "_data" --pseudodata "False"
```
If the analysis is still blinded, use the script `makeBlindFits.sh` to run postfits on data blinding part of the jet mass or the command:
`python runFitPlots_vjets_signal_bigcombo_splitRes.py -n ${inputdir}/workspace_JJ_BulkGWW_VVVH_13TeV_${period}_data.root  -i  ${inputdir}/JJ_${period}_nonRes_${c}.root -M 2000  -o ${outputdir} --channel ${c} -l ${c} --doVjets --addTop --doFit --blind -x 55,65,140,215 -y 55,65,140,215`

Add the option `-s` to run S+B fits.

Get pulls of systematics for 1 mass points and produce a nice plot:

```
combine -M FitDiagnostics -m 1200 workspace.root -v 2 --noErrors --minos none
root -l PlotPulls.C
```

* Check signal fits:

```
python plotSignalShapesFromJSON.py -i signalShapesRun2/ -y "Run2" -v mJ
python plotSignalShapesFromJSON.py -i signalShapesRun2/ -y "Run2" -v mVV
```

## 4. Run and plot limits ###

```
vvSubmitLimits.py Run2_MD_WHP10_WLP20/workspace_JJ_BulkGWW_VVVH_13TeV_Run2_pseudodata.root -s 1000 -q "testmatch" -m 3000 -M 6000 -C 1 -o "-M AsymptoticLimits -n BulkGWW_MD_WHP10_WLP20_VVVH_Run2" -n "BulkGWW_MD_WHP10_WLP20_VVVH_Run2_pt2" 
find higgsCombineTest.AsymptoticLimits.* -size +1500c | xargs hadd Limits_BulkGVV_13TeV_2016.root
```
The following script still needs some fixes:
```
vvMakeLimitPlot.py Limits_BulkGVV_13TeV_2016.root -x 1200 -X 4200 -s BulkGVV  --hvt 2 --HVTworkspace workspace_JJ_BulkGVV_VV_13TeV_2016.root -p 2016 #(expected limits)
vvMakeLimitPlot.py Limits_BulkGWW_HPHP_13TeV.root -x 1200 -X 4200 -b 0 #(expected+observed limits)
```







