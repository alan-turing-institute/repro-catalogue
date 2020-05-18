# Getting started with `catalogue`

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
Inside that folder, we'll create two more.
One will contain the code, and the other will hold the data.
We'll now move into the `repro-catalogue-demo` folder and create the new folders there.
```
cd repro-catalogue-demo
mkdir birthweight-data
mkdir birthweight-analysis
```

Why two separate folders?
Our analysis **code** will be worked on regularly, and all changes to it should therefore be tracked using a version control system.
On the other hand, our **data** will not change (or only be changed very rarely).
The code that we write will depend on the structure of the dataset, but not on the exact values within it.
We can therefore treat changes to our code and data **independently**, and the separated folders help us to achieve this.

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

Now, let's do a trial run of the script.
```
python birthweight-descriptive-stats.py
```

Once it's done, we can have a look at out outputs.
We can either print the file out at the command line with
```
cat ../birthweight-results/descriptive-stats.csv
```
or by navigating to the `birthweight-results` folder in a file browser and opening the `descriptive-stats.csv` file from there.

### Using `catalogue`

### Modifying the analysis script
