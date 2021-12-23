#!/usr/bin/env python
"""Error analysis on fairseq-generate output."""


import argparse
import re

from typing import Iterable, List, Tuple

# fairseq-generate parsing.


LOG_STATEMENT = r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} | INFO"
FINAL_STATEMENT = r"Generate (\w)+ with"


Sequence = List[str]


def _output(path: str) -> Iterable[Tuple[Sequence, Sequence, Sequence, float]]:
    """Generates source, target, hypothesis, and posterior score tuples."""
    with open(path, "r") as generate:
        while True:
            try:
                line = next(generate)
            except StopIteration:
                return
            if re.match(LOG_STATEMENT, line):
                continue
            if re.match(FINAL_STATEMENT, line):
                return
            # Otherwise, the format is:
            # S: "source"
            # T: "target"
            # H: score <tab> "hypothesis"
            # D: score <tab> "detokenized hypothesis"
            # P: positional scores per token.
            # We extract S, T, H, and H's score.
            assert line.startswith("S-"), line
            _, source_str = line.split("\t", 1)
            source = source_str.split()
            line = next(generate)
            assert line.startswith("T-"), line
            _, target_str = line.split("\t", 1)
            target = target_str.split()
            line = next(generate)
            assert line.startswith("H-"), line
            _, score_str, hypothesis_str = line.split("\t", 2)
            score = float(score_str)
            hypothesis = hypothesis_str.split()
            # TODO: I think there can be multiple hypotheses per S/T pair, but
            # this is not yet supported.
            yield source, target, hypothesis, score
            # Skips over the next two.
            line = next(generate)
            assert line.startswith("D-"), line
            line = next(generate)
            assert line.startswith("P-"), line


def main(args: argparse.Namespace) -> None:
    error = 0
    total = 0
    for _, tgt_lst, hyp_lst, _ in _output(args.pred):
        tgt = " ".join(tgt_lst)
        hyp = " ".join(hyp_lst)
        if tgt != hyp:
            error += 1
        total += 1
    wer = 100 * error / total
    print(f"WER:\t{wer:.2f}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pred", help="pred file path")
    main(parser.parse_args())
