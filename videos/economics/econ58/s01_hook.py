from __future__ import annotations

from videos.economics.econ58.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.sentence()
        self.question()
        self.title()
        self.objectives()

    def sentence(self):
        F = tables.FLOOD_1936
        card_ = history_card(1936, r"the Flood Control Act, \ section 1", r"the Federal Government should improve or "
                             r"participate in the improvement of navigable waters \ldots\ for flood-control purposes "
                             r"\textbf{if the benefits to whomsoever they may accrue are in excess of the estimated "
                             r"costs}, \ and if the lives and social security of people are otherwise adversely "
                             r"affected", color=E.ACCENT, width=11.6, font_size=24)
        card_.to_edge(UP, buff=0.5)
        who = label(r"to whomsoever they may accrue", font_size=34, color=E.ACCENT).next_to(card_, DOWN, buff=0.55)
        sides = VGroup(label(r"benefits", font_size=30, color=BEN), label(r"$>$", font_size=34),
                       label(r"costs", font_size=30, color=COST)).arrange(RIGHT, buff=0.4).next_to(who, DOWN,
                                                                                                    buff=0.45)
        tag = published_tag(F.tag, corner=DL, font_size=12)
        dup = history_card(1844, r"Jules Dupuit, \ engineer of bridges and roads", r"`On the measurement of the "
                           r"utility of public works': \ a bridge is worth not the tolls it collects \ but what its "
                           r"users would pay over and above them", color=TRAV, width=7.6, font_size=21)
        dup.to_edge(UP, buff=0.5)
        st = strait(width=9.0, height=2.3).next_to(dup, DOWN, buff=0.5)
        with self.voiceover(
            "In June 1936, after a spring of floods, Congress passed a Flood Control Act with a sentence that changed "
            "how governments decide. <bookmark mark='a'/> The federal government should take part in flood control, "
            "it said, if the benefits, to whomsoever they may accrue, are in excess of the estimated costs. "
            "<bookmark mark='b'/> To whomsoever they may accrue: not only to the government that pays, but to "
            "everyone. <bookmark mark='c'/> From then on the Army's engineers had to put a number on both sides of "
            "that inequality, for every dam and levee they proposed. <bookmark mark='d'/> The idea was older. In "
            "1844 Jules Dupuit, an engineer of the French bridges and roads service, asked what a bridge is worth, "
            "and answered: not the tolls it collects, but what its users would be willing to pay over and above "
            "them. <bookmark mark='e'/> The Island has a case. Bo's ferry carries people across the strait to the "
            "north shore; the ministry is asked to build a bridge. Cost-benefit analysis is what ninety years of "
            "producing those two numbers has become, and this part does it, for the bridge and then for a law."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(card_, shift=UP * 0.1), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(who, shift=UP * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(sides, shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeOut(card_), FadeOut(who), FadeOut(sides), FadeOut(tag))
            self.play(FadeIn(dup, shift=UP * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(VGroup(*[m for m in st if m not in (st.deck, st.piers, st.ferry, st.route)])),
                      run_time=1.2)
            self.play(Create(st.route), FadeIn(st.ferry))
            self.play(st.ferry.animate.move_to(st.route.get_end() + LEFT * 0.5 + UP * 0.05), run_time=3.0)
            self.play(Create(st.deck), FadeIn(st.piers), run_time=1.5)
        self.wait(0.5)
        self.clear_scene()

    def question(self):
        q = wrapped_label(ASK, 12.0, 34, E.ACCENT).to_edge(UP, buff=0.8)
        rows = VGroup(
            label(r"whose gains count, \ and against what would have happened anyway?", font_size=26, color=BEN),
            label(r"how do you price time, \ quiet, \ a beach, \ or a life?", font_size=26, color=SAFE),
            label(r"how much is a benefit in fifty years worth today?", font_size=26, color=RATE),
            label(r"what will a law cost, \ once people respond to it?", font_size=26, color=BEHAV),
            label(r"and how far can the forecasts behind it be trusted?", font_size=26, color=COST),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(q, DOWN, buff=0.6)
        with self.voiceover(
            "The question: how does a government decide whether a project or a law is worth it? <bookmark mark='a'/> "
            "Whose gains count, and against what would have happened anyway? <bookmark mark='b'/> How do you price "
            "time, quiet, a beach, or a life? <bookmark mark='c'/> How much is a benefit in fifty years worth today? "
            "<bookmark mark='d'/> What will a law cost, once people respond to it? <bookmark mark='e'/> And how far "
            "can the forecasts behind all of it be trusted?"
        ) as vo:
            self.play(FadeIn(q, shift=DOWN * 0.2))
            for mk, r_ in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
        self.clear_scene()

    def title(self):
        F = load("film")
        mini = plane([1984, 2026], [-16, 4], x_length=4.2, y_length=1.5)
        logo = VGroup(*[path(mini, b["fy"], b["v"], CBO, 1.0, smooth=False).set_stroke(opacity=0.5)
                        for b in F["baselines"][::3]])
        logo.add(path(mini, F["actual_fy"], F["actual"], WHITE, 2.4, smooth=False))
        tt = label(r"Economics, Built", font_size=60)
        sub = label(r"Part 58 \ $\cdot$ \ Scoring the Bill", font_size=34, color=E.ACCENT)
        VGroup(logo, tt, sub).arrange(DOWN, buff=0.45)
        with self.voiceover("Economics, Built. Part fifty-eight: scoring the bill."):
            self.play(LaggedStart(*[Create(m) for m in logo], lag_ratio=0.1), run_time=1.8)
            self.play(Write(tt), run_time=1.2)
            self.play(FadeIn(sub, shift=UP * 0.15))
        self.wait(1.0)
        self.clear_scene()

    def objectives(self):
        head = label(r"Act XI \ $\cdot$ \ Economics at Work", font_size=40, color=E.ACCENT)
        obj = objectives_card([
            r"the steps of a cost-benefit analysis: \ standing, \ the counterfactual, \ surplus, \ shadow prices",
            r"valuing time, \ noise, \ a beach and a statistical life, \ and what can bias each",
            r"discounting: \ the Treasury's rate, \ OMB's rates, \ and why long horizons need lower ones",
            r"scoring a bill: \ static, \ behavioural and dynamic scores, \ microsimulation, \ general equilibrium",
            r"optimism bias, \ reference classes, \ regulatory analysis, \ and what targets do to numbers",
        ], color=E.ACCENT, font_size=28, width=13.0)
        with self.voiceover(
            "Part fifty-seven read the economy as it is. This part prices a change to it. By the end you will know "
            "<bookmark mark='a'/> the steps of a cost-benefit analysis, from whose gains count to the shadow price of "
            "a worker's time; <bookmark mark='b'/> how time, noise, a beach and a statistical life are valued, and "
            "what can bias each number; <bookmark mark='c'/> how the future is discounted, and why the rate is "
            "argued over; <bookmark mark='d'/> how a bill is scored, statically, with behaviour and dynamically, "
            "with microsimulation and general equilibrium; <bookmark mark='e'/> and why forecasts of cost run "
            "optimistic, how rules are appraised, and what targets do to the numbers they target."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(head), FadeIn(obj.head), FadeIn(obj.rows[0], shift=RIGHT * 0.2))
            for mk, r_ in zip("bcde", obj.rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
        self.clear_scene()
