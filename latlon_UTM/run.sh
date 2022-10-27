#!/usr/bin/env bash
#This  one is to filver Danish characters
cat $1 | iconv -f iso8859-1 -t utf-8  > $1_clean
