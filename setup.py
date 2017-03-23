from distutils.core import setup

__version__ = '0.1.6'

with open('README.rst') as f:
    long_description = f.read()

setup(
    name = 'reposify',
    packages = ['reposify'],
    version = __version__,
    description = 'Reposify python bindings',
    long_description=long_description,
    author = 'Reposify',
    author_email = 'support@reposify.com',
    url = 'https://github.com/reposify/reposify-python',
    download_url = 'https://github.com/reposify/reposify-python/tarball/%s' % __version__,
    keywords = 'reposify api client iot cyber',
    install_requires=[
        'requests',
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ]
)
