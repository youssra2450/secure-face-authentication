import cv2
import pickle
import numpy as np
from deepface import DeepFace
import os

# =======================
# Déchiffrement automatique (une seule fois)
# =======================
if not os.path.exists("encodings_dec.pkl"):
    print(" Déchiffrement des données biométriques...")
    os.system("python decrypt_data.py")

ENCODINGS_FILE = "encodings_dec.pkl"
MODEL_NAME = "ArcFace"
THRESHOLD = 0.5

# --- CHARGER ENCODINGS ---
with open(ENCODINGS_FILE, "rb") as f:
    data = pickle.load(f)

print(" Encodings chargés avec succès !")

# calcul embedding moyen par personne
known_embeddings = {}
for person, embeddings in data.items():
    known_embeddings[person] = np.mean(np.array(embeddings), axis=0)

def cosine_distance(a, b):
    return 1 - np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def recognize_face(frame):
    identity = "Unknown"
    try:
        embedding = DeepFace.represent(frame, model_name=MODEL_NAME, enforce_detection=True)[0]["embedding"]
        embedding = np.array(embedding).flatten()

        min_dist = float("inf")
        for person, emb in known_embeddings.items():
            dist = cosine_distance(embedding, emb)
            if dist < min_dist:
                min_dist = dist
                identity = person if dist < THRESHOLD else "Unknown"
    except:
        pass
    return identity

# ================= MENU =================
print("\nChoisissez une option :")
print("1 - Webcam (caméra)")
print("2 - Vidéo MP4")
print("3 - Image (photo)")

choice = input("Votre choix (1/2/3) : ")

# ============ 1) WEBCAM ============
if choice == "1":
    cap = cv2.VideoCapture(0)
    print(" Webcam activée (q pour quitter)")

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        identity = recognize_face(frame)

        cv2.putText(frame, identity, (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2)
        cv2.imshow("Face Auth Secure", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

# ============ 2) VIDEO ============
elif choice == "2":
    video_path = input("Chemin de la vidéo MP4 : ")

    if not os.path.exists(video_path):
        print(" Vidéo introuvable !")
        exit()

    cap = cv2.VideoCapture(video_path)
    print(" Lecture vidéo...")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        identity = recognize_face(frame)

        cv2.putText(frame, identity, (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2)
        cv2.imshow("Face Auth Secure", frame)

        if cv2.waitKey(25) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

# ============ 3) IMAGE ============
elif choice == "3":
    image_path = input("Chemin de l'image : ")

    if not os.path.exists(image_path):
        print(" Image introuvable !")
        exit()

    frame = cv2.imread(image_path)
    identity = recognize_face(frame)

    cv2.putText(frame, identity, (30, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2)
    cv2.imshow("Face Auth Secure", frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

else:
    print("Choix invalide !")
