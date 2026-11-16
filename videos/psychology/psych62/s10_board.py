from __future__ import annotations

from videos.psychology.psych62.common import *  # noqa: F403


class Board(VoiceoverScene):
    def construct(self):
        card_section(self, 9, r"The Ledger, \ complete", r"What held?", scale=("society",), marr=("what",))
        self.chart()
        self.decades()
        self.pattern()

    def chart(self):
        d = load("board")
        head = heading(rf"{d['total']} rows, \ thirteen acts")
        tab = np.asarray(d["table"], float)
        frac = tab / tab.sum(1, keepdims=True)
        cols = [GOOD, PERSON, AUTH, GREY_B]
        W, H = 0.62, 4.2
        x0, y0 = -5.6, -2.0
        bars_ = VGroup()
        for i in range(len(d["acts"])):
            base = 0.0
            for j in range(4):
                h = float(frac[i, j]) * H
                if h > 0:
                    bars_.add(Rectangle(width=W, height=h, stroke_width=0, fill_color=cols[j], fill_opacity=0.9)
                              .move_to([x0 + i * 0.86, y0 + base + h / 2, 0]))
                base += h
        names = VGroup(*[label(a, font_size=16, color=GREY_A).move_to([x0 + i * 0.86, y0 - 0.25, 0])
                         for i, a in enumerate(d["acts"])])
        ns = VGroup(*[label(f"{int(t)}", font_size=13, color=GREY_B).move_to([x0 + i * 0.86, y0 + H + 0.2, 0])
                      for i, t in enumerate(tab.sum(1))])
        key = VGroup(*[label(t, font_size=15, color=c) for t, c in zip(
            (r"held", r"contested", r"failed or retracted", r"not directly tested"), cols)]).arrange(RIGHT, buff=0.4)
        key.next_to(head, DOWN, buff=0.2)
        c = d["counts"]
        held = c["replicated"] + c["replicated, smaller"] + c["story and record"]
        foot = wrapped_label(rf"held: \ {held} of {d['total']} ({100 * held / d['total']:.0f}\%), \ of which "
                             rf"{c['replicated, smaller']} smaller than first reported; \ contested {c['contested']}; "
                             rf"\ failed {c['failed']}; \ retracted {c['retracted']}", 12.4, 19, YOU)
        foot.to_edge(DOWN, buff=0.35)
        with self.voiceover(
            f"Here's the complete Ledger: {d['total']} rows, read by act. <bookmark mark='a'/> Green held: "
            f"replicated, replicated but smaller, or a finding that stands while the textbook story of it doesn't. "
            f"Yellow is contested, red failed or was retracted, and grey has never been directly tested. "
            f"<bookmark mark='b'/> Across the series, {held} rows held, about {round(100 * held / d['total'])} "
            f"percent, and {c['replicated, smaller']} of those are smaller than first reported. Sixty-four are "
            f"contested, forty-two failed, and four were retracted."
        ) as vo:
            self.play(FadeIn(head), FadeIn(key))
            vo.wait_until("a")
            self.play(FadeIn(names), FadeIn(ns), LaggedStart(*[FadeIn(b, shift=UP * 0.1) for b in bars_],
                                                               lag_ratio=0.02), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.wait(1.0)
        self.clear_scene()

    def pattern(self):
        rows_section(self, r"The pattern", [
            (r"what held best: \ the senses, \ learning and the machinery of thought (Acts III to V): \ effects "
             r"measured many times, \ in many people, \ with strong manipulations", GOOD),
            (r"what was contested or failed most: \ social, \ clinical, \ methodological and applied claims (Acts IX to XII): \ small "
             r"samples, \ subtle manipulations, \ outcomes far from the manipulation", AUTH),
            (r"the frontier is mostly open: \ its rows are young, \ and many are untested", GREY_B),
            (r"the date on every row: \ the Ledger is a record of a moment, \ to be checked again", YOU),
        ], "What's the pattern? <bookmark mark='a'/> What held best: the senses, learning and the machinery of "
           "thought, Acts Three to Five. Those effects were measured many times, in many people, with strong "
           "manipulations. <bookmark mark='b'/> What was contested or failed most: social, clinical, methodological and applied claims, in "
           "Acts Nine to Twelve, with small samples, subtle manipulations, and outcomes far from the "
           "manipulation. <bookmark mark='c'/> The frontier is mostly open. Its rows are young, and many are "
           "untested. <bookmark mark='d'/> And there's a date on every row. The Ledger is a record of a moment, to "
           "be checked again.")

    def decades(self):
        d = load("decades")
        tab = np.asarray(d["table"], float)
        frac = tab / tab.sum(1, keepdims=True)
        head = heading(r"By when the original study appeared")
        cols = [GOOD, PERSON, AUTH, GREY_B]
        W, H = 0.9, 3.4
        x0, y0 = -5.4, -1.7
        bars_ = VGroup()
        for i in range(len(d["labels"])):
            base = 0.0
            for j in range(4):
                h = float(frac[i, j]) * H
                if h > 0:
                    bars_.add(Rectangle(width=W, height=h, stroke_width=0, fill_color=cols[j], fill_opacity=0.9)
                              .move_to([x0 + i * 1.1, y0 + base + h / 2, 0]))
                base += h
        names = VGroup(*[wrapped_label(t, 1.05, 12, GREY_A).move_to([x0 + i * 1.1, y0 - 0.35, 0])
                         for i, t in enumerate(d["labels"])])
        ns = VGroup(*[label(f"{int(t)}", font_size=13, color=GREY_B).move_to([x0 + i * 1.1, y0 + H + 0.2, 0])
                      for i, t in enumerate(tab.sum(1))])
        held = frac[:, 0]
        rows = rows_of([
            (r"the same rows, \ sorted by the year of the original study; \ green held, \ gold contested, \ red "
             r"failed or retracted, \ grey untested", WHITE),
            (rf"before 1950, \ {100 * held[0]:.0f}\% held; \ since 2010, \ {100 * held[-1]:.0f}\%, \ with "
             rf"{100 * frac[-1, 1]:.0f}\% still contested", AUTH),
            (r"partly survivorship: \ old findings that failed were dropped from courses long ago, \ so a course "
             r"teaches the old ones that survived", MODEL),
            (r"partly time: \ a recent finding has not yet had its large replication; \ many gold bars will turn "
             r"green or red", PERSON),
            (r"and partly method: \ small samples and flexible analyses were at their height around 2010 (Part 4)",
             YOU),
        ], 5.6, 18, 0.32).move_to([3.6, -0.2, 0])
        with self.voiceover(
            "Here are the same rows sorted another way. <bookmark mark='a'/> By the year the original study "
            "appeared. Green held, gold is contested, red failed or was retracted, and grey is untested. "
            "<bookmark mark='b'/> Before nineteen fifty, ninety-six percent held. Since twenty ten, forty-two percent, "
            "with thirty-seven percent still contested. <bookmark mark='c'/> Part of that is survivorship. Old "
            "findings that failed were dropped from courses long ago, so a course teaches the old ones that survived. "
            "<bookmark mark='d'/> Part is time. A recent finding hasn't yet had its large replication, and many gold "
            "bars will turn green or red. <bookmark mark='e'/> And part is method. Small samples and flexible "
            "analyses were at their height around twenty ten, as Part 4 showed."
        ) as vo:
            self.play(FadeIn(head), FadeIn(names), FadeIn(ns))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), LaggedStart(*[FadeIn(b) for b in bars_], lag_ratio=0.05), run_time=2)
            for m, r in zip("bcde", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
