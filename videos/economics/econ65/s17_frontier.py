from __future__ import annotations

from videos.economics.econ65.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        card(self, 15, r"Frontier: \ scenarios and usage data", r"How do economists reason about transformative AI, "
             r"\ and how can they see its spread?", "Chapter fifteen. Frontier: scenarios and usage data.",
             lit={2024: "Korinek and Suh; Jones"}, scale=("world",), horizon=("a decade", "a century"))
        self.scenarios()
        self.usage()
        self.keynes()

    def scenarios(self):
        cards = point_cards([
            (r"scenarios, \ not forecasts", r"Korinek and Suh: \ the same model under business as usual, \ and "
             r"with every task automatable in twenty years or in five: \ chapter seven's race", MACH),
            (r"growth against risk", r"Jones: \ how much risk of catastrophe is worth faster growth depends on how "
             r"fast the value of more consumption falls; \ longer lives raise the stakes on both sides", NAIVE),
            (r"what is not modelled", r"politics, \ power, \ and what people want to do with their time: \ "
             r"Keynes's real problem", GDP),
        ], width=12.6, cols=1, font_size=20).move_to(DOWN * 0.1)
        head = label(r"reasoning about transformative AI", font_size=28, color=E.ACCENT).to_edge(UP, buff=0.5)
        tag = published_tag(r"Korinek and Suh, \ NBER WP 32255 (2024); \ Jones, \ AER: Insights 6(4) (2024)",
                            corner=DL, font_size=12)
        with self.voiceover(
            "At the frontier, economists are learning to reason about AI that could do most work. <bookmark "
            "mark='a'/> Anton Korinek and Donghyun Suh run one model under several futures, as in chapter seven: "
            "scenarios, not forecasts, so that policy can be ready for each. <bookmark mark='b'/> Charles Jones asks "
            "how much risk of catastrophe would be worth accepting for faster growth. The answer turns on how fast "
            "the value of extra consumption falls as we get richer: if it falls fast, a richer world has little "
            "to gain and everything to lose; and if AI also lengthens lives, the stakes rise on both sides. "
            "<bookmark mark='c'/> And none of these models captures politics, power, or what people would want to "
            "do with their time, which was Keynes's real problem."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c in zip("abc", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()

    def usage(self):
        rows = VGroup(
            VGroup(label(r"39\%", font_size=50, color=TEXT),
                   label(r"of Americans aged 18--64 had used generative AI by August 2024, \\ under two years after "
                         r"ChatGPT: \ faster than the PC or the internet", font_size=19, color=GREY_A)).arrange(
                RIGHT, buff=0.4),
            VGroup(label(r"28\%", font_size=50, color=WORK),
                   label(r"of employed respondents used it at work; \ more among the young, \\ men, \ and college "
                         r"graduates", font_size=19, color=GREY_A)).arrange(RIGHT, buff=0.4),
            VGroup(label(r"logs", font_size=50, color=MACH),
                   label(r"model makers now publish privacy-preserving statistics of the tasks \\ people bring to "
                         r"their models: \ usage, \ not exposure", font_size=19, color=GREY_A)).arrange(
                RIGHT, buff=0.4),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to(DOWN * 0.1)
        head = label(r"seeing adoption as it happens", font_size=28, color=E.ACCENT).to_edge(UP, buff=0.5)
        tag = published_tag(r"Bick, \ Blandin and Deming, \ NBER WP 32966 (2024); \ Handa et al., \ Anthropic "
                            r"Economic Index (2025); \ Tomlinson et al., \ Microsoft (2025)", corner=DL, font_size=12)
        with self.voiceover(
            "The other frontier is measurement. The number the experiments could not give us is adoption. "
            "<bookmark mark='a'/> Alexander Bick, Adam Blandin and David Deming added questions to a national "
            "survey: by August 2024, under two years after ChatGPT's release, about thirty-nine percent of "
            "Americans aged eighteen to sixty-four had used generative AI, faster adoption than the personal "
            "computer or the internet. <bookmark mark='b'/> About twenty-eight percent of employed respondents had "
            "used it at work, more among younger workers, men and college graduates. <bookmark mark='c'/> And the "
            "companies that make the models have begun publishing privacy-preserving statistics of the tasks "
            "people bring to them, from Anthropic and Microsoft among others. That measures usage task by task, "
            "where Eloundou and coauthors could only measure exposure. Putting those measures into Hulten's "
            "arithmetic, year by year, is how the Dials of chapter thirteen will be settled."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, r_ in zip("abc", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.15))
        self.clear_scene()

    def keynes(self):
        c = calls.CALLS["keynes_1930"]
        cc = call_card(tex_safe(c.who), c.when, tex_safe(c.said), tex_safe(c.outcome), c.verdict, width=12.6,
                       font_size=18)
        cc.move_to(UP * 0.4)
        lesson = label(r"the riches came; \ the question of what to do with them is still open", font_size=21,
                       color=E.ACCENT).next_to(cc, DOWN, buff=0.5)
        tag = data_tag(r"Maddison Project Database 2023; \ Penn World Table 11.0", corner=DL, font_size=12)
        with self.voiceover(
            "We began with Keynes. Called it? <bookmark mark='a'/> In 1930 he predicted that, a hundred years on, "
            "the progressive countries would be four to eight times richer, and work fifteen hours a week. "
            "<bookmark mark='b'/> They are between four and seven and a half times richer. They work roughly twice "
            "as many hours as he imagined. <bookmark mark='c'/> Partly right. <bookmark mark='d'/> We took the "
            "riches and not the time. If AI brings a second such century, his question, what people will do with "
            "the freedom, will matter more than ever."
        ) as vo:
            self.play(FadeIn(cc.card), FadeIn(cc[1][0]), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(cc.left))
            vo.wait_until("b")
            self.play(FadeIn(cc.right))
            vo.wait_until("c")
            self.play(FadeIn(cc.stamp, scale=1.4))
            vo.wait_until("d")
            self.play(FadeIn(lesson))
        self.clear_scene()
