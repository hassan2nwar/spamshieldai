from setuptools import setup, find_packages

setup(
    name='spamshieldai',
    version='0.1.0',
    description='SMS Spam Classifier with Flask API and React Frontend',
    author='Hassan Anwar',
    author_email='',
    url='https://github.com/hassan2nwar/spamshieldai',
    packages=find_packages(),
    python_requires='>=3.8',
    install_requires=[
        'pandas>=1.3.0',
        'scikit-learn>=1.0.0',
        'joblib>=1.0.0',
        'flask>=2.0.0',
        'flask-cors>=3.0.0',
        'pyyaml>=5.4.0',
    ],
    extras_require={
        'dev': [
            'pytest>=6.2.0',
            'pytest-cov>=2.12.0',
            'black>=21.5b0',
            'flake8>=3.9.0',
            'mypy>=0.910',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    entry_points={
        'console_scripts': [
            'spamshieldai-train=src.models.train:main',
        ],
    },
)
