from __future__ import annotations

from videos.economics.econ30.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        card(self, 15, r"In practice: \ policy simulations at central banks", r"How do central bank staff use these "
             r"three equations?", "Chapter fifteen. In practice: policy simulations at central banks.",
             lit={2002: r"Bernanke on deflation"}, scale=("nation",), horizon=("a quarter", "three years"))
        self.hump_fact()
        self.staff()
        self.called()

    def hump_fact(self):
        H = load("hybrid")
        f = next(x for x in facts.FACTS if x.key == "hump")
        data_m = label(r"after a tightening, \\ output falls for a year \\ or more \ (Part 31)", font_size=18,
                       color=WHITE)
        theory_m = label(r"habits, \ indexation \\ and gradual policy \\ spread the effect out", font_size=18,
                         color=OUTPUT)
        agora_m = label(rf"the Island: \ the trough \\ moves from impact \\ to {H['rich']['peak_x']} quarters later",
                        font_size=18, color=E.AGORA)
        fc = fact_card(tex_safe(f.statement), columns=((r"the data", data_m), (r"the theory", theory_m),
                                                         (r"Agora", agora_m)), width=12.4, font_size=22,
                       colors=(WHITE, OUTPUT, None)).move_to(UP * 0.3)
        tag = published_tag(r"Christiano, \ Eichenbaum and Evans (1999, 2005); \ the Island", corner=DR, font_size=12)
        with self.voiceover(
            "One of the series' facts gets its theory here. <bookmark mark='a'/> In the data, as Part thirty-one "
            "will measure, output's response to a monetary tightening is hump-shaped and peaks after a year or "
            "more. <bookmark mark='b'/> The theory: habits, indexation and gradual policy spread the effect out "
            "over time. <bookmark mark='c'/> On the Island, adding them moves the trough from the moment of the "
            f"shock to {H['rich']['peak_x']} quarters later: in the right direction, though still sooner than in the "
            "data."
        ) as vo:
            self.play(FadeIn(fc.card), FadeIn(fc[1][0]), *[FadeIn(c[:2]) for c in fc.cols], FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(fc.cols[0][2:]))
            vo.wait_until("b")
            self.play(FadeIn(fc.cols[1][2:]))
            vo.wait_until("c")
            self.play(FadeIn(fc.cols[2][2:]))
        self.clear_scene()

    def staff(self):
        rows = VGroup(
            label(r"what the staff do with the model", font_size=27, color=E.ACCENT),
            label(r"scenarios: \ what if oil prices jump? \ what if the natural rate is lower than we think?",
                  font_size=22, color=COST),
            label(r"alternative paths for the policy rate: \ faster, \ slower, \ a rule, \ the optimum",
                  font_size=22, color=CB),
            label(r"story-telling: \ which shocks explain this year's forecast errors?", font_size=22, color=OUTPUT),
            label(r"alongside, \ never instead of, \ judgement and simpler forecasting models", font_size=22,
                  color=GREY_A),
            label(r"the model's job: \ make the story add up, \ and make the assumptions explicit", font_size=23,
                  color=E.ACCENT),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.1)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Inside a central bank, the staff use these models in a few standard ways. <bookmark mark='a'/> "
            "Scenarios: what happens if oil prices jump, or if the natural rate is lower than we think? "
            "<bookmark mark='b'/> Alternative paths for the policy rate: faster, slower, following a rule, or "
            "chosen to minimize the loss. <bookmark mark='c'/> And story-telling: which shocks explain this year's "
            "forecast errors? <bookmark mark='d'/> Always alongside judgement and simpler forecasting models, "
            "never instead of them. <bookmark mark='e'/> The model's real job is to make the story add up, and to "
            "make every assumption visible."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def called(self):
        c = calls.CALLS["bernanke_2002"]
        K = load("called")
        cc = call_card(tex_safe(c.who), c.when, tex_safe(c.said), tex_safe(c.outcome), c.verdict, width=12.4,
                       font_size=17).to_edge(UP, buff=0.3)
        ax = plane([2006, 2020], [-3, 6], center=DOWN * 1.75 + LEFT * 1.3, x_length=9.0, y_length=3.0,
                   xticks=[2008, 2012, 2016, 2020], yticks=[-2, 0, 2, 4], xlabel=r"",
                   ylabel=r"change over twelve months, \ \%", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:.0f}", font_size=14)
        zlb = shade(ax, [(2008.96, 2015.96)], -3, 6, color=RATE, opacity=0.10)
        zero = seg(ax, 2006, 0, 2020, 0, GREY_C, 1.2)
        target = seg(ax, 2006, 2, 2020, 2, CB, 1.6, dashed=True)
        cpi = path(ax, K["cpi"]["t"], K["cpi"]["yoy"], INFL, 2.6, smooth=False)
        core = path(ax, K["core"]["t"], K["core"]["yoy"], PRICE, 3.2, smooth=False)
        key = VGroup(label(r"red: \ consumer prices", font_size=16, color=INFL),
                     label(r"gold: \ core PCE prices", font_size=16, color=PRICE),
                     label(r"dashed: \ the 2\% target \ (from 2012)", font_size=16, color=CB),
                     label(r"shaded: \ the rate at zero", font_size=16, color=RATE)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.22).next_to(ax, RIGHT, buff=0.4)
        tag = published_tag(r"Bernanke, \ remarks before the National Economists Club, \ 21 November 2002; \ BLS, "
                            r"\ BEA and the Federal Reserve via FRED", corner=DR, font_size=12)
        with self.voiceover(
            "And a forecast about the zero bound. Called it? <bookmark mark='a'/> In November 2002, Ben Bernanke, "
            "then a governor of the Federal Reserve, said that the central bank, with the rest of the government, "
            "had enough instruments to make sure that any deflation in America would be mild and brief. "
            "<bookmark mark='b'/> Six years later the federal funds rate hit zero and stayed there for seven years. "
            "<bookmark mark='d'/> Consumer prices fell over twelve months in 2009 and briefly in 2015, by at most "
            "two percent, <bookmark mark='e'/> while core inflation never went below zero. "
            "<bookmark mark='f'/> But core inflation also stayed below the two percent target "
            "most of the following decade. <bookmark mark='c'/> Right, about deflation."
        ) as vo:
            self.play(FadeIn(cc.card), FadeIn(cc[1]), FadeIn(tag), FadeIn(ax), FadeIn(zero))
            vo.wait_until("b")
            self.play(Indicate(cc.right, color=WHITE, scale_factor=1.01), FadeIn(zlb), FadeIn(key[3]))
            vo.wait_until("d")
            self.play(Create(cpi), FadeIn(key[0]), run_time=1.5)
            vo.wait_until("e")
            self.play(Create(core), FadeIn(key[1]), run_time=1.5)
            vo.wait_until("f")
            self.play(Create(target), FadeIn(key[2]))
            vo.wait_until("c")
            self.play(FadeIn(cc.stamp, scale=1.3))
        self.clear_scene()
