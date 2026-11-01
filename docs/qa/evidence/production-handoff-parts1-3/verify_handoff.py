#!/usr/bin/env python3
"""Read-only hash/version preflight; never imports scenes/producers or loads models.
Not a production loader guard. Use --strict-external before full-part expansion.
"""
import argparse
import hashlib
import importlib.metadata
import json
import os
import subprocess
from pathlib import Path

D = Path(__file__).resolve().parent
BASE = '927fba668656a682b3e29a288de64130ddc680dd'
SVD = 'videos/ai/ai3/s08_svd.py'
KNOWN_OVERLAYS = {
    'svd-reveal-v1': ('overlays/svd-reveal-v1.json',
                      '30bd30dd975727a0448111f40710cd8192ffc8ed1f13847dfaed5c634e379bf8'),
}


def digest(p):
    h = hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda: f.read(1024 * 1024), b''):
            h.update(b)
    return h.hexdigest()


def git(repo, *args):
    return subprocess.check_output(['git', *args], cwd=repo, stderr=subprocess.PIPE)


def load_overlay(name, errors):
    if name not in KNOWN_OVERLAYS:
        errors.append('Unknown reviewed overlay: ' + name)
        return None
    relative, expected = KNOWN_OVERLAYS[name]
    path = D / relative
    try:
        raw = path.read_bytes()
        overlay = json.loads(raw)
    except (OSError, ValueError) as exc:
        errors.append('Overlay manifest unavailable/invalid: ' + type(exc).__name__)
        return None
    if (not isinstance(overlay, dict) or type(overlay.get('schema_version')) is not int
            or overlay['schema_version'] != 1):
        errors.append('Overlay manifest schema_version must be exactly 1.')
        return None
    if hashlib.sha256(raw).hexdigest() != expected:
        errors.append('Overlay manifest hash mismatch; only the exact reviewed manifest is accepted.')
        return None
    # The byte pin protects every path/hash/size, optional evidence entry and patch identity.
    if overlay['overlay_id'] != name or overlay['base_commit'] != BASE:
        errors.append('Overlay identity/base mismatch.')
        return None
    replacement = overlay['source_replacement']
    paths = [replacement['before']['path'], replacement['after']['path']]
    evidence = overlay['optional_evidence_files']
    if (paths != [SVD, SVD]
            or len({row['path'] for row in evidence}) != len(evidence)
            or any(not row['path'].startswith('docs/qa/evidence/ai3-svd-reveal-motion-regression/')
                   or '..' in Path(row['path']).parts for row in evidence)):
        errors.append('Overlay contains an invalid or unreviewed path.')
        return None
    return overlay


def tree(repo, revision):
    entries = {}
    for record in git(repo, 'ls-tree', '-rz', '--full-tree', revision).split(b'\0'):
        if record:
            fields, path = record.split(b'\t', 1)
            mode, kind, blob = fields.decode().split()
            entries[path.decode()] = (mode, kind, blob)
    return entries


def overlay_tree_checks(repo, head, overlay, errors):
    """Allow one exact tree delta, not a new source HEAD or a relaxed loader."""
    base = tree(repo, BASE)
    current = tree(repo, head)
    replacement = overlay['source_replacement']
    before, after = replacement['before'], replacement['after']
    signature = lambda row: (row['git_mode'], 'blob', row['git_blob'])
    if before['path'] != SVD or after['path'] != SVD or base.get(SVD) != signature(before):
        errors.append('Overlay source path/base blob mismatch.')
        return
    optional = {row['path']: row for row in overlay['optional_evidence_files']}
    allowed = {SVD: after, **optional}
    for path in sorted(base.keys() | current.keys()):
        if base.get(path) != current.get(path):
            row = allowed.get(path)
            if row is None or current.get(path) != signature(row):
                errors.append('Overlay HEAD contains unrelated or unreviewed tree change: ' + path)
    # A non-base commit must actually contain the reviewed scene replacement.
    if head != BASE and current.get(SVD) != signature(after):
        errors.append('Overlay HEAD must be base 927 or an exact reviewed SVD overlay tree.')
    indexed = {}
    for record in git(repo, 'ls-files', '--stage', '-z').split(b'\0'):
        if not record:
            continue
        fields, raw_path = record.split(b'\t', 1)
        mode, blob, stage = fields.decode().split()
        path = raw_path.decode()
        if stage != '0':
            errors.append('Unmerged index entry: ' + path)
        indexed[path] = (mode, 'blob', blob)
    for path in sorted(base.keys() | indexed.keys()):
        if base.get(path) != indexed.get(path):
            row = allowed.get(path)
            if row is None or indexed.get(path) != signature(row):
                errors.append('Overlay index contains unrelated or unreviewed change: ' + path)
    changed = git(repo, 'diff', '--no-ext-diff', '--no-textconv', '--no-renames',
                  '--name-only', '-z', BASE, '--').split(b'\0')
    untracked = git(repo, 'ls-files', '--others', '--exclude-standard', '-z').split(b'\0')
    for raw_path in sorted(set(changed + untracked)):
        if not raw_path:
            continue
        path = raw_path.decode()
        row = allowed.get(path)
        target = repo / path
        if row is None:
            errors.append('Overlay worktree contains unrelated/unreviewed file: ' + path)
        elif (target.is_symlink() or not target.is_file()
              or bool(target.stat().st_mode & 0o111) != (row['git_mode'] == '100755')
              or target.stat().st_size != row['bytes'] or digest(target) != row['sha256']):
            errors.append('Overlay worktree file missing/size/hash/type mismatch: ' + path)
    # An entirely clean base tree is not the requested overlay.
    target = repo / SVD
    if (target.is_symlink() or not target.is_file()
            or bool(target.stat().st_mode & 0o111) != (after['git_mode'] == '100755')
            or target.stat().st_size != after['bytes'] or digest(target) != after['sha256']):
        errors.append('Overlay requires the exact reviewed SVD after bytes: ' + SVD)


