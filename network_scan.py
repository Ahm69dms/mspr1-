import nmap
import tkinter as tk
from tkinter import ttk, messagebox
import re

# Fonction pour valider l'adresse IP ou la plage d'adresses IP
def valider_ip(ip_range):
    # Vérifie si l'entrée est une plage d'IP valide (ex: 192.168.0.0/24)
    pattern = r"(\d{1,3}\.){3}\d{1,3}/\d{1,2}"  # Regex pour CIDR
    if re.match(pattern, ip_range):
        return True
    # Vérifie si c'est une seule IP valide (ex: 192.168.0.1)
    pattern_ip = r"(\d{1,3}\.){3}\d{1,3}"
    if re.match(pattern_ip, ip_range):
        return True
    return False

# Fonction pour scanner le réseau
def scanner_reseau():
    ip_range = entry_ip.get()
    # Validation de l'entrée IP
    if not valider_ip(ip_range):
        messagebox.showerror("Erreur", "Format d'IP invalide, veuillez entrer une IP ou une plage d'IP correcte.")
        return
    
    scanner = nmap.PortScanner()
    try:
        result = scanner.scan(hosts=ip_range, arguments='-sn')  # -sn pour un scan de découverte de hôtes
        afficher_resultats(result)
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur lors du scan : {e}")

# Fonction pour afficher les résultats dans l'interface
def afficher_resultats(scan_data):
    tree.delete(*tree.get_children())  # Efface les anciens résultats
    detected_ips = []  # Liste pour stocker les IP détectées
    for host, data in scan_data['scan'].items():
        # Récupérer l'état de l'hôte (actif ou non)
        state = data.get('status', {}).get('state', 'inconnu')
        # Récupérer d'autres informations comme les noms d'hôtes
        hostnames = data.get('hostnames', [])
        hostname = hostnames[0] if hostnames else "Inconnu"
        
        # Ajouter l'IP à la liste
        detected_ips.append(host)
        # Insérer l'IP, le nom d'hôte et son état dans le tableau
        tree.insert("", "end", values=(host, hostname, state))

    # Affichage des IP détectées dans la console
    print("IPs détectées : ", detected_ips)

# Fonction pour afficher les informations de l'application
def a_propos():
    messagebox.showinfo("À propos", "Seahawks Harvester v1.0\nScanner réseau local.")

# Configuration de la fenêtre principale
app = tk.Tk()
app.title("Seahawks Harvester")
app.geometry("600x400")

# Titre
label_title = tk.Label(app, text="Scanner Réseau Seahawks", font=("Arial", 16))
label_title.pack(pady=10)

# Champ pour entrer l'IP ou le réseau
frame_input = tk.Frame(app)
frame_input.pack(pady=10)

label_ip = tk.Label(frame_input, text="Entrez une IP ou une plage (ex: 192.168.0.1 ou 192.168.0.0/24)")
label_ip.pack(side=tk.LEFT)

entry_ip = tk.Entry(frame_input, width=20)
entry_ip.pack(side=tk.LEFT, padx=5)

button_scan = tk.Button(frame_input, text="Scanner", command=scanner_reseau)
button_scan.pack(side=tk.LEFT)

# Tableau pour afficher les résultats
frame_table = tk.Frame(app)
frame_table.pack(pady=10, fill=tk.BOTH, expand=True)

columns = ("Adresse IP", "Nom d'hôte", "État")
tree = ttk.Treeview(frame_table, columns=columns, show="headings")
tree.heading("Adresse IP", text="Adresse IP")
tree.heading("Nom d'hôte", text="Nom d'hôte")
tree.heading("État", text="État")
tree.pack(fill=tk.BOTH, expand=True)

# Bouton À propos
button_about = tk.Button(app, text="À propos", command=a_propos)
button_about.pack(pady=10)

# Lancement de l'application
app.mainloop()
