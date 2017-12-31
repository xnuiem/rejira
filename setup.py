from setuptools import setup

setup(
    name='rejira',
    description='The funniest joke in the world',
    url='http://github.com/storborg/funniest',
    author='Xnuiem',
    author_email='xnuiem@xmtek.net',
    license='Apache2',
    version='0.1',
    packages=['rejira'],
    install_requires=[
        'redis',
        'requests'
    ],
)
