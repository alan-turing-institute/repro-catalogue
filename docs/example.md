# Getting started with `catalogue`

## Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Our first example](#our-first-example)

## Overview

In this example, we'll show you how to use the `catalogue` tool to check the reproducibility of a small analysis pipeline.
We want to make sure that we reliably get the same numerical result from our analysis before we pass our scripts along to a colleague, or publish a report that uses our results.
`catalogue` gives us a simple method that we can use to compare our results as we update our input data and our code.

## Prerequisites

The `catalogue` tool requires a Python installation of version 3.6 or later.
If that is available, you can run
```
pip install repro-catalogue
```
from the command line to install the latest version of `catalogue`.

This example features scripts that are also written in Python.
The use of Python for the analysis is not essential - as long as the code is tracked with `git`, any language can be used.

Several points in this example show how to use `git` to version control your code.
If you haven't used `git` before, it's an incredibly useful tool for tracking changes in files.
We'll give full explanations of the commands we need during the example, and if you want to find out more we highly recommend the [Software Carpentry `git` lesson](https://swcarpentry.github.io/git-novice/).

We'll also make use of the command line to run `git`, Python, and the `catalogue` tool itself.
We will explain the necessary commands as we go along, and you can check out chapters 1-3 of the [Software Carpentry Unix shell lesson](http://swcarpentry.github.io/shell-novice/) if you'd like more details on any of the commands we use.
If you would rather create the folders and download files in an alternative way, feel free to do so :slightly_smiling_face:


And now, let's walk through our first example!

## Our first example

In this example, we're going to generate an output file that contains some simple descriptive statistics of a birthweight dataset :baby:
The dataset consists of the birthweights of 42 babies, together with other information on the babies and their parents.

### Setting up our project

We'll set our project up inside a new folder - let's create one called `repro-catalogue-demo`.
```
mkdir repro-catalogue-demo
```
Inside that folder, we'll create three more.
One will contain the code, one will hold the data and the final folder will be used to store our results.
We'll now move into the `repro-catalogue-demo` folder and create the new folders there.
```
cd repro-catalogue-demo
mkdir birthweight-data
mkdir birthweight-analysis
mkdir birthweight-results
```

Why three separate folders?
Our analysis **code** will be worked on regularly, and all changes to it should therefore be tracked using a version control system.
On the other hand, our **data** will not change (or only be changed very rarely).
The code that we write will depend on the structure of the dataset, but not on the exact values within it.
We can therefore treat changes to our code and data **independently**, and the separated folders help us to achieve this.
The same applies to our **results** - they are dependent on the input data and analysis code, but are not part of either grouping.
Keeping them separate helps us to pose questions such as _"Our results have changed. Is this due to a change in our analysis method, or a change in our input data?"_

### Getting the data

The data that we'll use in this example come from the [University of Sheffield's Maths and Statistics Help teaching datasets](https://www.sheffield.ac.uk/mash/statistics/datasets).
To download the data into our `birthweight-data` folder, run the following command (noting the single quotes)
```
curl 'https://www.sheffield.ac.uk/polopoly_fs/1.886038!/file/Birthweight_reduced_R.csv' --output birthweight-data/Birthweight_reduced_R.csv
```
or download the birthweight dataset in CSV format from the [website](https://www.sheffield.ac.uk/mash/statistics/datasets) and manually save it to the `birthweight-data` folder.

If you open up the file in your preferred text editor, or view the output by running
```
cat birthweight-data/Birthweight_reduced_R.csv
```
you'll see that there is one header row followed by 42 rows of data.
As the file is a csv, we can see commas are used to separate each value in the dataset.

### Writing our first analysis script

The aim of this exercise is to generate a results file that contains some simple descriptive statistics about the birthweight dataset.
In our first iteration of this script, we'll calculate the mean and standard deviation of the available birthweights and write both values to a file.
We'll use Python to write this script, but other languages can be used if you prefer.

Our analysis will be stored in the `birthweight-analysis` folder, so let's start by moving into that directory
```
cd birthweight-analysis
```
We want to track our analysis using `git`.
Before starting to prepare our analysis scripts, we'll initialise a `git` repository in this folder.
We can do that by running the following command from the `birthweight-analysis folder`:
```
git init
```

With `git` now ready to use, we'll prepare our analysis script.
Open a new file in your preferred text editor and copy in the contents of the code block below.
Once the code is in place, save the file to the `birthweight-analysis` folder with the filename `birthweight-descriptive-stats.py`.
```python
import os               # Utility commands for folder names etc.
import pandas as pd     # Useful module for manipulating data in tables - known as data frames in Pandas

# Read the birthweight data from the csv file (we use a relative path to specify the location of the file)
birthweights = pd.read_csv(os.path.join(os.getcwd(), "..", "birthweight-data", "Birthweight_reduced_R.csv"))

# Print out the first few rows of the table (not part of the analysis itself, but it's useful to have a look)
print(birthweights.head())

# Calculate the descriptive statistics that we are interested in
birthweight_average = birthweights["Birthweight"].mean()
birthweight_std_dev = birthweights["Birthweight"].std()

# Create a new data frame that contains our summary statistics
outputs = pd.DataFrame({"average": [birthweight_average],
                        "std dev": [birthweight_std_dev]})

# Save the outputs to a new csv file
outputs.to_csv(os.path.join(os.getcwd(), "..", "birthweight-results", "descriptive-stats.csv"),
               index=False,                     # don't print indices to the output file
               float_format="%.3f")             # print values to three decimal places
```

You'll notice that we use a couple of Python packages in this script - `pandas` and `os`.
The `os` module is included by default with Python, but you may need to install `pandas` if you haven't got it set up already.
If you need to, you can install `pandas` using `pip` (Python's package manager) by running
```
pip install pandas
```

### Tracking our changes with `git`

With our file ready, let's now track it using our version control system, `git`.
We track changes in `git` via **commits**.
A commit is essentially a snapshot of a set of files at a moment in time.
A message and unique identifier (often called a SHA or hash) are attached to each commit.
You can think of a commit as a **saved unit of work**.
It's good practice to commit whenever a set of related changes are complete - and as our initial version of the analysis script certainly meets that criteria, it's time to commit our work.

Let's take a look at `git`'s current status by running
```
git status
```
You should see something along the lines of this output:
```
On branch master

No commits yet

Untracked files:
  (use "git add <file>..." to include in what will be committed)

        birthweight-descriptive-stats.py
```
We won't focus on branches in this tutorial (if you're curious, see [Chapter 3](https://git-scm.com/book/en/v2/Git-Branching-Branches-in-a-Nutshell) of the Pro Git book); the following sections of the output are more relevant to us.
As expected, we don't have any commits yet.
However, `git` has detected that a new file is present in the `birthweight-analysis` folder.
We need to let `git` know that it is supposed to track this file, which we do with the following command:
```
git add birthweight-descriptive-stats.py
```
If we run `git status` again, we can see that the output has changed:
```
On branch master

No commits yet

Changes to be committed:
  (use "git rm --cached <file>..." to unstage)

        new file:   birthweight-descriptive-stats.py
```
`git` has recognised that we've added a new file, and we can now commit that change.
Our commit will contain changes to all files listed in the `Changes to be committed:` section.
Let's now commit those changes (we use the `-m` option to pass a message to the `commit` command) and then inspect our commit.
```
git commit -m "Add first version of analysis script"
git log
```

The output of `git log` will show some details about the commit: the author, date, commit message and - importantly for our use of `catalogue` later on - the unique commit identifier.

### Checking the script

Now, let's do a trial run of the script to make sure everything works as expected before we move on.
```
python birthweight-descriptive-stats.py
```

Once it's done, we can have a look at our outputs.
We can either print the file out at the command line with
```
cat ../birthweight-results/descriptive-stats.csv
```
or by navigating to the `birthweight-results` folder in a file browser and opening the `descriptive-stats.csv` file from there.

### Using `catalogue`

Now, let's start using `catalogue` to track our results.
Later on, we'll start to make changes to different aspects of this example and we want to understand the impact of those changes as we proceed.

To start using `catalogue`, we need to specify the folders that contain our data and our code as we call the utility
```
catalogue engage --input_data ../birthweight-data --code .
```
As our current working directory is the `birthweight-analysis` folder, we give a relative path to the data folder and pass our current directory as the code folder.
We should receive the following output:
```
'catalogue engage' succeeded. Proceed with analysis
```
We can now run our analysis scripts, using whichever tools we like.
For our case, we run the Python script we wrote earlier.
```
python birthweight-descriptive-stats.py
```

Once our analysis is complete (which could involve several steps if we have a more complex pipeline), we can disengage the `catalogue` tool.
As before, we provide the location of our input data and code, and this time we also provide the location of our output files.
```
catalogue disengage --input_data ../birthweight-data --code . --output_data ../birthweight-results
```
Running the `disengage` command should provide some output:
```
NOTE we expect the timestamp hashes to differ.

hashes differ in 1 places:
===========================
timestamp

hashes match in 2 places:
==========================
input_data
code

hashes could not be compared in 1 places:
==========================================
../birthweight-results/descriptive-stats.csv
```

The **hashes** that the output refers to are mappings of the contents of the relevant files to a unique string.
If two files are the same, the hashes of those files will also be the same.
If the files differ, even by a single character, their hashes will be different.

The output from `catalogue disengage` utilises the hashes of the files that we provided as options to `catalogue engage` and `catalogue disengage`.
- `timestamp` is generated by `catalogue` itself - it records the time at which `engage` and `disengage` occurred. As these two commands can't be performed at exactly the same time, their hashes will always differ.
- Our input data and code did not change in the time between when `catalogue engage` and `catalogue disengage` were ran.
- Our results were generated while we were using the catalogue tool, so a before/after comparison cannot be performed.
The hashes themselves can be seen in the timestamped `.json` file in newly-generated `catalogue_results` folder.
You can open that file in a text editor, of view the contents with
```
cat catalogue_results/20200518-184447.json
```
Note that the exact name of your file will be different as it will have been generated at a different time.

This process is useful for making sure that we didn't unintentionally made changes to our input data or code as we ran our analysis pipeline.
When we run `catalogue engage`, the tool checks all changes to the code have been committed to our version control system.
This ensures that we have a record of the code that was run.
However, the real utility of `catalogue` becomes apparent when we re-run our analysis after making changes to the code.

### Modifying the analysis script

We'll now illustrate how `catalogue` can be used to highlight the effects changes to different parts of our analysis pipeline.
In our typical workflow, some changes will have knock-on effects:
- Changing our input data (e.g. moving from a trial dataset to the full one)
- Altering our analysis technique
- Saving more outputs from our pipeline

while others won't (or rather, shouldn't!):
- Refactoring our code for speed or clarity
- Reorganising our file structure

We'll now see how we can use `catalogue` to make sure that some simple changes to our pipeline have the expected effects.

#### Refactoring the code

Let's start with a small amount of refactoring.
In our analysis script, there is one command which prints a few entries of our dataset to the screen.
We'll now remove that statement (in a slightly contrived example of how to tidy up our code!).
Open up your `birthweight-descriptive-stats.py` file, and remove the `print()` statement (which should be on line 8).
Save the file and close your editor, then run
```
catalogue engage --input_data ../birthweight-data --code .
```
Unlike last time, you should see a warning message
```
Working directory contains uncommitted changes.
Do you want to stage and commit all changes? (y/[n])
```
We haven't committed our changes, so we have no record of what we've just done in our version control system.
If we type `y`, `catalogue` handles the add and commit process for us; alternatively, we can select `n` and run `git add` and `git commit` as we did earlier in this walkthrough to track our changes.
If you like, run `git status` and `git log` to see the latest commit, before running the command to engage `catalogue` again.

With `catalogue` now engaged, we can run our analysis with
```
python birthweight-descriptive-stats.py
```
We won't see the output to the screen this time, but no other changes should have occurred.
If we disengage with
```
catalogue disengage --input_data ../birthweight-data --code . --output_data ../birthweight-results
```
we get the same output as we did the previous time.

Now, let's compare our outputs on the two occasions.
The file that contains our results is overwritten each time we call our anaysis script, but we can still use `catalogue` to compare the results.
We can see what `catalogue` has recorded by listing the files in the `catalogue_results` directory.
```
ls catalogue_results
```
Two `.json` files will be listed, with different timestamps - these are from the two occasions we have used `catalogue`.
We can compare the contents of the two files with
```
catalogue compare catalogue_results/20200518-184447.json catalogue_results/20200519-141323.json
```
Note that the timestamps used in your filenames will be different.
The comparison should yield
```
NOTE we expect the timestamp hashes to differ.

hashes differ in 2 places:
===========================
timestamp
code

hashes match in 2 places:
==========================
input_data
../birthweight-results/descriptive-stats.csv

hashes could not be compared in 0 places:
==========================================
```
In this case, we can see that our timestamp and code have changed between the two occasions on which we ran `catalogue`.
The timestamp is different due to the times at which we ran the tool, and we made the changes to the code ourselves.
The hashes of our input data folder (`birthweight-data`) and the files within our output data folder (`birthweight-results`) have not changed, giving us confidence that our small refactoring has not changed any of the functionality of our code.

#### Modifying the data

Let's now try a different case, by altering our input data slightly.
This might happen when we receive a new version of a data file.
We'll mimic this by adding a new record to the birthweight dataset.

Open up the data file (`birthweight-data/Birthweight_reduced_R.csv`), and add the following line to the end of the file:
```
2137,14,20,7.30,40,1,22,17,62,104,32,12,25,68,0,0,Normal
```
Then save the file.
We'll then run our pipeline using `catalogue` to track the files that are used and generated, and then compare with our previous run:
```
catalogue engage --input_data ../birthweight-data --code .
python birthweight-descriptive-stats.py
catalogue disengage --input_data ../birthweight-data --code . --output_data ../birthweight-results
catalogue compare catalogue_results/20200519-141323.json catalogue_results/20200519-173928.json
```
Again, noting that your timestamps will be different from those above (you can use `ls catalogue_results` to see the available timestamps).
The output will let us know where the differences in our pipeline arose:
```
NOTE we expect the timestamp hashes to differ.

hashes differ in 3 places:
===========================
timestamp
input_data
../birthweight-results/descriptive-stats.csv

hashes match in 1 places:
==========================
code

hashes could not be compared in 0 places:
==========================================
```
The output reports that our code is unchanged, and (most crucially) informs us that both our input data and our results files have changed.
If we were trying to track down why we were getting a different set of results, this report from `catalogue` would help us narrow it down to a change in the data as opposed to something having been changed in the code.

And with that, we've come to the end of our first example!
In this walkthrough, we've covered the main features of `catalogue` and shown how it can be used in a simple analysis pipeline.
We have discussed how it can be used to highlight changes in the data, code and outputs, but have only lightly touched on the many facets of reproducibility that often come up during analysis projects.
In our next example, we'll take a closer look at some of the more common challenges in making your project reproducible, and how `catalogue` can help in that process.
