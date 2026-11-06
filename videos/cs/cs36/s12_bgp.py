from __future__ import annotations

import random

from explainer.cs import *  # noqa: F403
from videos.cs.cs36.common import (DATA, HEAD, KERN, LAM, NO, PART, YES, grid_table, load)


class Bgp(VoiceoverScene):
    def construct(self):
        self.card()
        self.policy()
        self.hijack()
        self.rpki()

    def card(self):
        card = chapter_card(11, r"BGP", r"How do 75{,}000 independent networks agree on routes?", lit=(1989, 2001, 2008),
                            extra=((1989, r"BGP"), (2001, r"Gao and Rexford: \ stable policies"),
                                   (2008, r"YouTube's hijack")), part=PART)
        with self.voiceover("Chapter eleven. BGP."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def policy(self):
        b = load("bgp")
        head = label(r"Paths, \ and business", font_size=36).to_edge(UP, buff=0.3)
        tiers = VGroup()
        rng = random.Random(2)
        rows = [(5, YES, r"tier 1: \ a clique of peers"), (10, HEAD, r"tier 2: \ buy transit, \ peer"),
                (18, DATA, r"stubs: \ customers")]
        dots = []
        for k, (n, c, t) in enumerate(rows):
            row = VGroup(*[Dot(radius=0.09, color=c) for _ in range(n)]).arrange(RIGHT, buff=0.35 - k * 0.08)
            row.move_to([-2.8, 1.8 - k * 1.3, 0])
            lab = label(t, font_size=17, color=c).next_to(row, LEFT, buff=0.3)
            tiers.add(VGroup(row, lab))
            dots.append(row)
        links = VGroup()
        for i in range(5):
            for j in range(i + 1, 5):
                links.add(Line(dots[0][i].get_center(), dots[0][j].get_center(), color=YES, stroke_width=1,
                               stroke_opacity=0.5))
        for d in dots[1]:
            links.add(Line(d.get_center(), dots[0][rng.randrange(5)].get_center(), color=GREY_C, stroke_width=1))
        for d in dots[2]:
            links.add(Line(d.get_center(), dots[1][rng.randrange(10)].get_center(), color=GREY_C, stroke_width=1))
        rules = VGroup(
            wrapped_label(r"\textbf{path vector}: \ a route carries its whole AS path, \ so loops are seen and refused",
                  6.6, font_size=19, color=WHITE),
            wrapped_label(r"prefer routes from \textbf{customers} \ (they pay), \ then \textbf{peers} \ (free), \ then "
                  r"\textbf{providers} \ (cost)", 6.6, font_size=19, color=YES),
            wrapped_label(r"export customer routes to everyone; \ peer and provider routes only to customers", 6.6, font_size=19,
                  color=HEAD),
            wrapped_label(r"Gao and Rexford \ (2001): \ with these rules BGP always converges, \ to valley-free paths",
                  6.6, font_size=19, color=LAM),
            wrapped_label(rf"our {b['ases']} ASes: \ every AS reaches the prefix, \ in {b['rounds']} rounds; \ mean path "
                  rf"{b['mean_path']:.1f} ASes, \ e.g. \ "
                  + r" $\rightarrow$ ".join(str(a) for a in b["sample_path"]), 6.6, font_size=19, color=KERN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([3.4, 0.2, 0])
        rules.move_to([3.5, 0.2, 0])
        with self.voiceover(
            "Between networks, the Internet routes by policy, not by distance. <bookmark mark='a'/> It is made of "
            "about seventy-five thousand autonomous systems, each a network under one administration, connected as "
            "customers and providers, or as peers who exchange traffic for free. At the top, a handful of tier-one "
            "networks peer with each other and buy from nobody. <bookmark mark='b'/> They speak BGP. A route carries "
            "its whole path of systems, so a system that sees itself in a path rejects it: no counting to infinity. "
            "<bookmark mark='c'/> Then money decides. Prefer routes learned from customers, who pay you; then peers; "
            "then providers, whom you pay. <bookmark mark='d'/> And never carry traffic between two of your providers "
            "for free: export peer and provider routes only to customers. <bookmark mark='e'/> Lixin Gao and Jennifer "
            "Rexford proved in 2001 that these economic rules guarantee BGP converges. <bookmark mark='f'/> On our "
            "synthetic internet of a hundred and twenty-five systems, a stub's prefix reaches every system in six "
            "rounds, over paths of three or four."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(tiers), FadeIn(links))
            for mk, r in zip("bcdef", rules):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.wait(0.3)
        self.clear_scene()

    def hijack(self):
        b = load("bgp")
        head = label(r"Anyone can announce anything", font_size=36).to_edge(UP, buff=0.3)
        story = VGroup(
            label(r"24 February 2008: \ Pakistan Telecom is told to block YouTube inside Pakistan", font_size=20,
                  color=WHITE),
            label(r"it announces \texttt{208.65.153.0/24}, \ inside YouTube's \texttt{208.65.152.0/22}, \ and the "
                  r"announcement leaks to its provider", font_size=20, color=NO),
            label(r"longest prefix wins: \ within minutes most of the Internet sends YouTube's traffic to Pakistan, \ "
                  r"for about two hours", font_size=20, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).next_to(head, DOWN, buff=0.45)
        rows = [[r"the same prefix, \ \texttt{/22}", f"{b['origin_hijacked']} of {b['ases']}"],
                [r"a more specific \texttt{/24}", f"{b['sub_hijacked']} of {b['ases']}"]]
        tab = grid_table([r"a stub announces YouTube's address as its own", r"ASes that follow it"], rows,
                         widths=[6.4, 3.2], row_h=0.46, font_size=20, mono_cols=())
        tab.next_to(story, DOWN, buff=0.5).set_x(0)
        tab.cells[1][1].set_color(KERN)
        tab.cells[2][1].set_color(NO)
        foot = label(r"an equal claim splits the Internet by nearness; \ a more specific claim wins everywhere",
                     font_size=20, color=HEAD).next_to(tab, DOWN, buff=0.4)
        with self.voiceover(
            "BGP believes what it is told. <bookmark mark='a'/> In February 2008 Pakistan Telecom was ordered to "
            "block YouTube within Pakistan. <bookmark mark='b'/> It announced a slash-twenty-four inside YouTube's "
            "address block, to send local traffic nowhere, and the announcement leaked to its provider, and from there "
            "to the world. <bookmark mark='c'/> Because the longest prefix wins, most of the Internet sent YouTube's "
            "traffic to Pakistan for about two hours. <bookmark mark='d'/> We repeated it on our internet. A stub "
            "claiming the same prefix as the victim captures the forty percent of systems that are closer to it. A "
            "stub claiming a more specific prefix captures every one."
        ) as vo:
            self.play(FadeIn(head))
            for mk, s in zip("abc", story):
                vo.wait_until(mk)
                self.play(FadeIn(s))
            vo.wait_until("d")
            self.play(FadeIn(tab), FadeIn(foot))
        self.wait(0.3)
        self.clear_scene()

    def rpki(self):
        b = load("bgp")
        head = label(r"Signing who may announce what", font_size=36).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[0, 1, 0.25], y_range=[0, 1, 0.25], x_length=5.6, y_length=3.6,
                  axis_config={"color": GREY_D, "include_numbers": False}).move_to([-2.8, -0.3, 0])
        xt = VGroup(*[label(f"{int(x * 100)}\\%", font_size=16, color=GREY_B).next_to(ax.c2p(x, 0), DOWN, buff=0.1)
                      for x in (0, 0.25, 0.5, 0.75, 1)])
        yt = VGroup(*[label(f"{int(y * 100)}\\%", font_size=16, color=GREY_B).next_to(ax.c2p(0, y), LEFT, buff=0.1)
                      for y in (0.25, 0.5, 0.75, 1)])
        xl = label(r"ASes that validate origins \ (random choice)", font_size=17, color=GREY_A).next_to(xt, DOWN,
                                                                                                       buff=0.08)
        yl = label(r"ASes still hijacked", font_size=17, color=GREY_A).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        pts = [ax.c2p(a["frac"], a["hijacked"]) for a in b["adoption"]]
        cv = VMobject(color=NO, stroke_width=3).set_points_as_corners(pts)
        dots = VGroup(*[Dot(p, radius=0.06, color=NO) for p in pts])
        lines = VGroup(
            wrapped_label(r"\textbf{RPKI}: \ address holders sign \textbf{ROAs}, \ ``AS 1000 may announce "
                  r"\texttt{208.65.152.0/22}, \ no longer than /22''", 6.4, font_size=19, color=WHITE),
            wrapped_label(r"a validating AS drops announcements a ROA makes invalid", 6.4, font_size=19, color=YES),
            wrapped_label(r"protection grows faster than adoption: \ one validator on the path is enough", 6.4, font_size=19,
                  color=HEAD),
            wrapped_label(rf"if only the 25 transit providers validate: \ {b['transit_only']:.0%} hijacked".replace("%", r"\%"),
                  6.4, font_size=19, color=YES),
            wrapped_label(r"origin validation stops this mistake, \ not a forged path: \ BGPsec and ASPA aim at that",
                  6.4, font_size=19, color=KERN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([3.5, 0.0, 0])
        lines.move_to([3.6, 0.0, 0])
        with self.voiceover(
            "The defence is cryptography, from Part 30. <bookmark mark='a'/> Through the resource public key "
            "infrastructure, the holder of an address block signs a statement: this system may originate this "
            "prefix, and nothing longer. <bookmark mark='b'/> A system that validates drops any announcement such a "
            "statement contradicts. <bookmark mark='c'/> How many must validate? Choosing validators at random on our "
            "internet, a quarter of systems validating protects about half the rest, because one validator on a path "
            "is enough to stop the bad route spreading. <bookmark mark='d'/> And if the twenty-five transit networks "
            "validate, no stub is fooled at all. <bookmark mark='e'/> Origin validation stops mistakes like Pakistan "
            "Telecom's, but not a deliberate forgery of the path, which newer proposals aim at."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(Create(cv), FadeIn(dots), FadeIn(lines[2]), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(lines[3]))
            vo.wait_until("e")
            self.play(FadeIn(lines[4]))
        self.wait(0.3)
        self.clear_scene()


_ = (KERN,)
