from __future__ import annotations

import numpy as np

from videos.psychology.psych10.common import *  # noqa: F403

# a typical night, drawn: (start hour, end hour, stage); stages: 0 awake, 1 REM, 2 light sleep, 3 deep sleep
NIGHT = [(0.0, 0.15, 0), (0.15, 0.5, 2), (0.5, 1.3, 3), (1.3, 1.45, 2), (1.45, 1.6, 1),
         (1.6, 2.2, 2), (2.2, 2.9, 3), (2.9, 3.05, 2), (3.05, 3.35, 1),
         (3.35, 4.2, 2), (4.2, 4.5, 3), (4.5, 4.7, 2), (4.7, 5.15, 1),
         (5.15, 6.1, 2), (6.1, 6.65, 1), (6.65, 7.4, 2), (7.4, 7.95, 1), (7.95, 8.0, 0)]


def _trace(kind: str, width: float, height: float, color, seed: int = 0) -> VMobject:
    """A few seconds of brain waves of one kind, drawn (not recorded)."""
    g = np.random.default_rng(seed)
    t = np.linspace(0, 6, 900)
    noise = np.convolve(g.normal(size=len(t)), np.ones(5) / 5, mode="same")
    if kind == "awake":
        y = 0.16 * np.sin(TAU * 19 * t + 1) + 0.12 * np.sin(TAU * 11 * t) + 0.22 * noise
    elif kind == "light":
        spindle = np.exp(-((t - 3.4) / 0.35) ** 2) * 0.55 * np.sin(TAU * 13 * t)
        y = 0.3 * np.sin(TAU * 4.5 * t) + 0.18 * np.sin(TAU * 6.5 * t + 2) + spindle + 0.15 * noise
    elif kind == "deep":
        y = 1.0 * np.sin(TAU * 0.9 * t) + 0.35 * np.sin(TAU * 1.7 * t + 1) + 0.12 * noise
    else:
        y = 0.2 * np.sin(TAU * 15 * t) + 0.16 * (2 * ((3.2 * t) % 1) - 1) + 0.2 * noise
    pts = [np.array([width * (a / 6 - 0.5), height * b / 2.6, 0]) for a, b in zip(t, y)]
    return VMobject(color=color, stroke_width=2.5).set_points_as_corners(pts)


