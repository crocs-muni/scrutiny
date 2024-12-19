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

import argparse
import jsonpickle

from scrutiny.device import load_device
from scrutiny.interfaces import Contrast

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--reference",
                        help="Reference profile",
                        action="store", metavar="file",
                        required=True)
    parser.add_argument("-p", "--profile",
                        help="Profile to compare against reference",
                        action="store", metavar="file",
                        required=True)
    parser.add_argument("-o", "--output-file",
                        help="Name of output file",
                        action="store", metavar="outfile",
                        required=False, default="contrast.json")
    args = parser.parse_args()

    reference = load_device(args.reference)
    profile = load_device(args.profile)

    contrast = Contrast(reference.name, profile.name)

    for module in reference.modules.values():
        if module.module_name in profile.modules.keys():
            contrast.add_contrasts(
                module.contrast(profile.modules[module.module_name]))

    for module in contrast.contrasts:
        state = module.update_result()
        if state.value > contrast.result.value:
            contrast.result = state

    contrast.result = str(contrast.result)

    with open(args.output_file, "w") as f:
        f.write(jsonpickle.encode(contrast, indent=4))
