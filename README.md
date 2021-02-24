# JCPeg
An automated toolkit to identify and verify the type of Java Card smart cards.

## How does it work?
JCPeg will run set of open-source tools to gather information about your smart card. The information will be parsed and united into JSON file, eliminating the hassle of learning and parsing results from plethora of tools. Results can be compared with existing database of cards and shown in human-readable form.

Peg that unknown white smart card that has been lying in your drawer!

## Set-up
### 1. Download the repository:
`$ git clone https://github.com/NimRo97/jcpeg.git`
### 2. Run the set-up script:
`$ python -u setup.py`
### 3. Connect your card and run JCPeg:
`$ python pegcard.py -e Mysterious_Card_From_Mail`
### 4. Profit?

## Detailed usage
TODO

## Dependencies
Python 3 with PIP, Java Runtime Environment.

## Limitations
JCPeg is limited by the tools it depends on. Selection from multiple connected cards is not supported. Please, have at most one card connected to the PC when using JCPeg.

## Manual set-up
If `$ python -u setup.py` finished without errors, you can safely skip this section. If the setup script fails to fetch some necessary files, you can set them up manually using this section.

### GlobalPlatformPro
Building GPPro from submodule would create time-consuming and iffy dependency. Specific release wersion is downloaded from project's repository instead.

If setting up GlobalPlatformPro fails during setup.py, follow the download link in `jcpeg/jcpeg/config.py` and place `gp.jar` in `jcpeg/bin` folder (`jcpeg/bin/gp.jar`).

It is important to download the specific release from link, as the output format of this tool changes between versions.

### JCAlgTest
Building JCAlgTest from submodule would create time-consuming and iffy dependency. Specific release wersion is downloaded from project's repository instead. 

If setting up JCAlgTest fails during setup.py, follow the download link in `jcpeg/jcpeg/config.py` and place `AlgTestJClient.jar` in `jcpeg/bin` folder (`jcpeg/bin/AlgTestJClient.jar`). Place all 3 cap files `AlgTest***.cap` to `jcpeg/cap` folder (`jcpeg/cap/AlgTest***.cap`).

It is important to download the specific release from link.

### jsonpickle
Jsonpickle Python library is needed for JCPeg to generate and work with JSON database. Try running `pip install -U jsonpickle` manually or consult download section in jsonpickle documentation https://jsonpickle.github.io/#download-install.
