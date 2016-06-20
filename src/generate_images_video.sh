#!/bin/bash

# t="src='rollernet.dyn100_nb_in.txt'; dst='a.jpg'; xmax='70'; ymax='70'";

rm ../data/[1-9]*.jpg;

for i in `ls ../data | egrep "$1.+\.txt"`; do
    file="../data/$i";
    t="src='$file'; dst='${file%.txt}.jpg'; xmax='70'; ymax='70'";
    gnuplot -e "$t" plot.plg
done

cd ../data
# echo "`ls | egrep "$1.*out\.jpg"`"

# Generate "out" evolution video
for file in `ls | egrep "$1.*out\.jpg"` ; do mv "$file" "${file//$1/}" ; done
echo "`ls | egrep "[1-9].*out\.jpg" | sort -t'_' -k1,1n `" > file-list-out
mencoder "mf://@file-list-out" -mf fps=3 -o out.avi -ovc lavc -lavcopts vcodec=msmpeg4v2:vbitrate=800

# Generate "in" evolution video
for file in `ls | egrep "$1.*in\.jpg"` ; do mv "$file" "${file//$1/}" ; done
echo "`ls | egrep "[1-9].*in\.jpg" | sort -t'_' -k1,1n `" > file-list-in
mencoder "mf://@file-list-in" -mf fps=3 -o in.avi -ovc lavc -lavcopts vcodec=msmpeg4v2:vbitrate=800


# for file in `ls | egrep "$1.*out\.jpg"` ; do mv "$file" "${file//rollernet.dyn/}" ; done
# echo "`ls | egrep "$1.*out\.jpg" | sort -t'_' -k1,1n `"