from __future__ import annotations

from videos.economics.econ34.common import *  # noqa: F403

CC = {"USA": (USD, r"the United States"), "CHN": (CNY, r"China"), "DEU": (DEM, r"Germany"), "JPN": (CALM, r"Japan")}


class Imbalances(VoiceoverScene):
    def construct(self):
        card(self, 11, r"Global imbalances", r"Why does the richest country borrow from the rest of the world?",
             "Chapter eleven. Global imbalances.", lit={1965: r"`exorbitant privilege'", 2005: r"the saving glut"},
             scale=("nation", "world"), horizon=("a decade",))
        self.chart()
        self.privilege()

    def chart(self):
        I = load("imbalances")
        ax = plane([1980, 2026], [-8, 12], center=LEFT * 1.8 + DOWN * 0.4, x_length=8.8, y_length=4.6,
                   xticks=[1980, 1990, 2000, 2010, 2020], yticks=[-8, -4, 0, 4, 8, 12],
                   ylabel=r"current account, \ \% of GDP", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:+.0f}" if v else "0", font_size=14)
        zero = seg(ax, 1980, 0, 2026, 0, GREY_C, 1.2)
        lines = {c: path(ax, I[c]["year"], I[c]["value"], col, 3.0, smooth=False) for c, (col, _) in CC.items()}
        key = VGroup(*[label(n, font_size=16, color=col) for c, (col, n) in CC.items()]).arrange(RIGHT, buff=0.4)
        key.next_to(ax, UP, buff=0.12)
        side = VGroup(
            label(rf"China: \ {I['chn2007']:+.0f}\% in 2007", font_size=19, color=CNY),
            label(rf"America: \ {I['usa2006']:+.1f}\% in 2006", font_size=19, color=USD),
            label(rf"Germany: \ {I['deu2015']:+.0f}\% in 2015", font_size=19, color=DEM),
            label(r"Bernanke, \ 2005: \\ a global saving glut, \\ not only American \\ profligacy", font_size=18,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.3)
        tag = data_tag(r"World Bank, \ WDI: \ BN.CAB.XOKA.GD.ZS", corner=DR, font_size=12)
        with self.voiceover(
            "Chapter one's identity says a deficit is investment above saving. Across the world, the deficits and "
            "surpluses must match. <bookmark mark='a'/> In the 2000s they grew large: America's deficit reached "
            f"{abs(I['usa2006']):.1f} percent of GDP in 2006; <bookmark mark='b'/> China's surplus "
            f"{I['chn2007']:.0f} percent in 2007; <bookmark mark='c'/> and later Germany's "
            f"{I['deu2015']:.0f} percent, in 2015. <bookmark mark='d'/> Was America spending too much, or the rest "
            "of the world saving too much? In March 2005 Ben Bernanke, then a Fed governor, argued the second: a "
            "global saving glut, as Asian economies built reserves after 1997 and oil exporters saved their "
            "windfalls, pushed money into American assets and held down interest rates, which fed the housing boom "
            "of Part thirty-three."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(zero), FadeIn(key), FadeIn(tag))
            self.play(*[Create(ln) for ln in lines.values()], run_time=2.0)
            for mk, r_ in zip("abcd", side):
                vo.wait_until(mk)
                self.play(FadeIn(r_))
        self.clear_scene()

    def privilege(self):
        B = load("bop")
        rows = VGroup(
            label(r"the `exorbitant privilege': \ Val\'ery Giscard d'Estaing, \ in the 1960s", font_size=25,
                  color=E.ACCENT),
            label(r"America borrows in its own currency, \ cheaply, \ in safe assets the world wants", font_size=23,
                  color=USD),
            label(r"and earns more on its foreign assets \ (shares, \ firms) \ than it pays on its debts \ "
                  r"(Treasury bills)", font_size=22, color=WHITE),
            label(rf"its net position: \ {B['niip_last']:.0f}\% of GDP; \ the world's banker, \ and its insurer: \ "
                  r"in a crisis it pays out", font_size=22, color=CRISIS),
            label(r"the safe-asset shortage: \ when the world wants safety, \ it buys dollars", font_size=22,
                  color=CALM),
        ).arrange(DOWN, buff=0.45).move_to(UP * 0.1)
        tag = published_tag(r"Gourinchas and Rey, \ in Clarida (ed.), \ \emph{G7 Current Account Imbalances} (2007); "
                            r"\ Caballero, \ Farhi and Gourinchas (2017)", corner=DR, font_size=12)
        with self.voiceover(
            "America's position has a peculiar feature. <bookmark mark='a'/> In the 1960s the French finance "
            "minister, Valery Giscard d'Estaing, called it an exorbitant privilege. <bookmark mark='b'/> The United "
            "States borrows in its own currency, cheaply, by selling the safe assets the rest of the world wants to "
            "hold. <bookmark mark='c'/> Pierre-Olivier Gourinchas and Helene Rey showed that it earns more on what "
            "it owns abroad, shares and firms, than it pays on what it owes, mostly safe bonds: it is the world's "
            "banker, borrowing short and safe and lending long and risky. <bookmark mark='d'/> So a net position of "
            f"minus {abs(B['niip_last']):.0f} percent of GDP costs less than it looks, and in global crises, when "
            "its risky assets fall and its safe debts rise in value, America pays out, like an insurer. "
            "<bookmark mark='e'/> Ricardo Caballero, Emmanuel Farhi and Gourinchas argue that the world is short of "
            "safe assets, and that this shortage explains low interest rates and the dollar's strength in every "
            "panic, including one that started in America."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()
