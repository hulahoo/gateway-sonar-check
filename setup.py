import os
from setuptools import setup

setup(
    name=os.environ["CI_PROJECT_NAME"],
    version="local",
    description=os.environ["CI_PROJECT_TITLE"],
    url=os.environ["CI_PROJECT_URL"],
    install_requires=[
        "kafka-python>=2.0.2",
        "flake8>=5.0.4",
        "pydantic>=1.10.2",
        "loguru==0.6.0",
        "python-dotenv==0.21.0",
        "APScheduler==3.9.1.post1",
        "psycopg2>=2.9.5"
    ],
    entry_points={
        'console_scripts': [
            os.environ["CI_PROJECT_NAME"] +
            " = " +
            os.environ["CI_PROJECT_NAME"] +
            ":main"
        ]
    }
)
