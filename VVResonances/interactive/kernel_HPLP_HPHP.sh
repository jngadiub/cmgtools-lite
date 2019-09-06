#!bin/bash

name=2016_tau21DDT_rho_VV_OPT31and1_OPTXY1_OPTZ1_ownTemplates
postfitdir=postfit_qcd/${name}/
mkdir $postfitdir

#               pythia
#HPLP
python transferKernel.py -i results_2016/JJ_2016_nonRes_VV_HPLP.root --sample pythia --year 2016 -p x --pdfIn results_2016/JJ_2016_nonRes_3D_VV_HPLP.root | tee KernelTransf_2016_VV_HPLP_pythia_x_${name}.out
#python transferKernel.py -i results_2016/JJ_2016_nonRes_VV_HPLP.root --sample pythia --year 2016 -p x -z 1126,1600 --pdfIn results_2016/JJ_2016_nonRes_3D_VV_HPLP.root | tee KernelTransf_2016_VV_HPLP_pythia_x_${name}.out
#python transferKernel.py -i results_2016/JJ_2016_nonRes_VV_HPLP.root --sample pythia --year 2016 -p x -z 1600,2700 --pdfIn results_2016/JJ_2016_nonRes_3D_VV_HPLP.root | tee KernelTransf_2016_VV_HPLP_pythia_x_${name}.out
#python transferKernel.py -i results_2016/JJ_2016_nonRes_VV_HPLP.root --sample pythia --year 2016 -p x -z 2700,5500 --pdfIn results_2016/JJ_2016_nonRes_3D_VV_HPLP.root | tee KernelTransf_2016_VV_HPLP_pythia_x_${name}.out

python transferKernel.py -i results_2016/JJ_2016_nonRes_VV_HPLP.root --sample pythia --year 2016 -p y --pdfIn results_2016/JJ_2016_nonRes_3D_VV_HPLP.root | tee KernelTransf_2016_VV_HPLP_pythia_y_${name}.out
#python transferKernel.py -i results_2016/JJ_2016_nonRes_VV_HPLP.root --sample pythia --year 2016 -p y -z 1126,1600 --pdfIn results_2016/JJ_2016_nonRes_3D_VV_HPLP.root | tee KernelTransf_2016_VV_HPLP_pythia_y_${name}.out
#python transferKernel.py -i results_2016/JJ_2016_nonRes_VV_HPLP.root --sample pythia --year 2016 -p y -z 1600,2700 --pdfIn results_2016/JJ_2016_nonRes_3D_VV_HPLP.root | tee KernelTransf_2016_VV_HPLP_pythia_y_${name}.out
#python transferKernel.py -i results_2016/JJ_2016_nonRes_VV_HPLP.root --sample pythia --year 2016 -p y -z 2700,5500 --pdfIn results_2016/JJ_2016_nonRes_3D_VV_HPLP.root | tee KernelTransf_2016_VV_HPLP_pythia_y_${name}.out

