import traceback

from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA512


def sign_file(file_data, key_path, passphrase):
    try:
        private_key = open(key_path, "rb").read()
        rsa_key = RSA.importKey(private_key, passphrase=passphrase)
        signer = PKCS1_v1_5.new(rsa_key)
        digest = SHA512.new(file_data)

        if not signer.can_sign():
            raise Exception("La clé ne peut signer.")

        sign = signer.sign(digest)

        return sign

    except ValueError:
        traceback.print_exc()
        raise Exception("Passphrase invalide.")
    except Exception as e:
        traceback.print_exc()
        raise Exception("Erreur lors de la signature du fichier : %s" % e)
