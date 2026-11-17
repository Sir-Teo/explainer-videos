from __future__ import annotations

from videos.psychology.psych58.common import *  # noqa: F403


class Efficient(VoiceoverScene):
    def construct(self):
        card_section(self, 2, r"Efficient coding", r"Why would a neuron care about statistics?", marr=("what",))
        self.barlow()
        self.laughlin()
        self.whitening()

    def barlow(self):
        rows_section(self, r"Redundancy", [
            (r"Attneave, \ 1954: \ natural images are redundant; \ most of a picture can be guessed from its "
             r"neighbouring points and edges", WHITE),
            (r"Barlow, \ 1961: \ the senses send a few million fibres' worth of signal; \ a good code spends them on "
             r"what cannot be predicted", MODEL),
            (r"the efficient coding hypothesis: \ neurons are tuned to the statistics of the world, \ to carry as "
             r"much information as their limits allow", GOOD),
            (r"a normative theory: \ it says what a code should be, \ then checks whether neurons are like that", YOU),
        ], "Why would a neuron care about statistics? <bookmark mark='a'/> In 1954 Fred Attneave pointed out that "
           "natural images are redundant: most of a picture can be guessed from neighbouring points and edges. "
           "<bookmark mark='b'/> In 1961 Horace Barlow argued that the senses have limited capacity, so a good code "
           "spends it on what can't be predicted. <bookmark mark='c'/> That's the efficient coding hypothesis: "
           "neurons are tuned to the statistics of the world, to carry as much information as their limits allow. "
           "<bookmark mark='d'/> It's a normative theory. It says what a code should be, then checks whether "
           "neurons are like that.", tag=historical_tag(r"Barlow (1961)"))

    def laughlin(self):
        d = load("laughlin")
        c = load("codes")
        head = heading(r"A fly's contrast code")
        A = axes([-1, 1], [0, 1.0], x_length=5.6, y_length=3.2, xticks=[-1, -0.5, 0, 0.5, 1.0], yticks=[0, 0.5, 1.0],
                 xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", xlabel=r"local contrast",
                 ylabel=r"response", center=[-3.3, 0.2, 0], font_size=12)
        mids = 0.5 * (np.asarray(d["edges"][1:]) + np.asarray(d["edges"][:-1]))
        hist = np.asarray(d["hist"]) / np.max(d["hist"])
        hb = bars(A.ax, mids, hist, CROWD, width=0.045, opacity=0.5)
        resp = curve(A.ax, d["grid"], d["response"], PERSON, stroke_width=4)
        key = VGroup(label(r"how often each contrast occurs", font_size=13, color=CROWD),
                     label(r"the best response curve", font_size=13, color=PERSON)).arrange(RIGHT, buff=0.4)
        key.next_to(A, UP, buff=0.2)
        rows = rows_of([
            (r"Laughlin, \ 1981: \ a fly's large monopolar cells have a limited range of responses", WHITE),
            (r"to use every level equally often, \ the response should be the cumulative distribution of the "
             r"contrasts the fly meets", MODEL),
            (r"he measured the contrasts in the fly's habitat: \ the cells' response curve matched the prediction",
             GOOD),
            (rf"in Psyche's world, \ 20 levels give {c['matched_bits']:.1f} bits per response when matched, \ "
             rf"{c['linear_bits']:.1f} when spaced evenly; \ your third number: \ the commonest contrasts, \ near "
             rf"zero, \ get the most levels", YOU),
        ], 6.0, 19, 0.36).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{efficient.laughlin}")
        tag2 = published_tag(r"Laughlin (1981)").to_corner(DL, buff=0.3)
        with self.voiceover(
            "Here's the first clean test. <bookmark mark='a'/> In 1981 Simon Laughlin studied cells in a fly's eye "
            "that have a limited range of responses. <bookmark mark='b'/> To use every level equally often, the "
            "response should be the cumulative distribution of the contrasts the fly meets: steep where contrasts "
            "are common, flat where they're rare. <bookmark mark='c'/> He measured the contrasts in the fly's "
            "habitat, and the cells' response curve matched the prediction. <bookmark mark='d'/> In Psyche's world, "
            "twenty levels carry about four point two bits per response when they're matched, and three point seven "
            "when they're spaced evenly. Your third number: the commonest contrasts, near zero, get the most levels."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(tag2), FadeIn(A), FadeIn(key))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(hb))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), Create(resp), run_time=2.0)
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def whitening(self):
        d = load("images")
        head = heading(r"Centre-surround, \ derived")
        k = np.arange(1, len(d["spectrum"]) + 1)
        A = axes([0, 2.0], [-2.2, 0.2], x_length=4.6, y_length=3.0, xticks=[0, 1, 2], yticks=[-2, -1, 0],
                 xfmt=lambda v: rf"10^{{{int(v)}}}", yfmt=lambda v: rf"10^{{{int(v)}}}",
                 xlabel=r"component (by variance)", ylabel=r"variance", center=[-4.0, 0.3, 0], font_size=12)
        sp = np.asarray(d["spectrum"])[:-1]
        ws = np.asarray(d["white_spectrum"])[:-1]
        c1 = curve(A.ax, np.log10(k[:-1]), np.log10(sp / sp[0]), CROWD, stroke_width=4)
        c2 = curve(A.ax, np.log10(k[:-1]), np.log10(np.maximum(ws / ws[0], 1e-3)), GOOD, stroke_width=4)
        key = VGroup(label(r"patches", font_size=13, color=CROWD), label(r"whitened", font_size=13, color=GOOD))
        key.arrange(RIGHT, buff=0.4).next_to(A, UP, buff=0.2)
        f = np.asarray(d["filter"])
        filt = heat(np.clip(f / 1.2, -1, 1) * 0.5 + 0.5, height=2.4, grey=True, center=[0.6, 0.4, 0])
        fl = label(r"the whitening filter for one pixel", font_size=13, color=GREY_A).next_to(filt, DOWN, buff=0.1)
        rows = rows_of([
            (r"natural images have most power at low spatial frequencies, \ falling roughly as $1/f^2$", WHITE),
            (r"removing that redundancy (whitening) flattens the spectrum: \ every component carries equal variance",
             GOOD),
            (r"the filter that does it: \ a bright centre and a dark ring, \ Part 13's retinal ganglion cell", PERSON),
            (r"the retina adds a roll-off at high frequencies, \ where noise dominates (Atick and Redlich)", MODEL),
        ], 4.2, 18, 0.34).move_to([4.6, -0.1, 0])
        tag = psyche_tag(r"\texttt{efficient.zca}")
        with self.voiceover(
            "Now take the same idea to space. <bookmark mark='a'/> Natural images have most of their power at low "
            "spatial frequencies, falling roughly as one over frequency squared. Here's the variance of each "
            "component of Psyche's patches, on log scales. <bookmark mark='b'/> Removing that redundancy, called "
            "whitening, flattens the spectrum, so every component carries equal variance. <bookmark mark='c'/> And "
            "here's the filter that does it, for one pixel: a bright centre and a dark ring. It's Part 13's retinal "
            "ganglion cell. <bookmark mark='d'/> Joseph Atick and Norman Redlich added that the retina should roll "
            "off at high frequencies, where noise dominates, and that's what it does."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(key))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), Create(c1))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), Create(c2))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(filt), FadeIn(fl))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