python transferKernel.py -i results_2016/JJ_2016_nonRes_VV_HPLP.root --sample pythia --year 2016 -p z --pdfIn results_2016/JJ_2016_nonRes_3D_VV_HPLP.root | tee KernelTransf_2016_VV_HPLP_pythia_z_${name}.out
#python transferKernel.py -i results_2016/JJ_2016_nonRes_VV_HPLP.root --sample pythia --year 2016 -p z -x 55,75 -y 55,75 --pdfIn results_2016/JJ_2016_nonRes_3D_VV_HPLP.root | tee KernelTransf_2016_VV_HPLP_pythia_z_${name}.out
#python transferKernel.py -i results_2016/JJ_2016_nonRes_VV_HPLP.root --sample pythia --year 2016 -p z -x 75,105 -y 75,105 --pdfIn results_2016/JJ_2016_nonRes_3D_VV_HPLP.root | tee KernelTransf_2016_VV_HPLP_pythia_z_${name}.out
#python transferKernel.py -i results_2016/JJ_2016_nonRes_VV_HPLP.root --sample pythia --year 2016 -p z -x 105,169 -y 105,169 --pdfIn results_2016/JJ_2016_nonRes_3D_VV_HPLP.root | tee KernelTransf_2016_VV_HPLP_pythia_z_${name}.out
#python transferKernel.py -i results_2016/JJ_2016_nonRes_VV_HPLP.root --sample pythia --year 2016 -p z -x 169,215 -y 169,215 --pdfIn results_2016/JJ_2016_nonRes_3D_VV_HPLP.root | tee KernelTransf_2016_VV_HPLP_pythia_z_${name}.out
#                madgraph
#HPLP
python transferKernel.py -i results_2016/JJ_2016_nonRes_VV_HPLP.root --sample madgraph --year 2016 -p x --pdfIn results_2016/JJ_2016_nonRes_3D_VV_HPLP.root | tee KernelTransf_2016_VV_HPLP_madgraph_x_${name}.out                                                                   
#python transferKernel.py -i results_2016/JJ_2016_nonRes_VV_HPLP.root --sample madgraph --year 2016 -p x -z 1126,1600 --pdfIn results_2016/JJ_2016_nonRes_3D_VV_HPLP.root | tee KernelTransf_2016_VV_HPLP_madgraph_x_${name}.out
#python transferKernel.py -i results_2016/JJ_2016_nonRes_VV_HPLP.root --sample madgraph --year 2016 -p x -z 1600,2700 --pdfIn results_2016/JJ_2016_nonRes_3D_VV_HPLP.root | tee KernelTransf_2016_VV_HPLP_madgraph_x_${name}.out
#python transferKernel.py -i results_2016/JJ_2016_nonRes_VV_HPLP.root --sample madgraph --year 2016 -p x -z 2700,5500 --pdfIn results_2016/JJ_2016_nonRes_3D_VV_HPLP.root | tee KernelTransf_2016_VV_HPLP_madgraph_x_${name}.out

python transferKernel.py -i results_2016/JJ_2016_nonRes_VV_HPLP.root --sample madgraph --year 2016 -p y --pdfIn results_2016/JJ_2016_nonRes_3D_VV_HPLP.root | tee KernelTransf_2016_VV_HPLP_madgraph_y_${name}.out
#python transferKernel.py -i results_2016/JJ_2016_nonRes_VV_HPLP.root --sample madgraph --year 2016 -p y -z 1126,1600 --pdfIn results_2016/JJ_2016_nonRes_3D_VV_HPLP.root | tee KernelTransf_2016_VV_HPLP_madgraph_y_${name}.out
#python transferKernel.py -i results_2016/JJ_2016_nonRes_VV_HPLP.root --sample madgraph --year 2016 -p y -z 1600,2700 --pdfIn results_2016/JJ_2016_nonRes_3D_VV_HPLP.root | tee KernelTransf_2016_VV_HPLP_madgraph_y_${name}.out
#python transferKernel.py -i results_2016/JJ_2016_nonRes_VV_HPLP.root --sample madgraph --year 2016 -p y -z 2700,5500 --pdfIn results_2016/JJ_2016_nonRes_3D_VV_HPLP.root | tee KernelTransf_2016_VV_HPLP_madgraph_y_${name}.out

