"""The Part 23 input preflight is read-only and names each missing bundle."""
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from contextlib import redirect_stdout
from io import StringIO

from tools.check_part23_qa_inputs import REQUIRED, main, missing_inputs


class PreflightTests(unittest.TestCase):
    def test_absent_then_present(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.assertEqual(set(missing_inputs(root)), set(REQUIRED))
            out = StringIO()
            with redirect_stdout(out):
                self.assertEqual(main([str(root)]), 1)
            for key in REQUIRED:
                self.assertIn(f'MISSING  {key}.json', out.getvalue())
                (root / f'{key}.json').write_text('{}')
            with redirect_stdout(StringIO()):
                self.assertEqual(main([str(root)]), 0)
            self.assertEqual(set(p.name for p in root.iterdir()), {f'{key}.json' for key in REQUIRED})


if __name__ == '__main__':
    unittest.main()
