.. repro-catalogue documentation master file, created by
   sphinx-quickstart on Mon May 18 14:32:18 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to repro-catalogue's documentation!
===========================================

Research projects are frequently updated - new data are added, and the code undergoes regular changes. Under these circumstances, it's easy to store results, yet lose track of the context in which they were produced.

To ensure reproducibility of any scientific results we need to reliably record:

- what input data was used |:floppy_disk:|
- what code was run |:desktop_computer:|
- what outputs were produced |:chart_with_upwards_trend:|

The `catalogue` tool aids reproducibility by saving **hash values** of the input data and the results, along with the **git commit hash** of the code used to generate those results. The `catalogue` command line interface then allows the user to easily compare the hash values from different occasions on which the analysis was run so that changes to the input data, code and results can be identified and the impact on reproducibility can be understood.

**Hash functions** map arbitrary sized data to a binary "word" of a fixed length. The mapping is deterministic and the generated hash values are (for all practical purposes) unique. This means that hashing the same file (or a directory of files) will always produce the same value unless something in the files has changed, in which case the hash function would produce a new value. Because the hash value of a given input is unique, comparing hash values is a quick and easy way to check whether two files are the same.


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   2.getting_started
   3.commands_and_usage
   example_use
   example
   FAQs
   6.contributing



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
