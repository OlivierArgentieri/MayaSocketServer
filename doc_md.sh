#!/usr/bin/env bash

BASEDIR=$(dirname "$0")
BASEDIR="${BASEDIR//\\//}"
BASEDIR=$BASEDIR"/../../doc/sphinx/"
cd $BASEDIR
rez-env Sphinx PyYAML sphinx_rtd_theme sphinx_markdown_builder -- make markdown

$SHELL