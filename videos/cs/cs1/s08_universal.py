from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from explainer.cs.turing import CHAMPIONS, TM
from videos.cs.cs1.common import CODE, COST, CTRL, DATA, HEAD, HIST, PART, YES, fmt, say, live_int, load

LO = [0, -3, 0]  # the windows compute recorded for U's three tapes
FIELD_COLOR = [CTRL, DATA, DATA, GREY_B, CTRL]  # state, read, write, move, next


def color_encoding(view: TapeView, text: str, offset: int = 0):
    """Colour the symbols of <M> on a tape by field (state, read, write, move, next state), separators grey."""
    field = 0
    for i, ch in enumerate(text):
        m = view.syms[i + offset]
        if ch == "|":
            field += 1
            m.set_color(GREY_C)
        elif ch == "#":
            field = 0
            m.set_color(GREY_C)
        elif ch in "^$":
            m.set_color(GREY_C)
        else:
            m.set_color(FIELD_COLOR[field])


class Universal(VoiceoverScene):
    def construct(self):
        self.card()
        self.encode()
        self.machine_u()
        self.run_u()
        self.overhead()
        self.software()

    def card(self):
        card = chapter_card(7, r"The universal machine", r"Can one machine do the work of all of them?", lit=(1936,),
                            part=PART)
        with self.voiceover("Chapter seven. The universal machine."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def encode(self):
        d = load("universal")
        enc = d["encoding"]
        m = TM.parse(CHAMPIONS[2][0])
        zero = [tuple("0" if c == "_" else c for c in r) for r in m.table_text()]  # the busy-beaver convention
        table = RuleTable(zero, font_size=26).move_to(UP * 1.5 + LEFT * 3.2)
        tl = label(r"a machine $M$: \ four rules", font_size=28, color=GREY_A).next_to(table, UP, buff=0.25)
        key = VGroup(*[label(t, font_size=24, color=c) for t, c in (
            (r"states numbered in unary: \ $A = 1$, \ $B = 11$, \ halt $=$ nothing", CTRL),
            (r"symbols $0, 1$; \ moves $L, R$", DATA),
            (r"fields separated by $|$, \ rules by $\#$", GREY_B),
        )]).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to(UP * 1.4 + RIGHT * 3.4)
        view = TapeView(list(enc), head=None, state=None, cell=0.29, font_size=17, ellipsis=False)
        view.move_to(DOWN * 1.3)
        color_encoding(view, enc)
        bl = label(r"$\langle M \rangle$, \ the description of $M$: \ a string like any other", font_size=30,
                   color=CODE).next_to(view, DOWN, buff=0.4)
        rule_spans, k = [], 0
        for part in enc.split("#")[:-1]:
            rule_spans.append((k, k + len(part)))
            k += len(part) + 1
        with self.voiceover(
            "Here is the busy beaver with two states from earlier, as a table: four rules. A Turing machine's table "
            "is finite. So it can be written down as a string of symbols. <bookmark mark='a'/> One way: number the "
            "states in unary, A is one, B is one one, halting is the empty string. Write each rule as its state, the "
            "symbol read, the symbol written, the direction, and the next state, separated by bars, and end each rule "
            "with a hash. <bookmark mark='b'/> The first rule, A reading zero, write one, move right, go to B, becomes "
            "one, bar, zero, bar, one, bar, R, bar, one one, hash. <bookmark mark='c'/> And so on for all four. The whole "
            "machine is now this string. Call it angle-bracket M: the description of M."
        ) as vo:
            self.play(FadeIn(tl), FadeIn(table))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(k_) for k_ in key], lag_ratio=0.3))
            vo.wait_until("b")
            a, b = rule_spans[0]
            self.play(table.light(0), FadeIn(VGroup(*view.cells[a:b + 1], *view.syms[a:b + 1]), lag_ratio=0.1),
                      run_time=1.6)
            vo.wait_until("c")
            for r in range(1, 4):
                a, b = rule_spans[r]
                self.play(table.light(r), FadeIn(VGroup(*view.cells[a:b + 1], *view.syms[a:b + 1]), lag_ratio=0.1),
                          run_time=0.9)
            self.play(table.light(None), FadeIn(bl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def machine_u(self):
        d = load("universal")
        defn = definition_card(r"Universal Turing machine $U$",
                               r"given the description $\langle M \rangle$ of any machine $M$, and an input $w$, \ $U$ does "
                               r"exactly what $M$ does on $w$: \ it halts if and only if $M$ halts, \ and leaves $M$'s "
                               r"output.", color=CODE, width=11.0, font_size=28).move_to(UP * 1.6)
        eq = cmath(r"U(", r"\langle M \rangle", r",\ ", r"w", r")", r"=", r"M(", r"w", r")", font_size=48,
                   colors={r"\langle M \rangle": CODE, r"w": DATA}).next_to(defn, DOWN, buff=0.5)
        hc = history_card(1936, r"Turing, \ \S 6--7", r"constructs a universal machine, \ and uses it to prove his "
                          r"impossibility results", width=5.6, font_size=22).to_corner(DL, buff=0.4)
        ours = VGroup(*[label(t, font_size=26, color=c) for t, c in (
            (r"our $U$ (this series' own): \ three tapes", GREY_A),
            (rf"{d['u_states']} states, \ {d['u_rules']} rules", CTRL),
            (r"tape 1: \ $\langle M \rangle$ \quad tape 2: \ $M$'s tape \quad tape 3: \ $M$'s state", GREY_A),
        )]).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_corner(DR, buff=0.45)
        with self.voiceover(
            "Now the key idea. <bookmark mark='a'/> A universal machine, U, takes two inputs: the description of any "
            "machine M, and an input w. It does exactly what M would do on w. It halts if and only if M halts, and it "
            "leaves the same output. <bookmark mark='b'/> In symbols: U of M and w equals M of w. Turing built one in "
            "the same 1936 paper, and his impossibility proofs depend on it. <bookmark mark='c'/> Here is ours, written "
            f"for this series and tested against every machine it runs: {d['u_states']} states, {d['u_rules']} rules, "
            "and three tapes. The first holds the description. The second is M's tape. The third holds M's current "
            "state, in unary."
        ) as vo:
            self.play(FadeIn(defn, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(Write(eq), FadeIn(hc))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(o, shift=LEFT * 0.15) for o in ours], lag_ratio=0.3))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def views(self, e, enc):
        t1 = TapeView(list(e["tapes"][0]), head=e["heads"][0] - LO[0], state=e["state"], cell=0.3, font_size=18,
                      state_color=CODE)
        color_encoding(t1, e["tapes"][0])
        t2 = TapeView(list(e["tapes"][1]), head=e["heads"][1] - LO[1], state=None, cell=0.6, font_size=28)
        t3 = TapeView(list(e["tapes"][2]), head=e["heads"][2] - LO[2], state=None, cell=0.6, font_size=28)
        for s in t3.syms:
            s.set_color(CTRL)
        t1.move_to(UP * 1.75)
        t2.move_to(DOWN * 0.45 + LEFT * 2.4)
        t3.move_to(DOWN * 2.35 + LEFT * 2.4)
        return VGroup(t1, t2, t3)

    def run_u(self):
        d = load("universal")
        hist, enc = d["history"], d["encoding"]
        writes = set(d["writes"])
        V = self.views(hist[0], enc)
        labs = VGroup(label(r"tape 1: \ $\langle M \rangle$", font_size=24, color=CODE).next_to(V[0], DOWN, buff=0.12),
                      label(r"tape 2: \ $M$'s tape", font_size=24, color=DATA).next_to(V[1], UP, buff=0.15),
                      label(r"tape 3: \ $M$'s state", font_size=24, color=CTRL).next_to(V[2], UP, buff=0.15))
        ucnt = live_int(0, 36, COST)
        mcnt = live_int(0, 36, YES)
        counters = VGroup(VGroup(label(r"$U$'s steps:", font_size=28, color=GREY_A), ucnt).arrange(RIGHT, buff=0.2),
                          VGroup(label(r"$M$'s steps:", font_size=28, color=GREY_A), mcnt).arrange(RIGHT, buff=0.2)
                          ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(RIGHT * 3.9 + DOWN * 1.3)
        for c in counters:
            c[1].add_updater(lambda m, c=c: m.next_to(c[0], RIGHT, buff=0.2))
        phase = label(r"find the rule for $M$'s state", font_size=26, color=CODE).move_to(RIGHT * 3.9 + DOWN * 0.1)
        PH = {"match": r"compare $M$'s state with a rule's", "skip": r"not this rule: \ skip to the next",
              "rewind3": r"not this rule: \ skip to the next", "symbol": r"the state matches; \ the symbol?",
              "write": r"apply the rule: \ write", "move": r"apply the rule: \ move", "erase": r"copy the next state",
              "copy": r"copy the next state", "rewind": r"rewind, \ and go again", "check": r"has $M$ halted?",
              "check2": r"has $M$ halted?", "H": r"$M$ halted, \ so $U$ halts"}
        with self.voiceover(
            "Watch it work. At the start, tape three says M is in state one, A, and M's head on tape two reads a blank. "
            "<bookmark mark='a'/> U walks along the description, comparing each rule's state with tape three, one "
            "stroke at a time. The first rule matches: state A, reading zero. <bookmark mark='b'/> So U applies it to "
            "tape two: write a one, move right. Then it copies the rule's next state, one one, onto tape three, and "
            "rewinds. That was one step of M."
        ) as vo:
            self.play(FadeIn(V), FadeIn(labs), FadeIn(counters), FadeIn(phase))
            nM = 0
            stop = d["writes"][1] + 4
            marks = {d["writes"][0] - 4: "a", d["writes"][0]: "b"}
            for i in range(stop):
                a, b = hist[i], hist[i + 1]
                if i in marks:
                    vo.wait_until(marks[i])
                rt = 0.42 if i < 24 else 0.16
                anims = []
                for k in range(3):
                    new = b["tapes"][k][a["heads"][k] - LO[k]]
                    mv = b["heads"][k] - a["heads"][k]
                    anims.append(V[k].step(new, mv, b["state"] if k == 0 else V[k].state, run_time=rt))
                if a["state"] == "write":
                    nM += 1
                    anims.append(mcnt.tracker.animate(run_time=rt).set_value(nM))
                if b["state"] != a["state"] and b["state"] in PH:
                    anims.append(Transform(phase, label(PH[b["state"]], font_size=26, color=CODE).move_to(phase),
                                           run_time=rt))
                anims.append(ucnt.tracker.animate(run_time=rt).set_value(i + 1))
                self.play(*anims)
                if b["state"] == "erase" and a["state"] == "sep3":
                    pass
        # fast-forward to the end, one simulated step of M at a time
        checkpoints = [w for w in d["writes"][2:]] + [len(hist) - 1]
        with self.voiceover(
            f"Faster now. Every step of M costs U a scan through the description. <bookmark mark='a'/> M takes six "
            f"steps and halts with four ones on its tape. U takes {say(d['u_steps'])} steps to do the same, and halts "
            f"with the same four ones on tape two. A machine that can do what any machine does, given its description."
        ) as vo:
            nM_ = nM
            for c in checkpoints:
                e = hist[c]
                newV = self.views(e, enc)
                if c in writes:
                    nM_ += 1
                self.play(Transform(V, newV), ucnt.tracker.animate.set_value(c),
                          mcnt.tracker.animate.set_value(min(nM_, 6)),
                          Transform(phase, label(PH.get(e["state"], ""), font_size=26, color=CODE).move_to(phase)),
                          run_time=0.9)
            vo.wait_until("a")
            ones = label(r"four $1$s: \ the same as $M$ alone", font_size=26, color=YES).next_to(V[1], RIGHT, buff=0.4)
            self.play(Indicate(V[1], color=YES, scale_factor=1.05), FadeIn(ones))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def overhead(self):
        d = load("universal")
        rows = d["rows"]
        head = label(r"The price of universality", font_size=40).to_edge(UP, buff=0.4)
        hdr = [r"machine $M$", r"$|\langle M \rangle|$", r"$M$'s steps", r"$U$'s steps", r"ratio"]
        tab = VGroup(VGroup(*[label(h, font_size=26, color=GREY_B) for h in hdr]))
        for r in rows:
            tab.add(VGroup(label(rf"busy beaver, \ {r['n']} states", font_size=28),
                           label(rf"${r['len']}$", font_size=30, color=CODE),
                           label(rf"${fmt(r['m_steps'])}$", font_size=30, color=YES),
                           label(rf"${fmt(r['u_steps'])}$", font_size=30, color=COST),
                           label(rf"${r['u_steps'] / r['m_steps']:.0f}\times$", font_size=30, color=GREY_A)))
        xs = [-4.6, -1.6, 0.6, 2.9, 5.2]
        for k, r in enumerate(tab):
            for j, c in enumerate(r):
                c.move_to([xs[j], 1.4 - k * 0.8, 0])
        line = Line([-6.6, 1.0, 0], [6.6, 1.0, 0], color=GREY_D)
        expl = label(r"every simulated step scans the description: \\ the bigger $M$, \ the longer each step takes",
                     font_size=28, color=GREY_A).to_edge(DOWN, buff=0.9)
        with self.voiceover(
            "Universality has a price, and we can measure it. <bookmark mark='a'/> For the two-state busy beaver, U "
            f"runs about {rows[0]['u_steps'] // rows[0]['m_steps']} times slower than M. For three states, about "
            f"{rows[1]['u_steps'] // rows[1]['m_steps']} times. For four, about {rows[2]['u_steps'] // rows[2]['m_steps']}. "
            "<bookmark mark='b'/> Every simulated step scans the description, so the slowdown grows with the size of M. "
            "Real universal machines are built to make that price small, and much of this series is about how: "
            "the stored-program computer in Part 6, and the interpreters, compilers and virtual machines of Parts 13 "
            "to 15."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab[0]), Create(line))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in tab[1:]], lag_ratio=0.4), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(expl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def software(self):
        before = VGroup(label(r"before", font_size=32, color=GREY_B),
                        VGroup(*[node_box(t, c, font_size=24) for t, c in
                                 ((r"a machine \\ for tides", DATA), (r"a machine \\ for logarithms", DATA),
                                  (r"a machine \\ for ciphers", DATA))]).arrange(DOWN, buff=0.25)).arrange(DOWN, buff=0.35)
        after = VGroup(label(r"after", font_size=32, color=GREY_B),
                       node_box(r"one machine", CODE, font_size=30),
                       VGroup(*[node_box(t, CODE, font_size=22) for t in
                                (r"$\langle$tides$\rangle$", r"$\langle$logarithms$\rangle$",
                                 r"$\langle$ciphers$\rangle$", r"$\langle$anything$\rangle$")]).arrange(RIGHT, buff=0.2)
                       ).arrange(DOWN, buff=0.4)
        before.move_to(LEFT * 4.2 + UP * 0.2)
        after.move_to(RIGHT * 2.4 + UP * 0.2)
        arr = Arrow(before.get_right(), after.get_left(), buff=0.3, color=GREY_B, stroke_width=4)
        now = VGroup(*[label(t, font_size=26, color=GREY_A) for t in (
            r"the processor in your phone \ $=$ \ $U$; \ apps \ $=$ \ descriptions",
            r"emulators, \ the Java virtual machine, \ Python's interpreter: \ $U$ in software",
        )]).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "This is the idea that created software. <bookmark mark='a'/> Before it, a new task meant a new machine: one "
            "for tides, one for logarithms, one for ciphers. <bookmark mark='b'/> After it, one machine, and a "
            "description for each task. The description is data: it can be stored, copied, sent, and even computed by "
            "another program. <bookmark mark='c'/> The processor in your phone is a universal machine, and every app is "
            "a description. Emulators, the Java virtual machine and Python's interpreter are universal machines written "
            "in software, running on universal machines made of silicon."
        ) as vo:
            self.play(FadeIn(before[0]), FadeIn(before[1], shift=RIGHT * 0.2))
            vo.wait_until("a")
            self.play(Indicate(before[1], color=DATA, scale_factor=1.02))
            vo.wait_until("b")
            self.play(GrowArrow(arr), FadeIn(after, shift=LEFT * 0.2))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(n) for n in now], lag_ratio=0.4))
        self.wait(0.3)
        self.clear_scene()
