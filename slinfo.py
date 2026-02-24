# -*- coding: utf-8 -*-
import os
import socket

class SatLodgeInfo:
    def __init__(self):
        pass

    def getModel(self):
        """Legge il modello del decoder"""
        try:
            if os.path.exists("/proc/stb/info/boxtype"):
                return open("/proc/stb/info/boxtype").read().strip().upper()
            if os.path.exists("/proc/stb/info/model"):
                return open("/proc/stb/info/model").read().strip().upper()
        except:
            pass
        return "Unknown Box"

    def getImageVersion(self):
        """Legge la versione dell'immagine SatLodge"""
        try:
            if os.path.exists("/etc/satlodge-version"):
                return open("/etc/satlodge-version").read().strip()
            if os.path.exists("/etc/image-version"):
                # Cerca la riga version= dentro image-version
                for line in open("/etc/image-version"):
                    if "version=" in line:
                        return line.split("=")[1].strip()
        except:
            pass
        return "SatLodge Build"

    def getCpuTemp(self):
        """Legge la temperatura della CPU (se disponibile)"""
        try:
            # Percorsi comuni per i sensori di temperatura Enigma2
            paths = [
                "/proc/stb/fp/temp_sensor_avg",
                "/proc/stb/sensors/temp0/value",
                "/proc/stb/fp/temp_sensor",
                "/sys/class/thermal/thermal_zone0/temp"
            ]
            for path in paths:
                if os.path.exists(path):
                    temp = open(path).read().strip()
                    # Alcuni file riportano 45000 invece di 45, correggiamo se necessario
                    if len(temp) > 2:
                        temp = temp[:2]
                    return str(temp) + "°C"
        except:
            pass
        return "N/A"

    def getRamInfo(self):
        """Ritorna la RAM libera rispetto alla totale"""
        try:
            with open("/proc/meminfo", "r") as f:
                lines = f.readlines()
                total = 0
                free = 0
                for line in lines:
                    if "MemTotal" in line:
                        total = int(line.split()[1]) // 1024
                    if "MemFree" in line:
                        free = int(line.split()[1]) // 1024
                if total > 0:
                    return "%sMB / %sMB" % (free, total)
        except:
            pass
        return "N/A"

    def getIP(self):
        """Rileva l'indirizzo IP locale del decoder"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # Non serve connettersi davvero, serve solo per trovare l'interfaccia attiva
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "N/A"

    def getCpuInfo(self):
        """Legge il tipo di processore"""
        try:
            for line in open("/proc/cpuinfo"):
                if "model name" in line or "system type" in line:
                    return line.split(":")[1].strip()
        except:
            pass
        return "Generic CPU"
