from pathlib import Path
import setuptools


setuptools.setup(
    name="pmbuddy",
    version="0.0.1",
    description="A tool for extracting metadata from PubMed journals",
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    url="",
    author="dagsdags212",
    author_email="jegsamson.dev@gmail.com",
    license="The Unlicense",
    project_urls={
        "Source": "https://github.com/dagsdags212/pubmed-buddy"
    },
    classifiers=[
        "Development Status :: 2 - Pre-alpha",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.12",
    install_requires=["httpx", "pydantic", "pandas", "bs4"],
    packages=setuptools.find_packages(),
    include_package_data=True,
    #entry_points={'console_scripts': ["scrape = scraper.cli:main"]}
)
