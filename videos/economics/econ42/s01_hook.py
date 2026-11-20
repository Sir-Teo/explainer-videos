from __future__ import annotations

from videos.economics.econ42.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.draw()
        self.experiment()
        self.question()
        self.title()
        self.objectives()

    def draw(self):
        O = tables.OREGON_2008.data
        rng = np.random.default_rng(42)
        n, cols = 900, 45
        dots = VGroup(*[Dot(radius=0.055, color=GREY_D) for _ in range(n)])
        dots.arrange_in_grid(rows=n // cols, cols=cols, buff=0.11).move_to(LEFT * 1.7 + DOWN * 0.25)
        order = rng.permutation(n)
        drawn = order[: n * O["drawn"] // O["signups"]]
        enrolled = drawn[: n * O["places"] // O["signups"]]
        batches = np.array_split(drawn, 7)
        side = VGroup(
            label(rf"Oregon, \ 2008: \\ about {O['signups']:,} people \\ on the list", font_size=20, color=WHITE),
            label(r"each dot: \ 100 people", font_size=17, color=GREY_A),
            label(rf"about {O['drawn']:,} names \\ drawn by lottery, \\ March to September", font_size=20,
                  color=LOTTO),
            label(rf"about {O['places']:,} places \\ in Medicaid", font_size=20, color=GAIN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        month = label(r"March", font_size=22, color=LOTTO).next_to(dots, UP, buff=0.2)
        tag = published_tag(r"NBER, \ the Oregon Health Insurance Experiment; \ Oregon's Medicaid Advisory "
                            r"Committee, \ March 2008", corner=DR, font_size=10)
        with self.voiceover(
            "In early 2008 the state of Oregon had money to add about ten thousand low-income adults to its "
            "Medicaid programme, which pays for health care. About ninety thousand people put their names on the "
            "list. <bookmark mark='a'/> Each dot here stands for a hundred of them. <bookmark mark='b'/> The state "
            "could not take everyone, so it held a lottery: between March and September 2008 it drew about thirty "
            "thousand names, month by month. <bookmark mark='c'/> Those drawn could apply, and about ten thousand "
            "places were filled."
        ) as vo:
            self.play(FadeIn(dots, lag_ratio=0.001), FadeIn(side[0]), FadeIn(tag), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(side[1]), Indicate(dots[0], scale_factor=3))
            vo.wait_until("b")
            self.play(FadeIn(side[2]), FadeIn(month))
            for k, (bt, mo) in enumerate(zip(batches, ("March", "April", "May", "June", "July", "August",
                                                     "September"))):
                new = label(mo, font_size=22, color=LOTTO).move_to(month)
                self.play(*[dots[int(i)].animate.set_color(LOTTO).scale(1.25) for i in bt],
                          Transform(month, new), run_time=0.9)
            vo.wait_until("c")
            self.play(*[dots[int(i)].animate.set_color(GAIN) for i in enrolled], FadeIn(side[3]), FadeOut(month),
                      run_time=1.5)
        self.clear_scene()

    def experiment(self):
        cards = point_cards([
            (r"a lottery", r"winners and losers \\ alike in every way \\ but one", LOTTO),
            (r"a first", r"the first randomized \\ study of insuring \\ the uninsured in \\ the United States",
             UNEMP),
            (r"three questions", r"what does insurance \\ do to health, \ to \\ money, \ to peace \\ of mind?",
             HEALTH),
            (r"chapter 7", r"what it found, \\ and what it could \\ not find", GAIN),
        ], width=12.8, cols=4, font_size=19).move_to(DOWN * 0.1)
        head = label(r"a natural experiment, \ by design", font_size=28, color=E.ACCENT).to_edge(UP, buff=0.6)
        tag = published_tag(tables.OREGON_2008.tag, corner=DR, font_size=10)
        with self.voiceover(
            "For economists, the lottery was something rare. <bookmark mark='a'/> Because the names were drawn at "
            "random, winners and losers were alike in every way but one: the chance to be covered. "
            "<bookmark mark='b'/> It made the first randomized study of what happens when the uninsured in the "
            "United States get insurance. <bookmark mark='c'/> Comparing winners with losers would show what "
            "insurance does to health, to money, and to peace of mind. <bookmark mark='d'/> Chapter seven gives "
            "the answers, and what the study could not tell."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(cards.cards[0], shift=UP * 0.1))
            for mk, c in zip("bcd", cards.cards[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()

    def question(self):
        q = wrapped_label(ASK, 12.0, 38, E.ACCENT).to_edge(UP, buff=0.8)
        rows = VGroup(
            label(r"why do private markets underinsure, \ and what can the state pool?", font_size=26, color=RISK),
            label(r"how generous should unemployment benefits be, \ and how do we measure both sides?",
                  font_size=26, color=UNEMP),
            label(r"what does health insurance do, \ to spending and to health?", font_size=26, color=HEALTH),
            label(r"pensions, \ defaults, \ disability, \ the working poor: \ how do we compare them?",
                  font_size=26, color=PENSION),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42).next_to(q, DOWN, buff=0.6)
        note_ = label(r"education, \ not advice: \ this part describes how economists study insurance, \ not "
                      r"what anyone should buy", font_size=18, color=GREY_B).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "This part asks what the state should insure, and how generously. <bookmark mark='a'/> Why do private "
            "markets leave some risks uninsured, and what can a government pool that a company cannot? "
            "<bookmark mark='b'/> How generous should unemployment benefits be, and how can we measure both what "
            "they give and what they cost? <bookmark mark='c'/> What does health insurance do, to spending and to "
            "health? <bookmark mark='d'/> And how can programmes as different as pensions, disability insurance and "
            "help for the working poor be compared on one scale? A note before we start: this part is about how "
            "economists study insurance, not advice about anyone's own coverage."
        ) as vo:
            self.play(FadeIn(q, shift=DOWN * 0.2), FadeIn(rows[0], shift=RIGHT * 0.2))
            for mk, r_ in zip("bcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
            self.play(FadeIn(note_))
        self.clear_scene()

    def title(self):
        F = load("film")
        mini = plane([1967, 2027], [0, 1], x_length=4.2, y_length=1.4)
        v = np.log(np.array(F["v"]))
        v = (v - v.min()) / (v.max() - v.min())
        logo = path(mini, F["t"], v, UNEMP, 2.6, smooth=False)
        tt = label(r"Economics, Built", font_size=60)
        sub = label(r"Part 42 \ $\cdot$ \ Social Insurance", font_size=34, color=E.ACCENT)
        VGroup(logo, tt, sub).arrange(DOWN, buff=0.45)
        with self.voiceover("Economics, Built. Part forty-two: social insurance."):
            self.play(Create(logo), run_time=1.6)
            self.play(Write(tt), run_time=1.2)
            self.play(FadeIn(sub, shift=UP * 0.15))
        self.wait(1.0)
        self.clear_scene()

    def objectives(self):
        head = label(r"Act VIII \ $\cdot$ \ Work and the State", font_size=40, color=E.ACCENT)
        obj = objectives_card([
            r"why markets underinsure; \ a game; \ the optimal benefit derived",
            r"measuring both sides; \ moral hazard or liquidity; \ health insurance and Oregon",
            r"pensions; \ defaults; \ disability insurance",
            r"help for the working poor; \ a basic income; \ one yardstick",
            r"three dials; \ actuaries and evaluators; \ the frontier",
        ], color=E.ACCENT, font_size=31, width=13.0)
        with self.voiceover(
            "Here is the plan. <bookmark mark='a'/> Why markets underinsure, a game, and the formula for the best "
            "unemployment benefit, derived. <bookmark mark='b'/> How economists measure both sides of that formula, "
            "whether benefits work through moral hazard or through cash in hand, then health insurance and "
            "Oregon's answers. <bookmark mark='c'/> Pensions, defaults and disability insurance. "
            "<bookmark mark='d'/> Help for the working poor, the case for and against a basic income, and one "
            "yardstick for every programme. <bookmark mark='e'/> Three dials, the people who do this work, and the "
            "frontier."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(head), FadeIn(obj.head), FadeIn(obj.rows[0], shift=RIGHT * 0.2))
            for mk, r_ in zip("bcde", obj.rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
        self.clear_scene()
