import setuptools

from waimea import __version__

setuptools.setup(
    name='waimea-bigwave-detector',
    version=__version__,
    packages=[p for p in setuptools.find_packages() if 'waimea' in p],
    license='',
    description='Detect big wave swells at Waimea Bay',
    install_requires=[
        'requests',
        'flask',
        'pyspark',
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'waimea:monitor=waimea.monitor:main',
            'waimea:api=waimea.api:main',
            'waimea:detector=waimea.detector:main',
        ]
    },
)
