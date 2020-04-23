import catalogue as ct


def git_query():
    """
    Checks the git status of the code directory (hence the args.code argument)
    - if clean, returns true
    - if there are uncommitted changes, ask for the users input
        offer to stage and commit all and continues (returning True)
        or to quit (returning False)
    """
    pass


def lock(args):
    """
    creates .loc file (json structure) (requires hashing inputs)
    Parameters:
        input_data, code, store (where place file?), timestamp
    """
    pass


def unlock(args):
    """
    reads .loc file and deletes it
    Parameters:
        args.input_data, args.code, store (location of file?)
    Returns file contents (dictionary)
    """
    pass


def construct_dict(args):
    """
    Params:
        input_data, code, output_data, timestamp
    Returns:
        dict with hashes of all inputs
    """
    pass


def check_against_lock():
    """
    Compares two dictionaries (latest hash vs. lock hash)
    Paremeters:
        dictionary1, dictionary2
    returns: boolean (lock match), str (messages)
    """
    pass


def engage(args):
    timestamp = ...
    if git_query(args.code):
        try:
            lock(args.input_data, args.code, store, timestamp)
        except:
            print("Already engaged. To disengage run 'catalogue disengage...'")
            print("See 'catalogue disengage --help' for details")
        print("'catalogue engage' succeeded. Proceed with analysis")



def disengage(args):
    timestamp = ...
    try:
        lock_dict = unlock(args.input_data, args.code, store)
    except FileNotFoundError:
        print("Not currently engaged. To engage run 'catalogue engage...'")
        print("See 'catalogue engage --help' for details")
    hash_dict = construct_dict(args.input_data, args.code, args.output_data, timestamp)
    lock_match, messages = check_against_lock(hash_dict, lock_dict)
    if lock_match:
        # add engage timestamp to hash_dict
        hash_dict["timestamp"].update({"engage": lock_dict["timestamp"]})
        ct.store_hash(hash_dict)
