# repro-catalogue
A tool to catalogue versions of data, code and results to check the reproducibility of your research project 

## The situation
We are working on a dataset that is being regularly updated. Any scientific results we produce need to reliably record the version of the input data. 
We are also regularly tweaking our code, so we need to track what has changed between runs.
Finally, maybe our results change and we don't know why. We need to know: did the code change? did the data change?

## The solution
A command line tool `catalogue` that can be sandwiched around an analysis to record a hash value of the dataset that was used; the code that was run; and the outputs that were produced. 

What does this mean?
On the central sever we have a data repository
```
├── Data folder/
│   ├── OMOP database release 1/
│   ├── OMOP database release 2/
⋮    ⋮
│   └── version index
```

Elsewhere, in our user directory, perhaps on another computer, things look like this.

```
├── latest data/
├── latest code/
├── results/
│   ├── old results using old inputs 1/ 
│   ├── old results using old inputs 2/ 
│   └── latest results using latest code/ 
├── results versioning directory/
│   ├── TIMESTAMP1.json
│   ├── TIMESTAMP2.json
│   ├── TIMESTAMP3.json
│   └── TIMESTAMP4.json
```

We've just made some minor tweaks to our code and now we want to run our analysis. Before we start running any of the script in our code folder, we run
`catalogue engage --input_data latest\ data --code latest\ code`

This will do a series of things. First it will check that the git working tree in our code folder is clean. If not it will give users a choice:
```
catalogue has detected uncomitted changes in *latest\ results*
Either allow catalogue to stage and commit all changes, or exit
Commit all changes? (y/n)
```
If we choose to proceed `catalogue` will stage and commit all changes in the code directory. Next it will create a temporary file `results versioning directory/.lock` in json format.

```json
{
"timestamp" : <timestamp (of catalogue engage)>
"input_data": {
     ".../latest data/" : <hash of directory>
     }
"code" : {
     ".../latest code": [
         <hash of directory>,
         <latest git commit hash>
         ]
     }
}
```

Now we run whatever we need to perform our analysis.
Immediately after finishing our this we would run our `catalogue` tool to version these results
`catalogue disengage --input_data latest\ data --output_data results/latest\ results  --code latest\ code`

This starts by reading in and deleting the `.lock` file we created earlier. It checks that the `input_data` and `code` hashes match the hashes in `.lock`. If they do, it will take hashes of the files in `output_data` and might produce the following file

```json
// TIMESTAMP5.json
{
"timestamp" : {
     "engage": <timestamp (of .lock)>, 
     "disengage": <timestamp (new)>
     }
"input_data": {
     ".../latest data/" : <hash of directory>
     }
"output_data": { 
     "directory" : {
         "...results/latest results/":{
             "summary.txt": <hash of file>,
             "output.csv": <hash of file>,
             "metadata.json": <hash of file>
             }
         }
     },
"code" : {
     ".../latest code": [
         <hash of directory>,
         <git commit hash>
         ]
     }
}
```

## What can we do with all this?
#### compare one set of results to another:

Let's suppose that between timestamp4 and timestamp5 we modified the code to output a file `summary.txt`, but that otherwise nothing has changed. We would like to check that our file `.../output.csv` hasn't changed but oops! We've just overwritten it. Luckily we can compare to the json at timestamp4

`catalogue compare latest_results_TIMESTAMP4.json latest_results_TIMESTAMP5.json`

Let us also suppose that the metadata.json output includes a timestamp. The diff we would expect would look something like this
```
comparing latest_results_TIMESTAMP4.json 
to latest_results_TIMESTAMP5.json

results differ in *3* places:
=============================
- timestamp
- code version
- output_data :
    - .../metadata.json

results matched in *2* places:
==============================
- input_data 
- output_data :
    - .../output.csv

results could not be compared in *1* places: 
============================================
- output_data : 
    - .../summary.text
```
Of course this is what we *want*. We might find that our `output.csv` file *had* changed- and these hashes alone would do nothing to help us recover timestamp4 version, but they are enough to inform us of the problem, and importantly they do this without us having to permanently store the output of every analysis we run.

#### Share outputs
I've received a zip file of results from a colleague. They have also sent me their hash json.
If I have doubts to my colleague's ability to keep their data in order I can use `catalogue` to check that this json is correct for these output files.
`catalogue check_hashes --output_data islas_results/ --hashes islashashes.json`

```
Checking output_data
results differ in *0* places:
=============================

results matched in *2* places:
==============================
- output_data :
    - islasresults/analysis.csv
    - islasresults/metadata.txt
    
results could not be compared in *1* places:
============================================
- output_data :
    - islasresults/luna.gif
```
There doesn't seem to be a problem, although a dog pic seems to have ended up in this zip folder by mistake.
Now I want to check that we are working from the same input data.
`catalogue check_hashes --input_data latest_data/ --hashes islashashes.json`

