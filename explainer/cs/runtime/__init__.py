"""Runtimes (Part 15): the λ-core compiled to bytecode, a virtual machine with a heap of tagged words, and the
garbage collectors that keep it alive.

* :mod:`.bytecode`: closure conversion and compilation of the λ-core (:mod:`explainer.cs.lang.lam.ml`) to a stack
  bytecode with flat closures, known-arity calls and proper tail calls; the encoding the Pebble VM loads.
* :mod:`.vm`: the reference VM in Python, with pluggable collectors (Cheney's copying, mark–sweep, mark–compact,
  generational) and the statistics the scenes plot.
* :mod:`.pvm`: the same VM written in the Pebble language (Part 13), compiled and run on the Pebble emulator.
* :mod:`.tricolor`: incremental marking under a hostile mutator, with and without write barriers.
* :mod:`.cps`: continuation-passing style, call/cc and generators, on small terms.
"""
