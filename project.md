## Technical information
* Number of tokens roughly 330000
* max len of tokens: 14450 tokens (3.5 can go to 16k context window)


Dinge die beim cleanen rausgefallen sind:

* Welt, Mars, Saturnmonde etc. -> Planeten
* Bojern, Skythen, Gallier -> historische menschen gruppen 339
* bestimmte Orte in einer Stadt -> pariser Kathedrale zu Paris 339
* Landes-/Ortsnamen als adjektive -> aus Pariser [...] wird Paris
* Orte in Titeln -> Graf von Bückeburg zu Bückeburg 348
* adjektive von ortschaften oder ethnizitäten etc. -> Flämisch wird zu Flandern
* Großpolen zu Polen
* Städte, die heute anders heißen -> Åbo zu Turku
* Städte die im Briefverzeichnis anders aufgeführt werden wie in der absender zeile -> Ebsdorff zu Ebstorf

### Geocoding
* MMQGIS

1. Orte Kathegorisieren: Stadt, Land, Fluss 
2. Geocoden: https://www.geoapify.com/tools/geocoding-online/
3. Maps machen -> QGIS

