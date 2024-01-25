"""The tests for the stdout silencer."""
import sys

from django.test import TransactionTestCase

from apps.core.utils.silence_stdout_util import silence_stdout


class TestSilenceStdout(TransactionTestCase):
    """The tests for the stdout silencer."""

    def setUp(self) -> None:
        """Set up the data for the tests"""
        self.new_std = "nul" if sys.platform.startswith("win") else "/dev/null"
        super().setUp()

    def test_standard(self) -> None:
        """Run the tests"""
        with silence_stdout():
            self.assertEqual(sys.stdout, sys.__stdout__)
            self.assertEqual(sys.stderr, sys.__stderr__)
            self.assertEqual(sys.stdout.write, sys.__stdout__.write)
            self.assertEqual(sys.stderr.write, sys.__stderr__.write)
        with silence_stdout(
            stdout=True,
            stderr=True,
            django_stdout=False,
            django_stderr=False,
        ):
            sys.stdout.write("Test message")
            sys.stdout.flush()
            sys.stderr.write("Test error message")
            sys.stderr.flush()
        with silence_stdout(
            stdout=False,
            stderr=False,
            django_stdout=True,
            django_stderr=True,
        ):
            self.assertEqual(sys.stdout.write("Test message django"), None)
            self.assertEqual(sys.stdout.write("Test error message django"), None)
        self.assertEqual(sys.stdout, sys.__stdout__)
        self.assertEqual(sys.stderr, sys.__stderr__)
        self.assertEqual(sys.stdout.write, sys.__stdout__.write)
        self.assertEqual(sys.stderr.write, sys.__stderr__.write)
