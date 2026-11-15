# AgroBytes — guion (Mia y Mauro)

`→` = clic dentro de la misma diapositiva · `⏭️` = **siguiente diapositiva**

---

## 1 · Portada

**MIA:**
Hi! We are AgroBytes, from UABC.
`→`
Every season, a farmer makes a bet.
What to plant? When? Is there enough water?
The climate is changing, and the old rules don't work anymore.

`⏭️`

---

## 2 · The challenge

**MAURO:**
Our challenge is Field Shift: help farmers choose crop rotations that protect their soil and their water.
First, we looked at the problems: more heat, rain you can't predict, and tired soil.
`→`
Then we looked at the data. NASA has more than 40 years of climate data, for almost any place on Earth.
`→`
But this data is made for scientists, not for farmers. That is the gap.
So our idea is simple: NASA data in, rotation options out — for one field, in plain words.

`⏭️`

---

## 3 · How we built it

**MIA:**
This is how we built it.
One: the farmer draws the field on a map.
Two: we get 10 years of climate from NASA POWER, and the soil — texture and pH — from ISRIC SoilGrids.
Three: we use a library of 18 crops with FAO ranges.
Then our rules engine uses the FAO-56 water balance.
It is not a black box: every number has a source.
The result: your current rotation, plus 3 other options.

`⏭️`

---

## 4 · Live, on real NASA data

**MAURO:**
This is not a video. This is the real app, connected to our API right now.
First, we draw the field. The app measures it — 8.4 hectares — and finds the soil: loam, pH 8.
`→`
Then we choose the crop we grow today, and what matters most. Here: save water.
`→`
Now the app calls our API. Look at the top: this is a real request to NASA POWER and SoilGrids.
Every number has a simple meaning, like "dry soil".
`→`
And here are the options: our current rotation, and 3 strategies.
`→`
Each card says why, the evidence, the benefits and the risks.

**MIA:**
`→`
Now: what if next year is drier?
We move the sliders: 20% less rain, 1.5 degrees hotter.
The API calculates the plan again, live. Look at the irrigation: this field needs more water.
`→`
The app also shows when the field has no crop, gives frost and heat alerts, works offline, and makes a PDF for the agronomist.

`⏭️`

---

## 5 · Impact & validation

**MAURO:**
So, what is the impact? For this field, the recommended rotation needs 26% less irrigation per crop cycle.
Its nitrogen balance is about 58 kilos per hectare better than today. And soil health goes from 40 to 70.
These are estimates, and we say it clearly.
`→`
How do we keep it honest? Real NASA data. The FAO-56 method. Published crop ranges.
And we show the uncertainty, plus what to check locally.
Our next step: test it with real farmers and agronomists.

`⏭️`

---

## 6 · Cierre

**MIA:**
AgroBytes does not replace the farmer. It helps the farmer decide, with NASA science — for any field in North America.

**MAURO:**
From NASA data… to your field.

**LOS DOS:**
We are AgroBytes. Thank you!

---

*Los números (8.4 ha, 26 % por ciclo, 58 kg, 40 → 70) vienen en vivo de la API: si en pantalla salen otros, digan los de la pantalla. Ojo: es riego **por ciclo** (la rotación tiene más ciclos que «seguir como hoy», así que en total puede usar más agua) y si la pantalla dice "more", es "more".*
