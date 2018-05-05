from setuptools import setup, find_packages

setup(
    name='fastpipeline',
    version='1.0',
    description='The pipeline for FAST telescope spectrum data processing.',
    url='https://github.com/PennyQ/FAST-scripts',
    author='Penny Qian',
    author_email='foomail@foo.com',
    packages=find_packages(),  # same as name
    install_requires=['astropy', 'scipy', 'numpy', 'matplotlib'],
    entry_points={'console_scripts': ['fastpipeline = pipeline.main:start_pipeline'], }
)
