# MIT License
#
# Copyright (c) 2020-2024 SCRUTINY developers
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import sys
from pathlib import Path
import shutil

ATR_NAMES_FILES = 'atr_cardname.csv'


def search_files(folder):
    for root, dirs, files in os.walk(folder):
        yield from [os.path.join(root, x) for x in files]


def get_files_to_process(walk_dir: Path, required_extension: str):
    files_to_process = []
    for file_name in search_files(walk_dir):
        if not os.path.isfile(file_name):
            continue
        file_ext = file_name[file_name.rfind('.'):]
        if file_ext.lower() != required_extension:
            continue
        files_to_process.append(file_name)

    return files_to_process


def prepare_card_profiles(input_base_dir: str, out_target_dir: str):
    ALGSUPPORT_DIR = input_base_dir + '/results/'
    PERF_FIXED_DIR = input_base_dir + '/performance/fixed/'
    PERF_VARIABLE_DIR = input_base_dir + '/performance/variable/'
    algsupport_files = get_files_to_process(Path(ALGSUPPORT_DIR), '.csv')
    perffixed_files = get_files_to_process(Path(PERF_FIXED_DIR), '.csv')
    perfvariable_files = get_files_to_process(Path(PERF_VARIABLE_DIR), '.csv')

    if not os.path.isdir(out_target_dir + '/results/'):
        os.mkdir(out_target_dir + '/results/')

    transformed_files = {}
    with open(input_base_dir + '/' + ATR_NAMES_FILES) as f:
        lines = f.readlines()

        for line in lines:
            line = line.strip()
            if len(line) == 0:
                continue
            atr, cardname = line.split(';')
            cardname_under = cardname.replace(' ', '_')
            transformed_files[cardname_under] = []
            target_dir = out_target_dir + '/results/' + cardname_under + '/'
            if not os.path.isdir(target_dir):
                os.mkdir(target_dir)
            for file_name in algsupport_files:
                if os.path.basename(file_name).startswith(cardname_under):
                    # copy ALGSUPPORT_DIR/file_name to results/cardname/file_name
                    shutil.copy(file_name, target_dir)
                    transformed_files[cardname_under].append(file_name)
            for file_name in perffixed_files:
                if os.path.basename(file_name).startswith(cardname_under):
                    # copy ALGSUPPORT_DIR/file_name to results/cardname/file_name
                    shutil.copy(file_name, target_dir)
                    transformed_files[cardname_under].append(file_name)
            for file_name in perfvariable_files:
                if os.path.basename(file_name).startswith(cardname_under):
                    # copy ALGSUPPORT_DIR/file_name to results/cardname/file_name
                    shutil.copy(file_name, target_dir)
                    transformed_files[cardname_under].append(file_name)

    for cardname in transformed_files.keys():
        print(cardname)
        for file in transformed_files[cardname]:
            print('  ' + file)


if __name__ == "__main__":
    prepare_card_profiles(sys.argv[1], sys.argv[2])
