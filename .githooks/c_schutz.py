"""C-Schutz: Pre-commit-Pruefung gegen personenbezogene Daten Dritter (Schutzklasse C).

Identische Kopie in forschung, lehre und privat (jeweils .githooks/). Aenderungen in
allen drei Repos gleich nachziehen; die Versionszeile unten hilft beim Abgleich.

Was geprueft wird (nur vorgemerkte Dateien, im Stand des Index):
  - Namen aus den Listen der C-Ablage (nur vollstaendige Paare aus Vor- und Nachname),
    auch im Inneren von docx, pptx, xlsx, odt, pdf und xls
  - Matrikelnummern und E-Mail-Adressen aus diesen Listen, dazu das Muster
    "Matrikel..." mit Nummer (ausser den eigenen Nummern in _c_schutz\\eigene_nummern.txt)
  - Datendateien (SPSS, Access, Audio, Video)
  - neu hinzugefuegte Dateien, die .gitignore eigentlich ausschliesst (git add -f)

Die Listen werden nur zur Laufzeit gelesen. Gespeichert wird nichts, und die Meldung
nennt nur Datei und Trefferart, nie einen Namen.

Aufrufe:
  python .githooks/c_schutz.py --hook                 (vom Hook pre-commit)
  python .githooks/c_schutz.py --alle                 (alle getrackten Dateien pruefen)
  python .githooks/c_schutz.py --ausnahme PFAD GRUND  (Fehlalarm fuer genau diesen Stand freigeben)

Umgebung: C_SCHUTZ_ABLAGE ersetzt den Ort der C-Ablage (Standard %USERPROFILE%\\C-Ablage).
"""

VERSION = "c_schutz 1.2 (04.11.2026)"

import datetime
import html
import io
import json
import os
import re
import subprocess
import sys
import unicodedata
import zipfile

AUSNAHMEN = os.path.join(".githooks", "c_schutz_ausnahmen.tsv")
DATEN_ENDUNGEN = {
    ".sav": "SPSS-Datensatz", ".zsav": "SPSS-Datensatz", ".por": "SPSS-Datensatz",
    ".mdb": "Access-Datenbank", ".accdb": "Access-Datenbank",
    ".mp4": "Video", ".mov": "Video", ".avi": "Video", ".mkv": "Video", ".mts": "Video", ".wmv": "Video",
    ".wav": "Audio", ".m4a": "Audio", ".mp3": "Audio", ".wma": "Audio", ".aac": "Audio", ".flac": "Audio",
}
TEXT_ENDUNGEN = {
    ".txt", ".md", ".csv", ".tsv", ".json", ".yml", ".yaml", ".xml", ".html", ".htm", ".tex", ".bib",
    ".r", ".rmd", ".qmd", ".py", ".ps1", ".sh", ".js", ".css", ".ics", ".log", ".sps", ".ini", ".cfg",
}
MAX_GROESSE = 200 * 1024 * 1024
STOPPWOERTER = {
    "gruppe", "gruppen", "sitzung", "thema", "termin", "stand", "notiz", "seminar", "kurs", "pg",
    "dr", "prof", "herr", "frau", "und", "der", "die", "das",
}
MATRIKEL_MUSTER = re.compile(r"(?i)\b(?:matrikel(?:nummer|nr)?|matr\.?|mtknr|mat\.)\s*-?\s*(?:nr\.?|nummer)?\W{0,20}(\d{5,8})(?!\d)")
ZAHL = re.compile(r"(?<!\d)\d{5,8}(?!\d)")
MAIL = re.compile(r"(?<![\w.+-])[\w.+-]{1,64}@[\w-]{1,63}(?:\.[\w-]{1,63})+")  # linear, auch bei Base64
WORT = re.compile(r"[^\W\d_]+(?:[-'][^\W\d_]+)*")
TRANS = str.maketrans({"ä": "ae", "ö": "oe", "ü": "ue", "ß": "ss", "‑": "-", "‐": "-",
                       "–": "-", "’": "'", "­": ""})


def norm(text):
    t = text.casefold().translate(TRANS)
    t = unicodedata.normalize("NFKD", t)
    return "".join(c for c in t if not unicodedata.combining(c))


def woerter(text):
    return WORT.findall(norm(text))


def meldung(*teile):
    print(*teile, file=sys.stderr)