python transferKernel.py -i results_2016/JJ_2016_nonRes_VV_HPLP.root --sample madgraph --year 2016 -p z --pdfIn results_2016/JJ_2016_nonRes_3D_VV_HPLP.root | tee KernelTransf_2016_VV_HPLP_madgraph_z_${name}.out
#python transferKernel.py -i results_2016/JJ_2016_nonRes_VV_HPLP.root --sample madgraph --year 2016 -p z -x 55,75 -y 55,75 --pdfIn results_2016/JJ_2016_nonRes_3D_VV_HPLP.root | tee KernelTransf_2016_VV_HPLP_madgraph_z_${name}.out
#python transferKernel.py -i results_2016/JJ_2016_nonRes_VV_HPLP.root --sample madgraph --year 2016 -p z -x 75,105 -y 75,105 --pdfIn results_2016/JJ_2016_nonRes_3D_VV_HPLP.root | tee KernelTransf_2016_VV_HPLP_madgraph_z_${name}.out
#python transferKernel.py -i results_2016/JJ_2016_nonRes_VV_HPLP.root --sample madgraph --year 2016 -p z -x 105,169 -y 105,169 --pdfIn results_2016/JJ_2016_nonRes_3D_VV_HPLP.root | tee KernelTransf_2016_VV_HPLP_madgraph_z_${name}.out
#python transferKernel.py -i results_2016/JJ_2016_nonRes_VV_HPLP.root --sample madgraph --year 2016 -p z -x 169,215 -y 169,215 --pdfIn results_2016/JJ_2016_nonRes_3D_VV_HPLP.root | tee KernelTransf_2016_VV_HPLP_madgraph_z_${name}.out

#         herwig
#HPLP
python transferKernel.py -i results_2016/JJ_2016_nonRes_VV_HPLP.root --sample herwig --year 2016 -p x --pdfIn results_2016/JJ_2016_nonRes_3D_VV_HPLP.root | tee KernelTransf_2016_VV_HPLP_herwig_x_${name}.out
#python transferKernel.py -i results_2016/JJ_2016_nonRes_VV_HPLP.root --sample herwig --year 2016 -p x -z 1126,1600 --pdfIn results_2016/JJ_2016_nonRes_3D_VV_HPLP.root | tee KernelTransf_2016_VV_HPLP_herwig_x_${name}.out
#python transferKernel.py -i results_2016/JJ_2016_nonRes_VV_HPLP.root --sample herwig --year 2016 -p x -z 1600,2700 --pdfIn results_2016/JJ_2016_nonRes_3D_VV_HPLP.root | tee KernelTransf_2016_VV_HPLP_herwig_x_${name}.out
#python transferKernel.py -i results_2016/JJ_2016_nonRes_VV_HPLP.root --sample herwig --year 2016 -p x -z 2700,5500 --pdfIn results_2016/JJ_2016_nonRes_3D_VV_HPLP.root | tee KernelTransf_2016_VV_HPLP_herwig_x_${name}.out

python transferKernel.py -i results_2016/JJ_2016_nonRes_VV_HPLP.root --sample herwig --year 2016 -p y --pdfIn results_2016/JJ_2016_nonRes_3D_VV_HPLP.root | tee KernelTransf_2016_VV_HPLP_herwig_y_${name}.out
#python transferKernel.py -i results_2016/JJ_2016_nonRes_VV_HPLP.root --sample herwig --year 2016 -p y -z 1126,1600 --pdfIn results_2016/JJ_2016_nonRes_3D_VV_HPLP.root | tee KernelTransf_2016_VV_HPLP_herwig_y_${name}.out
#python transferKernel.py -i results_2016/JJ_2016_nonRes_VV_HPLP.root --sample herwig --year 2016 -p y -z 1600,2700 --pdfIn results_2016/JJ_2016_nonRes_3D_VV_HPLP.root | tee KernelTransf_2016_VV_HPLP_herwig_y_${name}.out
#python transferKernel.py -i results_2016/JJ_2016_nonRes_VV_HPLP.root --sample herwig --year 2016 -p y -z 2700,5500 --pdfIn results_2016/JJ_2016_nonRes_3D_VV_HPLP.root | tee KernelTransf_2016_VV_HPLP_herwig_y_${name}.out

