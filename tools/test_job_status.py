"""Regression tests for the documented `job.py kaggle status [slug]` CLI."""
import contextlib
import importlib.util
import io
from pathlib import Path
import unittest
from unittest.mock import patch


SPEC = importlib.util.spec_from_file_location(
    "job", Path(__file__).with_name("job.py"))
job = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(job)


class KaggleStatusArgumentsTests(unittest.TestCase):
    def test_status_uses_explicit_kernel_slug(self):
        with patch.object(job.sys, "argv", ["job.py", "kaggle", "status", "owner/kernel"]):
            with patch.object(job, "kaggle_status") as status:
                job.main()
        status.assert_called_once_with("owner/kernel")

    def test_status_without_slug_keeps_default_kernel(self):
        with patch.object(job.sys, "argv", ["job.py", "kaggle", "status"]):
            with patch.object(job, "kaggle_status") as status:
                job.main()
        status.assert_called_once_with(None)

    def test_status_rejects_extra_argument_without_polling(self):
        args = ["job.py", "kaggle", "status", "owner/kernel", "unexpected"]
        with patch.object(job.sys, "argv", args):
            with patch.object(job, "kaggle_status") as status:
                with contextlib.redirect_stdout(io.StringIO()):
                    with self.assertRaises(SystemExit) as error:
                        job.main()
        self.assertEqual(error.exception.code, 2)
        status.assert_not_called()


if __name__ == "__main__":
    unittest.main()
