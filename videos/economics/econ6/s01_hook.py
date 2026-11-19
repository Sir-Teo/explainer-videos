from __future__ import annotations

from videos.economics.econ6.common import *  # noqa: F403


def voucher_glyph(scale: float = 1.0, color=GIFF, text: str | None = None, font_size=30, sub: str | None = None) -> VGroup:
    """A grain voucher with a perforated edge: the part's emblem."""
    w, h = 3.2 * scale, 1.5 * scale
    body = RoundedRectangle(width=w, height=h, corner_radius=0.12 * scale, stroke_color=color, stroke_width=4,
                            fill_color=color, fill_opacity=0.08)
    perf = DashedLine(body.get_corner(UL) + RIGHT * 0.75 * scale + DOWN * 0.08 * scale,
                      body.get_corner(DL) + RIGHT * 0.75 * scale + UP * 0.08 * scale, color=color, stroke_width=2.5,
                      dash_length=0.08 * scale)
    stub = Text("¥", font_size=40 * scale, color=color, weight=BOLD).move_to(body.get_left() + RIGHT * 0.38 * scale)
    g = VGroup(body, perf, stub)
    if text is not None:
        t = VGroup(label(text, font_size=font_size * scale, color=WHITE))
        if sub:
            t.add(label(sub, font_size=0.62 * font_size * scale, color=GREY_A))
        t.arrange(DOWN, buff=0.08 * scale).move_to(body.get_center() + RIGHT * 0.38 * scale)
        g.add(t)
    g.body, g.perf, g.stub = body, perf, stub
    return g


