#!/usr/bin/env python3
"""
Script pour mettre à jour le DNS Cloudflare avec l'IP publique actuelle.
"""

import os
import sys
import time
import signal
import requests
import json
from typing import Optional, Dict, Any


class CloudflareDNSUpdater:
    """Classe pour gérer les mises à jour DNS Cloudflare."""
    
    def __init__(self, token: str, zone_name: str, record_name: str):
        """
        Initialise le client Cloudflare DNS.
        
        Args:
            token: Token d'API Cloudflare
            zone_name: Nom de la zone DNS (ex: stranix.net)
            record_name: Nom complet du record (ex: home.stranix.net)
        """
        self.token = token
        self.zone_name = zone_name
        self.record_name = record_name
        self.base_url = "https://api.cloudflare.com/client/v4"
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
    
    def get_public_ip(self) -> Optional[str]:
        """
        Récupère l'IP publique actuelle.
        
        Returns:
            L'IP publique ou None en cas d'erreur
        """
        services = [
            "https://api.ipify.org",
            "https://icanhazip.com",
            "https://ifconfig.me/ip"
        ]
        
        for service in services:
            try:
                response = requests.get(service, timeout=10)
                if response.status_code == 200:
                    ip = response.text.strip()
                    # Vérifier que c'est une IP valide (IPv4)
                    parts = ip.split('.')
                    if len(parts) == 4 and all(part.isdigit() and 0 <= int(part) <= 255 for part in parts):
                        return ip
            except Exception as e:
                print(f"Erreur lors de la récupération de l'IP depuis {service}: {e}", file=sys.stderr)
                continue
        
        return None
    
    def get_zone_id(self) -> Optional[str]:
        """
        Récupère l'ID de la zone Cloudflare.
        
        Returns:
            L'ID de la zone ou None en cas d'erreur
        """
        url = f"{self.base_url}/zones"
        params = {"name": self.zone_name}
        
        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get("success") and data.get("result"):
                return data["result"][0]["id"]
            else:
                print(f"Zone '{self.zone_name}' non trouvée", file=sys.stderr)
                return None
        except Exception as e:
            print(f"Erreur lors de la récupération de la zone: {e}", file=sys.stderr)
            return None
    
    def get_dns_record(self, zone_id: str) -> Optional[Dict[str, Any]]:
        """
        Récupère le record DNS existant.
        
        Args:
            zone_id: ID de la zone Cloudflare
            
        Returns:
            Le record DNS ou None s'il n'existe pas
        """
        url = f"{self.base_url}/zones/{zone_id}/dns_records"
        params = {"name": self.record_name, "type": "A"}
        
        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get("success") and data.get("result") and len(data["result"]) > 0:
                return data["result"][0]
            return None
        except Exception as e:
            print(f"Erreur lors de la récupération du record DNS: {e}", file=sys.stderr)
            return None
    
    def update_dns_record(self, zone_id: str, record_id: str, ip: str) -> bool:
        """
        Met à jour le record DNS existant.
        
        Args:
            zone_id: ID de la zone Cloudflare
            record_id: ID du record DNS
            ip: Nouvelle adresse IP
            
        Returns:
            True si la mise à jour réussit, False sinon
        """
        url = f"{self.base_url}/zones/{zone_id}/dns_records/{record_id}"
        data = {
            "type": "A",
            "name": self.record_name,
            "content": ip,
            "ttl": 300  # TTL de 5 minutes
        }
        
        try:
            response = requests.put(url, headers=self.headers, json=data, timeout=10)
            response.raise_for_status()
            result = response.json()
            
            if result.get("success"):
                return True
            else:
                print(f"Erreur lors de la mise à jour: {result.get('errors', [])}", file=sys.stderr)
                return False
        except Exception as e:
            print(f"Erreur lors de la mise à jour du DNS: {e}", file=sys.stderr)
            return False
    
    def create_dns_record(self, zone_id: str, ip: str) -> bool:
        """
        Crée un nouveau record DNS.
        
        Args:
            zone_id: ID de la zone Cloudflare
            ip: Adresse IP
            
        Returns:
            True si la création réussit, False sinon
        """
        url = f"{self.base_url}/zones/{zone_id}/dns_records"
        data = {
            "type": "A",
            "name": self.record_name,
            "content": ip,
            "ttl": 300  # TTL de 5 minutes
        }
        
        try:
            response = requests.post(url, headers=self.headers, json=data, timeout=10)
            response.raise_for_status()
            result = response.json()
            
            if result.get("success"):
                print(f"✓ Record DNS créé avec succès: {self.record_name} -> {ip}")
                return True
            else:
                print(f"Erreur lors de la création: {result.get('errors', [])}", file=sys.stderr)
                return False
        except Exception as e:
            print(f"Erreur lors de la création du DNS: {e}", file=sys.stderr)
            return False
    
    def update(self) -> bool:
        """
        Met à jour le DNS avec l'IP publique actuelle.
        
        Returns:
            True si la mise à jour réussit, False sinon
        """
        # Récupérer l'IP publique
        print("Récupération de l'IP publique...", flush=True)
        ip = self.get_public_ip()
        if not ip:
            print("❌ Impossible de récupérer l'IP publique", file=sys.stderr, flush=True)
            return False
        
        print(f"IP publique récupérée: {ip}", flush=True)
        
        # Récupérer l'ID de la zone
        print(f"Récupération de la zone Cloudflare '{self.zone_name}'...", flush=True)
        zone_id = self.get_zone_id()
        if not zone_id:
            print(f"❌ Impossible de récupérer la zone '{self.zone_name}'", file=sys.stderr, flush=True)
            return False
        
        print(f"Zone trouvée (ID: {zone_id})", flush=True)
        
        # Récupérer le record DNS existant
        print(f"Recherche du record DNS '{self.record_name}'...", flush=True)
        record = self.get_dns_record(zone_id)
        
        if record:
            current_ip = record.get("content")
            print(f"Record DNS trouvé - IP actuelle dans Cloudflare: {current_ip}", flush=True)
            
            if current_ip == ip:
                print(f"✓ L'IP est déjà à jour: {ip} (pas de changement nécessaire)", flush=True)
                return True
            
            print(f"🔄 CHANGEMENT D'IP DÉTECTÉ: {current_ip} -> {ip}", flush=True)
            print(f"Mise à jour du DNS Cloudflare...", flush=True)
            success = self.update_dns_record(zone_id, record["id"], ip)
            if success:
                print(f"✅ DNS mis à jour avec succès: {self.record_name} pointe maintenant vers {ip}", flush=True)
            else:
                print(f"❌ Échec de la mise à jour du DNS", file=sys.stderr, flush=True)
            return success
        else:
            print(f"⚠️  Record DNS non trouvé, création d'un nouveau record avec IP: {ip}", flush=True)
            success = self.create_dns_record(zone_id, ip)
            if success:
                print(f"✅ Record DNS créé avec succès: {self.record_name} -> {ip}", flush=True)
            return success


