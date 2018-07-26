#!/usr/bin/env bash
#
# Author: Kairo Araujo <kairo@kairo.eti.br>
#

function print_help (){
    echo "Usage [my_project] [new_my_project]"

}

function rename (){

        TEMP_DIR=$(echo /tmp/$2_dir_$(echo $RANDOM))
        PROJECT_DIR=$(pwd)

        FILE_LIST=$(grep -R $1 * | grep -vE "venv|__pycache__|^htmlcov|egg-info" | awk -F: '{ print $1 }' | uniq)

        mkdir ${TEMP_DIR}
        rm -rf $1.egg-info .tox htmlcov __pycache__
        tar cf - * | (cd ${TEMP_DIR}; tar xfp -)

        for file in ${FILE_LIST}; do
            echo "${file} -> ${TEMP_DIR}"
            sed -e "s/$1/$2/g" ${file} > ${TEMP_DIR}/${file}
        done

        cd ${TEMP_DIR}
        tar cf - * | (cd ${PROJECT_DIR}; tar xfp -)
        cd ${PROJECT_DIR}
        mv $1 $2
}

if [[ ! -z $1 ]] && [[ ! -z $2 ]]; then

    if [ ! -d $1 ]; then
        echo "Project name $1 not exists"
        exit 1
    fi

    rename $1 $2

else
    print_help

fi


