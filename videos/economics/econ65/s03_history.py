from __future__ import annotations

from videos.economics.econ65.common import *  # noqa: F403


class History(VoiceoverScene):
    def construct(self):
        card(self, 2, r"Technology and work, \ historically", r"When machines arrived before, \ what happened to the "
             r"people they replaced?", "Chapter two. Technology and work, historically.",
             lit={1811: "the Luddites", 1983: "Leontief"}, scale=("nation",), horizon=("a century",))
        self.luddites()
        self.engels()
        self.horses()
        self.atm()

    def luddites(self):
        cards = VGroup(
            history_card(r"1811--16", r"the Luddites", r"framework knitters in Nottinghamshire break the stocking "
                         r"frames that cut their piece rates; \ in 1812 Parliament makes frame-breaking a capital "
                         r"crime", color=NAIVE, width=11.4, font_size=21),
            history_card(r"1821", r"Ricardo changes his mind", r"in the third edition of his \emph{Principles} he "
                         r"adds a chapter, \ ``On Machinery'': \ the labourers' fear that machinery hurts them is "
                         r"not founded on prejudice", color=GDP, width=11.4, font_size=21),
        ).arrange(DOWN, buff=0.35).move_to(UP * 0.4)
        tag = published_tag(r"Ricardo, \ \emph{On the Principles of Political Economy and Taxation}, \ 3rd ed. "
                            r"(1821), \ ch. 31", corner=DL, font_size=12)
        with self.voiceover(
            "Machines have taken work before. <bookmark mark='a'/> Between 1811 and 1816, framework knitters in the "
            "English Midlands broke the stocking frames that were cutting their piece rates. Parliament made "
            "frame-breaking a capital crime, and sent soldiers. The word Luddite has meant a fool ever since. "
            "<bookmark mark='b'/> But in 1821 David Ricardo, the most rigorous economist of his day, added a "
            "chapter to his Principles called On Machinery. He had been wrong, he wrote: the labourers' fear that "
            "machinery would hurt them was not founded on prejudice, but on the correct principles of political "
            "economy. A machine can raise the owner's income and lower the workers', at least for a while."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(cards[0], shift=UP * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(cards[1], shift=UP * 0.1), FadeIn(tag))
        self.clear_scene()

    def engels(self):
        En = load("engels")
        ax = plane([1760, 1880], [70, 210], center=LEFT * 1.2 + DOWN * 0.3, x_length=9.0, y_length=5.0,
                   xticks=[1760, 1780, 1800, 1820, 1840, 1860, 1880], yticks=[80, 100, 120, 140, 160, 180, 200],
                   ylabel=r"index, \ 1770 = 100", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}",
                   font_size=14)
        gp = path(ax, En["year"], En["gdppc"], GDP, 3.0, smooth=False)
        rw = path(ax, En["year"], En["real_wage"], WORK, 3.0, smooth=False)
        pause = shade(ax, [(1790, 1840)], 70, 210, RECESS, 0.5)
        plab = label(r"Engels's pause", font_size=18, color=GREY_A).move_to(ax.ax.c2p(1815, 200))
        key = legend_rows([(GDP, "GDP per head"), (WORK, "a labourer's real wage")], font_size=16).next_to(
            ax.ax, RIGHT, buff=0.3).shift(UP * 1.5)
        tag = data_tag(r"Bank of England, \ \emph{A millennium of macroeconomic data}: \ England", corner=DL,
                       font_size=12)
        a40 = En["at"]["1840"]
        with self.voiceover(
            "He was right about the while. <bookmark mark='a'/> Here is England, indexed to 1770: in gold, GDP per "
            "head; in pink, a labourer's real wage. <bookmark mark='b'/> Through the decades of the new machines, "
            "output per head rose, and wages did not follow. By 1840 GDP per head was about "
            f"{a40['gdppc'] - 100:.0f} percent above its 1770 level, the real wage about "
            f"{a40['real_wage'] - 100:.0f} percent, after falling below it around 1800. Robert Allen called it "
            "Engels's pause, after the man who watched it from Manchester, and Part nineteen met it. <bookmark "
            "mark='c'/> Then wages caught up, and for a century and a half rose with output. Both halves of the "
            "story matter: the long run was good for workers, and the short run lasted a working life."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(gp), Create(rw), FadeIn(key), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(pause), FadeIn(plab))
            vo.wait_until("c")
            self.play(Indicate(rw, color=WORK, scale_factor=1.0))
        self.clear_scene()

    def horses(self):
        cards = VGroup(
            history_card(r"1910s--1960", r"the horse", r"tractors arrive on American farms; \ the horses and mules "
                         r"that pulled the ploughs, \ tens of millions of them, \ are not retrained", color=GREY_B,
                         width=11.4, font_size=21),
            history_card(r"1983", r"Leontief's warning", r"Wassily Leontief: \ people might go the way of the "
                         r"horse, \ as machines take over the work for which humans were the cheapest source of "
                         r"power and control", color=NAIVE, width=11.4, font_size=21),
            history_card(r"why not yet", r"people are not horses", r"a horse could only pull; \ people moved to tasks "
                         r"the machines could not do, \ and new tasks kept being invented", color=NEWT, width=11.4,
                         font_size=21),
        ).arrange(DOWN, buff=0.3).move_to(UP * 0.2)
        tag = published_tag(r"Leontief, \ Population and Development Review 9(3) (1983)", corner=DL, font_size=12)
        with self.voiceover(
            "There is a darker precedent. <bookmark mark='a'/> In the first half of the twentieth century, tractors "
            "replaced the horses and mules that had pulled American ploughs. There were tens of millions of them. "
            "Nobody retrained them. <bookmark mark='b'/> In 1983 Wassily Leontief, a Nobel laureate, warned that "
            "the role of humans as a factor of production might diminish in the same way. <bookmark mark='c'/> "
            "So far, people are not horses. A horse could only pull. When machines took over pulling, and then "
            "spinning and adding, people moved to tasks machines could not do, and new tasks kept being invented. "
            "Whether that remains true is the question of this part."
        ) as vo:
            for mk, c in zip("abc", cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1), *([FadeIn(tag)] if mk == "b" else []))
        self.clear_scene()

    def atm(self):
        ax = plane([-0.6, 1.6], [0, 24], center=LEFT * 3.4 + DOWN * 0.4, x_length=4.4, y_length=4.4, xticks=[],
                   yticks=[0, 5, 10, 15, 20], ylabel=r"employees per urban bank branch", yfmt=lambda v: f"{v:.0f}",
                   font_size=14)
        b = bars(ax, [0, 1], [20, 13], [GREY_B, MACH], width=0.6)
        bl = VGroup(label(r"1988", font_size=16, color=GREY_A).next_to(ax.ax.c2p(0, 0), DOWN, buff=0.15),
                    label(r"2004", font_size=16, color=GREY_A).next_to(ax.ax.c2p(1, 0), DOWN, buff=0.15))
        vals = VGroup(label(r"about 20", font_size=16, color=GREY_B).next_to(b[0], UP, buff=0.08),
                      label(r"a little over 13", font_size=16, color=MACH).next_to(b[1], UP, buff=0.08))
        side = VGroup(
            label(r"commercial bank branches, \ 1988--2006: \ $+39\%$", font_size=21, color=NEWT),
            label(r"cheaper branches, \ so more of them", font_size=19, color=GREY_A),
            label(r"the teller's job changed: \ less counting cash, \ more selling and advice", font_size=19,
                  color=WORK),
            label(r"new work: \ about 60\% of US jobs in 2018 had titles that did not exist in 1940", font_size=19,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(ax.ax, RIGHT, buff=0.8).shift(UP * 0.3)
        if side.width > 7.6:
            side.scale_to_fit_width(7.6).next_to(ax.ax, RIGHT, buff=0.8).shift(UP * 0.3)
        tag = published_tag(r"Hannan and Hanweck, \ Federal Reserve FEDS 2008-02; \ Bessen, \ \emph{Learning by "
                            r"Doing} (2015); \ Autor, \ Chin, \ Salomons and Seegmiller, \ QJE 139(3) (2024)",
                            corner=DL, font_size=12)
        with self.voiceover(
            "A modern example shows how. <bookmark mark='a'/> Cash machines spread through American banks from the "
            "nineteen-seventies. Timothy Hannan and Gerald Hanweck, at the Federal Reserve, counted the staff of a "
            "commercial bank's urban branch: about twenty in 1988, a little over thirteen by 2004. <bookmark "
            "mark='b'/> But a branch with fewer staff is cheaper to run, so banks opened more of them: between 1988 "
            "and 2006 the number of commercial bank branches rose by thirty-nine percent. <bookmark mark='c'/> James "
            "Bessen showed that the tellers' work changed with it: less counting of cash, more selling and advice. "
            "<bookmark mark='d'/> And across the economy, David Autor and coauthors find that about sixty percent of "
            "American jobs in 2018 had titles that did not exist in 1940. Machines take tasks; economies invent new "
            "ones. The economics of AI is a race between the two."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(bl), FadeIn(tag))
            vo.wait_until("a")
            self.play(GrowFromEdge(b[0], DOWN), FadeIn(vals[0]))
            self.play(GrowFromEdge(b[1], DOWN), FadeIn(vals[1]))
            for mk, r_ in zip("bcd", (side[0:2], side[2], side[3])):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.15))
        self.clear_scene()
