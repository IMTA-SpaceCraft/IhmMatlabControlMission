import re
import time
import os
import serial

# Configuration du port série (adaptable selon matériel)
SERIAL_PORT = "COM1"  # Sous Windows : "COM1", sous Linux/Mac : "/dev/ttyS0"
BAUD_RATE = 115200  # À ajuster si besoin

# Chemin du fichier .dat
file_path = "renseigner\\le\\chemin\\du\\fichier\\.dat"

# Initialisation du port série
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    print(f"Port série {SERIAL_PORT} ouvert à {BAUD_RATE} bauds.")
except serial.SerialException as e:
    print(f"Impossible d'ouvrir le port série : {e}")
    ser = None  # Désactiver l'envoi si le port est indisponible

def extract_last_frame(data):
    """Extrait la dernière trame complète du texte."""
    pattern = r"TT[-]+(\d{2}h\d{2}m\d{2}s,[^;]+);"
    matches = re.findall(pattern, data)
    
    if matches:
        last_frame = matches[-1] + ";"  # Ajouter le ';' final
        return last_frame
    return None

def read_new_data():
    """Lit le fichier sans bloquer l'écriture par un autre programme."""
    if not os.path.exists(file_path):
        print(f"Fichier introuvable : {file_path}")
        return None

    try:
        with open(file_path, "rb") as f:
            data = f.read().decode("utf-8", errors="ignore")  # Lire et ignorer erreurs d'encodage
        return data
    except Exception as e:
        print(f"Erreur de lecture : {e}")
        return None

while True:
    content = read_new_data()
    
    if content:
        last_frame = extract_last_frame(content)
        if last_frame:
            print("Dernière trame extraite :")
            print(last_frame)

            # Envoi sur le port série si disponible
            if ser and ser.is_open:
                try:
                    ser.write((last_frame + "\n").encode("utf-8"))
                    print("Trame envoyée sur COM1")
                except Exception as e:
                    print(f"Erreur lors de l'envoi série : {e}")
        else:
            print("Aucune trame trouvée.")
    
    time.sleep(30)  # Attendre 30 secondes avant la prochaine lecture
