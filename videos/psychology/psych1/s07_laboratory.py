from __future__ import annotations

import numpy as np

from videos.psychology.psych1.common import *  # noqa: F403


def dial(radius=1.0) -> VGroup:
    """A chronoscope's face: a ring of ticks and a hand (``.hand``, rotating about ``.centre``)."""
    ring = Circle(radius=radius, stroke_color=GREY_A, stroke_width=3, fill_color="#10151F", fill_opacity=1)
    ticks = VGroup()
    for k in range(100):
        a = TAU * k / 100
        r0 = radius * (0.84 if k % 10 == 0 else 0.92)
        ticks.add(Line([r0 * np.sin(a), r0 * np.cos(a), 0], [radius * 0.98 * np.sin(a), radius * 0.98 * np.cos(a), 0],
                       color=GREY_B, stroke_width=2 if k % 10 == 0 else 1))
    hand = Line(ORIGIN, UP * radius * 0.8, color=P.ACCENT, stroke_width=4)
    hub = Dot(radius=0.06, color=P.ACCENT)
    g = VGroup(ring, ticks, hand, hub)
    g.hand, g.ring = hand, ring
    return g


class Laboratory(VoiceoverScene):
    def construct(self):
        self.card()
        self.wundt()
        self.ebbinghaus()
        self.stall()

    def card(self):
        card = chapter_card(6, r"The first laboratories", r"What did an experiment on the mind look like, and where "
                            r"did it get stuck?", lit=(1879, 1885, 1890), part=PART, scale=("mind", "person"),
                            marr=("what",))
        with self.voiceover(
            "Chapter six. The first laboratories."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    # ------------------------------------------------------------------
    def wundt(self):
        hc = history_card(1879, r"Wilhelm Wundt, Leipzig", r"the first laboratory of experimental psychology",
                          color=P.ARCHIVE, width=7.2, font_size=30).to_edge(UP, buff=0.45)
        clock = dial(1.25)
        c_cap = VGroup(label(r"reaction times", font_size=34, color=P.ACCENT),
                       label(r"a chronoscope, reading to $\tfrac{1}{1000}$ s", font_size=26, color=GREY_A))
        c_cap.arrange(DOWN, buff=0.12)
        left = VGroup(clock, c_cap).arrange(DOWN, buff=0.35).move_to([-3.6, -1.0, 0])
        person = little_person(1.5, color=GREY_A)
        cloud = VGroup(*[Circle(radius=r, stroke_width=0, fill_color=KANT, fill_opacity=0.8).move_to([x, y, 0])
                         for x, y, r in ((-0.45, 0, 0.36), (-0.05, 0.2, 0.46), (0.4, 0.05, 0.4), (0.05, -0.15, 0.4))])
        cloud.next_to(person, UR, buff=0.05)
        obs = VGroup(person, cloud)
        o_cap = VGroup(label(r"trained introspection", font_size=34, color=KANT),
                       label(r"report exactly what you experience", font_size=26, color=GREY_A))
        o_cap.arrange(DOWN, buff=0.12)
        right = VGroup(obs, o_cap).arrange(DOWN, buff=0.35).move_to([3.6, -1.0, 0])
        right.align_to(left, DOWN)
        line = wrapped_label(r"Wundt: \ sensations and reactions can be studied by experiment; \ memory and thinking "
                             r"cannot.", 11.5, 28, WHITE).to_edge(DOWN, buff=0.45)
        students = VGroup(*[little_person(0.8, color=c) for c in (GREY_A, GREY_B) * 5]).arrange(RIGHT, buff=0.3)
        students.move_to([0, -1.2, 0])
        from_ = label(r"students from across Europe and America", font_size=28, color=GREY_A)
        from_.next_to(students, DOWN, buff=0.3)
        with self.voiceover(
            "By 1879 there were enough of these methods to fill a few rooms. In Leipzig, Wilhelm Wundt opened the "
            "first laboratory of experimental psychology, and students came from across Europe and America to be "
            "trained in it. <bookmark mark='a'/> It had two tools. One was Donders': the reaction time, measured "
            "with a chronoscope, a clock that reads to a thousandth of a second. <bookmark mark='b'/> The other "
            "was trained introspection: an observer who has practised describing exactly what he experiences, "
            "under controlled conditions. <bookmark mark='c'/> And Wundt himself drew a line. Sensations and "
            "reactions could be studied this way. Memory and thinking, he believed, were out of reach of "
            "experiment."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.2))
            self.play(LaggedStart(*[FadeIn(p_, shift=UP * 0.2) for p_ in students], lag_ratio=0.25), FadeIn(from_),
                      run_time=4.0)
            vo.wait_until("a")
            self.play(FadeOut(students), FadeOut(from_))
            self.play(FadeIn(left, shift=UP * 0.2))
            self.play(Rotate(clock.hand, angle=-TAU * 0.62, about_point=clock.ring.get_center()), run_time=2.0,
                      rate_func=linear)
            vo.wait_until("b")
            self.play(FadeIn(right, shift=UP * 0.2))
            vo.wait_until("c")
            self.play(VGroup(left, right).animate.shift(UP * 0.35), FadeIn(line, shift=UP * 0.15))
        self.clear_scene()

    def ebbinghaus(self):
        d = load("ebbinghaus")
        mins, save, pe = (np.asarray(d[k]) for k in ("minutes", "saving", "pe"))
        hc = history_card(1885, r"Hermann Ebbinghaus", r"\emph{On Memory}: \ one subject, himself", color=P.ARCHIVE,
                          width=5.4, font_size=26).to_corner(UL, buff=0.4)
        syl = VGroup(*[label(rf"\textsc{{{s}}}", font_size=36, color=WHITE) for s in
                       ("zat", "bok", "lif", "dup", "meg", "ruk", "waj", "nif")]).arrange_in_grid(2, 4, buff=(0.35, 0.22))
        syl_note = label(rf"about {fmt_int(d['syllables'])} syllables that mean nothing", font_size=26, color=GREY_A)
        ill = note(r"(these eight are illustrative)", font_size=20)
        sy = VGroup(syl, syl_note, ill).arrange(DOWN, buff=0.16).next_to(hc, DOWN, buff=0.45).align_to(hc, LEFT)
        saving = MathTex(r"\text{saving}", r"=", r"\frac{\text{first learning} - \text{relearning}}"
                         r"{\text{first learning}}", font_size=30)
        saving[0].set_color(P.ACCENT)
        saving.next_to(sy, DOWN, buff=0.5).align_to(hc, LEFT)
        if saving.width > 5.4:
            saving.width = 5.4
        lo, hi = np.log10(10), np.log10(60_000)
        A = axes([lo, hi], [0, 70], x_length=6.9, y_length=4.4, ylabel=r"time saved in relearning (\%)",
                 yticks=[0, 20, 40, 60], center=[3.1, -0.35, 0])
        ax = A.ax
        names = (r"20 min", r"1 h", r"9 h", r"1 d", r"2 d", r"6 d", r"31 d")
        xt = VGroup()
        for m, nm in zip(mins, names):
            p = ax.c2p(np.log10(m), 0)
            xt.add(Line(p, p + DOWN * 0.08, color=GREY_C, stroke_width=1.5))
            xt.add(label(nm, font_size=18, color=GREY_B).next_to(p, DOWN, buff=0.14))
        xl = label(r"time since learning (logarithmic)", font_size=22, color=GREY_A).next_to(ax, DOWN, buff=0.6)
        dots, bars = VGroup(), VGroup()
        for m, s_, e in zip(mins, save, pe):
            x = np.log10(m)
            bars.add(Line(ax.c2p(x, s_ - e), ax.c2p(x, s_ + e), color=P.HUMAN, stroke_width=2))
            dots.add(Dot(ax.c2p(x, s_), radius=0.085, color=P.HUMAN))
        fit = curve(ax, np.log10(np.asarray(d["grid"])), d["curve"], P.ARCHIVE, 3)
        vals = VGroup(*[MathTex(rf"{s_:.0f}", font_size=24, color=P.HUMAN).next_to(dt, UR, buff=0.05)
                        for s_, dt in zip(save, dots)])
        formula = MathTex(rf"b = \frac{{100\,k}}{{(\log t)^c + k}},\quad k = {d['k']},\ c = {d['c']}", font_size=28,
                          color=P.ARCHIVE).move_to(ax.c2p(3.3, 63))
        src = historical_tag(archive.EBBINGHAUS_1885.cite)
        with self.voiceover(
            "The boldest experiment of the era was done outside any laboratory, by a man working alone. Hermann "
            "Ebbinghaus set out to measure memory, the very thing Wundt had ruled out, and he did it on himself. "
            f"<bookmark mark='a'/> He made up about {d['syllables']:,} meaningless syllables, so that nothing he "
            "already knew could help him. He learned a list of them until he could recite it without a mistake, "
            "and timed how long that took. <bookmark mark='b'/> Then he waited. Twenty minutes, an hour, a day, a "
            "month. And he learned the same list again. The second time was quicker, and the time he saved was "
            "his measure of what memory had kept. <bookmark mark='c'/> These are his numbers, from 1885. After "
            f"twenty minutes, {save[0]:.0f} per cent saved. After an hour, {save[1]:.0f}. After a day, "
            f"{save[3]:.0f}. After a month, still {save[6]:.0f}. <bookmark mark='d'/> He fitted a curve to them, "
            "with the logarithm of time in it, and it misses none of his seven points by more than "
            f"{d['max_miss']:.1f} points. This is the first quantitative law of memory, and one man's patience "
            "produced it. Parts 20 and 21 take it apart."
        ) as vo:
            self.play(FadeIn(hc, shift=RIGHT * 0.2), FadeIn(src), FadeIn(A), FadeIn(xt), FadeIn(xl))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(s) for s in syl], lag_ratio=0.15), FadeIn(syl_note), FadeIn(ill))
            vo.wait_until("b")
            self.play(Write(saving))
            vo.wait_until("c")
            for i in (0, 1, 2, 3, 4, 5, 6):
                self.play(GrowFromCenter(dots[i]), FadeIn(bars[i]), FadeIn(vals[i]), run_time=0.7 if i in (0, 1, 3, 6)
                          else 0.35)
            vo.wait_until("d")
            self.play(Create(fit), FadeIn(formula), run_time=2.0)
        self.clear_scene()

    def stall(self):
        james = history_card(1890, r"William James", r"\emph{The Principles of Psychology}: \ the new science, in "
                             r"almost fourteen hundred pages", color=P.ARCHIVE, width=8.0, font_size=28)
        james.to_edge(UP, buff=0.45)

        def lab(name, where, says, x, color):
            people = VGroup(*[little_person(0.9, color=color) for _ in range(3)]).arrange(RIGHT, buff=0.2)
            nm = VGroup(label(name, font_size=30, color=color), label(where, font_size=22, color=GREY_A))
            nm.arrange(DOWN, buff=0.08)
            txt = label(says, font_size=28, color=WHITE)
            bubble = RoundedRectangle(width=txt.width + 0.5, height=txt.height + 0.4, corner_radius=0.18,
                                      stroke_color=color, stroke_width=2, fill_color=CARD_FILL, fill_opacity=1)
            txt.move_to(bubble)
            b = VGroup(bubble, txt)
            g = VGroup(b, people, nm).arrange(DOWN, buff=0.25).scale(1.2).move_to([x, -0.75, 0])
            g.bubble = b
            return g

        w = lab(r"W\"urzburg", r"K\"ulpe's observers", r"``a thought, with no image in it''", -4.2, "#7EC8F5")
        c = lab(r"Cornell", r"Titchener's observers", r"``there is always an image''", 4.2, "#F28FB8")
        mid = VGroup(MathTex(r"?", font_size=90, color=KANT),
                     label(r"no instrument but the observer", font_size=24, color=KANT)).arrange(DOWN, buff=0.15)
        mid.move_to([0, -0.75, 0])
        if mid.width > 2.6:
            mid.width = 2.6
        third = VGroup(label(r"3", font_size=40, color=KANT),
                       label(r"The observer disturbs: \ still unanswered", font_size=32, color=WHITE))
        third.arrange(RIGHT, buff=0.3).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "In 1890 William James pulled the new science together in almost fourteen hundred pages, The "
            "Principles of Psychology, which is still worth reading. <bookmark mark='a'/> But one of the field's "
            "two tools was failing. Introspection could not settle its own disputes. In Würzburg, trained "
            "observers reported thoughts with no images in them at all. <bookmark mark='b'/> At Cornell, trained "
            "observers reported that there is always an image, if you look carefully enough. "
            "<bookmark mark='c'/> Each side said the other's observers were badly trained. And no experiment "
            "could decide between them, because the only instrument was the observer. <bookmark mark='d'/> That "
            "is Kant's third objection, arriving on schedule."
        ) as vo:
            self.play(FadeIn(james, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(w, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(c, shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(mid, scale=1.2))
            self.play(Wiggle(w.bubble, scale_value=1.05), Wiggle(c.bubble, scale_value=1.05))
            vo.wait_until("d")
            self.play(FadeIn(third, shift=UP * 0.15))
        self.clear_scene()
