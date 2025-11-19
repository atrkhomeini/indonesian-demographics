from setuptools import find_packages, setup

setup(
    name='indonesia_demographics',
    packages=find_packages(),
    version='0.1.0',
    description='Market intelligence analysis of Indonesian demographics',
    author='Your Name',
    license='MIT',
    install_requires=[
        'pandas>=2.0.0',
        'numpy>=1.24.0',
        'sqlalchemy>=2.0.0',
        'psycopg2-binary>=2.9.0',
        'matplotlib>=3.7.0',
        'seaborn>=0.12.0',
        'python-dotenv>=1.0.0',
    ],
    python_requires='>=3.8',
)