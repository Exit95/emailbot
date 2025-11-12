#!/usr/bin/env python3
"""
Diagnose-Skript für Mailcow SMTP Verbindungsprobleme
Testet verschiedene Verbindungsmethoden und gibt detaillierte Informationen aus
"""

import socket
import smtplib
import sys
import os

# Auto-Erkennung: Wenn auf Mailcow-VM, verwende localhost
def detect_smtp_server():
    try:
        # Prüfe ob wir auf dem Mailcow-Server sind
        result = os.popen('docker ps 2>/dev/null | grep -i mailcow').read()
        if 'mailcow' in result.lower():
            print("✓ Mailcow Docker erkannt - verwende localhost")
            return 'localhost'
    except:
        pass

    # Fallback: Verwende externen Server
    return 'mail.danapfel-digital.de'

SMTP_SERVER = detect_smtp_server()
EMAIL_ADDRESS = 'office@danapfel-digital.de'
EMAIL_PASSWORD = ':,30,seNDSK'

print("=" * 70)
print("MAILCOW SMTP DIAGNOSE-TOOL")
print("=" * 70)

# Test 1: DNS Auflösung
print("\n[1/6] DNS Auflösung testen...")
print("-" * 70)
try:
    ipv4_addresses = []
    ipv6_addresses = []
    
    addr_info = socket.getaddrinfo(SMTP_SERVER, None)
    for info in addr_info:
        family, _, _, _, sockaddr = info
        ip = sockaddr[0]
        if family == socket.AF_INET:
            if ip not in ipv4_addresses:
                ipv4_addresses.append(ip)
        elif family == socket.AF_INET6:
            if ip not in ipv6_addresses:
                ipv6_addresses.append(ip)
    
    print(f"✓ DNS Auflösung erfolgreich!")
    print(f"  IPv4 Adressen: {', '.join(ipv4_addresses) if ipv4_addresses else 'Keine'}")
    print(f"  IPv6 Adressen: {', '.join(ipv6_addresses) if ipv6_addresses else 'Keine'}")
except Exception as e:
    print(f"✗ DNS Auflösung fehlgeschlagen: {e}")
    sys.exit(1)

# Test 2: IPv4 Socket-Verbindung zu Port 465
print("\n[2/6] IPv4 Socket-Verbindung zu Port 465 testen...")
print("-" * 70)
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(10)
    if ipv4_addresses:
        sock.connect((ipv4_addresses[0], 465))
        print(f"✓ IPv4 Socket-Verbindung zu {ipv4_addresses[0]}:465 erfolgreich!")
        sock.close()
    else:
        print("✗ Keine IPv4-Adresse verfügbar")
except Exception as e:
    print(f"✗ IPv4 Socket-Verbindung fehlgeschlagen: {e}")
    print("  HINWEIS: Port 465 ist möglicherweise nicht erreichbar!")

# Test 3: IPv4 Socket-Verbindung zu Port 587
print("\n[3/6] IPv4 Socket-Verbindung zu Port 587 testen...")
print("-" * 70)
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(10)
    if ipv4_addresses:
        sock.connect((ipv4_addresses[0], 587))
        print(f"✓ IPv4 Socket-Verbindung zu {ipv4_addresses[0]}:587 erfolgreich!")
        sock.close()
    else:
        print("✗ Keine IPv4-Adresse verfügbar")
except Exception as e:
    print(f"✗ IPv4 Socket-Verbindung fehlgeschlagen: {e}")

# Test 4: SMTP SSL/TLS (Port 465) mit IPv4
print("\n[4/6] SMTP SSL/TLS (Port 465) mit IPv4 testen...")
print("-" * 70)
try:
    # IPv4 erzwingen
    old_getaddrinfo = socket.getaddrinfo
    def getaddrinfo_ipv4_only(host, port, family=0, type=0, proto=0, flags=0):
        return old_getaddrinfo(host, port, socket.AF_INET, type, proto, flags)
    socket.getaddrinfo = getaddrinfo_ipv4_only
    
    server = smtplib.SMTP_SSL(SMTP_SERVER, 465, timeout=10)
    server.ehlo()
    print(f"✓ SMTP SSL/TLS Verbindung erfolgreich!")
    print(f"  Server: {server.ehlo_resp.decode('utf-8').split()[0]}")
    
    # Login testen
    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    print(f"✓ SMTP Login erfolgreich!")
    server.quit()
    
    socket.getaddrinfo = old_getaddrinfo
except Exception as e:
    print(f"✗ SMTP SSL/TLS fehlgeschlagen: {e}")
    socket.getaddrinfo = old_getaddrinfo

# Test 5: SMTP STARTTLS (Port 587) mit IPv4
print("\n[5/6] SMTP STARTTLS (Port 587) mit IPv4 testen...")
print("-" * 70)
try:
    # IPv4 erzwingen
    old_getaddrinfo = socket.getaddrinfo
    def getaddrinfo_ipv4_only(host, port, family=0, type=0, proto=0, flags=0):
        return old_getaddrinfo(host, port, socket.AF_INET, type, proto, flags)
    socket.getaddrinfo = getaddrinfo_ipv4_only
    
    server = smtplib.SMTP(SMTP_SERVER, 587, timeout=10)
    server.ehlo()
    server.starttls()
    server.ehlo()
    print(f"✓ SMTP STARTTLS Verbindung erfolgreich!")
    
    # Login testen
    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    print(f"✓ SMTP Login erfolgreich!")
    server.quit()
    
    socket.getaddrinfo = old_getaddrinfo
except Exception as e:
    print(f"✗ SMTP STARTTLS fehlgeschlagen: {e}")
    socket.getaddrinfo = old_getaddrinfo

# Test 6: Netzwerk-Route prüfen
print("\n[6/6] Netzwerk-Informationen...")
print("-" * 70)
try:
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    print(f"  Lokaler Hostname: {hostname}")
    print(f"  Lokale IP: {local_ip}")
except Exception as e:
    print(f"  Konnte lokale Netzwerk-Info nicht ermitteln: {e}")

print("\n" + "=" * 70)
print("DIAGNOSE ABGESCHLOSSEN")
print("=" * 70)
print("\nEMPFEHLUNG:")
print("  - Wenn Port 465 funktioniert: Verwenden Sie USE_SSL = True")
print("  - Wenn Port 587 funktioniert: Verwenden Sie USE_SSL = False")
print("  - Wenn beide fehlschlagen: Firewall/Netzwerk-Problem!")
print("=" * 70)

