from __future__ import annotations

from videos.economics.econ33.common import *  # noqa: F403

EVENTS = [
    (2007 + 220 / 365, r"9 Aug 2007: \ BNP Paribas freezes three funds", r"BNP Paribas"),
    (2008 + 75 / 365, r"16 Mar 2008: \ Bear Stearns sold, \ with Fed support", r"Bear Stearns"),
    (2008 + 250 / 365, r"7 Sep: \ Fannie Mae and Freddie Mac taken over", r"Fannie, \ Freddie"),
    (2008 + 258 / 365, r"15 Sep: \ Lehman Brothers files for bankruptcy", r"Lehman"),
    (2008 + 259 / 365, r"16 Sep: \ AIG rescued; \ a money fund breaks the buck", r"AIG"),
    (2008 + 276 / 365, r"3 Oct: \ TARP, \ \$700 billion, \ becomes law", r"TARP"),
]


class GFC(VoiceoverScene):
    def construct(self):
        card(self, 7, r"2008 in order", r"What happened, and in what order?", "Chapter seven. 2008 in order.",
             lit={2006: r"house prices peak", 2008: r"Lehman"}, scale=("household", "market", "world"),
             horizon=("a day", "a year"))
        self.houses()
        self.chain()
        self.the_run()
        self.fed()

    def houses(self):
        G = load("gfc")
        ax = plane([2000, 2013], [80, 200], center=LEFT * 3.3 + DOWN * 0.3, x_length=5.6, y_length=4.4,
                   xticks=[2000, 2004, 2008, 2012], yticks=[100, 150, 200], ylabel=r"house prices, \ Jan 2000 = 100",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=14)
        ax2 = plane([2000, 2013], [0, 12], center=RIGHT * 3.3 + DOWN * 0.3, x_length=5.6, y_length=4.4,
                    xticks=[2000, 2004, 2008, 2012], yticks=[0, 4, 8, 12],
                    ylabel=r"mortgages 30+ days late, \ \% (banks)", xfmt=lambda v: f"{v:.0f}",
                    yfmt=lambda v: f"{v:.0f}", font_size=14)
        cs = path(ax, G["cs_t"], G["cs"], HOUSE, 3.3, xr=(2000, 2013), smooth=False)
        dq = path(ax2, G["dq_t"], G["dq"], CRISIS, 3.3, xr=(2000, 2013), smooth=False)
        k1 = label(rf"peak {G['cs_peak_date'][:4]}, \ then $-{G['cs_fall']:.0f}\%$ to {G['cs_trough_date'][:4]}",
                   font_size=17, color=HOUSE).next_to(ax, UP, buff=0.1)
        k2 = label(rf"{G['dq_2005']:.1f}\% in 2005, \ {G['dq_peak']:.1f}\% in {G['dq_peak_date'][:4]}",
                   font_size=17, color=CRISIS).next_to(ax2, UP, buff=0.1)
        head = label(r"1. \ houses", font_size=26, color=E.ACCENT).to_edge(UP, buff=0.3)
        tag = data_tag(r"S\&P CoreLogic Case-Shiller; \ Federal Reserve Board; \ via FRED", corner=DR, font_size=12)
        with self.voiceover(
            "In order, then. First, houses. <bookmark mark='a'/> American house prices rose for a decade, faster "
            "after 2002, with mortgages offered to borrowers with little income or deposit and teaser rates that "
            f"reset higher after two years. They peaked in {G['cs_peak_date'][:4]} and fell "
            f"{G['cs_fall']:.0f} percent by {G['cs_trough_date'][:4]}. <bookmark mark='b'/> As rates reset and "
            "prices fell, borrowers who could no longer refinance stopped paying. At commercial banks, the share of "
            f"mortgages at least a month late went from {G['dq_2005']:.1f} percent in 2005 to "
            f"{G['dq_peak']:.1f} percent in {G['dq_peak_date'][:4]}. This was a large loss, but not, by itself, a "
            "large enough one to sink the world's financial system. What turned it into a crisis was where the "
            "losses sat."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(ax2), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(cs), FadeIn(k1), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(dq), FadeIn(k2), run_time=2.0)
        self.clear_scene()

    def chain(self):
        ch = flow_chain([(r"mortgages", HOUSE), (r"pooled into securities", CREDIT),
                         (r"sliced into tranches, \ the top rated AAA", RATE),
                         (r"held by banks and their vehicles", BANK), (r"funded overnight: \ repo, \ commercial "
                                                                      r"paper", CRISIS)],
                        box_w=2.35, box_h=1.35, buff=0.42, font_size=20,
                        notes=[r"originated \\ to be sold", r"cash flows \\ combined", r"losses hit \\ the bottom "
                               r"first", r"with thin capital", r"lenders could \\ leave any day"],
                        note_size=16).move_to(DOWN * 0.1)
        head = label(r"2. \ where the losses sat", font_size=26, color=E.ACCENT).to_edge(UP, buff=0.4)
        foot = label(r"long-term, \ hard-to-value assets, \ funded with money that could run: \ a bank without "
                     r"deposit insurance (Part 26)", font_size=21, color=WHITE).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Second, where the losses sat. <bookmark mark='a'/> Mortgages were made to be sold. <bookmark mark='b'/> "
            "They were pooled into securities, <bookmark mark='c'/> and the securities sliced into tranches: the "
            "bottom slices absorbed the first losses, so the top slices, rated triple A, looked safe. "
            "<bookmark mark='d'/> Banks, and vehicles they set up off their balance sheets, held these securities "
            "with very little capital, <bookmark mark='e'/> and funded them with short-term borrowing, overnight "
            "repurchase agreements and commercial paper, from lenders who could leave on any day. "
            "<bookmark mark='f'/> Long-term assets that were hard to value, funded with money that could run, and no "
            "deposit insurance: a bank, built outside the rules for banks, open to the run of Part twenty-six."
        ) as vo:
            self.play(FadeIn(head))
            for mk, k in zip("abcde", range(5)):
                vo.wait_until(mk)
                anims = [FadeIn(ch.boxes[k], shift=RIGHT * 0.1), FadeIn(ch.notes[k])]
                if k:
                    anims.append(GrowArrow(ch.arrows[k - 1]))
                self.play(*anims)
            vo.wait_until("f")
            self.play(FadeIn(foot))
        self.clear_scene()

    def the_run(self):
        G = load("gfc")
        ax = plane([2007, 2009.5], [0, 7], center=LEFT * 2.5 + DOWN * 0.6, x_length=7.6, y_length=4.2,
                   xticks=[2007, 2007.5, 2008, 2008.5, 2009, 2009.5], yticks=[0, 2, 4, 6],
                   ylabel=r"spreads, \ percentage points \ (monthly averages)",
                   xfmt=lambda v: f"{v:.0f}" if v == int(v) else "", yfmt=lambda v: f"{v:.0f}", font_size=14)
        ted = path(ax, G["ted_t"], G["ted"], CRISIS, 3.2, xr=(2007, 2009.5), smooth=False)
        baa = path(ax, G["baa_t"], G["baa"], HOUSE, 3.2, xr=(2007, 2009.5), smooth=False)
        key = VGroup(label(r"red: \ the TED spread: \ banks' lending to each other", font_size=17, color=CRISIS),
                     label(r"gold: \ companies' Baa bonds over Treasuries", font_size=17, color=HOUSE)).arrange(
            RIGHT, buff=0.5).next_to(ax, UP, buff=0.15)
        marks = VGroup()
        texts = VGroup()
        for k, (t, txt, short) in enumerate(EVENTS):
            marks.add(vline(ax, t, 0, 7, GREY_B, 1.5))
            texts.add(label(txt, font_size=17, color=WHITE))
        texts.arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_edge(RIGHT, buff=0.2).shift(UP * 0.2)
        if texts.get_left()[0] < ax.get_right()[0] + 0.2:
            texts.width = 6.9 - (ax.get_right()[0] + 0.25)
            texts.to_edge(RIGHT, buff=0.2)
        head = label(r"3. \ the run", font_size=26, color=E.ACCENT).to_edge(UP, buff=0.25)
        tag = data_tag(r"FRED: \ TEDRATE, \ BAA10Y", corner=DR, font_size=12)
        with self.voiceover(
            "Third, the run. <bookmark mark='a'/> On the ninth of August 2007 the French bank BNP Paribas froze "
            "three funds, saying it could no longer value their American mortgage securities. Lenders everywhere "
            "began to ask what was in each other's books, and the TED spread, the premium banks pay to borrow from "
            "each other, jumped. <bookmark mark='b'/> In March 2008 Bear Stearns, unable to roll over its "
            "borrowing, was sold to JPMorgan with help from the Federal Reserve. <bookmark mark='c'/> In September "
            "the government took over Fannie Mae and Freddie Mac. <bookmark mark='d'/> On the fifteenth, Lehman "
            "Brothers filed for bankruptcy, the largest in American history, with six hundred and thirty-nine "
            "billion dollars of assets. <bookmark mark='e'/> The next day the Fed rescued the insurer AIG, and a "
            "money market fund holding Lehman's paper broke the buck, setting off a run on money funds. "
            f"<bookmark mark='f'/> The TED spread reached {G['ted_peak']:.1f} points on the tenth of October. "
            "Corporate bond spreads went on rising into December. Congress passed the Troubled Asset Relief Program "
            "on the third of October. This is what the Queen was asking about."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(tag), FadeIn(key))
            self.play(Create(baa), run_time=1.0)
            for mk, k in zip("abcde", range(5)):
                vo.wait_until(mk)
                if k == 0:
                    self.play(Create(ted), FadeIn(marks[0]), FadeIn(texts[0]), run_time=1.6)
                elif k == 4:
                    self.play(FadeIn(marks[4]), FadeIn(texts[4]))
                else:
                    self.play(FadeIn(marks[k]), FadeIn(texts[k]))
            vo.wait_until("f")
            self.play(FadeIn(marks[5]), FadeIn(texts[5]))
        self.clear_scene()

    def fed(self):
        G = load("gfc")
        ax = plane([2007, 2011], [0, 2.6], center=LEFT * 1.8 + DOWN * 0.4, x_length=8.8, y_length=4.4,
                   xticks=[2007, 2008, 2009, 2010, 2011], yticks=[0, 0.5, 1.0, 1.5, 2.0, 2.5],
                   ylabel=r"the Federal Reserve's assets, \ \$ trillion", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:.1f}", font_size=14)
        w = path(ax, G["wal_t"], G["wal"], CB, 3.5, xr=(2007, 2011), smooth=False)
        side = VGroup(
            label(rf"10 Sep 2008: \ \${G['wal_before']:.2f} trillion", font_size=20, color=CB),
            label(rf"17 Dec 2008: \ \${G['wal_after']:.2f} trillion", font_size=20, color=CB),
            label(r"lending to banks, \ dealers, \\ money funds, \ commercial paper \\ and foreign central banks",
                  font_size=19, color=GREY_A),
            label(r"the lender of last resort \\ for a system, \ not a bank \\ (chapter 11)", font_size=19,
                  color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        tag = data_tag(r"Board of Governors (H.4.1), \ via FRED: \ WALCL", corner=DR, font_size=12)
        head = label(r"4. \ the response", font_size=26, color=E.ACCENT).to_edge(UP, buff=0.3)
        with self.voiceover(
            "Fourth, the response. <bookmark mark='a'/> In the fourteen weeks after Lehman, the Federal Reserve's "
            f"balance sheet went from {G['wal_before']:.2f} to {G['wal_after']:.2f} trillion dollars. "
            "<bookmark mark='b'/> It lent to banks, to securities dealers, to money market funds, to companies "
            "through the commercial paper market, and to foreign central banks short of dollars. "
            "<bookmark mark='c'/> Walter Bagehot's lender of last resort, from Part twenty-six, acting for a whole "
            "system rather than one bank. How well that worked, and what it cost, is chapter eleven."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(w), FadeIn(side[0]), FadeIn(side[1]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(side[2]))
            vo.wait_until("c")
            self.play(FadeIn(side[3]))
        self.clear_scene()
