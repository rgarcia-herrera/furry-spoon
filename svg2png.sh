#!/bin/bash

SVG=$1

PREFIX=`basename $SVG .svg`

PNG=${PREFIX}.png

convert $SVG $PNG