python transferKernel.py -i results_2016/JJ_2016_nonRes_VV_HPLP.root --sample herwig --year 2016 -p z --pdfIn results_2016/JJ_2016_nonRes_3D_VV_HPLP.root | tee KernelTransf_2016_VV_HPLP_herwig_z_${name}.out
#python transferKernel.py -i results_2016/JJ_2016_nonRes_VV_HPLP.root --sample herwig --year 2016 -p z -x 55,75 -y 55,75 --pdfIn results_2016/JJ_2016_nonRes_3D_VV_HPLP.root | tee KernelTransf_2016_VV_HPLP_herwig_z_${name}.out
#python transferKernel.py -i results_2016/JJ_2016_nonRes_VV_HPLP.root --sample herwig --year 2016 -p z -x 75,105 -y 75,105 --pdfIn results_2016/JJ_2016_nonRes_3D_VV_HPLP.root | tee KernelTransf_2016_VV_HPLP_herwig_z_${name}.out
#python transferKernel.py -i results_2016/JJ_2016_nonRes_VV_HPLP.root --sample herwig --year 2016 -p z -x 105,169 -y 105,169 --pdfIn results_2016/JJ_2016_nonRes_3D_VV_HPLP.root | tee KernelTransf_2016_VV_HPLP_herwig_z_${name}.out
#python transferKernel.py -i results_2016/JJ_2016_nonRes_VV_HPLP.root --sample herwig --year 2016 -p z -x 169,215 -y 169,215 --pdfIn results_2016/JJ_2016_nonRes_3D_VV_HPLP.root | tee KernelTransf_2016_VV_HPLP_herwig_z_${name}.out

#        merge 
python transferKernel.py -i results_2016/JJ_2016_nonRes_VV_HPLP.root --sample pythia --year 2016 -p z --pdfIn results_2016/JJ_2016_nonRes_3D_VV_HPLP.root --merge



# pythia
#HPHP
python transferKernel.py -i results_2016/JJ_2016_nonRes_VV_HPHP.root --sample pythia --year 2016 -p x --pdfIn save_new_shapes_2016_pythia_VV_HPLP_3D.root | tee KernelTransf_2016_VV_HPHP_pythia_x_${name}.out
#python transferKernel.py -i results_2016/JJ_2016_nonRes_VV_HPHP.root --sample pythia --year 2016 -p x -z 1126,1600 --pdfIn save_new_shapes_2016_pythia_VV_HPLP_3D.root | tee KernelTransf_2016_VV_HPHP_pythia_x_${name}.out
#python transferKernel.py -i results_2016/JJ_2016_nonRes_VV_HPHP.root --sample pythia --year 2016 -p x -z 1600,2700 --pdfIn save_new_shapes_2016_pythia_VV_HPLP_3D.root | tee KernelTransf_2016_VV_HPHP_pythia_x_${name}.out
#python transferKernel.py -i results_2016/JJ_2016_nonRes_VV_HPHP.root --sample pythia --year 2016 -p x -z 2700,5500 --pdfIn save_new_shapes_2016_pythia_VV_HPLP_3D.root | tee KernelTransf_2016_VV_HPHP_pythia_x_${name}.out

python transferKernel.py -i results_2016/JJ_2016_nonRes_VV_HPHP.root --sample pythia --year 2016 -p y --pdfIn save_new_shapes_2016_pythia_VV_HPLP_3D.root | tee KernelTransf_2016_VV_HPHP_pythia_y_${name}.out
#python transferKernel.py -i results_2016/JJ_2016_nonRes_VV_HPHP.root --sample pythia --year 2016 -p y -z 1126,1600 --pdfIn save_new_shapes_2016_pythia_VV_HPLP_3D.root | tee KernelTransf_2016_VV_HPHP_pythia_y_${name}.out
#python transferKernel.py -i results_2016/JJ_2016_nonRes_VV_HPHP.root --sample pythia --year 2016 -p y -z 1600,2700 --pdfIn save_new_shapes_2016_pythia_VV_HPLP_3D.root | tee KernelTransf_2016_VV_HPHP_pythia_y_${name}.out
#python transferKernel.py -i results_2016/JJ_2016_nonRes_VV_HPHP.root --sample pythia --year 2016 -p y -z 2700,5500 --pdfIn save_new_shapes_2016_pythia_VV_HPLP_3D.root | tee KernelTransf_2016_VV_HPHP_pythia_y_${name}.out

