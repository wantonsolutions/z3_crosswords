#!/bin/bash

# This script is used to run the controller for the Z3 Crossword puzzle.
# It takes in a single argument, the name of the file containing the puzzle.
# It then runs the controller, which will solve the puzzle and output the
trap 'pkill -P $$' SIGINT SIGTERM
usage="Usage: controller.sh <n>"

if [ -z "$1" ]
  then
    echo $usage
    exit 1
fi

n=$1
echo "Running controller for puzzle $n"

system_cores=`grep -c ^processor /proc/cpuinfo`
echo "System has $system_cores cores"

hostname=`hostname`
echo "running on $hostname"

for i in `seq 1 $n`;
do
    echo "Starting puzzle solver $i"
    python z3_crossword.py $n > "${hostname}_${i}_cxwords.out" &
done

echo "all children forked waiting..."
wait