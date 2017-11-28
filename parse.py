import csv

from scenario import Scenario, Ref

# Columns
RFACTOR = 0
CHINU = 1

def parse_cell(cell):
    """Transformer la valeur d'une cellule en nombre. 0 s'il n'y a rien"""
    try:
        return float(cell) if cell else 0
    except Exception:
        return cell

def parse_row(line):
    """Transformer les valeurs d'une ligne en nombres"""
    return map(parse_cell, line)

def parse_scenario(line, headers, subheaders, ref_line):
    """Transformer une ligne en un scenario"""
    chinu = line[CHINU]
    rfactor = line[RFACTOR]
    rfactor_ref = ref_line[RFACTOR]
    rfactor_delta = (rfactor - rfactor_ref) / rfactor_ref * 100
    refs = [Ref(headers[i], cell) for i, cell in enumerate(line) if cell and subheaders[i] == 'weight']
    refs = sorted(refs, key=lambda ref: -ref.weight)
    return (refs, rfactor, chinu, rfactor_delta)

def parse_scenarios_from_file(filename, limit=10):
    """Extraire d'un CSV les scenarios"""
    with open(filename, 'rb') as csvfile:
        reader = csv.reader(csvfile)
        reader = list(reader)
    headers = reader[0]
    subheaders = reader[1]
    results = reader[2:]
    results = map(parse_row, results)
    scenarios = []
    ref_line = results[0]
    for i, line in enumerate(results[:limit]):
        line = map(lambda x: float(x) if x else 0, line)
        results[i] = line
        chinu = line[CHINU]
        s = parse_scenario(line, headers, subheaders, ref_line)
        scenario_id = i + 1
        scenario = Scenario(*([scenario_id] + list(s)))
        scenarios.append(scenario)
    return scenarios
