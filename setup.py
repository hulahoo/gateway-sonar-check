import os
from setuptools import setup

install_requires = [
    ('kafka-python', '2.0.2'),
    ('flake8', '5.0.4'),
    ('pydantic', '1.10.2'),
    ('loguru', '0.6.0'),
    ('python-dotenv', '0.21.0'),
    ('APScheduler', '3.9.1.post1'),
    ('psycopg2-binary', '2.9.5'),
]

CI_PROJECT_NAME = os.environ.get("CI_PROJECT_NAME", "events-gateway").replace("-", "_")
ARTIFACT_VERSION = os.environ.get("ARTIFACT_VERSION", "local")
CI_PROJECT_TITLE = os.environ.get("CI_PROJECT_TITLE", "Событийный шлюз")
CI_PROJECT_URL = os.environ.get("CI_PROJECT_URL", "https://gitlab.rshbdev.ru/rshbintech/information-security/application-security/threat-intelligence/events-gateway")


setup(
    name=CI_PROJECT_NAME,
    version=ARTIFACT_VERSION,
    description=CI_PROJECT_TITLE,
    url=CI_PROJECT_URL,
    install_requires=[">=".join(req) for req in install_requires],
    python_requires=">=3.9.1",
    entry_points={
        'console_scripts': [
            CI_PROJECT_NAME +
            " = " +
            CI_PROJECT_NAME +
            ":main"
        ]
    }
)
