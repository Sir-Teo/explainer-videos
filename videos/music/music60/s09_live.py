from __future__ import annotations

import numpy as np

from videos.music.music60.common import *  # noqa: F403


class Live(SoundScene):
    def construct(self):
        chapter(self, 8, r"Live music: \ the cost disease and tickets", r"Why do concert tickets keep getting dearer?")
        self.quartet()
        self.disease()
        self.tickets()
        self.market()

    # ------------------------------------------------------------------
    def quartet(self):
        c = clip("live.quartet")
        players = VGroup(*[VGroup(Circle(radius=0.38, stroke_color=col, stroke_width=3), label(n, font_size=16, color=col)).arrange(DOWN, buff=0.15)
                           for n, col in ((r"violin", TUNE), (r"violin", TUNE), (r"viola", BLUE), (r"cello", BLUE))]).arrange(RIGHT, buff=0.9).move_to(UP * 0.5)
        note = label(r"four players, \ the same notes, \ the same time: \ in 1790 and in 2026", font_size=20, color=GREY_A).next_to(players, DOWN, buff=0.7)
        head = label(r"a string quartet", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("Hear a string quartet play the Tune. It took four players and the same half minute when Mozart was alive, and it still does."):
            self.play(FadeIn(head), FadeIn(players), FadeIn(note))
        with self.listen(c) as snd:
            window(snd, r"a quartet", kind="physical model", detail=r"Part 9's bowed strings", corner=DL, tag_corner=DR)
            pulse(snd, players, 0.0, c.duration, rate=5.0, color=GREY_B, buff=0.1)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def disease(self):
        d = load("live")
        ys = np.array(d["years"])
        rel = np.log10(np.array(d["relative"]))
        ax = frame_axes(width=8.6, height=3.2, xlo=1790, xhi=2026, ylo=0, yhi=2.2, center=DOWN * 0.4 + LEFT * 0.6)
        cv = curve(ys, rel, ax.to, color=TUNE, width=3.5)
        xt = VGroup(*[label(str(v), font_size=14, color=GREY_A).next_to(ax.to(v, 0), DOWN, buff=0.1) for v in (1800, 1850, 1900, 1950, 2000)])
        yt = VGroup(*[label(rf"$\times${v:g}", font_size=14, color=GREY_A).next_to(ax.to(1790, np.log10(v)), LEFT, buff=0.1) for v in (1, 10, 100)])
        eq = MathTex(r"\frac{\text{price of a performance}}{\text{price of goods}} \propto e^{g\,(t - t_0)}, \quad g \approx 2\%\ \text{a year}", font_size=30, color=WHITE).to_edge(UP, buff=1.0)
        note = label(rf"at 2\% a year: \ $\times${d['rise_1966']:.1f} since Baumol and Bowen wrote in 1966; \ $\times${d['rise_1790']:.0f} since 1790", font_size=17, color=GREY_A).to_edge(DOWN, buff=0.35)
        head = label(r"Baumol's cost disease", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "That is the cost disease, named by William Baumol and William Bowen in 1966. <bookmark mark='a'/> Elsewhere, our illustrative model assumes two-percent annual productivity growth elsewhere, and wages grow with it, musicians' included, or they would leave for other work. But a quartet's output per hour does not grow at all. <bookmark mark='b'/> So the price of a performance, relative to manufactured goods, rises exponentially: these multiples follow the assumed two-percent path; they are not measured historical ticket-price increases. <bookmark mark='c'/> Recording was the cure for listening: one performance, sold millions of times. But a concert cannot be copied, which creates cost pressure under these assumptions; subsidies, wages, capacity and technology also affect actual prices."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(xt), FadeIn(yt))
            vo.wait_until("a")
            self.play(FadeIn(eq))
            vo.wait_until("b")
            self.play(Create(cv), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(note))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def tickets(self):
        d = load("live")["tickets"]
        rows_ = [("face_value", rf"face value, \ \${d['face']:.0f}", WHITE), ("clearing_price", rf"one market price, \ \${d['clearing']:.0f}", BLUE),
                 ("dynamic", r"each seat at what its buyer would pay", EAR)]
        g = VGroup()
        for k, n, col in rows_:
            v = d[k]
            g.add(VGroup(label(n, font_size=18, color=col), label(rf"\${v['artist'] / 1e6:.1f}M", font_size=18, color=WHITE),
                         label(rf"\${v['resellers'] / 1e6:.1f}M", font_size=18, color=WHITE), label(rf"\${v['fans'] / 1e6:.1f}M", font_size=18, color=WHITE)))
        g.arrange(DOWN, buff=0.45)
        for r in g:
            r[0].set_x(-3.6)
            r[1].set_x(0.9)
            r[2].set_x(3.1)
            r[3].set_x(5.3)
        top = VGroup(*[label(t, font_size=15, color=GREY_A).move_to([x, g.get_top()[1] + 0.5, 0]) for t, x in
                       ((r"to the artist's side", 0.9), (r"to resellers", 3.1), (r"left with fans", 5.3))])
        note = label(rf"{d['seats']:,} seats, \ 60,000 fans; \ resellers buy a quarter of the face-value seats and sell at about \${d['resale_price']:.0f}",
                     font_size=16, color=GREY_A).to_edge(DOWN, buff=0.4)
        head = label(r"selling one night's tickets, \ three ways \ (a model)", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "And a tour date has more fans than seats. Monochord models one: twenty thousand seats, sixty thousand fans, each "
            "willing to pay a different amount. <bookmark mark='a'/> Sold at a face value well under the market, the artist's "
            "side takes 1.8 million dollars; resellers who buy a quarter of the seats take another 0.8, and the seats go to "
            "whoever was lucky, not to whoever wanted them most. <bookmark mark='b'/> At one price that just fills the house, the artist takes "
            "about twice as much and resellers nothing. <bookmark mark='c'/> And selling each seat at the most its buyer would "
            "pay, perfect first-degree price discrimination, which is stronger than ordinary dynamic pricing, takes everything fans would have kept."
        ) as vo:
            self.play(FadeIn(head), FadeIn(top), FadeIn(note))
            for mark, r in zip("abc", g):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def market(self):
        items = [
            (r"artists often price under the market on purpose: \ fairness, \ loyalty, \ and full rooms \ (Krueger, \ Rockonomics, \ 2019)", WHITE),
            (r"the gap is the resale market; \ bots buy seats in seconds, \ and laws against them are hard to enforce", WHITE),
            (r"2010: \ Ticketmaster and Live Nation merge; \ 2024: \ the US Department of Justice sues to break them up", WHITE),
            (r"2022 and 2024: \ crashed presales and surging dynamic prices for the largest tours provoke public anger", WHITE),
            (r"for most working bands, \ the problem is the opposite: \ costs rise, \ rooms are small, \ and fees take a share", TUNE),
        ]
        rows_scene(self, r"the ticket market \ (dated)", items,
                   "So pricing a ticket is a choice about who keeps what. <bookmark mark='b'/> Artists often price under the market "
                   "on purpose, for fairness, loyalty and full rooms, as the economist Alan Krueger documented in Rockonomics. "
                   "<bookmark mark='c'/> The gap becomes the resale market: bots buy seats in seconds, and laws against them are "
                   "hard to enforce. <bookmark mark='d'/> In 2010 Ticketmaster and Live Nation merged; in 2024 the Department of "
                   "Justice sued to break them up. <bookmark mark='e'/> Crashed presales in 2022 and surging dynamic prices in 2024 "
                   "made the largest tours national arguments. <bookmark mark='f'/> For most working bands the problem is the "
                   "opposite: costs rise, rooms are small, and fees take a share.", marks="bcdef")
