# SCRUTINY

[![Pylint](https://github.com/NimRo97/scrutiny/actions/workflows/pylint.yml/badge.svg?branch=main)](https://github.com/NimRo97/scrutiny/actions/workflows/pylint.yml)
[![Flake8](https://github.com/NimRo97/scrutiny/actions/workflows/flake8.yml/badge.svg?branch=main)](https://github.com/NimRo97/scrutiny/actions/workflows/flake8.yml)

An automated toolkit to analyze secure hardware, and build user-verifiable hardware profiles. SCRUTINY provides high-level frameworks to verify profiles against reference and produce detailed HTML reports. For now, SCRUTINY is capable of Java Card analysis and verification.

## How does it work?

SCRUTINY will run set of open-source tools to gather information about your smart card. The information will be parsed and united into JSON profile. Such profile can be compared to reference, producing verification JSON profile, which can be transformed to HTML report, easily readable by a human.

## Set-up

### 1. Download the repository

`$ git clone https://github.com/NimRo97/scrunity.git`

### 2. Run the set-up script

`$ python -u setup_script.py`

### 3. Connect your Java Card

### 4. Run SCRUTINY Java Card analysis

`$ python -u jcscrutinize.py Supposedly_NXP_P60`

### 5. Compare the profile with reference

`$ python -u verify.py --profile results/Supposedly_NXP_P60.json --reference database/NXP_P60.json -o NXP_P60_Verifycation.json`

### 6. Produce HTML report

`$ python -u projectHTML.py -c NXP_P60_Verifycation.json -o NXP_P60_Verifycation_Report.html`

### 7. Read the report using any decent web browser and learn about your Java Card

### 8. Profit?

## Detailed usage

Run any of the scripts with `-h/--help` to show detailed usage instructions.

## Dependencies

Python 3.8 with PIP, Java Runtime Environment.

## Limitations

SCRUTINY is limited by the tools it depends on. Selection from multiple connected smart cards is not supported. Please, have at most one card connected to the PC while performing SCRUTINY.