class Stages(VoiceoverScene):
    def construct(self):
        self.card()
        self.eyes()
        self.stages()
        self.night()

    def card(self):
        card = chapter_card(3, r"Sleep, found in the laboratory", r"What is the brain doing all night?",
                            lit={1953: r"REM sleep"}, part=PART, scale=("brain", "person"), marr=("what", "tissue"))
        with self.voiceover(
            "Chapter three. Sleep, found in the laboratory."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def eyes(self):
        a = archive.ASERINSKY_1953.data
        head = heading(r"Chicago, 1953: \ the eyes of sleepers")
        g = np.random.default_rng(5)
        A = axes([0, 8], [-1.2, 1.2], x_length=7.2, y_length=1.7, xticks=[0, 2, 4, 6, 8], yticks=[],
                 xlabel=r"hours asleep", ylabel=r"", center=[-3.2, 1.45, 0])
        ax = A.ax
        t = np.linspace(0, 8, 1600)
        y = 0.03 * g.normal(size=len(t))
        for s0, s1, st in NIGHT:
            if st == 1:
                m = (t >= s0) & (t <= s1)
                y[m] += 0.85 * np.sign(g.normal(size=m.sum())) * (g.random(m.sum()) < 0.3) * g.random(m.sum())
        trace = VMobject(color=REMC, stroke_width=2).set_points_as_corners([ax.c2p(a_, b_) for a_, b_ in zip(t, y)])
        tcap = label(r"the pen that follows the eyes", font_size=27, color=REMC).next_to(A, UP, buff=0.1, aligned_edge=LEFT)
        cells = VGroup(*[Square(side_length=0.36, stroke_width=0, fill_color=REMC if i < a["dreams_rem"] else GREY_D,
                                fill_opacity=0.95) for i in range(a["awakenings_rem"])])
        cells.arrange_in_grid(rows=3, cols=9, buff=0.08).move_to([-4.3, -1.6, 0])
        ccap = wrapped_label(rf"woken during the eye movements: \ {a['dreams_rem']} of {a['awakenings_rem']} told a detailed "
                             r"dream", 3.9, 28, REMC).next_to(cells, RIGHT, buff=0.35)
        quiet = wrapped_label(r"woken while the eyes were still: \ mostly, nothing to tell", 6.8, 28, GREY_A)
        quiet.next_to(cells, DOWN, buff=0.3, aligned_edge=LEFT)
        rows = rows_of([
            (r"a graduate student, Eugene Aserinsky, \ tapes electrodes beside sleepers' eyes and lets the pens run all "
             r"night", WHITE),
            (r"several times a night, for minutes on end, \ the eyes dart about under closed lids", REMC),
            (r"so they wake people up, \ and ask", WHITE),
            (r"a paper of two pages: \ sleep is something the brain does, \ with parts, \ on a schedule", THRESH),
        ], 4.6, 28, 0.28).move_to([4.6, -0.2, 0])
        keep_in_frame(rows)
        src = historical_tag(archive.ASERINSKY_1953.cite)
        tag = note(r"the trace: a drawing, \ not a recording").to_corner(DR, buff=0.3)
        with self.voiceover(
            "Kleitman's laboratory made one more discovery, and it's the one he's remembered for. In the "
            "early nineteen-fifties his graduate student, Eugene Aserinsky, spent his nights watching "
            "sleepers' eyes. <bookmark mark='a'/> He taped electrodes beside the eyes, and let the pen "
            "recorders run all night. For most of the night the pens barely moved. <bookmark mark='b'/> "
            "But several times a night, for minutes on end, they went wild. The eyes were darting about "
            "under closed lids, quickly and jerkily, as if the sleeper were watching something. "
            "<bookmark mark='c'/> So they woke people up, and asked. Woken during the eye movements, "
            f"sleepers told a detailed dream on {a['dreams_rem']} of {a['awakenings_rem']} occasions. "
            "<bookmark mark='d'/> Woken while the eyes were still, they mostly had nothing to tell. "
            "<bookmark mark='e'/> The paper was two pages long. Before it, sleep was thought of as the "
            "brain idling, like an engine left ticking over. After it, sleep was something the brain "
            "does: an active state, with parts, on a schedule."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(tag), FadeIn(A), FadeIn(tcap))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), Create(trace), run_time=6.0, rate_func=linear)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(cells, lag_ratio=0.05), FadeIn(ccap), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(quiet))
            vo.wait_until("e")
            self.play(FadeIn(rows[3], shift=UP * 0.1))
        self.clear_scene()

    def stages(self):
        head = heading(r"With the EEG on the scalp, \ the night has stages")
        items = [
            ("awake", r"awake", VOLT, r"small, fast waves"),
            ("light", r"light sleep", GREY_B, r"slower waves, \ with bursts called spindles; \ about half the night"),
            ("deep", r"deep sleep", SLEEPC, r"large slow waves, about one a second: \ the hardest to wake from"),
            ("rem", r"REM sleep", REMC, r"waves like waking; \ the eyes dart; \ the body's muscles are switched off"),
        ]
        rows = VGroup()
        for i, (kind, name, col, what) in enumerate(items):
            y = 2.05 - 1.45 * i
            nm = label(name, font_size=33, color=col)
            nm.move_to([0, y, 0]).align_to(np.array([-6.6, 0, 0]), LEFT)
            tr = _trace(kind, 5.0, 1.0, col, seed=i).move_to([-1.55, y, 0])
            wh = wrapped_label(what, 5.0, 29, WHITE)
            wh.move_to([0, y, 0]).align_to(np.array([1.5, 0, 0]), LEFT)
            rows.add(VGroup(nm, tr, wh))
        tag = note(r"the traces: drawings, \ not recordings").to_corner(DR, buff=0.3)
        with self.voiceover(
            "Add the E E G of Part 8, with its electrodes on the scalp, and the night falls into stages. "
            "<bookmark mark='a'/> Awake, the brain's waves are small and fast. <bookmark mark='b'/> In "
            "light sleep they slow down, with short bursts of a faster rhythm called spindles. About "
            "half the night is spent here. <bookmark mark='c'/> In deep sleep the waves are large and "
            "slow, about one a second, as great numbers of cortical neurons fall silent together and then "
            "fire together. It's called slow-wave sleep, and it's the hardest to wake from. "
            "<bookmark mark='d'/> And then the stage that Aserinsky found. The brain's waves look almost "
            "like waking. The eyes dart. And the muscles of the body are switched off: the brainstem "
            "holds them paralysed, which keeps the dreamer from acting out the dream. It's called REM "
            "sleep, for rapid eye movement. Its other name is paradoxical sleep: a brain that looks "
            "awake, in a body that can't move."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), *[FadeIn(r[0]) for r in rows])
            for mark_, r in zip("abcd", rows):
                vo.wait_until(mark_)
                self.play(Create(r[1]), FadeIn(r[2]), run_time=1.6)
        self.clear_scene()

    def night(self):
        head = heading(r"A night has an architecture")
        A = axes([0, 8], [-0.4, 3.4], x_length=7.4, y_length=3.9, xticks=[0, 1, 2, 3, 4, 5, 6, 7, 8], yticks=[],
                 xlabel=r"hours after lights out", ylabel=r"", center=[-1.45, -0.15, 0])
        ax = A.ax
        level = {0: 3.0, 1: 2.2, 2: 1.2, 3: 0.2}
        names = VGroup(*[label(n, font_size=27, color=c).next_to(ax.c2p(0, level[k]), LEFT, buff=0.2)
                         for k, n, c in ((0, r"awake", VOLT), (1, r"REM sleep", REMC), (2, r"light sleep", GREY_B),
                                         (3, r"deep sleep", SLEEPC))])
        pts = []
        for s0, s1, st in NIGHT:
            pts += [ax.c2p(s0, level[st]), ax.c2p(s1, level[st])]
        stairs = VMobject(color=VOLT, stroke_width=3).set_points_as_corners(pts)
        rem = VGroup(*[Line(ax.c2p(s0, level[1]), ax.c2p(s1, level[1]), color=REMC, stroke_width=11)
                       for s0, s1, st in NIGHT if st == 1])
        deep = VGroup(*[Line(ax.c2p(s0, level[3]), ax.c2p(s1, level[3]), color=SLEEPC, stroke_width=11)
                        for s0, s1, st in NIGHT if st == 3])
        rows = rows_of([
            (r"down into deep sleep, \ back up, \ a first short period of REM: \ one cycle, about ninety minutes", WHITE),
            (r"deep sleep comes early: \ most of it is over by the middle of the night", SLEEPC),
            (r"REM comes late: \ the periods lengthen toward morning", REMC),
            (r"recorded on thousands of nights: \ today's first row in the Ledger", THRESH),
        ], 3.9, 28, 0.28).move_to([4.95, -0.1, 0])
        keep_in_frame(rows)
        tag = note(r"a typical night, drawn; \ not one person's recording").to_corner(DR, buff=0.3)
        with self.voiceover(
            "Put the stages on a time line, and a night has an architecture. <bookmark mark='a'/> Down "
            "into deep sleep within the first hour. Back up. And a first, short period of REM. Then round "
            "again. Each cycle takes about ninety minutes, and there are four or five in a night. "
            "<bookmark mark='b'/> The deep sleep comes early. Most of it is over by the middle of the "
            "night. <bookmark mark='c'/> The REM comes late. Its periods grow longer toward morning, "
            "which is why the dream you remember is usually the last one. <bookmark mark='d'/> This "
            "picture has been drawn from thousands of nights, in sleep laboratories everywhere, and it's "
            "one of the most repeated observations in psychology. But it's a description. It says what "
            "sleep looks like. It doesn't say when sleep comes, or what it's for. Those are the next "
            "four chapters."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(names))
            vo.wait_until("a")
            self.play(Create(stairs), FadeIn(rows[0]), run_time=9.0, rate_func=linear)
            vo.wait_until("b")
            self.play(FadeIn(deep), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rem), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3], shift=UP * 0.1))
        self.clear_scene()