def git(*args, eingabe=None):
    r = subprocess.run(["git", *args], input=eingabe, capture_output=True)
    if r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)}: {r.stderr.decode(errors='replace').strip()}")
    return r.stdout


# ---------------------------------------------------------------- Quellen (C-Ablage)

class Quellen:
    def __init__(self):
        self.namen = set()      # Tupel normalisierter Woerter
        self.laengen = set()
        self.matrikel = set()
        self.mails = set()
        self.eigene = set()     # eigene Nummern (kein C), aus _c_schutz\eigene_nummern.txt
        self.dateien = 0
        self.fehler = []

    def person(self, nachname, vorname):
        s = [w for w in woerter(str(nachname)) if len(w) >= 2]
        g = [w for w in woerter(str(vorname)) if len(w) >= 2]
        if not s or not g or set(s + g) & STOPPWOERTER:
            return
        formen = {(*g, *s), (*s, *g)} | {(v, *s) for v in g} | {(*s, v) for v in g}
        for t in formen:
            self.namen.add(t)
            self.laengen.add(len(t))

    def vollname(self, text):
        text = str(text).strip()
        if not text:
            return
        if "," in text:
            nach, vor = text.split(",", 1)
            self.person(nach, vor)
        else:
            w = text.split()
            if len(w) >= 2:
                self.person(w[-1], " ".join(w[:-1]))

    def matrikelwert(self, wert):
        if wert is None:
            return
        if isinstance(wert, float) and wert.is_integer():
            wert = int(wert)
        s = re.sub(r"\s", "", str(wert))
        if re.fullmatch(r"\d{5,8}", s):
            self.matrikel.add(s)

    def mailwert(self, wert):
        if wert and "@" in str(wert):
            self.mails.add(str(wert).strip().lower())

    def tabelle(self, zeilen):
        kopf = None
        for zi, zeile in enumerate(zeilen[:15]):
            k = [norm(str(z)).strip() if z is not None else "" for z in zeile]
            if any(re.search(r"name|matr|mtknr|matrikel", x) for x in k):
                kopf = (zi, k)
                break
        if not kopf:
            return
        zi, k = kopf
        sp = {"nach": None, "vor": None, "voll": None, "matr": [], "mail": []}
        for i, x in enumerate(k):
            if not x:
                continue
            if "nachname, vorname" in x or "name, vorname" in x:
                sp["voll"] = i
            elif x in ("vorname", "vornamen") or x.startswith("vorname"):
                sp["vor"] = i
            elif x in ("name", "nachname", "familienname") or x.startswith("nachname"):
                sp["nach"] = i
            if re.search(r"matr|mtknr|matrikel", x):
                sp["matr"].append(i)
            if "mail" in x:
                sp["mail"].append(i)
        if sp["nach"] is not None and sp["vor"] is None:
            sp["voll"], sp["nach"] = sp["nach"], None
        for zeile in zeilen[zi + 1:]:
            zeile = list(zeile)

            def zelle(i):
                return zeile[i] if i is not None and i < len(zeile) else None

            if sp["voll"] is not None and zelle(sp["voll"]):
                self.vollname(zelle(sp["voll"]))
            if sp["nach"] is not None and sp["vor"] is not None and zelle(sp["nach"]) and zelle(sp["vor"]):
                self.person(zelle(sp["nach"]), zelle(sp["vor"]))
            for i in sp["matr"]:
                self.matrikelwert(zelle(i))
            for i in sp["mail"]:
                self.mailwert(zelle(i))

    def json_werte(self, x):
        if isinstance(x, dict):
            for v in x.values():
                self.json_werte(v)
        elif isinstance(x, list):
            for v in x:
                self.json_werte(v)
        elif isinstance(x, str):
            teile = [t.strip() for t in re.split(r"[,;\n]", x) if t.strip()]
            namenartig = [t for t in teile
                          if 2 <= len(t.split()) <= 4 and all(w[:1].isupper() and len(w) >= 2 for w in t.split())]
            if len(teile) >= 2 and len(namenartig) == len(teile):
                for t in teile:
                    w = t.split()
                    self.person(w[-1], " ".join(w[:-1]))

    def lade(self, basis):
        lehre = os.path.join(basis, "lehre")
        for wurzel, _, dateien in os.walk(lehre):
            for d in dateien:
                p = os.path.join(wurzel, d)
                e = os.path.splitext(d)[1].lower()
                try:
                    if e == ".xlsx":
                        import openpyxl
                        wb = openpyxl.load_workbook(p, read_only=True, data_only=True)
                        for ws in wb.worksheets:
                            self.tabelle([list(r) for r in ws.iter_rows(values_only=True)])
                        wb.close()
                    elif e == ".xls":
                        import xlrd
                        wb = xlrd.open_workbook(p)
                        for sh in wb.sheets():
                            self.tabelle([sh.row_values(i) for i in range(sh.nrows)])
                    elif e == ".csv":
                        with open(p, "r", encoding="utf-8-sig", errors="replace") as f:
                            text = f.read()
                        trenner = ";" if text.count(";") > text.count(",") else ","
                        self.tabelle([z.split(trenner) for z in text.splitlines()])
                    elif e == ".json":
                        with open(p, "r", encoding="utf-8") as f:
                            self.json_werte(json.load(f))
                    else:
                        continue
                    self.dateien += 1
                except Exception as ex:  # eine kaputte Liste soll den Rest nicht verhindern
                    self.fehler.append(f"{os.path.relpath(p, basis)}: {type(ex).__name__}")
        zusatz = os.path.join(basis, "_c_schutz", "zusatznamen.txt")
        if os.path.isfile(zusatz):
            with open(zusatz, "r", encoding="utf-8-sig") as f:
                for zeile in f:
                    zeile = zeile.strip()
                    if zeile and not zeile.startswith("#"):
                        self.vollname(zeile)
            self.dateien += 1
        eigen = os.path.join(basis, "_c_schutz", "eigene_nummern.txt")
        if os.path.isfile(eigen):
            with open(eigen, "r", encoding="utf-8-sig") as f:
                self.eigene = {z.strip() for z in f if re.fullmatch(r"\d{5,8}", z.strip())}


