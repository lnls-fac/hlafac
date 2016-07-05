
power_supplies = [
		"L-CV01A", "L-CH01A",
		"L-CV01B", "L-CH01B",
		"L-CV02", "L-CH02",
		]

parameters = [
        ':SlowReferenceCurrent',
        ':OutputCurrent',
        ':OnOff',
        ':CommandMode',
        ':HardInterlocks',
        ':Command',
        ]

pvdb = {}
for ps in power_supplies:
    pvdb[ps+parameters[0]] = {'value': 0.0, 'prec': 6, 'unit': 'A' }
    pvdb[ps+parameters[1]] = {'value': 0.0, 'prec': 6, 'unit': 'A' }
    pvdb[ps+parameters[2]] = {'type' : 'enum', 'enums': ['Off', 'On'], 'value' : 0 }
    pvdb[ps+parameters[3]] = {'type' : 'enum', 'enums': ['Remote', 'Local', 'PCHost'], 'value': 0 }
    pvdb[ps+parameters[4]] = {'type' : 'int', 'value' : 0 }
    pvdb[ps+parameters[5]] = {'type' : 'enum', 'enums': ['TurnOn', 'TurnOff', 'OpenLoop', 'CloseLoop', 'SetOperationMode', 'SetSlowReferenceCurrent',
                            'ConfigureWfmReference', 'ConfigureSignalGenerator', 'EnableSignalGenerator', 'DisableSignalGenerator', 'ResetInterlocks', 'None'], 'value': 11}
