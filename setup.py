from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='aria',
    version='0.1.0',
    description='',
    long_description=readme,
    author='Sound Chaser',
    author_email='soundchaser128@gmail.com',
    url='https://github.com/soundchaser128/aria-bot',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