# ---------------------------------------------------------------- Text aus Dateien

XML_TRENNER = re.compile(r"</(?:w:p|a:p|si|c|row|text:p|text:h)>|<(?:w:tab|w:br|a:br|text:tab|text:s)\b[^>]*/>")
TAG = re.compile(r"<[^>]+>")


def xml_text(daten):
    t = daten.decode("utf-8", errors="replace")
    t = XML_TRENNER.sub(" ", t)
    return html.unescape(TAG.sub("", t))


def text_aus(pfad, daten):
    e = os.path.splitext(pfad)[1].lower()
    teile = [pfad.replace("_", " ").replace("/", " ")]
    try:
        if daten[:2] == b"PK":
            with zipfile.ZipFile(io.BytesIO(daten)) as z:
                for info in z.infolist():
                    n = info.filename.lower()
                    if info.file_size > MAX_GROESSE or n.startswith(("word/media", "ppt/media", "xl/media")):
                        continue
                    ne = os.path.splitext(n)[1]
                    if ne == ".xml" and "/theme" not in n and not n.endswith(("styles.xml", "fonttable.xml", "settings.xml")):
                        teile.append(xml_text(z.read(info)))
                    elif ne in TEXT_ENDUNGEN:
                        teile.append(z.read(info).decode("utf-8", errors="replace"))
        elif daten[:5] == b"%PDF-":
            import fitz
            with fitz.open(stream=daten, filetype="pdf") as doc:
                teile.extend(seite.get_text() for seite in doc)
        elif e == ".xls" or daten[:8] == b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1":
            if e != ".xls":
                return "\n".join(teile), "Office-Altformat, Inhalt nicht geprueft"
            import xlrd
            wb = xlrd.open_workbook(file_contents=daten)
            for sh in wb.sheets():
                for i in range(sh.nrows):
                    teile.append(" ".join(str(v) for v in sh.row_values(i)))
        elif e in TEXT_ENDUNGEN or b"\x00" not in daten[:8192]:
            try:
                teile.append(daten.decode("utf-8"))
            except UnicodeDecodeError:
                teile.append(daten.decode("cp1252", errors="replace"))
    except Exception as ex:
        return "\n".join(teile), f"nicht lesbar ({type(ex).__name__})"
    return "\n".join(teile), None


# ---------------------------------------------------------------- Pruefung

