import os
from setuptools import setup, find_packages
setup(name='python-versioned',
      version='0.1.1',
      description=("Version files with hardlinks."),
      long_description=open('README.rst').read(),
      classifiers=['Development Status :: 3 - Alpha',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: MIT License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Utilities'
                    ],
      install_requires=[
            'docopt >= 0.6', 
            'dateutil >= 1.0', 
      ], 
      keywords='filesystem versioning backups',
      author='Stijn Debrouwere',
      author_email='stijn@debrouwere.org',
      download_url='https://www.github.com/debrouwere/versioned/tarball/master',
      license='ISC',
      packages=find_packages()
      )