#!bin/bash


script=makeInputs.py
signals=( "BGWW")
#signals=("ZprimeZH" "WprimeWH" "ZprimeWW" "BGWW" "BGZZ"  "WprimeWZ")
#periods=("2016" "2017" "2018" ) #"2016,2017,2018")
periods=("2016,2017,2018")
commands=("sigmj" "sigmvv") # "signorm")
'''
sed -i '/categories=/c\categories=["NP"]' ${script}
for signal in ${signals[*]}; do
    echo $signal
    for period in ${periods[*]}; do
        echo ${period}
	for cmd in ${commands[*]}; do
	    echo $cmd
	    python ${script} -p ${period} --run ${cmd} --signal ${signal} --batch False  | tee make_${cmd}_${signal}_2016.log
	done
    done
done
'''
commands=("signorm")
sed -i '/categories=/c\categories=["VV_HPLP"]' ${script}
#sed -i '/categories=/c\categories=["VH_HPHP","VH_HPLP","VH_LPHP","VV_HPHP","VV_HPLP"]' ${script}
for signal in ${signals[*]}; do
    echo $signal
    for cmd in ${commands[*]}; do
	for period in ${periods[*]}; do
	    echo ${period}
            echo $cmd
            python ${script} -p ${period} --run ${cmd} --signal ${signal} --batch False | tee make_${cmd}_${signal}_2016.log
	done
    done
done
'''
signals=("ZprimeToZh" "ZprimeToWW" "WprimeToWh" "BulkGravToWW" "BulkGravToZZ")
script=categorisation.py
inputdir="2016trainingV2/"
for signal in ${signals[*]}; do                                                                                                                                                                                                              
    echo $signal                                                                                                                                                                                                                             
    python ${script} -y 2016  -s ${signal} -d ${inputdir} | tee make_cat_${signal}_2016.log
done

rm tmp.root
'''
