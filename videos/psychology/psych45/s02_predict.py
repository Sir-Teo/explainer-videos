from __future__ import annotations

from videos.psychology.psych45.common import *  # noqa: F403

QUESTIONS = [
    (r"1", r"An adaptive test from a bank of 300 items stops when its standard error reaches 0.3. \ About how many "
           r"items does it give?", PERSON),
    (r"2", r"How many items does the best fixed form need to be as accurate?", MODEL),
    (r"3", r"Five law-school admission items, \ 1{,}000 people: \ does each item need its own discrimination, \ or "
           r"is the Rasch model enough?", SYMP),
    (r"4", r"Two groups differ in ability by 0.8 SD. \ On a perfectly fair item, \ by how much do their proportions "
           r"correct differ?", GOOD),
]


class Predict(VoiceoverScene):
    def construct(self):
        self.card()
        self.adaptive()
        self.quiz()

    def card(self):
        card = chapter_card(1, r"On you: \ an adaptive test, \ and four numbers", r"How sure can ten questions make "
                            r"us?", lit=(), part=PART, scale=("person",), marr=("what",))
        with self.voiceover("Chapter one. On you: an adaptive test, and four numbers."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def adaptive(self):
        d = load("cat")
        stage = demo_stage(13.2, 6.0, center=[0, -0.3, 0])
        n = len(d["ex_items"])
        A = axes([0, n + 1], [-3, 3], x_length=8.0, y_length=4.2, xticks=list(range(0, n + 1, 4)), yticks=[-2, 0, 2],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:g}", xlabel=r"question", ylabel=r"ability",
                 center=[-2.0, -0.4, 0], font_size=14)
        path, ses = d["ex_path"], d["ex_ses"]
        band = VGroup(*[Line(A.ax.c2p(k, path[k] - 1.96 * ses[k]), A.ax.c2p(k, path[k] + 1.96 * ses[k]), color=MODEL,
                             stroke_width=5, stroke_opacity=0.5) for k in range(len(path))])
        est = VGroup(*[Dot(A.ax.c2p(k, path[k]), radius=0.06, color=MODEL) for k in range(len(path))])
        items = VGroup()
        for k, (j, r) in enumerate(zip(d["ex_items"], d["ex_resp"])):
            items.add(label(r"$\checkmark$" if r else r"$\times$", font_size=18, color=GOOD if r else AUTH).move_to(
                A.ax.c2p(k + 1, float(np.clip(d["b"][int(j)], -2.9, 2.9)))))
        truth = DashedLine(A.ax.c2p(0, d["ex_true"]), A.ax.c2p(n + 1, d["ex_true"]), color=YOU, stroke_width=2)
        t_l = VGroup(DashedLine(ORIGIN, RIGHT * 0.5, color=YOU, stroke_width=2),
                     label(r"Psyche's true ability", font_size=13, color=YOU)).arrange(RIGHT, buff=0.12)
        t_l.next_to(A.ax.c2p(n + 1, 3.0), UP, buff=0.12, aligned_edge=RIGHT)
        rows = rows_of([
            (r"each question is chosen to be most informative at the current estimate: \ near 50:50 for this person",
             WHITE),
            (r"right answers (green) bring harder items, \ wrong ones easier; \ the marks sit at each item's difficulty",
             GOOD),
            (rf"the 95\% band narrows; \ it stops after {n} questions, \ when the standard error falls below 0.3", MODEL),
            (r"on the course site: \ a short adaptive test on you, \ unscored and stored nowhere", YOU),
        ], 3.8, 17, 0.32).move_to([4.4, -0.3, 0])
        tag = psyche_tag(r"\texttt{irt.cat}, \ a simulated bank of 300 items")
        with self.voiceover(
            "First, watch an adaptive test at work. Psyche takes it, with a true ability of one point three. "
            "<bookmark mark='a'/> Each question is chosen to be the most informative at the current estimate: one this "
            "person has about an even chance of getting right. <bookmark mark='b'/> Right answers bring harder items, "
            "wrong ones easier. Each mark sits at that item's difficulty. <bookmark mark='c'/> The band around the "
            "estimate narrows with every answer, and the test stops when the standard error falls below zero point "
            "three. <bookmark mark='d'/> On the course site you can take a short adaptive test yourself. It isn't "
            "scored, and nothing is stored."
        ) as vo:
            self.play(FadeIn(stage), FadeIn(A), FadeIn(truth), FadeIn(t_l), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(est[0]), FadeIn(band[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), LaggedStart(*[AnimationGroup(FadeIn(items[k]), FadeIn(est[k + 1]),
                                                                    FadeIn(band[k + 1])) for k in range(n)],
                                                   lag_ratio=0.5), run_time=6.0)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.wait(1.0)
        self.clear_scene()

    def quiz(self):
        stage = demo_stage(13.2, 6.0, center=[0, -0.3, 0])
        rows = VGroup()
        for n, q, c in QUESTIONS:
            rows.add(VGroup(label(n, font_size=34, color=c), wrapped_label(q, 9.4, 22, WHITE),
                            label(r"\underline{\hspace{1.2cm}}", font_size=26, color=YOU)).arrange(RIGHT, buff=0.35))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([0, -0.3, 0])
        with self.voiceover(
            "Now four numbers to write down. <bookmark mark='a'/> One: an adaptive test from a bank of three hundred "
            "items stops when its standard error reaches zero point three. About how many items does it give? "
            "<bookmark mark='b'/> Two: how many items does the best fixed form need to be as accurate? "
            "<bookmark mark='c'/> Three: five items from a law-school admission test, answered by a thousand people. "
            "Does each item need its own discrimination, or is the simplest model enough? <bookmark mark='d'/> And "
            "four: two groups differ in ability by zero point eight standard deviations. On a perfectly fair item, by "
            "how much do their proportions correct differ? Pause here, and write them down."
        ) as vo:
            self.play(FadeIn(stage))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.wait(1.0)
        self.clear_scene()
