#!/bin/bash
###############################################
RUNSTEP=/pipeline/run_step.sh $STATUS
###############################################
set -e
STATUS=$1

# Enter your pipeline steps below
# Syntax: $RUNSTEP $STATUS <DESCRIPTION> <COMMAND>
$RUNSTEP $STATUS "Sync Mails" "/src/imapbox.py"