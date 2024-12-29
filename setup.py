from setuptools import setup

setup(
    name="agent_test",
    version="1.0.0",
    install_requires=[
        "black",
        "datetime",
        "dotenv",
        "langchain"
        "langgraph",
        "numpy",
        "omegaconf",
        "pylint",
        "pytest",
    ],
    author="Dylan Miller",
    author_email="dylanamiller3@gmail.com",
    description=("LLM application backend to help studying for the LSAT."),
    keywords="lsat training machine learning llm",
    url="http://packages.python.org/an_example_pypi_project",
    packages=["agent_test"],
    classifiers=[
        "Development Status :: 3 - Alpha",
    ],
)
