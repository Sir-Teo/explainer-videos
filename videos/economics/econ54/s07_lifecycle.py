from __future__ import annotations

from videos.economics.econ54.common import *  # noqa: F403


class LifeCycle(VoiceoverScene):
    def construct(self):
        card(self, 6, r"The Island's households, estimated", r"Can simulated moments find the truth we planted?",
             "Chapter six. The Island's households, estimated.", lit={2002: r"Gourinchas and Parker"},
             scale=("household",), horizon=("a century",))
        self.setup_()
        self.profiles()
        self.results()

    def setup_(self):
        L = load("lifecycle")
        rows = VGroup(
            label(r"Part 22's household: \ work from 20 to 59 on a risky income, \ then a pension to 69", font_size=22,
                  color=WHITE),
            label(r"each age: \ choose consumption, \ save the rest at 3\%, \ never borrow", font_size=22,
                  color=GREY_A),
            label(r"hidden: \ patience $\beta$ \ and \ caution $\gamma$", font_size=22, color=MODEL),
            label(rf"the data: \ {L['n']:,} households' consumption at ten ages, \ wealth at six: \ 16 moments",
                  font_size=22, color=DATA),
            label(rf"each guess: \ solve the model backwards, \ simulate {L['S']} populations, \ compare", font_size=22,
                  color=EST),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.36).move_to(UP * 0.2)
        tag = published_tag(r"Gourinchas and Parker, \ Econometrica 70(1) (2002)", corner=DR, font_size=12)
        hc = history_card(2002, r"Pierre-Olivier Gourinchas and Jonathan Parker", r"``Consumption over the life "
                          r"cycle'': \ patience and caution, \ estimated from the shape of spending by age",
                          color=EST, width=10.0, font_size=24).move_to(UP * 0.4)
        with self.voiceover(
            "Now a full example, done the way Pierre-Olivier Gourinchas and Jonathan Parker did it for American "
            "households in 2002, but on the Island, where we planted the answer. <bookmark mark='a'/> The household "
            "is Part twenty-two's: it works from twenty to fifty-nine on a risky income, then lives on a pension "
            "to sixty-nine. <bookmark mark='b'/> Each year it chooses how much to consume, saves the rest at three "
            "percent, and cannot borrow. <bookmark mark='c'/> Two numbers are hidden: patience and caution. "
            f"<bookmark mark='d'/> The data are {L['n']:,} households' average consumption at ten ages and their "
            "wealth at six: sixteen moments. <bookmark mark='e'/> For each guess at the two numbers, the computer "
            f"solves the household's problem backwards from the last year, simulates {L['S']} populations with "
            "fixed draws, and compares their moments with the data's."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.1), FadeIn(tag))
            for mk, r_ in zip("abcde", rows):
                vo.wait_until(mk)
                if mk == "a":
                    self.play(FadeOut(hc))
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
        self.clear_scene()

    def profiles(self):
        L = load("lifecycle")
        ages = np.array(L["ages"])
        d = np.array(L["data"])
        f = np.array(L["fitted"])
        axc = plane([20, 70], [0.9, 1.45], center=LEFT * 3.4 + DOWN * 0.4, x_length=5.6, y_length=4.2,
                    xticks=[20, 30, 40, 50, 60, 70], yticks=[1.0, 1.1, 1.2, 1.3, 1.4], xlabel=r"age",
                    ylabel=r"consumption", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.1f}", font_size=13)
        axw = plane([20, 70], [0, 4.5], center=RIGHT * 3.3 + DOWN * 0.4, x_length=5.6, y_length=4.2,
                    xticks=[20, 30, 40, 50, 60, 70], yticks=[0, 1, 2, 3, 4], xlabel=r"age", ylabel=r"wealth",
                    xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=13)
        dc = VGroup(*[dot(axc, a, v, DATA, 0.08) for a, v in zip(ages, d[:10])])
        dw = VGroup(*[dot(axw, a, v, DATA, 0.08) for a, v in zip(ages[4:], d[10:])])
        fc = path(axc, ages, f[:10], MODEL, 2.6, smooth=False)
        fw = path(axw, ages[4:], f[10:], MODEL, 2.6, smooth=False)
        ret_c = vline(axc, 60, 0.9, 1.45, GREY_C, 1.2)
        ret_w = vline(axw, 60, 0, 4.5, GREY_C, 1.2)
        key = VGroup(label(r"blue: \ the Island's data", font_size=18, color=DATA),
                     label(r"purple: \ the model at the estimates", font_size=18, color=MODEL),
                     label(r"dashed: \ retirement", font_size=18, color=GREY_C)).arrange(RIGHT, buff=0.6).to_edge(
            UP, buff=0.45)
        tag = island_tag(r"simulated: \ the Island's households", corner=DR, font_size=13)
        with self.voiceover(
            "Here is what is being matched. <bookmark mark='a'/> On the left, consumption by age: it rises through "
            "the working years as incomes grow and the households build a buffer, peaks in the late thirties, and "
            "falls as the impatient households spend down. <bookmark mark='b'/> On the right, wealth: almost "
            "nothing at forty, a hump that peaks just before retirement, then run down through the pension years. "
            "<bookmark mark='c'/> The purple lines are the model at the estimated values. They pass through "
            "every point: sixteen facts matched with two numbers."
        ) as vo:
            self.play(FadeIn(axc), FadeIn(axw), FadeIn(key), Create(ret_c), Create(ret_w), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p_, scale=0.5) for p_ in dc], lag_ratio=0.1))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(p_, scale=0.5) for p_ in dw], lag_ratio=0.1))
            vo.wait_until("c")
            self.play(Create(fc), Create(fw), run_time=2.0)
        self.clear_scene()

    def results(self):
        L = load("lifecycle")
        th, se, tr = L["theta"], L["se"], L["truth"]
        rows = VGroup(
            VGroup(label(r"", font_size=20), label(r"start", font_size=20, color=GREY_A),
                   label(r"truth", font_size=20, color=TRUTHC), label(r"estimate", font_size=20, color=EST),
                   label(r"standard error", font_size=20, color=THEORY)),
            VGroup(label(r"patience, \ $\beta$", font_size=21, color=PATIENCE),
                   label(f"{L['start'][0]:.2f}", font_size=21, color=GREY_A),
                   label(f"{tr[0]:.3f}", font_size=21, color=TRUTHC), label(f"{th[0]:.4f}", font_size=21, color=EST),
                   label(f"{se[0]:.4f}", font_size=21, color=THEORY)),
            VGroup(label(r"caution, \ $\gamma$", font_size=21, color=CAUTION),
                   label(f"{L['start'][1]:.1f}", font_size=21, color=GREY_A),
                   label(f"{tr[1]:.2f}", font_size=21, color=TRUTHC), label(f"{th[1]:.3f}", font_size=21, color=EST),
                   label(f"{se[1]:.3f}", font_size=21, color=THEORY)),
        )
        grid = VGroup(*[c for r in rows for c in r]).arrange_in_grid(rows=3, cols=5, buff=(0.7, 0.35),
                                                                      col_alignments="lcccc").move_to(UP * 1.6)
        notes = VGroup(
            label(rf"{L['evals']} guesses, \ each a solved and simulated economy", font_size=21, color=GREY_A),
            label(rf"$J = {L['J']:.1f}$ \ on {L['df']} degrees of freedom: \ the model fits \ (p = {L['p_J']:.2f})",
                  font_size=21, color=GAIN),
            label(rf"the two estimates' correlation: \ {L['corr']:.4f}".replace("-", "{-}"), font_size=21,
                  color=E.ACCENT),
            label(r"the data pin down a line in the plane, \ and the curvature of the profiles a point on it",
                  font_size=21, color=WHITE),
        ).arrange(DOWN, buff=0.3).next_to(grid, DOWN, buff=0.6)
        with self.voiceover(
            f"The search started far away, at patience {L['start'][0]:.2f} and caution {L['start'][1]:.0f}. "
            f"<bookmark mark='a'/> After {L['evals']} guesses, each one a solved and simulated economy, it "
            f"stopped at patience {th[0]:.4f} and caution {th[1]:.2f}, against {tr[0]:.2f} and {tr[1]:.0f} planted: "
            "each within about one and a quarter standard errors of the truth. <bookmark mark='b'/> The J "
            f"statistic, {L['J']:.1f} on {L['df']} degrees of freedom, says the model fits, as it should: it is "
            "the model that made the data. <bookmark mark='c'/> And here is the warning from the Play it, in one "
            f"number. The two estimates' correlation is {say_num(L['corr'], 4)}. <bookmark mark='d'/> The sixteen "
            "facts pin down a line of patience-and-caution pairs very precisely; what picks a point on the line is "
            "the subtle curvature of the profiles. With real data, where the model is never exactly right, that "
            "is a thin thread to hang a number on."
        ) as vo:
            self.play(FadeIn(VGroup(*rows[0])), FadeIn(rows[1][:3]), FadeIn(rows[2][:3]))
            vo.wait_until("a")
            self.play(FadeIn(rows[1][3:]), FadeIn(rows[2][3:]), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(notes[3]))
        self.clear_scene()
