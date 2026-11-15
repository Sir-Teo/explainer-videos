from __future__ import annotations

from videos.psychology.psych25.common import *  # noqa: F403


class Selective(VoiceoverScene):
    def construct(self):
        self.card()
        self.claims()
        self.bounds_fit()
        self.brightness()
        self.exceptions()

    def card(self):
        card = chapter_card(6, r"Each parameter, \ a claim", r"Do the model's numbers mean what they say?",
                            lit={2004: r"Voss et al.", 2008: r"Wagenmakers et al.", 2014: r"Rae et al.",
                                 2019: r"Dutilh et al."},
                            part=PART, scale=("mind",), marr=("how",))
        with self.voiceover("Chapter six. Each parameter, a claim."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def claims(self):
        head = heading(r"Selective influence")
        items = [
            (r"$v$", r"drift", DRIFT, r"how clear the evidence is", r"harder stimuli: \ lower drift"),
            (r"$a$", r"bound", BOUND, r"how much evidence is asked for", r"``be accurate'': \ wider bounds"),
            (r"$z$", r"start", EVIDENCE, r"which answer is favoured before looking", r"a likelier or better-paid "
                                                                                      r"answer: \ start nearer it"),
            (r"$t_0$", r"non-decision", TIME, r"seeing and moving", r"a harder movement: \ longer $t_0$"),
        ]
        cols = VGroup()
        for k, (sym, name, c, what, test) in enumerate(items):
            box = RoundedRectangle(corner_radius=0.15, width=3.05, height=3.5, stroke_color=c, stroke_width=2,
                                   fill_color=c, fill_opacity=0.06).move_to([-4.85 + 3.23 * k, 0.5, 0])
            body = VGroup(VGroup(label(sym, font_size=42, color=c), label(name, font_size=26, color=c)).arrange(
                RIGHT, buff=0.2), wrapped_label(what, 2.6, 23, WHITE),
                label(r"predicts:", font_size=19, color=GREY_B), wrapped_label(test, 2.6, 23, c)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.24)
            body.move_to(box.get_top() + DOWN * 0.3, aligned_edge=UP).align_to(box, LEFT).shift(RIGHT * 0.22)
            cols.add(VGroup(box, body))
        note = label(r"each manipulation should move its own parameter, \ and only that one", font_size=26,
                     color=MODEL).to_edge(DOWN, buff=0.75)
        tag = published_tag(r"Ratcliff (1978); \ Voss, \ Rothermund \& Voss (2004)")
        with self.voiceover(
            "A model with four numbers makes four claims. <bookmark mark='a'/> The drift is the quality of the "
            "evidence, so harder stimuli should lower it. <bookmark mark='b'/> The bound is caution, so asking "
            "people to be accurate should widen it. <bookmark mark='c'/> The start is bias, so making one answer "
            "likelier, or better paid, should move the start toward it. <bookmark mark='d'/> And t zero is seeing "
            "and moving, so a harder movement should lengthen it. <bookmark mark='e'/> The test, called selective "
            "influence, is that each manipulation moves its own parameter and leaves the others alone. In 2004 "
            "Andreas Voss, Klaus Rothermund and Jochen Voss ran all four manipulations in one experiment, and mostly "
            "found exactly that."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, c in zip("abcd", cols):
                vo.wait_until(m)
                self.play(FadeIn(c, shift=UP * 0.15))
            vo.wait_until("e")
            self.play(FadeIn(note))
        self.clear_scene()

    def bounds_fit(self):
        d = load("selective")
        head = heading(r"17 people, \ fitted")
        par = d["params"]
        A = axes([0.6, 2.4], [0.6, 2.4], x_length=3.8, y_length=3.8, xticks=[1.0, 1.5, 2.0], yticks=[1.0, 1.5, 2.0],
                 xfmt=lambda v: f"{v:.1f}", yfmt=lambda v: f"{v:.1f}", xlabel=r"bound $a$, \ ``be accurate''",
                 ylabel=r"bound $a$, \ ``be fast''", center=[-4.4, -0.2, 0], font_size=15)
        diag = DashedLine(A.ax.c2p(0.6, 0.6), A.ax.c2p(2.4, 2.4), color=GREY_D)
        pts = scatter(A.ax, par[:, 1, 1], par[:, 0, 1], BOUND, 0.08, 1)
        names = [r"bound", r"drift", r"bound, $t_0$", r"all three"]
        B = axes([0, 4], [0, 12], x_length=3.8, y_length=3.0, xticks=[], yticks=[0, 5, 10],
                 yfmt=lambda v: f"{v:.0f}", ylabel=r"people best fitted", center=[0.2, 0.1, 0], font_size=15)
        wins = d["wins"]
        wb = VGroup(*[bars(B.ax, [k + 0.5], [w], c, 0.6) for k, (w, c) in
                      enumerate(zip(wins, (BOUND, DRIFT, TIME, MODEL)))])
        wl = VGroup(*[wrapped_label(n, 0.95, 15, GREY_A).next_to(B.ax.c2p(k + 0.5, 0), DOWN, buff=0.1)
                      for k, n in enumerate(names)])
        wn = VGroup(*[label(str(int(w)), font_size=18).next_to(b, UP, buff=0.06) for w, b in zip(wins, wb)])
        bt = label(r"which parameters differ between the blocks?", font_size=17, color=GREY_B).next_to(B, UP, buff=0.15)
        n = len(par)
        assert d["bound_beats_drift"] == n and d["a_lower_speed"] >= n - 1 and wins[1] == 0
        rows = rows_of([
            (rf"each person fitted twice, \ one block at a time: \ the bound is lower under speed for "
             rf"{d['a_lower_speed']} of {n}, \ at about {100 * d['a_ratio']:.0f}\% of its careful width", BOUND),
            (rf"letting only the bound differ beats letting only the drift differ for all {n}, \ by AIC", WHITE),
            (rf"but the best fits also let $t_0$ differ \ ({int(wins[2])} people), \ or $t_0$ and drift too \ "
             rf"({int(wins[3])})", TIME),
        ], 3.9, 20, 0.32).move_to([4.75, 0.0, 0])
        tag = psyche_tag(r"\texttt{decide.fit\_conditions}; \ open data: \ Wagenmakers et al. (2008)")
        with self.voiceover(
            "Back to the seventeen people told to be fast or accurate. <bookmark mark='a'/> Psyche fits the model to "
            "each person's speed blocks and accuracy blocks, letting everything differ. Each dot is a person, with "
            "the two bounds as coordinates. All but one fall below the diagonal: when told to be fast, people "
            f"lowered their bound, to about {100 * d['a_ratio']:.0f} percent of its careful width. "
            "<bookmark mark='b'/> Then Psyche compares four versions of the model, by how well they fit for the "
            f"parameters they use. One where only the bound differs between the blocks beats one where only the "
            f"drift does, for all {n} people. <bookmark mark='c'/> But it isn't the whole story. The best fits also "
            f"let the non-decision time change, for {int(wins[2])} people, or the non-decision time and the drift, "
            f"for {int(wins[3])}. Told to hurry, people also press faster, and some take in a little less."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), Create(diag))
            vo.wait_until("a")
            self.play(FadeIn(pts), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(B), FadeIn(bt), FadeIn(wl), FadeIn(wb[:2]), FadeIn(wn[:2]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(wb[2:]), FadeIn(wn[2:]), FadeIn(rows[2]))
        self.clear_scene()

    def brightness(self):
        d = load("rr98")
        head = heading(r"Three observers, \ 33 brightnesses, \ one drift per brightness")
        panels = VGroup()
        plots = []
        x = d["bin_mid"]
        for k, who in enumerate(d["ids"]):
            cx = -4.3 + 4.3 * k
            P = axes([0, 32], [0, 1], x_length=3.4, y_length=1.6, xticks=[0, 16, 32], yticks=[0, 0.5, 1],
                     xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.1f}", ylabel=r"P(``light'')" if k == 0 else "",
                     center=[cx, 1.25, 0], font_size=14)
            R = axes([0, 32], [0.2, 1.2], x_length=3.4, y_length=1.6, xticks=[0, 16, 32], yticks=[0.4, 0.8, 1.2],
                     xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.1f}", ylabel=r"mean time, \ s" if k == 0 else "",
                     xlabel=r"brightness" if k == 1 else "", center=[cx, -1.45, 0], font_size=14)
            name = label(rf"observer {who}", font_size=19, color=GREY_A).next_to(P, UP, buff=0.12)
            dots, lines = VGroup(), VGroup()
            for j, c in enumerate((SPEED, CAREFUL)):
                dots.add(scatter(P.ax, x, d["obs_p"][k, j], c, 0.055, 1), scatter(R.ax, x, d["obs_rt"][k, j], c,
                                                                                    0.055, 1))
                lines.add(curve(P.ax, x, d["mod_p"][k, j], c, 2.5), curve_in(R.ax, x, np.minimum(d["mod_rt"][k, j],
                                                                                                    1.2), c, 2.5))
            panels.add(VGroup(P, R, name))
            plots.append((dots, lines))
        key = legend([(SPEED, r"``be fast''"), (CAREFUL, r"``be accurate''"), (GREY_A, r"dots: \ data; \ lines: "
                                                                                      r"\ model")], font_size=17)
        key.arrange(RIGHT, buff=0.5).to_edge(DOWN, buff=0.55).to_edge(LEFT, buff=0.6)
        a = d["a"]
        assert np.all(a[:, 1] > 1.5 * a[:, 0]) and np.all(a[:, 1] < 2.5 * a[:, 0])
        tag = psyche_tag(r"open data: \ Ratcliff \& Rouder (1998), \ via rtdists")
        with self.voiceover(
            "A sterner test uses Ratcliff and Rouder's data from 1998. <bookmark mark='a'/> Three observers judged "
            "whether patches of pixels came from a light or a dark source, at thirty-three levels of brightness, "
            "again in fast and careful blocks, about eight thousand trials each. Top: how often they said light. "
            "Bottom: how long they took. <bookmark mark='b'/> Psyche fits each observer with one drift for each "
            "level of brightness, the same in both kinds of block, and a bound, a start and a non-decision time for "
            "each kind: fourteen numbers for four curves. <bookmark mark='c'/> They fit closely. In careful blocks, "
            "times peak at the hardest, most ambiguous patches and fall away on either side, and the model draws "
            "that arch from the drifts alone. Every observer's careful bound is between one and a half and two and "
            "a half times the fast one. <bookmark mark='d'/> Where it misses is telling: in fast blocks the model "
            "expects a small arch that people barely show. Something more than four numbers is at work, as the next "
            "chapter shows."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(panels))
            vo.wait_until("a")
            self.play(*[FadeIn(p[0]) for p in plots], FadeIn(key))
            vo.wait_until("b")
            self.play(*[Create(p[1]) for p in plots], run_time=2)
            vo.wait_until("c")
            self.play(*[Indicate(p[1][1], scale_factor=1.0) for p in plots])
            vo.wait_until("d")
            self.play(*[Indicate(p[1][2], scale_factor=1.0, color=SPEED) for p in plots])
        self.clear_scene()

    def exceptions(self):
        head = heading(r"Mostly, \ not purely")
        items = [
            (r"Rae, \ Heathcote, \ Donkin, \ Averell \& Brown, \ 2014", r"speed instructions lower the bound, \ and "
             r"also the drift: \ hurrying people take in less", BOUND),
            (r"Dutilh and 17 teams, \ 2019", r"14 datasets with hidden manipulations; \ modellers, \ blind, \ mostly "
             r"named the right parameter, \ and their choices of method mattered", MODEL),
            (r"the lesson", r"the parameters are claims about the mind, \ and claims can be tested; \ these pass "
             r"often, \ not always", WHITE),
        ]
        rows = VGroup()
        for who, what, c in items:
            rows.add(VGroup(label(who, font_size=24, color=c), wrapped_label(what, 11.8, 25, WHITE)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.15))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.55).move_to([0, 0.0, 0])
        tag = published_tag(r"Rae et al. (2014); \ Dutilh et al. (2019)")
        with self.voiceover(
            "So the parameters mostly mean what they claim, but not purely. <bookmark mark='a'/> In 2014 Benjamin "
            "Rae and colleagues found that speed instructions lower the drift as well as the bound: people in a "
            "hurry take in less. <bookmark mark='b'/> And in 2019 Gilles Dutilh organized a blind test. Seventeen "
            "teams of modellers received fourteen datasets, each with a hidden manipulation, and had to say what had "
            "changed. Most of the time they named the right parameter, though their choice of method mattered, "
            "and simple methods did about as well as elaborate ones. <bookmark mark='c'/> The parameters are "
            "claims about the mind, and claims can be tested. These pass often, not always."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abc", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
