# -*- coding: utf-8 -*-

from itertools import islice, chain
from parse import parse_scenarios_from_file

def output_scenarios(scenarios):
    print('\t'.join(['Name', 'Ref1', 'Ref2', 'R-factor', 'Chinu', 'Chinu Delta']))
    for i, scenario in enumerate(scenarios):
        if scenario.chinu_delta < 0.2:
            print(scenario.as_line())
    print()
    for scenario in scenarios:
        if scenario.chinu_delta < 0.2:
            print(scenario.as_block())
            print()

if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()
    scenarios = parse_scenarios_from_file(args.filename)
    output_scenarios(scenarios)