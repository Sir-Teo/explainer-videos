from __future__ import annotations

from explainer.cs import *  # noqa: F403
from explainer.cs.gates import gate
from videos.cs.cs55.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, load

# The climb, bottom to top: (layer key for the colour, what this series built there).
STATIONS = [("gates", r"a NAND gate, \ from two switches \ (Part 3)"),
            ("arith", r"an adder and a register \ (Parts 4--5)"),
            ("isa", r"Pebble, \ a stored-program computer \ (Part 6)"),
            ("uarch", r"a pipeline, \ out of order, \ caches, \ four cores \ (Parts 7--10)"),
            ("code", r"machine code, \ a loader, \ a stack \ (Part 11)"),
            ("lang", r"the Pebble language and its compiler \ (Parts 12--13)"),
            ("lang", r"a runtime with a garbage collector \ (Part 15)"),
            ("algo", r"counting with a hash table \ (Part 17)"),
            ("os", r"PebbleOS: \ traps, \ processes, \ pages \ (Parts 31--32)"),
            ("data", r"a file system and a database \ (Parts 34--35)"),
            ("net", r"packets, \ routes and TCP \ (Parts 36--37)"),
            ("dist", r"Raft, \ and MapReduce on sixteen Pebbles \ (Parts 38--39)"),
            ("cloud", r"a service on a cluster in the cloud \ (Parts 43--50)"),
            ("apps", r"the Job: \ thirty novels, \ counted")]

# What each layer trusts, and how this series earned that trust: (key, layer, trusts, earned).
HARDWARE = [("physics", r"switches", r"a switch is either on or off",
             r"Shannon's algebra of switches \ (Part 3); \ Part 5's metastability showed where it fails"),
            ("gates", r"gates", r"each gate computes its truth table",
             r"every block checked exhaustively \ (Part 3)"),
            ("arith", r"arithmetic and memory", r"the adder adds; \ a flip-flop keeps its bit",
             r"checked against arithmetic, \ beside a deliberately broken divider \ (Part 4)"),
            ("isa", r"instruction set", r"Pebble does what its manual says",
             r"the gate-level machine and the emulator agree on random programs \ (Part 6)"),
            ("uarch", r"microarchitecture", r"speed changes nothing but the time",
             r"every faster core gave Part 6's answers \ (Parts 7--10); \ but time is visible: \ Spectre")]
SOFTWARE = [("code", r"machine code", r"a call returns where it came from",
             r"Part 11's stack discipline; \ broken in Chapter 2, \ defended by canaries, \ NX and ASLR"),
            ("lang", r"languages", r"the compiler keeps the meaning; \ types rule out bad programs",
             r"differential fuzzing and z3 \ (Part 13); \ type safety \ (Part 14); \ DDC \ (Chapter 12)"),
            ("algo", r"algorithms", r"the code computes what it claims, \ in the time it claims",
             r"invariants and proofs, \ then measurement \ (Parts 16--24)"),
            ("os", r"operating system", r"one process cannot touch another's memory",
             r"the MMU checks every access against the page table \ (Part 32)"),
            ("data", r"storage and data", r"a committed write survives a crash",
             r"crashes injected, \ and recovered from \ (Parts 34--35)")]
MACHINES = [("net", r"networks", r"bytes arrive, \ in order",
             r"TCP tested under loss and reordering \ (Part 37); \ \textit{who} sent them needs Part 30's keys"),
            ("dist", r"distributed systems", r"replicas agree on one log",
             r"Raft under injected faults, \ its invariants checked \ (Part 38)"),
            ("cloud", r"services and the cloud", r"a retried request takes effect once",
             r"idempotency keys, \ double counts measured \ (Part 43); \ isolation \ (Chapter 7)"),
            ("apps", r"applications", r"everything below",
             r"nothing of its own: \ it inherits every reason, \ and every leak")]
# The kind of evidence behind each layer, for the summary
EVIDENCE = {"math": (r"proof", LAM), "physics": (r"an algebra of switches", LAM),
            "gates": (r"exhaustive check", YES), "arith": (r"exhaustive and random checks", YES),
            "isa": (r"agrees with a reference", DATA), "uarch": (r"agrees with a reference", DATA),
            "code": (r"a convention, \ hardened", KERN), "lang": (r"fuzzing, \ proof, \ DDC", DATA),
            "algo": (r"proof, \ then measurement", LAM), "os": (r"hardware checks every access", KERN),
            "data": (r"injected crashes", HEAD), "net": (r"injected loss; \ keys", HEAD),
            "dist": (r"injected faults", HEAD), "cloud": (r"idempotency, \ isolation", KERN),
            "apps": (r"inherited", GREY_B)}
