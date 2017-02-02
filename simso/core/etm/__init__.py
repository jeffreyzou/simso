from .WCET import WCET
from .ACET import ACET
from .CacheModel import CacheModel
from .FixedPenalty import FixedPenalty
from .OFRP import OFRP


execution_time_models = {
    'wcet': WCET,
    'acet': ACET,
    'cache': CacheModel,
    'fixedpenalty': FixedPenalty
	'ofrp': OFRP
}

execution_time_model_names = {
    'WCET': 'wcet',
    'ACET': 'acet',
    'Cache Model': 'cache',
    'Fixed Penalty': 'fixedpenalty'
	'Original FRP': 'ofrp'
}
