import sys

import ml_analyzers #seemingly unused here, but this makes the environment recognize the model analyzers

import qcl.analyze_models
from qcl.model_analyzer import decorated_analyzers

if __name__ == '__main__':
	qcl.analyze_models.main(
		sys.argv[1] if len(sys.argv) > 1 else input('Enter filename to extract feature data: '), 
		sys.argv[2] if len(sys.argv) > 2 else input('Enter filename to extract classification data: '), 
		None if len(sys.argv) > 3 and sys.argv[3] == 'all' else 
		sys.argv[3:] if len(sys.argv) > 3 else input('What would you like to do?\n' + 
		'\n'.join(('\t' + name for name in decorated_analyzers)) + '\n'
		).split()
	)
