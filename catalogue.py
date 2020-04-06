import os
import hashlib

from datetime import


def hash_file(filepath, m = hashlib.sha512()):
    with open(filename, 'rb') as f:
        # The following construction lets us read f in chunks,
        # instead of loading an arbitrary file in all at once.
        while True:
            b = f.read(2**10)
            if not b:
                break
            m.update(b)
    return m


def hash_dir_walk(folder):
    hashes = {}
    for path, directories, files in os.walk(folder):
        for file in sorted(files):
            hashes[os.path.join(*directories, file)] = hash_file(
                os.path.join(path, file)).digest()
        for dir in sorted(directories):
            hashes.update(hash_folder(os.path.join(path, dir)))
        break
    return hashes


def hash_dir_full(folder, m = hashlib.sha512()):
    for path, directories, files in os.walk(folder):
        for file in sorted(files):
            m = hash_file(os.path.join(path, file))
        for dir in sorted(directories):
            m = hash_dir_full(os.path.join(path, dir), m)
    return m


def hash_output(output_dirs):
    hashes = []
    for folder in output_dirs:
        hashes.append({folder : hash_dir_walk(folder).digest()})
    return hashes


def hash_input(input_dir):
    return {input_dir : hash_dir_full(input_dir)}


def hash_code(code_dir):
    return {code_dir : hash_dir_full(code_dir).digest()}  


def construct_dict(input_dir, code_dir, output_dirs, timestamp):
    return {
        "timestamp" : {"disengage" : timestamp}
        "input_data" : hash_input(input_dir),
        "output_data" : hash_output(output_dir),
        "code" : hash_code(code_dir)}


def store_hash(hash_dict, store, timestamp):
    with open(
            os.path.join(os.path.dirname(store), "{}.json".format(timestamp),
            "w") as f:
        json.dump(hash_dict, f)


def load_hash(filepath):
    with open(filepath, "r") as f:
        return json.load(f)
            
            
