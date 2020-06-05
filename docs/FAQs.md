# FAQs

## Running in the wrong order

The commands `catalogue engage` and `catalogue disengage` are meant to be run in that order.

The `catalogue engage` command will check that a `.lock` file does *not* exist. If it does, it will warn:
```
Already engaged (.lock file exists). To disengage run 'catalogue disengage...
See 'catalogue disengage --help' for details
```

The `catalogue disengage` command will check that a `.lock` file exists. If it doesn't, it will warn:
```
Not currently engaged (could not find .lock file). To engage run 'catalogue engage...
See 'catalogue engage --help' for details
```

## Intermediary data processing

It is likely that the analysis includes some preprocessing steps. Ideally all of this preprocessing would be run automatically in synchrony with the rest of our code. In that case we consider it output data, and it should be contained in the `output_data` folder.

## Randomness

Comparing two hashes tells you whether the hashed items are the same or different. This process cannot tell you if something is almost the same. If your analysis is non-deterministic, you will get a different hash every time.

There are several ways by which an analysis can be non-deterministic. One of the most common is the user of random numbers.
To deal with this, we recommend setting a random seed. Whatever language you're using should be able to provide you with documentation on how to do this - see, for example, the documentation for [Python](https://docs.python.org/3/library/random.html#random.seed).

Hashing tells you whether something is the same, or different. It cannot tell you if something is almost the same. If your analysis is non-deterministic, you will be getting a different hash every time. To deal with this, we recommend setting a random seed. Whatever language you're using should be able to provide you with documentation on how to do this.
