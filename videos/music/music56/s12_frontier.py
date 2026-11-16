from __future__ import annotations

from videos.music.music56.common import *  # noqa: F403

TCOL = {"vox": TUNE, "piano": BLUE, "guitar": "#A3E635", "bass": EAR, "kick": GREY_A, "snare": GREY_A, "hat": GREY_A}


class Frontier(SoundScene):
    def construct(self):
        chapter(self, 11, r"Frontier: \ automatic mixing", r"Can a machine mix?")
        self.history()
        self.rules()
        self.quiz()
        self.compare()
        self.consoles()
        self.problem()

    # ------------------------------------------------------------------
    def history(self):
        items = [
            (r"1975: \ Dan Dugan's automatic microphone mixer: \ many speech microphones, \ their gains shared so that the total stays constant", WHITE),
            (r"2009 on: \ Perez-Gonzalez and Reiss automate gain, \ panning and EQ from signal measurements", WHITE),
            (r"De Man and Reiss: \ the rules engineers state, \ tested; \ some hold, \ many are matters of taste", WHITE),
            (r"2016 on: \ commercial `assistants' suggest settings for each track; \ 2021: \ a differentiable console trained end to end \ (Steinmetz and colleagues)", WHITE),
            (r"intelligent music production: \ the machine as an assistant, \ or as the engineer", TUNE),
        ]
        rows_scene(self, r"machines that mix", items,
                   "The frontier is a machine that mixes. <bookmark mark='b'/> It began with speech: in 1975 Dan Dugan built an "
                   "automatic microphone mixer for panels and conferences, sharing gain among many microphones so that the total "
                   "stayed constant and only the talker was heard. <bookmark mark='c'/> From 2009 Enrique Perez-Gonzalez and Joshua "
                   "Reiss automated gain, panning and equalization from measurements of the signals. <bookmark mark='d'/> Brecht "
                   "De Man and Reiss collected the rules engineers state, and tested them: some hold, many are matters of taste. "
                   "<bookmark mark='e'/> From 2016 commercial assistants suggested settings for each track, and in 2021 Christian "
                   "Steinmetz and colleagues trained a differentiable mixing console end to end. <bookmark mark='f'/> The field "
                   "calls itself intelligent music production: the machine as an assistant, or as the engineer.", marks="bcdef")

    # ------------------------------------------------------------------
    def rules(self):
        items = [
            (r"loudness: \ every track to the same integrated loudness \ (BS.1770, \ Part 57), \ the lead 3 dB above", WHITE),
            (r"panning: \ the lead, \ and any track with a tenth of its energy below 150 Hz, \ in the centre", WHITE),
            (r"the rest spread alternately left and right, \ further out the brighter they are \ (by spectral centroid)", WHITE),
            (r"equalization: \ a high-pass at 80 Hz and a 3 dB cut at 250 Hz on every bright track", WHITE),
            (r"four rules, \ no ears: \ \texttt{studio.automix}", TUNE),
        ]
        rows_scene(self, r"Monochord's automatic mixer", items,
                   "Monochord's automatic mixer uses four rules from that literature. <bookmark mark='b'/> Loudness: every track to "
                   "the same integrated loudness, measured as Part 57 will measure it, with the lead three decibels above. "
                   "<bookmark mark='c'/> Panning: the lead, and every track with a tenth of its energy below a hundred and fifty "
                   "hertz, in the centre. <bookmark mark='d'/> The rest spread alternately left and right, further out the brighter "
                   "they are. <bookmark mark='e'/> And a high-pass at eighty hertz and a small cut at two hundred and fifty on every "
                   "bright track. <bookmark mark='f'/> Four rules, and no ears.", marks="bcdef")

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("automix")
        c = clip("automix.two")
        card = listen_card(r"Headphones on. \ Our session mixed twice: \ once by hand, \ once by Monochord's automatic mixer. \ "
                           r"Which was the machine?", width=10.0)
        with self.voiceover("Your turn, with headphones. Our session mixed twice: once by hand, once by the automatic mixer. Which was the machine?"):
            self.play(FadeIn(card))
        self.wait(0.8)
        boxes = choice_boxes([r"first", r"second"]).move_to(UP * 0.6)
        self.play(FadeOut(card), FadeIn(boxes))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"two mixes", kind="physical model", detail=r"our session, \ by hand and by rule", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["first"], st["second"] - 0.4, buff=0.08)
            pulse(snd, boxes[1], st["second"], c.duration, buff=0.08)
        with self.voiceover(
            'The second. Its hi-hat is far too loud, and its bass is thin: the rules gave every track the same loudness, which we judge too prominent for this example; preferences depend on production goals.'
        ):
            self.play(boxes[1][0].animate.set_stroke(TUNE, width=4), FadeIn(label(r"the second: \ every track at one loudness, \ the hi-hat as loud as the voice", font_size=19, color=TUNE).move_to(DOWN * 1.4)))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def compare(self):
        d = load("automix")
        tracks = ["vox", "piano", "guitar", "bass", "kick", "snare", "hat"]
        rows = VGroup(VGroup(label(r"track", font_size=16, color=GREY_A), label(r"by hand: \ fader, \ pan", font_size=16, color=GREY_A),
                             label(r"machine: \ fader, \ pan", font_size=16, color=GREY_A), label(r"masked: \ hand", font_size=16, color=GREY_A), label(r"machine", font_size=16, color=GREY_A)))
        for k in tracks:
            h, m = d["hand"][k], d["machine"][k]
            rows.add(VGroup(label(k, font_size=17, color=TCOL[k]), label(rf"{h[0]:+.0f} dB, \ {h[1]:+.2f}", font_size=17, color=WHITE), label(rf"{m[0]:+.0f} dB, \ {m[1]:+.2f}", font_size=17, color=WHITE),
                            label(rf"{100 * d['masked']['hand'][k]:.0f}\%", font_size=17, color=WHITE), label(rf"{100 * d['masked']['machine'][k]:.0f}\%", font_size=17, color=EAR if d['masked']['machine'][k] > 0.45 else WHITE)))
        rows.arrange(DOWN, buff=0.22)
        xs = [-5.2, -2.6, 0.4, 3.0, 4.9]
        for r in rows:
            for i, m in enumerate(r):
                m.set_x(xs[i])
        rows.move_to(DOWN * 0.1)
        note = label(r"the machine unmasks the hi-hat and the piano, \ and buries the bass; \ by the numbers it is not worse, \ by ear it is", font_size=17, color=TUNE).to_edge(DOWN, buff=0.35)
        head = label(r"the two mixes, \ setting by setting", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Compare the settings. <bookmark mark='a'/> The machine raised the hi-hat by eight decibels, because it was the "
            "quietest track, and centred the bass and kick by their low energy, as we did; its pans are not unlike ours. "
            "<bookmark mark='b'/> And the masking map tells a mixed story: the machine's hi-hat and piano are freer than ours, "
            f"but its bass is {say(100 * d['masked']['machine']['bass'])} per cent buried, against our "
            f"{say(100 * d['masked']['hand']['bass'])}. By these numbers the machine's mix is not worse. For our intended balance, we prefer the hand mix; this is not a blind listener study. "
            "Measures of a mix are not yet measures of a good one."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0]), FadeIn(ghost(rows[1:], 0.25)))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rows[1:]], lag_ratio=0.15), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(note))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def consoles(self):
        items = [
            (r"a differentiable console: \ every equalizer, \ compressor and fader written so that its output can be differentiated by its settings", WHITE),
            (r"then the settings can be learned by gradient descent, \ to match a target mix", WHITE),
            (r"trained on many multitracks with their engineers' mixes, \ a network proposes settings for a new session", WHITE),
            (r"the hard part is not the console but the target: \ what makes a mix good, \ for this song, \ for these listeners?", TUNE),
        ]
        rows_scene(self, r"differentiable consoles", items,
                   "The newest work makes the console itself learnable. <bookmark mark='b'/> Write every equalizer, compressor and "
                   "fader so that the output can be differentiated with respect to its settings, <bookmark mark='c'/> and the "
                   "settings can be learned by gradient descent to match a target mix. <bookmark mark='d'/> Trained on many "
                   "multitracks with their engineers' mixes, a network proposes settings for a new session. "
                   "<bookmark mark='e'/> But the hard part is not the console; it is the target. What makes a mix good, for this "
                   "song and these listeners?", marks="bcde")

    # ------------------------------------------------------------------
    def problem(self):
        rows_ = text_rows([
            (r"collect multitracks, \ several engineers' mixes of each, \ and listeners' blind preferences among them", WHITE),
            (r"fit a model of preference from the mix itself: \ loudness, \ masking, \ space, \ dynamics, \ and what they leave out", WHITE),
            (r"use it as the target for a differentiable console, \ and test the results blind against engineers", WHITE),
            (r"$\bigstar$ \ research problem: \ is there an objective, \ other than imitating a mix, \ that predicts which mix listeners prefer?", EAR),
            (r"an answer would turn mixing from imitation into design", TUNE),
        ])
        head = label(r"a research problem", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "A research problem to end on. <bookmark mark='a'/> Collect multitracks, several engineers' mixes of each, and "
            "listeners' blind preferences among them. <bookmark mark='b'/> Fit a model of preference from the mix itself: its "
            "loudness, masking, space and dynamics, and whatever those leave out. <bookmark mark='c'/> Use it as the target for "
            "a differentiable console, and test the results blind against engineers. <bookmark mark='d'/> The question: is there "
            "an objective, other than imitating a mix, that predicts which mix listeners prefer? <bookmark mark='e'/> An answer "
            "would turn automatic mixing from imitation into design."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ghost(rows_, 0.15)))
            for mark, r in zip("abcde", rows_):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()
