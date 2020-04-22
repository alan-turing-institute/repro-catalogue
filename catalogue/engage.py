import catalogue as ct

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
    hash_dict = ct.construct_dict(args.input_data, args.code, args.output_data, timestamp)
    lock_match, messages = check_against_lock(hash_dict, lock_dict)
    if lock_match:
        # add engage timestamp to hash_dict
        hash_dict["timestamp"].update({"engage": lock_dict["timestamp"]})
        ct.store_hash(hash_dict)
