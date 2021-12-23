#!/usr/bin/env python
"""Prepares the Tagalog data for preprocessing."""

import contextlib
import csv

from typing import TextIO


# I have chosen to hard-code the paths here since what else would I do?

TRAIN = "train.tgl.tsv"
TRAIN_LEMMA = "train.tgl.lemma"
TRAIN_AGFOCNFIN = "train.tgl.agfocnfin"

DEV = "dev.tgl.tsv"
DEV_LEMMA = "dev.tgl.lemma"
DEV_AGFOCNFIN = "dev.tgl.agfocnfin"

TEST = "test.tgl.tsv"
TEST_LEMMA = "test.tgl.lemma"
TEST_AGFOCNFIN = "test.tgl.agfocnfin"


def _split(source: TextIO, lemma: TextIO, agfocnfin: TextIO) -> None:
    reader = csv.reader(source, delimiter="\t")
    for c1, c2, _ in reader:
        print(" ".join(c1), file=lemma)
        print(" ".join(c2), file=agfocnfin)


def main() -> None:
    with contextlib.ExitStack() as stack:
        source = stack.enter_context(open(TRAIN, "r"))
        lemma = stack.enter_context(open(TRAIN_LEMMA, "w"))
        agfocnfin = stack.enter_context(open(TRAIN_AGFOCNFIN, "w"))
        _split(source, lemma, agfocnfin)
    # Processes development data.
    with contextlib.ExitStack() as stack:
        source = stack.enter_context(open(DEV, "r"))
        lemma = stack.enter_context(open(DEV_LEMMA, "w"))
        agfocnfin = stack.enter_context(open(DEV_AGFOCNFIN, "w"))
        _split(source, lemma, agfocnfin)
    # Processes test data.
    with contextlib.ExitStack() as stack:
        source = stack.enter_context(open(TEST, "r"))
        lemma = stack.enter_context(open(TEST_LEMMA, "w"))
        agfocnfin = stack.enter_context(open(TEST_AGFOCNFIN, "w"))
        _split(source, lemma, agfocnfin)


if __name__ == "__main__":
    main()
