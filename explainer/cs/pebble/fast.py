"""A compiled fast path for netlists: the same gates, evaluated by C instead of a Python loop.

    f = Fast(seq)                 # a Seq (registers kept inside the compiled state) or a plain Circuit
    f.reset(lanes=64)
    out = f.eval({"instr": words, "rdata": data})          # outputs, state unchanged
    out = f.eval({"instr": words, "rdata": data}, commit=True)   # ... then every register loads its D input

Lanes are bit-parallel exactly as in :mod:`.hdl`: bit j of each 64-bit word is copy j of the machine, so 64 copies
run in one pass.  Integer values in and out are numpy arrays with one entry per lane (``int64``, or ``uint64`` for
32-bit and wider signals).  The netlist is turned into one C function, one line per gate, compiled once with the
system ``cc`` and cached under ``.cache/hdl`` by a hash of the netlist; without a compiler the same interface falls
back to :meth:`hdl.Circuit.evaluate` (slow, but identical).
"""

from __future__ import annotations

import ctypes
import hashlib
import os
import subprocess
import tempfile
from pathlib import Path

import numpy as np

from .hdl import ONES, Circuit

CACHE = Path(__file__).resolve().parents[3] / ".cache" / "hdl"

_OPS = {"NAND": "~(v[{0}] & v[{1}])", "AND": "v[{0}] & v[{1}]", "OR": "v[{0}] | v[{1}]", "NOT": "~v[{0}]",
        "XOR": "v[{0}] ^ v[{1}]", "NOR": "~(v[{0}] | v[{1}])", "XNOR": "~(v[{0}] ^ v[{1}])", "BUF": "v[{0}]",
        "CONST0": "0", "CONST1": "~(uint64_t)0"}


def _source(c: Circuit, in_wires: list[int], out_wires: list[int], d_wires: list[int], q_wires: list[int]) -> str:
    lines = ["#include <stdint.h>", "#include <stdlib.h>",
             f"#define N {len(c.kinds)}",
             "void eval(int lanes, const uint64_t *in, uint64_t *state, uint64_t *out, int commit) {",
             "  static uint64_t v[N];",
             "  for (int w = 0; w < lanes; w++) {"]
    ni, nq, no = len(in_wires), len(q_wires), len(out_wires)
    for k, wire in enumerate(in_wires):
        lines.append(f"    v[{wire}] = in[{k} * lanes + w];")
    for k, wire in enumerate(q_wires):
        lines.append(f"    v[{wire}] = state[{k} * lanes + w];")
    for i, (kind, args) in enumerate(zip(c.kinds, c.args)):
        if kind == "INPUT":
            continue
        lines.append(f"    v[{i}] = {_OPS[kind].format(*args)};")
    for k, wire in enumerate(out_wires):
        lines.append(f"    out[{k} * lanes + w] = v[{wire}];")
    if nq:
        lines.append("    if (commit) {")
        for k, wire in enumerate(d_wires):
            lines.append(f"      state[{k} * lanes + w] = v[{wire}];")
        lines.append("    }")
    lines += ["  }", "}", f"int n_in(void) {{ return {ni}; }}", f"int n_out(void) {{ return {no}; }}",
              f"int n_state(void) {{ return {nq}; }}"]
    return "\n".join(lines) + "\n"


def _compile(src: str) -> ctypes.CDLL | None:
    key = hashlib.sha256(src.encode()).hexdigest()[:20]
    CACHE.mkdir(parents=True, exist_ok=True)
    so = CACHE / f"net_{key}.so"
    if not so.exists():
        with tempfile.TemporaryDirectory() as td:
            cfile = Path(td) / "net.c"
            cfile.write_text(src)
            tmp = Path(td) / "net.so"
            try:
                subprocess.run([os.environ.get("CC", "cc"), "-O1", "-shared", "-fPIC", "-o", str(tmp), str(cfile)],
                               check=True, capture_output=True, timeout=600)
            except (OSError, subprocess.SubprocessError):
                return None
            os.replace(tmp, so)
    lib = ctypes.CDLL(str(so))
    P = ctypes.POINTER(ctypes.c_uint64)
    lib.eval.argtypes = [ctypes.c_int, P, P, P, ctypes.c_int]
    lib.eval.restype = None
    return lib


