from setuptools import setup

with open("README.md" , "r") as fh:
    long_description = fh.read()
    
setup(
    name="mongolianlunaryear",
    version="0.1",
    description="Calculates mongolian lunar year.",
    long_description=long_description,
    long_description_content="text/markdown",
    url="http://github.com/JBayaraa22/mongolianlunaryear",
    author="Bayarjargal Jargalsaikhan",
    author_email="me@bayarjargal.com",
    license="MIT License",
    zip_safe=False,
    classifiers=[
        "Programming language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=['mongolianlunaryear , dateutil'],
)