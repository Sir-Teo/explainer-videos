from __future__ import annotations

from videos.economics.econ15.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.fable()
        self.contracts()
        self.today()
        self.question()
        self.title()
        self.objectives()

    def fable(self):
        hc = history_card(1952, r"James Meade, \ the Economic Journal", r"an orchard and a beekeeper: \ the textbook "
                          r"example of a benefit no market can price", color=DEMAND, width=11.4, font_size=24
                          ).to_edge(UP, buff=0.45)
        q = quote_card(r"``the apple-farmer cannot charge the bee-keeper for the bees' food''", r"James Meade, 1952",
                       width=10.4, font_size=26, color=DEMAND).next_to(hc, DOWN, buff=0.5)
        rows = VGroup(
            label(r"more apples feed more bees; \ more bees pollinate more apples", font_size=24, color=GOOD),
            label(r"neither pays the other, \ so each produces too little", font_size=24, color=SOCIAL),
            label(r"for twenty years the fable stood for a failure of the market", font_size=24, color=GREY_A),
        ).arrange(DOWN, buff=0.3).next_to(q, DOWN, buff=0.45)
        tag = published_tag(r"Meade, Economic Journal 62(245) (1952)", corner=DR, font_size=13)
        with self.voiceover(
            "In 1952 the economist James Meade needed an example of a benefit that no market could price, and "
            "chose an orchard and a beekeeper. <bookmark mark='a'/> The apple farmer, Meade wrote, cannot charge the "
            "beekeeper for the bees' food. <bookmark mark='b'/> More apple trees feed more bees, and more bees "
            "pollinate more apples. <bookmark mark='c'/> But neither pays the other, so each produces too little "
            "of what helps the other. <bookmark mark='d'/> For twenty years the apples and the bees were the "
            "textbook's picture of a market that fails."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.2), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(q, shift=UP * 0.1))
            for mk, r in zip("bcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def contracts(self):
        b = load("bees")
        hc = history_card(1972, r"Steven Cheung, \ Washington State", r"asking the beekeepers what they are paid",
                          color=GOOD, width=11.0, font_size=24).to_edge(UP, buff=0.45)
        rows = VGroup(
            label(r"nine beekeepers, \ about 10,000 hives, \ trucked from farm to farm", font_size=24),
            label(r"orchards pay the beekeepers to bring their hives: \ a pollination fee", font_size=24,
                  color=GOOD),
            label(r"for honey crops like mint, \ the beekeepers pay the farmers: \ an apiary rent", font_size=24,
                  color=DEMAND),
            label(r"and apple blossom, \ it turns out, \ gives the bees little honey at all", font_size=24,
                  color=GREY_A),
            label(r"the market the textbooks said couldn't exist \ had been running for decades", font_size=26,
                  color=E.ACCENT),
        ).arrange(DOWN, buff=0.36).next_to(hc, DOWN, buff=0.5)
        tag = published_tag(r"Cheung, JLE 16(1) (1973)", corner=DR, font_size=13)
        with self.voiceover(
            "In the spring of 1972 the economist Steven Cheung went to Washington State, one of the largest "
            "apple-growing regions, and asked the beekeepers what they were paid. <bookmark mark='a'/> Cheung talked to "
            "nine of them, with some ten thousand hives between them, trucked from farm to farm through the season. "
            "<bookmark mark='b'/> Orchards paid the beekeepers to bring their hives at blossom time: a pollination "
            "fee. <bookmark mark='c'/> For crops rich in nectar that need no pollinating, like mint, it went the other "
            "way: the beekeepers paid the farmers for the right to set their hives down. <bookmark mark='d'/> And apple blossom, it "
            "turned out, gives the bees little honey at all. <bookmark mark='e'/> The market the textbooks said "
            "could not exist had been running for decades. Cheung called the paper the fable of the bees."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.2), FadeIn(tag))
            for mk, r in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def today(self):
        rows = point_cards([
            (r"a kiln's smoke", r"over a neighbour's \\ drying fish", SMOKE),
            (r"a car at rush hour", r"slows every \\ car behind it", ROAD),
            (r"a power station", r"acid rain, \\ far downwind", SOCIAL),
            (r"a vaccination", r"protects the \\ unvaccinated too", GOOD),
            (r"a discovery", r"others build on it \\ for free", POT),
            (r"a fishing boat", r"leaves fewer fish \\ for every other", FISH),
        ], width=12.6, cols=3, font_size=22).move_to(DOWN * 0.3)
        head = label(r"my choice lands on you, \ and nobody pays", font_size=32, color=E.ACCENT).to_edge(UP,
                                                                                                    buff=0.5)
        with self.voiceover(
            "The bees are the gentle case. <bookmark mark='a'/> A kiln's smoke drifts over a neighbour's drying "
            "fish. A car at rush hour slows every car behind it. A power station's sulphur falls as acid rain "
            "hundreds of miles away. A vaccination protects the people around you as well as you. A discovery is "
            "built on by others, for free. And a fishing boat leaves fewer fish for every other boat. "
            "<bookmark mark='b'/> In every case a choice lands on someone else, and no price passes between them. "
            "Economists call these externalities, or spillovers."
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
            label(r"how much damage is too much, \ and is the right amount zero?", font_size=29, color=SOCIAL),
            label(r"should the state tax the damage, \ or let the people involved bargain?", font_size=29,
                  color=DEMAND),
            label(r"who pays for what everyone shares, \ and who looks after the commons?", font_size=29,
                  color=POT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(q, DOWN, buff=0.7)
        with self.voiceover(
            "Part fourteen was about two people and a contract. This part is about everyone outside the contract. "
            "What happens when my choice lands on you, and nobody pays? <bookmark mark='a'/> How much damage is too "
            "much, and is the right amount zero? <bookmark mark='b'/> Should the state tax the damage, or let the "
            "people involved bargain it away? <bookmark mark='c'/> And who pays for what everyone shares, and who "
            "looks after what nobody owns?"
        ) as vo:
            self.play(FadeIn(q, shift=DOWN * 0.2))
            for mk, r in zip("abc", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.2))
        self.clear_scene()

    def title(self):
        logo = pair(height=1.0)
        t = label(r"Economics, Built", font_size=60)
        sub = label(r"Part 15 \ $\cdot$ \ Spillovers", font_size=34, color=E.ACCENT)
        VGroup(logo, t, sub).arrange(DOWN, buff=0.45)
        with self.voiceover("Economics, Built. Part fifteen: spillovers."):
            self.play(FadeIn(logo, shift=UP * 0.2), run_time=1.2)
            self.play(Write(t), run_time=1.2)
            self.play(FadeIn(sub, shift=UP * 0.15))
        self.wait(1.0)
        self.clear_scene()

    def objectives(self):
        head = label(r"Act IV \ $\cdot$ \ Failure and Design", font_size=40, color=E.ACCENT)
        obj = objectives_card([
            r"play the shared pot; \ the wedge between private and social cost; \ Pigou's tax",
            r"Coase's bargain, \ and the beekeepers who proved it; \ public goods and the lighthouse",
            r"free riding in the laboratory; \ the commons from Gordon and Hardin to Ostrom",
            r"permits and the acid-rain market; \ prices or quantities; \ congestion and the toll",
            r"networks and ideas; \ a dial for roads; \ measuring the damage",
        ], color=E.ACCENT, font_size=31, width=13.0)
        with self.voiceover(
            "This part continues Act Four. <bookmark mark='a'/> You'll play a game of the shared pot, then meet the "
            "wedge between private and social cost, and Pigou's tax. <bookmark mark='b'/> Coase's bargain, and the "
            "beekeepers who proved it; public goods, and the lighthouse. <bookmark mark='c'/> Free riding measured "
            "in the laboratory, and the commons, from Gordon and Hardin to Elinor Ostrom. "
            "<bookmark mark='d'/> Permits and the acid-rain market; whether to set a price or a quantity; congestion "
            "and the toll. <bookmark mark='e'/> And networks and ideas, a dial for roads, and a frontier on "
            "measuring the damage."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(head), FadeIn(obj.head), FadeIn(obj.rows[0], shift=RIGHT * 0.2))
            for mk, r in zip("bcde", obj.rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.2))
        self.clear_scene()
