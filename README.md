# SCRUTINY

An automated toolkit to build and manage Java Card smart card profiles, and verify them against reference profiles.

## How does it work?

JCPeg will run set of open-source tools to gather information about your smart card. The information will be parsed and united into JSON file, eliminating the hassle of learning and parsing results from plethora of tools. Results can be compared and results shown in human-readable form.

## Set-up

### 1. Download the repository

`$ git clone https://github.com/NimRo97/jcpeg.git`

### 2. Run the set-up script

`$ python -u setup_script.py`

### 3. Connect your card and run JCPeg

`$ python -u pegcard.py -e Supposedly_NXP_P60`

### 4. Profit?

## Detailed usage

TODO

## Dependencies

Python 3 with PIP, Java Runtime Environment.

## Limitations

JCPeg is limited by the tools it depends on. Selection from multiple connected cards is not supported. Please, have at most one card connected to the PC when using JCPeg.
