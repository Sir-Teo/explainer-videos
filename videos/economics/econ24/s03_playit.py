from __future__ import annotations

from videos.economics.econ24.common import *  # noqa: F403

LETTERS = "ABCD"
CHIP = ("#F2C14E", "#7EC8F5", "#7BD88F", "#F2788F")


class PlayIt(VoiceoverScene):
    def construct(self):
        card(self, 2, r"Play it: \ take it or keep looking?", r"Offers arrive one a month. \ When do you stop?",
             "Chapter two. Play it: take it, or keep looking?", lit={1961: r"Stigler", 1970: r"McCall"},
             scale=("person",), horizon=("months",))
        self.rules()
        self.offers()
        self.score()

    def rules(self):
        p = load("playit")
        stage = game_stage(12.6, 6.4, center=DOWN * 0.1)
        rows = VGroup(
            label(r"you are out of work; \ one job offer arrives each month", font_size=23, color=GREY_A),
            label(rf"each offer is a wage between {p['low']:.0f} and {p['high']:.0f} a month, \ every value equally "
                  r"likely", font_size=22, color=JOB),
            label(rf"while you look, \ you get a benefit of {p['b']:.0f}; \ a job you take, \ you keep for ever",
                  font_size=22, color=BENEFIT),
            label(rf"next month's money is worth {p['beta']:.2f} of this month's", font_size=21, color=GREY_B),
            label(r"choose your rule before the offers arrive: \ take the first offer of at least \dots", font_size=25,
                  color=E.ACCENT),
        ).arrange(DOWN, buff=0.24).move_to(stage.box.get_top() + DOWN * 1.9)
        chips = VGroup(*[VGroup(RoundedRectangle(width=2.4, height=1.0, corner_radius=0.12, stroke_color=c,
                                                 stroke_width=3, fill_color=c, fill_opacity=0.12),
                                label(rf"{LETTERS[i]}: \ {r['R']}", font_size=28, color=c))
                         for i, (c, r) in enumerate(zip(CHIP, p["rules"]))]).arrange(RIGHT, buff=0.35)
        for ch in chips:
            ch[1].move_to(ch[0])
        chips.next_to(rows, DOWN, buff=0.45)
        ring = countdown().next_to(chips, DOWN, buff=0.3)
        with self.voiceover(
            "Your turn. You are out of work, and one job offer arrives each month. <bookmark mark='a'/> Each offer "
            f"is a monthly wage somewhere between {p['low']:.0f} and {p['high']:.0f}, every value equally likely. "
            f"<bookmark mark='b'/> While you look, you receive an unemployment benefit of {p['b']:.0f} a month. A "
            "job you accept, you keep for ever, and you cannot go back to an offer you turned down. "
            f"<bookmark mark='c'/> And you are a little impatient: next month's money is worth {p['beta']:.2f} of "
            "this month's. <bookmark mark='d'/> Choose your rule before the offers arrive. You will take the first "
            "offer of at least: A, eighty; B, a hundred; C, a hundred and twenty; or D, a hundred and forty. Pause, "
            "and choose."
        ) as vo:
            self.play(FadeIn(stage), FadeIn(rows[0]))
            for mk, r_ in zip("abcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_))
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in chips], lag_ratio=0.3), FadeIn(ring),
                      run_time=2.5)
        self.add(ring[1])
        self.play(ring.t.animate.set_value(0.0), run_time=8.0, rate_func=linear)
        self.clear_scene()

    def offers(self):
        p = load("playit")
        n = len(p["offers"])
        ax = plane([0.5, n + 0.5], [40, 155], center=LEFT * 1.6 + DOWN * 0.4, x_length=8.6, y_length=5.0,
                   xticks=list(range(1, n + 1)), yticks=[50, 80, 100, 120, 140], xlabel=r"month",
                   ylabel=r"the offer", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=16)
        bars = VGroup()
        for k, o in enumerate(p["offers"]):
            lo, hi = ax.ax.c2p(k + 1, 40), ax.ax.c2p(k + 1, o)
            bars.add(Rectangle(width=0.5, height=hi[1] - lo[1], fill_color=JOB, fill_opacity=0.75,
                               stroke_width=0).move_to((lo + hi) / 2))
        vals = VGroup(*[label(f"{o}", font_size=16, color=WHITE).next_to(b, UP, buff=0.06)
                        for b, o in zip(bars, p["offers"])])
        lines = VGroup(*[seg(ax, 0.5, r["R"], n + 0.5, r["R"], color=c, width=2, dashed=True)
                         for r, c in zip(p["rules"], CHIP)])
        tags = VGroup(*[label(LETTERS[i], font_size=18, color=c).next_to(ax.ax.c2p(n + 0.5, r["R"]), RIGHT,
                                                                         buff=0.1)
                        for i, (r, c) in enumerate(zip(p["rules"], CHIP))])
        side = VGroup()
        for i, (r, c) in enumerate(zip(p["rules"], CHIP)):
            txt = (rf"{LETTERS[i]}: \ took {r['wage']} in month {r['k'] + 1}" if r["k"] is not None
                   else rf"{LETTERS[i]}: \ still looking \\ after ten months")
            side.add(label(txt, font_size=20, color=c))
        side.arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Here come the offers. <bookmark mark='a'/> Eighty-eight; seventy-one; a hundred and four; sixty-three; "
            "ninety-seven; a hundred and twenty-one; seventy-nine; a hundred and thirty-five; ninety-two; a hundred "
            "and ten. <bookmark mark='b'/> Now your rule. <bookmark mark='c'/> A, eighty, stops at once: "
            "eighty-eight, in the first month. <bookmark mark='d'/> B, a hundred, takes a hundred and four in the "
            "third month. <bookmark mark='e'/> C, a hundred and twenty, waits until the sixth month and takes a "
            "hundred and twenty-one. <bookmark mark='f'/> And D, a hundred and forty, never stops: after ten months "
            "it is still looking, still living on the benefit. In hindsight, the best offer was a hundred and "
            "thirty-five, in month eight. But nobody searching knows which offer is the best one until it is too "
            "late."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), run_time=0.8)
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(b, DOWN), FadeIn(v)) for b, v in zip(bars, vals)],
                                  lag_ratio=0.5), run_time=9)
            vo.wait_until("b")
            self.play(FadeIn(lines), FadeIn(tags))
            for i, mk in enumerate("cdef"):
                vo.wait_until(mk)
                r = p["rules"][i]
                anims = [FadeIn(side[i])]
                if r["k"] is not None:
                    anims.append(Indicate(bars[r["k"]], color=CHIP[i], scale_factor=1.15))
                self.play(*anims)
        self.clear_scene()

    def score(self):
        p = load("playit")
        head = VGroup(label(r"rule", font_size=22, color=GREY_B), label(r"on these offers", font_size=22,
                                                                       color=GREY_B),
                      label(r"expected, \ before the draw", font_size=22, color=GREY_B),
                      label(r"as a wage for ever", font_size=22, color=GREY_B))
        rows = [head]
        for i, (r, c) in enumerate(zip(p["rules"], CHIP)):
            rows.append(VGroup(label(rf"{LETTERS[i]}: \ at least {r['R']}", font_size=23, color=c),
                               label(commas(r["value_here"]) if r["k"] is not None else r"still looking",
                                     font_size=23, color=c),
                               label(commas(r["value"]), font_size=23, color=c),
                               label(f"{r['equivalent']:.1f}", font_size=23, color=c)))
        rows.append(VGroup(label(r"the best rule", font_size=23, color=E.ACCENT), label(r"", font_size=23),
                           label(commas(p["best_value"]), font_size=23, color=E.ACCENT),
                           label(f"{p['reservation']:.1f}", font_size=23, color=E.ACCENT)))
        xs = (-4.6, -1.3, 1.6, 4.5)
        for k, row in enumerate(rows):
            for c, cell in enumerate(row):
                cell.move_to([xs[c], 2.3 - 0.72 * k, 0])
        table = VGroup(*rows)
        note_ = label(rf"the best rule: \ take the first offer of at least {p['reservation']:.1f}, \ the "
                      r"\emph{reservation wage}; \ C was almost exactly right", font_size=23,
                      color=E.ACCENT).to_edge(DOWN, buff=0.7)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "How did you do? Score each rule by the present value of everything it brings, benefits while "
            "searching and the wage for ever after. <bookmark mark='a'/> On these particular offers, C did best. But "
            "luck matters in any single draw, so the right score is the value a rule is expected to bring before "
            "the offers are seen. <bookmark mark='b'/> A, too eager, is worth a job paying about a hundred and ten "
            "for ever. B, about a hundred and seventeen. C, about a hundred and twenty-one. D, too choosy, about a "
            "hundred and nine: it waits ten months, on average, for an offer that good. <bookmark mark='c'/> The "
            "best possible rule, worked out in the next chapter, takes the first offer of at least "
            f"{p['reservation']:.1f}. If you chose C, you were almost exactly right."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), *[FadeIn(r[:2]) for r in rows[1:5]])
            vo.wait_until("b")
            self.play(*[FadeIn(r[2:]) for r in rows[1:5]])
            vo.wait_until("c")
            self.play(FadeIn(rows[5]), FadeIn(note_))
        del table
        self.clear_scene()
