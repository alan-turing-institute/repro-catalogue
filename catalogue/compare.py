from . import catalogue as ct

def compare(*args):
    """
    TODO: IMPLEMENT!
    """
    pass

# def checkhashes(args):
#     pass

def check_hashes(args):
    get_h = lambda x: x.values()[0]
    hash_dict = ct.load_hash(args.filepath)
    failures = []
    matches = []
    differs = []
    if args.input_data:
        try:
            input1 = get_h(hash_dict["input_data"])
        except:
            failures.append("input_data")
        if get_h(ct.hash_input(args.input_data)) == input1:
            matches.append("input_data")
        else:
            differs.append("input_data")
    if args.code:
        try:
            code1 = get_h(hash_dict["code"])
        except:
            failures.append("code")
        if ct.get_h(ct.hash_code(args.code)) == code1:
            matches.append("code")
        else:
            differs.append("code")
    if args.output_data:
        try:
            output1 = hash_dict["output_data"]
        except:
            failures.append("output_data")
        output2 = hash_output(args.output_data)
        n = min(len(output1, output2))
        for i in range(n):
            a, b, c = ct.compare_folders(output1[i], output2[i])
            failures.extend(a)
            matches.extend(b)
            differs.extend(c)
        else:
            differs.append("timestamp")
    return "\n".join(
        "results differ in {} places:".format(len(differs)),
        "===========================",
        *differs,
        "results match in {} places:".format(len(matches)),
        "==========================",
        *matches,
        "results could not be compared in {} places:".format(len(failures)),
        "==========================================",
        *failures
    )
