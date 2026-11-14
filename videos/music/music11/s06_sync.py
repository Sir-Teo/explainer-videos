from __future__ import annotations

import numpy as np

from videos.music.music11.common import *  # noqa: F403


def rhythm_panel(weights, pattern: str, width: float = 10.0, row: float = 0.3) -> VGroup:
    """A rhythm over the metre's grid of dots."""
    g = dot_grid(weights, width=width, row=row, radius=0.07)
    pr = pattern_row(pattern, g.xs, y=-0.55, size=min(0.4, 0.7 * g.pitch))
    out = VGroup(g, pr)
    out.grid, out.row = g, pr
    return out


class Sync(SoundScene):
    def construct(self):
        chapter(self, 5, r"Syncopation", r"Can ``off the beat'' be measured?", extra=((1984, r"Longuet-Higgins and Lee"),))
        self.idea()
        self.four()
        self.quiz()
        self.flip()
        self.groove()

    # ------------------------------------------------------------------
    def idea(self):
        d = load("sync")
        w = d["weights"]
        clave = d["patterns"][1]
        p = rhythm_panel(w, clave["pattern"], width=11.0, row=0.34).move_to(UP * 0.9)
        nums = VGroup(*[label(str(x), font_size=22, color=GREY_B).move_to([col.get_x(), p.row.get_y() - 0.5, 0]) for x, col in zip(w, p.grid.cols)])
        head = label(r"a rhythm from Cuba: \ the son clave", font_size=28, color=GREY_A).to_edge(UP, buff=0.45)
        cells = p.row.cells
        a1 = CurvedArrow(cells[3].get_bottom() + DOWN * 0.75, cells[4].get_bottom() + DOWN * 0.75, color=BAD, angle=0.9, stroke_width=3, tip_length=0.16)
        a2 = CurvedArrow(cells[6].get_bottom() + DOWN * 0.75, cells[8].get_bottom() + DOWN * 0.75, color=BAD, angle=0.7, stroke_width=3, tip_length=0.16)
        t1 = label(r"$3 - 1 = 2$", font_size=26, color=BAD).next_to(a1, DOWN, buff=0.1)
        t2 = label(r"$4 - 2 = 2$", font_size=26, color=BAD).next_to(a2, DOWN, buff=0.1)
        total = label(rf"syncopation index: \ {clave['index']}", font_size=34, color=TUNE).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "Now put a rhythm on the grid. The filled squares are where notes begin; the dots above are "
            "the meter's weights. <bookmark mark='a'/> A note on a strong moment confirms the meter. The "
            "interesting case is the reverse: a note on a weak moment, followed by silence on a stronger "
            "one. The listener's grid expected something there, and got nothing. That is a syncopation. "
            "<bookmark mark='b'/> In 1984 Christopher Longuet-Higgins and Christopher Lee made it a "
            "number. Find every note that is followed by a silent moment stronger than itself, and add "
            "up the differences in weight. <bookmark mark='c'/> Here the second note has weight one, and "
            "the silence after it has weight three: two. <bookmark mark='d'/> The third note has weight "
            "two, and the silent middle of the bar has four: two more. <bookmark mark='e'/> The last two "
            "notes are followed by nothing stronger. This rhythm scores four."
        ) as vo:
            self.play(FadeIn(head), FadeIn(p.grid), FadeIn(nums))
            self.play(LaggedStart(*[FadeIn(x) for x in cells], lag_ratio=0.05), run_time=1.5)
            vo.wait_until("a")
            self.play(Indicate(cells[0], color=WHITE), Indicate(p.grid.cols[0], color=WHITE))
            vo.wait_until("c")
            self.play(Create(a1), FadeIn(t1))
            vo.wait_until("d")
            self.play(Create(a2), FadeIn(t2))
            vo.wait_until("e")
            self.play(FadeIn(total))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def four(self):
        d = load("sync")
        c = clip("sync.four")
        w = d["weights"]
        rows = VGroup()
        for pt in d["patterns"]:
            g = dot_grid(w, width=7.4, row=0.0, radius=0.0)
            pr = pattern_row(pt["pattern"], g.xs, y=0.0, size=0.3)
            rows.add(VGroup(label(pt["name"], font_size=26, color=GREY_A), pr, label(str(pt["index"]), font_size=36, color=TUNE)))
        for r in rows:
            r[1].move_to(ORIGIN)
            r[0].next_to(r[1], LEFT, buff=0.4)
            r[2].next_to(r[1], RIGHT, buff=0.5)
        rows.arrange(DOWN, buff=0.55)
        for r in rows:
            r[1].set_x(0.6)
            r[0].next_to(r[1], LEFT, buff=0.4)
            r[2].next_to(r[1], RIGHT, buff=0.5)
        rows.move_to(UP * 0.5)
        top = dot_grid(w, width=7.4, row=0.16, radius=0.045).next_to(rows, UP, buff=0.3).set_x(rows[0][1].get_x())
        idx = label(r"index", font_size=22, color=GREY_B).next_to(rows[0][2], UP, buff=0.35)
        note = listen_note(r"four rhythms on a clave, \ each twice, \ over a bass drum that keeps the beat", width=9.6, font_size=26).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Here are four rhythms with their scores, from none at all to seven. You will hear each one "
            "twice on a clave, over a bass drum that plays the four beats, so that you always know where "
            "the grid is."
        ):
            self.play(FadeIn(top), LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.3), FadeIn(idx), FadeIn(note), run_time=2.5)
        self.play(FadeOut(note))
        with self.listen(c) as snd:
            window(snd, r"four rhythms, \ more and more off the beat", detail=r"clave and bass drum, \ modelled", corner=DL, tag_corner=DR)
            for k, (pt, r) in enumerate(zip(d["patterns"], rows)):
                t0 = d["starts"][k]
                pulse(snd, r[0], t0, t0 + 4.0, buff=0.1)
                on = [i for i, ch in enumerate(pt["pattern"]) if ch == "x"]
                ts = [t0 + (rep * 16 + i) * d["pulse"] for rep in range(2) for i in on]
                flash(snd, [r[1].cells[i] for rep in range(2) for i in on], ts, base=TUNE, hot=WHITE, fade=0.12)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("sync")
        c = clip("sync.quiz")
        card = listen_card(r"Two rhythms over the same bass drum. \ Which is more syncopated: \ A or B?", width=9.0)
        with self.voiceover("Your turn. Two rhythms over the same bass drum. Which is the more syncopated: A or B?"):
            self.play(FadeIn(card))
        self.wait(0.8)
        bx = boxes(("A", "B"), buff=1.2, width=2.4, height=1.2, font_size=48).move_to(UP * 1.8)
        self.play(FadeOut(card), FadeIn(bx))
        with self.listen(c) as snd:
            window(snd, r"A, \ then B", detail=r"clave and bass drum, \ modelled", corner=DL, tag_corner=DR)
            pulse(snd, bx[0], snd.time_of("A"), snd.time_of("B") - 0.9)
            pulse(snd, bx[1], snd.time_of("B"), c.duration)
        w = d["weights"]
        pa = rhythm_panel(w, d["quiz"]["A"], width=5.6, row=0.2).move_to(LEFT * 3.3 + DOWN * 0.8)
        pb = rhythm_panel(w, d["quiz"]["B"], width=5.6, row=0.2).move_to(RIGHT * 3.3 + DOWN * 0.8)
        la = label(rf"A: \ index {d['quiz_index']['A']}", font_size=30, color=GREY_A).next_to(pa, DOWN, buff=0.35)
        lb = label(rf"B: \ index {d['quiz_index']['B']}", font_size=30, color=TUNE).next_to(pb, DOWN, buff=0.35)
        with self.voiceover(
            f"B. Its index is {say(d['quiz_index']['B'])}, against {say(d['quiz_index']['A'])} for A. In A "
            "only two notes leave a stronger moment empty. In B the notes come every three sixteenths, "
            "so they drift across the beats of the bar and land on only one of them."
        ):
            self.play(FadeIn(pa), FadeIn(pb), FadeIn(la), FadeIn(lb))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def flip(self):
        d = load("sync")
        c = clip("sync.flip")
        w = d["weights"]
        heard = rhythm_panel(w, "x...x...x...x...", width=5.6, row=0.2).move_to(LEFT * 3.3 + UP * 0.3)
        played = rhythm_panel(w, "..x...x...x...x.", width=5.6, row=0.2).move_to(RIGHT * 3.3 + UP * 0.3)
        lh = label(r"alone: \ these strokes are the beat. \ Index 0", font_size=28, color=GREY_A).next_to(heard, DOWN, buff=0.4)
        lp = label(r"with the drum: \ the same strokes are off the beat. \ Index 7", font_size=28, color=TUNE).next_to(played, DOWN, buff=0.4)
        note = listen_note(r"strokes half a second apart, \ alone. \ Tap along with them. \ Then a bass drum joins: \ where does it fall?", width=10.0, font_size=26)
        with self.voiceover(
            "One thing about this number should bother you. It needs a grid, and chapter one said that "
            "the grid is in the listener. So try this. Here are clave strokes half a second apart, with "
            "nothing else. Tap along with them. After a while a bass drum joins. Notice where it falls."
        ):
            self.play(FadeIn(note))
        self.play(FadeOut(note))
        lamp = Dot(radius=0.3, color=TUNE).move_to(LEFT * 1.6)
        drum = Dot(radius=0.42, color=LOW).move_to(RIGHT * 1.6)
        self.add(lamp, drum)
        with self.listen(c) as snd:
            window(snd, r"strokes alone; \ then a drum", detail=r"clave and bass drum, \ modelled", corner=DL, tag_corner=DR)
            ft, fb = np.asarray(d["flip_times"]), np.asarray(d["flip_beats"])
            snd.drive(lamp, lambda m, t: m.set_opacity(float(np.exp(-9.0 * (t - ft[max(np.searchsorted(ft, t, side="right") - 1, 0)]))) if t >= ft[0] else 0.0))
            snd.drive(drum, lambda m, t: m.set_opacity(float(np.exp(-9.0 * (t - fb[max(np.searchsorted(fb, t, side="right") - 1, 0)]))) if t >= fb[0] else 0.0))
        self.remove(lamp, drum)
        with self.voiceover(
            "Alone, those strokes were the beat. You tapped with them, and their index was zero. "
            "<bookmark mark='a'/> Then the drum arrived in between, and the very same strokes turned "
            "into off-beats, with an index of seven. Nothing about the strokes had changed. Syncopation "
            "is not a property of a rhythm. It is a rhythm set against a grid that something else is "
            "holding: a drum, a bass, or the listener's memory of the bars before."
        ) as vo:
            self.play(FadeIn(heard), FadeIn(lh))
            vo.wait_until("a")
            self.play(FadeIn(played), FadeIn(lp))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def groove(self):
        g = axes([0, 10], [0, 1.1], x_length=8.0, y_length=3.0, xlabel=r"how syncopated the drum pattern is", ylabel=r"``makes me want to move''", xticks=[], yticks=[], font_size=24).move_to(UP * 0.4)
        xs = np.linspace(0.3, 9.7, 80)
        arch = curve_from(g, xs, 0.25 + 0.75 * np.exp(-0.5 * ((xs - 4.2) / 2.3) ** 2), TUNE, stroke_width=4)
        tags = VGroup(label(r"nothing to resolve", font_size=22, color=GREY_B).move_to(g.ax.c2p(1.3, 0.18)), label(r"the grid is lost", font_size=22, color=GREY_B).move_to(g.ax.c2p(8.6, 0.18)),
                      label(r"the most pleasure", font_size=24, color=TUNE).move_to(g.ax.c2p(4.2, 0.6)))
        src = label(r"the shape reported by Witek and colleagues (2014) for fifty drum breaks; \ drawn schematically", font_size=22, color=GREY_B).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Why would anyone want a rhythm that fights the meter? In 2014 Maria Witek and her "
            "colleagues played fifty drum patterns to listeners on the web and asked two things: does "
            "this make you want to move, and do you enjoy it? <bookmark mark='a'/> Plotted against a "
            "syncopation index like ours, both answers made an arch. With no syncopation there is "
            "nothing for the body to do: the pattern says only what the meter already said. With too "
            "much, the listener loses the grid. In the middle, the listener's own beat has to fill the "
            "gaps the drummer leaves, and that seems to be the pleasure of it."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(Create(arch), FadeIn(src), run_time=2.0)
            self.play(LaggedStart(*[FadeIn(t) for t in tags], lag_ratio=0.5), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
