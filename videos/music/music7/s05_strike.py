from __future__ import annotations

import numpy as np

from videos.music.music7.common import *  # noqa: F403


class Strike(SoundScene):
    def construct(self):
        chapter(self, 4, r"The hammer", r"What happens when a string is hit instead of plucked?", lit=(1701,), extra=((1700, r"Cristofori's piano"),))
        self.cristofori()
        self.contact()
        self.dynamics()
        self.quiz()
        self.where()

    # ------------------------------------------------------------------
    def cristofori(self):
        card = history_card(1700, r"Bartolomeo Cristofori, \ Florence",
                            r"keeper of instruments to the Medici. An inventory lists a new kind of harpsichord of his ``that makes soft and loud''.", width=5.6, font_size=20).to_corner(UL, buff=0.4)
        string = Line(LEFT * 2.2, RIGHT * 6.0, color=STR, stroke_width=4).move_to(RIGHT * 2.2 + UP * 1.9)
        head = VGroup(RoundedRectangle(width=0.5, height=0.7, corner_radius=0.2, stroke_width=0, fill_color=FELT, fill_opacity=1),
                      Line(DOWN * 0.35, DOWN * 0.35 + DL * 1.6, color=WOOD, stroke_width=6))
        head.move_to(RIGHT * 0.9 + DOWN * 0.4)
        path = ArcBetweenPoints(head[0].get_top(), string.get_start() + RIGHT * 1.0 + DOWN * 0.05, angle=-0.4, color=GREY_C, stroke_width=1.5)
        notes = VGroup(label(r"a harpsichord plucks: \ every note the same loudness", font_size=26, color=GREY_A),
                       label(r"a hammer is \emph{thrown}: \ it hits the string and bounces off", font_size=26, color=FELT),
                       label(r"how fast it is thrown is all the player controls", font_size=28, color=TUNE)).arrange(DOWN, buff=0.22, aligned_edge=LEFT).move_to(RIGHT * 2.4 + DOWN * 2.3)
        with self.voiceover(
            "Now the piano. A harpsichord plucks its strings with a quill, and every note comes out equally "
            "loud whatever the player does. <bookmark mark='a'/> Around 1700, in Florence, Bartolomeo "
            "Cristofori, who looked after the Medici's instruments, built a harpsichord that could play soft "
            "and loud. Instead of a quill, each key threw a small hammer at the string. <bookmark mark='b'/> "
            "Thrown is the word. The hammer is not pushed against the string: the mechanism lets go of "
            "it just before it arrives, so that it flies the last few millimetres freely, strikes, and bounces "
            "off. <bookmark mark='c'/> So the only thing a pianist controls about a note, once the key is "
            "going down, is how fast the hammer is travelling when it leaves. Everything else that a pianist "
            "does with touch has to come out of that one number. Let us see how much is in it."
        ) as vo:
            self.play(FadeIn(notes[0]))
            vo.wait_until("a")
            self.play(FadeIn(card), FadeIn(string), FadeIn(head))
            vo.wait_until("b")
            self.play(Create(path), head.animate.shift(UP * 1.95 + LEFT * 0.75), FadeIn(notes[1]), run_time=1.0)
            self.play(head.animate.shift(DOWN * 1.2 + RIGHT * 0.3), string.animate(rate_func=there_and_back).shift(UP * 0.08), run_time=0.8)
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def contact(self):
        d = load("hammer")
        rows = {r["name"]: r for r in d["rows"]}
        g = axes([0, 4], [0, 22], x_length=6.6, y_length=3.6, xlabel=r"milliseconds after the hammer touches", ylabel=r"force between felt and string (N)", xticks=[0, 1, 2, 3, 4], yticks=[0, 5, 10, 15, 20], font_size=20)
        g.move_to(RIGHT * 2.9 + DOWN * 0.3)
        cols = {"soft": AIR, "medium": TUNE, "hard": BAD}
        curves = {k: curve_from(g, d["t_ms"], d[f"force_{k}"], cols[k]) for k in cols}
        tags = VGroup(*[label(rf"{rows[k]['velocity']:g} m/s: \ {rows[k]['contact_ms']:.1f} ms, \ {rows[k]['peak_force']:.0f} N", font_size=24, color=cols[k]) for k in cols]).arrange(DOWN, buff=0.14, aligned_edge=LEFT)
        tags.move_to(LEFT * 3.7 + DOWN * 1.2)
        model = VGroup(label(r"Monochord's middle C:", font_size=26, color=GREY_A),
                       label(rf"{100 * d['string']['L']:.0f} cm of steel at {d['string']['T'] / 9.81:.0f} kg of tension", font_size=24),
                       label(rf"a hammer of {d['hammer']['mass_g']:.0f} grams of wood and felt", font_size=24),
                       MathTex(rf"\text{{felt: \ force}} = K \cdot \text{{squeeze}}^{{\,{d['hammer']['p']}}}", font_size=30, color=FELT)).arrange(DOWN, buff=0.16, aligned_edge=LEFT).move_to(LEFT * 3.7 + UP * 1.6)
        with self.voiceover(
            f"Here is Monochord's middle C: sixty-two centimetres of steel wire under the weight of "
            f"{say(d['string']['T'] / 9.81)} kilograms, and a hammer of three grams of wood covered in felt. The "
            "felt is the interesting part. It is not an ordinary spring. <bookmark mark='a'/> The more it is "
            "squeezed, the stiffer it gets: its force rises as the squeeze to the power two and a half. "
            "<bookmark mark='b'/> Throw that hammer at the string at half a metre a second, a gentle touch. "
            f"The felt meets the string, compresses, and is thrown back off: the two are in contact for "
            f"{say(rows['soft']['contact_ms'], 1)} thousandths of a second, and the force between them peaks at "
            f"about {say(rows['soft']['peak_force'])} newtons. <bookmark mark='c'/> Now a firm touch, and then a "
            f"hard one, eight times as fast as the first. The force does not grow eight times. It grows "
            f"{say(d['force_ratio'])} times, and the blow gets shorter: {say(rows['hard']['contact_ms'], 1)} "
            "milliseconds. A harder blow is a sharper blow, because the felt has turned hard."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(m) for m in model[:3]], lag_ratio=0.5), run_time=3.0)
            vo.wait_until("a")
            self.play(FadeIn(model[3]))
            vo.wait_until("b")
            self.play(FadeIn(g), Create(curves["soft"]), FadeIn(tags[0]), run_time=2.0)
            vo.wait_until("c")
            self.play(Create(curves["medium"]), FadeIn(tags[1]), run_time=1.5)
            self.play(Create(curves["hard"]), FadeIn(tags[2]), run_time=1.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def dynamics(self):
        d = load("hammer")
        c = clip("hammer.dynamics")
        rows = d["rows"]
        cols = (AIR, TUNE, BAD)
        groups = VGroup()
        for r, col in zip(rows, cols):
            lv = d[f"levels_{r['name']}"][:12]
            pb = partial_bars(lv, width=3.4, height=2.0, db=True, floor_db=-50.0, colors=[col] * 12, font_size=14)
            groups.add(VGroup(pb, label(rf"{r['velocity']:g} m/s", font_size=26, color=col).next_to(pb, UP, buff=0.2),
                              label(rf"brightness: \ {r['centroid']:.0f} Hz", font_size=24, color=GREY_A).next_to(pb, DOWN, buff=0.2)))
        groups.arrange(RIGHT, buff=0.6).move_to(UP * 0.3)
        head = label(r"the partials of middle C, \ struck at three speeds", font_size=30, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "And a sharper blow puts more of its energy into the high partials. Here is the recipe of the note "
            "for each of the three touches, and here is how they sound: soft, medium, hard."
        ):
            self.play(FadeIn(head), FadeIn(groups))
        with self.listen(c) as snd:
            window(snd, r"middle C: \ soft, \ medium, \ hard", detail=r"a hammer on a stiff string", corner=DL, tag_corner=DR)
            for r, gp in zip(rows, groups):
                t0 = snd.time_of(r["name"])
                pulse(snd, gp, t0, t0 + 1.6, buff=0.12)
        with self.voiceover(
            f"The loud note is not the soft note turned up. Its brightness, the average frequency of its "
            f"partials, has gone from {say(rows[0]['centroid'])} hertz to {say(rows[2]['centroid'])}. On a piano, "
            "loud means bright. That is not a choice the pianist makes; it is built into the felt. It is why "
            "a recording of a quiet piano, played back loud, does not sound like a loud piano, and why piano "
            "technicians spend hours pricking hammer felt with needles to soften it: they are adjusting that "
            "power of two and a half."
        ):
            self.play(Indicate(groups[2][0], color=WHITE, scale_factor=1.03))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def quiz(self):
        c = clip("hammer.quiz")
        q = listen_card(r"Two notes, \ brought to the same loudness. \\ One was struck hard and turned down. \ One was struck softly and turned up. \ Which is which?", width=10.0, font_size=26).to_edge(UP, buff=0.4)
        bx = boxes(buff=1.8, width=3.0, height=1.4).move_to(DOWN * 0.4)
        with self.voiceover(
            "Test your ear on that. Two notes, adjusted to the same loudness. One was struck hard and then "
            "turned down. The other was struck softly and turned up. Which is which?"
        ):
            self.play(FadeIn(q, shift=DOWN * 0.2), FadeIn(bx))
        with self.listen(c) as snd:
            window(snd, r"note A, \ then note B", detail=r"equal loudness", corner=DL, tag_corner=DR)
            for ev, b in zip("AB", bx):
                t0 = snd.time_of(ev)
                pulse(snd, b, t0, t0 + 1.8)
        ans = VGroup(label(r"struck hard: \ bright, \ with an edge", font_size=28, color=BAD).next_to(bx[0], DOWN, buff=0.25),
                     label(r"struck softly: \ round and dull", font_size=28, color=AIR).next_to(bx[1], DOWN, buff=0.25))
        with self.voiceover(
            "A was the hard blow. You did not need its loudness to know. The ear reads the force of a blow from "
            "its brightness, on a piano, on a drum, and in a voice that is shouting."
        ):
            self.play(FadeOut(q), FadeIn(ans))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def where(self):
        d = load("hammer")
        title = label(r"A worked example: \ where should the hammer strike?", font_size=36).to_edge(UP, buff=0.4)
        s = StringView(width=10.0).move_to(UP * 1.6)
        hit = s.p(d["hammer"]["at"])
        ham = VGroup(RoundedRectangle(width=0.36, height=0.5, corner_radius=0.15, stroke_width=0, fill_color=FELT, fill_opacity=1)).next_to(hit, DOWN, buff=0.05)
        hl = label(rf"{100 * d['hammer']['at']:.0f}\% of the way along", font_size=24, color=FELT).next_to(ham, DOWN, buff=0.15)
        ask = pause_card(r"In Part 1, \ a string plucked at one fifth of its length had no fifth partial. \\ This hammer strikes at about one eighth. \ Which partial does it leave out?", width=9.6, font_size=26).move_to(DOWN * 1.3)
        at = d["hammer"]["at"]
        take = [20 * np.log10(max(abs(np.sin(n * np.pi * at)), 1e-3)) for n in range(1, 13)]
        pb = partial_bars(take, width=6.4, height=2.2, db=True, floor_db=-24.0, font_size=18).move_to(DOWN * 1.3 + LEFT * 2.4)
        cap = label(r"how much of a blow at this point each partial can take up (dB)", font_size=20, color=GREY_B).next_to(pb, DOWN, buff=0.12)
        mode = VMobject(stroke_color=GREY_B, stroke_width=2)
        mode.set_points_as_corners([s.p(x, 0.3 * np.sin(8 * np.pi * x)) for x in np.linspace(0, 1, 200)])
        res = VGroup(label(r"the eighth partial has a node there:", font_size=26, color=GREY_A), label(r"a blow at a node cannot start it", font_size=26, color=GREY_A),
                     label(r"pianos are struck between $\tfrac17$ and $\tfrac19$:", font_size=26, color=GOOD), label(r"the 7th, \ 8th and 9th are held back", font_size=26, color=GOOD)).arrange(DOWN, buff=0.14, aligned_edge=LEFT).move_to(RIGHT * 3.9 + DOWN * 1.2)
        with self.voiceover(
            "A worked example, and you have met it before. In Part 1, a string plucked at one fifth of its "
            "length had no fifth partial. Our hammer strikes at twelve percent of the length, about one "
            "eighth of the way along. Which partial does it leave out? Pause, and say."
        ):
            self.play(FadeIn(title), FadeIn(s), FadeIn(ham), FadeIn(hl), FadeIn(ask, shift=UP * 0.2))
        self.wait(1.5)
        with self.voiceover(
            "The eighth. That partial has a node at one eighth of the length, a point that stays still, and a "
            "blow at a point that stays still cannot set it going. <bookmark mark='a'/> Here is how much of a "
            "blow at this point each partial can take up. Our hammer is not exactly on the node, so the "
            f"eighth partial is not silent, but it is {say(abs(take[7]))} decibels down, and its neighbours, the "
            f"seventh and the ninth, are held back too, by {say(abs(take[6]))} and {say(abs(take[8]))}. In the "
            "finished note this sits on top of what the felt does, which you have just heard: a gentle blow "
            "puts very little above the seventh partial anyway. Pianos have been struck between a seventh "
            "and a ninth of the way along for two centuries. Helmholtz's explanation was this one: it holds "
            "back the seventh and ninth partials, the ones that Part 5 found had no place among the "
            "consonances."
        ) as vo:
            self.play(FadeOut(ask), Create(mode))
            vo.wait_until("a")
            self.play(FadeIn(pb), FadeIn(cap), Indicate(pb.bars[7], color=BAD, scale_factor=1.5), FadeIn(res))
        self.wait(0.3)
        self.clear_scene()
