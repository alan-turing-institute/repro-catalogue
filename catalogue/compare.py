from . import catalogue as ct

def compare(*args):
    """
    TODO: IMPLEMENT!
    """
    pass

def check_hashes(args):
    pass

def compare_hashes(hash_dict_1, hash_dict_2):
    """
    Compare two hash dictionaries

    Compare two hash dictionaries. Returns a string summarizing the matches (when two hashes are
    identical), differences (when a hash has been computed for the same entity twice and they
    are different), and failures (when an entry only exists in one of the two hash dictionaries).

    Parameters
    ----------
    hash_dict_1: dict { str : dict }
        First hash dictionary
    hash_dict_2: dict { str : dict }
        Second has dictionary

    Returns
    -------
    str
    """

    get_h = lambda x: list(x.values())[0]
    failures = []
    matches = []
    differs = []

    for key in ["timestamp", "input_data", "code"]:
        try:
            entry_1 = get_h(hash_dict_1[key])
            entry_2 = get_h(hash_dict_2[key])
        except KeyError:
            failures.append(key)

        if entry_1 == entry_2:
            matches.append(key)
        else:
            differs.append(key)

    try:
        output_1 = get_h(hash_dict_1["output_data"])
    except KeyError:
        output_1 = None

    try:
        output_2 = get_h(hash_dict_2["output_data"])
    except KeyError:
        output_2 = None

    # if one or both accesses failed, append to failures
    if output_1 is None and output_2 is None:
        failures.append("output_data")
    elif output_1 is None:
        failures.extend(output_2.keys())
    elif output_2 is None:
        failures.extend(output_1.keys())
    else:
        # both accesses succeeded, check each unique file
        all_outputs = list(output_1.keys() | output_2.keys()) # union of two dict_keys objects converted to list

        for out_file in all_outputs:
            try:
                if output_1[out_file] == output_2[out_file]:
                    matches.append(out_file)
                else:
                    differs.append(out_file)
            except KeyError:
                failures.append(out_file)

    return "\n".join([
        "results differ in {} places:".format(len(differs)),
        "===========================",
        *differs,
        "results match in {} places:".format(len(matches)),
        "==========================",
        *matches,
        "results could not be compared in {} places:".format(len(failures)),
        "==========================================",
        *failures
    ])