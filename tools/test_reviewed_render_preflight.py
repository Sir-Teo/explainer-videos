from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from tools.check_reviewed_render_inputs import requirements


class ReviewedInputPreflightTests(unittest.TestCase):
    def test_default_and_selected_baseline_paths(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            default = requirements(root)
            self.assertEqual(len(default['Part 23: accepted JSON bundles']), 5)
            self.assertEqual(len(default['Part 27: default baseline bundle']), 3)
            selected = requirements(root, 'run-1')
            self.assertEqual(selected['Part 27: selected run audit'][0],
                             root / '.cache/ai27/baseline-runs/run-1/baselines_f64.audit.json')
            with self.assertRaises(ValueError):
                requirements(root, '../escape')
            self.assertEqual(list(root.iterdir()), [])


if __name__ == '__main__':
    unittest.main()
