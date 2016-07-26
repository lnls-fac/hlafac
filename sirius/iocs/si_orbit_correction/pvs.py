
numBPM = 160

pvdb = {
    'SICO-SOFB-STATUS': {'type': 'enum', 'enums': ['Off', 'OnH', 'OnV', 'OnHOnV', 'OnHV', 'OnH_F', 'OnV_F', 'OnHOnV_F', 'OnHV_F']},
    'SICO-SOFB-MEASRESPM': {'type': 'enum', 'enums': ['Off', 'OnH', 'OnV', 'OnHV', 'OnH_F', 'OnV_F', 'OnHV_F']},
    'SICO-SOFB-AVGORBIT-X': {'type': 'float', 'count': numBPM},
    'SICO-SOFB-AVGORBIT-Y': {'type': 'float', 'count': numBPM},
    'SICO-SOFB-AVGORBIT-NUMSAMPLES': {'type': 'int', 'value': 1},
    'SICO-SOFB-ERROR': {'type': 'enum', 'enums': ['None', 'MeasRespmError', 'SetAvgOrbitNumSamplesError', 'ReadOrbitError', 'SetRespmError', 'SetRefOrbitError', 'CalcEstatDataError']},
    'SICO-SOFB-RESPM': {'type': 'string', 'value': 'respm_hv_f_va'},
    'SICO-SOFB-REFORBIT-X': {'type': 'string', 'value': 'orbit_x_null'},
    'SICO-SOFB-REFORBIT-Y': {'type': 'string', 'value': 'orbit_y_null'},
    'SICO-SOFB-ORBIT-X-MEAN': {'type': 'float'},
    'SICO-SOFB-ORBIT-Y-MEAN': {'type': 'float'},
    'SICO-SOFB-ORBIT-X-MAX': {'type': 'float'},
    'SICO-SOFB-ORBIT-Y-MAX': {'type': 'float'},
    'SICO-SOFB-ORBIT-X-MIN': {'type': 'float'},
    'SICO-SOFB-ORBIT-Y-MIN': {'type': 'float'},
    'SICO-SOFB-ORBIT-X-RMS': {'type': 'float'},
    'SICO-SOFB-ORBIT-Y-RMS': {'type': 'float'},
}
