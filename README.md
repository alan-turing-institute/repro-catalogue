# repro-catalogue
[![All Contributors](https://img.shields.io/badge/all_contributors-7-orange.svg?style=flat-square)](#contributors-)
[![Build Status](https://travis-ci.com/alan-turing-institute/repro-catalogue.svg?branch=master)](https://travis-ci.com/alan-turing-institute/repro-catalogue)
[![PyPI version](https://badge.fury.io/py/repro-catalogue.svg)](https://badge.fury.io/py/repro-catalogue)

A command line tool to catalogue versions of data, code and results to support reproducibility of research projects.

## Contents

* [Introduction](#introduction)
* [Getting started](#getting-started)
  * [Installation](#installation)
  * [Prerequisites](Prerequisites)
* [Usage](#usage)
  * [Catalogue overview](#catalogue-overview)
  * [Available commands](#available-commands)
  * [Optional arguments](#optional-arguments)
* [Useful resources](#useful-resources)
* [Contributing](#contributing)
* [Contributors](#contributors)

## Introduction

Research projects are frequently updated - new data are added, and the code undergoes regular changes. Under these circumstances, it's easy to store results, yet lose track of the context in which they were produced.

To ensure reproducibility of any scientific results we need to reliably record:
- what input data was used :floppy_disk:
- what code was run :desktop_computer:
- what outputs were produced :chart_with_upwards_trend:

The `catalogue` tool aids reproducibility by saving **hash values** of the input data and the results, along with the **git commit hash** of the code used to generate those results. The `catalogue` command line interface then allows the user to easily compare the hash values from different occasions on which the analysis was run so that changes to the input data, code and results can be identified and the impact on reproducibility can be understood.

**Hash functions** map arbitrary sized data to a binary "word" of a fixed length. The mapping is deterministic and the generated hash values are (for all practical purposes) unique. This means that hashing the same file (or a directory of files) will always produce the same value unless something in the files has changed, in which case the hash function would produce a new value. Because the hash value of a given input is unique, comparing hash values is a quick and easy way to check whether two files are the same.

## Getting started

### Installation

The package is available on PyPI:

```{bash}
pip install repro-catalogue
```

### Prerequisites

**Data and code**

To use the tool, we assume you already have a project with some analysis code ready to run on your data. Your project structure might look something like this:

```
├── data_dir/
│   ├── my_data.csv
├── code_dir/
│   ├── my_analysis.py
├── results_dir/
```

**Git**

A pre-requisite for using `catalogue` is that the directory with the analysis code is a git repository. [Git](https://git-scm.com) is a really useful tool for version control (GitHub sits on top of git).

**Command line**

The tool has a command line interface so you will need to open something like Terminal in macOS or Command Prompt in Windows to use it.

Throughout, the tool will require you to provide paths to directories and files. Note that the directory path will look different on different operating systems. On Linux and macOS it may look like `data_dir/my_data.csv`, whereas on Windows it will be `data_dir\my_data.csv` (i.e., use `\` instead of `/`).

## Usage

### Catalogue overview

The `catalogue` tool comes with three commands (`engage`, `disengage`, `compare`) which should be run consecutively:

```
USAGE
  catalogue [-h] <command> [<arg1>] ... [<argN>]

ARGUMENTS
  <command>       The command to execute
  <arg>           The arguments of the command

GLOBAL OPTIONS
  -h (--help)     Display help message.

AVAILABLE COMMANDS
  engage          Run before an analysis. Saves hashes of `input_data` and `code`.
  disengage       Run after an analysis. Check `input_data` and `code` hashes now
                  are the same as at `engage`. Hash `output_data` and save all
                  hashes to a `TIMESTAMP.json` file.
  compare         Compare hashes.
```

Note that all arguments have default values which will be used if they are not provided. To see these use:

```{bash}
catalogue <command> -h
```

### Available commands

#### engage

This command is run before an analysis is conducted:

```{bash}
catalogue engage --input_data <data directory> --code <code directory>
```

Replace `<data directory>` and `<code directory>` with the path to the data and code directories. In practice, this might look something like this:

```{bash}
catalogue engage --input_data data_dir --code code_dir
```

This will do a series of things. First it will check that the git working tree in our code folder is clean. It gives users a choice:

```
Working directory contains uncommitted changes.
Do you want to stage and commit all changes? (y/[n])
```

If we choose to proceed, `catalogue` will stage and commit all changes in the code directory. Next it will create a temporary file `.lock` in json format:

```json
//catalogue_results/.lock
{
"timestamp" : {
    "engage": "<timestamp (of catalogue engage)>"
  },
"input_data": {
     "<data directory>" : "<hash of directory>"
   },
"code" : {
     "<code directory>": "<latest git commit hash>"
     }
}
```

Once catalogue is engaged, you can run your analysis.

#### disengage

The `disengage` command is run **immediately after finishing an analysis** to version the results.

For example, my analysis is done by running my code as an executable file in command prompt. Once I have finished running this code, I proceed to the disengage stage:

```{bash}
catalogue disengage \
  --input_data <data directory> \
  --code <code directory> \
  --output_data <results directory>
```

Replace all `<...>` with a path to the directory described. In practice, the command might look something like this:

```{bash}
catalogue disengage --input_data data_dir --code code_dir --output_data results_dir
```

Running this command checks that the `input_data` and `code` hashes match the hashes in the `.lock` file (created during `engage`). If they do, it will take hashes of the files in `output_data` and produce the following file in a `catalogue_results` directory:

```json
// catalogue_results/<TIMESTAMP>.json
{
"timestamp" : {
     "engage": "<timestamp (of .lock)>",
     "disengage": "<timestamp (new)>"
   },
"input_data": {
     "<data directory>": "<hash of directory>"
   },
"output_data": {
       "<results directory>":{
           "<output file 1>": "<hash of file>",
           "<output file 2>": "<hash of file>",
           ...
           }
     },
"code" : {
     "<code directory>": "<git commit hash>"
     }
}
```

#### compare

The `compare` command can be used to compare two catalogue output files against each other:

```{bash}
catalogue compare <TIMESTAMP1>.json <TIMESTAMP2>.json
```
The arguments should be the paths to the two files to be compared. For example, I might want to compare results produced on different days to check nothing has changed in this period:

```{bash}
catalogue compare catalogue_results/200510-120000.json catalogue_results/200514-170500.json
```

If the hashes in the files are the same, this means the same analysis was run on the same data with the same outputs both times. In that case, `catalogue` will output something like:

```{bash}
results differ in 1 places:
=============================
timestamp

results matched in 3 places:
==============================
input_data
code
output_data

results could not be compared in 0 places:
============================================
```

If only one file is provided to the `compare` command, then the hashes in the file are compared with hashes of the current state of the working directory. In that case, it is possible to also specify paths to the `input_data`, `code` and `output_data` (otherwise the default values are used).

### Optional arguments

#### --csv

It is possible to save the outputs from `disengage` to a csv rather than a json file. For this, use the `--csv` flag followed by the name of the file to save results to. Each new run will be appended as a new line to the csv file. For example:

```{bash}
catalogue disengage --input_data data_dir --code code_dir --output_data results_dir --csv hashes.csv
```

The `compare` command can then also be used with a `--csv` flag. In that case, one would provide the two timestamps to compare (these must exist in the csv file for the command to work):

```{bash}
catalogue compare 200510-120000 200514-170500 --csv hashes.csv
```

It is possible to provide just one timestamp instead of two and this will be compared against the state of the current working directory.

#### --catalogue_results

By default, all files created by `catalogue` are saved in a `catalogue_results` directory. It is possible to change this by using the optional `--catalogue_results` flag. For exmaple:

```{bash}
catalogue engage --input_data data_dir --code code_dir --catalogue_results versioning_files
```

Note that if you change the default `--catalogue_results` directory, you have to use this flag in each subsequent command. Also, this directory cannot be the same as the `--code` directory.

## Useful resources

- [Example usage](docs/example_use.md)
- [Frequently asked questions](docs/FAQs.md)

## Contributing

🚧 This repository is always a work in progress and everyone is encouraged to help us build something that is useful to the many. 🚧

Everyone is asked to follow our [code of conduct](CODE_OF_CONDUCT.md) and to checkout our [contributing guidelines](CONTRIBUTING.md) for more information on how to get started. 

## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="https://github.com/LouiseABowler"><img src="https://avatars1.githubusercontent.com/u/25640708?v=4" width="100px;" alt=""/><br /><sub><b>Louise Bowler</b></sub></a><br /><a href="https://github.com/alan-turing-institute/repro-catalogue/commits?author=LouiseABowler" title="Documentation">📖</a> <a href="#ideas-LouiseABowler" title="Ideas, Planning, & Feedback">🤔</a> <a href="https://github.com/alan-turing-institute/repro-catalogue/pulls?q=is%3Apr+reviewed-by%3ALouiseABowler" title="Reviewed Pull Requests">👀</a> <a href="#projectManagement-LouiseABowler" title="Project Management">📆</a> <a href="#design-LouiseABowler" title="Design">🎨</a> <a href="#maintenance-LouiseABowler" title="Maintenance">🚧</a> <a href="#infra-LouiseABowler" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a></td>
    <td align="center"><a href="http://isla.st"><img src="https://avatars2.githubusercontent.com/u/23707851?v=4" width="100px;" alt=""/><br /><sub><b>Isla</b></sub></a><br /><a href="#design-Islast" title="Design">🎨</a> <a href="#ideas-Islast" title="Ideas, Planning, & Feedback">🤔</a> <a href="https://github.com/alan-turing-institute/repro-catalogue/commits?author=Islast" title="Code">💻</a> <a href="https://github.com/alan-turing-institute/repro-catalogue/commits?author=Islast" title="Documentation">📖</a></td>
    <td align="center"><a href="https://whitakerlab.github.io"><img src="https://avatars1.githubusercontent.com/u/3626306?v=4" width="100px;" alt=""/><br /><sub><b>Kirstie Whitaker</b></sub></a><br /><a href="#design-KirstieJane" title="Design">🎨</a> <a href="#ideas-KirstieJane" title="Ideas, Planning, & Feedback">🤔</a> <a href="#infra-KirstieJane" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a></td>
    <td align="center"><a href="https://sgibson91.github.io/"><img src="https://avatars2.githubusercontent.com/u/44771837?v=4" width="100px;" alt=""/><br /><sub><b>Sarah Gibson</b></sub></a><br /><a href="https://github.com/alan-turing-institute/repro-catalogue/commits?author=sgibson91" title="Code">💻</a> <a href="https://github.com/alan-turing-institute/repro-catalogue/pulls?q=is%3Apr+reviewed-by%3Asgibson91" title="Reviewed Pull Requests">👀</a></td>
    <td align="center"><a href="https://github.com/kevinxufs"><img src="https://avatars2.githubusercontent.com/u/48526846?v=4" width="100px;" alt=""/><br /><sub><b>kevinxufs</b></sub></a><br /><a href="https://github.com/alan-turing-institute/repro-catalogue/pulls?q=is%3Apr+reviewed-by%3Akevinxufs" title="Reviewed Pull Requests">👀</a> <a href="#userTesting-kevinxufs" title="User Testing">📓</a> <a href="https://github.com/alan-turing-institute/repro-catalogue/commits?author=kevinxufs" title="Documentation">📖</a></td>
    <td align="center"><a href="https://github.com/edaub"><img src="https://avatars0.githubusercontent.com/u/45598892?v=4" width="100px;" alt=""/><br /><sub><b>Eric Daub</b></sub></a><br /><a href="#design-edaub" title="Design">🎨</a> <a href="#ideas-edaub" title="Ideas, Planning, & Feedback">🤔</a> <a href="https://github.com/alan-turing-institute/repro-catalogue/commits?author=edaub" title="Code">💻</a> <a href="https://github.com/alan-turing-institute/repro-catalogue/commits?author=edaub" title="Documentation">📖</a> <a href="https://github.com/alan-turing-institute/repro-catalogue/pulls?q=is%3Apr+reviewed-by%3Aedaub" title="Reviewed Pull Requests">👀</a> <a href="#maintenance-edaub" title="Maintenance">🚧</a> <a href="#projectManagement-edaub" title="Project Management">📆</a></td>
    <td align="center"><a href="https://github.com/radka-j"><img src="https://avatars2.githubusercontent.com/u/29207091?v=4" width="100px;" alt=""/><br /><sub><b>Radka Jersakova</b></sub></a><br /><a href="#design-radka-j" title="Design">🎨</a> <a href="#ideas-radka-j" title="Ideas, Planning, & Feedback">🤔</a> <a href="https://github.com/alan-turing-institute/repro-catalogue/commits?author=radka-j" title="Code">💻</a> <a href="https://github.com/alan-turing-institute/repro-catalogue/pulls?q=is%3Apr+reviewed-by%3Aradka-j" title="Reviewed Pull Requests">👀</a> <a href="https://github.com/alan-turing-institute/repro-catalogue/commits?author=radka-j" title="Documentation">📖</a> <a href="#maintenance-radka-j" title="Maintenance">🚧</a> <a href="#projectManagement-radka-j" title="Project Management">📆</a> <a href="#infra-radka-j" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a></td>
  </tr>
</table>

<!-- markdownlint-enable -->
<!-- prettier-ignore-end -->
<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!
