from __future__ import annotations

from videos.economics.econ26.common import *  # noqa: F403


class Cures(VoiceoverScene):
    def construct(self):
        card(self, 5, r"Suspension and deposit insurance", r"How do you remove the bad equilibrium?",
             "Chapter five. Suspension and deposit insurance.", lit={1933: r"the FDIC", 1983: r"Diamond and Dybvig"},
             scale=("nation",), horizon=("a year",))
        self.suspend()
        self.insure()
        self.history()

    def suspend(self):
        r = load("run")
        rows = VGroup(
            label(r"cure 1: \ suspend convertibility", font_size=28, color=E.ACCENT),
            label(r"announce: \ once a quarter of depositors have withdrawn, \ the bank pays no more until date 2",
                  font_size=22, color=GREY_A),
            label(rf"then a patient depositor who waits is sure of {r['c2_guaranteed']:.2f}, \ more than the "
                  rf"{r['run_pays']:.2f} from running", font_size=23, color=STAY),
            label(r"nobody runs, \ so the suspension is never used", font_size=24, color=STAY),
            label(r"but only if the bank knows how many truly need their money: \ if it does not, \ suspending hurts "
                  r"them", font_size=21, color=HOLD),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.1)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Diamond and Dybvig also showed how to remove the bad equilibrium. <bookmark mark='a'/> The first cure "
            "is to suspend convertibility: announce that once a quarter of the depositors have withdrawn, the share "
            "who are truly impatient, the bank will pay nothing more until the loans come due. "
            "<bookmark mark='b'/> Then a patient depositor who waits "
            f"is sure of {r['c2_guaranteed']:.2f}, more than the {r['run_pays']:.2f} that running brings. "
            "<bookmark mark='c'/> So nobody runs, and the suspension never has to be used. "
            "<bookmark mark='d'/> But it works only if the bank knows how many people genuinely need their money. "
            "If that number is uncertain, suspending can lock out people who need cash, which is what happened in "
            "the American panics of the nineteenth century."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def insure(self):
        rows = VGroup(
            label(r"cure 2: \ deposit insurance", font_size=28, color=E.ACCENT),
            label(r"the government promises every insured depositor full payment, \ whatever happens", font_size=23,
                  color=CB),
            label(r"then nobody has a reason to run, \ so the bank is never run", font_size=23, color=STAY),
            label(r"an insurance policy that is never paid out costs nothing: \ the promise does the work",
                  font_size=23, color=STAY),
            label(r"as long as it is believed, \ which needs a government that can raise the money if it must",
                  font_size=21, color=HOLD),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.1)
        with self.voiceover(
            "The second cure is deposit insurance. <bookmark mark='a'/> The government promises every insured "
            "depositor full payment, whatever happens to the bank. <bookmark mark='b'/> Then no depositor has any "
            "reason to run, so the bank is never run. <bookmark mark='c'/> And here is the remarkable part: in the "
            "model, insurance against runs is never paid out, so it costs nothing. The promise alone removes the bad "
            "equilibrium. <bookmark mark='d'/> As long as people believe it, which requires a government that could "
            "raise the money if it ever had to."
        ) as vo:
            self.play(FadeIn(rows[0]))
            for mk, r_ in zip("abcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def history(self):
        s = load("suspensions")
        ax = plane([1920.5, 1941.5], [0, 4200], center=LEFT * 1.8 + DOWN * 0.3, x_length=8.4, y_length=4.8,
                   xticks=[1922, 1926, 1930, 1934, 1938], yticks=[0, 1000, 2000, 3000, 4000],
                   ylabel=r"US commercial banks suspended, \ a year", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: commas(v), font_size=16)
        bars = VGroup()
        for y, v in zip(s["years"], s["annual"]):
            lo, hi = ax.ax.c2p(y, 0), ax.ax.c2p(y, max(v, 8))
            bars.add(Rectangle(width=0.32, height=hi[1] - lo[1], fill_color=RUN if y < 1934 else CB,
                               fill_opacity=0.8, stroke_width=0).move_to((lo + hi) / 2))
        side = VGroup(
            label(rf"1930--1933: \ {commas(s['sum_30_33'])} banks", font_size=21, color=RUN),
            label(rf"1933: \ {commas(s['y1933'])}", font_size=21, color=RUN),
            label(r"1 January 1934: \\ federal deposit insurance begins", font_size=20, color=CB),
            label(rf"1934: \ {s['y1934']}", font_size=24, color=CB),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(RIGHT, buff=0.35)
        tag = data_tag(r"Federal Reserve, \ \emph{Banking and Monetary Statistics}: \ suspensions of incorporated "
                       r"commercial banks, \ via FRED", corner=DR, font_size=12)
        with self.voiceover(
            "The cure has been tried. Here are American commercial banks suspended each year from 1921 to 1941. "
            f"<bookmark mark='a'/> From 1930 to 1933, about {s['sum_30_33']:,} banks failed or closed their doors. "
            f"<bookmark mark='b'/> In 1933 alone, {s['y1933']:,}. <bookmark mark='c'/> Federal deposit insurance "
            "began on the first of January 1934. <bookmark mark='d'/> That year, "
            f"{s['y1934']} banks were suspended. Other things changed in 1933 too, from the banking holiday to the "
            "end of the gold standard, but bank runs largely disappeared from America for the next seventy years."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.05),
                      run_time=2.5)
            for mk, r_ in zip("abcd", side):
                vo.wait_until(mk)
                self.play(FadeIn(r_))
        self.clear_scene()
