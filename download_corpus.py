# pylint: disable = C0330
'''
Utilities to download a corpus
'''

import os
import sys
import subprocess

def download_corpus(corpus_path, repo_user='timgianitsos'):
	'''
	Download a corpus from Github with a sparse checkout and shallow clone.
	https://stackoverflow.com/a/28039894/7102572

	If the directory specified by corpus_path already exists, no action will be taken.
	'''

	# Locally create a directory to hold the corpus, and prepare it for cloning the repo
	if not os.path.isdir(corpus_path[0]):
		try:
			cmd_list = [
				f'mkdir {corpus_path[0]}',
				f'git -C {corpus_path[0]} init',
				f'git -C {corpus_path[0]} remote add origin ' +
					f'https://github.com/{repo_user}/{corpus_path[0]}.git',

				# If the corpus path only has one element (the name of the repo), then the user wants
				# to clone the whole repo. If there are multiple elements, the user wants to import only
				# a subdirectory, so we prepare for a sparse checkout
				(
					f'git -C {corpus_path[0]} pull --depth=1 origin master'
					if len(corpus_path) == 1 else
					f'git -C {corpus_path[0]} config core.sparseCheckout true'
				),
			]
			for cmd in cmd_list:
				subprocess.run(cmd, check=True, shell=True)
		except OSError as ex:
			raise ex
		except subprocess.CalledProcessError as ex:
			raise ex

	# Perform a sparse checkout
	# If the corpus path has only one element, the whole directory will have already been cloned just
	# previously and this block won't execute a sparse checkout
	if not os.path.isdir(os.path.join(*corpus_path)):
		try:
			cmd_list = (
				f'echo {"/".join(corpus_path[1:])}/*'
					+ f' >> {os.path.join(corpus_path[0], ".git", "info", "sparse-checkout")}',
				f'git -C {corpus_path[0]} fetch --depth=1 origin master',
				f'git -C {corpus_path[0]} checkout master',
			)
			for cmd in cmd_list:
				subprocess.run(cmd, check=True, shell=True)
		except OSError as ex:
			raise ex
		except subprocess.CalledProcessError as ex:
			raise ex
