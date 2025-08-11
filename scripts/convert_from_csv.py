#!/usr/bin/env python3

import rdflib
import csv
from argparse import ArgumentParser
from pathlib import Path

JSON_LD_CONTEXT = {
    "skos": "http://www.w3.org/2004/02/skos/core#",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
}


def main():
    parser = ArgumentParser()
    parser.add_argument("inputfile")
    args = parser.parse_args()
    filename = args.inputfile
    g = rdflib.Graph()
    glossary_subject = rdflib.URIRef("https://popular-print-glossary.sites.uu.nl/glossary/")
    with open(filename) as f:
        reader = csv.DictReader(f, delimiter=',')
        for row in reader:
            uri = row['Permalink']
            term = row['Title']
            alias = row['Alias']
            subject = rdflib.URIRef(uri)
            label = rdflib.Literal(term)
            if alias:
                # If alias is filled, this row defines an alias for a main term.
                # (We don't need the value of alias, because the main term is given here)
                g.add((subject, rdflib.SKOS.altLabel, label))
            else:
                g.add((subject, rdflib.RDFS.member, glossary_subject))
                g.add((subject, rdflib.SKOS.prefLabel, label))

    save_path = Path(__file__).parent.parent  # Save in root directory of repository
    g.serialize(save_path / 'gemppg.ttl', format='turtle')
    g.serialize(save_path / 'gemppg.json', format='json-ld', context=JSON_LD_CONTEXT)

if __name__ == "__main__":
    main()
