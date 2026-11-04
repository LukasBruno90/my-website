# Repo my-website — persönliche Website

*Lukas Conrad Brandt. Stand: 24. August 2026.*

---

## Was ist das hier

Die statische persönliche Website: `index.html`, Zweisprachigkeit über `i18n.js`, dazu Impressum, Datenschutz, 404 und `CNAME` für die eigene Domain. Kein Build-System.

## Was hier NICHT geführt wird

| Thema | Führender Ort |
|---|---|
| Forschungsschwerpunkte — die homepage-reife Fassung DE + EN | `forschung/habil/forschungsschwerpunkte.md` |
| Lebenslauf und Bewerbungsmaterial | `privat/karriere/bewerbungen` |
| Publikationsliste | `forschung/publikationen/paper` · `forschung/wahlvip/diss` |

**Die Website ist ein Ausspielkanal, keine Quelle.** Inhalte kommen aus den Repos oben; hier steht nur die Darstellung. Bei Aktualisierung des Profils dort ändern und hier nachziehen.

## Verbund

*Ein Thema hat genau einen führenden Ort; die Wegweiser stehen in den Wurzel-CLAUDE.md von `forschung` und `privat`.*

**Sprache:** Deutsch. **Commits macht Claude, gepusht wird von Lukas.**

**Öffentlich:** Das Repo ist öffentlich; was hier gepusht wird, steht sofort im Netz. `_config.yml` hält `CLAUDE.md` und `README.md` aus der Website heraus.

**C-Schutz vor jedem Commit:** `.githooks/c_schutz.py` (aktiv über `core.hooksPath`, greift auch in GitHub Desktop) prüft die vorgemerkten Dateien auf Namen, Matrikelnummern und Mailadressen aus den Listen der C-Ablage, auch im Inneren von docx, pptx, xlsx und pdf, dazu Datendateien und mit `git add -f` erzwungene Dateien. Schlägt er an: nicht mit `--no-verify` umgehen, sondern Datei und Trefferart nennen (ohne Namen). Fehlalarme gibt nur Lukas frei (`python .githooks/c_schutz.py --ausnahme <pfad> "<Grund>"`).
