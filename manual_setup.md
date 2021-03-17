# Manual set-up
If `$ python -u setup.py` finished without errors, you can safely skip this section. If the setup script fails to fetch some necessary files, you can set them up manually using this section.

### Smart Card List
TODO

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

### dominate
TODO