python transferKernel.py -i results_2016/JJ_2016_nonRes_VV_HPHP.root --sample pythia --year 2016 -p z --pdfIn save_new_shapes_2016_pythia_VV_HPLP_3D.root | tee KernelTransf_2016_VV_HPHP_pythia_z_${name}.out
#python transferKernel.py -i results_2016/JJ_2016_nonRes_VV_HPHP.root --sample pythia --year 2016 -p z -x 55,75 -y 55,75 --pdfIn save_new_shapes_2016_pythia_VV_HPLP_3D.root | tee KernelTransf_2016_VV_HPHP_pythia_z_${name}.out
#python transferKernel.py -i results_2016/JJ_2016_nonRes_VV_HPHP.root --sample pythia --year 2016 -p z -x 75,105 -y 75,105 --pdfIn save_new_shapes_2016_pythia_VV_HPLP_3D.root | tee KernelTransf_2016_VV_HPHP_pythia_z_${name}.out
#python transferKernel.py -i results_2016/JJ_2016_nonRes_VV_HPHP.root --sample pythia --year 2016 -p z -x 105,169 -y 105,169 --pdfIn save_new_shapes_2016_pythia_VV_HPLP_3D.root | tee KernelTransf_2016_VV_HPHP_pythia_z_${name}.out
#python transferKernel.py -i results_2016/JJ_2016_nonRes_VV_HPHP.root --sample pythia --year 2016 -p z -x 169,215 -y 169,215 --pdfIn save_new_shapes_2016_pythia_VV_HPLP_3D.root | tee KernelTransf_2016_VV_HPHP_pythia_z_${name}.out



#                madgraph
#HPHP
python transferKernel.py -i results_2016/JJ_2016_nonRes_VV_HPHP.root --sample madgraph --year 2016 -p x --pdfIn save_new_shapes_2016_madgraph_VV_HPLP_3D.root   | tee KernelTransf_2016_VV_HPHP_madgraph_x_${name}.out                                                                   #python transferKernel.py -i results_2016/JJ_2016_nonRes_VV_HPHP.root --sample madgraph --year 2016 -p x -z 1126,1600 --pdfIn save_new_shapes_2016_madgraph_VV_HPLP_3D.root   | tee KernelTransf_2016_VV_HPHP_madgraph_x_${name}.out
#python transferKernel.py -i results_2016/JJ_2016_nonRes_VV_HPHP.root --sample madgraph --year 2016 -p x -z 1600,2700 --pdfIn save_new_shapes_2016_madgraph_VV_HPLP_3D.root   | tee KernelTransf_2016_VV_HPHP_madgraph_x_${name}.out
#python transferKernel.py -i results_2016/JJ_2016_nonRes_VV_HPHP.root --sample madgraph --year 2016 -p x -z 2700,5500 --pdfIn save_new_shapes_2016_madgraph_VV_HPLP_3D.root   | tee KernelTransf_2016_VV_HPHP_madgraph_x_${name}.out

python transferKernel.py -i results_2016/JJ_2016_nonRes_VV_HPHP.root --sample madgraph --year 2016 -p y --pdfIn save_new_shapes_2016_madgraph_VV_HPLP_3D.root   | tee KernelTransf_2016_VV_HPHP_madgraph_y_${name}.out
#python transferKernel.py -i results_2016/JJ_2016_nonRes_VV_HPHP.root --sample madgraph --year 2016 -p y -z 1126,1600 --pdfIn save_new_shapes_2016_madgraph_VV_HPLP_3D.root   | tee KernelTransf_2016_VV_HPHP_madgraph_y_${name}.out
#python transferKernel.py -i results_2016/JJ_2016_nonRes_VV_HPHP.root --sample madgraph --year 2016 -p y -z 1600,2700 --pdfIn save_new_shapes_2016_madgraph_VV_HPLP_3D.root   | tee KernelTransf_2016_VV_HPHP_madgraph_y_${name}.out
#python transferKernel.py -i results_2016/JJ_2016_nonRes_VV_HPHP.root --sample madgraph --year 2016 -p y -z 2700,5500 --pdfIn save_new_shapes_2016_madgraph_VV_HPLP_3D.root   | tee KernelTransf_2016_VV_HPHP_madgraph_y_${name}.out

