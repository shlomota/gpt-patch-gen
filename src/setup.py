from setuptools import setup, find_packages

setup(
    name='gpt-patch-gen',
    version='0.1',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    entry_points={
        'console_scripts': [
            'gpt-patch-gen=main:main',
        ],
    },
    install_requires=[
        'colorama',
        'openai'
    ],
)