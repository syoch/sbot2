#!/bin/bash
# libs/eval/build.sh
LD_PRELOAD=libs/eval/preload/preload python3 test.py
# [ -e safeEvalPy.log ] && (echo "Delete log file from shell script"; rm safeEvalPy.log)