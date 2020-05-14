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
We'll explain the necessary commands as we go along, and you can check out chapters 1-3 of the [Software Carpentry Unix shell lesson](http://swcarpentry.github.io/shell-novice/) if you'd like more details on any of the commands we use.

And now, let's walk through our first example!

## Our first example