def pruefe(pfad, daten, quellen):
    befund = {}

    def plus(art, n=1):
        befund[art] = befund.get(art, 0) + n

    e = os.path.splitext(pfad)[1].lower()
    if e in DATEN_ENDUNGEN:
        plus(f"Datendatei ({DATEN_ENDUNGEN[e]})")
    if len(daten) > MAX_GROESSE:
        return befund, "zu gross fuer die Inhaltspruefung"
    text, hinweis = text_aus(pfad, daten)
    if quellen is not None:
        w = woerter(text)
        if quellen.namen:
            for i in range(len(w)):
                for L in quellen.laengen:
                    if i + L <= len(w) and tuple(w[i:i + L]) in quellen.namen:
                        plus("Name aus C-Liste")
                        break
        if quellen.matrikel:
            n = sum(1 for z in ZAHL.findall(text) if z in quellen.matrikel)
            if n:
                plus("Matrikelnummer aus C-Liste", n)
        if quellen.mails:
            n = sum(1 for m in MAIL.findall(text) if m.lower() in quellen.mails)
            if n:
                plus("E-Mail aus C-Liste", n)
    eigene = quellen.eigene if quellen is not None else set()
    n = sum(1 for z in MATRIKEL_MUSTER.findall(text) if z not in eigene)
    if n:
        plus("Matrikelnummer-Muster", n)
    return befund, hinweis


def blobs_lesen(shas):
    """Liest Blobs ueber eine einzige git cat-file --batch Verbindung."""
    if not shas:
        return {}
    eingabe = ("\n".join(shas) + "\n").encode()
    roh = git("cat-file", "--batch", eingabe=eingabe)
    aus, pos = {}, 0
    for sha in shas:
        ende = roh.index(b"\n", pos)
        kopf = roh[pos:ende].decode().split()
        pos = ende + 1
        if len(kopf) < 3 or kopf[1] == "missing":
            aus[sha] = b""
            continue
        groesse = int(kopf[2])
        aus[sha] = roh[pos:pos + groesse]
        pos += groesse + 1
    return aus


def ausnahmen():
    frei = set()
    if os.path.isfile(AUSNAHMEN):
        with open(AUSNAHMEN, "r", encoding="utf-8") as f:
            for zeile in f:
                teile = zeile.rstrip("\n").split("\t")
                if teile and re.fullmatch(r"[0-9a-f]{40,64}", teile[0]):
                    frei.add(teile[0])
    return frei


def quellen_laden():
    basis = os.environ.get("C_SCHUTZ_ABLAGE") or os.path.join(os.path.expanduser("~"), "C-Ablage")
    if not os.path.isdir(basis):
        meldung(f"C-Schutz: C-Ablage nicht gefunden ({basis}); geprueft werden nur Dateitypen und Muster.")
        return None
    q = Quellen()
    q.lade(basis)
    for f in q.fehler:
        meldung(f"C-Schutz: Liste nicht lesbar: {f}")
    return q


def vorgemerkt():
    roh = git("diff", "--cached", "--raw", "-z", "--no-abbrev", "--diff-filter=ACMR")
    teile = roh.split(b"\x00")
    eintraege, i = [], 0
    while i < len(teile) - 1:
        kopf = teile[i].decode()
        if not kopf.startswith(":"):
            i += 1
            continue
        felder = kopf[1:].split()
        status, neu = felder[4], felder[3]
        if status[0] in "RC":
            pfad = teile[i + 2].decode("utf-8", errors="replace")
            i += 3
        else:
            pfad = teile[i + 1].decode("utf-8", errors="replace")
            i += 2
        eintraege.append((status[0], neu, pfad))
    return eintraege


def ignoriert(pfade):
    if not pfade:
        return set()
    r = subprocess.run(["git", "check-ignore", "--no-index", "--stdin", "-z"],
                       input=b"\x00".join(p.encode() for p in pfade) + b"\x00", capture_output=True)
    return {p.decode("utf-8", errors="replace") for p in r.stdout.split(b"\x00") if p}


def bericht(treffer, kopfzeile):
    meldung(kopfzeile)
    for pfad, befund in treffer:
        meldung(f"  {pfad}: " + ", ".join(f"{k} ({v})" for k, v in sorted(befund.items())))


