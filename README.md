# Intelligent-Hooligents 🕵🏻‍♂️

Beim Transport der Fans nach einem Fußballspiel / Sportevent muss darauf geachtet werden, dass sich die beiden Fanlager nicht zu nahe kommen und es zu keinen Ausschreitungen kommt. 

Grundsätzlich gibt es folgende Personengruppen:
- Fans Team A
- Fans Team B
- Neutrale Zuschauer

Innerhalb eines Transportmittels sollte die Anzahl der Fans eines Teams nicht bedeutend größer als die Anzahl der Fans des anderen Teams sein. Neutrale Zuschauer ohne Vereinszugehörigkeit haben keine Auswirkung auf das Risiko einer Ausschreitung innerhalb eines Transportmittels.

Die zu berücksichtigende Ausgangsmenge ist die Menge aller Zuschauer, die mit öffentlichen Verkehrsmitteln abreisen. Der Startpunkt ist für alle gleich (Stadion) und der Zielpunkt kann unterschiedlich sein (Zielhaltestelle).

Folgende Aspekte sind beim Transport der Zuschauer zu berücksichtigen:
- Anzahl und Kapazität der Transportmittel
- Anzahl der zu transportierenden Personen
- Verkehrsnetz inklusive Anzahl und Distanzen der Haltestellen (Start- bis Zielpunkt)

Optimiert werden die Transportdistanzen unter Berücksichtigung der oben beschriebenen Einschränkung bezüglich der Anzahl der Fans der jeweiligen Teams.

## Setup

Wir verwenden Python 3.12

`pip install -r requirements.txt`

`cd src`

`streamlit run streamlit_demo_intelligent_hooligents_model.py`

## Verkehrsnetz

- Erstellung des Graph über [Graph Online](https://graphonline.top/de/)
- Export und Import des Graph als Datei möglich
