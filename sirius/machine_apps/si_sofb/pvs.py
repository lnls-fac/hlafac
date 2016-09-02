
import numpy as _np
import api_status as _api_status

#enums are limited to 25 characters

pvdb = {
    'SICO-SOFB-MODE': {'type': 'enum', 'enums': ['Off', 'Orbit Correction', 'Matrix Measurement']},
    'SICO-SOFB-MODE-PLANE': {'type': 'enum', 'enums': ['H', 'V', 'HV', 'HV+K']},
    'SICO-SOFB-MODE-RFFREQ': {'type': 'enum', 'enums': ['Off', 'On']},
    'SICO-SOFB-AVGORBIT-X': {'type': 'float', 'count': _api_status.nBPM},
    'SICO-SOFB-AVGORBIT-Y': {'type': 'float', 'count': _api_status.nBPM},
    'SICO-SOFB-AVGORBIT-NUMSAMPLES': {'type': 'int', 'value': 1},
    'SICO-SOFB-ERROR': {'type': 'enum', 'enums': ['None', 'MeasRespmError', 'SetNumSamplesError', 'ReadOrbitError', 'SetRespmError', 'SetRefOrbitError', 'CalcStatDataError', 'CorrOrbitError', 'SetRespmSlotError', 'SetRefOrbitSlotError', 'UpdateRespmError', 'UpdateRefOrbitError', 'DeviceSelError', 'KickThresholdError', 'WeightOutRangeError', 'SetModeParameter]}, #0-15
    'SICO-SOFB-RESPM-SEL': {'type': 'enum', 'enums': ['user_shift', 'slot1', 'slot2']},
    'SICO-SOFB-RESPM': {'type': 'float', 'count': (_api_status.nBPM*2)*(_api_status.nCH+_api_status.nCV+1)},
    'SICO-SOFB-REFORBIT-X-SEL': {'type': 'enum', 'enums': ['null', 'slot1', 'slot2']},
    'SICO-SOFB-REFORBIT-Y-SEL': {'type': 'enum', 'enums': ['null', 'slot1', 'slot2']},
    'SICO-SOFB-REFORBIT-X': {'type': 'float', 'count': _api_status.nBPM},
    'SICO-SOFB-REFORBIT-Y': {'type': 'float', 'count': _api_status.nBPM},
    'SICO-SOFB-ORBIT-X-MEAN': {'type': 'float'},
    'SICO-SOFB-ORBIT-Y-MEAN': {'type': 'float'},
    'SICO-SOFB-ORBIT-X-MAX': {'type': 'float'},
    'SICO-SOFB-ORBIT-Y-MAX': {'type': 'float'},
    'SICO-SOFB-ORBIT-X-MIN': {'type': 'float'},
    'SICO-SOFB-ORBIT-Y-MIN': {'type': 'float'},
    'SICO-SOFB-ORBIT-X-RMS': {'type': 'float'},
    'SICO-SOFB-ORBIT-Y-RMS': {'type': 'float'},
    'SICO-SOFB-BPM-SEL': {'type': 'int', 'count': _api_status.nBPM},
    'SICO-SOFB-CH-SEL': {'type': 'int', 'count': _api_status.nCH},
    'SICO-SOFB-CV-SEL': {'type': 'int', 'count': _api_status.nCV},
    'SICO-SOFB-BPM-RMV': {'type': 'string'},
    'SICO-SOFB-BPM-ADD': {'type': 'string'},
    'SICO-SOFB-CH-RMV': {'type': 'string'},
    'SICO-SOFB-CH-ADD': {'type': 'string'},
    'SICO-SOFB-CV-RMV': {'type': 'string'},
    'SICO-SOFB-CV-ADD': {'type': 'string'},
    'SICO-BPM-DEVICENAMES': {'type': 'string', 'count': _api_status.nBPM, 'value': _api_status.devicenames_bpm},
    'SICO-CH-DEVICENAMES': {'type': 'string', 'count': _api_status.nCH, 'value': _api_status.devicenames_ch},
    'SICO-CV-DEVICENAMES': {'type': 'string', 'count': _api_status.nCV, 'value': _api_status.devicenames_cv},
    'SICO-SOFB-WEIGHT-H': {'type': 'float', 'value': 100, 'unit': '%', 'prec': 0},
    'SICO-SOFB-WEIGHT-V': {'type': 'float', 'value': 100, 'unit': '%', 'prec': 0},
}
