from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="commitify",
    version="0.1.0",
    author="Srinivas Sivaratri",
    author_email="srinivassivaratri1122@gmail.com",
    description="AI-powered git commit message generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/srinivassivaratri/commitify",
    packages=find_packages(),
    install_requires=[
        "requests>=2.31.0,<3.0.0",
        "python-dotenv>=0.19.0,<2.0.0",
        "colorama>=0.4.4,<0.5.0",
    ],
    entry_points={
        "console_scripts": [
            "ai-commit=aicommit.ai_commit:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7,<4.0",
)