# Variable globale pour gérer l'arrêt propre
running = True


def signal_handler(sig, frame):
    """Gestionnaire de signaux pour arrêter proprement le script."""
    global running
    print("\n\n🛑 Réception du signal d'arrêt, arrêt en cours...", flush=True)
    running = False


def main():
    """Fonction principale."""
    global running
    
    # Configuration depuis les variables d'environnement
    token = os.getenv("CLOUDFLARE_TOKEN")
    zone_name = os.getenv("CLOUDFLARE_ZONE", "stranix.net")
    record_name = os.getenv("CLOUDFLARE_RECORD", "home.stranix.net")
    check_interval = int(os.getenv("CHECK_INTERVAL", "300"))  # Par défaut 5 minutes
    
    if not token:
        print("Erreur: CLOUDFLARE_TOKEN n'est pas défini", file=sys.stderr)
        sys.exit(1)
    
    # Enregistrer les gestionnaires de signaux
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    updater = CloudflareDNSUpdater(token, zone_name, record_name)
    
    print("=" * 60, flush=True)
    print("🚀 Démarrage du service de mise à jour DNS Cloudflare", flush=True)
    print("=" * 60, flush=True)
    print(f"Zone DNS: {zone_name}", flush=True)
    print(f"Record DNS: {record_name}", flush=True)
    print(f"Intervalle de vérification: {check_interval} secondes ({check_interval // 60} minutes)", flush=True)
    
    # Récupérer et afficher l'IP publique au démarrage
    print("\nRécupération de l'IP publique au démarrage...", flush=True)
    startup_ip = updater.get_public_ip()
    if startup_ip:
        print(f"✅ IP publique actuelle: {startup_ip}", flush=True)
    else:
        print("⚠️  Impossible de récupérer l'IP publique au démarrage", file=sys.stderr, flush=True)
    
    print("\nPremière vérification du DNS...", flush=True)
    print("-" * 60, flush=True)
    
    # Première vérification immédiate
    updater.update()
    
    print("-" * 60, flush=True)
    print(f"\n⏳ Prochaine vérification dans {check_interval} secondes ({check_interval // 60} minutes)", flush=True)
    print("Appuyez sur Ctrl+C pour arrêter\n", flush=True)
    
    # Boucle principale
    while running:
        try:
            # Attendre l'intervalle configuré
            time.sleep(check_interval)
            
            if not running:
                break
            
            # Vérifier et mettre à jour le DNS
            print(f"\n{'=' * 60}", flush=True)
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Vérification de l'IP publique...", flush=True)
            print("-" * 60, flush=True)
            updater.update()
            print("-" * 60, flush=True)
            print(f"⏳ Prochaine vérification dans {check_interval} secondes ({check_interval // 60} minutes)", flush=True)
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Erreur inattendue: {e}", file=sys.stderr)
            # Continuer même en cas d'erreur
            continue
    
    print("\n" + "=" * 60, flush=True)
    print("✅ Arrêt du service de mise à jour DNS", flush=True)
    print("=" * 60, flush=True)
    sys.exit(0)


if __name__ == "__main__":
    main()
