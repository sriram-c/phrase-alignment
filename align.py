# coding=utf-8

import sys
import ast
import re
import  argparse
import regex

import codecs

def process_uniq(path):
	cont = codecs.open(path, 'r', 'utf-8').readlines()


def process_best

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Phrase Alignment of source and target sentence using Heuristics and ML tool", epilog="example: python3 align.py path/to/L1/text path/to/L2/text [options]")

	parser.add_argument("uq_path", type=str)
	parser.add_argument("best_path", type=str)
	parser.add_argument("--num-test-sents", type=int, default=None, help="None means all sentences")

	args = parser.parse_args()


	uniq_op = process_uniq(uq_path)
	best_op = process_best(best_path)


