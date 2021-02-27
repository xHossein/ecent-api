from setuptools import find_packages, setup

requirements = [
    'requests==2.25.1',
    'requests-toolbelt==0.9.1',
    'PySocks==1.7.1',
    'pydantic==1.7.3',
    'beautifulsoup4==4.9.3'
]

setup(
    name='ecent-api',
    version='0.1.0',
    author='xHossein',
    license='MIT',
    url='https://github.com/xHossein/ecent-api',
    install_requires=requirements,
    keywords='ecent api',
    description='Ecent API [ https://ecent2.guilan.ac.ir ]',
    packages=find_packages(),
    python_requires=">=3.6",
    include_package_data=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ]
)