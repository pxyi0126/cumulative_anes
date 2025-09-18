import pandas as pd
import re


var_code_pattern = re.compile(r"V08\d+")
description_pattern = re.compile(r"\s{4}\w+.\d.\s(\w.*$)")
section_separator = "============================================================================="

with open("small2008.txt", "r", encoding="utf-8") as f:
    lines = f.read()





