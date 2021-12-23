#!/bin/bash
# Part 3.

set -eou pipefail

rm -rf data-bin
./prepare.py
fairseq-preprocess \
    --source-lang tgl.lemma \
    --target-lang tgl.agfocnfin \
    --trainpref train \
    --validpref dev \
    --testpref test \
    --tokenizer space \
    --thresholdsrc 2 \
    --thresholdtgt 2
