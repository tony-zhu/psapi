try:
    from setuptools import setup, find_packages
except ImportError:
    import distribute_setup
    distribute_setup.use_setuptools()
    from setuptools import setup, find_packages
    

setup(
    name='psapi',
    version='0.1dev',
    author='Ahmed El-Hassany',
    author_email='ahassany@udel.edu',
    packages=find_packages(exclude=['test']),
    url='http://code.google.com/p/psapi/',
    license='GPL',
    description='Python API for perfSONAR',
    long_description=open('README').read(),
)