def hook():
    eintraege = vorgemerkt()
    if not eintraege:
        return 0
    frei = ausnahmen()
    eintraege = [e for e in eintraege if e[1] not in frei]
    if not eintraege:
        return 0
    quellen = quellen_laden()
    neu_ignoriert = ignoriert([p for s, _, p in eintraege if s == "A"])
    inhalte = blobs_lesen([sha for _, sha, _ in eintraege])
    treffer, hinweise = [], []
    for status, sha, pfad in eintraege:
        befund, hinweis = pruefe(pfad, inhalte.get(sha, b""), quellen)
        if pfad in neu_ignoriert:
            befund["von .gitignore ausgeschlossen, trotzdem hinzugefuegt"] = 1
        if befund:
            treffer.append((pfad, befund))
        if hinweis:
            hinweise.append(f"  {pfad}: {hinweis}")
    if hinweise:
        meldung("C-Schutz: Hinweis, nicht vollstaendig geprueft:")
        meldung("\n".join(hinweise))
    if not treffer:
        return 0
    bericht(treffer, f"C-Schutz: Commit angehalten. Verdacht auf personenbezogene Daten Dritter (Schutzklasse C) in {len(treffer)} Datei(en):")
    meldung("")
    meldung("Was tun: Datei pruefen; C-Inhalte gehoeren in die C-Ablage, nicht ins Repo.")
    meldung("Fehlalarm? Dann genau diesen Stand freigeben und erneut committen:")
    meldung('  python .githooks/c_schutz.py --ausnahme <pfad> "<Grund ohne Namen>"')
    return 1


def alle():
    quellen = quellen_laden()
    if quellen is not None:
        meldung(f"C-Schutz: {quellen.dateien} Listen gelesen, {len(quellen.namen)} Namensformen, "
                f"{len(quellen.matrikel)} Matrikelnummern, {len(quellen.mails)} Adressen.")
    roh = git("ls-files", "-s", "-z")
    eintraege = []
    for z in roh.split(b"\x00"):
        if z:
            kopf, pfad = z.split(b"\t", 1)
            eintraege.append((kopf.split()[1].decode(), pfad.decode("utf-8", errors="replace")))
    frei = ausnahmen()
    treffer, nicht = [], 0
    for start in range(0, len(eintraege), 200):
        block = eintraege[start:start + 200]
        inhalte = blobs_lesen([sha for sha, _ in block])
        for sha, pfad in block:
            if sha in frei:
                continue
            befund, hinweis = pruefe(pfad, inhalte.get(sha, b""), quellen)
            if hinweis:
                nicht += 1
            if befund:
                treffer.append((pfad, befund))
    bericht(treffer, f"C-Schutz --alle: {len(eintraege)} Dateien geprueft, {len(treffer)} mit Befund, {nicht} nicht vollstaendig lesbar.")
    return 1 if treffer else 0


def ausnahme(pfad, grund):
    zeile = git("ls-files", "-s", "--", pfad).decode().strip()
    if not zeile:
        meldung(f"C-Schutz: {pfad} ist nicht vorgemerkt (git add fehlt?).")
        return 2
    sha = zeile.split()[1]
    os.makedirs(os.path.dirname(AUSNAHMEN), exist_ok=True)
    neu = not os.path.isfile(AUSNAHMEN)
    with open(AUSNAHMEN, "a", encoding="utf-8", newline="\n") as f:
        if neu:
            f.write("# Freigegebene Fehlalarme des C-Schutzes: Blob-Hash, Pfad, Grund, Datum. Gilt nur fuer genau diesen Stand.\n")
        f.write(f"{sha}\t{pfad}\t{grund}\t{datetime.date.today().isoformat()}\n")
    git("add", "--", AUSNAHMEN)
    meldung(f"C-Schutz: Ausnahme fuer {pfad} ({sha[:10]}) eingetragen und vorgemerkt.")
    return 0


def main(argv):
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    if argv[:1] == ["--hook"]:
        return hook()
    if argv[:1] == ["--alle"]:
        return alle()
    if argv[:1] == ["--ausnahme"] and len(argv) >= 3:
        return ausnahme(argv[1], " ".join(argv[2:]))
    if argv[:1] == ["--version"]:
        print(VERSION)
        return 0
    meldung(__doc__)
    return 2


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except Exception as ex:
        meldung(f"C-Schutz: interner Fehler ({type(ex).__name__}: {ex}). Commit angehalten; bitte melden.")
        sys.exit(1)
