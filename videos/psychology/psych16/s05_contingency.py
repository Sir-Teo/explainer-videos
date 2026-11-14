from __future__ import annotations

import numpy as np

from videos.psychology.psych16.common import *  # noqa: F403


def plant(given: bool, bloom: bool, scale=1.0):
    """One trial of the game: a pot, a stem, a flower if it bloomed, and a bag of fertilizer if it was given."""
    pot = Polygon([-0.3, -0.5, 0], [0.3, -0.5, 0], [0.38, -0.1, 0], [-0.38, -0.1, 0], stroke_color=GREY_B,
                  stroke_width=2, fill_color="#3A2A20", fill_opacity=1)
    stem = Line([0, -0.1, 0], [0, 0.45, 0], color=CR, stroke_width=4)
    g = VGroup(pot, stem)
    if bloom:
        petals = VGroup(*[Circle(radius=0.13, stroke_width=0, fill_color=US, fill_opacity=1).move_to(
            [0.16 * np.cos(a), 0.55 + 0.16 * np.sin(a), 0]) for a in np.linspace(0, TAU, 6)[:-1]])
        g.add(petals, Circle(radius=0.08, stroke_width=0, fill_color=YOU, fill_opacity=1).move_to([0, 0.55, 0]))
    else:
        g.add(Line([0, 0.45, 0], [0.18, 0.35, 0], color=GREY_C, stroke_width=4))
    if given:
        bag = VGroup(RoundedRectangle(width=0.32, height=0.4, corner_radius=0.05, stroke_width=0, fill_color=CS,
                                      fill_opacity=1), label(r"F", font_size=16, color=BLACK)).move_to([-0.55, -0.25, 0])
        bag[1].move_to(bag[0])
        g.add(bag)
    return g.scale(scale)


