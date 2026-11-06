from __future__ import annotations

from explainer import narration_credit
from explainer.cs import *  # noqa: F403
from videos.cs.cs25.common import (BG, COST, CTRL, DATA, HEAD, LAM, NO, PART, YES, load, mono, wang_grid)


def tile(content, caption, color, TW=3.6, TH=2.3):
    frame = RoundedRectangle(width=TW + 0.3, height=TH + 0.75, corner_radius=0.15, stroke_color=GREY_D,
                             stroke_width=1.5, fill_color=BG, fill_opacity=1)
    if content.width > TW:
        content.scale_to_fit_width(TW)
    if content.height > TH:
        content.scale_to_fit_height(TH)
    content.move_to(frame.get_center() + UP * 0.25)
    cap = label(caption, font_size=22, color=color).move_to(frame.get_bottom() + UP * 0.3)
    return Group(frame, content, cap)


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.payoffs()
        self.practice()
        self.problems()
        self.next_time()
        self.references()

    def recap(self):
        t = load("tiles")
        g8 = next(r for r in t["rects"] if r["n"] == 8)["grid"]
        hat = load("hat")
        hp = Polygon(*[np.array([x, y, 0]) for x, y in hat["P"]], color=HEAD, stroke_width=3).set_fill(HEAD, 0.35)
        tiles = Group(
            tile(MathTex(r"A \le_m B", font_size=50, color=DATA), r"reductions; \ Rice", DATA),
            tile(mono("print(s % s)", 30, LAM), r"quines; \ Kleene", LAM),
            tile(wang_grid(t["tiles"], g8, s=0.26), r"dominoes and tiles", YES),
            tile(MathTex(r"x^2 - 61y^2 = 1", font_size=44, color=CTRL), r"Hilbert's tenth", CTRL),
            tile(MathTex(r"K(x),\ \Omega", font_size=50, color=NO), r"G\"odel; \ Chaitin", NO),
            tile(hp, r"the hat \ (2023)", HEAD),
        ).arrange_in_grid(rows=2, cols=3, buff=(0.35, 0.35)).move_to(DOWN * 0.2)
        head = label(rf"Part {PART}: \ Undecidable", font_size=38).to_edge(UP, buff=0.3)
        with self.voiceover(
            "What we built in this part. Decidable, recognizable and co-recognizable, and reductions that carry "
            "impossibility from one problem to the next. Rice's theorem, which forbids almost every question about "
            "what programs do. Programs that print their own source, in Python and in Pebble. Dominoes, tiles and "
            "Diophantine equations, each hiding a Turing machine, and the hat. Gödel's theorems, proved from "
            "halting; oracles and the arithmetic hierarchy; Kolmogorov complexity and Chaitin's Omega; and the busy "
            "beaver, where proof runs out."
        ):
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t_, shift=UP * 0.15) for t_ in tiles], lag_ratio=0.25), run_time=4.0)
        self.wait(0.5)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"the time hierarchy, \ by the same diagonal", [26]),
            (r"Rice's theorem, \ and verifiers that approximate", [54]),
            (r"safety in access control is undecidable \ (HRU)", [55]),
            (r"the trojan compiler, \ built from a quine", [55]),
            (r"Occam's razor and compression", [57]),
            (r"recursion as a fixed point", [58]),
        ], font_size=23)
        with self.voiceover(
            "Where this comes back. Part 26 proves the time hierarchy theorem with the same diagonal, and asks the "
            "question this part cannot answer: not whether, but how fast. Part 54 proves programs correct, and "
            "escapes Rice's theorem by approximating. Part 55 shows that safety in access control is undecidable, "
            "and builds Ken Thompson's trojan compiler on a quine. Part 57 turns Kolmogorov's idea into Occam's "
            "razor for learning, and Part 58 makes recursion a fixed point, the semantic cousin of Kleene's theorem."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.3), run_time=3.0)
        self.wait(0.5)
        self.clear_scene()

    def practice(self):
        card = practice_card([
            (r"static analysis", r"every analyzer approximates: \ false alarms or missed bugs, \ by Rice"),
            (r"security", r"no perfect malware detector; \ sandboxes and limits instead of prediction"),
            (r"language design", r"type systems and build files that are \textbf{deliberately} not Turing "
                                 r"complete"),
            (r"compilers", r"depth limits on templates and type checking; \ timeouts on optimization"),
            (r"testing", r"tests can show a bug, \ never its absence: \ halting in disguise"),
        ])
        with self.voiceover(
            "In practice. Every static analyzer is an approximation, trading false alarms against missed bugs, "
            "because of Rice. No malware scanner is perfect, so security relies on sandboxes and limits rather than "
            "prediction. Language designers keep configuration files, query languages and some type systems "
            "deliberately less than Turing complete, so their questions stay decidable. Compilers cap template and "
            "type-checking depth. And Dijkstra's remark, that testing can show the presence of bugs but never their "
            "absence, is the halting problem in disguise."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.35), run_time=3.0)
        self.wait(0.3)
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"Prove that $EQ_{TM}$ is neither recognizable nor co-recognizable.",
            r"Use Rice's theorem to show that ``$M$ accepts a palindrome'' is undecidable, \ and explain why ``$M$ has "
            r"a palindrome as its \textit{description}'' is not.",
            r"Prove that a language is decidable iff some machine enumerates it in increasing order.",
            r"Show that $K(x) \le |x| + c$, \ and that $K(x\,x) \le K(x) + c$; \ conclude that at most half of all "
            r"strings of each length have $K(x) < |x| - 1$.",
            r"\textit{Build.} \ A Pebble-language program that prints its own source \textbf{backwards}; \ run it on "
            r"the emulator.",
            r"$\bigstar$ \textit{Research.} \ Is PCP with three dominoes decidable? \ Start with words of length "
            r"$\le 3$: \ find the longest shortest match, \ or prove the lengths are bounded.",
        ], font_size=22)
        with self.voiceover(
            "Six problems, with full solutions in the part's notes. Pause on any of them. The fifth is a build "
            "problem: a program in the Pebble language that prints its own source backwards. The last, marked with a "
            "star, is a research problem: its answer is not known, and the notes say where to start."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r) for r in ps.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(6.0)
        self.clear_scene()

    def next_time(self):
        nxt = label(r"Next: \ Part 26, \ P versus NP", font_size=42).to_edge(UP, buff=0.6)
        items = VGroup(*[label(t, font_size=26, color=c) for t, c in (
            (r"G\"odel's letter of 1956: \ is finding a proof as easy as checking one?", DATA),
            (r"the time hierarchy, \ Savitch, \ and Cook--Levin's tableau", YES),
            (r"Karp's twenty-one problems, \ and why they are one", LAM),
            (r"why fifty years of attacks have failed", HEAD))]).arrange(DOWN, buff=0.35)
        items.move_to(UP * 0.0)
        q = label(r"Act V: \ limits and secrets", font_size=26, color=GREY_A).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "Next time: this part asked what can be computed at all. Part 26 asks what can be computed quickly. In "
            "1956 Gödel wrote to John von Neumann asking whether finding a proof could be as easy as checking one. "
            "Cook and Levin turned that letter into a single problem, Karp found it inside twenty-one others, and "
            "fifty years of attacks have failed. Part 26, P versus NP."
        ):
            self.play(FadeIn(nxt), LaggedStart(*[FadeIn(i) for i in items], lag_ratio=0.3))
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Sipser, \textit{Introduction to the Theory of Computation}, \ ch. 4--6; \ Rogers; \ Soare, "
             r"\textit{Turing Computability}",
             r"Boolos, Burgess and Jeffrey, \textit{Computability and Logic}; \ Li and Vit\'anyi, \textit{An "
             r"Introduction to Kolmogorov Complexity}",
             r"Matiyasevich, \textit{Hilbert's Tenth Problem}; \ Gr\"unbaum and Shephard, \textit{Tilings and "
             r"Patterns}"],
            [r"Post (1946); \ Rice (1953); \ Berger (1966); \ Davis (1973); \ Jones, Sato, Wada and Wiens (1976)",
             r"Chaitin (1975); \ Calude, Dinneen and Shu (2002); \ Aaronson (2020); \ Neary (2015)",
             r"Jeandel and Rao (2015); \ Smith, Myers, Kaplan and Goodman-Strauss (2023); \ Cubitt et al. (2015)",
             r"Koymans and Pagano (2024); \ Alp\"oge, Bhargava, Ho and Shnidman (2025); \ Koenigsmann (2016)"])
        credit = note(rf"narration: \ {narration_credit()}", font_size=18).to_edge(DOWN, buff=0.15)
        with self.voiceover("The books and papers this part follows are on screen and in the notes. Thank you for "
                            "watching."):
            self.play(FadeIn(card), FadeIn(credit))
        self.wait(4.0)
        self.clear_scene()
