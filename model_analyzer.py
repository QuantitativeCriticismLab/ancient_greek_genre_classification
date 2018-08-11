from collections import OrderedDict

decorated_analyzers = OrderedDict()

def model_analyzer():
	def decor(f):
		def wrapper(data, target, file_names, feature_names):
			return f(data, target, file_names, feature_names)
		decorated_analyzers[f.__name__] = wrapper
		return wrapper
	return decor
