from __future__ import annotations

import numpy as np

from videos.music.music34.common import *  # noqa: F403


class Tihai(SoundScene):
    def construct(self):
        chapter(self, 7, r"The tihai equation", r"How do you land exactly on sam?")
        self.equation()
        self.table()
        self.quiz()
        self.larger()
        self.chakkardar()

    # ------------------------------------------------------------------
    def equation(self):
        rows_ = text_rows([
            (r"a phrase of p beats, \ played three times, \ with gaps of g beats between", WHITE),
            (r"it starts on beat s and its last stroke must fall on sam", WHITE),
            (r"counting from 0 at sam: \ (s -- 1) + 3p + 2g -- 1 \ $\equiv$ \ 0 \ (mod the cycle)", TUNE),
            (r"the hook: \ s \ = \ 5, \ p \ = \ 3, \ g \ = \ 2: \ 4 + 9 + 4 -- 1 \ = \ 16 \ $\equiv$ \ 0 in Teentaal", WHITE),
            (r"g \ = \ 0 is \textit{bedam} \ (no breath); \ g $>$ 0 is \textit{dumdar} \ (with breath)", GREY_A),
        ], font_size=24)
        head = label(r"the tihai as an equation", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "The tihai is an equation. <bookmark mark='a'/> A phrase of p beats is played three times, with a gap of g beats "
            "between the repetitions. <bookmark mark='b'/> It starts on beat s, and its last stroke must land on sam. "
            "<bookmark mark='c'/> Counting from zero at sam, the last stroke is at s minus one, plus three p, plus two g, "
            "minus one, and that must be a whole number of cycles. <bookmark mark='d'/> In the hook, s was five, p three and "
            "g two: four plus nine plus four minus one is sixteen, exactly one cycle of Teentaal. <bookmark mark='e'/> With no "
            "gap it is called bedam, without breath; with gaps, dumdar."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("bcde", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def table(self):
        d = load("tihai")
        cols = VGroup()
        for st in ("1", "3", "5", "9"):
            sols = [x for x in d["solutions"][st] if x["cycles"] == 1]
            body = VGroup(*[label(rf"p {x['p']}, \ g {x['g']}", font_size=19, color=TUNE if x["g"] == 0 else WHITE) for x in sols]) if sols else VGroup(label(r"none", font_size=19, color=GREY_A))
            body.arrange(DOWN, buff=0.2)
            cols.add(VGroup(label(rf"start on beat {st}", font_size=20, color=GREY_A), body).arrange(DOWN, buff=0.35))
        cols.arrange(RIGHT, buff=1.0, aligned_edge=UP).move_to(UP * 0.1)
        head = label(r"a tihai solver: \ phrases up to 8 beats, \ gaps up to 4, \ landing on the next sam", font_size=24, color=GREY_A).to_edge(UP, buff=0.4)
        cap = label(r"gold: \ bedam \ (no gaps). \ Drummers solve this in their heads, \ in subdivisions of the beat too", font_size=20, color=GREY_A).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "A program can list every solution. For a tihai starting on beat one, three, five or nine of Teentaal, with "
            "phrases up to eight beats and gaps up to four, here is every combination that lands on the next sam. From beat "
            "nine there is a gapless phrase of three; from beat three, a gapless five. Real tihais are usually counted in "
            "subdivisions of the beat, halves, thirds, quarters, which opens many more solutions, and drummers find them in "
            "their heads at speed."
        ):
            self.play(FadeIn(head), FadeIn(cols), FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("tihai")
        c = clip("tihai.quiz")
        card = listen_card(r"Two tihais in Teentaal, \ each after a full cycle of theka. \ One is bedam, \ its phrase repeated without gaps; \ "
                           r"the other is dumdar, \ with gaps. \ Which one breathes, \ A or B?", width=10.4)
        with self.voiceover(
            "A question for your ears. Two tihais, each after a full cycle of Teentaal. One repeats its phrase without gaps, "
            "bedam; the other leaves gaps, dumdar. Count along if you can. Which one breathes, A or B?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        t = load("tala")["talas"]["Teentaal"]
        grids = VGroup()
        for key in "AB":
            pl = d["plans"][key]
            second = t["theka"][:pl["start"] - 1] + [""] * (16 - pl["start"] + 1)
            pos = pl["start"] - 1
            for k in range(3):
                for i, b in enumerate(pl["phrase"]):
                    if pos + i < 16:
                        second[pos + i] = b
                pos += pl["p"] + pl["g"]
            g = tala_grid(second, t["vibhags"], t["marks"], cell=0.56, size=14)
            grids.add(VGroup(label(key, font_size=36, color=GREY_A), g).arrange(RIGHT, buff=0.5))
        grids.arrange(DOWN, buff=0.7).move_to(UP * 0.2)
        for gg in grids:
            gg[1].set_opacity(0.15)
        self.play(FadeOut(card), FadeIn(grids))
        with self.listen(c) as snd:
            window(snd, r"A, \ then B", detail=r"modelled tabla", corner=DL, tag_corner=DR)
            b = d["beat"]
            for gi, key in enumerate("AB"):
                for cyc in (0, 1):
                    for i in range(16):
                        t0 = d["starts"][key] + (16 * cyc + i) * b
                        pulse(snd, grids[gi][1].cells[i][0], t0, t0 + b - 0.03, buff=0.03)
        ans = VGroup(label(r"A: \ dha-ti-ta-ti-dha three times from beat 3, \ no gaps: \ bedam", font_size=19, color=GREY_A),
                     label(r"B: \ dha-ti-dha three times from beat 5, \ gaps of two beats: \ dumdar", font_size=19, color=TUNE)).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=1.0)
        with self.voiceover(
            "B breathes. It is the hook's tihai, three strokes and two beats of rest, three times. A packs a five-stroke "
            "phrase three times into fifteen beats with no rest at all. Both end exactly on sam: one equation, two "
            "solutions, two characters."
        ):
            self.play(*[gg[1].animate.set_opacity(1.0) for gg in grids], FadeIn(ans))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def larger(self):
        items = [
            (r"\textit{chakkardar}: \ a tihai of tihais, \ each part itself repeated three times", WHITE),
            (r"nine statements of a phrase, \ and still the last stroke must find sam", WHITE),
            (r"Carnatic \textit{kor\=uvai} and \textit{mor\=a}: \ similar calculations, \ often in several speeds at once", WHITE),
            (r"the audience follows the arithmetic: \ the landing is the shared reward", TUNE),
            (r"Part 33's mathematics, \ performed rather than proved", GREY_A),
        ]
        rows_scene(self, r"tihais of tihais", items,
                   "It goes further. <bookmark mark='b'/> A chakkardar is a tihai of tihais: each of its three parts is itself "
                   "a phrase repeated three times, <bookmark mark='c'/> nine statements in all, and the last stroke still has to "
                   "find sam. <bookmark mark='d'/> Carnatic music has its own forms, the korvai and the mora, often worked out "
                   "across several speeds at once. <bookmark mark='e'/> The audience follows the arithmetic, and the landing is "
                   "the shared reward. <bookmark mark='f'/> It is Part 33's mathematics, performed rather than proved.",
                   marks="cdef")

    # ------------------------------------------------------------------
    def chakkardar(self):
        d = load("chakkardar")
        rows_ = VGroup()
        hdr = VGroup(*[label(s, font_size=18, color=GREY_A) for s in (r"start", r"phrase p", r"inner gap", r"outer gap", r"cycles")]).arrange(RIGHT, buff=0.7)
        rows_.add(hdr)
        for x in d["solutions"][:9]:
            r = VGroup(*[label(str(v), font_size=19, color=WHITE) for v in (x["start"], x["p"], x["g1"], x["g2"], x["cycles"])])
            for k, cell in enumerate(r):
                cell.move_to([hdr[k].get_x(), 0, 0])
            rows_.add(r)
        rows_.arrange(DOWN, buff=0.18).move_to(LEFT * 1.8 + DOWN * 0.3)
        for r in rows_[1:]:
            for k, cell in enumerate(r):
                cell.set_x(hdr[k].get_x())
        side = VGroup(*[label(s, font_size=20, color=c_) for s, c_ in (
            (r"a chakkardar: \ three tihais in a row", WHITE),
            (r"span \ = \ 3(3p + 2g$_1$) + 2g$_2$", TUNE),
            (rf"{d['count']} solutions in Teentaal \ for small p and gaps, \ from four starting beats", WHITE),
            (r"some take two or three cycles to land", GREY_A))]).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        side.move_to(RIGHT * 4.4)
        head = label(r"chakkardars, \ solved", font_size=28, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "The chakkardar's equation has one more layer. Each of its three parts is a tihai of span three p plus two inner "
            "gaps, and the parts are separated by two outer gaps: the whole spans three times three p plus two g one, plus two "
            f"g two. Searching small phrases and gaps from four starting beats of Teentaal finds {say(d['count'])} solutions; "
            "some need two or three cycles before the last stroke finds sam. The first few are listed."
        ):
            self.play(FadeIn(head), FadeIn(rows_), FadeIn(side))
        self.wait(0.4)
        self.clear_scene()
