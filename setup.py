#setup.py

try:
	from setuptools import setup
except ImportError:
	print "standard distutils"
	from distutils.core import setup
else:
	print 'setuptools'
import sys


setup(
	name="pypso",
	description="Python Particle Swarm Optimization Toolbox",
	version="0.1",
	author="Marcel Pinheiro Caraciolo",
	author_email="caraciol@gmail.com",
	url="http://code.google.com/p/psopybox/",
	packages=['pypso'],
	license="Apache",
	long_description="Python Particle Swarm Optimization (PSO) Toolbox for Win32, Linux and Mac OS",
	classifiers= ['Development Status :: 5 - Production/Stable',
			      'Intended Audience :: Developers',
			      'Intended Audience :: End Users/Desktop',
			      'License :: Apache 2.0 :: Apache 2.0 License',
			      'Natural Language :: English',
			      'Operating System :: Linux',
				  'Operating System :: Mac OS',
			      'Operating System :: Microsoft :: Windows',
			      'Programming Language :: Python',
			      'Topic :: Artificial Intelligence',
			      'Topic :: Software Development :: Libraries',
			      'Topic :: Optimization :: Evolutionary Algorithm',
				],
)