class Hook(VoiceoverScene):
    def construct(self):
        self.vouchers()
        self.result()
        self.rumour()
        self.slutsky()
        self.question()
        self.title()
        self.objectives()

    def vouchers(self):
        t = tables.JENSEN_MILLER_2008.data["design"]
        head = label(r"Hunan and Gansu, \ China, \ 2006", font_size=36, color=GIFF).to_edge(UP, buff=0.5)
        cards = VGroup(*[voucher_glyph(1.0, text=rf"{c:.2f} yuan off", sub=r"each jin of the staple", font_size=30)
                         for c in t["cuts_yuan_per_jin"]]).arrange(DOWN, buff=0.35).to_edge(LEFT, buff=0.7).shift(
            DOWN * 0.35)
        facts = VGroup(
            label(rf"{t['households']:,} of the poorest urban households".replace(",", "{,}"), font_size=32),
            label(rf"in {t['counties']} county towns: \\ {t['per_province']} in Hunan (rice), \ {t['per_province']} "
                  r"in Gansu (wheat flour)", font_size=27, color=GREY_A),
            label(rf"rice cost {t['rice_price_hunan']:.2f} yuan a jin (500 g): \\ the vouchers cut it by up to a "
                  r"quarter", font_size=29, color=COCO),
            label(r"a control group got none; \ each household's voucher \\ was drawn at random, \ June to October",
                  font_size=27, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42).next_to(cards, RIGHT, buff=0.7)
        tag = published_tag(r"Jensen and Miller, AER (2008)", corner=DR, font_size=15)
        with self.voiceover(
            "In the spring of 2006, two economists, Robert Jensen and Nolan Miller, went looking for some of the "
            "poorest households in China. <bookmark mark='a'/> They found thirteen hundred of them, on the lists of "
            "the urban poor in eleven county towns, half in Hunan in the south, where people live on rice, and half "
            "in Gansu in the north, where they live on wheat. <bookmark mark='b'/> For five months, some of those "
            "households received vouchers, drawn at random, worth ten, twenty or thirty fen off every jin of their "
            "staple, half a kilogram. Rice cost one yuan twenty a jin, so the biggest voucher cut its price by a "
            "quarter. <bookmark mark='c'/> A control group got nothing. It's a clean experiment: the price of one "
            "food falls, for some households and not others, and nothing else changes."
        ) as vo:
            self.play(FadeIn(head, shift=DOWN * 0.2), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(facts[0]), FadeIn(facts[1]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.2) for c in cards], lag_ratio=0.3), FadeIn(facts[2]))
            vo.wait_until("c")
            self.play(FadeIn(facts[3]))
        self.clear_scene()

    def result(self):
        h = tables.JENSEN_MILLER_2008.data["hunan"]
        q = label(r"cheaper rice: \ did they eat more rice?", font_size=36).to_edge(UP, buff=0.6)
        expect = VGroup(label(r"what any textbook predicts", font_size=30, color=GREY_A),
                        label(r"price $\downarrow$ \quad $\Rightarrow$ \quad rice $\uparrow$", font_size=48,
                              color=IC)).arrange(DOWN, buff=0.3)
        found = VGroup(label(r"what Hunan's poor-but-not-poorest households did", font_size=30, color=GREY_A),
                       label(r"price $\downarrow$ \quad $\Rightarrow$ \quad rice $\downarrow$", font_size=48,
                             color=GIFF)).arrange(DOWN, buff=0.3)
        VGroup(expect, found).arrange(RIGHT, buff=1.0).move_to(UP * 0.6)
        num = label(rf"rice 1\% dearer \ $\Rightarrow$ \ {h['share_le_080'][0]:.2f}\% \emph{{more}} rice "
                    r"\\ (households getting under 80\% of their calories from rice)", font_size=28,
                    color=GIFF).next_to(VGroup(expect, found), DOWN, buff=0.8)
        foot = label(r"they bought more rice when the vouchers ended, \ and less while they had them", font_size=24,
                     color=GREY_A).next_to(num, DOWN, buff=0.4)
        tag = published_tag(r"Jensen and Miller, AER (2008), table 3", corner=DR, font_size=15)
        with self.voiceover(
            "So: when rice got cheaper, did they eat more rice? <bookmark mark='a'/> Every textbook says yes. "
            "That's the law of demand, the most basic prediction in economics. <bookmark mark='b'/> In Hunan, among "
            "households that were poor but not the very poorest, the answer was no. They ate less rice while they "
            "held the vouchers, and more again when the vouchers ran out. <bookmark mark='c'/> On their numbers, a "
            "one percent rise in the price of rice raised those households' rice consumption by about 0.45 "
            "percent. Demand sloped up."
        ) as vo:
            self.play(FadeIn(q), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(expect, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(found, shift=UP * 0.2), FadeIn(foot))
            vo.wait_until("c")
            self.play(FadeIn(num, shift=UP * 0.1))
            self.play(Indicate(found[1], color=GIFF))
        self.clear_scene()

    def rumour(self):
        t = tables.JENSEN_MILLER_2008.data
        m = quote_card(t["marshall_1895"], r"Alfred Marshall, \emph{Principles of Economics}, 3rd edition (1895), "
                                           r"p.\ 208", width=11.4, font_size=25, color=GIFF).to_edge(UP, buff=0.4)
        s = quote_card(t["stigler_1987"], r"George Stigler, \emph{The Theory of Price} (1987), p.\ 23, on the law "
                                          r"of demand", width=10.0, font_size=25, color=E.ACCENT)
        s.next_to(m, DOWN, buff=0.4)
        tag = published_tag(r"both as quoted by Jensen and Miller (2008)", corner=DR, font_size=14)
        head = label(r"a century-old rumour", font_size=34, color=GIFF).to_edge(UP, buff=0.35)
        m.next_to(head, DOWN, buff=0.3)
        s.next_to(m, DOWN, buff=0.35)
        with self.voiceover(
            "This was not supposed to happen, or rather, it was supposed to be a rumour. <bookmark mark='a'/> In "
            "1895 Alfred Marshall added a sentence to the third edition of his Principles. A rise in the price of "
            "bread, he wrote, citing Robert Giffen, drains the poorer labouring families so badly that they must "
            "give up meat, and since bread is still the cheapest food, they consume more of it, and not less. "
            "<bookmark mark='b'/> For a hundred years economists taught the idea and looked for the thing. Nobody "
            "found it. George Stigler, Nobel laureate and sceptic, said that an economist who could show the law of "
            "demand failing in a real market would be assured of immortality, and rapid promotion while still alive."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(head, shift=DOWN * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(m, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(s, shift=UP * 0.2))
        self.clear_scene()

    def slutsky(self):
        t = tables.SLUTSKY_1915.data
        c1 = history_card(r"1915", r"Eugen Slutsky, Kiev: \ ``On the theory of the budget of the consumer''",
                          r"in Italian, in the \emph{Giornale degli Economisti}, July 1915, in the middle of a war",
                          color=SUB, width=5.6, font_size=22)
        c2 = history_card(r"1934--36", r"Hicks and Allen; \ then Schultz and Allen find Slutsky",
                          r"the same equation, reached again in London; Hicks later named it the fundamental "
                          r"equation of value theory", color=INC, width=5.6, font_size=22)
        VGroup(c1, c2).arrange(RIGHT, buff=0.5, aligned_edge=UP).move_to(UP * 0.5)
        eq = MathTex(r"\underbrace{\frac{\partial x}{\partial p}}_{\text{what you see}} \;=\; "
                     r"\underbrace{\frac{\partial h}{\partial p}}_{\text{cheaper relative to}} \;-\; "
                     r"\underbrace{x\,\frac{\partial x}{\partial m}}_{\text{richer or poorer}}",
                     font_size=40).next_to(VGroup(c1, c2), DOWN, buff=0.5)
        tag = published_tag(r"Chipman and Lenfant, HOPE 34(3) (2002)", corner=DR, font_size=14)
        with self.voiceover(
            "The equation that explains Hunan was written down in 1915, <bookmark mark='a'/> by Eugen Slutsky, a "
            "statistician in Kiev, in an Italian journal, in the middle of a world war. Almost nobody read it. "
            "<bookmark mark='b'/> Twenty years later John Hicks and Roy Allen, in London, found the same result "
            "for themselves, and only then did Henry Schultz and Allen bring Slutsky's paper to light. "
            "<bookmark mark='c'/> It says that every price change does two things at once. It makes the good "
            "cheaper or dearer relative to everything else, and it makes the buyer richer or poorer. This part is "
            "about those two things, and about what they're worth in dollars."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(c1, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(Indicate(c1, color=SUB, scale_factor=1.02))
            vo.wait_until("b")
            self.play(FadeIn(c2, shift=UP * 0.2))
            vo.wait_until("c")
            self.play(Write(eq), run_time=2.0)
        self.clear_scene()

    def question(self):
        q = wrapped_label(ASK, 12.0, 38, E.ACCENT).to_edge(UP, buff=0.7)
        rows = VGroup(
            label(r"how does one price change split into two effects?", font_size=30, color=WHITE),
            label(r"when can demand slope up, \ and who is it for?", font_size=30, color=GIFF),
            label(r"what is a price change worth in dollars, \ and what does it do to the cost of living?",
                  font_size=30, color=HICKS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(q, DOWN, buff=0.7)
        with self.voiceover(
            "So this part asks: when a price changes, what happens to what people buy, and to how well off they "
            "are? <bookmark mark='a'/> How does a single price change split into two effects? "
            "<bookmark mark='b'/> When can demand slope up, and for whom? <bookmark mark='c'/> And what is a price "
            "change worth in dollars: to one household, and to the cost of living of a whole country?"
        ) as vo:
            self.play(FadeIn(q, shift=DOWN * 0.2))
            for mk, r in zip("abc", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.2))
        self.clear_scene()

    def title(self):
        logo = voucher_glyph(0.9)
        t = label(r"Economics, Built", font_size=60)
        sub = label(r"Part 6 \ $\cdot$ \ Demand", font_size=34, color=E.ACCENT)
        g = VGroup(logo, t, sub).arrange(DOWN, buff=0.45)
        with self.voiceover("Economics, Built. Part six: demand."):
            self.play(Create(logo.body), Create(logo.perf), FadeIn(logo.stub), run_time=1.4)
            self.play(Write(t), run_time=1.2)
            self.play(FadeIn(sub, shift=UP * 0.15))
        self.wait(1.0)
        self.clear_scene()

    def objectives(self):
        head = label(r"Act II \ $\cdot$ \ Choosing", font_size=40, color=E.ACCENT)
        obj = objectives_card([
            r"feed a household for a week on \$21 yourself, \ and watch what a dearer staple does",
            r"the demand function, \ and Slutsky's two effects, \ drawn as two moves",
            r"Giffen behaviour: \ the theory, \ the rumour, \ and the experiment that found it",
            r"duality and integrability: \ four functions, \ and a loop that pumps money",
            r"Engel curves, \ welfare in dollars, \ the cost of living, \ and demand systems you can estimate",
        ], color=E.ACCENT, font_size=31, width=13.0)
        with self.voiceover(
            "This part continues Act Two, on choosing. <bookmark mark='a'/> You'll feed a household for a week on "
            "twenty-one dollars, and see for yourself what a dearer staple does. <bookmark mark='b'/> We'll draw the "
            "demand function, and Slutsky's two effects as two moves on a picture. <bookmark mark='c'/> We'll find "
            "out when demand slopes up, and how Jensen and Miller found it. <bookmark mark='d'/> We'll meet the four "
            "functions that describe one consumer, and a loop of prices that pumps money out of a consumer whose "
            "demand comes from no preference at all. <bookmark mark='e'/> And then Engel's law, the dollar value "
            "of a price change, the cost of living, and the demand systems economists actually estimate."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(head), FadeIn(obj.head), FadeIn(obj.rows[0], shift=RIGHT * 0.2))
            for mark, r in zip("bcde", obj.rows[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r, shift=RIGHT * 0.2))
        self.clear_scene()
