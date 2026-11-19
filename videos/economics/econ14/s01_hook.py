from __future__ import annotations

from videos.economics.econ14.common import *  # noqa: F403


def thumbprints(n=18, cols=6, color=CHINA):
    dots = VGroup()
    for k in range(n):
        d = Ellipse(width=0.42, height=0.55, stroke_width=0, fill_color=color, fill_opacity=0.75)
        ring = Ellipse(width=0.3, height=0.4, stroke_color=BACKGROUND, stroke_width=1.5, fill_opacity=0)
        dots.add(VGroup(d, ring).rotate(0.15 * ((k % 3) - 1)))
    dots.arrange_in_grid(rows=(n + cols - 1) // cols, cols=cols, buff=0.22)
    return dots


class Hook(VoiceoverScene):
    def construct(self):
        self.commune()
        self.contract()
        self.today()
        self.question()
        self.title()
        self.objectives()

    def commune(self):
        hc = history_card(1978, r"Xiaogang, \ Anhui province", r"a poor village in a commune: \ the land worked together, "
                          r"\\ the harvest shared out by work points", color=CHINA, width=11.4, font_size=24
                          ).to_edge(UP, buff=0.45)
        rows = VGroup(
            label(r"eighteen households share whatever the fields produce", font_size=25),
            label(r"a family that works harder adds to the harvest \ but gets about one eighteenth of what it adds",
                  font_size=24, color=TEAM),
            label(r"so nobody works much harder than anyone else, \ and the village goes hungry", font_size=24,
                  color=GREY_A),
            label(r"economists call it the free-rider problem of a team", font_size=25, color=E.ACCENT),
        ).arrange(DOWN, buff=0.34).next_to(hc, DOWN, buff=0.55)
        with self.voiceover(
            "In 1978 Xiaogang was a poor village in Anhui province, in eastern China, part of a people's commune. Its "
            "fields were worked together, and the harvest was shared out by work points. <bookmark mark='a'/> Some "
            "eighteen households shared whatever the land produced. <bookmark mark='b'/> A family that worked harder "
            "added to the harvest, but received only about an eighteenth of what it added. "
            "<bookmark mark='c'/> So nobody had much reason to work harder than anyone else, and in bad years the "
            "village went hungry. <bookmark mark='d'/> Economists call this the free-rider problem of a team."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.2))
            for mk, r in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def contract(self):
        prints = thumbprints().move_to(LEFT * 3.6 + DOWN * 0.2)
        side = VGroup(
            label(r"late in 1978, \ eighteen farmers meet in secret", font_size=23),
            label(r"they divide the fields among the families: \\ each delivers its quota to the state, \\ and keeps "
                  r"the rest", font_size=23, color=EFFORT),
            label(r"if the leaders are jailed for it, \\ the others will raise their children", font_size=23,
                  color=RISK),
            label(r"each family now keeps all of what it adds: \\ the next harvest is far larger", font_size=23,
                  color=PAY),
            label(r"within a few years, \ the ``household responsibility system'' \\ spreads across rural China",
                  font_size=23, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.4)
        note_ = label(r"accounts of the 1979 harvest differ in their numbers; \ all agree it was far larger", font_size=15,
                      color=GREY_B).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Late in 1978, eighteen farmers of Xiaogang met in secret and signed a contract with their thumbprints. "
            "<bookmark mark='a'/> They would divide the fields among the families. Each family would deliver its "
            "quota of grain to the state, and keep everything above it. <bookmark mark='b'/> It was illegal, and they "
            "knew it: if the leaders were jailed, the contract said, the others would raise their children. "
            "<bookmark mark='c'/> Now each family kept all of what it added. The next harvest was far larger than "
            "anything the village had produced before; accounts differ on the numbers, but not on that. "
            "<bookmark mark='d'/> Within a few years the household responsibility system, as it came to be called, "
            "spread across rural China."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(p, scale=1.3) for p in prints], lag_ratio=0.12), FadeIn(side[0]),
                      run_time=3)
            for mk, r in zip("abcd", side[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
            self.play(FadeIn(note_))
        self.clear_scene()

    def today(self):
        rows = point_cards([
            (r"a sales team", r"how hard did \\ each one sell?", PAY),
            (r"a chief executive", r"skill, \ or a \\ rising market?", SIGNAL),
            (r"a teacher", r"what was learnt, \\ beyond the test?", EFFORT),
            (r"a tenant farmer", r"good land, \\ or hard work?", CHINA),
            (r"a contractor", r"cut corners \\ you can't see?", RISK),
            (r"a machine-learning model", r"the score, \ or \\ the goal?", TEAM),
        ], width=12.6, cols=3, font_size=22).move_to(DOWN * 0.3)
        head = label(r"you see the result, \ not the effort", font_size=32, color=E.ACCENT).to_edge(UP, buff=0.5)
        with self.voiceover(
            "Xiaogang's problem is everywhere work is done for someone else. <bookmark mark='a'/> A sales manager sees "
            "a team's sales, not how hard each person tried. A board sees a company's profits, but not whether they "
            "came from skill or a rising market. A head teacher sees test scores, not what else was learnt. A "
            "landlord sees the harvest, not whether the tenant worked hard or the weather was kind. A client can't "
            "see the corners a contractor cut. And even a machine-learning model, trained to raise a score, may raise "
            "the score without reaching the goal. <bookmark mark='b'/> In every case you see the result, not the "
            "effort."
        ) as vo:
            self.play(FadeIn(head, shift=DOWN * 0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in rows.cards], lag_ratio=0.5), run_time=6)
            vo.wait_until("b")
            self.play(Indicate(head, color=WHITE))
        self.clear_scene()

    def question(self):
        q = wrapped_label(ASK, 12.0, 40, E.ACCENT).to_edge(UP, buff=0.8)
        rows = VGroup(
            label(r"how much should pay depend on results, \ when results are partly luck?", font_size=29, color=PAY),
            label(r"what should pay depend on, \ and what happens to what it ignores?", font_size=29, color=SIGNAL),
            label(r"when do incentives work, \ and when do they backfire?", font_size=29, color=RISK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(q, DOWN, buff=0.7)
        with self.voiceover(
            "Part thirteen was about what people know. This part is about what they do. How do you get someone to "
            "work for you, when you can't see what they do? <bookmark mark='a'/> How much should pay depend on "
            "results, when results are partly luck? <bookmark mark='b'/> What should pay depend on, and what happens "
            "to everything it ignores? <bookmark mark='c'/> And when do incentives work, and when do they backfire?"
        ) as vo:
            self.play(FadeIn(q, shift=DOWN * 0.2))
            for mk, r in zip("abc", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.2))
        self.clear_scene()

    def title(self):
        logo = pair(height=1.0)
        t = label(r"Economics, Built", font_size=60)
        sub = label(r"Part 14 \ $\cdot$ \ Incentives", font_size=34, color=E.ACCENT)
        VGroup(logo, t, sub).arrange(DOWN, buff=0.45)
        with self.voiceover("Economics, Built. Part fourteen: incentives."):
            self.play(FadeIn(logo, shift=UP * 0.2), run_time=1.2)
            self.play(Write(t), run_time=1.2)
            self.play(FadeIn(sub, shift=UP * 0.15))
        self.wait(1.0)
        self.clear_scene()

    def objectives(self):
        head = label(r"Act IV \ $\cdot$ \ Failure and Design", font_size=40, color=E.ACCENT)
        obj = objectives_card([
            r"write a contract for Friday; \ teams and free riders; \ the principal--agent model",
            r"insurance against incentives: \ the optimal share in one formula; \ pay on what's informative",
            r"piece rates at Safelite; \ multitasking and teaching to the test; \ tournaments and careers",
            r"efficiency wages and Ford's five dollars; \ sharecropping and China's reform",
            r"when incentives backfire; \ a dial for piece rates; \ relational contracts, \ and incentives for "
            r"machines",
        ], color=E.ACCENT, font_size=31, width=13.0)
        with self.voiceover(
            "This part continues Act Four. <bookmark mark='a'/> You'll write a contract for Friday, and we'll use it "
            "to meet teams and free riders, and the principal-agent model. <bookmark mark='b'/> The trade-off between "
            "insurance and incentives, solved in one formula, and why pay should depend on everything informative, "
            "and nothing else. <bookmark mark='c'/> Piece rates at a windscreen company; multitasking and teaching to "
            "the test; tournaments and careers. <bookmark mark='d'/> Efficiency wages and Henry Ford's five dollars a "
            "day; sharecropping, and China's reform measured. <bookmark mark='e'/> And when incentives backfire, a "
            "dial for piece rates, and a frontier on relational contracts and incentives for machines."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(head), FadeIn(obj.head), FadeIn(obj.rows[0], shift=RIGHT * 0.2))
            for mk, r in zip("bcde", obj.rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.2))
        self.clear_scene()
