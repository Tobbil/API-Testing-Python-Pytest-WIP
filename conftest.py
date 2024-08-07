import logging
import logging.config
import pytest

def pytest_configure(config):
    logging.config.fileConfig('config/logging.cfg')

@pytest.hookimpl(tryfirst=True)
def pytest_runtest_logreport(report):
    if report.when == 'call':
        if report.failed:
            logging.error(f"{report.nodeid} failed: {report.longrepr}")
        elif report.passed:
            logging.info(f"{report.nodeid} -- PASSED --")
        elif report.skipped:
            logging.warning(f"Test {report.nodeid} skipped: {report.longrepr}")
