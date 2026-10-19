"""The series' own reverse-mode automatic differentiation, small enough to read in one sitting (Part 4, "Change").

    from explainer.ai.autodiff import Tensor
    w = Tensor(np.zeros((27, 27)), requires_grad=True)
    loss = cross_entropy(w[prev], nxt)        # a forward pass builds the graph
    loss.backward()                           # one backward pass fills w.grad with dloss/dw
    w.data -= 0.5 * w.grad

Every operation records its inputs and how to send a gradient back to them (the "vector-Jacobian product").
``backward`` visits the graph in reverse topological order, so each node passes its gradient on only once all of
its uses have reported in: the chain rule, run backwards.  Part 4 checks it against finite differences and against
PyTorch; later parts train with it.
"""

from __future__ import annotations

import numpy as np


def _unbroadcast(g: np.ndarray, shape: tuple) -> np.ndarray:
    """Sum a gradient over the axes numpy broadcast, so it matches the input's shape."""
    while g.ndim > len(shape):
        g = g.sum(axis=0)
    for i, n in enumerate(shape):
        if n == 1 and g.shape[i] != 1:
            g = g.sum(axis=i, keepdims=True)
    return g


class Tensor:
    def __init__(self, data, requires_grad: bool = False, parents=(), op: str = ""):
        self.data = np.asarray(data, dtype=float)
        self.grad = np.zeros_like(self.data) if requires_grad else None
        self.requires_grad = requires_grad
        self.parents = parents  # (tensor, function taking the output's gradient to this input's gradient)
        self.op = op

    # -- building the graph ------------------------------------------------
    @staticmethod
    def _wrap(x) -> "Tensor":
        return x if isinstance(x, Tensor) else Tensor(x)

    def _make(self, data, parents, op):
        need = any(p.requires_grad for p, _ in parents)
        return Tensor(data, requires_grad=need, parents=tuple((p, f) for p, f in parents if p.requires_grad), op=op)

    def __add__(self, other):
        o = self._wrap(other)
        return self._make(self.data + o.data, [(self, lambda g: _unbroadcast(g, self.data.shape)),
                                               (o, lambda g: _unbroadcast(g, o.data.shape))], "+")

    __radd__ = __add__

    def __neg__(self):
        return self._make(-self.data, [(self, lambda g: -g)], "neg")

    def __sub__(self, other):
        return self + (-self._wrap(other))

    def __rsub__(self, other):
        return self._wrap(other) + (-self)

    def __mul__(self, other):
        o = self._wrap(other)

        def to_self(g):  # d(ab)/da = b
            return _unbroadcast(g * o.data, self.data.shape)

        def to_other(g):  # d(ab)/db = a
            return _unbroadcast(g * self.data, o.data.shape)

        return self._make(self.data * o.data, [(self, to_self), (o, to_other)], "*")

    __rmul__ = __mul__

    def __truediv__(self, other):
        return self * self._wrap(other) ** -1

    def __pow__(self, k: float):
        return self._make(self.data ** k, [(self, lambda g: g * k * self.data ** (k - 1))], f"**{k}")

    def __matmul__(self, other):
        o = self._wrap(other)
        return self._make(self.data @ o.data, [(self, lambda g: g @ o.data.T), (o, lambda g: self.data.T @ g)], "@")

    def __getitem__(self, idx):
        def back(g):
            out = np.zeros_like(self.data)
            np.add.at(out, idx, g)  # rows picked more than once collect all their gradients
            return out
        return self._make(self.data[idx], [(self, back)], "[]")

    def exp(self):
        e = np.exp(self.data)
        return self._make(e, [(self, lambda g: g * e)], "exp")

    def log(self):
        return self._make(np.log(self.data), [(self, lambda g: g / self.data)], "log")

    def tanh(self):
        t = np.tanh(self.data)
        return self._make(t, [(self, lambda g: g * (1 - t * t))], "tanh")

    def relu(self):
        return self._make(np.maximum(self.data, 0), [(self, lambda g: g * (self.data > 0))], "relu")

    def sum(self, axis=None, keepdims=False):
        def back(g):
            if axis is not None and not keepdims:
                g = np.expand_dims(g, axis)
            return np.broadcast_to(g, self.data.shape).copy()
        return self._make(self.data.sum(axis=axis, keepdims=keepdims), [(self, back)], "sum")

    def mean(self, axis=None):
        n = self.data.size if axis is None else self.data.shape[axis]
        return self.sum(axis=axis) * (1.0 / n)

    # -- running the chain rule backwards ----------------------------------
    def backward(self):
        order, seen = [], set()

        def visit(t):
            if id(t) in seen:
                return
            seen.add(id(t))
            for p, _ in t.parents:
                visit(p)
            order.append(t)

        visit(self)
        grads = {id(self): np.ones_like(self.data)}
        for t in reversed(order):
            g = grads.pop(id(t), None)
            if g is None:
                continue
            if t.grad is not None and not t.parents:
                t.grad += g  # a leaf: a parameter or an input that asked for its gradient
            for p, f in t.parents:
                grads[id(p)] = grads.get(id(p), 0) + f(g)


def log_softmax(z: Tensor, axis: int = -1) -> Tensor:
    m = Tensor(z.data.max(axis=axis, keepdims=True))  # a constant shift, for numerical safety
    s = z - m
    return s - s.exp().sum(axis=axis, keepdims=True).log()


def cross_entropy(logits: Tensor, targets: np.ndarray) -> Tensor:
    """The average surprise, in nats, of ``targets`` under the softmax of each row of ``logits``."""
    lp = log_softmax(logits)
    return -lp[np.arange(len(targets)), targets].mean()
