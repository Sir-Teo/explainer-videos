from __future__ import annotations

from videos.economics.econ31.common import *  # noqa: F403


class Methods(VoiceoverScene):
    def construct(self):
        card(self, 5, r"Four answers, \ scored against the truth", r"Which ways of measuring a policy shock get it "
             r"right?", "Chapter five. Four answers, scored against the truth.",
             lit={1989: r"Romer and Romer", 1999: r"Christiano, \ Eichenbaum and Evans",
                  2018: r"Nakamura and Steinsson"}, scale=("nation",), horizon=("a quarter", "four years"))
        self.four()
        self.vars()
        self.clean()
        self.info()

    def four(self):
        cards = point_cards([
            (r"recursive VARs", r"the shock: \ what recent data \\ cannot explain \ (Sims; \ Christiano, \\ "
                                r"Eichenbaum and Evans, \ 1999)", METHOD["var"]),
            (r"narrative shocks", r"read the bank's own forecasts; \\ the shock: \ what they cannot \\ explain "
                                  r"\ (Romer and Romer, \ 1989, \ 2004)", METHOD["narrative"]),
            (r"high-frequency surprises", r"the move in futures prices \\ in a narrow window around \\ an "
                                          r"announcement \ (Kuttner, \ 2001; \\ Gertler and Karadi, \ 2015)",
             METHOD["hf_clean"]),
            (r"the information effect", r"an announcement also reveals \\ what the bank knows \\ (Nakamura and "
                                        r"Steinsson, \ 2018)", METHOD["hf_info"]),
        ], width=12.8, cols=2, font_size=21).move_to(DOWN * 0.2)
        head = label(r"four ways to find the part of a rate move that is the bank's own", font_size=26,
                     color=E.ACCENT).to_edge(UP, buff=0.5)
        tag = published_tag(r"Christiano, \ Eichenbaum and Evans, \ \emph{Handbook of Macroeconomics} 1A (1999); \ "
                            r"Romer and Romer, \ \emph{NBER Macro Annual} (1989), \ \emph{AER} 94(4) (2004); \ "
                            r"Kuttner, \ \emph{JME} 47(3) (2001); \ Gertler and Karadi, \ \emph{AEJ: Macro} 7(1) "
                            r"(2015); \ Nakamura and Steinsson, \ \emph{QJE} 133(3) (2018)", corner=DR, font_size=11)
        with self.voiceover(
            "Economists have found four main ways to isolate the part of a rate move that is the bank's own. "
            "<bookmark mark='a'/> Recursive VARs, which you just saw: assume the bank reacts to this month's data "
            "but the economy does not react to the bank within the month, and call what the data cannot explain a "
            "shock. Lawrence Christiano, Martin Eichenbaum and Charles Evans set out the standard version in 1999. "
            "<bookmark mark='b'/> Narrative shocks: Christina and David Romer read the Federal Reserve's own "
            "forecasts, in the staff's Greenbook, and took as the shock the part of each decision those forecasts "
            "cannot explain. <bookmark mark='c'/> High-frequency surprises: futures markets price the expected "
            "rate, so the move in futures prices in a narrow window around an announcement is what the market did not "
            "expect: a day for Kenneth Kuttner in 2001, half an hour for Mark Gertler and Peter Karadi, who used "
            "such surprises as instruments in 2015. <bookmark mark='d'/> And a warning from Emi Nakamura and "
            "Jón Steinsson: an "
            "announcement also tells markets what the bank knows about the economy, so a surprise is not purely "
            "the bank's own choice."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()

    def _panels(self):
        M = load("mc")
        h = np.array(M["h"])
        axy = plane([0, 16], [-0.6, 1.1], center=LEFT * 3.3 + DOWN * 0.5, x_length=5.6, y_length=4.4,
                    xticks=[0, 4, 8, 12, 16], yticks=[-0.5, 0, 0.5, 1.0], xlabel=r"quarters after the shock",
                    ylabel=r"output gap, \ \%", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:+.1f}" if v else "0",
                    font_size=14)
        axp = plane([0, 16], [-0.6, 1.1], center=RIGHT * 3.3 + DOWN * 0.5, x_length=5.6, y_length=4.4,
                    xticks=[0, 4, 8, 12, 16], yticks=[-0.5, 0, 0.5, 1.0], xlabel=r"quarters after the shock",
                    ylabel=r"inflation, \ points", xfmt=lambda v: f"{v:.0f}",
                    yfmt=lambda v: f"{v:+.1f}" if v else "0", font_size=14)
        zeros = VGroup(seg(axy, 0, 0, 16, 0, GREY_D, 1.2), seg(axp, 0, 0, 16, 0, GREY_D, 1.2))
        truth = VGroup(DashedVMobject(path(axy, h, M["truth"]["y"], TRUTH_C, 3), num_dashes=30),
                       DashedVMobject(path(axp, h, M["truth"]["pi"], TRUTH_C, 3), num_dashes=30))

        def lines(m, width=3.2):
            v = M["methods"][m]
            return VGroup(path(axy, h, np.clip(v["y"]["mean"], -0.6, 1.1), METHOD[m], width),
                          path(axp, h, np.clip(v["pi"]["mean"], -0.6, 1.1), METHOD[m], width))
        return M, h, axy, axp, zeros, truth, lines

    def vars(self):
        M, h, axy, axp, zeros, truth, lines = self._panels()
        head = label(rf"the Island, \ {M['reps']} histories of {M['T'] // 4} years: \ the average answer of each "
                     r"method", font_size=21, color=E.ACCENT).to_edge(UP, buff=0.35)
        key = VGroup(label(r"white, \ dashed: \ the truth", font_size=17, color=TRUTH_C),
                     label(r"grey: \ the naive regression", font_size=17, color=METHOD["naive"]),
                     label(r"blue: \ recursive VAR", font_size=17, color=METHOD["var"]),
                     label(r"light blue: \ VAR with a commodity-price proxy", font_size=17, color=METHOD["var_news"]),
                     ).arrange(RIGHT, buff=0.4).next_to(head, DOWN, buff=0.2)
        if key.width > 13.2:
            key.width = 13.2
        nv, va, vn = lines("naive", 2.4), lines("var"), lines("var_news")
        P = M["peaks"]
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            f"Now run all of them on the Island: {M['reps']} histories of {M['T'] // 4} years each, about as long "
            "as America's postwar record, and average what each method finds. <bookmark mark='a'/> The truth, "
            "white and dashed: after a one-point policy shock, output falls by "
            f"{abs(P['truth']['y']['value']):.1f} percent at the trough, three quarters later, and inflation falls "
            "slowly. <bookmark mark='b'/> The naive regression gets even the sign wrong, for both. "
            "<bookmark mark='c'/> The recursive VAR does better, but output first rises, and inflation rises "
            f"{M['methods']['var']['pi']['mean'][2]:.2f} points: the Island has a price puzzle too, because the bank "
            "acts on news the VAR cannot see. <bookmark mark='d'/> Add a noisy proxy for the bank's news about "
            "costs, as Sims added commodity prices, and the price puzzle shrinks, but output's response is still "
            "wrong at first, because nothing in the VAR proxies for the demand news."
        ) as vo:
            self.play(FadeIn(axy), FadeIn(axp), FadeIn(zeros), FadeIn(head), FadeIn(tag), run_time=0.6)
            vo.wait_until("a")
            self.play(Create(truth), FadeIn(key[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(nv), FadeIn(key[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(nv.animate.set_stroke(opacity=0.3), Create(va), FadeIn(key[2]), run_time=1.5)
            vo.wait_until("d")
            self.play(va.animate.set_stroke(opacity=0.35), Create(vn), FadeIn(key[3]), run_time=1.5)
        self.clear_scene()

    def clean(self):
        M, h, axy, axp, zeros, truth, lines = self._panels()
        head = label(r"narrative shocks and clean surprises", font_size=22, color=E.ACCENT).to_edge(UP, buff=0.35)
        key = VGroup(label(r"white, \ dashed: \ the truth", font_size=17, color=TRUTH_C),
                     label(r"gold: \ narrative", font_size=17, color=METHOD["narrative"]),
                     label(r"green: \ high-frequency surprises", font_size=17, color=METHOD["hf_clean"]),
                     label(r"shaded: \ 90\% of single histories \ (narrative)", font_size=17, color=GREY_B),
                     ).arrange(RIGHT, buff=0.4).next_to(head, DOWN, buff=0.2)
        if key.width > 13.2:
            key.width = 13.2
        v = M["methods"]["narrative"]
        bands = VGroup(band(axy, h, np.clip(v["y"]["lo"], -0.6, 1.1), np.clip(v["y"]["hi"], -0.6, 1.1),
                            METHOD["narrative"], 0.12),
                       band(axp, h, np.clip(v["pi"]["lo"], -0.6, 1.1), np.clip(v["pi"]["hi"], -0.6, 1.1),
                            METHOD["narrative"], 0.12))
        na, hc = lines("narrative"), lines("hf_clean")
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "<bookmark mark='a'/> Narrative shocks, in gold. On the Island the bank's forecasts include its news, "
            "so the part of each decision they cannot explain is almost exactly the planted shock: the correlation "
            f"is {M['narrative_corr']:.2f}. The average response lies on the truth. <bookmark mark='b'/> "
            "High-frequency surprises, in green, when the announcement carries no news about the economy: also on "
            "the truth. <bookmark mark='c'/> But averages over three hundred histories are a luxury. The shaded "
            "band holds ninety percent of what one sixty-year history gives with the narrative method: wide enough "
            "to include no effect at all on inflation. America has only one history."
        ) as vo:
            self.play(FadeIn(axy), FadeIn(axp), FadeIn(zeros), FadeIn(head), FadeIn(truth), FadeIn(key[0]),
                      FadeIn(tag), run_time=0.6)
            vo.wait_until("a")
            self.play(Create(na), FadeIn(key[1]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(hc), FadeIn(key[2]), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(bands), FadeIn(key[3]))
        self.clear_scene()

    def info(self):
        M, h, axy, axp, zeros, truth, lines = self._panels()
        head = label(r"the information effect", font_size=22, color=E.ACCENT).to_edge(UP, buff=0.35)
        key = VGroup(label(r"white, \ dashed: \ the truth", font_size=17, color=TRUTH_C),
                     label(r"green: \ clean surprises", font_size=17, color=METHOD["hf_clean"]),
                     label(r"red: \ surprises that also reveal the bank's news about demand", font_size=17,
                           color=METHOD["hf_info"])).arrange(RIGHT, buff=0.4).next_to(head, DOWN, buff=0.2)
        if key.width > 13.2:
            key.width = 13.2
        hc, hi = lines("hf_clean"), lines("hf_info")
        P = M["peaks"]["hf_info"]
        foot = label(rf"output's trough: \ {P['y']['value']:+.2f}\% \ against the truth's "
                     rf"{M['peaks']['truth']['y']['value']:+.2f}\%; \ in the first quarter, \ "
                     rf"{P['y_1']:+.2f}\%", font_size=20, color=METHOD["hf_info"]).to_edge(DOWN, buff=0.35)
        tag = published_tag(r"Nakamura and Steinsson, \ \emph{QJE} 133(3) (2018); \ the Island", corner=DR,
                            font_size=12)
        with self.voiceover(
            "Now suppose that when the bank raises its rate, markets also learn that it sees strong demand ahead, "
            "and that the surprise carries, along with the shock, "
            f"{100 * island.truths(31)['mc']['info']:.0f} percent of the bank's reaction to its demand news. "
            "<bookmark mark='a'/> The clean surprises, in green, as before. "
            "<bookmark mark='b'/> The contaminated ones, in red: output seems to rise in the first quarter, and its "
            "fall is about half the truth. Inflation's fall is halved as well. <bookmark mark='c'/> A tightening "
            "that reveals good news about the economy looks less contractionary than it is. Nakamura and Steinsson "
            "found this pattern in American data: after surprise tightenings, forecasters revised up their "
            "forecasts of output growth. Separating the bank's choice from the bank's information is still the "
            "frontier of this literature."
        ) as vo:
            self.play(FadeIn(axy), FadeIn(axp), FadeIn(zeros), FadeIn(head), FadeIn(truth), FadeIn(key[0]),
                      FadeIn(tag), run_time=0.6)
            vo.wait_until("a")
            self.play(Create(hc), FadeIn(key[1]), run_time=1.5)
            vo.wait_until("b")
            self.play(hc.animate.set_stroke(opacity=0.35), Create(hi), FadeIn(key[2]), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()
