
from pathlib import Path
from rdflib import Graph

ROOT = Path("PLHIV")

FORMATS = {
    ".ttl": "turtle",
    ".rdf": "xml",
    ".owl": "xml",
    ".jsonld": "json-ld",
}

def main():
    if not ROOT.exists():
        raise SystemExit("ERREUR : dossier PLHIV absent")

    files = [
        p for p in ROOT.rglob("*")
        if p.is_file() and p.suffix.lower() in FORMATS
    ]

    if not files:
        raise SystemExit("ERREUR : aucune ontologie trouvee")

    errors = []

    for path in files:
        try:
            graph = Graph()
            graph.parse(
                str(path),
                format=FORMATS[path.suffix.lower()]
            )
            print(f"OK : {path} ({len(graph)} triplets)")
        except Exception as exc:
            errors.append(path)
            print(f"ERREUR : {path} : {exc}")

    if errors:
        raise SystemExit(
            f"{len(errors)} fichier(s) invalide(s)"
        )

    print(f"Validation terminee : {len(files)} fichier(s)")

if __name__ == "__main__":
    main()