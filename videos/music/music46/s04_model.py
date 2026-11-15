from __future__ import annotations

import numpy as np

from videos.music.music46.common import *  # noqa: F403


class Model(SoundScene):
    def construct(self):
        chapter(self, 3, r"A listener model", r"Can a program be surprised?")
        self.how()
        self.measures()
        self.viewpoints()
        self.tune()
        self.sing()
        self.corpus()

    # ------------------------------------------------------------------
    def how(self):
        rows_ = text_rows([
            (r"count, \ in the corpus, \ which note followed each context of 0, \ 1, \ 2, \ 3 and 4 notes", WHITE),
            (r"to predict, \ use the longest context seen before; \ keep some probability back for the unseen, \ and pass it to shorter contexts", WHITE),
            (r"this is prediction by partial matching, \ the method of Marcus Pearce's IDyOM \ (2005)", TUNE),
            (r"a long-term model knows the style; \ a short-term model learns the piece as it goes; \ the more certain counts for more", WHITE),
            (r"our corpus: \ the series' 51 major-key tunes \ (Part 14), \ each heard by a model trained on the others", GREY_A),
        ])
        head = label(r"how the listener works", font_size=28, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "Our listener learns the way an infant does, by counting. <bookmark mark='a'/> In the corpus, it counts which note "
            "followed every context of up to four notes. <bookmark mark='b'/> To predict, it uses the longest context it has "
            "seen before, keeps some probability back for the unseen, and passes that down to shorter contexts. "
            "<bookmark mark='c'/> This is prediction by partial matching, the method behind Marcus Pearce's model IDyOM. "
            "<bookmark mark='d'/> A long-term model knows the style; a short-term model learns the piece as it goes; the "
            "more certain of the two counts for more. <bookmark mark='e'/> Our corpus is the series' fifty-one major-key "
            "tunes from Part 14, and each tune is heard by a model trained on all the others."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_.copy().set_opacity(0.15)))
            for mark, r in zip("abcde", rows_):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def measures(self):
        items = [
            (r"surprise \ (information content): \ $-\log_2 p$ \ of the note that came, \ in bits", WHITE),
            (r"a certain note costs 0 bits; \ a one-in-two note 1 bit; \ a one-in-a-thousand note about 10", WHITE),
            (r"uncertainty \ (entropy): \ the expected surprise before the note, \ $-\sum p \log_2 p$", WHITE),
            (r"surprise is about what happened; \ uncertainty about what might", TUNE),
            (r"Pearce and colleagues found information content predicts listeners' ratings of expectedness", GREY_A),
        ]
        rows_scene(self, r"two numbers per note", items,
                   "It gives two numbers for every note. <bookmark mark='b'/> Surprise, or information content: minus the "
                   "logarithm, base two, of the probability the model gave the note that came, in bits. <bookmark mark='c'/> A "
                   "certain note costs nothing; a one-in-two note one bit; a one-in-a-thousand note about ten. "
                   "<bookmark mark='d'/> Uncertainty, or entropy: the surprise the model expects before the note arrives. "
                   "<bookmark mark='e'/> Surprise is about what happened; uncertainty about what might. <bookmark mark='f'/> "
                   "Pearce and colleagues found information content predicts listeners' ratings of how expected each note was.",
                   marks="bcdef")

    # ------------------------------------------------------------------
    def tune(self):
        d = load("tune")
        c = clip("tune.plain")
        ic, h = d["ic"], d["entropy"]
        top = 6.0
        a = bits_plot(ic, width=11.6, height=1.5, top=top, color=EAR, y0=0.5)
        b = bits_plot(h, width=11.6, height=1.5, top=top, color=BLUE, y0=-1.6)
        labs = VGroup(label(rf"surprise \ (mean {d['mean_ic']:.2f} bits)", font_size=17, color=EAR).move_to([-4.4, 2.3, 0]),
                      label(rf"uncertainty \ (mean {d['mean_entropy']:.2f} bits)", font_size=17, color=BLUE).move_to([-4.4, 0.2, 0]))
        head = label(r"the Tune, \ note by note", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        cap = label(r"one bar per note, \ 42 notes; \ scale up to 6 bits", font_size=16, color=GREY_A).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "Here is the Tune through the listener's ears: surprise above, uncertainty below, one bar per note, while the "
            "Tune plays. Watch where the bars rise."
        ):
            self.play(FadeIn(head), FadeIn(a), FadeIn(b), FadeIn(labs), FadeIn(cap))
        on = d["onsets"]
        with self.listen(c) as snd:
            window(snd, r"the Tune", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            flash(snd, list(a[1:]), on, hot=WHITE, base=EAR)
            flash(snd, list(b[1:]), on, hot=WHITE, base=BLUE)
        big = int(np.argmax(ic[:14]))
        with self.voiceover(
            f"The biggest surprise of the first phrase is the leap up to G, {say(ic[2], 1)} bits. Over the piece, surprise "
            f"falls, from about {say(float(np.mean(ic[0:7])), 1)} bits a note in the first phrase to "
            f"{say(float(np.mean(ic[35:42])), 1)} in the last: the short-term model has learned the piece, so the returning "
            "phrases cost little. The Tune averages "
            f"{say(d['mean_ic'], 2)} bits a note: very predictable, which is part of why children learn it."
        ):
            self.play(Indicate(a[3]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def corpus(self):
        d = load("corpus")
        e, s = np.array(d["entropy"]), np.array(d["ic"])
        x0, y0, W, H = -5.4, -2.4, 7.0, 4.4
        def P_(a, b):
            return [x0 + W * a / 5.0, y0 + H * min(b, 10) / 10.0, 0]
        ax = VGroup(Line(P_(0, 0), P_(5, 0), color=GREY_B), Line(P_(0, 0), P_(0, 10), color=GREY_B))
        dots = VGroup(*[Dot(P_(a, b), radius=0.025, color=BLUE, fill_opacity=0.5) for a, b in zip(e[::2], s[::2])])
        labs = VGroup(label(r"uncertainty before the note \ (bits)", font_size=15, color=GREY_A).move_to([x0 + W / 2, y0 - 0.4, 0]),
                      label(r"surprise \ (bits)", font_size=15, color=GREY_A).move_to([x0 + 0.5, y0 + H + 0.25, 0]))
        side = VGroup(label(rf"{d['notes']:,} notes of {d['tunes']} tunes", font_size=19, color=WHITE),
                      label(rf"mean surprise {d['mean_ic']:.2f} bits; \ mean uncertainty {d['mean_entropy']:.2f}", font_size=17, color=WHITE),
                      label(rf"correlation {d['corr']:.2f}: \ uncertain moments allow bigger surprises, \ but most notes are cheap", font_size=17, color=TUNE)).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to(RIGHT * 4.3)
        side.scale_to_fit_width(min(side.width, 4.8)).move_to(RIGHT * 4.3)
        head = label(r"the whole corpus", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            f"Now every note of all {say(d['tunes'])} tunes, each tune heard by a model trained on the rest. "
            "<bookmark mark='a'/> Across, the uncertainty before the note; up, the surprise when it came. Most notes sit low: "
            f"folk tunes average {say(d['mean_ic'], 2)} bits. Where the model is uncertain, bigger surprises are possible, "
            f"but the correlation is only {say(d['corr'], 2)}: the two numbers measure different things, and chapter seven "
            "shows why that matters."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(labs), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(FadeIn(dots), FadeIn(side[1:]), run_time=2.0)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def sing(self):
        d = load("sing")
        c = clip("sing.tune")
        notes = d["notes"]
        mel = [[60 + m, i, 1.0] for i, m in enumerate(notes)]
        r = mroll(mel, width=11.0, height=1.8, lo=53, hi=76, color=BLUE, total=len(notes) + 1, bar_h=0.14).move_to(UP * 0.4)
        head = label(r"the listener sings", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        cap = label(rf"each note drawn from the model's own prediction; \ mean surprise {d['mean_ic']:.2f} bits", font_size=18, color=GREY_A).to_edge(DOWN, buff=1.0)
        with self.voiceover(
            "A model that predicts can also generate. Let the listener sing: start on C, and draw each next note from its own "
            "prediction."
        ):
            self.play(FadeIn(head), FadeIn(r), FadeIn(cap))
        with self.listen(c) as snd:
            window(snd, r"the model's melody", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            flash(snd, r.notes, [i * 0.32 for i in range(len(notes))], hot=WHITE, base=BLUE)
        with self.voiceover(
            "It sounds like a folk tune that wanders: every step is plausible, and the phrase has no plan. That is what a "
            "listener without a sense of form produces, and Part 65 will ask what more a composing machine needs."
        ):
            self.play(Indicate(r))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def viewpoints(self):
        items = [
            (r"a melody can be predicted in more than one representation: \ pitch, \ interval, \ contour, \ scale degree, \ duration", WHITE),
            (r"IDyOM runs a model for each such `viewpoint' and combines them, \ weighting the more certain", WHITE),
            (r"ours uses pitch relative to the tonic only, \ with a long-term and a short-term model", WHITE),
            (r"richer viewpoints predict listeners better; \ ours is enough to show the shape of the idea", TUNE),
            (r"Conklin and Witten \ (1995) \ introduced multiple viewpoints for music", GREY_A),
        ]
        rows_scene(self, r"viewpoints", items,
                   "Pearce's full model is richer than ours. <bookmark mark='b'/> A melody can be predicted in more than one "
                   "representation: pitch, interval, contour, scale degree, duration. <bookmark mark='c'/> IDyOM runs a model for "
                   "each such viewpoint and combines them, weighting the more certain. <bookmark mark='d'/> Ours uses pitch "
                   "relative to the tonic only, with a long-term and a short-term model. <bookmark mark='e'/> Richer viewpoints "
                   "predict listeners better; ours is enough to show the shape of the idea. <bookmark mark='f'/> Darrell Conklin "
                   "and Ian Witten introduced multiple viewpoints for music in 1995.", marks="bcdef")
