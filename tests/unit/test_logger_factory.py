from logging import Logger
from unittest import mock

from app.logger.logger_factory import LoggerFactory


def test_initialize():
    LoggerFactory._initialize()

    assert LoggerFactory._LOG is not None
    assert LoggerFactory._LOG.name == "root"
    assert isinstance(LoggerFactory._LOG, Logger)


def test_get_root_logger():
    mock_logger = mock.MagicMock()
    LoggerFactory._LOG = mock_logger

    root_logger = LoggerFactory.get_root_logger()

    assert root_logger == mock_logger


def test_get_logger():
    LoggerFactory._initialize = mock.MagicMock()
    LoggerFactory._LOG = mock.MagicMock()
    module_name = "test_module"

    child_logger = LoggerFactory.get_logger(module_name)

    LoggerFactory._initialize.assert_called_once()
    LoggerFactory._LOG.getChild.assert_called_with(module_name)
    assert child_logger == LoggerFactory._LOG.getChild(module_name)
