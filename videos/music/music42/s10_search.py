from __future__ import annotations

import numpy as np

from videos.music.music42.common import *  # noqa: F403


class Search(SoundScene):
    def construct(self):
        chapter(self, 9, r"A searcher with critics", r"What does a program need in order to judge its own drafts?")
        self.critics()
        self.loop()
        self.rejections()
        self.hear_rejected()
        self.climb()
        self.hear_best()
        self.cope()

    # ------------------------------------------------------------------
    def critics(self):
        hard = VGroup(label(r"hard critics: \ refuse the draft", font_size=21, color=EAR),
                      label(r"leaps: \ no tritone, \ seventh, \ or more than an octave \ (Part 14)", font_size=18, color=WHITE),
                      label(r"cadence: \ end on C, \ on a downbeat, \ by step", font_size=18, color=WHITE),
                      label(r"range: \ no wider than a tenth", font_size=18, color=WHITE),
                      label(r"parallels: \ no fifths or octaves with the bass \ (Part 16)", font_size=18, color=WHITE),
                      label(r"harmony: \ three in four strong beats on chord tones \ (Part 18)", font_size=18, color=WHITE)).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        soft = VGroup(label(r"soft critics: \ score what survives, \ 0 to 1", font_size=21, color=TUNE),
                      label(r"recovered: \ leaps followed by a step back \ (Part 14's gap fill)", font_size=18, color=WHITE),
                      label(r"unity: \ bars the motive yields in two operations \ (chapter 2)", font_size=18, color=WHITE),
                      label(r"variety: \ bars not repeated note for note", font_size=18, color=WHITE),
                      label(r"tension: \ correlation with the plan \ (chapter 4)", font_size=18, color=WHITE),
                      label(r"harmony and flow: \ chord tones; \ no bar stuck on one held note", font_size=18, color=WHITE)).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        g = VGroup(hard, soft).arrange(RIGHT, buff=0.7, aligned_edge=UP)
        g.scale_to_fit_width(min(g.width, 12.8)).move_to(DOWN * 0.2)
        head = label(r"the critics: \ Act III's rules, \ turned into functions", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Now the searcher itself. Its judges are the series' own rules, turned into functions. <bookmark mark='a'/> Hard "
            "critics refuse a draft outright: no forbidden leap, from Part 14; a cadence on C; a range no wider than a tenth; "
            "no parallel fifths or octaves with the bass, from Part 16; and at least three in four strong beats on chord "
            "tones. <bookmark mark='b'/> Soft critics score what survives, each from zero to one: leaps recovered by a step "
            "back; unity and variety, from chapter two; how well the tension follows the plan, from chapter four; chord "
            "tones, and flow."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(hard))
            vo.wait_until("b")
            self.play(FadeIn(soft))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def loop(self):
        boxes = VGroup()
        texts = [(r"generate a draft: \ a random developing variation of the motive, \ each bar a chord tone away from the last", WHITE),
                 (r"hard critics: \ refuse it, \ and note why", EAR),
                 (r"soft critics: \ score it", TUNE),
                 (r"keep it if it beats the best so far", WHITE)]
        for t, col in texts:
            b = RoundedRectangle(width=9.6, height=0.85, corner_radius=0.15, stroke_color=col, stroke_width=2)
            boxes.add(VGroup(b, label(t, font_size=19, color=WHITE).move_to(b)))
        boxes.arrange(DOWN, buff=0.35).move_to(LEFT * 0.6 + DOWN * 0.1)
        arrows = VGroup(*[Arrow(boxes[i].get_bottom(), boxes[i + 1].get_top(), buff=0.05, color=GREY_B, stroke_width=3) for i in range(3)])
        back = CurvedArrow(boxes[3].get_right() + RIGHT * 0.1, boxes[0].get_right() + RIGHT * 0.1, angle=PI / 2, color=GREY_B)
        rep = label(r"2,000 times", font_size=19, color=GREY_A).next_to(back, RIGHT, buff=0.15)
        head = label(r"generate and test", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "The loop is Hiller and Isaacson's, with better parts. <bookmark mark='a'/> Generate a draft: a random developing "
            "variation, the motive stated first, then each bar a random chain of up to two operations, placed on a chord tone "
            "near where the last bar ended. <bookmark mark='b'/> Let the hard critics refuse it, and note why. "
            "<bookmark mark='c'/> Let the soft critics score it, and keep it if it beats the best so far. "
            "<bookmark mark='d'/> Two thousand times."
        ) as vo:
            self.play(FadeIn(head), FadeIn(boxes[0]))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(GrowArrow(arrows[0]), FadeIn(boxes[1]))
            vo.wait_until("c")
            self.play(GrowArrow(arrows[1]), FadeIn(boxes[2]), GrowArrow(arrows[2]), FadeIn(boxes[3]))
            vo.wait_until("d")
            self.play(Create(back), FadeIn(rep))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def rejections(self):
        d = load("search")
        rej = d["rejected"]
        order = sorted(rej, key=lambda k: -rej[k]) + ["kept to score"]
        vals = dict(rej, **{"kept to score": d["survivors"]})
        x0, W = -2.0, 7.0
        mx = max(vals.values())
        bars = VGroup()
        for i, k in enumerate(order):
            w = W * vals[k] / mx
            y = 1.4 - 0.7 * i
            bars.add(VGroup(label(k, font_size=20, color=WHITE).move_to([x0 - 0.3, y, 0], aligned_edge=RIGHT),
                            Rectangle(width=max(w, 0.03), height=0.42, stroke_width=0, fill_color=TUNE if k == "kept to score" else EAR, fill_opacity=0.85).move_to([x0 + w / 2, y, 0]),
                            label(f"{vals[k]:,}", font_size=18, color=WHITE).move_to([x0 + w + 0.25, y, 0], aligned_edge=LEFT)))
        head = label(rf"{d['drafts']:,} drafts, \ and the first critic that refused each", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        cap = label(r"most drafts die at the seams: \ a bar moved to fit its chord leaps badly from the bar before", font_size=18, color=GREY_A).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            f"Of {say(d['drafts'])} drafts, <bookmark mark='a'/> {say(rej['leaps'])} die on a forbidden leap, "
            f"{say(rej['parallels'])} on parallels with the bass, {say(rej['range'])} on range, and {say(rej['harmony'])} on "
            f"harmony. Only {say(d['survivors'])} survive to be scored. Most deaths happen at the seams between bars: a "
            "figure moved to fit its chord leaps badly from the bar before. A composer's hand does that join without "
            "thinking; the searcher has to be told."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b) for b in bars], lag_ratio=0.2), FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hear_rejected(self):
        d = load("search")
        c = clip("search.rejected")
        shown = d["shown"]
        cells = VGroup()
        for s in shown:
            r = scored(s["melody"], d["chords"], width=3.8, height=1.3, lo=50, hi=86, size=11)
            cells.add(VGroup(label(rf"draft {s['draft']}", font_size=18, color=WHITE), r, label(WHY[s["why"]], font_size=15, color=EAR)).arrange(DOWN, buff=0.15))
        cells.arrange(RIGHT, buff=0.45).move_to(UP * 0.2)
        head = label(r"three drafts it threw away", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        reasons = ", then ".join(f"draft {say(s['draft'])}, for {WHY_SAID[s['why']]}" for s in shown)
        with self.voiceover(f"Hear three of the drafts it threw away, each for a different reason: {reasons}."):
            self.play(FadeIn(head), FadeIn(cells))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"rejected drafts", detail=r"Part 7's piano, \ a plucked bass", corner=DL, tag_corner=DR)
            for i, s in enumerate(shown):
                t0 = st[f"r{i}"]
                end = st[f"r{i + 1}"] - 0.3 if i + 1 < len(shown) else c.duration
                pulse(snd, cells[i], t0, end, buff=0.08)
                cursor(snd, cells[i][1], t0, 0.42)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def climb(self):
        d = load("search")
        imp = d["improvements"]
        x0, y0, W, H = -5.0, -1.8, 8.0, 3.2
        lo_, hi_ = 0.7, 0.92
        def X(n):
            return x0 + W * np.log10(n) / np.log10(d["drafts"])
        def Y(v):
            return y0 + H * (v - lo_) / (hi_ - lo_)
        pts = []
        for i, (n, v) in enumerate(imp):
            if pts:
                pts.append([X(n), pts[-1][1], 0])
            pts.append([X(n), Y(v), 0])
        pts.append([X(d["drafts"]), pts[-1][1], 0])
        stair = VMobject(color=TUNE, stroke_width=4).set_points_as_corners(pts)
        dots = VGroup(*[Dot([X(n), Y(v), 0], radius=0.07, color=TUNE) for n, v in imp])
        labs = VGroup(*[label(rf"draft {n:,}: \ {v:.3f}", font_size=15, color=WHITE).next_to(Dot([X(n), Y(v), 0]), UP + LEFT * 0.3, buff=0.08) for n, v in imp])
        ax = VGroup(Line([x0, y0, 0], [x0 + W, y0, 0], color=GREY_B), Line([x0, y0, 0], [x0, y0 + H, 0], color=GREY_B))
        ticks = VGroup(*[label(f"{n:,}", font_size=14, color=GREY_A).move_to([X(n), y0 - 0.3, 0]) for n in (1, 10, 100, 1000)])
        xl = label(r"draft number \ (logarithmic)", font_size=16, color=GREY_A).move_to([x0 + W / 2, y0 - 0.7, 0])
        head = label(r"the best score so far", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            f"Here is the best score so far, draft by draft, on a logarithmic axis. <bookmark mark='a'/> It improves "
            f"{say(len(imp))} times, the last at draft {say(imp[-1][0])}, and each improvement is smaller than the one "
            "before. Random search finds good drafts quickly and excellent ones slowly; a composer's training is, in part, "
            "a better generator."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(ticks), FadeIn(xl))
            vo.wait_until("a")
            self.play(Create(stair), FadeIn(dots), FadeIn(labs), run_time=2.0)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hear_best(self):
        d = load("search")
        c = clip("search.best")
        b = d["best"]
        g = scored(b["melody"], d["chords"], width=11.6, height=2.1, lo=57, hi=81).move_to(UP * 0.6)
        ders = VGroup()
        for k, der in enumerate(b["derivations"]):
            txt = r"cadence" if k == len(b["derivations"]) - 1 else (r"the motive" if der == [] else (r"bent" if der is None else r" + ".join(x.replace("first three notes", "3 notes") for x in der)))
            x = g.frame.get_left()[0] + 11.6 * (k + 0.5) / g.nb
            ders.add(label(txt, font_size=12, color=BLUE if der else (GREY_A if der is None else TUNE)).move_to([x, g.frame.get_bottom()[1] - 0.3 - 0.28 * (k % 2), 0]))
        v = b["verdict"]
        score = label(rf"score {v['score']:.2f}: \ unity {v['unity']:.2f}, \ variety {v['variety']:.2f}, \ tension fit {v['tension_fit']:.2f}, \ chord tones {v['harmony']:.2f}", font_size=18, color=GREY_A).to_edge(DOWN, buff=1.0)
        head = label(rf"the kept draft: \ number {b['draft']:,}", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        ders_ = b["derivations"][:-1]
        plain, varied, bent = sum(x == [] for x in ders_), sum(bool(x) for x in ders_), sum(x is None for x in ders_)
        bent_said = f" {say(bent)} bar{'s' if bent > 1 else ''} bent toward the cadence;" if bent else ""
        with self.voiceover(
            "And the draft it kept, the second melody of the opening question. Under each bar, how the critics traced it back "
            f"to the motive: the motive itself in {say(plain)} bars, on different degrees; varied in {say(varied)};"
            f"{bent_said} and the cadence."
        ):
            self.play(FadeIn(head), FadeIn(g), FadeIn(ders), FadeIn(score))
        with self.listen(c) as snd:
            window(snd, r"the kept draft", detail=r"Part 7's piano, \ a plucked bass", corner=DL, tag_corner=DR)
            flash(snd, g.roll.notes, [n[1] * 0.42 for n in b["melody"]], hot=WHITE, base=TUNE)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def cope(self):
        items = [
            (r"David Cope's \textit{Experiments in Musical Intelligence} \ (from 1981): \ new pieces in the style of Bach, \ Chopin, \ Mozart", WHITE),
            (r"recombinancy: \ cut a composer's works into fragments, \ reassemble them where the voice leading matches", WHITE),
            (r"`signatures': \ short patterns a composer repeats, \ kept intact", WHITE),
            (r"listeners often could not tell its chorales and mazurkas from the originals", TUNE),
            (r"its generator was the composer's own music: \ chapter 8's copying problem, \ by design", GREY_A),
        ]
        rows_scene(self, r"recombination: \ David Cope", items,
                   "Generate and test can be pushed much further. <bookmark mark='b'/> From 1981 David Cope's Experiments in "
                   "Musical Intelligence wrote new pieces in the style of Bach, Chopin and Mozart. <bookmark mark='c'/> Its "
                   "method was recombination: cut a composer's works into fragments and reassemble them where the voice leading "
                   "matches, <bookmark mark='d'/> keeping intact the short patterns Cope called signatures. "
                   "<bookmark mark='e'/> Listeners often could not tell its chorales and mazurkas from the originals. "
                   "<bookmark mark='f'/> Its generator was the composer's own music, so it raises chapter eight's copying "
                   "question by design.", marks="cdef")
