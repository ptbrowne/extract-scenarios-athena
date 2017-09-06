Extraction de scénarios
=======================

A partir du fichier Excel généré par Athena

1. Le réenregistrer en CSV
2. Utiliser `extract_scenarios.py` pour extraire les scénarios

```bash
$ python extract_scenarios.py Zn_GrandPradoA_subs_LCF_2refs.csv
Name    Ref1    Ref2    R-factor        Chinu   Chinu Delta
Scenario 1      nano-ZnS-E_dec2015 * 94.1%      Zn_sorbed_Fhyd_synthe Marie_SSRL_He * 8.2%      0.0042055       0.0021459       0.0198052099352
Scenario 2      Zn_Phytate_FAME_He * 9.83%      B_decembre_2016_030_001_tr.avg * 90.6%  0.004268        0.0021778       0.0341629167049
Scenario 3      nano-ZnS-E_dec2015 * 95.02%     Zn_Phytate_FAME_He * 6.84%      0.0043339       0.0022114       0.0488378402822
Scenario 4      nano-ZnS-E_dec2015 * 94.28%     Zn3(PO4)2_SSRL_He * 7.87%       0.0044471       0.0022692       0.0730653974969
Scenario 5      nano-ZnS-E_dec2015 * 93.52%     Kaolinite Zn High_Voegelin_FAME_He * 8.38%      0.0044711       0.0022814       0.078022267029
Scenario 6      nano-ZnS-E_dec2015 * 94.04%     Zn_Methionine_FAME_He * 6.98%   0.0047159       0.0024063       0.125877903836
Scenario 7      B_decembre_2016_030_001_tr.avg * 88.6%  Kaolinite Zn High_Voegelin_FAME_He * 11.76%     0.0047706       0.0024342       0.135896803878
Scenario 8      Zn_Methionine_FAME_He * 10.23%  B_decembre_2016_030_001_tr.avg * 89.15% 0.0047853       0.0024418       0.138586288803

Scenario 1
nano-ZnS-E_dec2015 * 94.1%
Zn_sorbed_Fhyd_synthe Marie_SSRL_He * 8.2%

Scenario 2
Zn_Phytate_FAME_He * 9.83%
B_decembre_2016_030_001_tr.avg * 90.6%

Scenario 3
nano-ZnS-E_dec2015 * 95.02%
Zn_Phytate_FAME_He * 6.84%

Scenario 4
nano-ZnS-E_dec2015 * 94.28%
Zn3(PO4)2_SSRL_He * 7.87%

Scenario 5
nano-ZnS-E_dec2015 * 93.52%
Kaolinite Zn High_Voegelin_FAME_He * 8.38%

Scenario 6
nano-ZnS-E_dec2015 * 94.04%
Zn_Methionine_FAME_He * 6.98%

Scenario 7
B_decembre_2016_030_001_tr.avg * 88.6%
Kaolinite Zn High_Voegelin_FAME_He * 11.76%

Scenario 8
Zn_Methionine_FAME_He * 10.23%
B_decembre_2016_030_001_tr.avg * 89.15%
```