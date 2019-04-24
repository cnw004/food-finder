from setuptools import setup
setup(name='fp',
      version='0.1',
      description='A CLI tool for finding restaurants',
      url='https://github.com/cnw004/food-finder',
      author='Cole Whitley',
      author_email='colewhit29@gmail.com',
      license='MIT',
      packages=['fp'],
      zip_safe=False,
      entry_points={
        'console_scripts': ['fp = fp.cli:main']
      },
      install_requires=[
        'Click'
    ])
