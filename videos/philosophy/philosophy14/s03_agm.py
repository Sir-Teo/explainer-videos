from __future__ import annotations

from videos.philosophy.philosophy14.common import *  # noqa: F403

CARDS = [
    ("K*1", "closure", r"K * A = \mathrm{Cn}(K * A)", r"the result is a belief set"),
    ("K*2", "success", r"A \in K * A", r"the news is believed"),
    ("K*3", "inclusion", r"K * A \subseteq K + A", r"nothing gratuitous is added"),
    ("K*4", "vacuity", r"\lnot A \notin K \Rightarrow K + A \subseteq K * A", r"no conflict, \ no loss"),
    ("K*5", "consistency", r"K * A \text{ consistent if } A \text{ is}", r"never revise into contradiction"),
    ("K*6", "extensionality", r"A \equiv B \Rightarrow K * A = K * B", r"only content matters"),
    ("K*7", "superexpansion", r"K * (A \land B) \subseteq (K * A) + B", r"revising by more is no bolder"),
    ("K*8", "subexpansion", r"\lnot B \notin K * A \Rightarrow (K * A) + B \subseteq K * (A \land B)",
     r"and no timider"),
]


class AGM(VoiceoverScene):
    def construct(self):
        card = chapter_card(2, r"The AGM postulates", r"What must any rational revision do?", lit=(1985,), part=PART)
        with self.voiceover("Chapter two. The AGM postulates."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.origins()
        self.cards()
        self.contraction_cards()
        self.table()
        self.satoh()

    def origins(self):
        hc = history_card(1985, r"Alchourrón, \ Gärdenfors \ and Makinson", r"`On the Logic of Theory Change'",
                          width=6.6, color=HIST).to_corner(UL, buff=0.35)
        rows = stack([
            (r"Carlos Alchourrón: \ what happens to a legal code when a law is repealed?", WHITE),
            (r"Peter Gärdenfors: \ how belief should change, \ and what conditionals mean", WHITE),
            (r"David Makinson: \ the logician who made the two one theory", WHITE),
            (r"the method: \ do not define \textit{the} revision; \ state the constraints \textit{any} must meet", GOAL),
            (r"and a guiding idea: \ minimal change, \ informational economy", NEW),
        ], font_size=24, buff=0.32, width=12.4, aligned_edge=LEFT).next_to(hc, DOWN, buff=0.5).set_x(0)
        with self.voiceover(
            "The theory of belief change has three founders. <bookmark mark='a'/>Carlos Alchourrón, a legal "
            "philosopher, asked what becomes of a legal code when a law is repealed: which of its consequences survive? "
            "<bookmark mark='b'/>Peter Gärdenfors asked how rational belief should change, and what conditionals mean. "
            "<bookmark mark='c'/>And David Makinson, a logician, saw that these were one problem. Their 1985 paper "
            "gives the theory its name, AGM. <bookmark mark='d'/>Its method is the one this series keeps meeting: do "
            "not define the one true revision; state the constraints that any rational revision must meet, and see "
            "what satisfies them. <bookmark mark='e'/>The guiding idea is minimal change: when you must give something "
            "up, give up as little as you can."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def cards(self):
        head = label(r"Eight postulates for revision", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        cards = VGroup()
        for key, name, form, gloss in CARDS:
            box = RoundedRectangle(width=6.3, height=1.25, corner_radius=0.15, color=NEW if key in ("K*7", "K*8")
                                   else BEL, stroke_width=2.5, fill_color="#0E1621", fill_opacity=1)
            k = label(rf"{key} \ \ {name}", font_size=21, color=NEW if key in ("K*7", "K*8") else BEL)
            f = MathTex(form, font_size=26)
            if f.width > 5.9:
                f.width = 5.9
            g = label(gloss, font_size=18, color=GREY_A)
            inner = VGroup(k, f, g).arrange(DOWN, buff=0.08)
            inner.move_to(box)
            cards.add(VGroup(box, inner))
        cards.arrange_in_grid(rows=4, cols=2, buff=(0.3, 0.18)).next_to(head, DOWN, buff=0.25)
        foot = label(r"K*1--K*6: \ the basic postulates; \ \ K*7, K*8: \ revising by a conjunction", font_size=21,
                     color=GREY_A).to_edge(DOWN, buff=0.15)
        with self.voiceover(
            "The eight postulates for revision. <bookmark mark='a'/>Closure: the result is a belief set, closed under "
            "logic. <bookmark mark='b'/>Success: the new information is believed. <bookmark mark='c'/>Inclusion: "
            "revising adds nothing beyond what plain expansion would. <bookmark mark='d'/>Vacuity: if the news doesn't "
            "conflict with what you believe, nothing is lost; revision is just expansion. "
            "<bookmark mark='e'/>Consistency: unless the news is itself contradictory, the result is consistent. "
            "<bookmark mark='f'/>Extensionality: logically equivalent news gives the same result. "
            "<bookmark mark='g'/>The last two govern conjunctions. Superexpansion: revising by A and B is no bolder "
            "than revising by A and then adding B. <bookmark mark='h'/>Subexpansion: and, if B is consistent with the "
            "revision by A, no more timid either. <bookmark mark='i'/>The first six are the basic postulates; the "
            "last two tie revisions by different inputs together."
        ) as vo:
            self.play(FadeIn(head))
            for mk, c in zip("abcdefgh", cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
            vo.wait_until("i")
            self.play(FadeIn(foot))
        self.clear_scene()

    def contraction_cards(self):
        head = label(r"And six for contraction", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        items = [(r"K$\div$1 \ closure", r"K \div A = \mathrm{Cn}(K \div A)"),
                 (r"K$\div$2 \ inclusion", r"K \div A \subseteq K"),
                 (r"K$\div$3 \ vacuity", r"A \notin K \Rightarrow K \div A = K"),
                 (r"K$\div$4 \ success", r"\nvDash A \Rightarrow A \notin K \div A"),
                 (r"K$\div$5 \ recovery", r"K \subseteq (K \div A) + A"),
                 (r"K$\div$6 \ extensionality", r"A \equiv B \Rightarrow K \div A = K \div B")]
        cards = VGroup()
        for name, form in items:
            col = NEW if "recovery" in name else BEL
            box = RoundedRectangle(width=6.0, height=1.0, corner_radius=0.15, color=col, stroke_width=2.5,
                                   fill_color="#0E1621", fill_opacity=1)
            inner = VGroup(label(name, font_size=21, color=col), MathTex(form, font_size=26)).arrange(DOWN, buff=0.1)
            inner.move_to(box)
            cards.add(VGroup(box, inner))
        cards.arrange_in_grid(rows=3, cols=2, buff=(0.4, 0.25)).next_to(head, DOWN, buff=0.4)
        foot = label(r"recovery, \ highlighted, \ is the contested one \ (Chapter 1)", font_size=22,
                     color=GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Contraction has its own postulates. <bookmark mark='a'/>The result is a belief set; it contains nothing new; "
            "if you didn't believe A, nothing changes; and unless A is a logical truth, you really do stop believing "
            "it. <bookmark mark='b'/>Recovery, the contested one from the first chapter: contracting and then adding "
            "back loses nothing. And extensionality. <bookmark mark='c'/>Through the Levi and Harper identities, which "
            "we meet in the next chapter, these six correspond exactly to the basic six for revision."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c) for c in cards[:4]], lag_ratio=0.3), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(cards[4]), FadeIn(cards[5]))
            vo.wait_until("c")
            self.play(FadeIn(foot), Indicate(cards[4], color=NEW, scale_factor=1.03))
        self.clear_scene()

    def table(self):
        d = load("agm")
        head = label(r"The Reasoner checks four operators", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        sub = label(r"three atoms, \ eight worlds; \ every pair of propositions $A$, $B$ \ ($255^2$ cases)",
                    font_size=22, color=GREY_A).next_to(head, DOWN, buff=0.2)
        keys = [k for k, _, _ in d["postulates"]]
        hd = [label(r"operator", font_size=21, color=P.CLAIM)] + [label(k, font_size=21, color=P.CLAIM) for k in keys]
        names = list(d["table"])
        rows = [[label(n, font_size=21)] + [mark(d["table"][n][k], 26) for k in keys] for n in names]
        grid = ValueGrid(hd, rows, col_w=[4.2] + [1.2] * len(keys), cell_h=0.62, font_size=21).next_to(sub, DOWN,
                                                                                                    buff=0.4)
        notes = stack([
            (r"spheres and Dalal's distance revision: \ all eight", OK),
            (r"Satoh's minimal \textit{sets} of changes: \ fails subexpansion", BAD),
            (r"Winslett's update: \ fails it too, \ and fails vacuity when you believe more than one world", BAD),
            (r"K*1 and K*6 hold automatically when beliefs are sets of worlds", GREY_A),
        ], font_size=22, width=12.4).next_to(grid, DOWN, buff=0.4)
        with self.voiceover(
            "Which ways of revising pass? <bookmark mark='a'/>The Reasoner takes three atoms, eight worlds, and checks "
            "every postulate against every pair of propositions. <bookmark mark='b'/>Four operators. Revision by "
            "spheres, which we meet in the next chapter. Mukesh Dalal's revision, which keeps the worlds at the "
            "smallest number of changed atoms. Ken Satoh's, which keeps the worlds whose set of changed atoms is "
            "minimal under inclusion. And Marianne Winslett's update. <bookmark mark='c'/>Spheres and Dalal pass all "
            "eight. <bookmark mark='d'/>Satoh's fails subexpansion. <bookmark mark='e'/>So does Winslett's update; and, "
            "as the book and the magazine showed, it fails vacuity once you believe more than one world. "
            "<bookmark mark='f'/>Closure and extensionality hold automatically when beliefs are sets of worlds."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(sub))
            vo.wait_until("b")
            self.play(FadeIn(grid.head), Create(grid.rule))
            for r in range(len(names)):
                self.play(FadeIn(grid.cell[r][0]), run_time=0.5)
            vo.wait_until("c")
            self.play(*[FadeIn(m) for r in (0, 1) for m in grid.cell[r][1:]], FadeIn(notes[0]))
            vo.wait_until("d")
            self.play(*[FadeIn(m) for m in grid.cell[2][1:]], FadeIn(notes[1]))
            vo.wait_until("e")
            self.play(*[FadeIn(m) for m in grid.cell[3][1:]], FadeIn(notes[2]))
            vo.wait_until("f")
            self.play(FadeIn(notes[3]))
        self.clear_scene()

    def satoh(self):
        d = load("agm")["satoh"]
        head = label(r"Where Satoh's revision goes wrong", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        K = MathTex(r"K = \{" + wtex(d["K"][0]) + r"\}", font_size=32, color=BEL)
        A = MathTex(r"A = \{" + r",\ ".join(wtex(w) for w in d["A"]) + r"\}", font_size=30, color=NEW)
        B = MathTex(r"B = \{" + r",\ ".join(wtex(w) for w in d["B"]) + r"\}", font_size=30, color=NEW)
        top = VGroup(K, A, B).arrange(DOWN, buff=0.2).next_to(head, DOWN, buff=0.35)
        changes = stack([
            (r"from $pqr$: \ \ $pq\bar r$ changes $\{r\}$, \ \ $p\bar q r$ changes $\{q\}$, \ \ $\bar p q \bar r$ "
             r"changes $\{p, r\}$", WHITE),
            (r"$K * A$: \ $\{r\}$ and $\{q\}$ are minimal: \ $\{pq\bar r,\ p\bar q r\}$", BEL),
            (r"$(K * A) + B = \{p\bar q r\}$", BEL),
            (r"$K * (A \land B)$: \ $\{q\}$ and $\{p, r\}$ are \textit{incomparable}: \ both kept", BAD),
            (r"so $(K * A) + B \not\subseteq K * (A \land B)$: \ subexpansion fails", BAD),
            (r"counting changes \ (Dalal) \ instead of comparing sets of them \ restores it", OK),
        ], font_size=23, buff=0.26, width=12.4).next_to(top, DOWN, buff=0.4)
        with self.voiceover(
            "Here is the Reasoner's counterexample to Satoh. <bookmark mark='a'/>You believe one world, where p, q and r "
            "are all true. You revise by A, which rules that world out and leaves three. <bookmark mark='b'/>Reaching "
            "them means changing r, or q, or both p and r. <bookmark mark='c'/>The first two changes are minimal, so "
            "revising by A keeps those two worlds. <bookmark mark='d'/>Adding B leaves just one. "
            "<bookmark mark='e'/>But revise by A and B together, and the competitors are changing q, or changing p and "
            "r: neither set includes the other, so both survive. <bookmark mark='f'/>Revising by more has kept more. "
            "Subexpansion fails. <bookmark mark='g'/>Counting the changes, as Dalal does, instead of comparing the sets "
            "of them, restores the postulate. Minimal change needs a measure that compares everything."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(top))
            for mk, r in zip("bcdefg", changes):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
