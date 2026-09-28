from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

ENC_FILE = "encodings.enc"
KEY_FILE = "aes_key.enc"
OUTPUT_FILE = "encodings_dec.pkl"

print(" Déchiffrement du fichier biométrique...")

# 1) Charger clé privée RSA
with open("private_key.pem", "rb") as f:
    private_key = serialization.load_pem_private_key(f.read(), password=None)

# 2) Lire clé AES chiffrée
with open(KEY_FILE, "rb") as f:
    encrypted_key = f.read()

aes_key = private_key.decrypt(
    encrypted_key,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

# 3) Lire fichier chiffré
with open(ENC_FILE, "rb") as f:
    encrypted_data = f.read()

iv = encrypted_data[:16]
ciphertext = encrypted_data[16:]

cipher = Cipher(algorithms.AES(aes_key), modes.CFB(iv), backend=default_backend())
decryptor = cipher.decryptor()
data_bytes = decryptor.update(ciphertext) + decryptor.finalize()

# 4) Sauvegarder fichier déchiffré
with open(OUTPUT_FILE, "wb") as f:
    f.write(data_bytes)

print(" encodings_dec.pkl déchiffré avec succès !")
