from __future__ import annotations

from videos.psychology.psych24.common import *  # noqa: F403


def cubes(path, center=(0, 0, 0), s: float = 0.32, angle: float = 0.0, color=SEARCH, mirror: bool = False):
    """A Shepard-Metzler-like figure drawn flat: unit cubes along a path of grid steps, rotated in the plane."""
    g = VGroup()
    pos = np.zeros(2)
    pts = [pos.copy()]
    for step in path:
        pos = pos + np.array(step, float)
        pts.append(pos.copy())
    pts = np.array(pts)
    if mirror:
        pts[:, 0] = -pts[:, 0]
    pts = pts - pts.mean(0)
    c, sn = np.cos(np.radians(angle)), np.sin(np.radians(angle))
    R = np.array([[c, -sn], [sn, c]])
    for p in pts:
        q = R @ p * s
        sq = Square(s * 0.96, stroke_color=WHITE, stroke_width=1.5, fill_color=color, fill_opacity=0.75)
        sq.rotate(np.radians(angle)).move_to(np.array(center, float) + np.array([q[0], q[1], 0]))
        g.add(sq)
    return g


SHAPE = [(1, 0), (1, 0), (0, 1), (0, 1), (0, 1), (-1, 0), (-1, 0), (0, 1)]


class Imagery(VoiceoverScene):
    def construct(self):
        self.card()
        self.rotation()
        self.data()
        self.debate()

    def card(self):
        card = chapter_card(9, r"Mental imagery", r"Do you rotate a picture in your head?",
                            lit={1971: r"Shepard \& Metzler", 1978: r"Kosslyn et al.", 2015: r"Ganis \& Kievit"},
                            part=PART, scale=("mind",), marr=("how",))
        with self.voiceover("Chapter nine. Mental imagery."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def rotation(self):
        head = heading(r"Same, \ or mirror image?")
        pairs = VGroup()
        for k, (ang, mir) in enumerate(((0, False), (60, False), (120, True))):
            a = cubes(SHAPE, center=(-5.4 + 4.4 * k, 1.1, 0), s=0.27, angle=0)
            b = cubes(SHAPE, center=(-3.4 + 4.4 * k, 1.1, 0), s=0.27, angle=ang, mirror=mir)
            ans = label(r"same" if not mir else r"mirror", font_size=20, color=MODEL if not mir else LOST)
            ans.next_to(VGroup(a, b), DOWN, buff=0.2)
            pairs.add(VGroup(a, b, ans))
        rows = rows_of([
            (r"Shepard \& Metzler, \ 1971: \ pairs of drawn block figures, \ the second turned by 0 to 180 degrees; "
             r"\ same object, \ or its mirror image?", WHITE),
            (r"the time to say \emph{same} grew in a straight line with the angle: \ about one second for every 60 "
             r"degrees", SEARCH),
            (r"as if people turned a picture at a steady speed until the two lined up", MODEL),
        ], 12.6, 25, 0.34).move_to([0, -1.8, 0])
        tag = historical_tag(r"Shepard \& Metzler (1971), \ \emph{Science}")
        with self.voiceover(
            "In 1971 Roger Shepard and Jacqueline Metzler showed people pairs of drawings of block figures. "
            "<bookmark mark='a'/> The second was the same object turned through some angle, or its mirror image. "
            "Same, or mirror? <bookmark mark='b'/> The time to answer same grew in a straight line with the angle "
            "between them: about a second for every sixty degrees. <bookmark mark='c'/> It was as if people turned a "
            "picture in their heads at a steady speed until the two lined up. The figures here are flat sketches; "
            "the originals were drawn in perspective and turned in depth as well."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(rows[0]), FadeIn(pairs[0][:2]))
            vo.wait_until("a")
            self.play(FadeIn(pairs[0][2]), LaggedStart(*[FadeIn(p) for p in pairs[1:]], lag_ratio=0.5), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def data(self):
        d = load("rotation")
        head = heading(r"54 people, \ open data")
        A = axes([0, 160], [1000, 3800], x_length=5.4, y_length=3.4, xticks=[0, 50, 100, 150],
                 yticks=[1000, 2000, 3000], xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}",
                 xlabel=r"angle between the objects, \ degrees", ylabel=r"time to say \emph{same}, \ ms",
                 center=[-3.3, 0.3, 0], font_size=16)
        pts = scatter(A.ax, d["angles"], d["mean"], DATA, 0.09, 1)
        err = VGroup(*[Line(A.ax.c2p(a, m - 2 * s), A.ax.c2p(a, m + 2 * s), color=DATA, stroke_width=2)
                       for a, m, s in zip(d["angles"], d["mean"], d["se"])])
        dline = curve(A.ax, d["angles"], d["mean"], DATA, 2)
        mline = DashedVMobject(curve(A.ax, d["angles"], d["model_mean"], MODEL, 3), num_dashes=24)
        key = legend([(DATA, r"people: \ mean of 54"), (MODEL, r"Psyche: \ steady rotation")], font_size=17).move_to(
            A.ax.c2p(40, 3450))
        rate = d["median_rate"]
        rows = rows_of([
            (rf"Ganis \& Kievit, \ 2015: \ {d['n']} people, \ {num(d['n_trials'])} trials, \ objects 0, \ 50, \ "
             rf"100 or 150 degrees apart", WHITE),
            (rf"times rise from {d['mean'][0] / 1000:.1f} to {d['mean'][-1] / 1000:.1f} seconds; \ errors on mirror "
             rf"pairs from {pct(d['err_diff'][0])} to {pct(d['err_diff'][-1])}", DATA),
            (rf"fitted person by person: \ {d['positive']} of {d['n']} slopes rise; \ the median person turns about "
             rf"{rate:.0f} degrees a second", MODEL),
            (r"a steady rotation fits the trend but not the bend: \ the first 50 degrees cost the most, \ perhaps "
             r"because identical views can be matched without turning at all", GREY_A),
        ], 5.6, 22, 0.34).move_to([3.6, 0.0, 0])
        tag = psyche_tag(r"\texttt{reason.rotation\_fit}, \ \texttt{rotation\_model}; \ open data: \ Ganis \& Kievit "
                         r"(2015)")
        assert d["positive"] >= d["n"] - 2
        with self.voiceover(
            "Does it hold up? Giorgio Ganis and Rogier Kievit made a new set of these figures in 2015, tested "
            f"{d['n']} people, and released every trial. <bookmark mark='a'/> Here are the mean times to say same, "
            f"at four angles. They rise from {d['mean'][0] / 1000:.1f} seconds to {d['mean'][-1] / 1000:.1f}, and "
            f"errors on mirror pairs rise from {spct(d['err_diff'][0])} to {spct(d['err_diff'][-1])}. "
            f"<bookmark mark='b'/> Psyche fits a line to each person separately. {d['positive']} of the {d['n']} "
            f"slopes rise, and the median person turns about {rate:.0f} degrees a second. "
            "<bookmark mark='c'/> Psyche's own model rotates at that steady speed. It fits the trend, but not the "
            "bend: the first fifty degrees cost the most. Perhaps a pair seen from the same angle can be matched "
            "without rotating at all. The finding replicates; the simplest model of it is close, not exact."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(FadeIn(pts), FadeIn(err), Create(dline), FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(Create(mline), FadeIn(key), FadeIn(rows[3]))
        self.clear_scene()

    def debate(self):
        head = heading(r"Pictures in the head?")
        items = [
            (r"depictive", SEARCH, r"Kosslyn",
             [r"images are picture-like: \ scanning across a memorized map takes longer for longer distances "
              r"\ (Kosslyn, \ Ball \& Reiser, \ 1978)",
              r"imagery uses parts of the visual brain"]),
            (r"descriptive", LOGIC, r"Pylyshyn",
             [r"images are descriptions; \ the timings reflect what people know about seeing and moving, \ "
              r"\emph{tacit knowledge}",
              r"a picture in the head would need someone to look at it"]),
        ]
        cols = VGroup()
        for k, (t, c, who, lines) in enumerate(items):
            body = VGroup(label(t, font_size=32, color=c), label(who, font_size=21, color=GREY_B),
                          rows_of([(lines[0], WHITE), (lines[1], GREY_A)], 5.5, 24, 0.3)
                          ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
            box = RoundedRectangle(corner_radius=0.15, width=6.2, height=3.5, stroke_color=c, stroke_width=2,
                                   fill_color=c, fill_opacity=0.06).move_to([-3.35 + 6.7 * k, 0.8, 0])
            body.move_to(box.get_top() + DOWN * 0.3, aligned_edge=UP).align_to(box, LEFT).shift(RIGHT * 0.3)
            cols.add(VGroup(box, body))
        note = rows_of([
            (r"aphantasia: \ a few percent of people report no visual imagery at all \ (Zeman, \ Dewar \& Della "
             r"Sala, \ 2015), \ yet many of them solve rotation problems, \ often more slowly", INSIGHT),
        ], 12.6, 25, 0.3).to_edge(DOWN, buff=0.85)
        tag = published_tag(r"Kosslyn, \ Ball \& Reiser (1978); \ Pylyshyn (1981); \ Zeman et al. (2015)")
        with self.voiceover(
            "What is a mental image? A long debate had two sides. <bookmark mark='a'/> Stephen Kosslyn argued that "
            "images are picture-like. When people memorize a map and then scan an image of it, the time grows with "
            "the distance scanned, and imagery uses parts of the brain that seeing does. <bookmark mark='b'/> Zenon "
            "Pylyshyn argued that images are descriptions, and that the timings reflect what people know about how "
            "seeing and moving work. A picture in the head, he said, would need someone in the head to look at it. "
            "<bookmark mark='c'/> And a recent twist. Adam Zeman and colleagues named aphantasia in 2015: a few "
            "percent of people report no visual imagery at all. Many of them still solve rotation problems, often "
            "more slowly, which suggests there's more than one way to do it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, c in zip("ab", cols):
                vo.wait_until(m)
                self.play(FadeIn(c, shift=UP * 0.15))
            vo.wait_until("c")
            self.play(FadeIn(note))
        self.clear_scene()
