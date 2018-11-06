"""
    install script for graph_ql_sly
"""

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

TEST_REQUIRE = ['pytest']

setup(name="graph_ql_sly",
      description="GraphQL with SLY",
      long_description="""
A GraphQL parser built using the SLY library.
""",
      license="""MIT""",
      version="0.0.0",
      author="Stephen Ingram",
      author_email="stephenfroweingram@gmail.com",
      maintainer="Stephen Ingram",
      maintainer_email="stephenfroweingram@gmail.com",
      url="https://github.com/sfingram/graph_ql_sly",
      packages=['sly'],
      install_requires=[],
      tests_require=TEST_REQUIRE,
      extras_require={
          'test': TEST_REQUIRE,
      },
      classifiers=[
          'Programming Language :: Python :: 3',
      ])
