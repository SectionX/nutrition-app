################################################################
#This software is developed by <developer name> for <development reason>
#
#It's released under <LICENSE NAME> license.

from distutils.core import setup
from setuptools import find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

with open('README.md') as f:
    long_description = f.read()

setup(
    name='project_name', #change this
    version='version_number', #change this
    author='author_name', #change this
    author_email='author email', #change this
    description='A sort description of the project', #add description
    long_description=long_description, # uses the contents of README.md by default
    url='https://github.com/authorname/repositoryname', #change this
    classifiers=[
        'Development Status :: Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3.11',
    ],
    entry_points={
        'console_scripts': [
            'project_name = project_name.__main__:main', #include this if you want to run
        ],                                               #the program as executable.
    },                                                   #it runs the main() function of
    packages=find_packages(),                            #__main__.py script
    include_package_data=True,
    package_data={'package_name': ['datafile/*']}, #use this to include assets, templates and 
    requires = requirements                        #other non python files.
)