from distutils.core import setup

setup(
    name='BKPrecisionMultimeter',
    version='1.0',
    packages=['bkprecision'],
    url='',
    license='',
    author='Marco Calderon',
    author_email='marco.calderon.perez@gmail.com',
    description='Software for controlling a BK Precision multimeter 2831E.',
    install_requires=[
        'pyserial',
    ]
)
