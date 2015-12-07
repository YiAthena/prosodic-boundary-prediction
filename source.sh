#!/bin/sh
#
# Author: Chuang Ding
# Date  : 2015/08/19
# Email : cding@nwpu-aslp.org
# Usage : accent conversion

HOME=/home/zhaoyi/prosody
DIR_DATA=${HOME}/data
DIR_BK=${DIR_DATA}/bk
DIR_RHY=${DIR_DATA}/rhy
DIR_SCRIPTS=${HOME}/scripts
DIR_MODEL=${HOME}/model
DIR_LOG=${HOME}/log
DIR_RESULT=${HOME}/result

# ===== matlab =====
MATLAB='/usr/local/MATLAB/R2013a/bin/matlab -nojvm -nodisplay -nodesktop -nosplash'

# ===== BOM =====
BOM=false

all_rhy=${DIR_RHY}/all_rhy # needed

# ===== PUNC =====
PUNC=false

all_raw=${DIR_RHY}/all_raw
all_xml=${DIR_RHY}/all_xml
all_pos=${DIR_RHY}/all_pos
punc_list=${DIR_RHY}/punc.list

# ===== split =====
SPLIT=false

train_rhy=${DIR_RHY}/train_rhy
test_rhy=${DIR_RHY}/test_rhy
val_rhy=${DIR_RHY}/val_rhy

# ===== pos =====
POS=false

DIR_CRF_DATA=${DIR_DATA}/CRF
train_raw=${DIR_CRF_DATA}/train_raw
test_raw=${DIR_CRF_DATA}/test_raw
val_raw=${DIR_CRF_DATA}/val_raw

ltp_test=/work/dingchuang/research/tts/prosody/subjective/tools/ltp-3.2.0/bin/ltp_test
train_xml=${DIR_CRF_DATA}/train_xml
test_xml=${DIR_CRF_DATA}/test_xml
val_xml=${DIR_CRF_DATA}/val_xml
train_pos=${DIR_CRF_DATA}/train_pos
test_pos=${DIR_CRF_DATA}/test_pos
val_pos=${DIR_CRF_DATA}/val_pos

# ===== CRF data =====
CRF_DATA=false

train_pw=${DIR_CRF_DATA}/train_pw
test_pw=${DIR_CRF_DATA}/test_pw
val_pw=${DIR_CRF_DATA}/val_pw
train_pph=${DIR_CRF_DATA}/train_pph
test_pph=${DIR_CRF_DATA}/test_pph
val_pph=${DIR_CRF_DATA}/val_pph
train_iph=${DIR_CRF_DATA}/train_iph
test_iph=${DIR_CRF_DATA}/test_iph
val_iph=${DIR_CRF_DATA}/val_iph

# ===== CRF train =====
CRF_TRAIN=false

crf_learn=/work/dingchuang/research/tts/prosody/subjective/tools/CRF++-0.58/crf_learn
crf_test=/work/dingchuang/research/tts/prosody/subjective/tools/CRF++-0.58/crf_test
DIR_TEMPL=${DIR_DATA}/templ
templ_pw=${DIR_TEMPL}/pw/template
templ_pph=${DIR_TEMPL}/pph/template
templ_iph=${DIR_TEMPL}/iph/template
DIR_CRF_MODEL=${DIR_MODEL}/CRF
crf_model_pw=${DIR_CRF_MODEL}/pw
crf_model_pph=${DIR_CRF_MODEL}/pph
crf_model_iph=${DIR_CRF_MODEL}/iph
DIR_CRF_LOG=${DIR_LOG}/CRF
DIR_CRF_RESULT=${DIR_RESULT}/CRF
crf_result_pw=${DIR_CRF_RESULT}/pw
crf_result_pph=${DIR_CRF_RESULT}/pph
crf_result_iph=${DIR_CRF_RESULT}/iph

# ===== get best CRF =====
BEST_CRF=false

pw_best=${DIR_CRF_RESULT}/pw_best
pph_best=${DIR_CRF_RESULT}/pph_best
iph_best=${DIR_CRF_RESULT}/iph_best

# ===== get all CRF =====
ALL_CRF=false

DIR_CRF_ALL=${DIR_CRF_RESULT}/all
model_crf_pw_best=${DIR_CRF_ALL}/model_pw
model_crf_pph_best=${DIR_CRF_ALL}/model_pph
model_crf_iph_best=${DIR_CRF_ALL}/model_iph

data_pw=${DIR_CRF_ALL}/data_pw
data_pph=${DIR_CRF_ALL}/data_pph
data_iph=${DIR_CRF_ALL}/data_iph
result_pw=${DIR_CRF_ALL}/result_pw
result_pph=${DIR_CRF_ALL}/result_pph
result_iph=${DIR_CRF_ALL}/result_iph

pred_crf=${DIR_CRF_ALL}/pred_crf
result_crf=${DIR_CRF_ALL}/result_crf

# ===== DL one hot =====
DL_ONE=false

DIR_DL_DATA=${DIR_DATA}/DL

## ===== DICT =====
MKDICT_ONE=false

