\# Secure Face Authentication



Système d'authentification biométrique par reconnaissance faciale, avec chiffrement des données sensibles via RSA-2048 et AES-256.



\---



\## Présentation



Ce projet implémente un système complet d'authentification par reconnaissance faciale. Les encodages biométriques sont chiffrés au repos à l'aide d'un chiffrement symétrique (AES-256), dont la clé est elle-même protégée par un chiffrement asymétrique (RSA-2048). L'objectif est de garantir la confidentialité des données biométriques et de la clé de chiffrement.



\---



\## Fonctionnalités



\- Reconnaissance faciale via DeepFace (modèle ArcFace)

\- Enregistrement de plusieurs personnes (vidéo MP4 ou webcam)

\- Chiffrement AES-256 des encodages biométriques

\- Chiffrement RSA-2048 de la clé AES

\- Authentification en temps réel (webcam, vidéo, image)

\- Protection des fichiers sensibles via `.gitignore`



\---



\## Architecture du projet



| Fichier | Rôle |

|---|---|

| `rsa\_keys.py` | Génération du couple de clés RSA (privée / publique) |

| `test.py` | Enregistrement des visages et extraction des encodages |

| `encrypt\_data.py` | Chiffrement du fichier biométrique (AES + RSA) |

| `decrypt\_data.py` | Déchiffrement du fichier biométrique |

| `authentif\_secure.py` | Application principale d'authentification |

| `encodings.pkl` | Fichier des encodages biométriques (non versionné) |

| `encodings.enc` | Fichier biométrique chiffré (non versionné) |

| `aes\_key.enc` | Clé AES chiffrée par RSA (non versionné) |

| `private\_key.pem` | Clé privée RSA (non versionnée) |

| `public\_key.pem` | Clé publique RSA (non versionnée) |



\---



\## Technologies utilisées



\- Python 3

\- DeepFace — reconnaissance faciale (modèle ArcFace)

\- OpenCV — capture et traitement vidéo

\- Cryptography — chiffrement RSA et AES

\- NumPy — manipulation des vecteurs d'encodage

\- Pickle — sérialisation des données



\---



\## Installation



\### Prérequis



\- Python 3.8 ou supérieur

\- pip



\### Étapes



1\. Cloner le dépôt :



```bash

git clone https://github.com/youssra2450/secure-face-authentication.git

cd secure-face-authentication

