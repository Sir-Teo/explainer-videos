from __future__ import annotations

import numpy as np

from videos.music.music43.common import *  # noqa: F403

WHAT = {"as written": (r"nothing changed", "stretch"), "phrase arch": (r"slower and softer at phrase ends", "stretch"),
        "duration contrast": (r"long notes a little longer", "stretch"), "high loud": (r"higher notes louder", "vel"),
        "punctuation": (r"the last note of a phrase detached", "held"), "final ritardando": (r"the end slows to a stop", "stretch")}


class Rules(SoundScene):
    def construct(self):
        chapter(self, 2, r"Rules of expression", r"Can expression be written as rules?")
        self.kth()
        self.each()
        self.combine()
        self.strength()
        self.limits()

    # ------------------------------------------------------------------
    def kth(self):
        items = [
            (r"Johan Sundberg, \ Anders Friberg, \ Roberto Bresin and colleagues at KTH, \ Stockholm, \ from the 1980s", WHITE),
            (r"method: \ analysis by synthesis \ --- \ a rule is proposed, \ a computer plays it, \ a professional pianist judges", WHITE),
            (r"about thirty rules: \ phrase arch, \ duration contrast, \ high loud, \ punctuation, \ final ritardando, \ melodic charge ...", WHITE),
            (r"each rule has a strength k; \ a performance is the sum of chosen rules at chosen strengths", TUNE),
            (r"our module \texttt{perform.py} implements five of them, \ simplified", GREY_A),
        ]
        rows_scene(self, r"the KTH rule system", items,
                   "Can expression be written down as rules? A group at the Royal Institute of Technology in Stockholm, Johan "
                   "Sundberg, Anders Friberg, Roberto Bresin and colleagues, has tried since the 1980s. <bookmark mark='b'/> "
                   "Their method is analysis by synthesis: propose a rule, let a computer play it, and let a professional "
                   "musician judge. <bookmark mark='c'/> About thirty rules came out of it: the phrase arch, duration contrast, "
                   "high loud, punctuation, the final ritardando, melodic charge and more. <bookmark mark='d'/> Each rule has a "
                   "strength, k, and a performance is the sum of chosen rules at chosen strengths. <bookmark mark='e'/> Our "
                   "module implements five of them, simplified.", marks="bcde")

    # ------------------------------------------------------------------
    def each(self):
        d = load("rules")
        c = clip("rules.each")
        names = d["names"]
        cells = VGroup()
        for nm in names:
            what, key = WHAT[nm]
            if key == "stretch":
                vals, base, sc, col = d["stretch"][nm], 1.0, 2.0, TUNE
            elif key == "vel":
                vals, base, sc, col = d["vel"][nm], 0.6, 2.5, EAR
            else:
                vals = list(d["held"][nm])
                vals[-1] = d["stretch"][nm][-1]
                base, sc, col = 1.0, 1.2, BLUE
            bars = value_bars(vals, width=3.6, height=0.9, base=base, scale=sc, color=col, neg=BLUE if col != BLUE else EAR)
            ylab = {"stretch": r"length", "vel": r"loudness", "held": r"how long held"}[key]
            cells.add(VGroup(label(nm, font_size=19, color=TUNE if nm != "as written" else GREY_B), label(what, font_size=14, color=GREY_A), bars,
                             label(ylab, font_size=13, color=GREY_A)).arrange(DOWN, buff=0.12))
        cells.arrange_in_grid(rows=2, cols=3, buff=(0.55, 0.5)).move_to(DOWN * 0.05)
        head = label(rf"each rule alone, \ exaggerated \ (k = {d['k']})", font_size=26, color=GREY_A).to_edge(UP, buff=0.3)
        with self.voiceover(
            "Hear each rule alone, exaggerated so it is easy to catch, on the Tune's first two phrases: as written; the "
            "phrase arch, slower and softer at the ends of each phrase; duration contrast, long notes a little longer; high "
            "loud, the higher notes louder; punctuation, a breath after each phrase; and the final ritardando, slowing to a "
            "stop. Each panel shows what its rule changes, note by note."
        ):
            self.play(FadeIn(head), FadeIn(cells))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"one rule at a time", detail=r"Part 7's piano, \ a plucked bass", corner=DL, tag_corner=DR)
            for i, nm in enumerate(names):
                end = st[names[i + 1]] - 0.3 if i + 1 < len(names) else c.duration
                pulse(snd, cells[i], st[nm], end, buff=0.08)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def combine(self):
        rows_ = text_rows([
            (r"a note's length: \ written length \ $\times$ \ (1 + k $\sum_r w_r s_r$), \ $s_r$ the stretch each rule asks for", WHITE),
            (r"its velocity: \ the base velocity \ + \ k $\sum_r w_r v_r$", WHITE),
            (r"the weights $w_r$ are a performer's taste: \ one pianist arches every phrase, \ another barely slows", WHITE),
            (r"Friberg's program \textit{Director Musices} lets a user set them and hear the result", TUNE),
            (r"chapter 8 gives ten model pianists ten sets of weights", GREY_A),
        ])
        head = label(r"how rules combine", font_size=28, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "How do the rules combine? <bookmark mark='a'/> A note's length is its written length times one plus k times the "
            "weighted sum of the stretches each rule asks for. <bookmark mark='b'/> Its velocity is the base velocity plus k "
            "times the weighted sum of the rules' changes. <bookmark mark='c'/> The weights are a performer's taste: one "
            "pianist arches every phrase, another barely slows. <bookmark mark='d'/> Friberg's program Director Musices lets "
            "a user set them and hear the result. <bookmark mark='e'/> In chapter eight we give ten model pianists ten sets of "
            "weights, and try to tell them apart."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_.copy().set_opacity(0.35)))
            for mark, r in zip("abcde", rows_):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def limits(self):
        items = [
            (r"rules capture the common part of expression well: \ listeners prefer rule performances to deadpan ones", WHITE),
            (r"they miss interpretation: \ which phrase is the climax, \ which voice to bring out, \ what the piece is about", WHITE),
            (r"Widmer's machine learning found rules in about 100,000 notes played by a concert pianist \ (2002)", WHITE),
            (r"today's models learn expression from large recorded datasets \ (chapter 10)", TUNE),
            (r"chapter 3: \ the one rule with a law of physics behind it", GREY_A),
        ]
        rows_scene(self, r"what rules can and cannot do", items,
                   "How far do rules go? <bookmark mark='b'/> They capture the common part of expression well, and listeners "
                   "prefer rule performances to deadpan ones. <bookmark mark='c'/> They miss interpretation: which phrase is the "
                   "climax, which voice to bring out, what the piece is about. <bookmark mark='d'/> Gerhard Widmer's machine "
                   "learning found rules of its own in about a hundred thousand notes played by a concert pianist, in 2002, "
                   "<bookmark mark='e'/> and today's models learn expression from large recorded datasets, chapter ten's "
                   "subject. <bookmark mark='f'/> Chapter three looks at the one rule with something like a law of physics behind "
                   "it.", marks="bcdef")

    # ------------------------------------------------------------------
    def strength(self):
        d = load("strength")
        c = clip("strength.three")
        tot = max(d["lengths"].values())
        cols = {"0": GREY_B, "1": TUNE, "2": EAR}
        rolls = VGroup(*[VGroup(label(rf"k = {k}", font_size=19, color=cols[k]), perf_roll(d["perfs"][k], width=9.4, height=0.9, lo=58, hi=72, total=tot, color=cols[k], vel=k != "0")).arrange(RIGHT, buff=0.4)
                         for k in ("0", "1", "2")]).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(UP * 0.2)
        cap = label(rf"lengths: \ {d['lengths']['0']:.1f} s, \ {d['lengths']['1']:.1f} s, \ {d['lengths']['2']:.1f} s", font_size=18, color=GREY_A).to_edge(DOWN, buff=1.0)
        head = label(r"all five rules, \ at three strengths", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Hear all five rules together at three strengths: k equal to zero, which is the score as written; k equal to "
            "one, a moderate performance; and k equal to two, every effect doubled. Listeners in the KTH studies usually "
            "preferred moderate strengths: too little sounds mechanical, too much sounds mannered."
        ):
            self.play(FadeIn(head), FadeIn(rolls), FadeIn(cap))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"k = 0, \ 1, \ 2", detail=r"Part 7's piano, \ a plucked bass", corner=DL, tag_corner=DR)
            for i, k in enumerate(("0", "1", "2")):
                flash(snd, rolls[i][1].notes, [st[k] + p["t"] for p in d["perfs"][k]], hot=WHITE, base=cols[k])
                cursor(snd, rolls[i][1], st[k], 1.0, color=cols[k])
        self.wait(0.3)
        self.clear_scene()