def verify(repo, *, strict_external=False, optional_audio=False, overlay_id=None):
    repo = Path(repo).resolve()
    errors = []
    checked = 0

    def check(p, row):
        nonlocal checked
        try:
            if not p.is_file() or p.stat().st_size != row['bytes'] or digest(p) != row['sha256']:
                errors.append(str(p) + ': missing/size/hash mismatch')
            checked += 1
        except OSError as exc:
            errors.append(str(p) + ': ' + type(exc).__name__)

    core = json.loads((D / 'cache-inventory.json').read_text())
    sources = json.loads((D / 'reviewed-source-inventory.json').read_text())
    external = json.loads((D / 'external-validation-dependencies.json').read_text())
    overlay = load_overlay(overlay_id, errors) if overlay_id is not None else None
    head = git(repo, 'rev-parse', 'HEAD').decode().strip()
    if overlay_id is None:
        if head != sources['commit']:
            errors.append('Full-part source HEAD must equal ' + sources['commit']
                          + '; this check is not the separate cache-independent SVD pilot proof.')
    elif overlay is not None:
        if sources['commit'] != BASE:
            errors.append('Overlay source inventory must retain original base ' + BASE)
        else:
            overlay_tree_checks(repo, head, overlay, errors)
    replacement = overlay['source_replacement'] if overlay is not None else None
    source_rows = list(sources['files'])
    if replacement is not None:
        matches = [row for row in source_rows if row['path'] == SVD]
        before = replacement['before']
        if (len(matches) != 1 or any(matches[0][k] != before[k] for k in ['path', 'bytes', 'sha256'])):
            errors.append('Overlay source inventory before identity mismatch.')
        else:
            source_rows = [replacement['after'] if row['path'] == SVD else row for row in source_rows]
    for row in core['files'] + source_rows:
        check(repo / row['path'], row)
    if strict_external:
        for row in external['extra_repo_relative_files'] + external['source_inputs']:
            check(repo / row['path'], row)
        for name, expected in external['required_observed_packages'].items():
            try:
                actual = importlib.metadata.version(name)
            except importlib.metadata.PackageNotFoundError:
                actual = None
            if actual != expected:
                errors.append(f'Package {name}: expected exact {expected}, found {actual}; STOP, do not weaken current().')
        base = Path(os.environ.get('HF_HUB_CACHE', str(Path(os.environ.get(
            'HF_HOME', str(Path.home() / '.cache/huggingface'))) / 'hub')))
        for row in external['gpt2']['files']:
            check(base / row['snapshot_relative_path'], row)
        model_repo = base / 'models--openai-community--gpt2'
        ref = model_repo / 'refs/main'
        if ref.is_file():
            if ref.read_text().strip() != external['gpt2']['revision']:
                errors.append('GPT-2 refs/main points to a different revision.')
        elif sorted(p.name for p in (model_repo / 'snapshots').glob('*')) != [external['gpt2']['revision']]:
            errors.append('GPT-2 snapshot resolution is missing or ambiguous.')
    if optional_audio:
        for block in json.loads((D / 'real-information-audio.json').read_text())['blocks']:
            for row in block['files']:
                check(repo / row['path'], row)
    if git(repo, 'rev-parse', 'HEAD').decode().strip() != head:
        errors.append('Source HEAD changed during preflight.')
    return {
        'scope': 'Read-only source/cache/dependency file hashes and package metadata only; no scene/producer imports, normal loads or model loads. Not a runtime inherited producer guard or visual/audio approval.',
        'reviewed_overlay': overlay_id,
        'strict_external_requested': strict_external,
        'checked_files': checked,
        'errors': errors,
        'next_gate': 'If no errors, run existing cached-only QA with all source/data writers stopped; full production still requires an inherited fail-on-call producer guard coordinated with parent.',
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--strict-external', action='store_true')
    parser.add_argument('--optional-audio', action='store_true')
    parser.add_argument('--overlay', help='Explicit reviewed overlay ID; only svd-reveal-v1 is supported.')
    args = parser.parse_args()
    result = verify(args.repo, strict_external=args.strict_external,
                    optional_audio=args.optional_audio, overlay_id=args.overlay)
    print(json.dumps(result, indent=2))
    return 1 if result['errors'] else 0


if __name__ == '__main__':
    raise SystemExit(main())
