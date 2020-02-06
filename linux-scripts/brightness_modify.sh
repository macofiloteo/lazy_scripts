#!/bin/bash
source config.sh

re='^[0-9]+$'
brightness=98

if [ ! -z $1 ]
then
	brightness=$1
fi

if ! [[ $brightness =~ $re ]]
then
	echo "error: Not a number"
	exit 1
fi

if [ $brightness -gt 100 ]
then
	echo "Pick brightness number less than or equal to 100!"
	exit 1
elif [ $brightness -lt 1 ]
then
	echo "Pick brightness number greathan than or equal to 1!"
	exit 1
else
	echo $brightness | sudo tee $BRIGHTNESS_PATH
	echo "Brightness set to $brightness."
fi