python transferKernel.py -i results_2016/JJ_2016_nonRes_VV_HPHP.root --sample madgraph --year 2016 -p z --pdfIn save_new_shapes_2016_madgraph_VV_HPLP_3D.root   | tee KernelTransf_2016_VV_HPHP_madgraph_z_${name}.out
#python transferKernel.py -i results_2016/JJ_2016_nonRes_VV_HPHP.root --sample madgraph --year 2016 -p z -x 55,75 -y 55,75 --pdfIn save_new_shapes_2016_madgraph_VV_HPLP_3D.root   | tee KernelTransf_2016_VV_HPHP_madgraph_z_${name}.out
#python transferKernel.py -i results_2016/JJ_2016_nonRes_VV_HPHP.root --sample madgraph --year 2016 -p z -x 75,105 -y 75,105 --pdfIn save_new_shapes_2016_madgraph_VV_HPLP_3D.root   | tee KernelTransf_2016_VV_HPHP_madgraph_z_${name}.out
#python transferKernel.py -i results_2016/JJ_2016_nonRes_VV_HPHP.root --sample madgraph --year 2016 -p z -x 105,169 -y 105,169 --pdfIn save_new_shapes_2016_madgraph_VV_HPLP_3D.root   | tee KernelTransf_2016_VV_HPHP_madgraph_z_${name}.out
#python transferKernel.py -i results_2016/JJ_2016_nonRes_VV_HPHP.root --sample madgraph --year 2016 -p z -x 169,215 -y 169,215 --pdfIn save_new_shapes_2016_madgraph_VV_HPLP_3D.root   | tee KernelTransf_2016_VV_HPHP_madgraph_z_${name}.out
 


#herwig
#HPHP
python transferKernel.py -i results_2016/JJ_2016_nonRes_VV_HPHP.root --sample herwig --year 2016 -p x --pdfIn save_new_shapes_2016_herwig_VV_HPLP_3D.root   | tee KernelTransf_2016_VV_HPHP_herwig_x_${name}.out                                                         
#python transferKernel.py -i results_2016/JJ_2016_nonRes_VV_HPHP.root --sample herwig --year 2016 -p x -z 1126,1600 --pdfIn save_new_shapes_2016_herwig_VV_HPLP_3D.root   | tee KernelTransf_2016_VV_HPHP_herwig_x_${name}.out
#python transferKernel.py -i results_2016/JJ_2016_nonRes_VV_HPHP.root --sample herwig --year 2016 -p x -z 1600,2700 --pdfIn save_new_shapes_2016_herwig_VV_HPLP_3D.root   | tee KernelTransf_2016_VV_HPHP_herwig_x_${name}.out
#python transferKernel.py -i results_2016/JJ_2016_nonRes_VV_HPHP.root --sample herwig --year 2016 -p x -z 2700,5500 --pdfIn save_new_shapes_2016_herwig_VV_HPLP_3D.root   | tee KernelTransf_2016_VV_HPHP_herwig_x_${name}.out

python transferKernel.py -i results_2016/JJ_2016_nonRes_VV_HPHP.root --sample herwig --year 2016 -p y --pdfIn save_new_shapes_2016_herwig_VV_HPLP_3D.root   | tee KernelTransf_2016_VV_HPHP_herwig_y_${name}.out
#python transferKernel.py -i results_2016/JJ_2016_nonRes_VV_HPHP.root --sample herwig --year 2016 -p y -z 1126,1600 --pdfIn save_new_shapes_2016_herwig_VV_HPLP_3D.root   | tee KernelTransf_2016_VV_HPHP_herwig_y_${name}.out
#python transferKernel.py -i results_2016/JJ_2016_nonRes_VV_HPHP.root --sample herwig --year 2016 -p y -z 1600,2700 --pdfIn save_new_shapes_2016_herwig_VV_HPLP_3D.root   | tee KernelTransf_2016_VV_HPHP_herwig_y_${name}.out
#python transferKernel.py -i results_2016/JJ_2016_nonRes_VV_HPHP.root --sample herwig --year 2016 -p y -z 2700,5500 --pdfIn save_new_shapes_2016_herwig_VV_HPLP_3D.root   | tee KernelTransf_2016_VV_HPHP_herwig_y_${name}.out

