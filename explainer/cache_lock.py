"""Serialize one cache item across local threads and rendering processes."""

from contextlib import contextmanager
from functools import wraps
from pathlib import Path
import fcntl
import threading

_guards = {}
_local = threading.local()


def cache_signature(path):
    """Identity of both published files, including atomic replacements."""
    identity = []
    for p in (Path(path), Path(path).with_suffix(".npz")):
        try:
            stat = p.stat()
            identity.append((stat.st_dev, stat.st_ino, stat.st_mtime_ns, stat.st_size))
        except FileNotFoundError:
            identity.append(None)
    return tuple(identity)


@contextmanager
def cache_lock(path):
    path = Path(path).resolve()
    guard = _guards.setdefault(path, threading.RLock())
    with guard:
        held = getattr(_local, "held", None)
        if held is None:
            held = _local.held = set()
        if path in held:
            yield
            return
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.with_suffix(path.suffix + ".lock").open("a") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            held.add(path)
            try:
                yield
            finally:
                held.remove(path)


def locked_item(path_for):
    def decorate(function):
        @wraps(function)
        def wrapped(*args, **kwargs):
            with cache_lock(path_for(*args, **kwargs)):
                return function(*args, **kwargs)
        return wrapped
    return decorate
