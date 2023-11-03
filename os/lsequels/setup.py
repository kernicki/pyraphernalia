from setuptools import setup

setup(name='lsequels',
      version='1.0',
      description='L(ist file )seque(nces as sing)l(e entitie)s',
      url='http://github.com/kernickii/paraphernalia.git',
      author='CG Engineer',
      author_email='{id}+{user_name}@users.noreply.github.com',
      license='Apache',
      packages=['lsequels'],
      install_requires=[
          'argparse'
      ],
      entry_points={
          'console_scripts': ['lsequels=lsequels.command_line:main'],
      },
      include_package_data=True,
      zip_safe=False)