```
Checking input_data
results differ in *1* places:
=============================
- input_data

results matched in *0* places:
==============================
```
Clearly the input data I have in `/latest_data` is not the data that Isla was using. But what was? we can look at the archive of past releases to determine which one of them hashes to the right value. If none of them do we will have to inform Isla that she may have been using incorrect data. 
(the process of finding out what data Isla used could be smoothed by the releasers maintaining a hash to version index)

#### Archiving results

Similar to the above. We may archive some results and lose track of the context in which they were produced. If we keep hold of the json we can track which version of the data they used. Even if the results aren't stored anywhere near the json file, if we have both, we can always hash the results again and figure out which json they match to. 

(Maybe the jsons should be automatically pushed to a central repo on creation. In this case they would need a userid attached as timestamps wouldn't be enough to distinguish them.)

## Why do we hash by file in the output directory but by directory for code and input data?

My reasoning is this:
* The versioning of the input data should be taken care of higher up: by the people who are releasing it - our hashing here is a mechanism to ensure we are using the data we think we are using. E.g our response to any inconsistency in the data hash with the one we are expecting should be to throw our results away and to repull the input data from the releasers.
    * Discussions with kirstie suggest that researchers may be each using particular subsets of the data, in which case that is the level at which we should be hashing.
* In contrast we do need this granularity for the output data. If changes in our code cause unexpected changes, knowing which files they are changing can help us to debug. Furthermore when changes in our code cause *expected* changes we must be able to check that only the files we expect to change change.
* Finally, the code. I could go either way on this. Git is a much more sophisticated tool for version control that is specifically engineered towards code development. People should use Git (or a similar equivalent) whenever possible. I want to work with the possibility of researchers who do not use git in mind, but I don't want to encourage them to use a significantly underengineered tool like this one for their code versioning. If people were sufficiently comfortable with git, we could ask them to commit all their code before running and then store the latest commit hash. 
    * It seems like using git commit hashes is the plan going forward

## Intermediary data processing.
We have some data coming from the releasers, in a probably unfamiliar format. We're almost certainly going to have to do some preprocessing steps. Ideally all of this preprocessing would be run automatically in synchrony with the rest of our code. In that case we consider it output data, and it should be contained in our `output_data` folder.

## Randomness
Hashing tells you whether something is the same, or different. It cannot tell you if something is almost the same. If your analysis is non-deterministic, you be getting a different hash every time. To deal with this, I recommend setting a random seed. Whatever language you're using should be able to provide you with documentation on how to do this.

## Which hash function should we use?
sha 512? I'm not an expert on the security of hash functions, is there any official guidance?

## Ignoring files
It's no help to hash files if we don't care about them changing. A good example of a file we wouldn't want to track is a `.git` file. We could consider a couple of ways to ignore files
* Passing a `--ignore` flag to `catalogue`
* Maintaining some kind of `.catalogueignore` config file within each directory just as you would for Git
* automatically ignoring any `.` files

## What happens if the hashes in .lock don't match the new hashes?
I think we should record this discrepancy in the json file and inform the command line user.

## Running `catalogue engage` and `catalogue disengage` in the wrong order
`catalogue disengage` will check that a `.lock` file exists. If it doesn't it will warn
```
Oops looks like you're already disengaged
To engage, run "catalogue engage..."
```
`catalogue engage` will check that a `.lock` file does *not* exist. If it does, it will warn
```
Oops, looks like you're still engaged
To disengage rin "catalogue disengage..."
```

## "cheating"
It is possible under this system for a researcher to fiddle around with their code, fiddle around with their outputs ad nauseam, and then only realise at the end that they haven't been using catalogue. They can then run 
```
catalogue engage ...
catalogue disengage ...
```
one ofter the other. Is this a problem?
The system I'm proposing here is designed more around helping researchers track their work, rather than forcing them to work in a particular way, so I've been considering the possibility of this sort of "cheating" to be a feature rather than a bug. 
If people want to prevent this though, I'm sure we can figure something out. So far the only ideas I have to prevent this involve toggling permissions on the outputs/code folders. 

## Further possibilities
It would be possible to keep a `.unlock` file inside our versioning directory. This could record the hash of the output_data at time of the last `catalogue disengage` so that each  time we run `catalogue engage` it checks whether the outputs have been changed during the "unlocked" phase. I leave it up to somebody who knows more about the sorts of analysis being done to decide whether this will be a help or a hindrance
