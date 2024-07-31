#!/usr/bin/env bash
# This is currently working only on my py39 env
#quarto preview stations_evaluation.qmd --no-browser --no-watch-inputs
NBOOK=plots_for_report.qmd
quarto preview $NBOOK --no-browser --no-watch-inputs

