from __future__ import annotations

from videos.economics.econ40.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        card(self, 16, r"Frontier: \ national accounts, \ wealth taxes, \ families",
             r"What is still being worked out?", "Chapter sixteen. Frontier: national accounts, wealth taxes, "
             "families.", lit={2018: r"Piketty, \ Saez and Zucman", 2020: r"Jakobsen et al.; \ Black et al."},
             scale=("household", "nation"), horizon=("a decade",))
        self.open()

    def open(self):
        cards = point_cards([
            (r"distributional national accounts", r"give every dollar of \\ national income \\ to a person, \\ so "
                                                   r"the shares add up \\ to GDP; \ the open \\ question: \ untaxed "
                                                   r"income", TOP),
            (r"wealth taxes", r"Denmark's wealth tax: \\ clear effects on \\ wealth, \ largest at the \\ top; \ a "
                              r"sizeable \\ long-run elasticity", WEALTH),
            (r"genes, \ family, \ luck", r"Swedish adoptees: \\ the adoptive parents' \\ wealth predicts theirs \\ "
                                         r"far better than the \\ biological parents'", CHILD),
        ], width=12.6, cols=3, font_size=19).move_to(DOWN * 0.2)
        head = label(r"open questions", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.5)
        tag = published_tag(tables.FRONTIER40.tag, corner=DR, font_size=10)
        with self.voiceover(
            "Three frontiers. <bookmark mark='a'/> Distributional national accounts. Piketty, Saez and Gabriel "
            "Zucman allocate every dollar of national income to a person, so that the shares of the rich, the "
            "middle and the poor add up to the economy, and so that inequality and growth can be read from one set "
            "of books. Chapter three's dispute is about exactly the parts of national income that no tax return "
            "records. <bookmark mark='b'/> Wealth taxes. If the tail of wealth depends on the return the very rich "
            "keep, a tax on wealth should change it, and how much wealth responds is the decisive number. In "
            "Denmark, which taxed wealth and then cut and abolished the tax, Katrine Jakobsen, Kristian Jakobsen, "
            "Henrik Kleven and Zucman found clear responses, largest at the top. <bookmark mark='c'/> And genes, "
            "family and luck. Among Swedish adoptees, Sandra Black, Paul Devereux, Petter Lundborg "
            "and Kaveh Majlesi found that the wealth of the adoptive parents predicts the child's wealth far better "
            "than the wealth of the biological parents, and more so once bequests arrive: wealth passes on mostly "
            "through the family that raises you, not through its genes."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c in zip("abc", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
