from distutils.core import setup
setup(
    name='zdai',
    packages=['zdai', 'zdai.api', 'zdai.config', 'zdai.models'],
    install_requires=[
        'requests >= 2.31.0'
    ]
)
