import pandas as pd
import re

var_code_pattern = re.compile(r"V08\d+")
description_pattern = re.compile(r"\s{4}\w+.\d.\s(\w.*$)")
section_separator = "============================================================================="

rows = []

with open("small2008.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()
    lines_iter = iter(lines)
    for line in lines_iter:
        if line == section_separator:
            line = next(lines_iter)
            while line != section_separator:
                var_name = re.match(var_code_pattern, line)
                description = re.match(description_pattern, line)
                print(var_name, description)