# Leaks this part met, as (from layer, to layer, name)
LEAKS = [("arith", "os", r"\textbf{Rowhammer}: \ memory cells are not independent"),
         ("uarch", "apps", r"\textbf{Spectre}: \ speculation leaves traces"),
         ("lang", "apps", r"\textbf{the trojan}: \ a binary need not match its source"),
         ("net", "cloud", r"\textbf{a BGP hijack}: \ announcements are believed")]
ALL = tuple(k for k, _ in LAYERS) + ("limits", "practice")


def lit_tower(lit=ALL, **kw):
    """The series' tower, with the practice column moved right so the limits column's name fits beside its bar."""
    tw = tower(lit=lit, **kw)
    tw.column["practice"].shift(RIGHT * 0.3)
    return tw


def station(key, text):
    """One stop on the climb: a NAND symbol for the bottom, a coloured slab for the rest."""
    col = LAYER_COLOR[key]
    r = RoundedRectangle(width=7.4, height=0.62, corner_radius=0.08, stroke_color=col, stroke_width=2,
                         fill_color=col, fill_opacity=0.14)
    t = label(text, font_size=20, color=WHITE)
    if t.width > 7.1:
        t.width = 7.1
    t.move_to(r)
    g = VGroup(r, t)
    if text.startswith(r"a NAND"):
        sym = gate("NAND", size=0.5)
        sym.next_to(r, RIGHT, buff=0.3)
        g.add(sym)
    return g


def trust_row(key, name, trusts, earned, width=8.0):
    col = LAYER_COLOR[key]
    mark = Square(0.22, stroke_width=0, fill_color=col, fill_opacity=0.9)
    head = VGroup(mark, label(name, font_size=22, color=col)).arrange(RIGHT, buff=0.15)
    tr = wrapped_label(r"trusts: \ " + trusts, width, font_size=20, color=WHITE)
    er = wrapped_label(r"earned: \ " + earned, width, font_size=20, color=YES)
    body = VGroup(tr, er).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
    body.next_to(head, DOWN, buff=0.06, aligned_edge=LEFT).shift(RIGHT * 0.37)
    return VGroup(head, body)


