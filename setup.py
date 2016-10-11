from setuptools import setup, find_packages


def readme():
    with open('README.rst') as f:
        return f.read()

version = open('packaging/VERSION').read().strip()
requirements = open('packaging/requirements.txt').read().split("\n")
# test_requirements = open('packaging/requirements-test.txt').read().split("\n")

setup(
    name='prngmgr',
    version=version,
    author='Workonline Communications',
    author_email='communications@workonkonline.co.za',
    description='Django webapp for peering session management using PeeringDB API',
    long_description=readme(),
    license='LICENSE',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet',
    ],
    packages=find_packages(
        include=[
            'prngmgr',
            'prngmgr.*',
            'test'
        ],
        exclude=[]
    ),
    include_package_data=True,

    url='https://github.com/wolcomm/prngmgr',
    download_url='https://github.com/prngmgr/%s' % version,

    install_requires=requirements,
    # test_requires=test_requirements,
    test_suite='test.exec'
)
