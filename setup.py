from setuptools import setup

setup(
    name="fourinsight-campaigns",
    version="0.0.1",
    description="4insight campaigns",
    author="4Subsea",
    author_email="support@4subsea.com",
    url="https://4insight.io/",
    packages=["fourinsight.campaigns"],
    install_requires=[
        "fourinsight-api",
        "pandas",
    ],
    zip_safe=False,
)
