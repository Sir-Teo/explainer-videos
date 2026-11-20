from __future__ import annotations

from videos.economics.econ33.common import *  # noqa: F403


class Macropru(VoiceoverScene):
    def construct(self):
        card(self, 12, r"Macroprudential policy", r"Can regulators lean against a credit boom?",
             "Chapter twelve. Macroprudential policy.", lit={2000: r"Spain's dynamic provisions",
                                                              2010: r"Basel III"},
             scale=("nation",), horizon=("a year", "a decade"))
        self.tools()
        self.guide()

    def tools(self):
        cards = point_cards([
            (r"countercyclical capital buffer", r"banks hold up to 2.5\% more capital \\ when credit runs ahead; \\ "
                                                r"released in a bust", BANK),
            (r"limits on borrowers", r"loan-to-value and \\ debt-to-income caps \\ on mortgages", HOUSE),
            (r"the evidence", r"119 countries, \ 2000--13: \\ less credit growth, \\ but weaker in open and \\ "
                              r"advanced economies, \ and leaks \\ to lenders outside the rules", CREDIT),
        ], width=12.8, cols=3, font_size=21).move_to(DOWN * 0.2)
        head = label(r"leaning against the boom: \ rules for the system, \ not one bank", font_size=28,
                     color=E.ACCENT).to_edge(UP, buff=0.5)
        tag = published_tag(r"Basel Committee (2010); \ Cerutti, \ Claessens and Laeven, \ \emph{JFS} 28 (2017)",
                            corner=DR, font_size=12)
        with self.voiceover(
            "If credit booms raise the odds of a crisis, why not lean against them? Rules for a single bank's "
            "safety, microprudential rules, miss what happens when all banks lend into the same boom. "
            "Macroprudential policy aims at the system. <bookmark mark='a'/> Basel III, agreed after the crisis, "
            "added a countercyclical capital buffer: when credit runs ahead of the economy, regulators can require "
            "banks to hold up to two and a half percent more capital, to be released in the bust. "
            "<bookmark mark='b'/> Many countries also cap mortgages, by the loan's share of the house's value, or "
            "by the borrower's debt relative to income. <bookmark mark='c'/> Does it work? Eugenio Cerutti, Stijn "
            "Claessens and Luc Laeven studied 119 countries from 2000 to 2013: more use of these tools went with "
            "slower credit growth, but much less so in open and advanced economies, where borrowers can turn to "
            "foreign lenders, or to lenders the rules do not cover."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c in zip("abc", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()

    def guide(self):
        C = load("ccyb")
        es, us = C["ESP"], C["USA"]
        ax = plane([1985, 2012], [-30, 45], center=LEFT * 3.3 + DOWN * 0.3, x_length=5.6, y_length=4.4,
                   xticks=[1985, 1995, 2005], yticks=[-30, -15, 0, 15, 30, 45], ylabel=r"the credit gap, \ points",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=14)
        ax2 = plane([1985, 2012], [0, 2.8], center=RIGHT * 3.3 + DOWN * 0.3, x_length=5.6, y_length=4.4,
                    xticks=[1985, 1995, 2005], yticks=[0, 0.5, 1.0, 1.5, 2.0, 2.5],
                    ylabel=r"the guide's buffer, \ \% of risk-weighted assets", xfmt=lambda v: f"{v:.0f}",
                    yfmt=lambda v: f"{v:.1f}", font_size=14)
        zero = seg(ax, 1985, 0, 2012, 0, GREY_C, 1.2)
        band_ = Rectangle(width=(ax.ax.c2p(2012, 0) - ax.ax.c2p(1985, 0))[0],
                          height=(ax.ax.c2p(0, 10) - ax.ax.c2p(0, 2))[1], fill_color=HOUSE, fill_opacity=0.12,
                          stroke_width=0).move_to(ax.ax.c2p(1998.5, 6))
        lines = {}
        for k, d, c in (("ESP", es, CRISIS), ("USA", us, CB)):
            lines[k] = (path(ax, d["years"], d["gap"], c, 3.2, xr=(1985, 2012), smooth=False),
                        path(ax2, d["years"], d["buffer"], c, 3.2, xr=(1985, 2012), smooth=False))
        crisis = vline(ax2, 2008, 0, 2.8, GREY_B, 1.5)
        k1 = VGroup(label(r"red: \ Spain; \ blue: \ the United States", font_size=16, color=WHITE),
                    label(r"gold band: \ a gap of 2 to 10 points", font_size=16, color=HOUSE)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.05).next_to(ax, UP, buff=0.1)
        k2 = label(r"dashed: \ 2008", font_size=16, color=GREY_B).next_to(ax2, UP, buff=0.1)
        foot = VGroup(
            label(rf"Spain: \ the full buffer every year from {es['first_full']}; \ its own dynamic provisions, \ "
                  r"from 2000, \ cushioned the bust but did not stop the boom", font_size=19, color=CRISIS),
            label(r"America's credit came mostly from markets, \ not banks: \ measured by bank loans, \ the guide "
                  r"barely moves", font_size=19, color=CB),
        ).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.55)
        tag = data_tag(r"Jord\`a, \ Schularick and Taylor; \ the Basel guide computed here (bank loans for all "
                       r"credit; \ annual $\lambda = 1562.5$)", corner=DR, font_size=11)
        with self.voiceover(
            "Basel's guide for when to raise the buffer is a computable rule. <bookmark mark='a'/> Take credit as a "
            "share of GDP, and subtract its trend estimated only from the data available at each date: the credit "
            "gap. A gap between two and ten points maps into a buffer between zero and two and a half percent. "
            "<bookmark mark='b'/> Here it is for Spain, using bank loans for credit. The gap passed ten points in "
            f"{es['first_full']} and stayed there; by 2007 it was {es['gap2007']:.0f} points. The guide would have "
            "demanded the full buffer for nine years before the crisis. Spain did have a buffer of its own, "
            "dynamic provisions from 2000; Gabriel Jimenez and coauthors found that it cushioned lending in the "
            "bust, but it did not stop the boom. <bookmark mark='c'/> For the United States, measured the same way, "
            "the guide barely moves, because most American mortgage credit came from securities markets, not bank "
            "loans: the boom was outside the measure, as it was outside the rules. <bookmark mark='d'/> The tools "
            "exist. Knowing when to use them, and reaching the credit that moves outside banks, is the hard part."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(ax2), FadeIn(zero), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(band_), FadeIn(k1[1]))
            vo.wait_until("b")
            self.play(Create(lines["ESP"][0]), Create(lines["ESP"][1]), FadeIn(k1[0]), FadeIn(crisis), FadeIn(k2),
                      FadeIn(foot[0]), run_time=2.0)
            vo.wait_until("c")
            self.play(Create(lines["USA"][0]), Create(lines["USA"][1]), FadeIn(foot[1]), run_time=2.0)
        self.clear_scene()
