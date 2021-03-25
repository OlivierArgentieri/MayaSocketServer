#!/usr/bin/env bash

BASEDIR=$(dirname "$0")
BASEDIR="${BASEDIR//\\//}"  # backslash to forward slash
echo $BASEDIR
rez-env DccSocketServer -- maya # start with maya for example

$SHELL