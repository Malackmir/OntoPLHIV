from pathlib import Path
from rdflib import Graph

# Racine du projet OntoPLHIV
ROOT = Path(__file__).resolve().parent.parent
ONTOLOGY_DIR = ROOT / "PLHIV"

# Fichier contenant les métadonnées et les préfixes
META_FILE = ONTOLOGY_DIR / "plhiv_meta.ttl"

# Fichiers sources
SOURCES = [
    ONTOLOGY_DIR / "maladie.ttl",
    ONTOLOGY_DIR / "biologie.ttl",
    ONTOLOGY_DIR / "patient.ttl",
    ONTOLOGY_DIR / "traitement.ttl",
]

# Fichier final
OUTPUT = ONTOLOGY_DIR / "plhiv.ttl"

# 1. Charger les métadonnées
graph = Graph()
graph.parse(META_FILE.as_posix(), format="turtle")

# Conserver les préfixes des métadonnées
metadata_prefixes = list(graph.namespaces())

print(f"Métadonnées : {len(graph)} triplets")

# 2. Charger ET fusionner les quatre fichiers
for source in SOURCES:
    if not source.is_file():
        raise FileNotFoundError(
            f"Fichier introuvable : {source}"
        )

    print(f"\nChargement de : {source.name}")

    temporary_graph = Graph()

    try:
        temporary_graph.parse(
            source.as_posix(),
            format="turtle"
        )

        source_count = len(temporary_graph)

        # Fusionner les triplets du sous-domaine
        for triple in temporary_graph:
            graph.add(triple)

        # Récupérer les préfixes du sous-domaine
        for prefix, namespace in temporary_graph.namespaces():
            graph.bind(prefix, namespace, override=False)

        print(
            f"OK : {source.name} "
            f"({source_count} triplets chargés)"
        )

    except Exception as error:
        print(f"ERREUR dans : {source.name}")
        print(error)
        raise

# 3. Restaurer les préfixes de référence
for prefix, namespace in metadata_prefixes:
    graph.bind(prefix, namespace, override=True)

# 4. Générer le fichier consolidé
graph.serialize(
    destination=OUTPUT.as_posix(),
    format="turtle"
)

print("\nFusion terminée avec succès.")
print(f"Fichier généré : {OUTPUT}")
print(f"Nombre total de triplets RDF : {len(graph)}")