python transferKernel.py -i results_2016/JJ_2016_nonRes_VV_HPHP.root --sample herwig --year 2016 -p z --pdfIn save_new_shapes_2016_herwig_VV_HPLP_3D.root   | tee KernelTransf_2016_VV_HPHP_herwig_z_${name}.out
#python transferKernel.py -i results_2016/JJ_2016_nonRes_VV_HPHP.root --sample herwig --year 2016 -p z -x 55,75 -y 55,75 --pdfIn save_new_shapes_2016_herwig_VV_HPLP_3D.root   | tee KernelTransf_2016_VV_HPHP_herwig_z_${name}.out
#python transferKernel.py -i results_2016/JJ_2016_nonRes_VV_HPHP.root --sample herwig --year 2016 -p z -x 75,105 -y 75,105 --pdfIn save_new_shapes_2016_herwig_VV_HPLP_3D.root   | tee KernelTransf_2016_VV_HPHP_herwig_z_${name}.out
#python transferKernel.py -i results_2016/JJ_2016_nonRes_VV_HPHP.root --sample herwig --year 2016 -p z -x 105,169 -y 105,169 --pdfIn save_new_shapes_2016_herwig_VV_HPLP_3D.root   | tee KernelTransf_2016_VV_HPHP_herwig_z_${name}.out
#python transferKernel.py -i results_2016/JJ_2016_nonRes_VV_HPHP.root --sample herwig --year 2016 -p z -x 169,215 -y 169,215 --pdfIn save_new_shapes_2016_herwig_VV_HPLP_3D.root   | tee KernelTransf_2016_VV_HPHP_herwig_z_${name}.out 


#merge HPHP
python transferKernel.py -i results_2016/JJ_2016_nonRes_VV_HPHP.root --sample pythia --year 2016 -p z --pdfIn results_2016/JJ_2016_nonRes_3D_VV_HPLP.root --merge

mv postfit_qcd/PostFit_*.* $postfitdir



#     control plots
#HPLP
python Projections3DHisto.py --mc results_2016/JJ_2016_nonRes_VV_HPLP.root,nonRes -k save_new_shapes_2016_pythia_VV_HPLP_3D.root,histo -o control-plots-QCD_pythia_signals_HPLP_${name}/       
python Projections3DHisto.py --mc results_2016/JJ_2016_nonRes_VV_HPLP_altshapeUp.root,nonRes -k save_new_shapes_2016_pythia_VV_HPLP_3D.root,histo -o control-plots-QCD_herwig_signals_HPLP_${name}/
python Projections3DHisto.py --mc results_2016/JJ_2016_nonRes_VV_HPLP_altshape2.root,nonRes -k save_new_shapes_2016_pythia_VV_HPLP_3D.root,histo -o control-plots-QCD_madgraph_signals_HPLP_${name}/

#HPHP
python Projections3DHisto_HPHP.py --mc results_2016/JJ_2016_nonRes_VV_HPHP.root,nonRes -k save_new_shapes_2016_pythia_VV_HPHP_3D.root,histo -o control-plots-QCD_pythia_signals_HPHP_${name}/
python Projections3DHisto_HPHP.py --mc results_2016/JJ_2016_nonRes_VV_HPHP_altshapeUp.root,nonRes -k save_new_shapes_2016_pythia_VV_HPHP_3D.root,histo -o control-plots-QCD_herwigh_signals_HPHP_${name}
python Projections3DHisto_HPHP.py --mc results_2016/JJ_2016_nonRes_VV_HPHP_altshape2.root,nonRes -k save_new_shapes_2016_pythia_VV_HPHP_3D.root,histo -o control-plots-QCD_madgraph_signals_HPHP_${name}/

