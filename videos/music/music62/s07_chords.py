from __future__ import annotations

import numpy as np

from videos.music.music62.common import *  # noqa: F403


class Chords(SoundScene):
    def construct(self):
        chapter(self, 6, r"Recognizing chords", r"How does knowing what usually comes next help?")
        self.hmm()
        self.compare()
        self.confusions()
        self.prior()

    # ------------------------------------------------------------------
    def hmm(self):
        lines = VGroup(
            label(r"a hidden Markov model: \ the chord is hidden, \ the chroma observed", font_size=21, color=WHITE),
            MathTex(r"P(c_{1:T} \mid x_{1:T}) \;\propto\; \pi(c_1)\prod_t A(c_{t-1}, c_t)\prod_t e^{\beta \cos(\mathbf{t}_{c_t}, \mathbf{x}_t)}", font_size=32, color=TUNE),
            label(r"$A$: \ how chords follow chords; \ mostly they stay put, \ frame to frame", font_size=19, color=WHITE),
            label(r"the Viterbi algorithm finds the most likely sequence, \ by dynamic programming again", font_size=19, color=WHITE),
            label(r"two priors: \ `stay or move anywhere', \ and Part 18's chorale statistics \ (I to IV, \ IV to V, \ V to I, \dots)", font_size=19, color=GREY_A),
        ).arrange(DOWN, buff=0.38)
        head = label(r"chords in context", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Listeners hear chords in context, and so can a machine. <bookmark mark='a'/> In a hidden Markov model the chord "
            "is hidden and the chroma observed. <bookmark mark='b'/> The probability of a chord sequence multiplies how well each "
            "chord's template fits its frame by how likely each chord is to follow the last. <bookmark mark='c'/> Mostly, frame "
            "to frame, a chord stays put. <bookmark mark='d'/> The Viterbi algorithm finds the most likely sequence by dynamic "
            "programming, as the beat tracker did. <bookmark mark='e'/> Monochord tries two priors: stay or move anywhere, and "
            "the transitions Part 18 counted in Bach's chorales, I to IV, IV to V, V to I."
        ) as vo:
            self.play(FadeIn(head))
            for mark, ln in zip("abcde", lines):
                vo.wait_until(mark)
                self.play(FadeIn(ln))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def compare(self):
        d = load("chords")
        labels = d["labels"]
        truth = np.array(d["truth"])
        n = len(truth)
        hop = d["hop_s"]
        w = 11.0
        rows = [("played", truth, GREY_B), ("frame by frame", np.array(d["frame"])[:n], EAR), ("HMM, \\ stay or move", np.array(d["hmm"])[:n], BLUE),
                ("HMM, \\ Bach's prior", np.array(d["bach"])[:n], TUNE)]
        g = VGroup()
        for i, (name, seq, col) in enumerate(rows):
            y = 1.6 - 1.05 * i
            segs = VGroup()
            k = 0
            while k < n:
                j = k
                while j < n and seq[j] == seq[k]:
                    j += 1
                ok = col == GREY_B or np.mean(seq[k:j] == truth[k:j]) > 0.5
                r = Rectangle(width=w * (j - k) / n, height=0.55, stroke_color=BLACK, stroke_width=1, fill_color=col if ok else RED, fill_opacity=0.55)
                r.move_to([-w / 2 + w * (k + j) / 2 / n + 0.6, y, 0])
                t = label(labels[seq[k]], font_size=12, color=WHITE).move_to(r) if (j - k) / n * w > 0.35 else VGroup()
                segs.add(VGroup(r, t))
                k = j
            g.add(VGroup(label(name, font_size=15, color=col).move_to([-w / 2 - 0.4, y, 0]), segs))
        acc = d["acc"]
        note = label(rf"frames right: \ {100 * acc['frame']:.0f}\%, \ {100 * acc['hmm']:.0f}\%, \ {100 * acc['bach']:.0f}\% \ (red: \ wrong)", font_size=17, color=WHITE).to_edge(DOWN, buff=0.35)
        head = label(r"the session's Tune, \ four phrases", font_size=26, color=GREY_A).to_edge(UP, buff=0.3)
        with self.voiceover(
            "Here are the three recognizers on four phrases of the session, against the chords played. <bookmark mark='a'/> "
            f"Frame by frame, the templates flicker, fooled by the melody and the attacks: {say(100 * acc['frame'])} percent of "
            f"frames right. <bookmark mark='b'/> An HMM that only knows chords tend to stay put smooths the flicker: "
            f"{say(100 * acc['hmm'])} percent. <bookmark mark='c'/> With Bach's transitions as the prior, the recognizer prefers "
            f"the progressions music actually uses, and gets {say(100 * acc['bach'])} percent. Knowing what usually comes next is "
            "worth as much as listening harder."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g[0]))
            vo.wait_until("a")
            self.play(FadeIn(g[1]))
            vo.wait_until("b")
            self.play(FadeIn(g[2]))
            vo.wait_until("c")
            self.play(FadeIn(g[3]), FadeIn(note))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def confusions(self):
        d = load("chords")
        conf = d["confusions"]
        top = max(v for _, v in conf)
        g = VGroup()
        for k, v in conf:
            a, b_ = k.split(">")
            b_ = r"no chord" if b_ == "N" else b_
            row = VGroup(label(rf"{a} \ heard as \ {b_}", font_size=19, color=WHITE),
                         Rectangle(width=4.0 * v / top, height=0.32, stroke_width=0, fill_color=EAR, fill_opacity=0.8),
                         label(f"{v}", font_size=16, color=GREY_A)).arrange(RIGHT, buff=0.3)
            g.add(row)
        g.arrange(DOWN, buff=0.28, aligned_edge=LEFT).move_to(LEFT * 1.6 + DOWN * 0.2)
        side = VGroup(label(r"C as G; \ G as D: \ a fifth up", font_size=18, color=TUNE),
                      label(r"every note's third partial is its fifth, \ an octave up, \ so chroma leans each chord toward the chord a fifth above", font_size=16, color=GREY_A),
                      label(r"and `no chord' where attacks and sung notes blur the frame", font_size=16, color=GREY_A)).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(RIGHT * 4.0 + DOWN * 0.2)
        for s_ in side:
            s_.set_width(min(s_.width, 4.2))
        head = label(r"what the frame-by-frame matcher confuses", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Which mistakes does the frame-by-frame matcher make? <bookmark mark='a'/> Most often, C heard as G, and G heard as D: "
            "each chord mistaken for the chord a fifth above. <bookmark mark='b'/> Physics explains it. Every note's third partial "
            "is its fifth, an octave up, so the chroma of a C chord carries extra G, and leans toward G major. "
            "<bookmark mark='c'/> The rest are frames called no chord, where an attack or a loud sung note blurs everything. "
            "Context, in the HMM, repairs both kinds."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in g], lag_ratio=0.2), FadeIn(side[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def prior(self):
        items = [
            (r"a prior helps where the evidence is weak, \ and misleads where the music breaks its habits", WHITE),
            (r"Bach's transitions suit the Tune; \ they would fight a blues, \ a modal folk song, \ a jazz standard", WHITE),
            (r"modern recognizers learn both parts from data: \ networks for the evidence, \ sequence models for the prior", WHITE),
            (r"and a larger vocabulary: \ sevenths, \ inversions, \ suspensions; \ the ceiling is set by annotators who disagree", WHITE),
            (r"Part 18's statistics, \ built to describe music, \ turn out to be what a listener \ (or a machine) \ uses to hear it", TUNE),
        ]
        rows_scene(self, r"what a prior does", items,
                   "A prior is a bet. <bookmark mark='b'/> It helps where the evidence is weak, and misleads where the music breaks "
                   "its habits. <bookmark mark='c'/> Bach's transitions suit the Tune; they would fight a blues, a modal folk song "
                   "or a jazz standard. <bookmark mark='d'/> Modern recognizers learn both parts from data: networks for the "
                   "evidence, sequence models for the prior. <bookmark mark='e'/> And they use a larger vocabulary, sevenths, "
                   "inversions and suspensions, where annotators themselves start to disagree. <bookmark mark='f'/> Part 18's "
                   "statistics, built to describe music, turn out to be what a listener, or a machine, uses to hear it.",
                   marks="bcdef")
