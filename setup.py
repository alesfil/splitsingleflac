from setuptools import setup, find_packages

setup(
    name = 'splitsingleflac',
    version = '0.3',
    author = 'Alessandro Filippo',
    author_email = 'alessandro.filippo@infinito.it',
    license = 'GPLv2+',

    packages = find_packages('src'),
    package_dir = {'':'src'},
    scripts = ['./src/scripts/splitsingleflac'],

    include_package_data = True,
    package_data = {'':['splitsinglefile.desktop']},
 
)
