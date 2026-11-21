from __future__ import annotations

from videos.economics.econ54.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.railway()
        self.how()
        self.question()
        self.title()
        self.objectives()

    def railway(self):
        B = load("bart")
        ax = plane([0.4, 3.6], [0, 17], center=LEFT * 1.6 + DOWN * 0.4, x_length=7.0, y_length=4.8, xticks=[],
                   yticks=[0, 5, 10, 15], ylabel=r"share of work trips by BART, \ \%", yfmt=lambda v: f"{v:.0f}",
                   font_size=16)
        specs = [(1, B["official"], GRID, r"the official \\ forecast", r"about 15\%"),
                 (2, B["mcfadden"], EST, r"McFadden's \\ model, 1973", rf"{B['mcfadden']:.1f}\%"),
                 (3, B["actual"], DATA, r"what happened, \\ 1975", rf"{B['actual']:.1f}\%")]
        bars = VGroup()
        for x, v, c, name, val in specs:
            p0, p1 = ax.ax.c2p(x - 0.32, 0), ax.ax.c2p(x + 0.32, v)
            r = Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], fill_color=c, fill_opacity=0.85,
                          stroke_width=0).move_to((p0 + p1) / 2)
            nm = label(name, font_size=17, color=c).next_to(ax.ax.c2p(x, 0), DOWN, buff=0.2)
            vl = label(val, font_size=20, color=c).next_to(r, UP, buff=0.12)
            bars.add(VGroup(r, nm, vl))
        side = VGroup(
            label(r"the official model: \\ trips between zones of the map", font_size=19, color=GRID),
            label(r"McFadden's: \ each commuter's choice \\ among car, \ bus and train, \\ fitted to a survey "
                  r"\\ taken before BART opened", font_size=19, color=EST),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).to_edge(RIGHT, buff=0.5)
        tag = published_tag(r"McFadden, \ Access 20 (2002); \ Nobel lecture, \ AER 91(3) (2001)", corner=DR,
                            font_size=12)
        head = label(r"the San Francisco Bay Area's new railway, \ BART", font_size=26, color=E.ACCENT).to_edge(
            UP, buff=0.45).shift(RIGHT * 2.6)
        with self.voiceover(
            "In the early 1970s the San Francisco Bay Area was building a railway, BART, and planners had to say "
            "how many people would ride it. <bookmark mark='a'/> The official forecast, from a model of the trips "
            "between zones of the map, said about fifteen percent of work trips. <bookmark mark='b'/> Daniel "
            "McFadden tried something else. Before a single train ran, he took a survey of commuters: how long "
            "each trip took by car and by bus, what it cost, and what each person chose. From those choices he "
            "estimated how much a minute and a dollar mattered to them, and used that to forecast a choice they had "
            f"never had. His model said {B['mcfadden']:.1f} percent. <bookmark mark='c'/> When BART was running, "
            f"in 1975, it carried {B['actual']:.1f} percent. McFadden went back to the same travellers to check."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(head, shift=DOWN * 0.1))
            vo.wait_until("a")
            self.play(FadeIn(bars[0], shift=UP * 0.1), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(bars[1], shift=UP * 0.1), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(bars[2], shift=UP * 0.1))
            self.play(Indicate(VGroup(bars[1][2], bars[2][2]), color=WHITE, scale_factor=1.05))
        self.clear_scene()

    def how(self):
        steps = flow_chain(steps=[(r"choices people made", DATA), (r"a model with hidden parameters", MODEL),
                                  (r"estimates, with their uncertainty", EST),
                                  (r"a forecast of a world nobody has seen", GAIN)],
                           box_w=2.9, box_h=1.2, font_size=20, buff=0.45).move_to(UP * 0.6)
        notes = VGroup(
            label(r"the parameters: \ what a minute, \ a dollar, \ the future, \ a risk is worth to people",
                  font_size=21, color=MODEL),
            label(r"they stay put when the policy changes, \ so the model can be asked about a new one",
                  font_size=21, color=GAIN),
        ).arrange(DOWN, buff=0.3).next_to(steps, DOWN, buff=0.8)
        with self.voiceover(
            "That is what this part is about. <bookmark mark='a'/> Start with choices people actually made. "
            "<bookmark mark='b'/> Write a model in which those choices come from hidden quantities: what a minute, "
            "a dollar, the future or a risk is worth to them. <bookmark mark='c'/> Find the values of those "
            "quantities that make the model's predictions match the choices, and say how sure you are. "
            "<bookmark mark='d'/> Then ask the model about a world nobody has seen: a new railway, a new tax, a "
            "new pension. <bookmark mark='e'/> It works only if the hidden quantities stay put when the world "
            "changes, and only if the data really pin them down. Both of those can fail, and this part shows how "
            "to tell."
        ) as vo:
            for mk, k in zip("abcd", range(4)):
                vo.wait_until(mk)
                an = [FadeIn(steps.boxes[k], shift=UP * 0.1)]
                if k > 0:
                    an.append(Create(steps.arrows[k - 1]))
                self.play(*an)
                if k == 1:
                    self.play(FadeIn(notes[0]))
            vo.wait_until("e")
            self.play(FadeIn(notes[1]))
        self.clear_scene()

    def question(self):
        q = wrapped_label(ASK, 12.0, 34, E.ACCENT).to_edge(UP, buff=0.8)
        rows = VGroup(
            label(r"what makes a model's parameters worth measuring?", font_size=26, color=MODEL),
            label(r"how are they measured: \ likelihood, \ moments, \ simulation?", font_size=26, color=EST),
            label(r"what in the data pins down which parameter?", font_size=26, color=DATA),
            label(r"and how would we know if the answer were wrong?", font_size=26, color=ERR),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42).next_to(q, DOWN, buff=0.6)
        with self.voiceover(
            "The question: how is a model's hidden machinery measured from the choices it predicts? <bookmark "
            "mark='a'/> What makes a model's parameters worth measuring at all? <bookmark mark='b'/> How are they "
            "measured: by likelihood, by moments, by simulation? <bookmark mark='c'/> What in the data pins down "
            "which parameter? <bookmark mark='d'/> And how would we know if the answer were wrong?"
        ) as vo:
            self.play(FadeIn(q, shift=DOWN * 0.2))
            for mk, r_ in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
        self.clear_scene()

    def title(self):
        F = load("film")
        mini = plane([F["t"][0], F["t"][-1]], [0, 1], x_length=4.2, y_length=1.4)
        v = np.array(F["v"])
        v = (v - v.min()) / (v.max() - v.min())
        logo = path(mini, F["t"], v, DATA, 2.6, smooth=False)
        tt = label(r"Economics, Built", font_size=60)
        sub = label(r"Part 54 \ $\cdot$ \ Estimating Models", font_size=34, color=E.ACCENT)
        VGroup(logo, tt, sub).arrange(DOWN, buff=0.45)
        with self.voiceover("Economics, Built. Part fifty-four: estimating models."):
            self.play(Create(logo), run_time=1.6)
            self.play(Write(tt), run_time=1.2)
            self.play(FadeIn(sub, shift=UP * 0.15))
        self.wait(1.0)
        self.clear_scene()

    def objectives(self):
        head = label(r"Act X \ $\cdot$ \ The Graduate Core", font_size=40, color=E.ACCENT)
        obj = objectives_card([
            r"what makes a model structural, \ and why new policies need one",
            r"maximum likelihood, \ the generalized method of moments, \ simulation",
            r"identification: \ which facts in the data pin down which parameters",
            r"calibration, \ sufficient statistics, \ validation, \ and bounds",
            r"the Island's commuters and households, \ estimated with the truth known",
        ], color=E.ACCENT, font_size=31, width=13.0)
        with self.voiceover(
            "By the end of this part you will be able to say <bookmark mark='a'/> what makes a model structural, "
            "and why a forecast of a new policy needs one; <bookmark mark='b'/> how maximum likelihood, the "
            "generalized method of moments and simulation estimate its parameters, with standard errors; "
            "<bookmark mark='c'/> which facts in the data pin down which parameters, and how to check; <bookmark "
            "mark='d'/> where calibration, sufficient statistics, validation against experiments and bounds fit "
            "in; <bookmark mark='e'/> and you will have watched all of it done on the Island, where the truth is "
            "known, so every estimate can be graded."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(head), FadeIn(obj.head), FadeIn(obj.rows[0], shift=RIGHT * 0.2))
            for mk, r_ in zip("bcde", obj.rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
        self.clear_scene()
