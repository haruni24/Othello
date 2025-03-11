from setuptools import setup, find_packages

setup(
    name='alphazero-project',
    version='0.1.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='A project implementing AlphaZero for board games.',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'numpy',
        'tensorflow',  # or 'torch' depending on your neural network framework
        'gym',         # if using OpenAI Gym for game environments
        # Add other dependencies as needed
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)