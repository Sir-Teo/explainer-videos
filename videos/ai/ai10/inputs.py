"""Verified, cached-only scene inputs. This module never imports scientific producers."""
from __future__ import annotations

import hashlib
import io
import json
import math
import os
from pathlib import Path
import stat
import zipfile

import numpy as np


MAX_ARRAY_BYTES = 64 * 1024 * 1024
MAX_ARRAY_MEMBERS = 256


class SceneInputs:
    """Read explicitly adopted bytes; scientific provenance must be checked by the caller."""

    def __init__(self, root: Path):
        self.root = Path(root).resolve()
        self.manifest = Path('.cache/ai10/scene-inputs.json')
        self._manifest_digest = None

    def _bytes(self, relative: str) -> bytes:
        path = Path(relative)
        if path.is_absolute() or not path.parts or path.parts[0] != '.cache' or '..' in path.parts:
            raise ValueError('Scene input paths must stay inside the repository cache')
        descriptors = []
        directories = []
        try:
            parent_fd = os.open(self.root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
            descriptors.append(parent_fd)
            directories.append((self.root, os.fstat(parent_fd)))
            named = self.root
            for component in path.parts[:-1]:
                parent_fd = os.open(component, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                                    dir_fd=parent_fd)
                descriptors.append(parent_fd)
                named = named / component
                directories.append((named, os.fstat(parent_fd)))
            fd = os.open(path.name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=parent_fd)
            descriptors.append(fd)
            first = os.fstat(fd)
            before = os.stat(path.name, dir_fd=parent_fd, follow_symlinks=False)
            if not stat.S_ISREG(first.st_mode) or first.st_size > 64 * 1024 * 1024:
                raise ValueError('Scene inputs must be bounded regular files')
            with os.fdopen(fd, 'rb', closefd=False) as stream:
                raw = stream.read(first.st_size + 1)
            last = os.fstat(fd)
            after = os.stat(path.name, dir_fd=parent_fd, follow_symlinks=False)
            identity = lambda x: (x.st_dev, x.st_ino, x.st_size, x.st_mtime_ns, x.st_ctime_ns)
            if not (identity(before) == identity(first) == identity(last) == identity(after)) or len(raw) != first.st_size:
                raise ValueError('Scene input changed while reading')
            for named, opened in directories:
                current = named.lstat()
                if not stat.S_ISDIR(current.st_mode) or (current.st_dev, current.st_ino) != (opened.st_dev, opened.st_ino):
                    raise ValueError('Scene input directory changed while reading')
            return raw
        except FileNotFoundError:
            raise
        except OSError as exc:
            raise ValueError('Scene inputs require ordinary files and directories') from exc
        finally:
            for fd in reversed(descriptors):
                os.close(fd)

    def _entry(self, part: str, name: str) -> dict:
        if part not in {'ai1', 'ai7', 'ai9', 'ai10'} or not name.isascii() or not name.isidentifier():
            raise ValueError('Unknown scene input name')
        raw = self._bytes(str(self.manifest))
        digest = hashlib.sha256(raw).hexdigest()
        if self._manifest_digest is not None and digest != self._manifest_digest:
            raise ValueError('Scene input manifest changed; start a new process')
        manifest = json.loads(raw)
        if type(manifest.get('version')) is not int or manifest['version'] != 1:
            raise ValueError('Expected scene input manifest version 1')
        key = f'{part}/{name}'
        if key not in manifest.get('inputs', {}):
            raise FileNotFoundError(f'No verified scene input declared for {key}')
        entry = manifest['inputs'][key]
        if entry.get('kind') not in {'canonical', 'qualified'}:
            raise ValueError('Declare canonical or qualified scene input')
        if entry['kind'] == 'qualified' and (not isinstance(entry.get('qualification'), str)
                                              or not entry['qualification'].strip()):
            raise ValueError('Alternate scene inputs need an explicit qualification')
        self._manifest_digest = digest
        return entry

    def _verified(self, entry: dict, field: str, canonical: str) -> bytes:
        spec = entry[field]
        expected = spec['sha256']
        if not isinstance(expected, str) or len(expected) != 64 or any(c not in '0123456789abcdef' for c in expected):
            raise ValueError('Expected a SHA256 identity for every input file')
        if entry['kind'] == 'canonical' and spec['path'] != canonical:
            raise ValueError('An alternate path requires a qualified input declaration')
        raw = self._bytes(spec['path'])
        if hashlib.sha256(raw).hexdigest() != expected:
            raise ValueError('Scene input checksum mismatch')
        return raw

    def _check_arrays(self, raw: bytes) -> None:
        # Compressed size alone does not bound allocation from an NPY header.
        with zipfile.ZipFile(io.BytesIO(raw)) as archive:
            members = archive.infolist()
            if len(members) > MAX_ARRAY_MEMBERS or len({m.filename for m in members}) != len(members):
                raise ValueError('Too many or duplicate scene array members')
            if sum(m.file_size for m in members) > MAX_ARRAY_BYTES:
                raise ValueError('Scene array decompressed size exceeds the bound')
            for member in members:
                if member.is_dir() or not member.filename.endswith('.npy') or '/' in member.filename:
                    raise ValueError('Unexpected scene array member')
                with archive.open(member) as stream:
                    version = np.lib.format.read_magic(stream)
                    if version == (1, 0):
                        shape, _, dtype = np.lib.format.read_array_header_1_0(stream, max_header_size=16384)
                    elif version == (2, 0):
                        shape, _, dtype = np.lib.format.read_array_header_2_0(stream, max_header_size=16384)
                    else:
                        raise ValueError('Unsupported scene array format')
                    if dtype.hasobject or any(n < 0 for n in shape):
                        raise ValueError('Scene arrays must have bounded numeric or text values')
                    count = math.prod(shape)
                    size = count * dtype.itemsize
                    if count > MAX_ARRAY_BYTES or size > MAX_ARRAY_BYTES:
                        raise ValueError('Scene array shape exceeds the bound')
                    if size != member.file_size - stream.tell():
                        raise ValueError('Scene array payload does not match its header')

    def load(self, part: str, name: str) -> dict:
        entry = self._entry(part, name)
        stem = f'.cache/{part}/{name}'
        data = json.loads(self._verified(entry, 'json', stem + '.json'))
        if not isinstance(data, dict):
            raise ValueError('A scene cache must contain an object')
        if 'npz' in entry:
            raw = self._verified(entry, 'npz', stem + '.npz')
            self._check_arrays(raw)
            with np.load(io.BytesIO(raw), allow_pickle=False) as arrays:
                data.update({key: arrays[key] for key in arrays.files})
        return data

    def text(self, part: str, name: str) -> str:
        entry = self._entry(part, name)
        raw = self._verified(entry, 'text', f'.cache/{part}/{name}.txt')
        with io.TextIOWrapper(io.BytesIO(raw), encoding='utf-8', newline=None) as stream:
            return stream.read()


_INPUTS = SceneInputs(Path(__file__).resolve().parents[3])


def load(name: str) -> dict:
    return _INPUTS.load('ai10', name)


def load_cached(part: str, name: str) -> dict:
    return _INPUTS.load(part, name)


def read_cached_text(part: str, name: str) -> str:
    return _INPUTS.text(part, name)
