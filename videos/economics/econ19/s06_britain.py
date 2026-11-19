from __future__ import annotations

from videos.economics.econ19.common import *  # noqa: F403

CASE = "#7BD88F"
CRIT = "#F29E8E"


def argument(title, who, case, critics, color, width=12.4):
    head = VGroup(label(title, font_size=30, color=color), label(who, font_size=20, color=GREY_A)).arrange(
        DOWN, buff=0.12)
    a = VGroup(label(r"the best case", font_size=21, color=CASE),
               *[label(c, font_size=21, color=WHITE) for c in case]).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
    b = VGroup(label(r"the critics", font_size=21, color=CRIT),
               *[label(c, font_size=21, color=GREY_A) for c in critics]).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
    for g in (a, b):
        for r in g:
            if r.width > width / 2 - 0.4:
                r.width = width / 2 - 0.4
    body = VGroup(a, b).arrange(RIGHT, buff=0.6, aligned_edge=UP)
    return VGroup(head, body).arrange(DOWN, buff=0.5)


class Britain(VoiceoverScene):
    def construct(self):
        card(self, 5, r"Why 1760, \ and why Britain?", r"Three famous answers: \ prices, \ ideas and institutions. \ "
             r"What is the best case for each, \ and what do the critics say?", "Chapter five. Why 1760, and why "
             "Britain?", lit={1688: r"the Glorious Revolution", 1764: r"the spinning jenny", 1776: r"Watt's engine"},
             scale=("firm", "nation"), horizon=("a century",))
        self.overview()
        self.prices()
        self.ideas()
        self.institutions()

    def overview(self):
        cards = point_cards([
            (r"prices", r"dear labour, \ cheap coal: \\ machines paid \ (Allen)", WAGE),
            (r"ideas", r"a culture of useful \\ knowledge \ (Mokyr)", EDU),
            (r"institutions", r"Parliament, \ property \\ and credit \ (North and Weingast)", TECH),
        ], width=12.6, cols=3, font_size=23).move_to(DOWN * 0.2)
        head = label(r"spinning jennies, \ water frames, \ steam engines: \ why there, \ why then?", font_size=27,
                     color=E.ACCENT).to_edge(UP, buff=0.6)
        with self.voiceover(
            "From the 1760s a run of inventions in Britain, the spinning jenny, the water frame, Watt's steam engine, "
            "began to change how cloth, iron and power were made. Why there, and why then? <bookmark mark='a'/> Three "
            "answers dominate. One is prices: labour was dear and coal was cheap. One is ideas: a culture that "
            "prized useful knowledge. <bookmark mark='b'/> And one is institutions: a Parliament that protected "
            "property and made credit cheap. Each has a best case, and each has critics."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cards.cards[0], shift=UP * 0.1))
            vo.wait_until("a")
            self.play(FadeIn(cards.cards[1], shift=UP * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(cards.cards[2], shift=UP * 0.1))
        self.clear_scene()

    def prices(self):
        g = argument(r"prices: \ dear labour, \ cheap coal", r"Robert Allen, \emph{The British Industrial Revolution "
                     r"in Global Perspective} (2009)",
                     [r"British wages were high, \ and coal near the towns cheap", r"a machine that saved labour and "
                      r"burned coal \\ paid in Britain, \ not in France or India", r"so inventing it paid there first"],
                     [r"Jane Humphries: \ the spinners replaced were \\ women and children, \ paid little",
                      r"the Dutch had high wages too, \ and no revolution", r"Kelly, \ Mokyr and Ó Gráda: \ British "
                      r"workers \\ were also taller, \ better fed and more skilled"], WAGE).move_to(DOWN * 0.1)
        tag = published_tag(r"Allen (2009); \ Humphries, EcHR 66(3) (2013); \ Kelly, Mokyr and Ó Gráda, Annu.\ Rev.\ "
                            r"Econ.\ 6 (2014)", corner=DR, font_size=11)
        with self.voiceover(
            "Robert Allen's answer is prices. <bookmark mark='a'/> British wages, he showed, were high by the "
            "standards of the time, and coal near the towns was cheap. A machine that saved labour and burned coal "
            "paid in Britain, but not in France, where labour was cheaper, or in India. So the inventions that "
            "needed years of costly tinkering were worth making there first. <bookmark mark='b'/> The critics: Jane "
            "Humphries pointed out that the spinners the new machines replaced were mostly women and children, who "
            "were not well paid. The Dutch had high wages too, and no industrial revolution. And Morgan Kelly, Joel "
            "Mokyr and Cormac Ó Gráda argued that British workers were also unusually well fed and skilled, which "
            "made the machines possible to build and run."
        ) as vo:
            self.play(FadeIn(g[0]), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(g[1][0], shift=UP * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(g[1][1], shift=UP * 0.1))
        self.clear_scene()

    def ideas(self):
        g = argument(r"ideas: \ a culture of growth", r"Joel Mokyr, \emph{The Enlightened Economy} (2009); \ "
                     r"\emph{A Culture of Growth} (2016)",
                     [r"an industrial Enlightenment: \ knowledge \\ should be useful, \ and shared", r"scientists, "
                      r"engineers and craftsmen \\ in conversation \ (the Lunar Society)", r"a market for ideas "
                      r"across Europe; \\ in Britain, \ the most skilled mechanics"],
                     [r"culture is hard to measure, \ and easy \\ to fit after the fact", r"France had an "
                      r"Enlightenment, \\ and industrialized later", r"why the 1760s, \ if the ideas were older?"],
                     EDU).move_to(DOWN * 0.1)
        tag = published_tag(r"Mokyr (2009, 2016)", corner=DR, font_size=13)
        with self.voiceover(
            "Joel Mokyr's answer is ideas. <bookmark mark='a'/> Europe's Enlightenment, he argues, included an "
            "industrial Enlightenment: the belief that knowledge should be useful, and shared. Scientists, engineers "
            "and craftsmen talked to one another, in places like Birmingham's Lunar Society, where Watt and his "
            "partner Matthew Boulton met chemists and potters. And Britain had the most skilled mechanics to turn "
            "ideas into machines. <bookmark mark='b'/> The critics: culture is hard to measure, and easy to fit "
            "after the fact. France had an Enlightenment too, and industrialized later. And if the ideas were older, "
            "why did the take-off wait for the 1760s?"
        ) as vo:
            self.play(FadeIn(g[0]), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(g[1][0], shift=UP * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(g[1][1], shift=UP * 0.1))
        self.clear_scene()

    def institutions(self):
        g = argument(r"institutions: \ Parliament and credit", r"Douglass North and Barry Weingast, \ JEH 49(4) (1989)",
                     [r"after 1688 Parliament controlled \\ taxes and the king's borrowing", r"a government that "
                      r"could not seize \\ or default at will", r"cheaper public debt, \ safer property: \\ room to "
                      r"invest"],
                     [r"Gregory Clark: \ private interest rates \\ and land returns show no break at 1688",
                      r"government borrowing stayed dear \\ for decades", r"good institutions are needed, \\ but "
                      r"did they decide the timing?"], TECH).move_to(DOWN * 0.1)
        tag = published_tag(r"North and Weingast, JEH 49(4) (1989); \ Clark, J.\ Interdiscip.\ Hist.\ 26(4) (1996)",
                            corner=DR, font_size=12)
        foot = label(r"most historians now combine them: \ prices made it pay, \ skills and ideas made it possible",
                     font_size=22, color=E.ACCENT).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Douglass North and Barry Weingast's answer is institutions. <bookmark mark='a'/> After the Glorious "
            "Revolution of 1688, Parliament controlled taxes and the crown's borrowing. A government that could no "
            "longer seize property or default at will could borrow more cheaply, and owners could invest without "
            "fear. <bookmark mark='b'/> The critics: Gregory Clark found no break at 1688 in private interest rates "
            "or the returns on land, and the government's own borrowing stayed expensive for decades. Institutions "
            "matter, but did they decide the timing? <bookmark mark='c'/> Most historians now combine the answers: "
            "prices made the machines pay, and skills and ideas made them possible."
        ) as vo:
            self.play(FadeIn(g[0]), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(g[1][0], shift=UP * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(g[1][1], shift=UP * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()
