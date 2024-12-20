from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

# Fonction pour connecter à la base de données SQLite
def get_db_connection():
    conn = sqlite3.connect('MSPR1.db')  # Base de données MSPR1.db
    conn.row_factory = sqlite3.Row
    return conn

# Route pour afficher le tableau de bord des clients
@app.route('/')
def dashboard():
    conn = get_db_connection()
    clients = conn.execute('SELECT * FROM clients').fetchall()  # Récupérer tous les clients
    conn.close()
    return render_template('dashboard.html', clients=clients)

# Route pour afficher les résultats d'un scan spécifique
@app.route('/scan/<int:scan_id>')
def scan_details(scan_id):
    conn = get_db_connection()

    # Récupérer les informations du scan
    scan = conn.execute('SELECT * FROM scans WHERE id = ?', (scan_id,)).fetchone()
    
    # Récupérer les machines détectées lors du scan
    machines = conn.execute('SELECT * FROM machines WHERE scan_id = ?', (scan_id,)).fetchall()
    
    # Récupérer les ports ouverts pour chaque machine
    machine_ports = {}
    for machine in machines:
        machine_id = machine['id']
        ports = conn.execute('SELECT port_number FROM open_ports WHERE machine_id = ?', (machine_id,)).fetchall()
        machine_ports[machine['ip_address']] = [port['port_number'] for port in ports]
    
    conn.close()

    return render_template('scan_details.html', scan=scan, machines=machines, machine_ports=machine_ports)

# Démarrer l'application Flask
if __name__ == '__main__':
    app.run(debug=True)
