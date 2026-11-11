"""Auditable observations and benchmark protocols for CS15."""
from __future__ import annotations

import hashlib
import math
import re
import subprocess
import tempfile
from pathlib import Path

from explainer.cs.runtime import vm as V


class ObservedCheney(V.Cheney):
    """Track collection observations without calling them object death times."""

    def __init__(self, semispace):
        super().__init__(semispace, track_ages=True)
        self.observed_ids = set()

    def collect(self):
        super().collect()
        a = self.base
        while a < self.free:
            self.observed_ids.add(self.ids[a])
            a += 1 + (self.mem[a] >> 4)

    def observation_summary(self):
        stack, sp, globals_ = self.roots()
        todo = [v >> 1 for v in [*stack[:sp], *globals_] if V._ptr(v)]
        reached = set()
        while todo:
            a = todo.pop()
            if a in reached:
                continue
            assert self.base <= a < self.free
            reached.add(a)
            n = self.mem[a] >> 4
            todo.extend(v >> 1 for v in self.mem[a + 1:a + 1 + n] if V._ptr(v))
        final_ids = {self.ids[a] for a in reached}
        return dict(objects=len(self.lifetimes), collections=len(self.log),
                    observed_at_collection=len(self.observed_ids),
                    never_observed_at_collection=len(self.lifetimes) - len(self.observed_ids),
                    reachable_at_end=len(final_ids),
                    reachable_at_end_never_observed=len(final_ids - self.observed_ids),
                    scope="Last-observed-live allocation ages are lower bounds, not death times. "
                          "Final reachable objects are end-censored; unobserved objects may still be live.")


def positive_seconds(value):
    value = float(value)
    if not math.isfinite(value) or value <= 0:
        raise ValueError(f"Invalid elapsed time: {value}")
    return value


def checked_churn_result(raw, allocations=60_000_000):
    lines = [line.split() for line in raw.splitlines()
             if re.fullmatch(r"-?\d+ [\d.eE+-]+", line.strip())]
    assert len(lines) == 1, lines
    checksum, seconds = lines[0]
    assert int(checksum) == allocations * (allocations - 1) // 2, checksum
    return positive_seconds(seconds)


def java_pause_events(raw):
    events = []
    for line in raw.splitlines():
        if " Pause " not in line:
            continue
        match = re.search(r"GC\((\d+)\) (.*?Pause.*?) ([\d.eE+-]+)ms$", line)
        assert match, line
        event = dict(cycle=int(match[1]), phase=match[2], ms=float(match[3]), raw=line)
        assert math.isfinite(event['ms']) and event['ms'] >= 0
        events.append(event)
    assert events, "No JVM pause events parsed"
    assert len({e['raw'] for e in events}) == len(events)
    return events


def go_pause_events(raw):
    events = []
    for line in raw.splitlines():
        if not line.startswith('gc '):
            continue
        match = re.search(r"^gc (\d+) @.*?: ([\d.eE+-]+)\+([\d.eE+-]+)\+([\d.eE+-]+) ms clock", line)
        assert match, line
        for phase, group in [('sweep termination', 2), ('mark termination', 4)]:
            ms = float(match[group])
            assert math.isfinite(ms) and ms >= 0
            events.append(dict(cycle=int(match[1]), phase=phase, ms=ms, raw=line))
    assert events, "No Go pause events parsed"
    return events


def barrier_color_witness():
    """Apply the same scripted stores to the actual tri-color teaching model."""
    from explainer.cs.runtime import tricolor as T
    rows = []
    for barrier in (None, 'dijkstra', 'yuasa'):
        heap = T.Heap(fields=[[1, None], [2, None], [3, None], [None, None]],
                      color=[T.BLACK, T.BLACK, T.GRAY, T.WHITE], regs=[0], gray=[2])
        stages = [heap.color[3]]
        T.write(heap, 1, 1, 3, barrier)
        stages.append(heap.color[3])
        T.write(heap, 2, 0, None, barrier)
        stages.append(heap.color[3])
        while heap.mark_step():
            pass
        stages.append(heap.color[3])
        rows.append(dict(barrier=barrier or 'none', colors=stages,
                         reachable=3 in heap.reachable(), lost=heap.color[3] == T.WHITE))
    return rows


def measure_dispatch(sh, source, version):
    flags = ['-O2', '-std=c++17', '-fno-devirtualize', '-fno-devirtualize-speculatively', '-fno-lto']
    with tempfile.TemporaryDirectory() as directory:
        Path(directory, 'x.cpp').write_text(source)
        sh(['g++', *flags, '-o', 'x', 'x.cpp'], cwd=directory)
        raw = sh(['./x'], cwd=directory)
        assembly = sh(['objdump', '-d', '--disassemble=run_virtual', 'x'], cwd=directory)
        assert re.search(r'call\s+\*', assembly), 'Virtual loop contains no indirect call'
        # A smaller instance checks the same arithmetic and exception paths under UBSan.
        sh(['g++', *flags, '-DN=100000', '-DM=1000', '-fsanitize=undefined',
            '-fno-sanitize-recover=all', '-o', 'checked', 'x.cpp'], cwd=directory)
        sanitizer_output = sh(['./checked'], cwd=directory)
    rows = {}
    for line in raw.splitlines():
        name, duration, checksum, iterations = line.split()
        seconds = positive_seconds(duration)
        rows[name] = dict(seconds=seconds, checksum=int(checksum), iterations=int(iterations),
                          ns=1e9 * seconds / int(iterations))
    assert set(rows) == {'direct', 'virtual_mono', 'virtual_poly', 'plain', 'try', 'setjmp', 'throw'}
    n = rows['direct']['iterations']
    mask = (1 << 64) - 1
    squares = n * (n - 1) * (2 * n - 1) // 6
    expected = dict(direct=squares & mask, virtual_mono=squares & mask,
                    virtual_poly=sum(i * i if i % 2 == 0 else i * i // 2 for i in range(n)) & mask,
                    plain=n * (n + 1) // 2 & mask, try_=n * (n + 1) // 2 & mask)
    expected['try'] = expected.pop('try_')
    j = rows['setjmp']['iterations']
    expected['setjmp'] = j * (j + 1) // 2 & mask
    expected['throw'] = -rows['throw']['iterations'] & mask
    assert all(rows[name]['checksum'] == value for name, value in expected.items()), rows
    return {**{name + '_ns': row['ns'] for name, row in rows.items()}, 'gcc': version,
            'protocol': dict(flags=flags, repeats=3, statistic='minimum of three runs',
                             arithmetic='uint64_t; defined modulo 2^64 accumulation',
                             opaque_boundaries='GCC noipa; virtual devirtualization explicitly disabled',
                             scope='single-host illustrative loop timings; no universal call-cost ordering'),
            'measurements': rows, 'raw_output': raw, 'sanitizer_output': sanitizer_output,
            'source_sha256': hashlib.sha256(source.encode()).hexdigest(),
            'virtual_loop_disassembly': assembly}
