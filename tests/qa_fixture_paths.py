from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARCHIVED_EVIDENCE = Path("docs/qa/evidence")
FIXTURES = ROOT / "tests/fixtures/qa"


def repo_file(path):
    # Archived manifests retain their original paths and byte hashes.
    path = Path(path)
    if path.is_relative_to(ARCHIVED_EVIDENCE):
        return FIXTURES / path.relative_to(ARCHIVED_EVIDENCE)
    return ROOT / path
