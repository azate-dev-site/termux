
import subprocess
import sys
import os
import platform
import socket
import uuid
import json
from datetime import datetime

def install_dependencies():
    """Install required packages automatically"""
    required_packages = ['psutil', 'requests', 'geocoder']
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            print(f"Installation de {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"{package} installé avec succès!")

# Install dependencies first
install_dependencies()

# Now import the required modules
import psutil
import requests
import geocoder

def get_system_info():
    """Collect comprehensive system information"""
    info = {}
    
    # Basic system info
    info['system'] = {
        'platform': platform.platform(),
        'system': platform.system(),
        'node': platform.node(),
        'release': platform.release(),
        'version': platform.version(),
        'machine': platform.machine(),
        'processor': platform.processor(),
        'architecture': platform.architecture(),
        'hostname': socket.gethostname(),
        'mac_address': ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0,2*6,2)][::-1])
    }
    
    # CPU information
    info['cpu'] = {
        'physical_cores': psutil.cpu_count(logical=False),
        'total_cores': psutil.cpu_count(logical=True),
        'max_frequency': f"{psutil.cpu_freq().max:.2f}Mhz" if psutil.cpu_freq() else "N/A",
        'min_frequency': f"{psutil.cpu_freq().min:.2f}Mhz" if psutil.cpu_freq() else "N/A",
        'current_frequency': f"{psutil.cpu_freq().current:.2f}Mhz" if psutil.cpu_freq() else "N/A",
        'cpu_usage': f"{psutil.cpu_percent(interval=1):.1f}%"
    }
    
    # Memory information
    svmem = psutil.virtual_memory()
    info['memory'] = {
        'total': f"{svmem.total / (1024**3):.2f} GB",
        'available': f"{svmem.available / (1024**3):.2f} GB",
        'used': f"{svmem.used / (1024**3):.2f} GB",
        'percentage': f"{svmem.percent:.1f}%"
    }
    
    # Disk information
    info['disk'] = {}
    partitions = psutil.disk_partitions()
    for partition in partitions:
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
            info['disk'][partition.device] = {
                'mountpoint': partition.mountpoint,
                'file_system': partition.fstype,
                'total_size': f"{partition_usage.total / (1024**3):.2f} GB",
                'used': f"{partition_usage.used / (1024**3):.2f} GB",
                'free': f"{partition_usage.free / (1024**3):.2f} GB",
                'percentage': f"{(partition_usage.used / partition_usage.total) * 100:.1f}%"
            }
        except PermissionError:
            continue
    
    # Network information
    info['network'] = {}
    if_addrs = psutil.net_if_addrs()
    for interface_name, interface_addresses in if_addrs.items():
        addr_info = []
        for address in interface_addresses:
            if str(address.family) == 'AddressFamily.AF_INET':
                addr_info.append({
                    'ip_address': address.address,
                    'netmask': address.netmask,
                    'broadcast_ip': address.broadcast
                })
            elif str(address.family) == 'AddressFamily.AF_PACKET':
                addr_info.append({
                    'mac_address': address.address,
                    'netmask': address.netmask,
                    'broadcast_mac': address.broadcast
                })
        info['network'][interface_name] = addr_info
    
    # Boot time
    boot_time_timestamp = psutil.boot_time()
    bt = datetime.fromtimestamp(boot_time_timestamp)
    info['boot_time'] = f"{bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}"
    
    return info

def get_public_ip():
    """Get public IP address"""
    try:
        response = requests.get('https://api.ipify.org?format=json', timeout=5)
        return response.json()['ip']
    except:
        return "Impossible d'obtenir l'IP publique"

def get_ip_location(ip):
    """Get location based on IP address"""
    try:
        response = requests.get(f'http://ip-api.com/json/{ip}', timeout=5)
        data = response.json()
        if data['status'] == 'success':
            return {
                'country': data.get('country', 'N/A'),
                'region': data.get('regionName', 'N/A'),
                'city': data.get('city', 'N/A'),
                'zip': data.get('zip', 'N/A'),
                'latitude': data.get('lat', 'N/A'),
                'longitude': data.get('lon', 'N/A'),
                'timezone': data.get('timezone', 'N/A'),
                'isp': data.get('isp', 'N/A')
            }
    except:
        pass
    return "Impossible d'obtenir la localisation IP"

