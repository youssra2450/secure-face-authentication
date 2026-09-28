import cv2
import pickle
import numpy as np
from deepface import DeepFace
import os

# --- CONFIG ---
OUTPUT_FILE = "encodings.pkl"
MODEL_NAME = "ArcFace"
FRAME_STEP = 10  # prendre 1 frame chaque 10 frames

PERSON_NAME = input("Nom de la personne : ").strip()

print("\nChoisissez la source :")
print("1 - Vidéo MP4")
print("2 - Caméra (Webcam)")
choice = input("Votre choix (1/2) : ").strip()

encodings = []

# ================== MODE VIDEO ==================
if choice == "1":
    VIDEO_PATH = input("Chemin de la vidéo (ex: personne.mp4) : ").strip()

    if not os.path.exists(VIDEO_PATH):
        print(" Vidéo introuvable !")
        exit()

    cap = cv2.VideoCapture(VIDEO_PATH)
    print(" Extraction des visages depuis la vidéo...")

# ================== MODE CAMERA ==================
elif choice == "2":
    cap = cv2.VideoCapture(0)
    print("📷 Enregistrement via la caméra...")
    print("👉 Appuyez sur 'q' pour arrêter l'enregistrement")

else:
    print(" Choix invalide !")
    exit()

frame_id = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_id += 1

    # prendre 1 frame sur FRAME_STEP
    if frame_id % FRAME_STEP != 0:
        continue

    try:
        embedding = DeepFace.represent(
            img_path=frame,
            model_name=MODEL_NAME,
            enforce_detection=True
        )[0]["embedding"]

        embedding = np.array(embedding).flatten()
        encodings.append(embedding)
        print(f"Embedding extrait ({len(encodings)})")

    except:
        print(" Aucun visage détecté sur cette frame")

    # affichage caméra (seulement en mode webcam)
    if choice == "2":
        cv2.imshow("Capture visage", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

cap.release()
cv2.destroyAllWindows()

print(f"\n Total embeddings extraits : {len(encodings)}")

# --- SAUVEGARDE ---
if os.path.exists(OUTPUT_FILE):
    with open(OUTPUT_FILE, "rb") as f:
        data = pickle.load(f)
else:
    data = {}

# ajouter la personne (sans écraser les autres)
data[PERSON_NAME] = encodings

with open(OUTPUT_FILE, "wb") as f:
    pickle.dump(data, f)

print(f" Données sauvegardées pour {PERSON_NAME} dans {OUTPUT_FILE}")
