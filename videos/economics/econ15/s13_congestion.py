from __future__ import annotations

from videos.economics.econ15.common import *  # noqa: F403

TOLLC = "#7BD88F"


def clock(h: float) -> str:
    hh = int(h)
    mm = int(round((h - hh) * 60))
    if mm == 60:
        hh, mm = hh + 1, 0
    return f"{hh}:{mm:02d}"


class Congestion(VoiceoverScene):
    def construct(self):
        card(self, 11, r"Congestion: \ the bottleneck and the toll", r"Why does everyone queue at once, \ and what would "
             r"a toll do?", "Chapter eleven. Congestion: the bottleneck and the toll.",
             lit={1969: r"Vickrey's bottleneck", 1996: r"the Nobel", 2006: r"Stockholm's trial",
                  2011: r"Duranton and Turner"}, scale=("city",), horizon=("a day", "a year"))
        self.bottleneck()
        self.toll()
        self.stockholm()

    def bottleneck(self):
        b = load("bottleneck")
        t, q = np.array(b["t"]), np.array(b["wait_hours"]) * 60
        ax = plane([b["t0"] - 0.1, b["t1"] + 0.1], [0, 42], center=LEFT * 2.8 + DOWN * 0.3, x_length=6.4,
                   y_length=4.4, xticks=[b["t0"], b["t_star"], b["t1"]], yticks=[0, 10, 20, 30, 40],
                   xlabel=r"time of arrival at work", ylabel=r"minutes in the queue", font_size=16,
                   xfmt=clock, yfmt=lambda v: f"{v:.0f}")
        a = ax.ax
        c = path(ax, t, q, color=ROAD, width=3.5, smooth=False)
        fill = Polygon(*[a.c2p(x, y) for x, y in zip(t, q)], a.c2p(t[-1], 0), a.c2p(t[0], 0), stroke_width=0,
                       fill_color=ROAD, fill_opacity=0.2)
        star = seg(ax, b["t_star"], 0, b["t_star"], 42, color=GREY_B, width=1.5, dashed=True)
        sl = label(r"start of work", font_size=14, color=GREY_B).next_to(a.c2p(b["t_star"], 42), RIGHT, buff=0.08)
        side = VGroup(
            label(rf"{b['N']:,.0f} commuters, \ one causeway \\ that carries {b['s']:,.0f} an hour", font_size=20),
            label(r"each wants to arrive at 9:00; \\ early is costly, \ late costlier, \\ queueing costliest", font_size=20),
            label(rf"in equilibrium the queue grows \\ to {b['max_wait_min']:.0f} minutes for the 9:00 arrival", font_size=20,
                  color=ROAD),
            label(r"every commuter ends up equally badly off: \\ less queue means more time early or late",
                  font_size=20, color=GREY_A),
            label(r"each driver who joins slows everyone behind: \\ a spillover nobody pays for", font_size=20,
                  color=SOCIAL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.3)
        tag = published_tag(r"Vickrey, AER 59(2) (1969); \ Arnott, de Palma and Lindsey (1990); \ the curve: \ Agora",
                            corner=DR, font_size=12)
        with self.voiceover(
            "Traffic is a spillover everyone has met. In 1969 William Vickrey drew it as a bottleneck. "
            "<bookmark mark='a'/> Six thousand commuters must cross one causeway into town, and it carries four "
            "thousand cars an hour. <bookmark mark='b'/> Each wants to arrive at nine. Arriving early costs them "
            "time, arriving late costs more, and sitting in the queue costs most of all. "
            "<bookmark mark='c'/> In equilibrium the queue builds up toward nine, and whoever arrives exactly on "
            "time has queued thirty-six minutes. <bookmark mark='d'/> Every commuter ends up equally badly off: "
            "those who queue less pay for it by arriving early or late. If any time were better, people would move "
            "to it. <bookmark mark='e'/> And each driver who joins the queue slows everyone behind, without paying "
            "for it."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]), Create(star), FadeIn(sl))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(c), FadeIn(fill), FadeIn(side[2]), run_time=2.5)
            for mk, r in zip("de", side[3:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def toll(self):
        b = load("bottleneck")
        t, toll = np.array(b["t"]), np.array(b["toll"])
        ax = plane([b["t0"] - 0.1, b["t1"] + 0.1], [0, 13.5], center=LEFT * 2.8 + DOWN * 0.3, x_length=6.4,
                   y_length=4.4, xticks=[b["t0"], b["t_star"], b["t1"]], yticks=[0, 4, 8, 12],
                   xlabel=r"time of crossing", ylabel=r"the toll, \ shells", font_size=16, xfmt=clock,
                   yfmt=lambda v: f"{v:.0f}")
        c = path(ax, t, toll, color=TOLLC, width=3.5, smooth=False)
        side = VGroup(
            label(r"Vickrey's answer: \ a toll that rises \\ and falls with the queue it replaces", font_size=20,
                  color=TOLLC),
            label(r"the same people cross at the same times, \\ at the causeway's full capacity", font_size=20),
            label(r"but nobody queues: \ the time wasted \\ becomes money paid to the town", font_size=20,
                  color=TOLLC),
            label(rf"the cost of the rush hour to the island \\ is cut in half: \ {b['total_cost']:,.0f} shells' worth "
                  rf"\\ to {b['schedule_cost']:,.0f}", font_size=20, color=E.ACCENT),
            label(r"and the toll's revenue can be handed back", font_size=20, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.3)
        tag = published_tag(r"Vickrey (1969); \ Arnott, de Palma and Lindsey, J. Urban Econ. 27(1) (1990)",
                            corner=DR, font_size=12)
        with self.voiceover(
            "Vickrey's answer, pressed for the rest of a long career, was a toll. <bookmark mark='a'/> Charge a "
            "toll that rises and falls through the rush hour exactly as the queue would have. "
            "<bookmark mark='b'/> The same commuters cross, at the same times, at the causeway's full capacity. "
            "<bookmark mark='c'/> But nobody queues: the time that was wasted in the queue becomes money paid to "
            "the town. <bookmark mark='d'/> Half of the rush hour's cost was time in the queue, so the cost to the "
            "island is cut in half. <bookmark mark='e'/> And the revenue can be spent, or handed back to the "
            "commuters, who then come out ahead. Vickrey won a share of the Nobel prize in 1996, and died three days "
            "after it was announced."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(c), run_time=2)
            for mk, r in zip("bcde", side[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def stockholm(self):
        r = load("dial")["roads"]
        hc = history_card(2006, r"Stockholm, \ January to July", r"a congestion charge, \ tried for seven months, \ "
                          r"then put to a vote", color=ROAD, width=11.0, font_size=24).to_edge(UP, buff=0.45)
        rows = VGroup(
            label(r"traffic across the charging cordon fell by about a fifth", font_size=24, color=TOLLC),
            label(r"opinion, \ mostly against before the trial, \ turned slightly in favour during it", font_size=24),
            label(rf"September 2006: \ {100 * r['stockholm_yes_city']:.0f}\% of the city's voters said keep it; \ the "
                  r"county as a whole said no", font_size=23, color=GREY_A),
            label(rf"the charge became permanent in {r['stockholm_permanent']}, \ and support has grown since",
                  font_size=24, color=TOLLC),
            label(r"seeing the queues gone convinced people \ where arguments had not", font_size=24,
                  color=E.ACCENT),
        ).arrange(DOWN, buff=0.38).next_to(hc, DOWN, buff=0.5)
        tag = published_tag(r"Eliasson et al., Transportation Research A 43(3) (2009), \ as summarized", corner=DR,
                            font_size=13)
        with self.voiceover(
            "Tolls like Vickrey's are unpopular, until people try one. <bookmark mark='a'/> In 2006 Stockholm "
            "charged drivers to cross into the centre, for a seven-month trial. Traffic across the cordon fell by "
            "about a fifth, and the queues largely went. <bookmark mark='b'/> Most people had opposed the charge "
            "before the trial; during it, opinion turned slightly in favour. <bookmark mark='c'/> In a vote that "
            "September, fifty-three percent of the city's voters chose to keep it, though the county as a whole said "
            "no. <bookmark mark='d'/> The charge became permanent in 2007, and support has grown since. "
            "<bookmark mark='e'/> Seeing the queues gone convinced people where the arguments had not."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.2), FadeIn(tag))
            for mk, r_ in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()
