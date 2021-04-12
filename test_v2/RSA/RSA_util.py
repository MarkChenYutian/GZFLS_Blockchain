"""
By Mark, 2021/3/12
Provide RSA Service

Reference: https://www.jianshu.com/p/7a4645691c68.
**WARNING: The Crypto Code provided on this url have defect !**


It is already known that the Python Crypto module is hard to install in some situations,
if you have problems installing Crypto Module, perhaps this url will help.
https://stackoverflow.com/questions/19623267/importerror-no-module-named-crypto-cipher
"""
from Crypto.PublicKey import RSA
from Crypto.PublicKey.RSA import RsaKey
from Crypto.Cipher import PKCS1_v1_5 as PKCS1_v1_5_cipher
from hashlib import sha3_256
import Crypto
import base64
import os


def generateRSAKey(bits=1024, privateKeyPath="./RSA/PrivateKey.pem", publicKeyPath="./RSA/PublicKey.pem") -> None:
    """
    Generate Keys in ./RSA folder
    :param bits: The length of RSA Key
    :param privateKeyPath: The path of private key file
    :param publicKeyPath: The path of public key file
    :return: None
    """
    privateKey = RSA.generate(bits)
    with open(privateKeyPath, "wb") as privateKey_file:
        privateKey_file.write(privateKey.export_key())
    with open(publicKeyPath, "wb") as pubkey_file:
        pubkey_file.write(privateKey.publickey().export_key())


def loadKeys(pubKeyPath="./RSA/PublicKey.pem", privateKeyPath="./RSA/PrivateKey.pem") -> tuple:
    """
    Load Keys from file.
    :param pubKeyPath: The path of public key, can be None
    :param privateKeyPath: The path of private key, can be None
    :return: (publicKey, privateKey). If the file path is none, then returned key will be None
    """
    publicKey = RSA.import_key(open(pubKeyPath).read()) if pubKeyPath is not None else None
    privateKey = RSA.import_key(open(privateKeyPath).read()) if privateKeyPath is not None else None
    return publicKey, privateKey


def getMaxBlockSize(rsaKey: RsaKey, isEncrypt=True) -> int:
    """
    Calculate the Maximum Block Size of RSA Process
    :param rsaKey: The RSA Key used to encrypt / decrypt message
    :param isEncrypt: Whether the message will be encrypted or decrypted. If decrypt, isEncrypt=False.
    :return: the maximum info in a single block.
    """
    blockSize = Crypto.Util.number.size(rsaKey.n) / 8
    reservedBlockSize = 11 if isEncrypt else 0  # No reserved size of decryption process
    maxSize = blockSize - reservedBlockSize
    return int(maxSize)


def encrypt(rsaKey: RsaKey, message: str) -> str:
    """
    Encrypt Result using given rsa Key
    :param rsaKey: The RSA Key used to encrypt Message
    :param message: The message you want to encrypt (must be string)
    :return: base 64 encryption result
    """
    message = message.encode("ascii")
    encryptRes = b""
    maxBlockSize = getMaxBlockSize(rsaKey=rsaKey)
    cipher = PKCS1_v1_5_cipher.new(rsaKey)
    while message:
        input_data, message = message[:maxBlockSize], message[maxBlockSize:]  # Get a block of input data
        out_data = cipher.encrypt(input_data)
        encryptRes += out_data
    encryptRes = base64.b64encode(encryptRes)
    return encryptRes.decode("ascii")


def decrypt(rsaKey: RsaKey, message: str) -> str:
    message = message.encode("ascii")
    decryptRes = b""
    maxBlockSize = getMaxBlockSize(rsaKey=rsaKey, isEncrypt=False)
    message = base64.b64decode(message)
    cipher = PKCS1_v1_5_cipher.new(rsaKey)
    while message:
        input_data, message = message[:maxBlockSize], message[maxBlockSize:]
        # My IDE show warning on the line below, but kwarg sentinel must be included here or Exception will be raised
        out_data = cipher.decrypt(input_data, sentinel="")
        decryptRes += out_data
    return decryptRes.decode("ascii")


def signSignature(rsaKey: RsaKey, message: str) -> str:
    msgHash = sha3_256(message.encode("ascii")).hexdigest()
    return encrypt(rsaKey, msgHash)


def verifySignature(rsaKey: RsaKey, signatureString: str, expectContent: str) -> bool:
    sigContent = decrypt(rsaKey, signatureString)
    return sigContent == sha3_256(expectContent.encode("ascii")).hexdigest()


def loadKeyFromString(rsaKeyString: str) -> RsaKey:
    """
    :param rsaKeyString: Load an RsaKey object from the RSA Key String.
    :return: RsaKey loaded from String
    """
    return RSA.import_key(rsaKeyString)


if __name__ == "__main__":
    print("Current Working Directory: ", end="")
    os.chdir("./..")
    print(os.getcwd() + "\n--------------")
    pubKey, privateKey = loadKeys()
    signature = signSignature(privateKey, "This is a Signature Test.")
    print(verifySignature(pubKey, signature, "This is a Signature Test"))
