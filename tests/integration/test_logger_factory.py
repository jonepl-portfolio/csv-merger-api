import pytest
from pathlib import Path
from pytest import MonkeyPatch

from app.logger.logger_factory import LoggerFactory, ROOT_LOGGER_NAME
from logging import Logger


@pytest.fixture
def tmp_log_dir(tmp_path: Path):
    # Create a temporary directory for log files
    log_dir = tmp_path / "logs"
    log_dir.mkdir()
    yield log_dir


@pytest.fixture
def configure_environment(monkeypatch: MonkeyPatch, tmp_log_dir: Path):
    # Set the environment variable
    monkeypatch.setenv("APP_ENV", "TEST")

    # Configure logging settings to use the temporary log directory
    config = {
        "version": 1,
        "formatters": {
            "simple": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            },
        },
        "handlers": {
            "file": {
                "class": "logging.FileHandler",
                "filename": tmp_log_dir / "app.log",
                "formatter": "simple",
            },
        },
        "root": {
            "level": "DEBUG",
            "handlers": ["file"],
        },
    }

    monkeypatch.setattr("logger.config.config", config)

    # Clear the existing logger factory state
    LoggerFactory._LOG = None


def test_initialize(configure_environment):
    # Initialize the LoggerFactory
    LoggerFactory._initialize()

    # Verify that the logger was created
    assert LoggerFactory._LOG is not None
    assert isinstance(LoggerFactory._LOG, Logger)


def test_get_root_logger(configure_environment):
    # Initialize the LoggerFactory
    LoggerFactory._initialize()

    # Get the root logger
    root_logger = LoggerFactory.get_root_logger()

    # Verify that the root logger is the one initialized by the factory
    assert root_logger == LoggerFactory._LOG


def test_get_logger(configure_environment):
    # Initialize the LoggerFactory
    LoggerFactory._initialize()

    # Define a module name for the test
    module_name = "test_module"

    # Get a child logger
    child_logger = LoggerFactory.get_logger(module_name)

    # Check if the child logger is a child of the root logger
    assert child_logger is not None
    assert child_logger.name == f"{ROOT_LOGGER_NAME}.{module_name}"
    assert child_logger.parent == LoggerFactory._LOG


# def test_file_logging(configure_environment, tmp_log_dir: Path):
#     # Initialize the LoggerFactory
#     LoggerFactory._initialize()

#     # Get the root logger
#     root_logger = LoggerFactory.get_root_logger()

#     # Log a message
#     message = "This is a test log message."
#     root_logger.debug(message)

#     # Check if the log file was created and contains the message
#     log_file = tmp_log_dir / "app.log"
#     assert log_file.exists()

#     with open(log_file, "r") as file:
#         content = file.read()
#         assert message in content
