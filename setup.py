from setuptools import setup, find_packages
import io

# Use io.open with explicit encoding
with io.open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="chatsage",
    version="0.1.0",
    author="Mohamed Kouhou",
    author_email="mohamed.kouhou@hotmail.com",
    description="A multi-model chatbot application",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/chatsage",
    packages=find_packages(exclude=["tests*"]),
    include_package_data=True,
    install_requires=[
        "flask>=3.0.2",
        "gunicorn>=21.2.0",
        "requests>=2.31.0",
        "transformers>=4.36.2",
        "torch>=2.2.1",
        "openai>=1.6.1",
        "anthropic>=0.7.8",
        "numpy>=1.26.4",
        "pandas>=2.2.1",
        "python-dotenv>=1.0.1",
        "flask-cors>=4.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=8.0.2",
            "flake8>=7.0.0",
            "black>=24.2.0",
            "coverage>=7.4.1",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.12",
    entry_points={
        "console_scripts": [
            "chatsage=src.main:main",
        ],
    },
)