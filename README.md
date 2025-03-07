Eine GUI zur Visualisierung von Pfadsuch-Algorithmen

Dieses Programm wurde zur Visualisierung von Pfadsuchalgorithmen entwickelt.

Wichtige Hinweise:
-------------------
Manuelle Änderungen an der Konfigurationsdatei `Config` können zu unerwartetem Verhalten führen. 
Die Standardwerte lassen sich wiederherstellen, indem die Datei `Config` gelöscht wird. 
Sollte beim Programmstart keine `Config`-Datei geladen werden können, erstellt das Programm automatisch eine neue `Config`-Datei mit den Standardwerten.

Es wird empfohlen, nur Graphen zu laden, die mit diesem Programm gespeichert wurden. 
Zwar ist es grundsätzlich möglich, andere Graphen zu laden, da die manuelle Eingabe auf Koordinaten im Bereich von 1000x1000 limitiert wurde,
jedoch kann es unter bestimmten Bildschirmgrößen und Seitenverhältnissen dazu kommen,
dass Knoten außerhalb des darstellbaren Bereichs des Canvas liegen.

Voraussetzungen:
----------------
- Python 3.13 oder neuer
  -> Laden Sie Python hier herunter: https://www.python.org/downloads/
  
- NetworkX Version 3.4.2
  -> Installieren Sie die benötigte Version mit dem folgenden Befehl:

     pip install networkx==3.4.2

Ausführung:
-----------
Das Programm kann durch Aufrufen des folgenden Befehls in der Kommandozeile innerhalb des Ordners, in dem sich das Programm befindet, gestartet werden:
  
    python pfadsuche.py
