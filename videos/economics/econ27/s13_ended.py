from __future__ import annotations

from videos.economics.econ27.common import *  # noqa: F403


class Ended(VoiceoverScene):
    def construct(self):
        card(self, 11, r"What ended the Depression?", r"Gold, \ money, \ or war?", "Chapter eleven. What ended the "
             "Depression?", lit={1985: r"Eichengreen and Sachs", 1992: r"Romer"}, scale=("nation", "world"),
             horizon=("a decade",))
        self.gold()
        self.money()
        self.war()

    def gold(self):
        rows = VGroup(
            label(r"the gold standard: \ every currency convertible into gold at a fixed price", font_size=23,
                  color=COUPON),
            label(r"to defend it, \ a central bank losing gold must raise rates and shrink its money", font_size=23,
                  color=PRICE),
            label(r"Britain left in September 1931; \ the United States in 1933; \ France and the gold bloc held "
                  r"on until 1936", font_size=22, color=GREY_A),
            label(r"Eichengreen and Sachs, \ 1985: \ the earlier a country left gold, \ the sooner it recovered",
                  font_size=23, color=OUTPUT),
            label(r"\emph{Golden Fetters} (1992): \ the gold standard spread the Depression and held countries in it",
                  font_size=22, color=E.ACCENT),
        ).arrange(DOWN, buff=0.45).move_to(UP * 0.1)
        tag = published_tag(r"Eichengreen and Sachs, \ JEH 45(4) (1985): \ 925--946; \ Eichengreen, \emph{Golden "
                            r"Fetters} (1992)", corner=DR, font_size=12)
        with self.voiceover(
            "What ended the Depression? The first answer is gold. <bookmark mark='a'/> Under the gold standard, "
            "every currency could be converted into gold at a fixed price. <bookmark mark='b'/> A central bank that "
            "was losing gold had to defend that price by raising interest rates and shrinking its money, in the "
            "middle of a slump. <bookmark mark='c'/> Britain left gold in September 1931. The United States left "
            "in 1933. France and the countries of the gold bloc held on until 1936. <bookmark mark='d'/> Barry "
            "Eichengreen and Jeffrey Sachs showed in 1985 that the earlier a country left gold, the sooner it "
            "recovered. <bookmark mark='e'/> In Eichengreen's phrase, gold was a set of golden fetters: it spread "
            "the Depression from country to country, and held each one in it."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def money(self):
        g = load("gold")
        ax = plane([1929, 1942], [0, 25], center=LEFT * 1.8 + DOWN * 0.3, x_length=8.4, y_length=4.8,
                   xticks=[1929, 1931, 1933, 1935, 1937, 1939, 1941], yticks=[0, 5, 10, 15, 20, 25],
                   ylabel=r"US monetary gold stock, \ billions of dollars", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:.0f}", font_size=16)
        gl = path(ax, g["t"], g["gold"], color=COUPON, width=3, smooth=False)
        scale_ip = 25 / 13.0
        ipl = path(ax, g["ip_t"], [v * scale_ip for v in g["ip"]], color=OUTPUT, width=3, smooth=False)
        side = VGroup(
            label(rf"gold: \ \${g['gold_1933']:.1f} billion in March 1933", font_size=20, color=COUPON),
            label(rf"1934: \ revalued from \$20.67 to \$35 an ounce: \\ \${g['gold_1934']:.1f} billion", font_size=19,
                  color=COUPON),
            label(rf"then gold flowed in from Europe: \\ \${g['gold_1941']:.1f} billion by 1941", font_size=20,
                  color=COUPON),
            label(r"green: \ industrial production \\ (scaled)", font_size=19, color=OUTPUT),
            label(r"Romer, \ 1992: \ nearly all the recovery \\ before 1942 came from money", font_size=20,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.3)
        tag = data_tag(r"NBER Macrohistory Database: \ monetary gold stock; \ Federal Reserve: \ industrial "
                       r"production; \ via FRED", corner=DR, font_size=12)
        with self.voiceover(
            "The second answer is money, and in America the money came from gold. <bookmark mark='a'/> In March "
            f"1933, the country's gold stock was worth about {g['gold_1933']:.0f} billion dollars. "
            "<bookmark mark='b'/> In January 1934, the government raised the price of gold from twenty dollars and "
            f"sixty-seven cents an ounce to thirty-five, and the same gold was worth {g['gold_1934']:.0f} billion. "
            "<bookmark mark='c'/> Then gold poured in, as Europe's savers fled the threat of war, to about "
            f"{g['gold_1941']:.0f} billion by 1941. The Treasury let it swell the money supply. "
            "<bookmark mark='d'/> In green, industrial production, rising with it, apart from the slump of 1937, "
            "when the Federal Reserve and the Treasury tightened. <bookmark mark='e'/> Christina Romer estimated in "
            "1992 that nearly all of America's recovery before 1942 came from this monetary expansion, through "
            "lower real interest rates, and very little from fiscal policy, which was never large."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(gl), run_time=1.5)
            for mk, r_ in zip("abc", side[:3]):
                vo.wait_until(mk)
                self.play(FadeIn(r_))
            vo.wait_until("d")
            self.play(Create(ipl), FadeIn(side[3]), run_time=1.5)
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def war(self):
        f = load("film")
        d = load("depression")
        rows = VGroup(
            label(r"and then the war", font_size=28, color=E.ACCENT),
            label(rf"industrial production: \ {f['peak29']:.1f} in 1929, \ {f['peak_war']:.1f} at the wartime peak "
                  r"\ (2017 $= 100$)", font_size=23, color=OUTPUT),
            label(r"unemployment fell to the lowest rates on record", font_size=23, color=OUTPUT),
            label(r"the biggest fiscal expansion in American history, \ financed partly by money", font_size=23,
                  color=GOV),
            label(r"Keynes's theory, \ tested by accident, \ at a scale no peacetime government would have tried",
                  font_size=22, color=E.ACCENT),
            label(rf"and still: \ output had passed 1929's level by {d['gnp_back']}, \ before any war spending",
                  font_size=22, color=HOLD),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.1)
        tag = data_tag(r"Federal Reserve: \ industrial production; \ BEA: \ real GNP; \ via FRED", corner=DR,
                       font_size=12)
        with self.voiceover(
            "And then the war. <bookmark mark='a'/> American industrial production, which had been "
            f"{f['peak29']:.0f} in 1929 on today's index, reached about {f['peak_war']:.0f} at its wartime peak, "
            "more than double. <bookmark mark='b'/> Unemployment fell to the lowest rates on record. "
            "<bookmark mark='c'/> It was the biggest fiscal expansion in American history, paid for partly by "
            "borrowing from the banking system. <bookmark mark='d'/> Keynes's theory was tested by accident, at a "
            "scale no peacetime government would have tried. <bookmark mark='e'/> But the order of events matters. "
            f"Output had already passed its 1929 level by {d['gnp_back']}, before any war spending. Gold and money "
            "did the first part of the work; the war finished it."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()
