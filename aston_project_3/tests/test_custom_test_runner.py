"""Custom test runner."""
import sys
from test.support.os_helper import EnvironmentVarGuard

from django.test.runner import DiscoverRunner

from unittest import TestSuite, TextTestResult


class CustomTestRunner(DiscoverRunner):
    """Custom test runner."""

    def run_suite(self, suite: TestSuite, **kwargs) -> TextTestResult:
        """Runs the test suite."""
        result = super().run_suite(suite, **kwargs)
        return result

    def suite_result(self, suite: TestSuite, result: TextTestResult, **kwargs) -> int:
        """Computes and returns a return code based on a test suite, and the result from that test suite."""
        if result is not None:
            # Django unit tests were run
            result = super().suite_result(suite, result, **kwargs)
        else:
            result = 0
        return result

    def run_tests(self, *args, **kwargs) -> int:
        """Run the test suite."""
        with EnvironmentVarGuard() as environ:
            print(
                "Starting the unit tests (this may take some minutes...)",
                file=sys.stderr,
            )
            environ["UNIT_TEST"] = "True"
            return super(CustomTestRunner, self).run_tests(*args, **kwargs)
