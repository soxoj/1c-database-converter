# 1C database converter

The tool for extacting content of 1CD and other 1C files and exporting to CSV.

## Usage

```sh
$ python3 -m onec_database_converter <target>

# or simply

$ onec_database_converter <target>

# or locally without installing

$ ./run.py <target>
```

<details>
<summary>Targets</summary>
</br>

Specify targets one or more times:
```sh
$ onec_database_converter conf.cf 8-2-14.1CD
Target: conf.cf
Results found: 1
1) Out Dir: conf.cf_unpack
File Type: container
Status: Exported content of container file

------------------------------
Target: 8-2-14.1CD
Results found: 1
1) Out Dir: 8-2-14.1CD_csv
File Type: 1CD
Status: Exported content of 1CD file

------------------------------
Total found: 2
```

Or use a file with files list:
```sh
$ onec_database_converter --target-list files.txt
```

Or combine tool with other through input/output pipelining:
```sh
$ cat list.txt | onec_database_converter --targets-from-stdin
```
</details>

## Installation

Make sure you have Python3 and pip installed.


<details>
<summary>Manually</summary>
</br>

1. Clone or [download](https://github.com/soxoj/osint-cli-tool-skeleton/archive/refs/heads/main.zip) respository
```sh
$ git clone https://github.com/soxoj/osint-cli-tool-skeleton
```

2. Install dependencies
```sh
$ pip3 install -r requirements.txt
```
</details>

<details>
<summary>As a the package</summary>
</br>

You can clone/download repo and install it from the directory to use as a Python package.
```sh
$ pip3 install .
```

Also you can install it from the PyPI registry:
```sh
$ pip3 install https://github.com/soxoj/osint-cli-tool-skeleton
```
</details>
