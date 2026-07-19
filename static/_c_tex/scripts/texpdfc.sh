#!/usr/bin/env bash

# Copyright (c) 2026 Jack Bennett
# From the TexEdit project: https://github.com/kosude/texedit/

# This script compiles PDF output from (La)TeX input, on Unix (including
# Darwin/macOS) systems. Execute it DIRECTLY - do not run with 'source'.

usage() {
    cat << EOF
usage: texpdfc.sh (darwin|linux) TEXNAME OUTDIR

darwin - Use macOS binaries for TeX compilation
linux - Use Linux binaries for TeX compilation
EOF
}

if [ $# -ne 3 ] ; then
    echo Error: malformed syntax
    usage
    exit 1
fi

arch=$1
filename=$(realpath $2)
outdir=$(realpath $3)

base_dir="$(realpath "${0%/*}")"
texlive_bin_dir="$(realpath "$base_dir/bin/$arch")"
pdflatex_bin="$texlive_bin_dir/pdflatex"

source $base_dir/env_$arch.sh $base_dir

cmd="$pdflatex_bin -interaction=nonstopmode -file-line-error -output-directory=$outdir $filename"

echo "texpdfc % $cmd"
$cmd
