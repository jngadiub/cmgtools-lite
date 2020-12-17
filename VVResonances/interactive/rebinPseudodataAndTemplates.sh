#!bin/bash

basedir=results_Run2/
categories=("VV_HPHP" "VV_HPLP" "VH_HPHP" "VH_LPHP" "VH_HPLP")

#dir20=${basedir}pseudo20/
#echo $dir20
#mkdir $dir20
dir40=${basedir}pseudo40/
mkdir $dir40
#dir10=${basedir}pseudo10/
#mkdir $dir10

for cat in ${categories[*]}; do
    echo $cat
    #echo $dir20
    #python rebinPseudodataAndTemplates.py -c $cat -i ${basedir}pseudo80/ -o $dir20 -b 4  -p "Run2" --wtd "pseudonormshapes"
    echo $dir40
    python rebinPseudodataAndTemplates.py -c $cat -i ${basedir}pseudo80/ -o $dir40 -b 2 -p "Run2" --wtd "shapespseudonormdata" #tt
    #   echo $dir10
#    python rebinPseudodata.py -c $cat -i ${basedir}pseudo80/ -o $dir10 -b 8


done


