"""Lab 11: count the holes in a first-fit heap against Knuth's rule, then smash Pebble's stack and stop it twice."""

from videos.coursekit import labs

import numpy as np

from explainer.cs.pebble import heap as H
from explainer.cs.pebble import smash
from explainer.cs.pebble.asm import assemble

TITLE = "Holes in the heap, and 81 bytes on the stack"
GOAL = ("Keep N blocks live in Pebble's first-fit heap, free one at random and allocate a new one thousands of times, "
        "and compare the number of holes with Knuth's fifty-percent rule, p N / 2. Then feed the linked greeting "
        "program its 81-byte attack, and run it again with a stack canary and with a no-execute stack.")
TASKS = [
    "Use H.BestFit instead of H.FirstFit. Does p change, and does the hole count still follow p N / 2?",
    "Free the oldest block instead of a random one (live.pop(0)). Which assumption of the rule breaks, and what happens to the holes?",
    "Shorten the attack by one byte and lengthen it by four. Which inputs still print 'pwned', and why?",
]


class Counting(H.FirstFit):
    """First fit that records how each request was met: a hole split, a hole taken whole, or the heap extended."""

    def __init__(self):
        super().__init__()
        self.splits = self.whole = self.grown = 0

    def after_split(self, i):
        self.splits += 1

    def after_take(self, i):
        self.whole += 1

    def malloc(self, n):
        top = self.top
        a = super().malloc(n)
        self.grown += self.top != top
        return a


def churn(n_live, steps, rng):
    heap = Counting()
    live = [heap.malloc(int(s)) for s in rng.integers(16, 2001, n_live)]
    heap.splits = heap.whole = heap.grown = 0
    sizes, picks, holes = rng.integers(16, 2001, steps), rng.random(steps), []
    for k in range(steps):
        heap.free(live.pop(int(picks[k] * len(live))))  # a uniformly chosen live block dies
        live.append(heap.malloc(int(sizes[k])))
        holes.append(len(heap.addrs))
    p = heap.splits / (heap.splits + heap.whole + heap.grown)
    return np.array(holes), p


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()
    traces = {}
    for n_live in (200, 1000):
        holes, p = churn(n_live, 15000, rng)
        mean = holes[5000:].mean()  # after warm-up
        traces[n_live] = (holes, p)
        lab.row(f"N = {n_live} live blocks: holes", f"{mean:.0f} measured   p N / 2 = {p * n_live / 2:.0f}   (p = {p:.2f})")
        assert abs(mean / n_live - p / 2) < 0.03, "Knuth's rule: about p N / 2 holes"

    exe = smash.build()
    attack = smash.exploit(exe)
    benign, owned = smash.run(exe, b"Ada\n"), smash.run(exe, attack)
    nx = smash.run(exe, attack, nx=True)
    guarded = smash.build(canary=True)
    caught = smash.run(guarded, smash.exploit(guarded))
    lab.row("greet, given 'Ada'", repr(benign["output"]))
    lab.row(f"greet, given the {len(attack)}-byte attack", "prints 'pwned'" if "pwned" in owned["output"] else "survives")
    lab.row("the same, with a no-execute stack", nx["fault"] or "no fault")
    lab.row("the same, with a canary", caught["output"].strip().splitlines()[-1])
    assert benign["output"] == "hello, Ada\nbye\n" and "pwned" not in benign["output"]
    assert len(attack) == 81 and owned["output"].endswith("pwned") and "bye" not in owned["output"]
    assert nx["fault"] and "no-execute" in nx["fault"] and "pwned" not in nx["output"]
    assert "stack smashing detected" in caught["output"] and "pwned" not in caught["output"]
    lab.note = ("With random frees, a first-fit heap settles at about p N / 2 holes; the copy that runs 76 bytes "
                "past a buffer's start reaches the saved return address, and each defence stops a different step "
                "of the attack.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    for n_live, color in ((200, labs.BLUE), (1000, labs.GOLD)):
        holes, p = traces[n_live]
        ax[0].plot(holes / n_live, color=color, lw=0.8, label=f"N = {n_live}: holes / N")
        ax[0].axhline(p / 2, color=color, ls="--", lw=1.2, label=f"p / 2 = {p / 2:.2f}")
    ax[0].set(title="First fit under random frees: holes per live block", xlabel="free-and-allocate steps", ylabel="holes / N",
              ylim=(0, 0.6))
    ax[0].legend(ncols=2, loc="lower right")
    code = len(assemble(smash.SHELLCODE).image)  # the injected instructions; the rest is padding
    parts = [("buffer (64 bytes)", 0, 64, labs.BLUE), ("gap", 64, 72, labs.GREY), ("canary slot", 72, 76, labs.GREEN),
             ("saved return address", 76, 80, labs.RED)]
    for name, lo, hi, color in parts:
        ax[1].barh(1, hi - lo, left=lo, color=color, height=0.5, label=name)
    ax[1].barh(0, code, left=0, color=labs.PURPLE, height=0.5, label=f"attack: {code} bytes of code")
    ax[1].barh(0, smash.RA_OFF - code, left=code, color=labs.SAND, height=0.5, label="attack: padding")
    ax[1].barh(0, 4, left=smash.RA_OFF, color=labs.ORANGE, height=0.5, label="attack: the buffer's address")
    ax[1].set(title="greet's 80-byte frame, and the input copied over it", xlabel="byte offset from sp", yticks=[0, 1],
              yticklabels=["input", "frame"], ylim=(-0.6, 3.4), xlim=(0, 80))
    ax[1].legend(ncols=2, loc="upper center")
    lab.fig = fig
    return lab
