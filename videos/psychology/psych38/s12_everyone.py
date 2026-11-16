from __future__ import annotations

from videos.psychology.psych38.common import *  # noqa: F403


class Everyone(VoiceoverScene):
    def construct(self):
        self.card()
        self.decade()
        self.network()

    def card(self):
        card = chapter_card(11, r"A psychology of everyone", r"Has the sample changed?",
                            lit={2018: r"Rad et al.", 2021: r"Thalmayer et al."}, part=PART,
                            scale=("culture",), marr=("what",))
        with self.voiceover("Chapter eleven. A psychology of everyone."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def decade(self):
        head = heading(r"A decade later")
        A = axes([-0.6, 1.6], [0, 80], x_length=4.2, y_length=3.2, xticks=None, yticks=[0, 20, 40, 60, 80],
                 yfmt=lambda v: f"{v:.0f}\\%", ylabel=r"American share of samples", center=[-3.6, -0.1, 0],
                 font_size=14)
        b = bars(A.ax, [0, 1], [68, 61], [PERSON, PERSON], width=0.6)
        names = VGroup(wrapped_label(r"2003 to 2007", 1.8, 15, GREY_A).next_to(A.ax.c2p(0, 0), DOWN, buff=0.15),
                       wrapped_label(r"2014 to 2018", 1.8, 15, GREY_A).next_to(A.ax.c2p(1, 0), DOWN, buff=0.15))
        tops = VGroup(label(r"68\%", font_size=17, color=PERSON).next_to(A.ax.c2p(0, 68), UP, buff=0.08),
                      label(r"a little over 60\%", font_size=15, color=PERSON).next_to(A.ax.c2p(1, 61), UP, buff=0.08))
        rows = rows_of([
            (r"Thalmayer, \ Toscanelli and Arnett, \ 2021: \ the same six journals, \ 2014 to 2018", WHITE),
            (r"American samples fell to a little over 60\%; \ the gain went mostly to other English-speaking and "
             r"Western European countries", PERSON),
            (r"samples from the majority world, \ where most people live, \ were still about 4 to 5\%", WORLD),
            (r"Rad, \ Martingano and Ginges, \ 2018: \ in \emph{Psychological Science} in 2014, \ about half the "
             r"samples were American, \ and most papers did not say why their sample should generalize", AUTH),
        ], 6.0, 19, 0.36).move_to([3.4, -0.2, 0])
        tag = published_tag(r"Thalmayer, \ Toscanelli \& Arnett (2021); \ Rad, \ Martingano \& Ginges (2018)")
        with self.voiceover(
            "Has the sample changed since the WEIRD paper? <bookmark mark='a'/> In 2021 Amber Thalmayer, Cecilia "
            "Toscanelli and Jeffrey Arnett repeated the count in the same six journals, for 2014 to 2018. "
            "<bookmark mark='b'/> American samples had fallen to a little over sixty percent. The gain went mostly "
            "to other English-speaking and Western European countries. <bookmark mark='c'/> Samples from the "
            "majority world, where most people live, were still about four to five percent. <bookmark mark='d'/> "
            "And in Psychological Science in 2014, about half the samples were American, and most papers didn't say "
            "why their sample should generalize. The Ledger marks WEIRD sampling as replicated: still true a decade "
            "on."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(names))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), GrowFromEdge(b[0], DOWN), FadeIn(tops[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), GrowFromEdge(b[1], DOWN), FadeIn(tops[1]))
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def network(self):
        head = heading(r"Science by network")
        # a schematic world: dots for laboratories joined to a hub
        hub = Dot([-3.6, 0.2, 0], radius=0.14, color=MODEL)
        rng = np.random.default_rng(45)
        labs = VGroup()
        for k in range(45):
            a = TAU * k / 45
            r = 1.4 + 0.6 * rng.random()
            labs.add(Dot([-3.6 + 1.25 * r * np.cos(a), 0.2 + 0.95 * r * np.sin(a), 0], radius=0.06,
                         color=WORLD if k % 3 else WEST))
        spokes = VGroup(*[Line(hub.get_center(), d.get_center(), color=GREY_D, stroke_width=1) for d in labs])
        note = label(r"schematic", font_size=13, color=GREY_B).move_to([-3.6, -2.6, 0])
        rows = rows_of([
            (r"the fix is organizational: \ networks of laboratories that run one registered protocol in many "
             r"countries at once", WHITE),
            (r"the Psychological Science Accelerator, \ ManyBabies, \ Many Labs, \ and the trolley study of "
             r"chapter eight", MODEL),
            (r"what they buy: \ samples beyond one campus, \ tests of whether an effect varies, \ and results "
             r"that do not depend on one laboratory", GOOD),
            (r"what they cannot buy alone: \ theories built from the start by people from the places being "
             r"studied", YOU),
        ], 6.0, 19, 0.36).move_to([3.4, -0.2, 0])
        with self.voiceover(
            "The fix that's working is organizational. <bookmark mark='a'/> Networks of laboratories now run one "
            "registered protocol in many countries at once. <bookmark mark='b'/> The Psychological Science "
            "Accelerator, ManyBabies, Many Labs, and the trolley study of chapter eight are examples. "
            "<bookmark mark='c'/> They buy samples beyond one campus, tests of whether an effect varies, and results "
            "that don't depend on one laboratory. <bookmark mark='d'/> What they can't buy on their own is theory "
            "built from the start by people from the places being studied."
        ) as vo:
            self.play(FadeIn(head), FadeIn(hub), FadeIn(note))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), Create(spokes), LaggedStart(*[FadeIn(d) for d in labs], lag_ratio=0.03))
            for m, r in zip("bcd", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
