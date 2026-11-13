from __future__ import annotations

import numpy as np

from videos.music.music3.common import *  # noqa: F403


class Timbre(SoundScene):
    def construct(self):
        chapter(self, 10, r"More than the spectrum", r"Same recipe, \ same sound?", lit=(1863,),
                extra=((1948, r"Schaeffer's cut bell"), (1977, r"Grey's timbre space")))
        self.backwards()
        self.listen_three()
        self.what_else()

    def strips(self, d, width=10.4):
        out = VGroup()
        for key, name, col in (("fwd", r"forwards", TUNE), ("back", r"backwards", AIR), ("cut", r"its first eighth of a second removed", RATIO)):
            env = np.asarray(d[f"env_{key}"])
            a, b = np.array([-width / 2, 0, 0]), np.array([width / 2 * len(env) / 180.0 - width / 2 + 0.0, 0, 0])
            b = np.array([-width / 2 + width * len(env) / 185.0, 0, 0])
            lens = Lens(a, b, amp=0.42, color=col, opacity=0.5, shape=env, n=min(len(env), 300))
            tag = label(name, font_size=24, color=col)
            out.add(VGroup(lens, tag))
        return out

    # ------------------------------------------------------------------
    def backwards(self):
        d = load("timbre")
        st = self.strips(d)
        ys = [1.7, -0.1, -1.9]
        for row, y in zip(st, ys):
            old = row[0]
            env = old.env
            new = Lens([-5.2, y, 0], [-5.2 + (old.b[0] - old.a[0]), y, 0], amp=0.42, color=old.get_color(), opacity=0.5, shape=env, n=len(env))
            row.remove(old)
            row.add_to_back(new)
            row[1].next_to(new, UP, buff=0.08).align_to(new, LEFT)
        same = VGroup(label(r"the amount of every frequency, \ forwards and backwards:", font_size=26, color=GREY_A),
                      label(r"identical, \ to 16 decimal places", font_size=30, color=GOOD)).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Now the second half of Helmholtz's claim: that the recipe of partials is the quality of a sound. Here "
            "is the test promised at the start. <bookmark mark='a'/> Take the plucked string of Part 1: a sudden "
            "start, a long fading tail. <bookmark mark='b'/> Now play the very same recording backwards. Running a "
            "sound backwards cannot change how much of each frequency is in it: a sine wave played backwards is the "
            "same sine wave. <bookmark mark='c'/> We checked: the two spectra agree to sixteen decimal places. If "
            "the recipe were everything, these two would sound alike. <bookmark mark='d'/> And a third version: the "
            "pluck with its first eighth of a second cut off and the rest faded in."
        ) as vo:
            claim = VGroup(label(r"Helmholtz's second claim", font_size=28, color=GREY_B),
                           label(r"the recipe of partials \emph{is} the quality of a sound", font_size=36)).arrange(DOWN, buff=0.25)
            self.play(FadeIn(claim))
            vo.wait_until("a")
            self.play(FadeOut(claim), run_time=0.3)
            self.play(FadeIn(st[0]))
            vo.wait_until("b")
            self.play(FadeIn(st[1]))
            vo.wait_until("c")
            self.play(FadeIn(same))
            vo.wait_until("d")
            self.play(FadeIn(st[2]), FadeOut(same))
        self.st = st
        self.wait(0.2)

    # ------------------------------------------------------------------
    def listen_three(self):
        c = clip("timbre.three")
        st = self.st
        with self.listen(c) as snd:
            window(snd, r"one pluck: \ forwards, \ backwards, \ without its attack", corner=DL, tag_corner=UR)
            for key, row, end in (("fwd", st[0], snd.time_of("back") - 0.4), ("back", st[1], snd.time_of("cut") - 0.4), ("cut", st[2], c.duration)):
                t0 = snd.time_of(key)
                snd.wait_until(t0)
                lens = row[0]
                x0, x1 = lens.a[0], lens.b[0]
                head = Line([x0, lens.a[1] - 0.5, 0], [x0, lens.a[1] + 0.5, 0], color=WHITE, stroke_width=2)
                snd.show(head)
                snd.drive(head, lambda m, t, t0=t0, end=end, x0=x0, x1=x1: m.set_x(x0 + (x1 - x0) * float(np.clip((t - t0) / (end - t0), 0, 1))).set_opacity(1.0 if t0 <= t < end else 0.0))
                snd.wait_until(end)
        with self.voiceover(
            "Three different instruments. The first is a plucked string. The second swells like something bowed, or "
            "an accordion, and ends with a snap. The third has lost whatever made it a pluck: it could be almost "
            "anything. The recipe barely changed. The sound did."
        ):
            self.play(Indicate(st[1][1], color=WHITE, scale_factor=1.1), Indicate(st[2][1], color=WHITE, scale_factor=1.1))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def what_else(self):
        d = load("timbre")
        g = axes([0, 1.7], [220, 440], x_length=5.6, y_length=3.0, xlabel=r"seconds after the pluck", ylabel=r"brightness: \ centre of the spectrum (Hz)",
                 xticks=[0, 0.5, 1.0, 1.5], yticks=[250, 300, 350, 400], font_size=20)
        g.move_to(LEFT * 3.6 + DOWN * 1.0)
        tt = np.arange(len(d["centroid"])) * d["centroid_dt"]
        line = curve(g.ax, tt, d["centroid"], RATIO, stroke_width=3)
        head = VGroup(*[label(t, font_size=22, color=GREY_B) for t in (r"", r"attack", r"brightness")])
        rows = VGroup(head)
        for r in d["rows"]:
            att = rf"{r['attack_ms']:.0f} ms" if r["attack_ms"] < 1000 else rf"{r['attack_ms'] / 1000:.1f} s"
            rows.add(VGroup(label(r["name"], font_size=26), label(att, font_size=26, color=TIME), label(rf"{r['centroid']:.0f} Hz", font_size=26, color=FREQ)))
        xs = [0.2, 3.2, 4.8]
        for i, r in enumerate(rows):
            for cell, x in zip(r, xs):
                cell.move_to([x, 2.9 - 0.5 * i, 0], aligned_edge=LEFT)
        cards = VGroup(history_card(1948, r"Pierre Schaeffer", r"cuts the attack off a recorded bell: it sounds like an oboe", width=5.6),
                       history_card(1977, r"John Grey", r"listeners sort instrument tones along three axes: brightness, attack, "
                                    r"and how the spectrum changes during the note", width=5.6)).arrange(DOWN, buff=0.2).move_to(RIGHT * 3.4 + DOWN * 1.6)
        with self.voiceover(
            "So what else is there? Measure the three sounds. <bookmark mark='a'/> Their overall brightness, the "
            "centre of gravity of the spectrum, is nearly the same. What differs is the attack: six thousandths of "
            "a second for the pluck, a hundred and seventy for the cut one, most of two seconds backwards. "
            "<bookmark mark='b'/> And within one note the recipe is not fixed at all. The pluck starts bright and "
            "its brightness slides down as the high partials die. A spectrum of the whole note averages that story "
            "away. <bookmark mark='c'/> In 1948 Pierre Schaeffer, working with disc recorders in a Paris radio "
            "studio, cut the attack off a recorded bell and found he had made an oboe. "
            "<bookmark mark='d'/> And in 1977 John Grey asked listeners to judge how alike instrument tones were. "
            "Their answers needed three axes: brightness, attack, and how the spectrum moves during the note. "
            "Timbre is a recipe that changes in time, and the first tenth of a second matters most. Synthesizer "
            "builders learned this the practical way: the first thing they gave every sound was a shape in time, an "
            "attack, a decay, a level to hold and a release. We will build that in Part 51."
        ) as vo:
            ask = label(r"So what else is there?", font_size=40, color=TUNE).to_corner(UL, buff=0.6)
            self.play(FadeIn(ask))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.3), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(g), Create(line), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(cards[0]))
            vo.wait_until("d")
            self.play(FadeIn(cards[1]))
        self.wait(0.3)
        self.clear_scene()
