#!/bin/bash
SCRIPT_DIR=$(dirname "$(readlink -f "$0")")
PROJ_DIR=$(dirname $SCRIPT_DIR)
export PYTHONPATH=$PROJ_DIR
cd $PROJ_DIR
jupyter lab