def get_gps_location():
    """Try to get GPS location using various methods"""
    locations = []
    
    # Method 1: geocoder.ip
    try:
        g = geocoder.ip('me')
        if g.ok:
            locations.append({
                'latitude': g.latlng[0],
                'longitude': g.latlng[1],
                'address': g.address,
                'method': 'Geocoder IP',
                'accuracy': 'City level'
            })
    except:
        pass
    
    # Method 2: Using multiple IP services
    services = [
        'http://ip-api.com/json/',
        'https://ipapi.co/json/',
        'https://freegeoip.app/json/'
    ]
    
    for service in services:
        try:
            response = requests.get(service, timeout=3)
            data = response.json()
            
            if service.startswith('http://ip-api.com'):
                if data.get('status') == 'success':
                    locations.append({
                        'latitude': data.get('lat'),
                        'longitude': data.get('lon'),
                        'address': f"{data.get('city')}, {data.get('regionName')}, {data.get('country')}",
                        'method': 'IP-API Service',
                        'accuracy': data.get('accuracy', 'Unknown'),
                        'isp': data.get('isp'),
                        'timezone': data.get('timezone')
                    })
            elif service.startswith('https://ipapi.co'):
                locations.append({
                    'latitude': data.get('latitude'),
                    'longitude': data.get('longitude'),
                    'address': f"{data.get('city')}, {data.get('region')}, {data.get('country_name')}",
                    'method': 'IPAPI Service',
                    'accuracy': 'ISP level',
                    'org': data.get('org')
                })
        except:
            continue
    
    # Method 3: Try WiFi/Bluetooth scanning (limited on servers)
    try:
        import subprocess
        # Try to get WiFi networks (works on some systems)
        result = subprocess.run(['iwlist', 'scan'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            wifi_networks = len([line for line in result.stdout.split('\n') if 'ESSID:' in line])
            if wifi_networks > 0:
                locations.append({
                    'method': f'WiFi Scan détecté {wifi_networks} réseaux',
                    'note': 'Géolocalisation WiFi non disponible sur serveur'
                })
    except:
        pass
    
    if locations:
        return {
            'primary_location': locations[0],
            'alternative_locations': locations[1:] if len(locations) > 1 else [],
            'total_methods': len(locations)
        }
    
    return "Aucune méthode de géolocalisation disponible"

def display_info(info, public_ip, ip_location, gps_location):
    """Display all collected information in a formatted way"""
    print("="*80)
    print("           INFORMATIONS DÉTAILLÉES DE L'APPAREIL")
    print("="*80)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    print("🖥️  SYSTÈME:")
    print("-"*50)
    for key, value in info['system'].items():
        print(f"  {key.replace('_', ' ').title()}: {value}")
    
    print("\n🔧 PROCESSEUR:")
    print("-"*50)
    for key, value in info['cpu'].items():
        print(f"  {key.replace('_', ' ').title()}: {value}")
    
    print("\n💾 MÉMOIRE:")
    print("-"*50)
    for key, value in info['memory'].items():
        print(f"  {key.replace('_', ' ').title()}: {value}")
    
    print("\n💿 DISQUES:")
    print("-"*50)
    for device, details in info['disk'].items():
        print(f"  Périphérique: {device}")
        for key, value in details.items():
            print(f"    {key.replace('_', ' ').title()}: {value}")
        print()
    
    print("🌐 RÉSEAU:")
    print("-"*50)
    print(f"  IP Publique: {public_ip}")
    for interface, addresses in info['network'].items():
        if addresses:
            print(f"  Interface {interface}:")
            for addr in addresses:
                for key, value in addr.items():
                    if value:
                        print(f"    {key.replace('_', ' ').title()}: {value}")
    
    print(f"\n  Heure de démarrage: {info['boot_time']}")
    
    print("\n📍 LOCALISATION:")
    print("-"*50)
    if isinstance(ip_location, dict):
        for key, value in ip_location.items():
            print(f"  {key.replace('_', ' ').title()}: {value}")
    else:
        print(f"  {ip_location}")
    
    print("\n🛰️  COORDONNÉES GPS:")
    print("-"*50)
    if isinstance(gps_location, dict):
        if 'primary_location' in gps_location:
            primary = gps_location['primary_location']
            print("  📍 LOCALISATION PRINCIPALE:")
            for key, value in primary.items():
                print(f"    {key.replace('_', ' ').title()}: {value}")
            
            if 'latitude' in primary and 'longitude' in primary:
                print(f"\n  🗺️  Lien Google Maps:")
                print(f"    https://www.google.com/maps?q={primary['latitude']},{primary['longitude']}")
                print(f"  🌍 Coordonnées exactes: {primary['latitude']}, {primary['longitude']}")
            
            if gps_location.get('alternative_locations'):
                print(f"\n  📊 SOURCES ALTERNATIVES ({len(gps_location['alternative_locations'])}):")
                for i, alt in enumerate(gps_location['alternative_locations'], 1):
                    print(f"    Source {i}: {alt.get('method', 'Unknown')}")
                    if 'latitude' in alt and 'longitude' in alt:
                        print(f"      Coordonnées: {alt['latitude']}, {alt['longitude']}")
        else:
            for key, value in gps_location.items():
                print(f"  {key.replace('_', ' ').title()}: {value}")
    else:
        print(f"  {gps_location}")
    
    print("\n" + "="*80)
    print("⚠️  AVERTISSEMENT: Ces informations sont à des fins éducatives uniquement!")
    print("="*80)

def main():
    """Main function to execute the device info collection"""
    print("🔄 Collecte des informations de l'appareil en cours...")
    print("📦 Vérification et installation des dépendances...")
    
    # Collect system information
    system_info = get_system_info()
    
    # Get public IP
    public_ip = get_public_ip()
    
    # Get IP-based location
    ip_location = get_ip_location(public_ip)
    
    # Try to get GPS location
    gps_location = get_gps_location()
    
    # Display all information
    display_info(system_info, public_ip, ip_location, gps_location)
    
    # Save to file
    all_data = {
        'timestamp': datetime.now().isoformat(),
        'system_info': system_info,
        'public_ip': public_ip,
        'ip_location': ip_location,
        'gps_location': gps_location
    }
    
    try:
        with open('device_info_log.json', 'w', encoding='utf-8') as f:
            json.dump(all_data, f, indent=2, ensure_ascii=False)
        print(f"\n💾 Données sauvegardées dans 'device_info_log.json'")
    except Exception as e:
        print(f"\n❌ Erreur lors de la sauvegarde: {e}")

if __name__ == "__main__":
    main()
