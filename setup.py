from setuptools import setup

setup(
    name='robot',
    version='0.1',
    description='a simple material transfer robot simulator package',
    url='http://github.com/markrgrant/robot',
    author='Mark Grant',
    author_email='markrgrant@yahoo.com',
    license='MIT',
    packages=['robot'],
    install_requires=[
        'nose'
    ],
    zip_safe=False
)
