from setuptools import setup

setup(name='sim',
      version='0.1',
      description='Allocating arrivals',
      url='https://github.com/TriageCapacityPlanning/Triage-Backend/sim',
      packages=['resources'],
      install_requires=['pytest','setuptools','numpy','pytest-cov'],
      zip_safe=False)
