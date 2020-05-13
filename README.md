# repro-catalogue
<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-3-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->

A command line tool to catalogue versions of data, code and results to support reproducibility of research projects.

## Contents

* [Introduction](#introduction)
* [Installation](#installation)
* [Getting started](#getting-started)
  * [Catalogue overview](#catalogue-overview)
  * [Available commands](#available-commands)
* [Example usage](#example-usage)
  * [Run analysis](#run-analysis)
  * [Check outputs](#check-outputs)
  * [Share outputs](#share-outputs)
* [FAQs](#faqs)
  * [Running in the wrong order](#running-in-the-wrong-order)
  * [Intermediary data processing](#intermediary-data-processing)
  * [Randomness](#randomness)

## Introduction

Research projects commonly have data that is being regularly updated. The code is also regularly tweaked. Given this, it is fairly common to save some results and lose track of the context (data and code) in which they were produced.

To ensure reproducibility of any scientific results we need to reliably record:
- what input data was used
- what code was run
- what outputs were produced

To aid reproducibility, `catalogue` provides a command line interface for recording a hash value of the dataset that was used and the outputs that were produced in an analysis. It also saves the latest git commit hash of the code that was run to do the analysis.

Hash functions map arbitrary sized data to a binary "word" of a fixed length. The mapping is deterministic and the generated hash values are (for all practical purposes) unique. This means that hashing the same file (or a directory of files) will always produce the same value unless something in the files has changed, in which case the hash function would produce a new value. Because the hash value of a given input is unique, comparing hash values is a quick and easy way to check whether two files are the same.

## Installation

```{bash}
git clone https://github.com/alan-turing-institute/repro-catalogue.git
cd repro-catalogue
pip install .
```

## Getting started

### Catalogue overview

The command line interface `catalogue` comes with three commands (`engage`, `disengage`, `compare`) meant to be run consecutively:

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

A **pre-requisite** for using `catalogue` is that the directory with the analysis code is a git repository.

### Available commands

#### engage

This command is run before an analysis is conducted:

```{bash}
catalogue engage --input_data <data directory> --code <code directory>
```

This will do a series of things. First it will check that the git working tree in our code folder is clean. If gives users a choice:

```
Working directory contains uncommitted changes.
Do you want to stage and commit all changes? (y/[n])
```

If we choose to proceed `catalogue` will stage and commit all changes in the code directory. Next it will create a temporary file `.lock` in json format:

```json
//catalogue_results/.lock
{
"timestamp" : {
    "engage": <timestamp (of catalogue engage)>
  },
"input_data": {
     <data_directory> : <hash of directory>
   },
"code" : {
     <code_directory>: <latest git commit hash>
     }
}
```

#### disengage

Immediately after finishing our analysis we run this to version the results:

```{bash}
catalogue disengage \
  --input_data <data directory> \
  --code <code directory> \
  --output_data <results directory>
```

This checks that the `input_data` and `code` hashes match the hashes in `.lock` (created during `engage`). If they do, it will take hashes of the files in `output_data` and produce the following file:

```json
// catalogue_results/TIMESTAMP.json
{
"timestamp" : {
     "engage": <timestamp (of .lock)>,
     "disengage": <timestamp (new)>
   },
"input_data": {
     <data directory>: <hash of directory>
   },
"output_data": {
       <results directory>:{
           <output file 1>: <hash of file>,
           <output file 2>: <hash of file>,
           ...
           }
     },
"code" : {
     <code directory>: <git commit hash>
     }
}
```

#### compare

We can use `catalogue` to compare two catalogue output files against each other:

```{bash}
catalogue compare <TIMESTAMP1.json> <TIMESTAMP2.json>
```

If the hashes in the files are the same, this means the same analysis was run on the same data with the same outputs both times. In that case, `catalogue` will output something like:

```
results differ in 0 places:
=============================

results matched in 3 places:
==============================
input_data
code
output_data

results could not be compared in 0 places:
============================================
```

If only one input is provided to the `compare` command, then the input is compared with the current state of the working directory.

## Example usage

Imagine that on a central sever we have a data repository
```
├── Data folder/
│   ├── database release 1/
│   ├── database release 2/
⋮    ⋮
│   └── version index
```

Elsewhere, in our user directory, perhaps on another computer, things look like this.

```
├── latest_data/
├── latest_code/
├── results/
│   ├── old_results_with_inputs_1/
│   ├── old_results_with_inputs_2/
│   └── latest_results/
├── catalogue_results/
│   ├── TIMESTAMP1.json
│   ├── TIMESTAMP2.json
│   ├── TIMESTAMP3.json
│   └── TIMESTAMP4.json
```

### Run analysis

We've just made some minor tweaks to our code and now we want to run our analysis. Before we start running any of the script in our code folder, we run:

```{bash}
catalogue engage --input_data latest_data --code latest_code
```

Now we run whatever we need to perform our analysis. Immediately after finishing this we run:

```{bash}
catalogue disengage --input_data latest_data --output_data results/latest_results  --code latest_code
```

This will produce the following file:

```json
// catalogue_results/TIMESTAMP5.json
{
"timestamp" : {
     "engage": <timestamp (of .lock)>,
     "disengage": <timestamp (new)>
   },
"input_data": {
     "latest_data" : <hash of directory>
   },
"output_data": {
       "results/latest results":{
           "summary.txt": <hash of file>,
           "output.csv": <hash of file>,
           "metadata.json": <hash of file>
           }
     },
"code" : {
     "latest_code": <git commit hash>
     }
}
```

### Check outputs

Let's suppose that between TIMESTAMP4 and TIMESTAMP5 we modified the code to output a file `summary.txt`, but that otherwise nothing has changed. We would like to check that our file `output.csv` hasn't changed but oops! We've just overwritten it. Luckily we can compare to the json at TIMESTAMP4.

```
catalogue compare \
  catalogue_results/TIMESTAMP4.json \
  catalogue_results/TIMESTAMP5.json
```

Let us also suppose that the `metadata.json` output includes a timestamp. The diff we would expect would look something like this:

```
results differ in *3* places:
=============================
timestamp
code
results/latest_results/metadata.json

results matched in *2* places:
==============================
input_data
results/latest_results/output.csv

results could not be compared in *1* places:
============================================
results/latest_results/summary.text
```

Of course this is what we *want*.

Alternatively, we might find that our `output.csv` file *had* changed. In that case `catalogue` would inform us of the problem without us having to permanently store the output of every analysis we run. The hashes alone would not be enough to recover the original TIMESTAMP4 version. But since we have recorded the timestamp, that information can help us track down the data version, and the git commit digest tells us exactly what version of the code is used, making it easier to try and reproduce those results should we wish to do so.

### Share outputs

We can then send a zip file of the results to a colleague along with the hash json produced during the final analysis (`TIMESTAMP5.json`).

They can rerun the analysis and use `catalogue` to check that the json they received is the same as their state:

```{bash}
catalogue compare TIMESTAMP4.json
```

## FAQs

### Running in the wrong order

The commands `catalogue engage` and `catalogue disengage` are meant to be run in that order.

The `catalogue disengage` command will check that a `.lock` file exists. If it doesn't it will warn:
```
Already engaged (.lock file exists). To disengage run 'catalogue disengage...
See 'catalogue disengage --help' for details
```

The `catalogue engage` command will check that a `.lock` file does *not* exist. If it does, it will warn:
```
Not currently engaged (could not find .lock file). To engage run 'catalogue engage...
See 'catalogue engage --help' for details
```

### Intermediary data processing

It is likely that the analysis includes some preprocessing steps. Ideally all of this preprocessing would be run automatically in synchrony with the rest of our code. In that case we consider it output data, and it should be contained in the `output_data` folder.

### Randomness

Hashing tells you whether something is the same, or different. It cannot tell you if something is almost the same. If your analysis is non-deterministic, you will be getting a different hash every time. To deal with this, we recommend setting a random seed. Whatever language you're using should be able to provide you with documentation on how to do this.

## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="https://github.com/LouiseABowler"><img src="https://avatars1.githubusercontent.com/u/25640708?v=4" width="100px;" alt=""/><br /><sub><b>Louise Bowler</b></sub></a><br /><a href="https://github.com/alan-turing-institute/repro-catalogue/commits?author=LouiseABowler" title="Documentation">📖</a> <a href="#ideas-LouiseABowler" title="Ideas, Planning, & Feedback">🤔</a> <a href="https://github.com/alan-turing-institute/repro-catalogue/pulls?q=is%3Apr+reviewed-by%3ALouiseABowler" title="Reviewed Pull Requests">👀</a> <a href="#projectManagement-LouiseABowler" title="Project Management">📆</a> <a href="#design-LouiseABowler" title="Design">🎨</a> <a href="#maintenance-LouiseABowler" title="Maintenance">🚧</a></td>
    <td align="center"><a href="http://isla.st"><img src="https://avatars2.githubusercontent.com/u/23707851?v=4" width="100px;" alt=""/><br /><sub><b>Isla</b></sub></a><br /><a href="#design-Islast" title="Design">🎨</a> <a href="#ideas-Islast" title="Ideas, Planning, & Feedback">🤔</a> <a href="https://github.com/alan-turing-institute/repro-catalogue/commits?author=Islast" title="Code">💻</a> <a href="https://github.com/alan-turing-institute/repro-catalogue/commits?author=Islast" title="Documentation">📖</a></td>
    <td align="center"><a href="https://whitakerlab.github.io"><img src="https://avatars1.githubusercontent.com/u/3626306?v=4" width="100px;" alt=""/><br /><sub><b>Kirstie Whitaker</b></sub></a><br /><a href="#design-KirstieJane" title="Design">🎨</a> <a href="#ideas-KirstieJane" title="Ideas, Planning, & Feedback">🤔</a> <a href="#infra-KirstieJane" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a></td>
  </tr>
</table>

<!-- markdownlint-enable -->
<!-- prettier-ignore-end -->
<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!