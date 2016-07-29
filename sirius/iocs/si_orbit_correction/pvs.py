
numBPM = 160
numCH = 120
numCV = 160

pvdb = {
    'SICO-SOFB-STATUS': {'type': 'enum', 'enums': ['Off', 'OnH', 'OnV', 'OnHOnV', 'OnHV', 'OnH_F', 'OnV_F', 'OnHOnV_F', 'OnHV_F']},
    'SICO-SOFB-MEASRESPM': {'type': 'enum', 'enums': ['Off', 'OnH', 'OnV', 'OnHV', 'OnH_F', 'OnV_F', 'OnHV_F']},
    'SICO-SOFB-AVGORBIT-X': {'type': 'float', 'count': numBPM},
    'SICO-SOFB-AVGORBIT-Y': {'type': 'float', 'count': numBPM},
    'SICO-SOFB-AVGORBIT-NUMSAMPLES': {'type': 'int', 'value': 1},
    'SICO-SOFB-ERROR': {'type': 'enum', 'enums': ['None', 'MeasRespmError', 'SetAvgOrbitNumSamplesError', 'ReadOrbitError', 'SetRespmError', 'SetRefOrbitError', 'CalcEstatDataError', 'CorOrbitError', 'SetRespmSlotError', 'SetRefOrbitSlotError', 'UpdateRespmError', 'UpdateRefOrbitError']}, #0-11
    'SICO-SOFB-RESPM-SEL': {'type': 'enum', 'enums': ['user_shift', 'slot1', 'slot2']},
    'SICO-SOFB-RESPM': {'type': 'float', 'count': (numBPM*2)*(numCH+numCV+1)},
    'SICO-SOFB-REFORBIT-X-SEL': {'type': 'enum', 'enums': ['null', 'slot1', 'slot2']},
    'SICO-SOFB-REFORBIT-Y-SEL': {'type': 'enum', 'enums': ['null', 'slot1', 'slot2']},
    'SICO-SOFB-REFORBIT-X': {'type': 'float', 'count': numBPM},
    'SICO-SOFB-REFORBIT-Y': {'type': 'float', 'count': numBPM},
    'SICO-SOFB-ORBIT-X-MEAN': {'type': 'float'},
    'SICO-SOFB-ORBIT-Y-MEAN': {'type': 'float'},
    'SICO-SOFB-ORBIT-X-MAX': {'type': 'float'},
    'SICO-SOFB-ORBIT-Y-MAX': {'type': 'float'},
    'SICO-SOFB-ORBIT-X-MIN': {'type': 'float'},
    'SICO-SOFB-ORBIT-Y-MIN': {'type': 'float'},
    'SICO-SOFB-ORBIT-X-RMS': {'type': 'float'},
    'SICO-SOFB-ORBIT-Y-RMS': {'type': 'float'},
}
