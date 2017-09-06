import csv

from scenario import Scenario, Ref

# Columns
RFACTOR = 1
CHINU = 2

def parse_cell(cell):
    """Transformer la valeur d'une cellule en nombre. 0 s'il n'y a rien"""
    try:
        return float(cell) if cell else 0
    except Exception:
        return cell

def parse_row(line):
    """Transformer les valeurs d'une ligne en nombres"""
    return map(parse_cell, line)

def parse_scenario(line, headers, subheaders, chinu_ref):
    """Transformer une ligne en un scenario"""
    chinu = line[CHINU]
    rfactor = line[RFACTOR]
    chinu_delta = (chinu - chinu_ref) / chinu 
    scen = [Ref(headers[i], cell) for i, cell in enumerate(line) if cell and subheaders[i] == 'weight']
    return (scen, rfactor, chinu, chinu_delta)

def parse_scenarios_from_file(filename):
    """Extraire d'un CSV les scenarios"""
    with open(filename, 'rb') as csvfile:
        reader = csv.reader(csvfile)
        reader = list(reader)
    headers = reader[0]
    subheaders = reader[1]
    results = reader[2:]
    results = map(parse_row, results)
    scenarios = []
    for i, line in enumerate(results[:10]):
        if i < 2:
            continue
        line = map(lambda x: float(x) if x else 0, line)
        results[i] = line
        chinu = line[CHINU]
        chinu_ref = results[1][CHINU]
        s = parse_scenario(line, headers, subheaders, chinu_ref)
        scenario = Scenario(*([i - 1] + list(s)))
        scenarios.append(scenario)
    return scenarios
