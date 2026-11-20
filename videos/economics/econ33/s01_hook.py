from __future__ import annotations

from videos.economics.econ33.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.visit()
        self.letter()
        self.question()
        self.title()
        self.objectives()

    def visit(self):
        G = load("gfc")
        head = VGroup(label(r"5 November 2008: \ the London School of Economics", font_size=30, color=E.ACCENT),
                      label(r"the Queen opens a new building, \ and is briefed on the crisis", font_size=22,
                            color=GREY_A)).arrange(DOWN, buff=0.18).to_edge(UP, buff=0.4)
        ax = plane([2000, 2009], [80, 200], center=LEFT * 2.6 + DOWN * 0.7, x_length=6.4, y_length=3.6,
                   xticks=[2000, 2002, 2004, 2006, 2008], yticks=[100, 150, 200],
                   ylabel=r"US house prices, \ January 2000 = 100", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:.0f}", font_size=15)
        cs = path(ax, G["cs_t"], G["cs"], HOUSE, 3.2, xr=(2000, 2008.84), smooth=False)
        ted_ax = plane([2006, 2009], [0, 5], center=RIGHT * 3.6 + DOWN * 0.7, x_length=4.6, y_length=3.6,
                       xticks=[2006, 2007, 2008, 2009], yticks=[0, 1, 2, 3, 4, 5],
                       ylabel=r"the TED spread, \ points \ (monthly average)", xfmt=lambda v: f"{v:.0f}",
                       yfmt=lambda v: f"{v:.0f}",
                       font_size=15)
        ted = path(ted_ax, G["ted_t"], G["ted"], CRISIS, 3.2, xr=(2006, 2008.84), smooth=False)
        q = label(r"``Why did nobody notice it?''", font_size=40, color=WHITE).move_to(DOWN * 0.5)
        note = label(r"as reported: \ accounts of her exact words differ", font_size=18, color=GREY_B).next_to(
            q, DOWN, buff=0.25)
        ans = label(r"Luis Garicano, \ as reported: \ ``at every stage, \ someone was relying on somebody else, \\ "
                    r"and everyone thought they were doing the right thing''", font_size=21, color=GREY_A).next_to(
            note, DOWN, buff=0.5)
        tag = data_tag(r"S\&P CoreLogic Case-Shiller and the TED spread, \ via FRED", corner=DR, font_size=12)
        with self.voiceover(
            "On the fifth of November 2008, Queen Elizabeth opened a new building at the London School of "
            "Economics. <bookmark mark='a'/> By then American house prices had been falling for two years, "
            f"{G['cs_fall']:.0f} percent from their peak by the time they bottomed, <bookmark mark='b'/> and the "
            "rate at which banks lent to each other had just spiked above the Treasury rate: on the tenth of "
            f"October the gap reached {G['ted_peak']:.1f} points, against about half a point in 2006, the sign of "
            "banks that no longer trusted one another. <bookmark mark='c'/> During a briefing on "
            "the crisis she asked a simple question. As it was reported, she asked: why did nobody notice it? "
            "<bookmark mark='d'/> One of the economists, Luis Garicano, answered that at every stage someone was "
            "relying on somebody else, and everyone thought they were doing the right thing."
        ) as vo:
            self.play(FadeIn(head, shift=DOWN * 0.2), FadeIn(ax), FadeIn(ted_ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(cs), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(ted), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeOut(VGroup(ax, ted_ax, cs, ted, tag)), FadeIn(q, scale=1.05), FadeIn(note))
            vo.wait_until("d")
            self.play(FadeIn(ans, shift=UP * 0.1))
        self.clear_scene()

    def letter(self):
        head = label(r"22 July 2009: \ the British Academy's answer", font_size=30, color=E.ACCENT).to_edge(
            UP, buff=0.6)
        qc = quote_card(r"the failure to foresee the timing, \ extent and severity of the crisis and to head it off, "
                        r"\ while it had many causes, \ was principally a failure of the collective imagination of "
                        r"many bright people, \ both in this country and internationally, \ to understand the risks "
                        r"to the system as a whole", r"Tim Besley and Peter Hennessy, \ for the British Academy",
                        width=11.0, font_size=26)
        qc.next_to(head, DOWN, buff=0.6)
        aim = label(r"this part: \ what there was to see, \ and how much of it could have been seen",
                    font_size=24, color=HOUSE).to_edge(DOWN, buff=0.7)
        tag = published_tag(r"Besley and Hennessy, \ letter to the Queen, \ 22 July 2009 (British Academy)",
                            corner=DR, font_size=12)
        with self.voiceover(
            "The question stung. The British Academy gathered economists, officials and bankers to answer it, and "
            "in July 2009 two professors, Tim Besley and Peter Hennessy, wrote to the Queen. <bookmark mark='a'/> "
            "Their letter concluded that the failure to foresee the timing, extent and severity of the crisis, and "
            "to head it off, while it had many causes, was principally a failure of the collective imagination of "
            "many bright people, both in Britain and abroad, to understand the risks to the system as a whole. "
            "<bookmark mark='b'/> This part reconstructs what there was to see: the theories that predicted this "
            "kind of event, the data that warned of it, and how much a careful observer could have known in advance."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(qc, shift=UP * 0.2), run_time=1.2)
            vo.wait_until("b")
            self.play(FadeIn(aim, shift=UP * 0.1))
        self.clear_scene()

    def question(self):
        q = wrapped_label(ASK, 12.0, 40, E.ACCENT).to_edge(UP, buff=0.8)
        rows = VGroup(
            label(r"why does a little bad news become a crisis? \ amplification", font_size=26, color=CREDIT),
            label(r"what did 2008 look like from the inside, \ in order?", font_size=26, color=HOUSE),
            label(r"can crises be predicted, \ and what can be done about them?", font_size=26, color=CRISIS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(q, DOWN, buff=0.7)
        with self.voiceover(
            "This part's question: why do financial systems blow up, and why is it so hard to see it coming? "
            "<bookmark mark='a'/> Why does a little bad news, a fall in house prices or one bank's losses, become a "
            "collapse of the whole system? <bookmark mark='b'/> What did 2008 look like, in order, from the inside? "
            "<bookmark mark='c'/> And can crises be predicted, and what can be done before and after?"
        ) as vo:
            self.play(FadeIn(q, shift=DOWN * 0.2))
            for mk, r_ in zip("abc", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
        self.clear_scene()

    def title(self):
        F = load("film")
        mini = plane([1870, 2020], [0, 120], x_length=4.2, y_length=1.4)
        logo = path(mini, F["years"], F["median"], CREDIT, 2.6, smooth=False)
        tt = label(r"Economics, Built", font_size=60)
        sub = label(r"Part 33 \ $\cdot$ \ Crises", font_size=34, color=E.ACCENT)
        VGroup(logo, tt, sub).arrange(DOWN, buff=0.45)
        with self.voiceover("Economics, Built. Part thirty-three: crises."):
            self.play(Create(logo), run_time=1.6)
            self.play(Write(tt), run_time=1.2)
            self.play(FadeIn(sub, shift=UP * 0.15))
        self.wait(1.0)
        self.clear_scene()

    def objectives(self):
        head = label(r"Act VI \ $\cdot$ \ Money and the Cycle", font_size=40, color=E.ACCENT)
        obj = objectives_card([
            r"eight credit booms to judge; \ Kindleberger's anatomy and Minsky's borrowers",
            r"debt deflation; \ the financial accelerator; \ collateral cycles; \ the leverage cycle",
            r"2008 in order; \ households' balance sheets",
            r"150 years in 18 countries: \ credit booms and crises; \ your guesses scored",
            r"fighting crises; \ macroprudential policy; \ sudden stops; \ two dials",
        ], color=E.ACCENT, font_size=31, width=13.0)
        with self.voiceover(
            "Here is the plan. <bookmark mark='a'/> First you judge eight credit booms from history, and meet the "
            "old descriptions of how manias end. <bookmark mark='b'/> Then four mechanisms that turn small losses "
            "into large ones: falling prices that raise the weight of debt, net worth and the cost of borrowing, "
            "collateral, and leverage. <bookmark mark='c'/> The crisis of 2008 in order, and what debt did to "
            "households. <bookmark mark='d'/> A hundred and fifty years of data from eighteen countries, to ask "
            "whether credit booms predict crises, and your guesses scored. <bookmark mark='e'/> What governments "
            "and central banks do in a crisis and before one, crises in emerging markets, and two dials."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(head), FadeIn(obj.head), FadeIn(obj.rows[0], shift=RIGHT * 0.2))
            for mk, r_ in zip("bcde", obj.rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
        self.clear_scene()
