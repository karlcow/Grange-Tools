#!/bin/bash
# modified for Nikon D300 - June 2008
# modified for Fuji X100 - November 2011
# We expect one argument only
# This program is really tailored for my own usage
# once photos have been downloaded from your camera 
# they will be moved to a dated space and renamed 
# with the time when they have been taken.
#
if [ $# != 1 ]; then
    echo ""
    echo "Usage: photodated.sh <root-dir>" 
    echo ""
    echo "This program:-"
    echo "  * takes the photos from one directory and puts them in a dated space with a name containing the time, the serial number and the camera type. You must have epinfo installed."
    exit 1  
fi

rootdir=$1

##
# testing if epinfo is here first
#
# 
if [ ! -f /usr/local/bin/epinfo ]; then
    echo "You should install epinfo first"
    echo "See http://www.lightner.net/lightner/bruce/photopc/epinfo.html"
    exit -1
else 
    echo "EPINFO is already installed. Let's move on."
fi


list=`find $1 -iname "*.JPG" -print`

for file in $list
{
    echo "Processing  $file"

    dateinfo=`epinfo $file | grep DateTimeOriginal | sed 's/DateTimeOriginal=//g;s/"//g;'`
    datepath=`echo $dateinfo | awk '{print $1}' |sed 's/:/\//g'`
    if [ ! -d "$HOME/Pictures/$datepath/" ]; then
        echo "Creating    $HOME/Pictures/$datepath/"
        mkdir -p "$HOME/Pictures/$datepath/"
    else
        echo "Already     $HOME/Pictures/$datepath/"
        
    fi
    phototime=`echo $dateinfo | awk '{print $2}'|sed 's/:/-/g'`
    if [[ $file = *DSC_* ]]; then
        echo "Camera       Nikon D300";
        number=`echo $file | sed 's/\.\/DSC_//' | sed 's/\.JPG//'`
        filename="$HOME/Pictures/$datepath/pic$phototime-$number-d300.jpg"
    elif [[ $file = *DSCF* ]]; then
         echo "Camera      Fuji X100";
         number=`echo $file | sed 's/\.\/DSCF//' | sed 's/\.JPG//'`
         filename="$HOME/Pictures/$datepath/pic$phototime-$number-x100.jpg"
    fi
    echo "Name        $filename";
    mv $file $filename
    Echo "DONE........................................................."
        
}

