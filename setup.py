from setuptools import setup

setup(
    name='rejira',
    description='A look aside for JIRA using redis as the cache',
    url='https://github.com/xnuiem/rejira',
    author='Xnuiem',
    author_email='ryan.meinzer@xmtek.net',
    license='Apache2',
    version='0.1',
    packages=['rejira'],
    install_requires=[
        'redis',
        'requests'
    ],
    python_requires='>=3',
)
