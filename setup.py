from distutils.core import setup
setup(
    name='zdai',
    version='1.0.0',
    description='Zuva DocAI (ZDAI) Python Wrapper',
    author='Zuva Inc.',
    author_email='support@zuva.ai',
    url='https://github.com/zuvaai/zdai-python',
    license='Apache 2.0',
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries',
    ],
    packages=['zdai', 'zdai.api', 'zdai.config', 'zdai.models'],
    install_requires=[
        'requests >= 2.31.0'
    ]
)
