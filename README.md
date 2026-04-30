# simonfiller.eu

Persönliche Website von Simon Filler — statisches HTML/CSS/JS, kein Build-Schritt.

## Struktur

| Datei | Zweck |
|---|---|
| `index.html` | Hauptseite: Forschung, Publikationen, Kontakt (DE/EN, Light/Dark) |
| `matrix.html` | „Rabbit Hole" — Coaching / Mentoring / Beratung |
| `impress.html` | Impressum |
| `style.css` | Styles für `index.html` |
| `i18n.js` | Übersetzungen + Sprachumschaltung für `index.html` |
| `profile.jpg` | Foto auf der Hauptseite |
| `avatar.jpg` | Foto auf der Rabbit-Hole-Seite |

`matrix.html` und `impress.html` sind standalone — Styles und Skripte liegen jeweils inline in der Datei.

## Lokal ansehen

Reicht jeder beliebige statische Server, z.B.:

```sh
python -m http.server 8000
# dann http://localhost:8000 im Browser öffnen
```

Doppelklick auf `index.html` geht auch, dann blockiert der Browser aber teilweise lokale Fetches.

## Deployment

Geplant: Custom Domain `simonfiller.eu`. Konkretes Setup folgt.

## Offene Punkte

- Impressum: Adresse, Telefon, ggf. USt-IdNr. ergänzen
- Datenschutzerklärung anlegen (Google Fonts werden aktuell vom Google-CDN geladen)
- Favicon (`favicon.ico` / `favicon.svg`) bereitstellen
