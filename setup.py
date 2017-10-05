try:
    # Try using ez_setup to install setuptools if not already installed.
    from ez_setup import use_setuptools
    use_setuptools()
except ImportError:
    # Ignore import error and assume Python 3 which already has setuptools.
    pass

from setuptools import setup, find_packages


setup(name='cpds',
      version='0.1.0',
      author='Evan Simkowitz, Brian Lam',
      author_email='esimkowitz@wustl.edu',
      description='A set of scripts for running plagiarism detection using MOSS',
      license='MIT',
      classifiers=[
          'Development Status :: 2 - Beta',
          'License :: OSI Approved :: MIT License',
          'Intended Audience :: Educators',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Topic :: Education :: Plagiarism Detection'],
      url='https://github.com/esimkowitz/cpds/',
      install_requires=['PyGithub>=1.35'],
      packages=find_packages(),
      zip_safe=True)
