#!bin/bash
indir=$1
name=$2_OPT3_0and2_OPTXY0and2_OPTZ0and2_PTZ0and2 #OPT31and1_OPTXY2_OPTZ2
postfitdir=postfit_qcd/${name}/
mkdir $postfitdir
categories=('VH_LPHP' 'VH_HPHP' 'VH_HPLP' 'VV_HPLP' 'VV_HPHP')
#categories=('VV_HPHP')
period=$3
fileperiod=$4
for cat in ${categories[*]}; do
    #               pythia
    python transferKernelUnique.py -i ${indir}JJ_${fileperiod}_nonRes_${cat}.root --sample pythia --year ${period} -p x --pdfIn ${indir}JJ_${fileperiod}_nonRes_3D_NP.root | tee KernelTransf_${fileperiod}_${cat}_pythia_x_${name}.out
    #python transferKernel.py -i ${indir}JJ_${fileperiod}_nonRes_${cat}.root --sample pythia --year ${period} -p y --pdfIn ${indir}JJ_${fileperiod}_nonRes_3D_NP.root | tee KernelTransf_${fileperiod}_${cat}_pythia_y_${name}.out
    #python transferKernel.py -i ${indir}JJ_${fileperiod}_nonRes_${cat}.root --sample pythia --year ${period} -p z --pdfIn ${indir}JJ_${fileperiod}_nonRes_3D_NP.root | tee KernelTransf_${fileperiod}_${cat}_pythia_z_${name}.out

    #                madgraph
    python transferKernelUnique.py -i ${indir}JJ_${fileperiod}_nonRes_${cat}.root --sample madgraph --year ${period} -p x --pdfIn ${indir}JJ_${fileperiod}_nonRes_3D_NP.root | tee KernelTransf_${fileperiod}_${cat}_madgraph_x_${name}.out                   
    #python transferKernel.py -i ${indir}JJ_${fileperiod}_nonRes_${cat}.root --sample madgraph --year ${period} -p y --pdfIn ${indir}JJ_${fileperiod}_nonRes_3D_NP.root | tee KernelTransf_${fileperiod}_${cat}_madgraph_y_${name}.out
    #python transferKernel.py -i ${indir}JJ_${fileperiod}_nonRes_${cat}.root --sample madgraph --year ${period} -p z --pdfIn ${indir}JJ_${fileperiod}_nonRes_3D_NP.root | tee KernelTransf_${fileperiod}_${cat}_madgraph_z_${name}.out
    
    #         herwig

    python transferKernelUnique.py -i ${indir}JJ_${fileperiod}_nonRes_${cat}.root --sample herwig --year ${period} -p x --pdfIn ${indir}JJ_${fileperiod}_nonRes_3D_NP.root | tee KernelTransf_${fileperiod}_${cat}_herwig_x_${name}.out
    #python transferKernel.py -i ${indir}JJ_${fileperiod}_nonRes_${cat}.root --sample herwig --year ${period} -p y --pdfIn ${indir}JJ_${fileperiod}_nonRes_3D_NP.root | tee KernelTransf_${fileperiod}_${cat}_herwig_y_${name}.out
    #python transferKernel.py -i ${indir}JJ_${fileperiod}_nonRes_${cat}.root --sample herwig --year ${period} -p z --pdfIn ${indir}JJ_${fileperiod}_nonRes_3D_NP.root | tee KernelTransf_${fileperiod}_${cat}_herwig_z_${name}.out

    #        merge 
    python transferKernelUnique.py -i ${indir}JJ_${fileperiod}_nonRes_${cat}.root --sample pythia --year ${period} -p z --pdfIn ${indir}JJ_${fileperiod}_nonRes_3D_NP.root --merge
    
    mv postfit_qcd/PostFit_*.* $postfitdir

    #     control plots

    #python Projections3DHisto.py --mc ${indir}JJ_${fileperiod}_nonRes_${cat}.root,nonRes -k save_new_shapes_${fileperiod}_pythia_${cat}_3D.root,histo -o control-plots-QCD_pythia_signals_${cat}_${name}/       
    #python Projections3DHisto.py --mc ${indir}JJ_${fileperiod}_nonRes_${cat}_altshapeUp.root,nonRes -k save_new_shapes_${fileperiod}_herwig_${cat}_3D.root,histo -o control-plots-QCD_herwig_signals_${cat}_${name}/
    #python Projections3DHisto.py --mc ${indir}JJ_${fileperiod}_nonRes_${cat}_altshape2.root,nonRes -k save_new_shapes_${fileperiod}_madgraph_${cat}_3D.root,histo -o control-plots-QCD_madgraph_signals_${cat}_${name}/
    python Projections3DHisto_HPHP.py --mc ${indir}JJ_${fileperiod}_nonRes_${cat}.root,nonRes -k save_new_shapes_${fileperiod}_pythia_${cat}_3D.root,histo -o control-plots-QCD_pythia_signals_${cat}_${name}/   -p ${fileperiod}
    python Projections3DHisto_HPHP.py --mc ${indir}JJ_${fileperiod}_nonRes_${cat}_altshapeUp.root,nonRes -k save_new_shapes_${fileperiod}_herwig_${cat}_3D.root,histo -o control-plots-QCD_herwig_signals_${cat}_${name}/ -p ${fileperiod}
    python Projections3DHisto_HPHP.py --mc ${indir}JJ_${fileperiod}_nonRes_${cat}_altshape2.root,nonRes -k save_new_shapes_${fileperiod}_madgraph_${cat}_3D.root,histo -o control-plots-QCD_madgraph_signals_${cat}_${name}/ -p ${fileperiod}
    
done    
