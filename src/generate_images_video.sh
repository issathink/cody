#!/bin/bash

##########################################################
# To launch : ./script.sh rollernet.dyn 70 rollernet rep #
# First parameter : data filename                        #
# Second parameter : max range of X and Y axis           #
# Third parameter : video filename suffix                #
# Fourth parameter : data to plot (.txt files)           #
##########################################################

tmp=`pwd`; cd $4; rm [0-9]*.jpg; cd $tmp

for i in `ls "$4" | egrep "$1.+\.txt"`; do
    file="$4/$i";
    t="src='$file'; dst='${file%.txt}.jpg'; xmax='$2'; ymax='$2'";
    gnuplot -e "$t" plot.plg
done

# cd ../data
cd $4

# echo "`ls | egrep "$1.*out\.jpg"`"

# Generate "out" evolution video
for file in `ls | egrep "$1.*out\.jpg"` ; do mv "$file" "${file//$1/}" ; done
echo "`ls | egrep "[0-9].*out\.jpg" | sort -t'_' -k1,1n `" > file-list-out
mencoder "mf://@file-list-out" -mf fps=2 -o "out$3.avi" -ovc lavc -lavcopts vcodec=msmpeg4v2:vbitrate=800

# Generate "in" evolution video
for file in `ls | egrep "$1.*in\.jpg"` ; do mv "$file" "${file//$1/}" ; done
echo "`ls | egrep "[0-9].*in\.jpg" | sort -t'_' -k1,1n `" > file-list-in
mencoder "mf://@file-list-in" -mf fps=2 -o "in$3.avi" -ovc lavc -lavcopts vcodec=msmpeg4v2:vbitrate=800

mv "in$3.avi" "out$3.avi" ..

# for file in `ls | egrep "$1.*out\.jpg"` ; do mv "$file" "${file//rollernet.dyn/}" ; done
# echo "`ls | egrep "$1.*out\.jpg" | sort -t'_' -k1,1n `"
