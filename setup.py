from setuptools import find_packages, setup


GITHUB_URL = "https://github.com/tfiers/fileflow"

with open("README.md", mode="r") as f:
    readme = f.read()

setup(
    name="fileflow",
    description="File processing pipelines without boilerplate",
    author="Tomas Fiers",
    author_email="tomas.fiers@gmail.com",
    long_description=readme,
    long_description_content_type="text/markdown",
    url=GITHUB_URL,
    project_urls={"Source Code": GITHUB_URL},
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    install_requires=(
        "typeguard ~=2.2.2",
        "gitpython ~=2.1.11",
        "decopatch ~=1.4.5",
    ),
    use_scm_version=True,  # Get package version from git tags
    setup_requires=["setuptools_scm"],
)
