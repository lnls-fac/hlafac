
numBPM = 160

pvdb = {
    'SICO-SOFB-STATUS': {'type': 'enum', 'enums': ['Off', 'OnH', 'OnV', 'OnHOnV', 'OnHV', 'OnH_F', 'OnV_F', 'OnHOnV_F', 'OnHV_F']},
    'SICO-SOFB-MEASRESPM': {'type': 'enum', 'enums': ['Off', 'OnH', 'OnV', 'OnHV']},
    'SICO-SOFB-AVGORBIT-X': {'type': 'float', 'count': numBPM},
    'SICO-SOFB-AVGORBIT-Y': {'type': 'float', 'count': numBPM},
    'SICO-SOFB-AVGORBIT-NUMSAMPLES': {'type': 'int', 'value': 1},
    'SICO-SOFB-ERROR': {'type': 'enum', 'enums': ['None', 'MeasRespmError', 'SetAvgOrbitNumSamplesError', 'ReadOrbitError', 'SetRespmError']},
    'SICO-SOFB-RESPM': {'type': 'string', 'value': 'respm_hv_f_va'},
}
