from __future__ import annotations

from videos.economics.econ28.common import *  # noqa: F403


class Fixes(VoiceoverScene):
    def construct(self):
        card(self, 11, r"The fixes: \ conservative bankers, \ independence, \ targets", r"How do you make a promise "
             r"of low inflation believable?", "Chapter eleven. The fixes: conservative bankers, independence, "
             "targets.", lit={1985: r"Rogoff", 1990: r"New Zealand"}, scale=("nation", "world"),
             horizon=("decades",))
        self.rogoff()
        self.independence()

    def rogoff(self):
        B = load("bg")
        R = B["rogoff"]
        ax = plane([0, 1.5], [3, 6], center=LEFT * 2.2 + DOWN * 0.3, x_length=7.0, y_length=4.8,
                   xticks=[0, 0.5, 1.0, 1.5], yticks=[3, 4, 5, 6], xlabel=r"the banker's weight on output, $w$",
                   ylabel=r"society's expected loss", xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", font_size=15)
        curve = path(ax, R["w"], R["loss"], color=CB, width=4, yr=(3, 6))
        society = seg(ax, B["lam"], 3, B["lam"], 6, color=GREY_B, width=2, dashed=True)
        best = dot(ax, R["best"], R["best_loss"], color=OUTPUT, r=0.1)
        side = VGroup(
            label(r"Rogoff, \ 1985: \ appoint a banker \\ who cares less about output \\ than society does",
                  font_size=19, color=CB),
            label(rf"society's own weight ($w = {B['lam']:.0f}$): \\ loss {R['loss_at_lam']:.1f}", font_size=19,
                  color=GREY_A),
            label(rf"a pure inflation hawk ($w = 0$): \\ loss {R['loss_at_zero']:.1f}", font_size=19, color=INFL),
            label(rf"best: \ $w = {R['best']:.2f}$, \ loss {R['best_loss']:.2f}", font_size=21, color=OUTPUT),
            label(r"less inflation bias, \\ at the price of steadying \\ output less after shocks", font_size=19,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.3)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Kenneth Rogoff proposed one fix in 1985. <bookmark mark='a'/> Appoint a central banker who cares less "
            "about output than society does. Add supply shocks to the Island's game, and plot society's expected "
            "loss against the banker's weight on output. <bookmark mark='b'/> A banker who shares society's tastes "
            f"leaves the full inflation bias: a loss of {R['loss_at_lam']:.1f}. <bookmark mark='c'/> A pure "
            f"inflation hawk, who ignores output entirely, removes the bias but lets every shock hit output: "
            f"{R['loss_at_zero']:.1f}. <bookmark mark='d'/> The best appointment is in between: a banker with about "
            f"{R['best']:.1f} of society's concern for output, and a loss of {R['best_loss']:.1f}. "
            "<bookmark mark='e'/> Conservative, but not fanatical."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(curve), FadeIn(side[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(society), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(GrowFromCenter(best), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def independence(self):
        rows = VGroup(
            label(r"independence: \ put the banker out of the government's reach", font_size=25, color=E.ACCENT),
            label(r"Alesina and Summers, \ 1993: \ rich countries with more independent central banks had lower "
                  r"inflation, \ and no worse growth or unemployment", font_size=21, color=CB),
            label(r"a correlation: \ countries that wanted low inflation also chose independence", font_size=21,
                  color=HOLD),
            label(r"inflation targets: \ New Zealand, \ 1990: \ a number, \ a deadline, \ a governor accountable "
                  r"for both", font_size=21, color=OUTPUT),
            label(r"then Canada, \ Britain, \ Sweden, \ ...; \ the Federal Reserve named 2\% in 2012", font_size=21,
                  color=GREY_A),
            label(r"a target turns a vague promise into one the public can check", font_size=23, color=EXPECT),
        ).arrange(DOWN, buff=0.4).move_to(UP * 0.1)
        tag = published_tag(r"Rogoff, \ QJE 100(4) (1985); \ Alesina and Summers, \ JMCB 25(2) (1993); \ the Reserve "
                            r"Bank of New Zealand Act 1989", corner=DR, font_size=12)
        with self.voiceover(
            "The other fix is independence. Put the central bank out of the government's reach, "
            "so that nobody facing an election can order a surprise. <bookmark mark='b'/> Alberto Alesina and "
            "Lawrence Summers found in 1993 that rich countries with more independent central banks had lower "
            "inflation, and no worse growth or unemployment. <bookmark mark='c'/> It is a correlation: countries "
            "that wanted low inflation may also have been the ones that chose independence. "
            "<bookmark mark='d'/> Then came targets. In 1990 New Zealand gave its central bank a number, a deadline "
            "and a governor accountable for both. <bookmark mark='e'/> Canada, Britain, Sweden and dozens more "
            "followed, and the Federal Reserve named two percent in 2012. <bookmark mark='f'/> A target turns a "
            "vague promise into one the public can check, year by year."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("bcdef", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()
