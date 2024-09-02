import json

from retriever.services.db_session_builder import db_session_builder

if __name__ == "__main__":
    # Find path

    # Schema as text
    with db_session_builder.build() as db_session:
        result = db_session.run("CALL apoc.meta.schema()")
        schema = result.single()["value"]

        with open("schema.json", "w") as f:
            json.dump(schema, f, indent=2)

    # Filter and simplify schema
    stripped_schema = {}
    nodes = []
    for key, value in schema.items():
        if value.get("type") == "node":
            node = {
                "name": key,
                "properties": [
                    {"name": prop, "type": prop_info["type"]}
                    for prop, prop_info in value["properties"].items()
                ],
                "relationships": [
                    {
                        "name": rel,
                        "from": (
                            key
                            if rel_info["direction"] == "out"
                            else rel_info["labels"][0]
                        ),
                        "to": (
                            rel_info["labels"][0]
                            if rel_info["direction"] == "out"
                            else key
                        ),
                    }
                    for rel, rel_info in value["relationships"].items()
                ],
            }
            nodes.append(node)
    stripped_schema = {"nodes": nodes}
    # Define descriptions for each node type
    node_descriptions = {
        "Membership": "Über Objekte dieses Typs wird die Mitgliedschaft von Personen in Gruppierungen dargestellt. Diese Mitgliedschaften können zeitlich begrenzt sein. Zudem kann abgebildet werden, dass eine Person eine bestimmte Rolle bzw. Position innerhalb der Gruppierung innehat, beispielsweise den Vorsitz einer Fraktion.",
        "Organization": "Dieser Objekttyp dient dazu, Gruppierungen von Personen abzubilden, die in der parlamentarischen Arbeit eine Rolle spielen. Dazu zählen in der Praxis insbesondere Fraktionen und Gremien.",
        "Meeting": "Eine Sitzung ist die Versammlung einer oder mehrerer Gruppierungen (oparl:Organization) zu einem bestimmten Zeitpunkt an einem bestimmten Ort. Die geladenen Teilnehmer der Sitzung sind jeweils als Objekte vom Typ oparl:Person, die in entsprechender Form referenziert werden. Verschiedene Dateien (Einladung, Ergebnis- und Wortprotokoll, sonstige Anlagen) können referenziert werden. Die Inhalte einer Sitzung werden durch Tagesordnungspunkte (oparl:AgendaItem) abgebildet.",
        "Paper": "Dieser Objekttyp dient der Abbildung von Drucksachen in der parlamentarischen Arbeit, wie zum Beispiel Anfragen, Anträgen und Beschlussvorlagen. Drucksachen werden in Form einer Beratung (oparl:Consultation) im Rahmen eines Tagesordnungspunkts (oparl:AgendaItem) einer Sitzung (oparl:Meeting) behandelt. Drucksachen spielen in der schriftlichen wie mündlichen Kommunikation eine besondere Rolle, da in vielen Texten auf bestimmte Drucksachen Bezug genommen wird. Hierbei kommen in parlamentarischen Informationssystemen in der Regel unveränderliche Kennungen der Drucksachen zum Einsatz.",
        "Body": "Der Objekttyp oparl:Body dient dazu, eine Körperschaft zu repräsentieren. Eine Körperschaft ist in den meisten Fällen eine Gemeinde, eine Stadt oder ein Landkreis. In der Regel sind auf einem OParl-Server Daten von genau einer Körperschaft gespeichert und es wird daher auch nur ein Body-Objekt ausgegeben. Sind auf dem Server jedoch Daten von mehreren Körperschaften gespeichert, muss für jede Körperschaft ein eigenes Body-Objekt ausgegeben werden.",
        "File": "Ein Objekt vom Typ oparl:File repräsentiert eine Datei, beispielsweise eine PDF-Datei, ein RTF- oder ODF-Dokument, und hält Metadaten zu der Datei sowie URLs zum Zugriff auf die Datei bereit. Objekte vom Typ oparl:File können unter anderem mit Drucksachen (oparl:Paper) oder Sitzungen (oparl:Meeting) in Beziehung stehen. Dies wird durch die Eigenschaft paper bzw. meeting angezeigt. Mehrere Objekte vom Typ oparl:File können mit einander in direkter Beziehung stehen, z.B. wenn sie den selben Inhalt in unterschiedlichen technischen Formaten wiedergeben. Hierfür werden die Eigenschaften masterFile bzw. derivativeFile eingesetzt. Das gezeigte Beispiel-Objekt repräsentiert eine PDF-Datei (zu erkennen an der Eigenschaft mimeType) und zeigt außerdem über die Eigenschaft masterFile an, von welcher anderen Datei es abgeleitet wurde. Umgekehrt kann über die Eigenschaft derivativeFile angezeigt werden, welche Ableitungen einer Datei existieren.",
        "Location": "Dieser Objekttyp dient dazu, einen Ortsbezug formal abzubilden. Ortsangaben können sowohl aus Textinformationen bestehen (beispielsweise dem Namen einer Straße/eines Platzes oder eine genaue Adresse) als auch aus Geodaten. Ortsangaben sind auch nicht auf einzelne Positionen beschränkt, sondern können eine Vielzahl von Positionen, Flächen, Strecken etc. abdecken.",
        "AgendaItem": "Tagesordnungspunkte sind die Bestandteile von Sitzungen (oparl:Meeting). Jeder Tagesordnungspunkt widmet sich inhaltlich einem bestimmten Thema, wozu in der Regel auch die Beratung bestimmter Drucksachen gehört. Die Beziehung zwischen einem Tagesordnungspunkt und einer Drucksache wird über ein Objekt vom Typ oparl:Consultation hergestellt, das über die Eigenschaft consultation referenziert werden kann.",
        "LegislativeTerm": "Dieser Objekttyp dient der Beschreibung einer Wahlperiode.",
        "Person": "Jede natürliche Person, die in der parlamentarischen Arbeit tätig und insbesondere Mitglied in einer Gruppierung (oparl:Organization) ist, wird mit einem Objekt vom Typ oparl:Person abgebildet.",
    }

    # Add descriptions to the nodes
    for node in stripped_schema["nodes"]:
        if node["name"] in node_descriptions:
            node["description"] = node_descriptions[node["name"]]

    # Write stripped schema to file
    with open("stripped_schema.json", "w", encoding="utf-8") as f:
        json.dump(stripped_schema, f, indent=2, ensure_ascii=False)

    # TODO Add descirptions to relationships

    # Prompt
    prompt_template = """
    You are a graph traverser. Your job is to traverse the graph of the given schema.

    I will give you an entry node (specified by its type and id) and a target node (described in natural language and by its type).


    """

    # Structured output with possible connections nothing more

    # then call and print

    # Func to convert a description of a node to a node_Type
    # def infer_node_type(description: str) -> str:
    # Have a list of node types and their descriptions
