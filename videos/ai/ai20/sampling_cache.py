"""Part-20-only native cache contract. Reads never invoke a producer."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

from explainer.ai.cache import Cache
from explainer.cache_lock import cache_lock

CONTRACT = 'ai20_sampling_v2'
PRODUCTS = ('toys', 'bilinear', 'jsw', 'langevin', 'hopfield', 'ar2d', 'vae2d',
            'collapse2d', 'flow2d', 'gan2d', 'gan2d_collapse', 'ebm2d', 'cnf',
            'eval2d', 'classifier', 'rbm', 'vae_map', 'vae', 'gan', 'flow',
            'pixelcnn', 'wgan', 'beta', 'collapse', 'vq', 'evaluate')

DEPENDENCIES = {
    'gan2d_collapse': ('gan2d',),
    'eval2d': ('toys', 'ar2d', 'vae2d', 'gan2d', 'flow2d', 'ebm2d'),
    'vae': ('classifier',), 'vq': ('classifier',),
    'gan': ('classifier',), 'wgan': ('classifier',), 'flow': ('classifier',),
    'pixelcnn': ('classifier',), 'collapse': ('classifier',),
    'evaluate': ('classifier', 'pixelcnn', 'vae', 'gan', 'wgan', 'flow', 'vq'),
}


def sha256(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()


def consumer_source_sha256():
    source = Path(__file__).parent
    return {name: sha256(source / name)
            for name in ('compute.py', 'gendigits.py', 'gen2d.py', 'sampling_cache.py')}


def consumer_class(model):
    cls = type(model)
    module = cls.__module__
    if module == '__main__':
        main_file = getattr(sys.modules.get('__main__'), '__file__', None)
        if main_file is not None and Path(main_file).resolve() == Path(__file__).with_name('compute.py').resolve():
            module = 'videos.ai.ai20.compute'
    return module + '.' + cls.__qualname__


def validate_origin(origin, model=None):
    if origin['kind'] not in ('accepted-migration', 'explicit-generation'):
        raise ValueError('Unknown native product/state origin')
    if origin['consumer_source_sha256'] != consumer_source_sha256():
        raise ValueError('Consumer numerical source has changed; reconcile compatibility before use')
    if model is not None and origin['consumer_class'] != consumer_class(model):
        raise ValueError('Model consumer class binding mismatch')


def atomic_json(path, value):
    path = Path(path)
    tmp = path.with_suffix(path.suffix + '.tmp')
    tmp.write_text(json.dumps(value, sort_keys=True, indent=1, allow_nan=False) + '\n')
    tmp.replace(path)


def state_hash(state):
    h = hashlib.sha256()
    for key, value in sorted(state.items()):
        h.update(key.encode())
        h.update(str(value.dtype).encode())
        h.update(str(tuple(value.shape)).encode())
        h.update(value.detach().cpu().contiguous().numpy().tobytes())
    return h.hexdigest()


def native_receipt(directory, name, origin, scale=1.0):
    directory = Path(directory)
    files = {name + '.json': sha256(directory / (name + '.json'))}
    npz = directory / (name + '.npz')
    if npz.exists():
        files[npz.name] = sha256(npz)
    dependencies = {}
    for dependency in DEPENDENCIES.get(name, ()):
        validate_native(directory, dependency, scale)
        dependencies[dependency] = sha256(directory / (dependency + '.contract.json'))
    return dict(contract=CONTRACT, scale=scale, item=name, files=files, origin=origin, dependencies=dependencies)


def validate_native(directory, name, scale=1.0):
    """Cache-only validation needs native files/contract, never raw data or models."""
    directory = Path(directory)
    if name not in PRODUCTS:
        raise ValueError(f'Unknown Part20 native product: {name}')
    marker = directory / (name + '.contract.json')
    try:
        receipt = json.loads(marker.read_text())
        if receipt['contract'] != CONTRACT or receipt['item'] != name or receipt['scale'] != scale:
            raise ValueError('Wrong item/sampling contract')
        validate_origin(receipt['origin'])
        actual_files = {name + '.json'}
        if (directory / (name + '.npz')).exists():
            actual_files.add(name + '.npz')
        if set(receipt['files']) != actual_files:
            raise ValueError('JSON/NPZ presence mismatch')
        for filename, digest in receipt['files'].items():
            if sha256(directory / filename) != digest:
                raise ValueError(f'Native file hash mismatch: {filename}')
        if set(receipt['dependencies']) != set(DEPENDENCIES.get(name, ())):
            raise ValueError('Wrong native dependency set')
        for dependency, digest in receipt['dependencies'].items():
            if sha256(directory / (dependency + '.contract.json')) != digest:
                raise ValueError(f'Stale dependency: {dependency}')
            validate_native(directory, dependency, scale)
    except (OSError, KeyError, ValueError, AssertionError, TypeError) as error:
        raise RuntimeError(f'Part20 {name}: missing/invalid {marker}; import an accepted '
                           f'{CONTRACT} product or explicitly compute this named item. '
                           'No producer or download was started.') from error
    return receipt


class SamplingCache(Cache):
    """Versioned Part20 adapter; shared Cache behavior is not changed."""
    def __init__(self, scale=1.0):
        super().__init__(CONTRACT)
        self.scale = scale

    def load(self, name):
        with cache_lock(self.path(name)):
            validate_native(self.dir, name, self.scale)
            # Never enter shared Cache.load's compute-on-missing branch.
            import numpy as np
            value = json.loads(self.path(name).read_text())
            arrays = self.path(name).with_suffix('.npz')
            if arrays.exists():
                with np.load(arrays, allow_pickle=False) as archive:
                    value.update({key: archive[key] for key in archive.files})
            return value

    def save(self, name, out):
        if name not in PRODUCTS:
            raise ValueError(f'Unknown Part20 native product: {name}')
        with cache_lock(self.path(name)):
            marker = self.dir / (name + '.contract.json')
            marker.unlink(missing_ok=True)
            super().save(name, out)
            origin = dict(kind='explicit-generation',
                          consumer_source_sha256=consumer_source_sha256())
            atomic_json(marker, native_receipt(self.dir, name, origin, self.scale))

    def partial(self, name, params):
        versioned = dict(sampling_contract=CONTRACT, scale=self.scale,
                         consumer_source_sha256=consumer_source_sha256(), recipe_params=params)
        path = self.dir / (name + '.partial.json')
        if path.exists():
            saved = json.loads(path.read_text())
            if saved.get('params') != versioned:
                raise RuntimeError(f'{path}: incompatible partial; preserve and reconcile it. '
                                   'No completed work was discarded or retrained.')
        return super().partial(name, versioned)

    def main(self, items, description=None):
        """Explicit CLI generation; an invocation without names requests all items."""
        parser = argparse.ArgumentParser(description=description)
        parser.add_argument('names', nargs='*')
        parser.add_argument('--force', action='store_true')
        args = parser.parse_args()
        requested = args.names or tuple(items)
        for name in requested:
            if name not in items:
                parser.error(f'unknown item: {name}')
        self.items = items
        for name in requested:
            with cache_lock(self.path(name)):
                if self.path(name).exists() or (self.dir / (name + '.contract.json')).exists():
                    validate_native(self.dir, name, self.scale)
                    if not args.force:
                        print(f'  cached {CONTRACT}/{name}')
                        continue
                # Fail before expensive training when an explicit dependency is absent.
                for dependency in DEPENDENCIES.get(name, ()):
                    validate_native(self.dir, dependency, self.scale)
                print(f'  explicitly computing {CONTRACT}/{name}', flush=True)
                self.save(name, items[name]())
