# JCPeg
An automated toolkit to identify and verify the type of Java Card smart cards.

## How does it work?
JCPeg will run set of open-source tools to gather information about your smart card. The information will be parsed and united into JSON file, eliminating the hassle of learning and parsing results from plethora of tools. Results can be compared with existing database of cards and shown in human-readable form.

Peg that unknown white smart card that has been lying in your drawer!

## Set-up
### 1. Download the repository:
`$ git clone https://github.com/NimRo97/jcpeg.git`
### 2. Run the set-up script:
`$ python setup.py`
### 3. Connect your card and run JCPeg:
`$ python pegcard.py -e Mysterious_Card_From_Mail`
### 4. Profit?

## Detailed usage

## Manual set-up
TODO

## Dependencies
Python 3 and Java Runtime Environment.

## Limitations
JCPeg is limited by the tools it depends on. Selection from multiple connected cards is not supported. Please, have at most one card connected to the PC when using JCPeg.
