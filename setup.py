from setuptools import setup

setup(
    name='instasteeem',
    version='0.0.1',
    packages=['instasteem'],
    url='https://github.com/emre/instasteem',
    license='MIT',
    author='Emre Yilmaz',
    author_email='mail@emreyilmaz.me',
    description='A CLI app/library to sync your Instagram posts to STEEM',
    entry_points={
        'console_scripts': [
            'instasteem = instasteem.cli:main',
        ],
    },
    install_requires=['python-slugify',]
)
