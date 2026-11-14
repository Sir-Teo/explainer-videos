from __future__ import annotations

import numpy as np

from videos.music.music21.common import *  # noqa: F403
from videos.music.variations import rows_before


class Outro(SoundScene):
    def construct(self):
        self.variation()
        self.recap()
        self.problems()
        self.payoffs()
        self.next_part()

    # ------------------------------------------------------------------
    def variation(self):
        d = load("sonata")
        v = load("variation")
        c = clip("sonata.whole")
        head = VGroup(label(r"Variation 21", font_size=48, color=TUNE), label(r"the Tune as a miniature sonata", font_size=30, color=GREY_A)).arrange(RIGHT, buff=0.5, aligned_edge=DOWN).to_edge(UP, buff=0.3)
        total = d["total"]
        big = d["big"]
        st = strip([big[k][0] for k in big], list(big), total, width=11.4, height=0.5, colors={"exposition": "#F5C542", "development": "#7DD3FC", "recapitulation": "#A3E635"}, font_size=22).move_to(UP * 1.5)
        names = d["names"]
        short = {"first theme": "1st", "second theme": "2nd", "transition": "tr", "closing": "cl", "retransition": "retr"}
        lab = [short.get(n, n.replace("development: ", "")) for n in names]
        cols = {n: c_ for n, c_ in zip(lab, ["#F5C542"] * len(lab))}
        sec = strip(d["starts"], lab, total, width=11.4, height=0.4, colors={**{k: GREY_B for k in lab}, "1st": "#F5C542", "2nd": "#F472B6"}, font_size=16).next_to(st, DOWN, buff=0.15)
        events = d["events"]
        mel = [e for e in events if e[0] >= 67]
        g = roll([e[0] for e in mel], [e[2] for e in mel], width=11.4, height=1.8, color=TUNE, lo=64, hi=86, lines=())
        g.move_to(DOWN * 1.2)
        with self.voiceover(
            "Every part ends by doing something to the Tune with what it has built. This part built forms. "
            "<bookmark mark='a'/> So the Tune becomes a miniature sonata: its opening as the first theme in C; a "
            "transition to G; a second theme that is the opening turned upside down; a development that carries the "
            "Tune's first notes through three keys; and a recapitulation that brings both themes home. Listen for the "
            "second theme coming back in C."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(st), FadeIn(sec), FadeIn(g))
        cur = Line(ORIGIN, ORIGIN, color=WHITE, stroke_width=3)
        with self.listen(c) as snd:
            window(snd, r"Variation 21", detail=r"Part 7's piano", corner=DL, tag_corner=DR)

            def upd(m, t):
                b = min(max(t / d["beat"], 0.0), total)
                x = st.get_left()[0] + st.width * b / total
                m.put_start_and_end_on([x, st.get_top()[1] + 0.15, 0], [x, g.get_bottom()[1] - 0.1, 0])

            snd.drive(cur, upd)
            self.add(cur)
            on = [e[1] for e in mel]
            starts_ = []
            seen = set()
            for k, e in enumerate(mel):
                starts_.append(e[1] * d["beat"])
            flash(snd, g.notes, starts_, hot=WHITE, base=TUNE)
            for k in range(len(d["starts"])):
                a = d["starts"][k] * d["beat"]
                b = (d["starts"][k + 1] if k + 1 < len(d["starts"]) else total) * d["beat"]
                pulse(snd, sec[k], a, b - 0.05, buff=0.04)
        self.play(FadeOut(st), FadeOut(sec), FadeOut(g), FadeOut(cur))
        rws = (rows_before(PART) + [{"part": v["part"], "title": v["title"], "seconds": v["seconds"], "measure": v["measure"]}])[-6:]
        led = variations_ledger(rws, highlight=(len(rws) - 1,)).to_edge(DOWN, buff=0.25)
        sc = d["score"]
        with self.voiceover(
            f"Row twenty-one of the ledger. {say(v['seconds'])} seconds. The measurement: the program of chapter eight, "
            f"listening to the sound alone, found {say(sc['hits'])} of its {say(len(d['truth']))} section boundaries within "
            "two beats."
        ):
            self.play(FadeIn(led, shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def recap(self):
        r = load("repetition")
        g = load("golden")
        s = load("sonata")
        card = objectives_card([
            r"repetition turns speech into song; \ form is the plan of what returns",
            r"period: \ question and answer; \ sentence: \ idea, \ idea, \ acceleration",
            r"binary, \ ternary, \ rondo, \ variation, \ sonata, \ song: \ return or transformation",
            r"the self-similarity matrix: \ stripes are repeats, \ blocks are sections; \ novelty finds the seams",
            rf"the Tune's sonata: \ {s['score']['hits']} of {len(s['truth'])} boundaries found from sound; \ variations hardly at all",
            rf"tunes repeat {100 * r['mean']:.0f} notes in 100 \ (shuffled {100 * r['mean_shuffled']:.0f}); \ golden sections by chance: \ 1 in {1 / g['base_rate']:.0f}",
        ], title=r"What we found", font_size=23).move_to(DOWN * 0.1)
        with self.voiceover(
            "What did we find? Repetition turns speech into song, and form is the plan of what returns. "
            "<bookmark mark='a'/> The period works by question and answer, the sentence by an idea repeated and then "
            "broken up. <bookmark mark='b'/> The large forms bring material back, or transform it. "
            "<bookmark mark='c'/> A self-similarity matrix shows repeats as stripes and sections as blocks, and its "
            "novelty curve finds the seams. <bookmark mark='d'/> From sound alone a program found most of the sonata's "
            "sections, but hardly any variation's. <bookmark mark='e'/> Tunes repeat a third of their notes against one in "
            "a hundred by chance, and golden sections turn up by chance one time in six."
        ) as vo:
            self.play(FadeIn(card.head), FadeIn(card.rows[0]))
            for mark, rr in zip("abcde", card.rows[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(rr), run_time=0.5)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def problems(self):
        ps = problem_set([
            r"Label the phrases of \textit{Ode to Joy} \ (Part 14's version) \ and say whether its first eight bars are a period or a sentence.",
            r"Show that a self-similarity matrix is symmetric with ones on its diagonal, \ and that a passage repeated after $d$ beats "
            r"makes a stripe on the $d$-th diagonal.",
            r"\textbf{Ear.} \ The lab plays six short forms on the Tune. \ For each, \ name the plan: \ AABB, \ ABA, \ ABACA, \ AABA, \ or variations.",
            r"\textbf{Build.} \ Add a stripe detector to the segmenter, \ so that it finds the seam between a passage and its own repeat, \ "
            r"and score it on this part's pieces.",
            r"$\bigstar$ \ Design an experiment that measures listeners' memory for themes and for keys separately, \ over minutes.",
        ], font_size=23)
        with self.voiceover(
            "Five problems. One to compute, one to prove, one for your ears, one to build, and a research problem, "
            "marked with a star. Solutions are in this part's notes. Pause here."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r) for r in ps.rows], lag_ratio=0.25), run_time=3.0)
        self.wait(5.0)
        self.clear_scene()

    # ------------------------------------------------------------------
    def payoffs(self):
        pay = payoff_card([
            (r"analysis: \ form as a grammar and as a tree", [22]),
            (r"the classical style: \ the sonata at work", [26]),
            (r"the Romantic century: \ forms stretched", [27]),
            (r"the song: \ verse, \ chorus, \ the loop", [40]),
            (r"composing: \ planning ten minutes", [42]),
            (r"beat, \ chords and structure, \ by machine", [62]),
        ], font_size=26)
        with self.voiceover(
            "Where does this come back? In analysis, which asks whether form is a grammar. In the classical style, where "
            "the sonata is at home, and the Romantic century, which stretched it. In the song, in composing a long piece, "
            "and in Part 62, where the segmenter of this part grows up into a structure analyser."
        ):
            self.play(FadeIn(pay.head), LaggedStart(*[FadeIn(r) for r in pay.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        prac = practice_card([
            (r"listeners", r"draw a piece's plan in letters as you hear it, \ then check the score"),
            (r"performers", r"shape the returns: \ the second A is not the first"),
            (r"songwriters", r"decide what comes back, \ and when the listener wants it"),
            (r"producers and DJs", r"structure analysis finds the sections for a remix or a loop"),
        ], font_size=26)
        with self.voiceover(
            "And in practice. Listeners can draw a piece's plan in letters as they hear it. Performers shape the returns, "
            "since the second A is not the first. Songwriters decide what comes back, and when the listener will want "
            "it. And producers use structure analysis to find the sections of a track."
        ):
            self.play(FadeIn(prac.head), LaggedStart(*[FadeIn(r) for r in prac.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        refs = reference_card(
            [r"W. E. Caplin, \ \textit{Classical Form} \ (1998)",
             r"J. Hepokoski and W. Darcy, \ \textit{Elements of Sonata Theory} \ (2006)",
             r"E. H. Margulis, \ \textit{On Repeat} \ (2014)",
             r"C. Rosen, \ \textit{Sonata Forms} \ (1980)"],
            [r"D. Deutsch, \ T. Henthorn and R. Lapidis, \ ``Illusory transformation from speech to song'', \ \textit{JASA} 129 (2011)",
             r"J. Foote, \ ``Automatic audio segmentation using a measure of audio novelty'', \ ICME \ (2000)",
             r"N. Cook, \ ``The perception of large-scale tonal closure'', \ \textit{Music Perception} 5 (1987)",
             r"M. Karno and V. J. Konečni, \ ``The effects of structural interventions in the first movement of Mozart's Symphony in G minor'', \ \textit{Music Perception} 10 (1992)",
             r"J. Putz, \ ``The golden section and the piano sonatas of Mozart'', \ \textit{Mathematics Magazine} 68 (1995)",
             r"J. B. L. Smith and others, \ ``Design and creation of a large-scale database of structural annotations'', \ ISMIR \ (2011)"],
            font_size=18)
        with self.voiceover("The books and papers this part follows. The full list, with notes, is in the README."):
            self.play(FadeIn(refs))
        self.wait(1.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_part(self):
        q = label(r"is there a grammar of music, \ as there is of language?", font_size=30, color=EAR).move_to(UP * 0.4)
        top = label(r"forms: \ plans of sections", font_size=30, color=GREY_A).to_edge(UP, buff=0.8)
        nxt = VGroup(label(r"Part 22", font_size=32, color=GREY_B), label(r"Analysis", font_size=50, color=TUNE)).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "This part treated form as a plan of sections, laid out in time. <bookmark mark='a'/> But analysts since "
            "Heinrich Schenker have heard pieces as trees, every note an elaboration of a simpler one, and linguists have "
            "asked whether that is a grammar. Is there a grammar of music, as there is of language? "
            "<bookmark mark='b'/> Next time. Part 22: Analysis."
        ) as vo:
            self.play(FadeIn(top))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.0)
        self.clear_scene()
