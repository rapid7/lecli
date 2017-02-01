from setuptools import setup, find_packages
import lecli

setup(
    name='logentries-lecli',
    version=lecli.__version__,
    author='John Fitzpatrick, Safa Topal',
    author_email='john.fitzpatrick@rapid7.com, safa.topal@rapid7.com',
    description='Logentries Command Line Interface',
    long_description=open('README.md').read(),
    packages=find_packages(exclude=['*tests*']),
    license='MIT',
    install_requires=['click==6.6', 'requests==2.9.1', 'pytz==2016.4', 'termcolor==1.1.0',
                      'tabulate==0.7.5', 'appdirs==1.4.0', 'validators==0.11.2'],
    entry_points={'console_scripts': ['lecli = lecli.cli:cli']},
    url='https://github.com/logentries/lecli',
    zip_safe=False
)
