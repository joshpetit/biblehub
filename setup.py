import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="biblehub",
    version="2.0a5",
    author="Joshua Petitma",
    author_email="joshuapetitma@yahoo.com",
    description="A module to scrape biblehub.com, also cli app",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/joshpetit/biblehub",
    packages=setuptools.find_packages(),
    install_requires=[
      'bs4',
      'pypassage'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    scripts=['scripts/biblehub'],
    obsoleteDist="BibleHubScrapper (<1.3.5)"
)
