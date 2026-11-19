from __future__ import annotations

from videos.economics.econ17.common import *  # noqa: F403


class Lottery(VoiceoverScene):
    def construct(self):
        card(self, 12, r"What a lottery reveals", r"If a match breaks ties by lottery, \ can it tell us whether a "
             r"school is any good?", "Chapter twelve. What a lottery reveals.",
             lit={2017: r"Abdulkadiroğlu, Angrist, Narita and Pathak"}, scale=("person", "city"),
             horizon=("a year",))
        self.problem()
        self.agora()
        self.spread()
        self.denver()

    def problem(self):
        rows = VGroup(
            label(r"do pupils at a sought-after school do better because of the school, \ or because of who applies?",
                  font_size=23, color=E.ACCENT),
            label(r"comparing its pupils with everyone else mixes the two", font_size=23, color=REJECT),
            label(r"but when a school is oversubscribed, \ a match gives out its places partly by lottery",
                  font_size=23, color=HELD),
            label(r"among applicants of the same type, \ who wins is chance: \ an experiment, \ built into the "
                  r"market", font_size=23, color=STABLE),
            label(r"the catch: \ the chance of an offer differs by type \ (siblings first, \ say), \ so compare "
                  r"within types", font_size=22, color=GREY_A),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.1)
        with self.voiceover(
            "The match has one more gift, for researchers. <bookmark mark='a'/> Do pupils at a sought-after school "
            "do better because of the school, or because of who chooses to apply to it? "
            "<bookmark mark='b'/> Comparing its pupils with everyone else mixes the two up. "
            "<bookmark mark='c'/> But when a school has more applicants than places, the match gives out its places "
            "partly by lottery. <bookmark mark='d'/> Among applicants of the same type, who wins is pure chance: a "
            "randomized experiment, built into the market. <bookmark mark='e'/> The catch is that the chance of an "
            "offer differs by type. Siblings of current pupils may come first, for example. So the comparison must "
            "be made within types."
        ) as vo:
            self.play(FadeIn(rows[0]))
            for mk, r in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def agora(self):
        lt = load("lottery")
        names = [r"its pupils against \\ everyone else", r"offered against not, \\ ignoring type",
                 r"offered against not, \\ within type"]
        vals = lt["mean"]
        cols = [REJECT, HELD, STABLE]
        ax = plane([-0.6, 2.6], [-0.1, 1.0], center=LEFT * 2.3 + DOWN * 0.4, x_length=7.0, y_length=4.6, xticks=[],
                   yticks=[0, 0.2, 0.4, 0.6, 0.8, 1.0], ylabel=r"estimated effect of the school", font_size=16,
                   yfmt=lambda v: f"{v:.1f}")
        a = ax.ax
        truth = VGroup(DashedLine(a.c2p(-0.6, lt["effect"]), a.c2p(2.6, lt["effect"]), color=WHITE,
                                  stroke_width=2),
                       label(rf"the truth Agora planted: \ {lt['effect']:.1f}", font_size=17).next_to(
                           a.c2p(2.6, lt["effect"]), UP, buff=0.08).shift(LEFT * 1.2))
        bars, labs, nums = VGroup(), VGroup(), VGroup()
        for i, (v, c, nm) in enumerate(zip(vals, cols, names)):
            lo, hi = a.c2p(i - 0.3, min(0, v)), a.c2p(i + 0.3, max(0, v))
            r = Rectangle(width=hi[0] - lo[0], height=max(hi[1] - lo[1], 0.03), stroke_width=0, fill_color=c,
                          fill_opacity=0.85).move_to((lo + hi) / 2)
            bars.add(r)
            labs.add(label(nm, font_size=16, color=GREY_A).next_to(a.c2p(i, -0.1), DOWN, buff=0.12))
            nums.add(label(rf"{v:.2f}", font_size=20, color=c).next_to(r, UP, buff=0.08))
        side = VGroup(
            label(rf"{lt['reps']} lotteries in a district \\ of {TRUTH_STUDENTS:,} pupils".replace(",", "{,}"),
                  font_size=20, color=GREY_A),
            label(r"stronger pupils apply more; \\ siblings, \ weaker on average, \\ get places first", font_size=20,
                  color=GREY_A),
            label(r"its pupils: \ twice the truth", font_size=21, color=REJECT),
            label(r"ignoring type: \ almost nothing", font_size=21, color=HELD),
            label(r"within type: \ the truth", font_size=22, color=STABLE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        tag = agora_tag(corner=DR, font_size=15)
        with self.voiceover(
            "Agora can show the catch. It builds a district with one oversubscribed school, which raises every "
            "pupil's score by four tenths of a standard deviation. <bookmark mark='a'/> Stronger pupils are more "
            "likely to apply, and siblings of current pupils, who are weaker on average, get places first; the rest "
            "are drawn by lottery. Agora runs two hundred such lotteries. <bookmark mark='b'/> Comparing the "
            "school's pupils with everyone else gives about eight tenths: twice the truth, because of who applies. "
            "<bookmark mark='c'/> Comparing applicants who were offered a place with those who were not, ignoring "
            "type, gives almost nothing, because the offered are mostly the weaker siblings. "
            "<bookmark mark='d'/> Comparing within type, and scaling up for the pupils who enrol anyway, gives "
            "four tenths, the truth."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(labs), FadeIn(truth), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(FadeIn(side[1]))
            for mk, i in zip("bcd", range(3)):
                vo.wait_until(mk)
                self.play(GrowFromEdge(bars[i], DOWN), FadeIn(nums[i]), FadeIn(side[2 + i]))
        self.clear_scene()

    def spread(self):
        lt = load("lottery")
        d1, d0 = np.array(lt["draws"]), np.array(lt["draws_nc"])
        edges = np.linspace(-0.15, 0.6, 31)
        h1, _ = np.histogram(d1, edges)
        h0, _ = np.histogram(d0, edges)
        top = max(h1.max(), h0.max()) * 1.15
        ax = plane([-0.15, 0.6], [0, top], center=LEFT * 1.4 + DOWN * 0.3, x_length=8.6, y_length=4.6,
                   xticks=[-0.1, 0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6], yticks=[], xlabel=r"estimate, \ lottery by lottery",
                   font_size=16, xfmt=lambda v: f"{v:g}")
        a = ax.ax

        def hist(h, c):
            g = VGroup()
            for i, k in enumerate(h):
                if k == 0:
                    continue
                lo, hi = a.c2p(edges[i], 0), a.c2p(edges[i + 1], k)
                g.add(Rectangle(width=hi[0] - lo[0], height=hi[1] - lo[1], stroke_width=0.5, stroke_color=BACKGROUND,
                                fill_color=c, fill_opacity=0.75).move_to((lo + hi) / 2))
            return g

        g0, g1 = hist(h0, HELD), hist(h1, STABLE)
        tline = DashedLine(a.c2p(lt["effect"], 0), a.c2p(lt["effect"], top), color=WHITE, stroke_width=2)
        side = VGroup(
            label(r"ignoring type", font_size=21, color=HELD),
            label(r"within type", font_size=21, color=STABLE),
            label(rf"within type: \ mean {lt['mean'][2]:.2f}, \\ spread {lt['sd'][2]:.2f}", font_size=20,
                  color=STABLE),
            label(r"one lottery can miss; \\ the method doesn't", font_size=21, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        tag = agora_tag(corner=DR, font_size=15)
        with self.voiceover(
            "Here are all two hundred estimates. <bookmark mark='a'/> Ignoring type, they pile up near zero, far "
            "from the truth. <bookmark mark='b'/> Within type, they centre on four tenths. "
            "<bookmark mark='c'/> Any one lottery can miss by a few hundredths, but the method is right on average, "
            "which is what a randomized experiment promises."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tline), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(r, DOWN) for r in g0], lag_ratio=0.05), FadeIn(side[0]), run_time=2)
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(r, DOWN) for r in g1], lag_ratio=0.05), FadeIn(side[1]),
                      FadeIn(side[2]), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def denver(self):
        d = load("schools")["denver"]
        st = study_card(r"Denver's charter schools, through the city's match", r"Abdulkadiroğlu, Angrist, Narita and "
                        r"Pathak (2017)",
                        [(r"varied", r"a charter school offer from the city's deferred-acceptance match, with lottery "
                                     r"tie-breaks"),
                         (r"method", r"compare offered and not offered within each applicant type, using the chance "
                                     r"of an offer the match implies"),
                         (r"found", rf"attending raised math scores by {d['math'][0]:.2f} standard deviations "
                                    rf"(s.e. {d['math'][1]:.3f}), reading by {d['reading'][0]:.2f}, writing by "
                                    rf"{d['writing'][0]:.2f}"),
                         (r"without", rf"ignoring the chance of an offer: math {d['math_no_score_controls'][0]:.2f}, "
                                      r"too small by about half")],
                        design="IV", width=12.0, font_size=21).move_to(UP * 0.3)
        foot = label(r"the match that assigns the places is also the experiment that evaluates them",
                     font_size=24, color=E.ACCENT).to_edge(DOWN, buff=0.6)
        tag = published_tag(r"Abdulkadiroğlu, Angrist, Narita and Pathak, Econometrica 85(5) (2017), Table 6",
                            corner=DR, font_size=12)
        with self.voiceover(
            "Real cities do this. <bookmark mark='a'/> Denver assigns its school places, charter schools included, "
            "through one deferred-acceptance match with lottery tie-breaks. Atila Abdulkadiroğlu, Joshua Angrist, "
            "Yusuke Narita and Parag Pathak worked out each applicant's chance of a charter offer from the match's "
            "own rules, and compared applicants with the same chance. <bookmark mark='b'/> Attending a charter "
            "school raised math scores by about four tenths of a standard deviation, a very large effect, and "
            "reading and writing by less. <bookmark mark='c'/> Ignoring the chance of an offer, as in Agora's middle "
            "bar, gave an estimate too small by about half. <bookmark mark='d'/> The match that assigns the places "
            "is also the experiment that evaluates them."
        ) as vo:
            self.play(FadeIn(st), FadeIn(tag))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()


TRUTH_STUDENTS = island.truths(17)["lottery"]["students"]
