
from pcaspy import Severity


pvdb = {
#     'SHIFT-TYPE': {
#         'type': 'string',
#         'value': 'User'
#     },
    'SHIFT-TYPE': {
        'type': 'enum',
        'enums': [
            'User Shift',
            'Accelerator Shift',
            'Maintenance Shift',
            'Conditioning Shift'
        ],
        'severity': 4*[Severity.NO_ALARM]
    },
    'MESSAGE': {
        'type': 'string',
        'value': 'In case of trouble, call Control Room.'
    },    
}
