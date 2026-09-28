from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

INPUT_FILE = "encodings.pkl"

print(" Chiffrement du fichier biométrique...")

# 1) Charger clé publique RSA
with open("public_key.pem", "rb") as f:
    public_key = serialization.load_pem_public_key(f.read())

# 2) Lire encodings.pkl
with open(INPUT_FILE, "rb") as f:
    data_bytes = f.read()

# 3) Générer clé AES + IV
aes_key = os.urandom(32)  # 256 bits
iv = os.urandom(16)

cipher = Cipher(algorithms.AES(aes_key), modes.CFB(iv), backend=default_backend())
encryptor = cipher.encryptor()
encrypted_data = encryptor.update(data_bytes) + encryptor.finalize()

# 4) Sauvegarder fichier chiffré
with open("encodings.enc", "wb") as f:
    f.write(iv + encrypted_data)

# 5) Chiffrer la clé AES avec RSA
encrypted_key = public_key.encrypt(
    aes_key,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

with open("aes_key.enc", "wb") as f:
    f.write(encrypted_key)

print(" encodings.pkl chiffré !")
print(" Fichiers : encodings.enc + aes_key.enc")
