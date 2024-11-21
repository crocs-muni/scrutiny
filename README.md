# SCRUTINY

[![Pylint](https://github.com/crocs-muni/scrutiny/actions/workflows/pylint.yml/badge.svg?branch=main)](https://github.com/crocs-muni/scrutiny/actions/workflows/pylint.yml)
[![Flake8](https://github.com/crocs-muni/scrutiny/actions/workflows/flake8.yml/badge.svg?branch=main)](https://github.com/crocs-muni/scrutiny/actions/workflows/flake8.yml)

An automated toolkit to analyze secure hardware, and build user-verifiable hardware profiles. SCRUTINY provides high-level frameworks to verify profiles against reference and produce detailed HTML reports. For now, SCRUTINY is capable of JavaCard smartcards, Trusted Platform Modules (TPM), self-encrypted disks (SED) and cryptographic libraries analysis and verification using domain-specific tools listed below (tools marked with * are developed primarily by a third party):

- [JCAlgTest](https://github.com/crocs-muni/JCAlgTest)    ![stars](https://img.shields.io/github/stars/crocs-muni/JCAlgTest.svg?style=social) ![lastcommit](https://img.shields.io/github/last-commit/crocs-muni/JCAlgTest.svg) ![numcontributors](https://img.shields.io/github/contributors-anon/crocs-muni/JCAlgTest.svg) 
  <br>
Automated testing tool for algorithms from JavaCard API supported by particular smart card. Performance testing of almost all available methods. The results for more than 60+ cards available at https://jcalgtest.org. 


- [jcAIDScan](https://github.com/petrs/jcAIDScan)    ![stars](https://img.shields.io/github/stars/petrs/jcAIDScan.svg?style=social) ![lastcommit](https://img.shields.io/github/last-commit/petrs/jcAIDScan.svg) ![numcontributors](https://img.shields.io/github/contributors-anon/petrs/jcAIDScan.svg) 
  <br>
An automated scanner for JavaCard packages installed and supported by target card. Evaluates all packages from JavaCard API specification up to JC API 3.0.5.

- [GlobalPlatformPro tool*](https://github.com/martinpaljak/GlobalPlatformPro)    ![stars](https://img.shields.io/github/stars/martinpaljak/GlobalPlatformPro.svg?style=social) ![lastcommit](https://img.shields.io/github/last-commit/martinpaljak/GlobalPlatformPro.svg) ![numcontributors](https://img.shields.io/github/contributors-anon/martinpaljak/GlobalPlatformPro.svg) 
  <br>
Mature tool for managing applets via GlobalPlatform

- [TPMAlgTest](https://github.com/crocs-muni/tpm2-algtest)    ![stars](https://img.shields.io/github/stars/crocs-muni/tpm2-algtest.svg?style=social) ![lastcommit](https://img.shields.io/github/last-commit/crocs-muni/tpm2-algtest.svg) ![numcontributors](https://img.shields.io/github/contributors-anon/crocs-muni/tpm2-algtest.svg) 
  <br>
A scanner for Trusted Platform Module algorithms, performance and properties of cryptographic implementation. 

- [JCMathLib - ECPoint library](https://github.com/OpenCryptoProject/JCMathLib)    ![stars](https://img.shields.io/github/stars/OpenCryptoProject/JCMathLib.svg?style=social) ![lastcommit](https://img.shields.io/github/last-commit/OpenCryptoProject/JCMathLib.svg) ![numcontributors](https://img.shields.io/github/contributors-anon/OpenCryptoProject/JCMathLib.svg)   <br>
Provides software re-implementation of low-level operations like ECPoint or BigInteger without any use of proprietary API. Used for JavaCard capabilities testing.

- [ECTester](https://github.com/crocs-muni/ectester)    ![stars](https://img.shields.io/github/stars/crocs-muni/ectester.svg?style=social) ![lastcommit](https://img.shields.io/github/last-commit/crocs-muni/ectester.svg) ![numcontributors](https://img.shields.io/github/contributors-anon/crocs-muni/ectester.svg) 
  <br>
ECTester is a tool for testing and analysis of elliptic curve cryptography implementations on JavaCards and in cryptographic libraries.

- [pyecsca](https://github.com/J08nY/pyecsca)    ![stars](https://img.shields.io/github/stars/J08nY/pyecsca.svg?style=social) ![lastcommit](https://img.shields.io/github/last-commit/J08nY/pyecsca.svg) ![numcontributors](https://img.shields.io/github/contributors-anon/J08nY/pyecsca.svg) 
  <br>
Python Elliptic Curve cryptography Side-Channel Analysis toolkit. Focuses on black-box implementations of ECC and presents a way to extract implementation information about a black-box implementation of ECC through side-channels. The main goal of pyecsca is to be able to reverse engineer the curve model, coordinate system, addition formulas, scalar multiplier and even finite-field implementation details.

- [ec-detector](https://github.com/crocs-muni/ec-detector)    ![stars](https://img.shields.io/github/stars/crocs-muni/ec-detector.svg?style=social) ![lastcommit](https://img.shields.io/github/last-commit/crocs-muni/ec-detector.svg) ![numcontributors](https://img.shields.io/github/contributors-anon/crocs-muni/ec-detector.svg) 
  <br>
EC detector is a code parser that can determine, with some degree of confidence, which elliptic curves a given piece of code contains. 

- [roca_detect](https://github.com/crocs-muni/roca)    ![stars](https://img.shields.io/github/stars/crocs-muni/roca.svg?style=social) ![lastcommit](https://img.shields.io/github/last-commit/crocs-muni/roca.svg) ![numcontributors](https://img.shields.io/github/contributors-anon/crocs-muni/roca.svg) 
  <br>
Tester of properties of keys vulnerable to Return of the Coppersmith’s Attack (CVE-2017-15361) allowing practical factorization of RSA keys from Infineon chips.

- [RSABias](https://github.com/crocs-muni/RSABias)    ![stars](https://img.shields.io/github/stars/crocs-muni/RSABias.svg?style=social) ![lastcommit](https://img.shields.io/github/last-commit/crocs-muni/RSABias.svg) ![numcontributors](https://img.shields.io/github/contributors-anon/crocs-muni/RSABias.svg) 
  <br>
Tester of statistical properties of RSA keys, which vary between different cryptographic libraries. 

- [Javus](https://github.com/crocs-muni/Javus)    ![stars](https://img.shields.io/github/stars/crocs-muni/Javus.svg?style=social) ![lastcommit](https://img.shields.io/github/last-commit/crocs-muni/Javus.svg) ![numcontributors](https://img.shields.io/github/contributors-anon/crocs-muni/Javus.svg) 
  <br>
A testing framework for executing known logical attacks against the JavaCard platform. The behavioral characteristics of JCVM are retrieved.

- [JCProfilerNext](https://github.com/lzaoral/JCProfilerNext)    ![stars](https://img.shields.io/github/stars/lzaoral/JCProfilerNext.svg?style=social) ![lastcommit](https://img.shields.io/github/last-commit/lzaoral/JCProfilerNext.svg) ![numcontributors](https://img.shields.io/github/contributors-anon/lzaoral/JCProfilerNext.svg)  <br>
Performance profiler for Java Card code. Provides a completely automated preprocessing, compilation, installation and profiling of JavaCard code on JavaCard smart cards. Produces interactive performance graphs.

- [opal-toolset](https://github.com/crocs-muni/opal-toolset)    ![stars](https://img.shields.io/github/stars/crocs-muni/opal-toolset.svg?style=social) ![lastcommit](https://img.shields.io/github/last-commit/crocs-muni/opal-toolset.svg) ![numcontributors](https://img.shields.io/github/contributors-anon/crocs-muni/opal-toolset.svg) 
  <br>
A set of tools for managing and analysing Opal SED devices.

- [booltest](https://github.com/ph4r05/booltest)    ![stars](https://img.shields.io/github/stars/ph4r05/booltest.svg?style=social) ![lastcommit](https://img.shields.io/github/last-commit/ph4r05/booltest.svg) ![numcontributors](https://img.shields.io/github/contributors-anon/ph4r05/booltest.svg)  <br>
Boolean PRNG tester - analysing statistical properties of PRNGs.

- [cooltest](https://github.com/jirigav/cooltest/)    ![stars](https://img.shields.io/github/stars/jirigav/cooltest.svg?style=social) ![lastcommit](https://img.shields.io/github/last-commit/jirigav/cooltest.svg) ![numcontributors](https://img.shields.io/github/contributors-anon/jirigav/cooltest.svg)  <br>
CoolTest is a randomness-testing tool using distinguishers based on a histogram construction. 

- [sec-certs](https://github.com/crocs-muni/sec-certs)    ![stars](https://img.shields.io/github/stars/crocs-muni/sec-certs.svg?style=social) ![lastcommit](https://img.shields.io/github/last-commit/crocs-muni/sec-certs.svg) ![numcontributors](https://img.shields.io/github/contributors-anon/crocs-muni/sec-certs.svg) 
  <br>
A tool for data scraping and analysis of security certificates from Common Criteria and FIPS 140-2/3 frameworks.

## How does it work?

SCRUTINY will run set of open-source tools (see above) to gather information about your smart card, TPM, disk or cryptographic library. The information will be parsed and united into JSON profile. Such profile can be compared to reference, producing verification JSON profile, which can be transformed to HTML report, easily readable by a human.

## Set-up

### 1. Download the repository

`$ git clone https://github.com/crocs-muni/scrutiny.git`

### 2. Run the set-up script

`$ python -u setup_script.py`

### 3. Connect your Java Card

### 4. Run SCRUTINY Java Card analysis

`$ python -u measure_javacard.py Supposedly_NXP_P60`

### 5. Compare the profile with reference

`$ python -u verify.py --profile results/Supposedly_NXP_P60.json --reference database/NXP_P60.json -o NXP_P60_Verification.json`

### 6. Produce HTML report

`$ python -u report_html.py -v NXP_P60_Verification.json -o NXP_P60_Verification_Report.html`

### 7. Read the report using any decent web browser and learn about your Java Card

### 8. Profit?

## Detailed usage

Run any of the scripts with `-h/--help` to show detailed usage instructions.

## Dependencies

Python 3.8 with PIP, Java Runtime Environment.

## Limitations

SCRUTINY is limited by the tools it depends on. Selection from multiple connected smart cards in the measurement script is not supported. Please, have at most one card connected to the PC while performing SCRUTINY Measure for Java Cards.
