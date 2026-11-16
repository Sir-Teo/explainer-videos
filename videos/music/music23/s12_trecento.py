from __future__ import annotations

import numpy as np

from videos.music.music23.common import *  # noqa: F403


class Trecento(SoundScene):
    def construct(self):
        chapter(self, 11, r"A century, counted", r"What do eighty-nine pieces say about the style?", extra=((1390, r"Landini and Ciconia"),))
        self.corpus()
        self.beats()
        self.parallels()
        self.landini()

    # ------------------------------------------------------------------
    def corpus(self):
        d = load("census")
        comp = sorted(d["composers"].items(), key=lambda x: -x[1])
        named = [(k, v) for k, v in comp if k != "anonymous"][:6]
        rows_ = VGroup(*[label(rf"{k}: \ {v}", font_size=21, color=TUNE if k in ("Johannes Ciconia", "Francesco Landini", "Philippe de Vitry") else WHITE) for k, v in named]
                       + [label(rf"anonymous: \ {d['composers'].get('anonymous', 0)}", font_size=21, color=GREY_A)]).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        rows_.move_to(LEFT * 3.4 + DOWN * 0.2)
        g = d["genres"]
        kinds = VGroup(*[label(t, font_size=21, color=c_) for t, c_ in (
            (rf"Mass movements: \ {g.get('gloria', 0)} Glorias, \ {g.get('credo', 0)} Credos, \ {g.get('kyrie', 0)} Kyries", WHITE),
            (rf"motets, \ madrigals, \ ballate and others: \ {g.get('other', 0) + g.get('madrigal', 0) + g.get('sanctus', 0)}", WHITE),
            (rf"two voices: \ {d['voices'].get('2', 0)}; \ three: \ {d['voices'].get('3', 0)}; \ four or five: \ {d['voices'].get('4', 0) + d['voices'].get('5', 0)}", WHITE),
            (r"pitches and lengths from the modern edition, \ editors' accidentals included", GREY_A))]).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        kinds.scale_to_fit_width(min(kinds.width, 6.4))
        kinds.move_to(RIGHT * 3.0 + DOWN * 0.2)
        head = label(rf"the corpus: \ {d['pieces']} pieces, \ about 1320 to 1410", font_size=28, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            f"Part 17 counted Bach's chorales. This chapter counts the fourteenth century: {say(d['pieces'])} pieces "
            "encoded by students of the musicologist Michael Scott Cuthbert from the edition Polyphonic Music of the "
            "Fourteenth Century, and kept in the music21 library's corpus. <bookmark mark='a'/> The named composers "
            "are mostly Italian: Johannes Ciconia, a singer from Liège who worked in Padua around 1400; Giovanni da "
            "Cascia and Jacopo da Bologna from the middle of the century; Francesco Landini, the blind organist of "
            "Florence; and four motets by de Vitry. <bookmark mark='b'/> Most of the pieces are Mass movements, and most "
            "are for three voices. It is not a random sample of the century, and nothing in it is by Machaut, but it is "
            "large enough to count."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r) for r in rows_], lag_ratio=0.15), run_time=1.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in kinds], lag_ratio=0.2), run_time=1.5)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def beats(self):
        d = load("census")
        on, off = d["on"], d["off"]
        keys = ("perfect", "imperfect", "dissonant")
        cols = {"perfect": TUNE, "imperfect": BLUE, "dissonant": RED}
        bars = VGroup()
        for j, (name, src) in enumerate(((r"at the start of a bar", on), (r"everywhere else", off))):
            stack = VGroup()
            y = 0.0
            for k in keys:
                h = 3.2 * src[k]
                r = Rectangle(width=1.6, height=max(h, 0.01), stroke_width=0, fill_color=cols[k], fill_opacity=0.9)
                r.move_to([0, y + h / 2, 0])
                t = label(rf"{100 * src[k]:.0f}", font_size=20, color=BLACK if k != "dissonant" else WHITE).move_to(r)
                stack.add(VGroup(r, t))
                y += h
            stack.add(label(name, font_size=20, color=GREY_A).next_to(stack, DOWN, buff=0.25))
            stack.move_to([-3.6 + 3.0 * j, -0.3, 0])
            bars.add(stack)
        key = VGroup(*[VGroup(Square(side_length=0.22, stroke_width=0, fill_color=cols[k], fill_opacity=0.9), label(t, font_size=19, color=GREY_A)).arrange(RIGHT, buff=0.15)
                       for k, t in zip(keys, (r"unison, \ fifth, \ octave", r"third, \ sixth", r"second, \ fourth, \ seventh, \ tritone"))]).arrange(DOWN, buff=0.25, aligned_edge=LEFT).move_to(RIGHT * 3.8 + UP * 0.6)
        cap = label(r"intervals above the lowest voice, \ in 100s", font_size=19, color=GREY_B).to_edge(UP, buff=0.5)
        with self.voiceover(
            "First, the rule of Notre Dame: perfect consonances on the strong beats. Measure every interval above the "
            "lowest sounding voice, separately at the start of each bar of the edition and everywhere else. "
            f"<bookmark mark='a'/> At the start of a bar, {say(round(100 * on['perfect']))} in a hundred are unisons, "
            f"fifths or octaves, {say(round(100 * on['imperfect']))} are thirds or sixths, and only {say(round(100 * on['dissonant']))} "
            f"are dissonant. <bookmark mark='b'/> Between, the perfect intervals fall to {say(round(100 * off['perfect']))}, "
            f"thirds and sixths become the majority, and dissonance rises to {say(round(100 * off['dissonant']))}. "
            "A century after Pérotin, the beat still belongs to the perfect intervals, while thirds and sixths, "
            "officially imperfect, do most of the work in between."
        ) as vo:
            self.play(FadeIn(cap), FadeIn(key), FadeIn(bars[0]))
            vo.wait_until("a")
            self.play(Indicate(bars[0], color=WHITE, scale_factor=1.03))
            vo.wait_until("b")
            self.play(FadeIn(bars[1]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def parallels(self):
        d = load("census")
        pt, pb = d["parallels"]["trecento"], d["parallels"]["bach"]
        rt, rb = 100 * pt["parallels"] / pt["moves"], 100 * pb["parallels"] / pb["moves"]
        f, bf = d["finals"], d["bach_finals"]
        rows_ = text_rows([
            (rf"parallel fifths and octaves: \ {pt['parallels']:,} in {pt['moves']:,} moves \ ({rt:.1f} in 100)".replace(",", "{,}"), WHITE),
            (rf"in Bach's chorales, \ counted the same way: \ {pb['parallels']} in {pb['moves']:,} \ ({rb:.2f} in 100)".replace(",", "{,}"), WHITE),
            (rf"about {rt / rb:.0f} times as common: \ under this detector; \ encoding and sampling also matter", TUNE),
            (rf"last chords: \ {f.get('open', 0)} of {d['pieces']} bare fifths and octaves; \ Bach: \ all {bf.get('third', 0)} with a third", WHITE),
            (r"the third, \ imperfect in theory, \ was often avoided in final sonorities of this selected repertory", GREY_A),
        ])
        head = label(r"two rules, \ before they were rules", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "Two more counts, against Part 17's chorales. <bookmark mark='a'/> Parallel fifths and octaves: in this "
            f"corpus, {say(pt['parallels'])} among {say(pt['moves'])} moves of pairs of voices, about {rt:.0f} in a hundred. "
            f"<bookmark mark='b'/> Counted the same way, Bach's chorales have {say(pb['parallels'])}. <bookmark mark='c'/> "
            f"The fourteenth century writes them about {say(round(rt / rb))} times as often. Theorists already "
            "discouraged them; these counts also depend on editorial encoding, sampling and the simplified detector; no historical rule was literally exceptionless. <bookmark mark='d'/> And the last chord: "
            f"{say(f.get('open', 0))} of the {say(d['pieces'])} pieces end on bare fifths and octaves, while every one of "
            f"Bach's {say(bf.get('third', 0))} chorales ends with a third. <bookmark mark='e'/> In the fourteenth century the "
            "third was an imperfect consonance, fine in passing and often avoided in final sonorities of this selected repertory. Part 16's rules are not "
            "timeless laws of hearing; they changed, and here is the century they were changing in."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("bcde", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def landini(self):
        d = load("landini")
        c = clip("landini.cadence")
        vs = d["voices"]
        g = voices_roll(vs, width=7.0, height=2.6, colors=[TUNE, BLUE, GREY_A, GREY_B], bar_h=0.12).move_to(LEFT * 2.6 + UP * 0.3)
        title = label(rf"Landini, \ \textit{{{d['title'].split('.')[-1].strip()}}}: \ a cadence", font_size=21, color=GREY_A).next_to(g, UP, buff=0.3)
        by = d["by_composer"]
        tab = VGroup()
        for name in ("Francesco Landini", "Johannes Ciconia", "Giovanni da Cascia", "Jacopo da Bologna"):
            n, p = by.get(name, [0, 0])
            tab.add(label(rf"{name}: \ {n} in {p} pieces", font_size=20, color=TUNE if name in ("Francesco Landini", "Johannes Ciconia") else WHITE))
        tab.arrange(DOWN, buff=0.25, aligned_edge=LEFT).move_to(RIGHT * 3.6 + UP * 0.3)
        cap = VGroup(label(r"the top voice: \ the leading tone, \ a step down, \ then up a third to the final", font_size=21, color=WHITE),
                     label(r"named after Landini by later historians; \ Ciconia writes it as often", font_size=21, color=EAR)).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "One cadence carries a composer's name. In the so-called Landini cadence, the top voice reaches the leading "
            "tone, drops a step, and then leaps up a third to the final, decorating the double leading tone. Here is one "
            "in a ballata by Landini himself, sung from the edition."
        ):
            self.play(FadeIn(title), FadeIn(g), FadeIn(cap[0]))
        with self.listen(c) as snd:
            window(snd, r"a Landini cadence", detail=r"from the edition, \ synthetic voices", kind="synthesized", corner=UR, tag_corner=UL)
            flash_voices(snd, g, vs, 0.0, d["quarter"], colors=[TUNE, BLUE, GREY_A, GREY_B])
            cursor(snd, g, 0.0, d["quarter"])
        ln, lp = by.get("Francesco Landini", [0, 1])
        cn, cp = by.get("Johannes Ciconia", [0, 1])
        with self.voiceover(
            f"A program counts the figure: {say(d['total'])} times in the corpus. <bookmark mark='a'/> Landini's four "
            f"pieces have {say(ln)}, about {ln / lp:.1f} a piece; but Ciconia's eighteen have {say(cn)}, about {cn / cp:.1f} a "
            "piece, just as many; and the earlier Italians, Jacopo and Giovanni, hardly use it. <bookmark mark='b'/> The "
            "name was given by later historians. The figure belongs not to one composer but to the later decades of "
            "the century, and this small, uneven sample supports that association but cannot establish a universal chronology."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tab))
            vo.wait_until("b")
            self.play(FadeIn(cap[1]))
        self.wait(0.4)
        self.clear_scene()
