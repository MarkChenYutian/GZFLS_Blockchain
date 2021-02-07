import hashlib
import pickle

def hashObject(inObject):
    return hashlib.sha3_256(pickle.dumps(inObject)).hexdigest()