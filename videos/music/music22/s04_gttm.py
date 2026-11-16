from __future__ import annotations

import numpy as np

from videos.music.music22.common import *  # noqa: F403


class Gttm(SoundScene):
    def construct(self):
        chapter(self, 3, r"Grouping and metre", r"Can the rules of hearing be written down?", extra=((1983, r"Lerdahl and Jackendoff's GTTM"),))
        self.book()
        self.grouping()
        self.metre()
        self.computed()

    # ------------------------------------------------------------------
    def book(self):
        rows_ = VGroup(*[label(t, font_size=26, color=c_) for t, c_ in (
            (r"1983: \ Fred Lerdahl and Ray Jackendoff, \ a composer and a linguist", WHITE),
            (r"\textit{A Generative Theory of Tonal Music}: \ the structures an experienced listener infers", WHITE),
            (r"four of them: \ grouping, \ metre, \ time-span reduction, \ prolongational reduction", WHITE),
            (r"rules of two kinds: \ well-formedness \ (what is possible) \ and preference \ (what is likely)", TUNE),
            (r"preference rules can conflict: \ the hearing is the best compromise", GREY_A))]).arrange(DOWN, buff=0.38, aligned_edge=LEFT).move_to(DOWN * 0.1)
        head = label(r"a generative theory", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "In 1983 a composer and a linguist, Fred Lerdahl and Ray Jackendoff, set out to write the rules down. "
            "<bookmark mark='a'/> <bookmark mark='b'/> Their Generative Theory of Tonal Music describes the structures an "
            "experienced listener infers from a piece, <bookmark mark='c'/> four of them: grouping into motives and "
            "phrases, metre, and two kinds of reduction. <bookmark mark='d'/> Their rules come in two kinds: "
            "well-formedness rules say which structures are possible at all; preference rules say which are likely. "
            "<bookmark mark='e'/> Preference rules can conflict, and the hearing is the best compromise among them, an "
            "idea borrowed from the study of vision."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("bcde", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def grouping(self):
        d = load("grouping")
        notes = d["notes"]
        T = 48.0
        g = mroll(notes, width=11.4, height=1.4, lo=70, hi=84, total=T).move_to(UP * 1.2)
        s = np.array(d["strength"])
        bars = VGroup()
        for gap, v in zip(d["gaps"], s):
            x = g.frame.get_left()[0] + g.frame.width * gap / T
            h = 0.5 * v
            bars.add(Rectangle(width=0.12, height=max(h, 0.02), stroke_width=0, fill_color=EAR if gap in d["top"] else WEAK, fill_opacity=0.9).move_to([x, -0.9 + h / 2, 0]))
        base = Line([g.frame.get_left()[0], -0.9, 0], [g.frame.get_right()[0], -0.9, 0], color=DIM)
        cap = VGroup(label(r"how strongly each gap invites a boundary: \ a long note before it, \ a leap across it, \ a change of note length", font_size=20, color=GREY_A),
                     label(r"the five strongest gaps: \ exactly the Tune's five phrase ends", font_size=24, color=TUNE)).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Take grouping. Three of their preference rules: a boundary is preferred after a long note, across a leap, "
            "and where the note lengths change. <bookmark mark='a'/> Score every gap between the Tune's notes by those "
            "three rules. <bookmark mark='b'/> The five strongest gaps fall exactly on the Tune's five phrase ends, each "
            "after a long note. These selected rules match the supplied phrase boundaries of this teaching tune; listener agreement is not measured here."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(Create(base), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.03), FadeIn(cap[0]), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(cap[1]))
        c = clip("grouping.tune")
        with self.voiceover("Listen for the five places where the Tune breathes."):
            pass
        top = [b for gap, b in zip(d["gaps"], bars) if gap in d["top"]]
        with self.listen(c) as snd:
            window(snd, r"the Tune's melody", detail=r"Part 7's piano", corner=UL, tag_corner=UR)
            flash(snd, g.notes, [n[1] * d["beat"] for n in notes], hot=WHITE, base=TUNE)
            flash(snd, top, [gp * d["beat"] for gp in sorted(d["top"])], hot=WHITE, base=EAR, fade=0.6)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def metre(self):
        T = 16
        dots = VGroup()
        for t in range(T):
            lev = 1 + (t % 2 == 0) + (t % 4 == 0) + (t % 8 == 0)
            for k in range(lev):
                dots.add(Dot([-5.0 + 10.0 * t / (T - 1), -0.6 + 0.35 * k, 0], radius=0.06, color=TUNE if k == lev - 1 and lev == 4 else GREY_B))
        cap = label(r"the metrical grid: \ more dots, \ a stronger beat", font_size=22, color=GREY_A).next_to(dots, DOWN, buff=0.4)
        rows_ = VGroup(*[label(t, font_size=24, color=c_) for t, c_ in (
            (r"metre: \ levels of beats, \ in this duple-grid example, each twice as slow as the one below; other metres group beats differently \ (Part 11)", WHITE),
            (r"preference rules: \ a strong beat where notes begin, \ where they are long, \ where harmony changes", WHITE),
            (r"the reduction uses both: \ a span's head is stable \ and on a strong beat", TUNE))]).arrange(DOWN, buff=0.3, aligned_edge=LEFT).to_edge(UP, buff=0.6)
        rows_.scale_to_fit_width(min(rows_.width, 12.6))
        with self.voiceover(
            "Metre gets the same treatment. <bookmark mark='a'/> A metrical grid stacks levels of beats, each twice as "
            "slow as the one below, as in Part 11. <bookmark mark='b'/> Preference rules put strong beats where notes "
            "begin, where they are long, and where the harmony changes. <bookmark mark='c'/> And the time-span "
            "reduction of the next chapter uses grouping and metre together: the head of each span is its most stable "
            "note, preferring notes on strong beats."
        ) as vo:
            self.play(FadeIn(dots), FadeIn(cap), FadeIn(rows_[0]))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(rows_[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows_[2]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def computed(self):
        rows_ = VGroup(*[label(t, font_size=25, color=c_) for t, c_ in (
            (r"the book's rules have no weights: \ when they conflict, \ the reader decides", WHITE),
            (r"2000s: \ Hamanaka, \ Hirata and Tojo give every rule a numerical weight", WHITE),
            (r"their analysers compute grouping, \ metre and time-span trees from a score", WHITE),
            (r"tuned by hand, \ then learned from analyses made by experts", WHITE),
            (r"to compute a theory, \ every ``prefer'' must become a number", TUNE))]).arrange(DOWN, buff=0.38, aligned_edge=LEFT)
        rows_.scale_to_fit_width(min(rows_.width, 12.6))
        rows_.move_to(DOWN * 0.1)
        head = label(r"computing the theory", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "Lerdahl and Jackendoff did not say how much each rule counts. <bookmark mark='a'/> When rules conflict, "
            "the book leaves the decision to the reader's musical judgement. <bookmark mark='b'/> In the 2000s Masatoshi "
            "Hamanaka, Keiji Hirata and Satoshi Tojo developed computational subsets and numerical preference weights, <bookmark mark='c'/> and built "
            "programs that compute grouping, metre and time-span trees from a score, <bookmark mark='d'/> first with "
            "weights tuned by hand, later learned from analyses made by experts. <bookmark mark='e'/> That is the price "
            "of computing a theory: every word prefer must become a number, and the numbers are themselves claims that "
            "can be tested."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("bcde", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()