class Contingency(VoiceoverScene):
    def construct(self):
        self.card()
        self.game()
        self.table()
        self.rescorla()

    def card(self):
        card = chapter_card(4, r"Contingency, \ not pairing", r"Does a cue have to predict, \ or just to appear?",
                            lit={1968: r"Rescorla"}, part=PART, scale=("mind",), marr=("what",))
        with self.voiceover("Chapter four. Contingency, not pairing."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def game(self):
        d = load("contingency")
        stage = demo_stage(12.6, 5.6, center=[0, -0.15, 0])
        title = label(r"Does the fertilizer make the plants bloom?", font_size=30, color=YOU)
        title.next_to(stage.box.get_top(), DOWN, buff=0.35)
        grid = VGroup(*[plant(bool(g), bool(b), 0.62) for g, b in zip(d["given"], d["bloom"])])
        grid.arrange_in_grid(rows=3, cols=8, buff=(0.55, 0.35)).move_to(stage.box.get_center() + DOWN * 0.25)
        key = label(r"F: \ fertilizer given", font_size=20, color=CS).next_to(stage.box.get_corner(UR), DL, buff=0.3)
        scale = VGroup(*[label(t, font_size=24, color=c) for t, c in
                         ((r"$-100$: \ prevents blooming", INHIB), (r"0: \ no effect", WHITE),
                          (r"$+100$: \ makes them bloom", CR))]).arrange(RIGHT, buff=0.9)
        scale.next_to(stage.box.get_bottom(), UP, buff=0.3)
        with self.voiceover(
            "Before the history, a game. <bookmark mark='a'/> You're a gardener testing a fertilizer. Twenty-four "
            "plants: some get the fertilizer, marked with a blue bag, and some don't, and each one either blooms or "
            "doesn't. Watch them go by. <bookmark mark='b'/> Don't count. Just form an impression."
        ) as vo:
            self.play(FadeIn(stage), FadeIn(title), FadeIn(key))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p, shift=UP * 0.1) for p in grid], lag_ratio=0.5), run_time=10.0)
            vo.wait_until("b")
        with self.voiceover(
            "Now rate it. How strongly does the fertilizer make the plants bloom, from minus a hundred, it prevents "
            "blooming, through zero, no effect, to plus a hundred? Pause and pick a number."
        ):
            self.play(grid.animate.shift(UP * 0.25), FadeIn(scale))
        self.wait(3.0)
        self.clear_scene()

    def table(self):
        d = load("contingency")
        c = d["cells"]
        head = heading(r"Count them: \ the contingency")
        cells = VGroup()
        txt = [[rf"{c[0, 0]}", rf"{c[0, 1]}"], [rf"{c[1, 0]}", rf"{c[1, 1]}"]]
        for i in range(2):
            for j in range(2):
                sq = Square(1.3, stroke_color=GREY_B, stroke_width=2).move_to([-3.6 + 1.3 * j, 0.9 - 1.3 * i, 0])
                cells.add(VGroup(sq, label(txt[i][j], font_size=40, color=CR if j == 0 else GREY_A).move_to(sq)))
        top = VGroup(label(r"bloomed", font_size=24, color=CR).next_to(cells[0], UP, buff=0.15),
                     label(r"did not", font_size=24, color=GREY_A).next_to(cells[1], UP, buff=0.15))
        side = VGroup(label(r"fertilizer", font_size=24, color=CS).next_to(cells[0], LEFT, buff=0.2),
                      label(r"none", font_size=24, color=GREY_A).next_to(cells[2], LEFT, buff=0.2))
        eq = VGroup(
            MathTex(r"\Delta P = P(\text{bloom}\mid\text{fertilizer}) - P(\text{bloom}\mid\text{none})", font_size=34),
            MathTex(rf"= \tfrac{{{c[0, 0]}}}{{{c[0].sum()}}} - \tfrac{{{c[1, 0]}}}{{{c[1].sum()}}} = 0", font_size=40,
                    color=YOU),
        ).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to([3.0, 0.9, 0])
        keep_in_frame(eq)
        rows = rows_of([
            (r"most of the fertilized plants bloomed: \ the pairings are vivid", CS),
            (r"but the unfertilized ones bloomed just as often: \ the fertilizer does nothing", WHITE),
            (r"when the outcome is common, \ people often rate a useless cause as working: \ the outcome-density "
             r"effect", INHIB),
            (r"over many conditions, \ people's ratings follow $\Delta P$ closely", CR),
        ], 12.4, 26, 0.24).to_edge(DOWN, buff=0.65)
        tag = published_tag(archive.WASSERMAN_1993.cite)
        with self.voiceover(
            "Here are the counts. <bookmark mark='a'/> Of the twelve fertilized plants, nine bloomed. That's what you "
            "notice: fertilizer, then flowers, again and again. <bookmark mark='b'/> But of the twelve plants with no "
            "fertilizer, nine bloomed too. The chance of blooming is three in four either way. The right measure is "
            "the contingency, delta P: the probability of the outcome with the cause, minus the probability without "
            "it. Here it's exactly zero. The fertilizer does nothing. <bookmark mark='c'/> If you gave it a positive "
            "number, you're in good company. When an outcome is common, people often judge a useless cause to be "
            "working, the outcome-density effect, and it's the engine of many folk remedies: most colds get better "
            "whatever you take. <bookmark mark='d'/> Even so, when Edward Wasserman and colleagues had people rate "
            "many such contingencies in 1993, the ratings followed delta P closely. People, like rats, are mostly "
            "tracking contingency, not pairing."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cells), FadeIn(top), FadeIn(side), FadeIn(tag))
            vo.wait_until("a")
            self.play(Indicate(cells[0], color=CS), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Indicate(cells[2], color=CS), FadeIn(eq[0]), FadeIn(rows[1]))
            self.play(FadeIn(eq[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def rescorla(self):
        p = archive.RESCORLA_1968.data
        head = heading(r"Rescorla's rats, \ 1968")
        rows = rows_of([
            (rf"{p['exp2_rats']} rats; \ a two-minute tone, \ {p['tones_per_session']} times a session, \ for "
             rf"{p['sessions']} sessions", WHITE),
            (r"in every two minutes, \ a set chance of a brief shock while the tone is on, \ and another while it is "
             r"off", US),
            (r"fear measured later, \ as how much the tone suppresses lever-pressing for food", CS),
        ], 12.4, 26, 0.26).move_to([0, 2.0, 0])
        grid = VGroup()
        ps = [0.4, 0.2, 0.1, 0.0]
        for i, p_cs in enumerate(ps[:3]):
            for j, p_no in enumerate(ps):
                if p_no > p_cs:
                    continue
                eq_ = p_no == p_cs
                sq = Square(0.8, stroke_color=GREY_B, stroke_width=2, fill_color=INHIB if eq_ else "#05070B",
                            fill_opacity=0.25 if eq_ else 1).move_to([-1.6 + 0.88 * j, 0.25 - 0.88 * i, 0])
                grid.add(VGroup(sq, label(rf"{p_cs:g}, \ {p_no:g}", font_size=18).move_to(sq)))
        zero = Square(0.8, stroke_color=GREY_B, stroke_width=2, fill_color=INHIB, fill_opacity=0.25).move_to(
            [-1.6 + 0.88 * 3, 0.25 - 0.88 * 3, 0])
        grid.add(VGroup(zero, label(r"0, \ 0", font_size=18).move_to(zero)))
        cap_r = label(r"chance of shock: \ tone on, \ tone off", font_size=22, color=GREY_A).next_to(grid, LEFT, buff=0.4)
        cap_r.shift(UP * 1.2)
        keep_in_frame(cap_r)
        res = rows_of([
            (r"equal chances, \ shaded: \ little or no fear of the tone, \ however many pairings", INHIB),
            (r"the same chance with the tone, \ more shocks without it: \ less fear", US),
            (r"fear grows with the difference between the two: \ the contingency", CR),
        ], 4.6, 24, 0.34).move_to([4.7, -0.9, 0])
        keep_in_frame(res)
        tag = historical_tag(archive.RESCORLA_1968.cite)
        with self.voiceover(
            "In 1968 Robert Rescorla ran the animal version, with exactly the puzzle from the start of this part. "
            "<bookmark mark='a'/> Eighty rats heard a two-minute tone, twelve times a session, for five sessions. "
            "<bookmark mark='b'/> In every two-minute stretch there was some chance of a brief shock while the tone "
            "was on, and some other chance while it was off. Ten groups had ten different pairs of chances. "
            "<bookmark mark='c'/> Fear of the tone was measured afterwards, by how much it made the rats stop pressing "
            "a lever for food. <bookmark mark='d'/> The result was clean. Whenever the two chances were equal, the "
            "shaded squares, the rats learned little or no fear of the tone, even in the group that heard it paired "
            "with shock again and again. With the chance during the tone held fixed, adding shocks when the tone was "
            "off reduced the fear. Fear followed the difference between the two chances, the contingency, not the "
            "number of pairings. <bookmark mark='e'/> The obvious next question is what kind of learning machine "
            "computes a contingency. The answer came four years later, after one more experiment."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(grid), FadeIn(cap_r))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(r) for r in res], lag_ratio=0.8), run_time=5.0)
            vo.wait_until("e")
        self.clear_scene()
