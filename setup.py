from setuptools import setup

setup(
    name='rejira',
    description='A look aside for JIRA using redis as the cache',
    long_description='The JIRA RESTful API can be slow, especially on large self hosted projects. '
                     'This package uses redis to create a dynamic cache for the read requests from JIRA, both by Issue'
                     ' or by JQL',
    url='https://github.com/xnuiem/rejira',
    author='Xnuiem',
    author_email='ryan.meinzer@xmtek.net',
    license='Apache',
    version='0.0.1.dev1',
    packages=['rejira'],
    install_requires=[
        'redis',
        'requests'
    ],
    python_requires='>=3',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
