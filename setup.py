from setuptools import setup, find_packages

"""
打包和发布: 
python setup.py sdist bdist_wheel
pip install twine
twine upload dist/*
"""

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="cqbot",
    version="0.0.1",
    description="go-cqhttp python 框架，可以用于快速塔建 bot",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    license="MIT",
    url="https://github.com/lhlyu/cqbot",
    author="lhlyu",
    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=[
        "requests",
        "pyyaml",
        "websocket-client"
    ],
    python_requires='>=3.10'
)