class Fast:
    """A compiled netlist.  ``seq`` is a :class:`.seq.Seq` (its registers live in ``self.state``) or a Circuit."""

    def __init__(self, seq):
        self.seq = seq if hasattr(seq, "regs") else None
        self.c: Circuit = seq.c if self.seq else seq
        c = self.c
        self.reg_names = list(self.seq.regs) if self.seq else []
        self.in_names = [n for n in c.inputs if not n.startswith("q:")]
        self.out_names = [n for n in c.outputs if not n.startswith("d:")]
        self.in_wires = [w for n in self.in_names for w in c.inputs[n]]
        self.out_wires = [w for n in self.out_names for w in c.outputs[n]]
        self.q_wires = [w for n in self.reg_names for w in c.inputs["q:" + n]]
        self.d_wires = [w for n in self.reg_names for w in c.outputs["d:" + n]]
        self.lib = _compile(_source(c, self.in_wires, self.out_wires, self.d_wires, self.q_wires))
        self.lanes = 1
        self.state = np.zeros((len(self.q_wires), 1), np.uint64)

    @property
    def compiled(self) -> bool:
        return self.lib is not None

    # -- packing: integers per copy <-> bit-parallel words ---------------------------------------------------
    @staticmethod
    def _pack(vals: np.ndarray, width: int, lanes: int) -> np.ndarray:
        """``vals`` (one integer per copy, up to 64 * lanes copies) -> (width, lanes) uint64 words."""
        vals = np.asarray(vals, dtype=np.uint64)
        n = vals.shape[0]
        bits = ((vals[None, :] >> np.arange(width, dtype=np.uint64)[:, None]) & np.uint64(1)).astype(np.uint8)
        pad = lanes * 64 - n
        if pad:
            bits = np.concatenate([bits, np.zeros((width, pad), np.uint8)], axis=1)
        return np.packbits(bits.reshape(width, lanes, 64)[:, :, ::-1], axis=2).view(">u8").reshape(width, lanes) \
            .astype(np.uint64)

    @staticmethod
    def _unpack(words: np.ndarray, copies: int) -> np.ndarray:
        """(width, lanes) words -> one integer per copy."""
        width, lanes = words.shape
        b = np.unpackbits(words.astype(">u8").view(np.uint8).reshape(width, lanes, 8), axis=2)
        b = b.reshape(width, lanes, 64)[:, :, ::-1].reshape(width, lanes * 64)[:, :copies].astype(np.uint64)
        return (b << np.arange(width, dtype=np.uint64)[:, None]).sum(axis=0, dtype=np.uint64)

    def reset(self, copies: int = 1, init: dict[str, int] | None = None) -> None:
        self.copies = copies
        self.lanes = (copies + 63) // 64
        rows = []
        for n in self.reg_names:
            width, default = self.seq.regs[n]
            v = (init or {}).get(n, default)
            rows.append(self._pack(np.broadcast_to(np.asarray(v, dtype=np.uint64), (copies,)), width, self.lanes))
        self.state = np.ascontiguousarray(np.concatenate(rows) if rows else np.zeros((0, self.lanes), np.uint64))

    def get(self, reg: str) -> np.ndarray:
        """A register's value in every copy."""
        k = 0
        for n in self.reg_names:
            width = self.seq.regs[n][0]
            if n == reg:
                return self._unpack(self.state[k:k + width], self.copies)
            k += width
        raise KeyError(reg)

    def set(self, reg: str, values) -> None:
        k = 0
        for n in self.reg_names:
            width = self.seq.regs[n][0]
            if n == reg:
                self.state[k:k + width] = self._pack(np.broadcast_to(np.asarray(values, dtype=np.uint64),
                                                                     (self.copies,)), width, self.lanes)
                return
            k += width
        raise KeyError(reg)

    def eval(self, inputs: dict, commit: bool = False) -> dict[str, np.ndarray]:
        lanes, c = self.lanes, self.c
        ins = np.ascontiguousarray(np.concatenate([
            self._pack(np.broadcast_to(np.asarray(inputs[n], dtype=np.uint64), (self.copies,)), len(c.inputs[n]),
                       lanes) for n in self.in_names]) if self.in_names else np.zeros((0, lanes), np.uint64))
        out = np.zeros((len(self.out_wires), lanes), np.uint64)
        if self.lib is not None:
            P = ctypes.POINTER(ctypes.c_uint64)
            self.lib.eval(lanes, ins.ctypes.data_as(P), self.state.ctypes.data_as(P), out.ctypes.data_as(P),
                          int(commit))
        else:  # the slow, identical fallback
            vals = {}
            k = 0
            for n in self.in_names:
                w = len(c.inputs[n])
                vals[n] = list(ins[k:k + w])
                k += w
            k = 0
            for n in self.reg_names:
                w = self.seq.regs[n][0]
                vals["q:" + n] = list(self.state[k:k + w])
                k += w
            res = c.evaluate(vals)
            k = 0
            for n in self.out_names:
                w = len(c.outputs[n])
                out[k:k + w] = np.array(res[n])
                k += w
            if commit and self.reg_names:
                self.state = np.ascontiguousarray(np.concatenate([np.array(res["d:" + n]) for n in self.reg_names]))
        res, k = {}, 0
        for n in self.out_names:
            w = len(c.outputs[n])
            res[n] = self._unpack(out[k:k + w], self.copies)
            k += w
        return res


__all__ = ["Fast", "ONES"]
