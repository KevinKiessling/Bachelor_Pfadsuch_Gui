# Bachelor


Bachelorarbeit zum Thema "Eine GUI zur Visualisierung von Pfadsuch-Algorithmen"

Ausführen aus dem Directory von pfadsuche.py per "python pfadsuche.py"

Python Version 3.13

Benötigte Pip Imports:
- pip install networkx     ->-> Wird aktuell nur für den TestCase genutzt um Dijkstra Ergebnisse mit confirmed 
korrekten von networkx zu vergleichen, wird später entfernt


Aktueller Stand 27.1:
- Graph erstellung refactored, Heap Visualisierung als Baum, komplett colourisation umgeschrieben
- Pseudocode für Liste und normal Dijkstra an Vorlesung angepasst
- 


Nächste Schritte:
Liste und Normal Dijkstra auch klein stufiger machen.
- Pseudocode highlighting für die beiden anderen Algorithmen und die Farben mit Parent Class linken, da grade die Farben 
noch hardcoded sind bis auf die Heap Farbe
- Liste ähnlich wie der heap darstellen.