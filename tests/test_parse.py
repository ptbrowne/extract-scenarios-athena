import sys
import os.path as osp

test_dir = osp.dirname(__file__)
sys.path.append(osp.abspath(osp.join(test_dir, '..')))

from scenario import Scenario

def float_equal(f1, f2):
    return abs(f2 - f1) < 0.00001

def test_parse():
    test_file = osp.join(test_dir, 'Zn_Clos_sub_SSRL_LCF_2refs.csv')
    scenarios = Scenario.from_file(test_file)
    
    # First scenario
    assert scenarios[0].id == 1
    assert scenarios[0].rfactor == 0.0123688
    assert scenarios[0].chinu == 0.1907206
    assert scenarios[0].rfactor_delta == 0

    # Second scenario
    assert scenarios[1].id == 2
    assert scenarios[1].rfactor == 0.0138136
    assert scenarios[1].chinu == 0.2108279
    assert float_equal(scenarios[1].rfactor_delta, 11.6810038161)
