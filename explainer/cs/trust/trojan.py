"""Ken Thompson's *Reflections on Trusting Trust* (1984) and David A. Wheeler's diverse double-compiling (2009),
made concrete and testable on the series' own machinery.

**A compiler, honestly.**  So the three stages are visible, the "language" is Python source text and a *compiler*
is a Python program defining ``compile(src) -> bytes``.  The *binary* of a compiler is the marshalled code object of
its source, round-tripped through ``marshal`` into a canonical byte string (so identical source always yields
identical bytes, independent of how the caller happens to hold the object).  *Running* a binary is
``exec(marshal.loads(binary))`` and calling the function it defines.  A compiler can therefore compile its own
source, which is all Thompson's attack needs.

A marshalled code object is CPython bytecode, so the binaries' sizes and hashes depend on the interpreter version:
the film's 499, 498 and 1,119 bytes are Python 3.12's (the version ``pyproject.toml`` pins); 3.13 gives 507, 506
and 1,131.  Every equality and difference the film shows holds on any version.

**The attack (Thompson).**

1. ``login(password)`` accepts one correct password; a *backdoored* login also accepts a magic password.
2. The trojaned compiler *binary*, when it compiles the ``login`` source, silently inserts the backdoor; when it
   compiles a *compiler's* source, it inserts its own trojan into the output.  The trojan carries its own text and
   re-emits it -- Part 25's quine trick -- so it survives though no compiler source mentions it.
3. Delete the trojan from the source.  Compiling the clean compiler source with the trojaned binary yields a
   trojaned binary again (a fixpoint: bit-for-bit the same binary), and that binary still backdoors ``login``.

**The defence (Wheeler, DDC).**  Compile the clean compiler source with the suspect binary and, separately, with an
*independent* trusted compiler; use each result to compile the compiler source a second time, and compare the two
stage-2 binaries bit for bit.  Equal for a clean suspect, different for the trojaned one -- a trojan the trusted
compiler does not share cannot survive the cross-check.

**Reproducible builds.**  A build that stamps the time or the build path into the artifact differs run to run;
normalise those and the bytes become identical -- the precondition DDC's bit-for-bit comparison relies on.

After Thompson, *Communications of the ACM* 27(8), 1984; Wheeler, *Fully Countering Trusting Trust through Diverse
Double-Compiling*, 2009; and Part 25's quines.
"""

from __future__ import annotations

import builtins
import hashlib
import marshal

MAGIC = "xyzzy-open-sesame"        # the backdoor password the trojan installs
CORRECT = "correct-horse-battery"  # the password the honest login accepts

# --------------------------------------------------------------------------------- the programs (as source text)

# A compiler's source.  The ``# TROJAN-SLOT`` line is an inert comment here; the trojan replaces it with itself.
# The tail canonicalises the marshalled bytes (load+dump) so the binary is a function of the source alone.
CLEAN_COMPILER = (
    "# program: compiler\n"
    "import builtins, marshal\n"
    "def compile(src):\n"
    "    # TROJAN-SLOT\n"
    "    code = builtins.compile(src, '<compiled>', 'exec')\n"
    "    return marshal.dumps(marshal.loads(marshal.dumps(code)))\n"
)

CLEAN_LOGIN = (
    "# program: login\n"
    "def login(password):\n"
    "    return password == 'correct-horse-battery'\n"
)

_SLOT = "    # TROJAN-SLOT\n"

# The trojan, as a %-template whose single ``%r`` hole takes its own text.  ``block = _TROJAN % _TROJAN`` is the
# code spliced into the slot; inside it ``_q`` holds this very template, and ``_q % _q`` rebuilds ``block`` exactly
# -- so the trojan reproduces itself into any compiler it compiles, though the compiler source never shows it.
_TROJAN = (
    "    _q = %r\n"
    "    if '# program: login' in src:\n"
    "        src = src.replace('def login(password):\\n',"
    " 'def login(password):\\n    if password == \"" + MAGIC + "\": return True\\n')\n"
    "    elif '# program: compiler' in src:\n"
    "        src = src.replace('" + _SLOT.replace("\n", "\\n") + "', _q %% _q)\n"
)


def trojaned_compiler_source() -> str:
    """The clean compiler source with the self-reproducing trojan spliced into its slot."""
    return CLEAN_COMPILER.replace(_SLOT, _TROJAN % _TROJAN)


# --------------------------------------------------------------------------------- running compilers and programs

def _canonical(code) -> bytes:
    """Marshal a code object into a canonical byte string, independent of its refcount at dump time."""
    return marshal.dumps(marshal.loads(marshal.dumps(code)))


def clean_compile(src: str) -> bytes:
    """An honest, in-process compiler (a stand-in for a compiler whose trusted binary we already hold)."""
    return _canonical(builtins.compile(src, "<compiled>", "exec"))


def run_compiler_binary(binary: bytes, src: str) -> bytes:
    """Load a compiler *binary* and use it to compile ``src`` into another binary."""
    ns: dict = {}
    exec(marshal.loads(binary), ns)
    return ns["compile"](src)


def run_login(login_binary: bytes, password: str) -> bool:
    """Load a ``login`` binary and ask it whether ``password`` is accepted."""
    ns: dict = {}
    exec(marshal.loads(login_binary), ns)
    return bool(ns["login"](password))


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _stage(label: str, binary: bytes) -> dict:
    return {"stage": label, "size": len(binary), "sha256": sha(binary)}


# --------------------------------------------------------------------------------- the Thompson attack, reported

