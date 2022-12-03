data = [
    "Blutige Ausbeute",
    "Jetmir, Nexus der Feierlichkeiten",
    "Mantel aus Flüsterseide",
    "Loyaler Wächter",
    "Wertberichtigung",
    "Ghired, Konklave-Exilant (V.1)",
    "Erleuchteter Lehrmeister",
    "Loyaler Wächter",
    "Ruf der Nachtschwinge",
    "Unheilige Transfusion",
    "Hof der List",
    "Stunde der Abrechnung",
    "Entdeckungen der Sippe",
    "Aufhetzerei",
    "Eldrazi-Monument",
    "Mykoloth",
    "Ezuris Hetzjagd",
    "Aufklärungsmission",
    "Ruf nach Führung",
    "Aurascherben",
    "Geistreicher Röstmeister",
    "Verrücktmachender Missklang",
    "Unheilige Transfusion",
    "Göttliche Erscheinung",
    "Stunde der Abrechnung",
    "Idyllischer Lehrmeister",
    "Eldrazi-Monument"

]

if __name__ == "__main__":
    out = []
    for x in data:
        if x in out:
            print(x)
        else:
            out.append(x)
