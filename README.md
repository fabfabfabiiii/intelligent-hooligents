# intelligent-hooligents 🕵🏻‍♂️

Link zu Google Doc: https://docs.google.com/document/d/1lMQypHCQ1DxZwfQJfexfcJzT0jgwsWzoLuHd6C_VS2Y/edit?tab=t.0

Beim Transport der Fans nach einem Fußballspiel / Sportevent muss darauf geachtet werden, dass sich die beiden Fanlager nicht zu nah kommmen und es zu keinen Ausschreitungen kommt. 

Grundsätzlich gibt es folgende Personengruppen:
- Fans Team A
- Fans Team B
- Neutrale Zuschauer

Innerhalb eines Transportmittels sollte die Anzahl der Fans eines Teams nicht bedeutend größer als die Anzahl der Fans des anderen Teams sein. Neutrale Zuschauer ohne optische Merkmale der Vereinszugehörigkeit haben keine Auswirkung auf das Risiko einer Ausschreitung innerhalb eines Transportmittels.

Die zu berücksichtigende Ausgangsmenge ist die Menge aller Zuschauer, die mit öffentlichen Verkehrsmitteln abreisen. Der Startpunkt ist für alle gleich (Stadion) und der Zielpunkt kann unterschiedlich sein (Zielhaltestelle).

Folgende Aspekte sind beim Transport der Zuschauer zu berücksichtigen:
- Kapazität der Transportmittel
- Anzahl der zu transportierenden Personen
- Verkehrsnetz inkl. Anzahl und Distanzen der Haltestellen (Start- bis Zielpunkt)

Optimiert werden die Transportdistanzen unter Berücksichtigung der oben beschriebenen Einschränkung bezüglich der Anzahl der Fans der jeweiligen Teams.

Optionale Erweiterungen:
- Mitreisende Polizisten können eine bestimmte Überzahl an Fans eines Teams ausgleichen
- Umstiege
- Verschiedene Transportmittel
   - unterschiedliche Kapazitäten
   - unterschiedliche Distanzen pro Zeiteinheit


# Beispiel
Ausgangslage:
- 300 Fans Team A
- 300 Fans Team B
- 300 neutrale Zuschauer

Jeder Zuschauer möchte zu einer Zielstation aus der Menge Z {Haltestelle 1, Haltestelle 2, Haltestelle 3, ... }


## Setup
Wir verwenden Python 3.12

`pip install -r requirements.txt`

## Verkehrsnetz

- Erstellung des Graph über [Graph Online](https://graphonline.top/de/)
- Export und Import des Graph als Datei möglich
