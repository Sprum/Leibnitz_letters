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

TODO: als nächstes
COMPARE EACH LETTER old and NEW und dann immer das größere nehmen außerdem die komische default scheiße los werden
1. Geocoden
3. vlt auch nach Absendeort aggregieren...? per person??

Differenzen:
{'Frankfurt an der Oder', 'Kanarische Inseln', 'Schwaben', 'Wolffenbüttel', 'OberUngarn', 'Flandern', 'Rotes Meer','Ebdorff', 'Ebsdorff'}

* Zählen: 
102
103
115
127
146
193
194
213
216
236
237
240
242
243
249
253
280
289
303
31
317
344
35
351
354
36
360
364
37
375
41
44
49
50
52
53
56
79
87
93
96
das sind alle Briefe von Sophie bei denen der absende ort nicht in der csv gefunden wurde...