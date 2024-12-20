import tkinter as tk
from tkinter import ttk
import nmap
import sqlite3
import random
from datetime import datetime

# Fonction pour connecter à la base de données SQLite
def get_db_connection():
    conn = sqlite3.connect('MSPR1.db')  # Base de données utilisée
    conn.row_factory = sqlite3.Row
    return conn

# Fonction pour scanner un sous-réseau et récupérer les informations de ports ouverts
def scan_network_and_ports(subnet):
    nm = nmap.PortScanner()
    nm.scan(hosts=subnet, arguments='-p 22,80,443,8080')  # Scan des ports spécifiés
    open_ports = {}

    # Vérifier les ports ouverts pour chaque hôte
    for ip in nm.all_hosts():
        open_ports[ip] = []
        for proto in nm[ip].all_protocols():
            lport = nm[ip][proto].keys()
            for port in lport:
                if nm[ip][proto][port]['state'] == 'open':
                    open_ports[ip].append(port)

    return open_ports

# Fonction pour insérer les résultats du scan dans la base de données
def insert_scan_to_db(client_name, client_location, subnet, open_ports, latency):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Ajouter un client (franchise) dans la base de données
    cursor.execute('INSERT INTO clients (name, location) VALUES (?, ?)', (client_name, client_location))
    client_id = cursor.lastrowid

    # Ajouter un scan dans la base de données
    scan_date = datetime.now()
    application_version = "1.0.0"  # Version de l'application
    cursor.execute('INSERT INTO scans (client_id, scan_date, latency_wan, application_version) VALUES (?, ?, ?, ?)', 
                   (client_id, scan_date, latency, application_version))
    scan_id = cursor.lastrowid

    # Ajouter les résultats du scan pour chaque IP
    for ip, ports in open_ports.items():
        hostname = f"Host-{random.randint(1, 100)}"  # Nom de la machine simulé
        cursor.execute('INSERT INTO machines (scan_id, ip_address, hostname) VALUES (?, ?, ?)', 
                       (scan_id, ip, hostname))
        machine_id = cursor.lastrowid

        # Ajouter les ports ouverts pour chaque machine
        for port in ports:
            cursor.execute('INSERT INTO open_ports (machine_id, port_number) VALUES (?, ?)', 
                           (machine_id, port))

    # Sauvegarder les modifications dans la base de données
    conn.commit()
    conn.close()

# Fonction pour afficher les résultats dans l'interface graphique
def display_info():
    result_text.insert(tk.END, "Scan en cours...\n")
    root.update()

    subnet = "192.168.1.0/24"  # Sous-réseau à scanner
    client_name = "Franchise A"
    client_location = "Paris"
    
    # Scanner les IP et récupérer les résultats du scan
    open_ports = scan_network_and_ports(subnet)

    # Simuler la latence (par exemple, une latence moyenne de 50 ms)
    latency = random.uniform(10, 100)  # Latence simulée

    # Enregistrer les résultats dans la base de données
    insert_scan_to_db(client_name, client_location, subnet, open_ports, latency)

    # Afficher les résultats dans l'interface graphique
    result_text.delete(1.0, tk.END)  # Effacer les résultats précédents
    result_text.insert(tk.END, f"Scan terminé pour le sous-réseau {subnet}\n")
    result_text.insert(tk.END, f"Latence simulée : {latency:.2f}ms\n")
    
    for ip, ports in open_ports.items():
        # Récupérer un nom de machine simulé (par exemple, "VM-1", "VM-2")
        vm_name = f"Host-{random.randint(1, 100)}"
        result_text.insert(tk.END, f"IP : {ip}, Nom de la VM : {vm_name}, Ports ouverts : {', '.join(map(str, ports))}\n")

# Création de l'interface graphique
root = tk.Tk()
root.title("Seahawks Harvester")

# Label pour afficher un message de scan
scan_label = ttk.Label(root, text="Cliquez pour scanner toutes les IP possibles.")
scan_label.pack(pady=5)

# Bouton pour lancer le scan
scan_button = ttk.Button(root, text="Scanner", command=display_info)
scan_button.pack(pady=10)

# Zone de texte pour afficher les résultats du scan
result_text = tk.Text(root, height=20, width=50)
result_text.pack(pady=5)

# Lancer l'application
root.mainloop()
