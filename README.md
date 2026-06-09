# lukasbrandt.de

Persönliche Website von Lukas Brandt — statisches HTML/CSS/JS, kein Build-Schritt.

## Struktur

| Datei | Zweck |
|---|---|
| `index.html` | Hauptseite: Forschung, Publikationen, Kontakt (DE/EN, Light/Dark) |
| `impress.html` | Impressum |
| `style.css` | Styles für `index.html` |
| `i18n.js` | Übersetzungen + Sprachumschaltung für `index.html` |
| `profile.jpg` | Foto auf der Hauptseite |
| `favicon.png` | Favicon |
| `CNAME` | Custom-Domain-Eintrag für GitHub Pages |

`impress.html` ist standalone — Styles liegen inline in der Datei.

## Lokal ansehen

Reicht jeder beliebige statische Server, z. B.:

```sh
python -m http.server 8000
# dann http://localhost:8000 im Browser öffnen
```

Doppelklick auf `index.html` geht auch, dann blockiert der Browser aber teilweise lokale Fetches.

## Deployment

GitHub Pages mit Custom Domain `lukasbrandt.de` (siehe `CNAME`). Nach dem ersten Push: in den Repo-Settings → Pages die Domain registrieren und beim DNS-Provider den `CNAME`-Eintrag setzen.

## Offene Punkte

- Datenschutzerklärung anlegen (Google Fonts werden aktuell vom Google-CDN geladen)
- Favicon ggf. austauschen (aktuell `favicon.png` aus der Vorlage)
- OG-Image für Social-Media-Previews