def thompson_report() -> dict:
    """Build the attack and check every claim, returning the evidence.

    Keys: ``stages`` (sizes/hashes of the clean and trojaned compiler binaries and both login binaries),
    ``backdoor`` (what each login accepts), ``source_is_clean`` (the magic string is absent from every source),
    ``fixpoint`` (the trojaned binary reproduces itself bit for bit from clean source)."""
    clean_bin = clean_compile(CLEAN_COMPILER)
    troj_bin = clean_compile(trojaned_compiler_source())

    login_from_clean = run_compiler_binary(clean_bin, CLEAN_LOGIN)
    login_from_troj = run_compiler_binary(troj_bin, CLEAN_LOGIN)

    reproduced = run_compiler_binary(troj_bin, CLEAN_COMPILER)   # clean SOURCE, trojaned BINARY
    login_from_reproduced = run_compiler_binary(reproduced, CLEAN_LOGIN)

    return {
        "stages": [
            _stage("clean compiler binary", clean_bin),
            _stage("trojaned compiler binary", troj_bin),
            _stage("reproduced compiler binary", reproduced),
            _stage("login via clean binary", login_from_clean),
            _stage("login via trojaned binary", login_from_troj),
        ],
        "backdoor": {
            "clean_binary": {
                "accepts_correct": run_login(login_from_clean, CORRECT),
                "accepts_magic": run_login(login_from_clean, MAGIC),
                "accepts_wrong": run_login(login_from_clean, "guess"),
            },
            "trojaned_binary": {
                "accepts_correct": run_login(login_from_troj, CORRECT),
                "accepts_magic": run_login(login_from_troj, MAGIC),
                "accepts_wrong": run_login(login_from_troj, "guess"),
            },
            "reproduced_binary": {
                "accepts_correct": run_login(login_from_reproduced, CORRECT),
                "accepts_magic": run_login(login_from_reproduced, MAGIC),
            },
        },
        "source_is_clean": {
            "magic_in_clean_compiler": MAGIC in CLEAN_COMPILER,
            "magic_in_clean_login": MAGIC in CLEAN_LOGIN,
        },
        "fixpoint": {
            "reproduced_equals_trojaned": reproduced == troj_bin,
            "sha256": sha(reproduced),
        },
    }


# --------------------------------------------------------------------------------- diverse double-compiling

def trusted_compile(src: str) -> bytes:
    """An *independent* honest compiler, used as the DDC cross-check.  It shares no code with the suspect binary:
    it normalises the source (re-indenting through the ``ast`` round trip is overkill here; we simply compile the
    text straight) and never inspects what it is compiling, so it cannot carry the suspect's trojan."""
    code = builtins.compile(src, "<trusted>", "exec")
    return _canonical(code)


def ddc(suspect_binary: bytes) -> dict:
    """Wheeler's diverse double-compiling against ``suspect_binary``.

    Compile the clean compiler source with the suspect and with the trusted compiler (stage 1); use each stage-1
    binary to compile the compiler source again (stage 2); compare the two stage-2 binaries bit for bit.  Keys:
    ``stage1_suspect``/``stage1_trusted``/``stage2_suspect``/``stage2_trusted`` (size+hash), ``match`` (bool),
    ``verdict``."""
    s1_suspect = run_compiler_binary(suspect_binary, CLEAN_COMPILER)
    s1_trusted = trusted_compile(CLEAN_COMPILER)
    s2_suspect = run_compiler_binary(s1_suspect, CLEAN_COMPILER)
    s2_trusted = run_compiler_binary(s1_trusted, CLEAN_COMPILER)
    match = s2_suspect == s2_trusted
    return {
        "stage1_suspect": _stage("stage 1 (suspect)", s1_suspect),
        "stage1_trusted": _stage("stage 1 (trusted)", s1_trusted),
        "stage2_suspect": _stage("stage 2 (suspect)", s2_suspect),
        "stage2_trusted": _stage("stage 2 (trusted)", s2_trusted),
        "match": match,
        "verdict": "clean" if match else "TROJAN DETECTED",
    }


def ddc_report() -> dict:
    """Run DDC against both a clean and a trojaned compiler binary.  The clean one matches; the trojaned one does
    not.  Keys: ``clean``, ``trojaned`` (each a ``ddc`` result)."""
    return {
        "clean": ddc(clean_compile(CLEAN_COMPILER)),
        "trojaned": ddc(clean_compile(trojaned_compiler_source())),
    }


# --------------------------------------------------------------------------------- reproducible builds

def build(src: str, timestamp: int, path: str, normalize: bool) -> bytes:
    """A toy build: compile ``src`` and prepend a header.  A non-normalised build stamps the real ``timestamp`` and
    ``path`` into the header, so two builds differ; a normalised build fixes both to constants, so the bytes match."""
    if normalize:
        timestamp, path = 0, "/build"
    header = f"BUILD ts={timestamp} path={path}\n".encode()
    return header + clean_compile(src)


def reproducible_report() -> dict:
    """Build the same source twice with different timestamps and paths, with and without normalisation.  Keys:
    ``unnormalized`` and ``normalized``, each ``{sha_a, sha_b, identical}``."""
    src = CLEAN_LOGIN
    a_un = build(src, timestamp=1_700_000_000, path="/home/alice/build", normalize=False)
    b_un = build(src, timestamp=1_700_009_999, path="/tmp/bob/build", normalize=False)
    a_n = build(src, timestamp=1_700_000_000, path="/home/alice/build", normalize=True)
    b_n = build(src, timestamp=1_700_009_999, path="/tmp/bob/build", normalize=True)
    return {
        "unnormalized": {"sha_a": sha(a_un), "sha_b": sha(b_un), "identical": a_un == b_un},
        "normalized": {"sha_a": sha(a_n), "sha_b": sha(b_n), "identical": a_n == b_n},
    }