class Tower(VoiceoverScene):
    def construct(self):
        self.card()
        self.rise()
        self.hardware()
        self.software()
        self.machines()
        self.evidence()
        self.lit()

    def card(self):
        card = chapter_card(13, r"The tower, end to end", r"What does each layer trust, \ and why?",
                            lit=(1937, 1984), part=PART)
        with self.voiceover("Chapter thirteen. The tower, end to end."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def rise(self):
        nbytes = load("job")["timing"]["bytes"]
        head = label(r"From a NAND gate to the cluster", font_size=36).to_edge(UP, buff=0.3)
        mask = Rectangle(width=15, height=1.7, stroke_width=0, fill_color=self.camera.background_color,
                         fill_opacity=1).move_to([0, 3.45, 0])
        mask.set_z_index(5)
        head.set_z_index(6)
        col = VGroup(*[station(k, t) for k, t in STATIONS]).arrange(UP, buff=0.42)
        col.shift(RIGHT * 0.4 - col[0][0].get_center() + DOWN * 2.6)
        sx = col[0][0].get_left()[0] - 0.15
        spine = Line([sx, col[0][0].get_bottom()[1], 0], [sx, col[-1][0].get_top()[1], 0], color=GREY_D,
                     stroke_width=2)
        climb = VGroup(spine, col)
        job = label(rf"the Job: \ \texttt{{Counter}} over {nbytes:,} bytes of novels", font_size=19,
                    color=HEAD).set_z_index(6)
        job.move_to([0, 2.88, 0])
        total = col[-1][0].get_y() - 1.6
        steps = [0.36 * total, 0.36 * total, 0.28 * total]
        with self.voiceover(
            "Follow the Job one last time, from the bottom. <bookmark mark='a'/> A line of Python counts the words "
            "of thirty novels, about twenty-five million bytes. Beneath it is a NAND gate made of two "
            "switches, then an adder and a register, then Pebble, the computer of Part 6, made fast by pipelines, "
            "caches and cores. <bookmark mark='b'/> On it run machine code, a compiler, a runtime, a hash table, "
            "and PebbleOS with its traps and pages, a file system and a database. <bookmark mark='c'/> Above them, "
            "packets and TCP, Raft and MapReduce, and services on a cluster in the cloud, and at the very top the "
            "Job. Every one of these was built in this series, from the one below it, and each one trusts the one "
            "below to keep its promise."
        ) as vo:
            self.add(mask, head)
            self.play(FadeIn(climb))
            vo.wait_until("a")
            self.play(FadeIn(job), Indicate(col[0], color=HEAD, scale_factor=1.03))
            self.play(climb.animate.shift(DOWN * steps[0]), run_time=4, rate_func=smooth)
            vo.wait_until("b")
            self.play(climb.animate.shift(DOWN * steps[1]), run_time=4, rate_func=smooth)
            vo.wait_until("c")
            self.play(climb.animate.shift(DOWN * steps[2]), run_time=3.5, rate_func=smooth)
            self.play(Indicate(col[-1], color=HEAD, scale_factor=1.03))
        self.wait(0.4)
        self.clear_scene()

    def trust_section(self, title, rows, text, marks):
        head = label(title, font_size=36).to_edge(UP, buff=0.3)
        tw = lit_tower(height=5.7, width=2.9, font_size=16, labels="all").to_edge(LEFT, buff=0.3)
        tw.shift(DOWN * 0.35)
        keys = {k for k, *_ in rows}
        dim = [s for k, s in tw.layer.items() if k not in keys] + list(tw.column.values())
        rws = VGroup(*[trust_row(*r) for r in rows]).arrange(DOWN, aligned_edge=LEFT, buff=0.32)
        if rws.height > 6.1:
            rws.height = 6.1
        rws.next_to(tw, RIGHT, buff=0.45).align_to(tw, UP).shift(UP * 0.2)
        if rws.get_right()[0] > 6.9:
            rws.shift(LEFT * (rws.get_right()[0] - 6.9))
        with self.voiceover(text) as vo:
            self.play(FadeIn(head), FadeIn(tw))
            self.play(*[m.animate.set_opacity(0.18) for m in dim])
            for mk, r, (k, *_) in zip(marks, rws, rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=LEFT * 0.1), Indicate(tw.layer[k], color=WHITE, scale_factor=1.06))
        self.wait(0.4)
        self.clear_scene()

    def hardware(self):
        self.trust_section(
            r"What the hardware trusts", HARDWARE,
            "Now ask each layer what it trusts, and how this series earned it. <bookmark mark='a'/> The switch "
            "trusts physics to be on or off; Shannon's algebra made switches into logic, and Part 5's metastability "
            "showed where that fails. <bookmark mark='b'/> Gates trust their truth tables, which we checked "
            "exhaustively. <bookmark mark='c'/> Arithmetic trusts its adders, checked against arithmetic itself. "
            "<bookmark mark='d'/> The instruction set trusts the gates, and the gate-level machine agreed with the "
            "emulator on random programs. <bookmark mark='e'/> And every faster core gave Part 6's answers, which "
            "is all the architecture promised. It never promised anything about time, and Spectre lives there.",
            "abcde")

    def software(self):
        self.trust_section(
            r"What the software trusts", SOFTWARE,
            "<bookmark mark='a'/> Machine code trusts that a call returns where it came from; Chapter 2 broke that, "
            "and canaries, non-executable memory and randomised layouts defend it. <bookmark mark='b'/> Languages "
            "trust the compiler to keep the meaning: we fuzzed ours differentially without a mismatch, proved "
            "rewrite rules with z3, and, in this part, checked a compiler against an independent one. <bookmark mark='c'/> "
            "Algorithms rest on invariants and proofs, then measurement. <bookmark mark='d'/> The kernel's "
            "isolation rests on the memory unit checking every access. <bookmark mark='e'/> And storage promises "
            "that a committed write survives a crash, which we tested by crashing it.",
            "abcde")

    def machines(self):
        self.trust_section(
            r"What the machines trust", MACHINES,
            "<bookmark mark='a'/> The network promises bytes in order, and TCP kept that promise under loss and "
            "reordering; but who sent the bytes needs the keys of Part 30. <bookmark mark='b'/> Replicas trust "
            "Raft to agree, which we checked by injecting failures. <bookmark mark='c'/> Services trust that a "
            "retry takes effect once, which idempotency keys made true. <bookmark mark='d'/> And the application "
            "at the top earns nothing of its own. It inherits every reason below it, and every leak.",
            "abcd")

    def evidence(self):
        head = label(r"Reasons, \ and leaks", font_size=36).to_edge(UP, buff=0.3)
        tw = lit_tower(height=5.9, width=2.9, font_size=16, labels="all").move_to([0.2, -0.4, 0])
        badges = VGroup()
        x_left = tw.get_right()[0] + 0.35
        for k, _ in LAYERS:
            t, c = EVIDENCE[k]
            b = label(t, font_size=17, color=c).next_to(tw.layer[k][0], RIGHT)
            b.set_x(x_left + b.width / 2)
            badges.add(b)
        bl = label(r"the evidence", font_size=19, color=GREY_A).next_to(badges, UP, buff=0.2).align_to(badges, LEFT)
        arcs, names, marks = VGroup(), VGroup(), VGroup()
        for i, ((a, b, n), ang) in enumerate(zip(LEAKS, (-0.8 * PI, -0.95 * PI, -0.55 * PI, -0.8 * PI)), start=1):
            p, q = tw.layer[a][0].get_left(), tw.layer[b][0].get_left()
            arc = ArcBetweenPoints(p + LEFT * 0.04, q + LEFT * 0.04, angle=ang, color=NO, stroke_width=3)
            arc.add_tip(tip_length=0.16)
            far = arc.point_from_proportion(0.5)
            m = VGroup(Circle(radius=0.17, stroke_color=NO, stroke_width=2, fill_color=BG, fill_opacity=1),
                       label(str(i), font_size=17, color=NO)).move_to(far)
            m[1].move_to(m[0])
            nm = VGroup(label(str(i), font_size=18, color=NO),
                        wrapped_label(n, 2.9, font_size=18, color=NO)).arrange(RIGHT, buff=0.15, aligned_edge=UP)
            arcs.add(arc)
            marks.add(m)
            names.add(nm)
        names.arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(LEFT, buff=0.3).align_to(tw, UP).shift(DOWN * 0.4)
        ll = label(r"what leaked through", font_size=19, color=NO).next_to(names, UP, buff=0.2).align_to(names, LEFT)
        with self.voiceover(
            "Put the reasons side by side, and there are only a few kinds. <bookmark mark='a'/> Proof, for the "
            "mathematics and the algorithms. Exhaustive checks, for the gates. Agreement with an independent "
            "reference, for the processor and the compiler, the same idea as Wheeler's. Injected failures, for "
            "storage, networks and replicas. And hardware that checks every access. <bookmark mark='b'/> The leaks "
            "of this part are the places where a layer relied on a promise nobody had checked: that memory cells "
            "are independent, that speculation leaves no trace, that a binary matches its source, that a route "
            "announcement is honest. Each one crosses the boundary that was supposed to hide it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tw))
            vo.wait_until("a")
            self.play(FadeIn(bl), LaggedStart(*[FadeIn(b, shift=LEFT * 0.1) for b in badges], lag_ratio=0.12),
                      run_time=4)
            vo.wait_until("b")
            self.play(FadeIn(ll))
            for arc, m, nm in zip(arcs, marks, names):
                self.play(Create(arc), FadeIn(m), FadeIn(nm), run_time=1.2)
        self.wait(0.4)
        self.clear_scene()

    def lit(self):
        dark = lit_tower(lit=(), height=6.1, width=4.6, font_size=18, labels="all").move_to([-2.6, -0.3, 0])
        bright = lit_tower(height=6.1, width=4.6, font_size=18, labels="all").move_to(dark)
        notes = VGroup(
            wrapped_label(r"each layer hides the one below, \ and trusts it", 4.6, font_size=21, color=WHITE),
            wrapped_label(r"each trust was earned by a reason: \ a proof, \ a check, \ an independent reference, \ "
                          r"an injected fault, \ a key", 4.6, font_size=21, color=YES),
            wrapped_label(r"where a reason was missing, \ this part found an attack", 4.6, font_size=21,
                          color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([4.2, 0.0, 0])
        with self.voiceover(
            "So here is the tower, lit from end to end. <bookmark mark='a'/> Every layer hides the one below it, "
            "and trusts it. <bookmark mark='b'/> Where that trust was earned, by a proof, a check, an independent "
            "reference, an injected fault or a key, the layer held. <bookmark mark='c'/> Where it was only assumed, "
            "this part found an attack. That is what trusting trust means in the end: not faith in any one layer, "
            "but a reason for each."
        ) as vo:
            self.play(FadeIn(dark))
            self.play(LaggedStart(*[ReplacementTransform(dark.layer[k], bright.layer[k]) for k, _ in LAYERS],
                                  lag_ratio=0.15),
                      ReplacementTransform(dark.column["limits"], bright.column["limits"]),
                      ReplacementTransform(dark.column["practice"], bright.column["practice"]), run_time=4)
            vo.wait_until("a")
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
        self.wait(0.6)
        self.clear_scene()


_ = (BG, DATA, HEAD, KERN, LAM, NO, YES)
