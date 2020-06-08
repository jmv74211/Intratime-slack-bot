from setuptools import setup, find_namespace_packages
import shutil, glob

setup(name='pepe',
      version='1.1',
      description='Slack app to clock in Intratime API',
      url='https://github.com/jmv74211/intratime_slack_bot',
      author='jmv74211',
      author_email='jmv74211@gmail.com',
      license='GPLv3',
      package_dir={"": "src"},
      packages=find_namespace_packages(where="src"),
      install_requires=[
          'pycrypto==2.6.1',
          'pymongo==3.10.0',
          'requests==2.22.0',
          'Unidecode==1.1.1',
          'Flask==1.1.1',
          'slackclient==2.5.0'
      ],
      zip_safe=False
      )

# Clean build files
shutil.rmtree('dist')
shutil.rmtree('build')
shutil.rmtree(glob.glob('src/*.egg-info')[0])
