import glob
import os
import time
from typing import List

import typer
from thesmuggler import smuggle
from tqdm import tqdm

from .classes import ColorText, Summary, TestSuite
from .utils import *


def run_test_suites(suites: List[TestSuite], sync=True):

    tqdm.write(ColorText.WHITE + f"Running {len(suites)} test suites \n")

    for suite in tqdm(
        suites, bar_format="{l_bar}{bar:30}{r_bar}{bar:-30b}", desc="All test suites"
    ):
        suite.run(sync=sync)

    summary = Summary(suites)

    tqdm.write(ColorText.YELLOW + "\n*** Summary ***")
    tqdm.write(ColorText.WHITE + summary.print_suites_passed())
    tqdm.write(ColorText.WHITE + summary.print_tests_passed())


def find_test_suites(test_file: str) -> List[TestSuite]:
    assert os.path.isfile(test_file)
    test_module = smuggle(test_file)
    return [
        variable
        for _, variable in test_module.__dict__.items()
        if isinstance(variable, TestSuite)
    ]


def find_test_files(dir: str) -> List[str]:
    """
    Find test files that match the following naming patter:
    - *test.py
    - test*.py

    Search is recursive, so pass in only the parent directory for search
    """
    assert os.path.isdir(dir)
    return match_dir(dir)