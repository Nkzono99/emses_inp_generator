from setuptools import setup, find_packages


def _require_packages(filename):
    return open(filename).read().splitlines()


long_description = open('README.md', 'r', encoding='utf-8').read()

setup(
    name='emses_inp_generator',
    description='Tool for automatic generation of parameter file "plasma.inp" for EMSES',
    long_description=long_description,
    long_description_content_type="text/markdown",
    version='1.0.0',
    install_requires=_require_packages('requirements.txt'),
    author='Nkzono99',
    author_email='210x218x@gsuite.stu.kobe-u.ac.jp',
    url='https://github.com/Nkzono99/emses_inp_generator',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'inpgen = emses_inp_generator.main:main',
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    include_package_data=True,
)