dict_character=${DIR_DL_DATA}/dict_character
freq=3

## ===== make data one hot =====
MKDATA_ONE=false

test_pw_in=${DIR_DL_DATA}/test_pw_in
test_pw_out=${DIR_DL_DATA}/test_pw_out
test_pph_in=${DIR_DL_DATA}/test_pph_in
test_pph_out=${DIR_DL_DATA}/test_pph_out
test_iph_in=${DIR_DL_DATA}/test_iph_in
test_iph_out=${DIR_DL_DATA}/test_iph_out
test_frame=${DIR_DL_DATA}/test_frame

val_pw_in=${DIR_DL_DATA}/val_pw_in
val_pw_out=${DIR_DL_DATA}/val_pw_out
val_pph_in=${DIR_DL_DATA}/val_pph_in
val_pph_out=${DIR_DL_DATA}/val_pph_out
val_iph_in=${DIR_DL_DATA}/val_iph_in
val_iph_out=${DIR_DL_DATA}/val_iph_out
val_frame=${DIR_DL_DATA}/val_frame

train_pw_in=${DIR_DL_DATA}/train_pw_in
train_pw_out=${DIR_DL_DATA}/train_pw_out
train_pph_in=${DIR_DL_DATA}/train_pph_in
train_pph_out=${DIR_DL_DATA}/train_pph_out
train_iph_in=${DIR_DL_DATA}/train_iph_in
train_iph_out=${DIR_DL_DATA}/train_iph_out
train_frame=${DIR_DL_DATA}/train_frame

# ===== NC =====
NC_ONE=false

test_pw_nc=${DIR_DL_DATA}/test_pw.nc
test_pph_nc=${DIR_DL_DATA}/test_pph.nc
test_iph_nc=${DIR_DL_DATA}/test_iph.nc

val_pw_nc=${DIR_DL_DATA}/val_pw.nc
val_pph_nc=${DIR_DL_DATA}/val_pph.nc
val_iph_nc=${DIR_DL_DATA}/val_iph.nc

train_pw_nc=${DIR_DL_DATA}/train_pw.nc
train_pph_nc=${DIR_DL_DATA}/train_pph.nc
train_iph_nc=${DIR_DL_DATA}/train_iph.nc

## ===== DL ONE TRAIN ====
DL_ONE_TRAIN=false

DIR_EXP=${HOME}/exp
DIR_DL_ONE_EXP=${DIR_EXP}/DL_ONE
EXP_PW=${DIR_DL_ONE_EXP}/pw
EXP_PPH=${DIR_DL_ONE_EXP}/pph
EXP_IPH=${DIR_DL_ONE_EXP}/iph

# ===== make data embedding =====
NC_WORD_EMBEDDING=true

function run_crf()
{
    f=$1
    c=$2
    item=$3
    result=$4
    t=$( date +%Y%m%d%H%M%S )
    template=$( eval "echo \$templ_${item}" )
    train_data=$( eval "echo \$train_${item}" )
    model=$( eval "echo \$crf_model_${item}" )
    model=${model}/model_${f}_${c}
    ${crf_learn} -f $f -c $c -p 10 -a CRF-L1 ${template} ${train_data} ${model} > ${DIR_CRF_LOG}/${item}_${f}_${c}

    dir_result=$( eval "echo \$crf_result_${item}" )

    train_result=${dir_result}/train_${f}_${c}
    ${crf_test} -m ${model} ${train_data} > ${train_result} 
    echo $f $c "train" >> ${result}
    python ${DIR_SCRIPTS}/evalCRF.py ${train_result} >> ${result}

    val_data=$( eval "echo \$val_${item}" )
    val_result=${dir_result}/val_${f}_${c}
    ${crf_test} -m ${model} ${val_data} > ${val_result}
    echo $f $c "val" >> ${result}    
    python ${DIR_SCRIPTS}/evalCRF.py ${val_result} >> ${result}

    test_data=$( eval "echo \$test_${item}" )
    test_result=${dir_result}/test_${f}_${c}
    ${crf_test} -m ${model} ${test_data} > ${test_result}
    echo $f $c "test" >> ${result}    
    python ${DIR_SCRIPTS}/evalCRF.py ${test_result} >> ${result}
}

function loop_crf()
{
    f=$1
    ck=$3
    item=$5
    result=$( eval "echo \$crf_result_${item}")
    result=${result}/loop_crf
    rm ${result}
    touch ${result}
    while (( $f <= $2 ))
    do
        c=${ck}
        while (( $( echo " $c <= $4 " | bc ) ))
        do
            run_crf $f $c $item $result
            c=$( echo " $c + 0.2 " | bc )
        done
        f=$( echo " $f + 1 " | bc )
    done

    echo "Done!!!"
}

function mymkdir()
{
    directory=$1
    if [ ! -d ${directory} ]; then
        mkdir ${directory}
    else
        echo "[WARNING]: Folder "${directory} already exists!
    fi
}

function rhy2raw()
{
    rhy=$1
    raw=$2
    sed 's/1//g;s/2//g;s/3//g' ${rhy} > ${raw}
}
