#!/bin/bash
libs/eval/build.sh
LD_PRELOAD=libs/eval/preload python3 main.py