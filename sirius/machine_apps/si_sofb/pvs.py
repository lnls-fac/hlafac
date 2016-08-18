
import numpy as _np
import api_status as _api_status

#enums are limited to 25 characters

pvdb = {
    'SICO-SOFB-MODE': {'type': 'enum', 'enums': ['Off', 'Corr-OnH', 'Corr-OnV', 'Corr-OnHOnV', 'Corr-OnHV', 'Corr-OnH_F', 'Corr-OnV_F', 'Corr-OnHOnV_F', 'Corr-OnHV_F', 'MeasRespm-OnH', 'MeasRespm-OnV', 'MeasRespm-OnHV', 'MeasRespm-OnH_F', 'MeasRespm-OnV_F', 'MeasRespm-OnHV_F']},
    'SICO-SOFB-AVGORBIT-X': {'type': 'float', 'count': _api_status.nBPM},
    'SICO-SOFB-AVGORBIT-Y': {'type': 'float', 'count': _api_status.nBPM},
    'SICO-SOFB-AVGORBIT-NUMSAMPLES': {'type': 'int', 'value': 1},
    'SICO-SOFB-ERROR': {'type': 'enum', 'enums': ['None', 'MeasRespmError', 'SetNumSamplesError', 'ReadOrbitError', 'SetRespmError', 'SetRefOrbitError', 'CalcEstatDataError', 'CorrOrbitError', 'SetRespmSlotError', 'SetRefOrbitSlotError', 'UpdateRespmError', 'UpdateRefOrbitError', 'DeviceSelError', 'KickThresholdError', 'WeightOutRangeError']}, #0-14
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
    'SICO-SOFB-WEIGHT': {'type': 'float', 'value': 1},
}
