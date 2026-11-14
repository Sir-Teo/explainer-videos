from __future__ import annotations

import numpy as np

from videos.psychology.psych6.common import *  # noqa: F403


def field(center, r_in=0.3, r_out=0.8):
    """A centre-surround receptive field: an excitatory disc inside an inhibitory ring."""
    ring = Annulus(inner_radius=r_in, outer_radius=r_out, color=INH, fill_opacity=0.45, stroke_width=2).move_to(center)
    disc = Circle(radius=r_in, color=EXC, stroke_width=2, fill_color=EXC, fill_opacity=0.6).move_to(center)
    return VGroup(ring, disc, label(r"$+$", font_size=26, color=WHITE).move_to(center),
                  label(r"$-$", font_size=26, color=WHITE).move_to(np.asarray(center) + UP * (r_in + r_out) / 2))


class Grid(VoiceoverScene):
    def construct(self):
        self.card()
        self.look()
        self.account()
        self.test()

    def card(self):
        card = chapter_card(7, r"On you: \ a grid of grey spots", r"Does lateral inhibition explain what you see?",
                            lit=(), part=PART, scale=("circuit", "mind"), marr=("what", "how"))
        with self.voiceover(
            "Chapter seven. On you: a grid of grey spots."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def look(self):
        h = load("hermann")
        stage = demo_stage(13.2, 6.6, tag=r"On you: \ the Hermann grid (1870)", center=[0, -0.25, 0])
        c = stage.box.get_center()
        img = picture(h["image"], height=5.4).move_to(c + LEFT * 3.1)
        ring = countdown_ring(0.5).move_to(c + np.array([3.4, -2.0, 0]))
        steps = VGroup(
            wrapped_label(r"1. \ Look at the whole grid. \ Notice the crossings of the white streets.", 5.2, 28,
                          WHITE),
            wrapped_label(r"2. \ Faint grey spots sit on the crossings, \ in the corner of your eye.", 5.2, 28,
                          WHITE),
            wrapped_label(r"3. \ Look straight at one of them. \ It is gone.", 5.2, 28, P.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to(c + np.array([3.4, 0.6, 0]))
        with self.voiceover(
            "Now an experiment on you, with the same circuit in two dimensions. In 1870 the physiologist "
            "Ludimar Hermann noticed something while reading a book with a grid of figures in it. "
            "<bookmark mark='a'/> Black squares, white streets. Look at the whole thing for a few seconds, and "
            "attend to the places where the streets cross. <bookmark mark='b'/> Most people see faint grey "
            "smudges sitting on the crossings. They flicker in and out, and they're always somewhere you're "
            "not quite looking. <bookmark mark='c'/> Now pick one crossing and look straight at it. The spot "
            "on that one is gone, and the others carry on. There is no grey anywhere on this screen. The "
            "streets are the same white all the way along."
        ) as vo:
            self.play(FadeIn(stage))
            vo.wait_until("a")
            self.play(FadeIn(img), FadeIn(steps[0]), FadeIn(ring))
            self.play(ring.t.animate.set_value(0.0), run_time=7.0, rate_func=linear)
            vo.wait_until("b")
            self.play(FadeIn(steps[1]), FadeOut(ring))
            vo.wait_until("c")
            self.play(FadeIn(steps[2]))
        self.wait(2.0)
        self.clear_scene()

    def account(self):
        h = load("hermann")
        head = heading(r"The textbook account: \ count the light on the surround")
        # a piece of the grid, large: four squares and the streets between them
        u, sw = 1.55, 0.62  # square size, street width
        c0 = np.array([-4.1, -0.3, 0])
        bg = Rectangle(width=2 * u + 3 * sw, height=2 * u + 3 * sw, stroke_width=0, fill_color=WHITE, fill_opacity=1)
        bg.move_to(c0)
        sq = VGroup(*[Square(side_length=u, stroke_width=0, fill_color=BLACK, fill_opacity=1).move_to(
            c0 + np.array([sx * (u + sw) / 2, sy * (u + sw) / 2, 0])) for sx in (-1, 1) for sy in (-1, 1)])
        cross, street = c0, c0 + np.array([(u + sw) / 2, 0, 0])
        f1, f2 = field(street, 0.26, 0.74), field(cross, 0.26, 0.74)
        A = axes([0, 3], [0, 0.45], x_length=3.4, y_length=3.0, xticks=[], yticks=[0, 0.2, 0.4],
                 yfmt=lambda v: f"{v:.1f}", ylabel=r"the model cell's response", center=[1.2, -0.75, 0])
        ax = A.ax
        bars = VGroup()
        for i, (name, v, col) in enumerate(((r"street", h["street"], VOLT), (r"crossing", h["crossing"], THRESH))):
            b = Rectangle(width=0.8, height=np.linalg.norm(ax.c2p(0, v) - ax.c2p(0, 0)), stroke_width=0,
                          fill_color=col, fill_opacity=0.9)
            b.move_to(ax.c2p(0.8 + 1.3 * i, v / 2))
            bars.add(VGroup(b, label(name, font_size=24, color=col).next_to(ax.c2p(0.8 + 1.3 * i, 0), DOWN, buff=0.12),
                            label(rf"{v:.2f}", font_size=26, color=col).next_to(b, UP, buff=0.08)))
        side = VGroup(
            wrapped_label(r"on a street: \ the surround catches light from two directions", 3.9, 26, VOLT),
            wrapped_label(r"on a crossing: \ from four. \ More inhibition, a weaker response, a dimmer spot", 3.9,
                          26, THRESH),
            wrapped_label(r"where you look, \ the fields are smaller than the street: \ no spot", 3.9, 26, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([5.0, -0.2, 0])
        keep_in_frame(side)
        src = published_tag(archive.GEIER_2008.cite + r", on Baumgartner's account of 1960")
        tag = psyche_tag()
        with self.voiceover(
            "For most of the last sixty years, every textbook gave the same explanation, and it's a lovely "
            "one. It's due to Günter Baumgartner, in 1960. <bookmark mark='a'/> A cell early in your visual "
            "system looks at a small patch of the image, and it's wired like the crab's eye. Light on the "
            "centre of its patch excites it. Light on the surrounding ring inhibits it. "
            "<bookmark mark='b'/> Put such a cell on a street, half way between two crossings. Its centre is "
            "on white. Its surround catches white from two directions, along the street. "
            "<bookmark mark='c'/> Now put it on a crossing. The centre is on white again. But the surround "
            "catches white from four directions. More light on the surround means more inhibition, and a "
            "weaker response. So the crossing should look dimmer than the street. <bookmark mark='d'/> We can "
            "compute it. Pass the grid through a centre-surround filter, and the response on the street is "
            f"{h['street']:.2f}; at the crossing, {h['crossing']:.2f}. <bookmark mark='e'/> And the spot "
            "vanishes where you look, the account says, because at the centre of your gaze the receptive "
            "fields are tiny, smaller than the street, so centre and surround are both in the light. It "
            "explains the spots, where they are, and where they aren't. It's hard to ask for more."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(tag), FadeIn(bg), FadeIn(sq))
            vo.wait_until("a")
            self.play(FadeIn(f1, scale=0.6))
            vo.wait_until("b")
            self.play(Indicate(f1[0], color=WHITE, scale_factor=1.1), FadeIn(side[0]))
            vo.wait_until("c")
            self.play(FadeIn(f2, scale=0.6), FadeIn(side[1]))
            vo.wait_until("d")
            self.play(FadeIn(A), LaggedStart(*[FadeIn(b, shift=UP * 0.1) for b in bars], lag_ratio=0.5))
            vo.wait_until("e")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def test(self):
        h = load("hermann")
        stage = demo_stage(13.2, 6.6, tag=r"On you: \ the same grid, with wavy streets", center=[0, -0.25, 0])
        c = stage.box.get_center()
        img = picture(h["curved_image"], height=5.0).move_to(c + LEFT * 3.3 + UP * 0.2)
        ring = countdown_ring(0.45).move_to(c + np.array([6.0, 2.6, 0]))
        rows = VGroup(
            wrapped_label(r"Are the spots still there?", 5.4, 32, WHITE),
            wrapped_label(r"observers: \ the spots vanish", 5.4, 28, THRESH),
            wrapped_label(rf"the model, on this grid: \ street {h['curved_street']:.2f}, \ crossing "
                          rf"{h['curved_crossing']:.2f}. \ It still predicts spots", 5.4, 28, MODEL),
            wrapped_label(r"A crossing still has four arms. \ The account has nothing to say about straightness.",
                          5.4, 27, GREY_A),
            wrapped_label(r"A model that predicts an effect has passed half a test. \ The other half: \ does it "
                          r"predict when the effect goes away?", 5.4, 28, P.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(c + np.array([3.3, 0.1, 0]))
        src = published_tag(archive.GEIER_2008.cite).next_to(stage.box.get_corner(DL), UR, buff=0.14)
        tag = psyche_tag().next_to(stage.box.get_corner(DR), UL, buff=0.14)
        with self.voiceover(
            "So let's ask for more. Here's the same grid with one change. The streets have been given a "
            "slight wave. The squares are the same size, the streets the same width, the crossings where they "
            "were. <bookmark mark='a'/> Look at it the way you looked before. Are the spots still there? "
            "<bookmark mark='b'/> In 2008 János Geier and his colleagues reported what you've probably just "
            "found. With curved streets, the spots vanish. <bookmark mark='c'/> Now ask the model. Each "
            "crossing still has four arms of white around it, and each street two. The filter gives "
            f"{h['curved_street']:.2f} on the street and {h['curved_crossing']:.2f} at the crossing. The model "
            "still predicts spots. <bookmark mark='d'/> And nobody sees them. The account has nothing in it "
            "about whether a street is straight, so it can't be the whole explanation, and it may not be the "
            "right one at all. What does produce the spots is still argued. <bookmark mark='e'/> Take the "
            "lesson, because we'll use it for the rest of the series. A model that predicts an effect has "
            "passed half a test. The other half is whether it predicts when the effect goes away."
        ) as vo:
            self.play(FadeIn(stage), FadeIn(src), FadeIn(tag), FadeIn(img))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(ring))
            self.play(ring.t.animate.set_value(0.0), run_time=5.0, rate_func=linear)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeOut(ring))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4], shift=UP * 0.1))
        self.clear_scene()
