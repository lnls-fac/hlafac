
import numpy as _np

numBPM = 160
numCH = 120
numCV = 160

pvdb = {
    'SICO-SOFB-MODE': {'type': 'enum', 'enums': ['Off', 'Corr-OnH', 'Corr-OnV', 'Corr-OnHOnV', 'Corr-OnHV', 'Corr-OnH_F', 'Corr-OnV_F', 'Corr-OnHOnV_F', 'Corr-OnHV_F', 'MeasRespm-OnH', 'MeasRespm-OnV', 'MeasRespm-OnHV', 'MeasRespm-OnH_F', 'MeasRespm-OnV_F', 'MeasRespm-OnHV_F']},
    'SICO-SOFB-AVGORBIT-X': {'type': 'float', 'count': numBPM},
    'SICO-SOFB-AVGORBIT-Y': {'type': 'float', 'count': numBPM},
    'SICO-SOFB-AVGORBIT-NUMSAMPLES': {'type': 'int', 'value': 1},
    'SICO-SOFB-ERROR': {'type': 'enum', 'enums': ['None', 'MeasRespmError', 'SetAvgOrbitNumSamplesError', 'ReadOrbitError', 'SetRespmError', 'SetRefOrbitError', 'CalcEstatDataError', 'CorrOrbitError', 'SetRespmSlotError', 'SetRefOrbitSlotError', 'UpdateRespmError', 'UpdateRefOrbitError', 'DeviceSelError']}, #0-12
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
    'SICO-SOFB-BPM-SEL': {'type': 'int', 'count': numBPM},
    'SICO-SOFB-CH-SEL': {'type': 'int', 'count': numCH},
    'SICO-SOFB-CV-SEL': {'type': 'int', 'count': numCV},
    'SICO-SOFB-BPM-RMV': {'type': 'string'},
    'SICO-SOFB-BPM-ADD': {'type': 'string'},
    'SICO-SOFB-CH-RMV': {'type': 'string'},
    'SICO-SOFB-CH-ADD': {'type': 'string'},
    'SICO-SOFB-CV-RMV': {'type': 'string'},
    'SICO-SOFB-CV-ADD': {'type': 'string'},
    'SICO-BPM-DEVICENAMES': {'type': 'string', 'count': numBPM, 'value': _np.genfromtxt('txt/dname-bpm.txt', dtype='str')},
    'SICO-CH-DEVICENAMES': {'type': 'string', 'count': numCH, 'value': _np.genfromtxt('txt/dname-ch.txt', dtype='str')},
    'SICO-CV-DEVICENAMES': {'type': 'string', 'count': numCV, 'value': _np.genfromtxt('txt/cv.txt', dtype='str')},
}
