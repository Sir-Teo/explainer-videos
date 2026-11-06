from __future__ import annotations

from videos.philosophy.philosophy23.common import *  # noqa: F403


class Design(VoiceoverScene):
    def construct(self):
        card = chapter_card(7, r"Design and fine-tuning", r"Is the universe set up for life?", lit=(1802, 2000),
                            part=PART)
        with self.voiceover("Chapter seven. Design and fine-tuning."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.watch()
        self.tuning()
        self.computed()
        self.objections()

    def watch(self):
        head = label(r"From the watch to the likelihood", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"Paley \ (1802)", r"a watch on a heath implies a watchmaker; \ the eye is more intricate still", HIST),
            (r"Hume \ (1779)", r"the analogy is weak; \ one universe gives no frequencies; \ why one designer, \ and "
                               r"why a good one?", NAT),
            (r"Darwin \ (1859)", r"selection makes eyes without foresight \ (Part 19)", OK),
            (r"Sober \ (2003)", r"a likelihood argument: \ does the evidence fit design better than chance?", ABS),
            (r"the test", r"$P(E \mid \text{design}) \gg P(E \mid \text{chance})$ \ favours design, \ if design "
                          r"predicts $E$", GOAL),
        ]
        g = rows_table(rows, top=1.9, gap=0.45, width=8.8, x_text=-2.6, label_size=21)
        with self.voiceover(
            "The teleological argument has had three lives. <bookmark mark='a'/>William Paley: a watch found on a "
            "heath implies a watchmaker, and the eye is more intricate than any watch. <bookmark mark='b'/>Hume had "
            "already objected that the analogy is weak, that we have one universe and no frequencies of universes "
            "made by gods, and that the argument cannot tell us whether the designer is one, or good. "
            "<bookmark mark='c'/>Darwin answered the biological version: natural selection makes eyes without "
            "foresight, as Part 19 built. <bookmark mark='d'/>Elliott Sober recast what remains as a likelihood "
            "argument. <bookmark mark='e'/>Evidence favours design over chance if it is much more probable given "
            "design, and only if the design hypothesis really predicts it."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def tuning(self):
        d = load("tuning")
        head = label(r"The fine-tuning argument", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        bar = Rectangle(width=11.0, height=0.5, color=GREY_B, fill_opacity=0.1).move_to([0, 1.3, 0])
        win = Rectangle(width=0.08, height=0.5, color=OK, fill_opacity=0.9).move_to([1.7, 1.3, 0])
        bl = label(r"possible values of a constant", font_size=18, color=GREY_A).next_to(bar, UP, buff=0.1)
        wl = label(r"life-permitting window: \ width " + f"{d['eps']}", font_size=18, color=OK).next_to(win, DOWN,
                                                                                                        buff=0.15)
        rows = stack([(r"examples cited: \ the cosmological constant; \ the strength of gravity relative to "
                       r"electromagnetism; \ the Hoyle state of carbon", WHITE),
                      (r"by chance, \ landing in the window has probability " + f"{d['eps']}", NAT),
                      (r"a designer who wanted life would aim for it: \ say probability " + f"{d['q_design']}", DIV),
                      (r"likelihood ratio, \ design to chance: \ " + f"{d['lr_design_vs_chance']:.0f}", ABS)],
                     font_size=21, aligned_edge=LEFT, width=12.2).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Its third life is physics. <bookmark mark='a'/>Several constants of nature appear to lie in narrow "
            "ranges compatible with life: the cosmological constant, the strength of gravity relative to "
            "electromagnetism, the energy level in carbon that lets stars make it. <bookmark mark='b'/>Model one "
            "constant as a point on a line, and the life-permitting values as a window one thousandth wide. By "
            "chance, landing in the window has probability one in a thousand. <bookmark mark='c'/>A designer who "
            "wanted life would aim for the window; say, with probability one half. <bookmark mark='d'/>The likelihood "
            "ratio, design to chance, is five hundred. On these numbers, life-permitting constants strongly favour "
            "design over a single chancy universe."
        ) as vo:
            self.play(FadeIn(head), FadeIn(bar), FadeIn(bl))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(win), FadeIn(wl), FadeIn(rows[1]))
            for mk, r in zip("cd", rows[2:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def computed(self):
        d = load("tuning")
        head = label(r"Add a multiverse", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        hd = [r"\text{hypothesis}", r"P(\text{some universe permits life})", r"P(\text{\textit{this} one does})"]
        L = d["likelihoods"]
        names = [("single chance", r"\text{one chancy universe}"), ("multiverse",
                                                                    r"\text{multiverse, }" + f"{d['universes']:,}".replace(",", r"\,") + r"\text{ universes}"),
                 ("design", r"\text{design}")]
        rows = [[MathTex(t, font_size=20), MathTex(f"{L[k]['some']:.4g}", font_size=22),
                 MathTex(f"{L[k]['this']:.4g}", font_size=22)] for k, t in names]
        grid = ValueGrid(hd, rows, col_w=[4.2, 3.8, 3.2], cell_h=0.55, font_size=19).move_to([0, 1.1, 0])
        ps = d["posterior_some"]
        pt = d["posterior_this"]
        post = VGroup(label(r"with equal priors, \ posterior on `some universe': \ multiverse " +
                            f"{ps['multiverse']:.2f}" + r", \ design " + f"{ps['design']:.2f}", font_size=20,
                            color=ARG),
                      label(r"posterior on `this universe': \ multiverse " + f"{pt['multiverse']:.3f}" +
                            r", \ design " + f"{pt['design']:.3f}", font_size=20, color=DIV)).arrange(
            DOWN, buff=0.15).next_to(grid, DOWN, buff=0.35)
        rows2 = stack([(r"Hacking \ (1987); \ White \ (2000): \ that \textit{this} universe permits life is no more "
                        r"likely with many universes: \ the inverse gambler's fallacy", GOAL),
                       (r"the reply: \ we could only observe a life-permitting universe, \ so the right evidence is "
                        r"`some universe permits life' \ (Bradley; \ Manson)", BAD)], font_size=19, aligned_edge=LEFT,
                      width=12.2).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The usual reply is the multiverse. <bookmark mark='a'/>If there are ten thousand universes with "
            "independently chancy constants, it is almost certain that some universe permits life. On the evidence "
            "that some universe does, the multiverse fits as well as design, and with equal priors it ends up the "
            "most probable hypothesis. <bookmark mark='b'/>But Ian Hacking and Roger White pointed out that our "
            "evidence is that this universe permits life, and the chance that this particular universe lands in the "
            "window is one in a thousand however many others there are. On that evidence the multiverse does no "
            "better than a single chancy universe, and design dominates. Inferring many universes from one fine-tuned "
            "universe is the inverse gambler's fallacy: thinking that a double six makes it likely the dice have been "
            "thrown many times. <bookmark mark='c'/>Others reply that, since we could only ever observe a "
            "life-permitting universe, the correct evidence is that some universe permits life, and then the "
            "multiverse is confirmed. The calculation is easy; choosing the evidence is the philosophy."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), Create(grid.rule),
                      *[FadeIn(grid.cell[r][0]) for r in range(3)])
            vo.wait_until("a")
            self.play(*[FadeIn(grid.cell[r][1]) for r in range(3)], FadeIn(post[0]))
            vo.wait_until("b")
            self.play(*[FadeIn(grid.cell[r][2]) for r in range(3)], FadeIn(post[1]), FadeIn(rows2[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows2[1]))
        self.clear_scene()

    def objections(self):
        head = label(r"Other objections", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"the measure", r"over an infinite range of values no uniform probability exists \ (McGrew, \ McGrew and "
                             r"Vestrup, \ 2001)", BAD),
            (r"the prediction", r"what would a designer choose? \ Sober: \ without independent knowledge, \ "
                                r"$P(E \mid \text{design})$ is unknown", ABS),
            (r"life as we know it", r"other values might permit other kinds of life", NAT),
            (r"deeper laws", r"a future theory may fix the constants: \ then the question moves to the laws", ARG),
            (r"the anthropic principle", r"we can only observe a world that allows observers \ (Carter, \ 1974)",
             GOAL),
        ]
        g = rows_table(rows, top=1.9, gap=0.45, width=8.8, x_text=-2.4, label_size=21)
        with self.voiceover(
            "There are other objections. <bookmark mark='a'/>The measure problem: if a constant could take any of "
            "infinitely many values, there is no uniform probability distribution over them, and one in a thousand "
            "has no clear meaning. <bookmark mark='b'/>The prediction problem: what would a designer choose? Without "
            "independent knowledge of a designer's aims, Sober argues, the probability of the evidence given design "
            "is simply unknown. <bookmark mark='c'/>Other values might permit other kinds of life. "
            "<bookmark mark='d'/>A deeper physical theory might fix the constants, which would move the question to "
            "the laws themselves. <bookmark mark='e'/>And Brandon Carter's anthropic principle reminds us that we "
            "could only observe a universe compatible with observers."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
