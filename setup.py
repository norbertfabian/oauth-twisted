from setuptools import setup, find_packages, Extension

setup(
    name='api',
    version='0.0.1',
    description='oAuth authorization server api',
    author='Martin Miksanik',
    author_email='martin@miksanik.net',
    license='GNUGPL',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'templates': ['oauth/templates/*'],
        'static': ['oauth/static/*']        
        },
    zip_safe=False,
    install_requires=[
        'twisted',
        'autobahn[twisted]',
        'pyyaml',
        'psycopg2',
        'txpostgres',
    ],
    scripts=[
        'bin/oauth',
    ]
)

