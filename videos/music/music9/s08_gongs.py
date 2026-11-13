from __future__ import annotations

import numpy as np

from videos.music.music9.common import *  # noqa: F403


class Gongs(SoundScene):
    def construct(self):
        chapter(self, 7, r"Gongs and cymbals", r"Why does a gong's pitch move, and what is a crash?", lit=(1883,), extra=((1983, r"Rossing and Fletcher on gongs"),))
        self.glide()
        self.crash()

    # ------------------------------------------------------------------
    def glide(self):
        d = load("gongs")
        c = clip("gongs.pair")
        g = axes([0, 3], [200, 370], x_length=7.0, y_length=3.6, xlabel=r"seconds after the blow", ylabel=r"pitch of the lowest partial (Hz)", xticks=[0, 1, 2, 3], yticks=[220, 260, 300, 340], font_size=20)
        g.move_to(RIGHT * 2.8 + DOWN * 0.6)
        cd = curve_from(g, d["t"], d["down"], BRONZE)
        cu = curve_from(g, np.asarray(d["t"])[:240], np.asarray(d["up"])[:240], AIR)
        ld = label(rf"a large gong: \ falls {d['down_cents']:.0f} cents", font_size=24, color=BRONZE).next_to(g.ax.c2p(1.5, 225), UP, buff=0.15)
        lu = label(rf"a small one: \ rises {abs(d['up_cents']):.0f}", font_size=24, color=AIR).next_to(g.ax.c2p(1.6, 350), DOWN, buff=0.2)
        notes = VGroup(label(r"so far, \ pitch has not \\ depended on loudness", font_size=26, color=GREY_A),
                       label(r"a thin plate, \ struck hard, \\ stretches as it bends: \\ stiffer while it is loud", font_size=26, color=BRONZE),
                       label(r"a shallow dome can \\ do the opposite", font_size=26, color=AIR)).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(LEFT * 4.3 + DOWN * 0.4)
        note = listen_note(r"Two gongs. \ Follow the pitch of each as it dies away.", width=7.6, font_size=24).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Everything so far has obeyed one quiet rule: the pitch of a thing does not depend on how hard "
            "you hit it. A loud note and a soft one are the same note. Part 1 mentioned that a string "
            "stretched far enough breaks the rule slightly. <bookmark mark='a'/> A thin metal plate breaks "
            "it thoroughly. When a plate bends a long way, it also has to stretch, and stretching makes it "
            "stiffer. So while the motion is large the plate is stiffer than it will be later, and its "
            "pitch is higher. As the sound dies away, the pitch sinks. <bookmark mark='b'/> A shallow dome "
            "can do the opposite: bending flattens it, which makes it less stiff, so it starts low and "
            "climbs. The orchestra of the Chinese opera has one gong of each kind. Listen, and follow the "
            "pitch of each."
        ) as vo:
            self.play(FadeIn(notes[0]), FadeIn(g))
            vo.wait_until("a")
            self.play(FadeIn(notes[1]))
            vo.wait_until("b")
            self.play(FadeIn(notes[2]), FadeIn(note))
        cd.set_stroke(opacity=0.35)
        cu.set_stroke(opacity=0.35)
        td, tu = np.asarray(d["t"]), np.asarray(d["t"])[:240]
        dot_d = Dot(g.ax.c2p(0, d["down"][0]), radius=0.11, color=BRONZE).set_opacity(0)
        dot_u = Dot(g.ax.c2p(0, d["up"][0]), radius=0.11, color=AIR).set_opacity(0)
        self.add(cd, cu, dot_d, dot_u)
        with self.listen(c) as snd:
            window(snd, r"two gongs", kind="synthesized", detail=r"modes whose stiffness changes with their size", corner=DL, tag_corner=DR)
            t_f, t_r = snd.time_of("falls"), snd.time_of("rises")

            def follow_down(m, t):
                u = float(np.clip(t - t_f, 0.0, 3.0))
                return m.set_opacity(1.0 if t_f <= t < t_r - 0.3 else 0.0).move_to(g.ax.c2p(u, float(np.interp(u, td, d["down"]))))

            def follow_up(m, t):
                u = float(np.clip(t - t_r, 0.0, 2.4))
                return m.set_opacity(1.0 if t >= t_r else 0.0).move_to(g.ax.c2p(u, float(np.interp(u, tu, np.asarray(d["up"])[:240]))))

            snd.drive(dot_d, follow_down)
            snd.drive(dot_u, follow_up)
            snd.drive(cd, lambda m, t: m.set_stroke(opacity=1.0 if t >= t_f else 0.35))
            snd.drive(cu, lambda m, t: m.set_stroke(opacity=1.0 if t >= t_r else 0.35))
        cd.set_stroke(opacity=1)
        cu.set_stroke(opacity=1)
        dot_d.set_opacity(0)
        dot_u.set_opacity(0)
        with self.voiceover(
            f"The first fell by {say(d['down_cents'])} cents, a whole tone, as it faded. The second rose by "
            "nearly as much. No tension was changed and nothing was retuned. The gong's pitch is a record "
            "of its own loudness."
        ):
            self.play(FadeOut(note), FadeIn(ld), FadeIn(lu))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def crash(self):
        d = load("gongs")
        c = clip("gongs.crash")
        rng = np.random.default_rng(9)
        f = np.sort(rng.uniform(d["cymbal_lo"], d["cymbal_hi"], d["cymbal_modes"]))
        g = axes([0, 13000], [0, 1], x_length=11.0, y_length=1.6, xlabel=r"frequency (Hz)", ylabel="", xticks=[0, 2000, 4000, 6000, 8000, 10000, 12000], yticks=[], font_size=20).move_to(UP * 0.6)
        ticks = VGroup(*[Line(g.ax.c2p(v, 0), g.ax.c2p(v, 0.75), color=STEEL, stroke_width=1.2) for v in f])
        head = label(rf"A cymbal: \ {d['cymbal_modes']} partials, \ and no pattern", font_size=34, color=GREY_A).to_edge(UP, buff=0.45)
        note = listen_note(r"A sketch of a crash. \ Listen for the brightness arriving a moment after the blow.", width=9.4, font_size=24).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "A cymbal goes further. It is so thin, and struck so hard, that its modes do not merely shift. "
            "They trade energy with each other. <bookmark mark='a'/> A cymbal has hundreds of modes within "
            "the range of hearing, crowded together with no pattern at all. The stick sets the low ones "
            "going. Within a few hundredths of a second, energy has spilled from them into the modes above, "
            "and from those into the ones above them, in a cascade, the way a large eddy in a stream breaks "
            "into smaller ones. That is the crash: not a note, but a shimmer that brightens just after the "
            "blow. Here is a sketch of one, made from four hundred and twenty partials."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(t) for t in ticks], lag_ratio=0.004), FadeIn(note), run_time=4.0)
        with self.listen(c) as snd:
            window(snd, r"a cymbal, \ sketched", kind="synthesized", detail=r"420 partials, \ the high ones late", corner=UL, tag_corner=UR)
            snd.drive(ticks, lambda m, t: [tk.set_stroke(opacity=float(np.clip((1 - np.exp(-t / (0.004 + 0.05 * fk / 13000.0))) * np.exp(-t * (0.9 + 2.2 * fk / 13000.0)) * 2.2, 0.08, 1.0))) for tk, fk in zip(m, f)] and m)
        with self.voiceover(
            "I call it a sketch because I told each partial when to arrive. In a real cymbal nobody tells "
            "them. The cascade follows from the plate's own equations, and computing it honestly is one of "
            "the frontiers we will come to."
        ):
            self.play(FadeOut(note))
        self.wait(0.3)
        self.clear_scene()
