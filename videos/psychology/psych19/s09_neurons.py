from __future__ import annotations

from videos.psychology.psych19.common import *  # noqa: F403


class Neurons(VoiceoverScene):
    def construct(self):
        self.card()
        self.delay()
        self.ring()
        self.drift()
        self.silent()

    def card(self):
        card = chapter_card(8, r"How neurons hold a thought", r"What keeps a memory alive when the thing is gone?",
                            lit={1989: r"Funahashi et al.", 2014: r"Wimmer et al."}, part=PART,
                            scale=("circuit", "brain"), marr=("how", "tissue"))
        with self.voiceover("Chapter eight. How neurons hold a thought."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def delay(self):
        head = heading(r"Delay activity in prefrontal cortex")
        t = np.linspace(-1.0, 5.0, 400)
        pref = 6 + 34 * ((t > 0) & (t < 0.5)) + 22 * ((t >= 0.5) & (t < 3.5)) + 30 * ((t >= 3.5) & (t < 3.8))
        other = 6 + 4 * ((t > 0) & (t < 0.5)) + 0 * t
        A = axes([-1, 5], [0, 45], x_length=7.2, y_length=3.0, xticks=[0, 0.5, 3.5], yticks=[0, 20, 40],
                 xfmt=lambda v: {0: "cue", 0.5: r"delay", 3.5: r"saccade"}[v] if v in (0, 0.5, 3.5) else "",
                 ylabel=r"spikes per second, \ schematic", center=[-2.3, 0.4, 0], font_size=18)
        ax = A.ax
        c1 = curve_in(ax, t, pref, MEM, 4)
        c2 = curve_in(ax, t, other, GREY_B, 3)
        band = Rectangle(width=ax.c2p(3.5, 0)[0] - ax.c2p(0.5, 0)[0], height=ax.c2p(0, 45)[1] - ax.c2p(0, 0)[1],
                         stroke_width=0, fill_color=MEM, fill_opacity=0.08).move_to(
            [(ax.c2p(0.5, 0)[0] + ax.c2p(3.5, 0)[0]) / 2, (ax.c2p(0, 0)[1] + ax.c2p(0, 45)[1]) / 2, 0])
        key = legend([(MEM, r"cue in the neuron's memory field"), (GREY_B, r"cue elsewhere")], font_size=18)
        key.next_to(A, DOWN, buff=0.3)
        rows = rows_of([
            (r"1989: \ Funahashi, \ Bruce and Goldman-Rakic; \ monkeys fixate while a spot flashes, \ then remember "
             r"where", WHITE),
            (r"after a delay of a few seconds, \ they look to the remembered place", GREY_A),
            (r"neurons in dorsolateral prefrontal cortex keep firing through the delay, \ for one region of space: "
             r"\ a memory field", MEM),
            (r"on error trials the delay firing is weaker or gone", LOST),
        ], 5.0, 22, 0.3).move_to([4.15, 0.3, 0])
        tag = historical_tag(archive.FUNAHASHI_1989.cite)
        with self.voiceover(
            "Where is the thing being held? <bookmark mark='a'/> In 1989 Shintaro Funahashi, Charles Bruce and "
            "Patricia Goldman-Rakic trained monkeys to fixate a central spot while another spot flashed somewhere in "
            "the periphery. <bookmark mark='b'/> After a delay of a few seconds, the fixation spot went out and the "
            "monkey moved its eyes to where the flash had been. <bookmark mark='c'/> Many neurons in the "
            "dorsolateral prefrontal cortex kept firing through the delay, with nothing on the screen, but only "
            "when the flash had been in one region of space, their memory field. The drawing is a schematic of that "
            "pattern. <bookmark mark='d'/> And on trials where the monkey went to the wrong place, the delay "
            "activity was weaker. Something was holding the location in activity. How can a circuit do that, "
            "with neurons whose own activity dies away in tens of milliseconds?"
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(band))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(c1), Create(c2), FadeIn(key), FadeIn(rows[2]), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def ring(self):
        d = load("ring")
        head = heading(r"A ring attractor, \ computed")
        th = d["theta"]
        rates = d["rates"]
        R = 1.7
        center = np.array([-3.6, 0.5, 0])
        ring = Circle(R, color=GREY_D, stroke_width=2).move_to(center)
        units = VGroup(*[Dot(center + R * np.array([np.cos(a), np.sin(a), 0]), radius=0.06,
                             color=interpolate_color(ManimColor(GREY_D), ManimColor(MEM),
                                                     float(min(1, r_ / max(rates.max(), 1e-6)))))
                         for a, r_ in zip(th, rates)])
        bump = VMobject(color=MEM, stroke_width=4)
        pts = [center + (R + 0.15 + 1.1 * r_ / max(rates.max(), 1e-6)) * np.array([np.cos(a), np.sin(a), 0])
               for a, r_ in zip(np.r_[th, th[:1]], np.r_[rates, rates[:1]])]
        bump.set_points_smoothly(pts)
        eq = MathTex(r"\tau\,\dot r_i = -r_i + f\Big(\textstyle\sum_j W_{ij} r_j + I_i + \text{noise}\Big)", font_size=34)
        w = MathTex(r"W_{ij} = \tfrac{1}{n}\big(J_0 + J_1 \cos(\theta_i - \theta_j)\big)", font_size=34, color=EXEC)
        right = VGroup(eq, w).arrange(DOWN, buff=0.3).move_to([3.3, 1.9, 0])
        rows = rows_of([
            (r"96 units on a ring, \ each preferring one angle", WHITE),
            (r"neighbours excite each other, \ distant units inhibit: \ $J_1 = 6$, \ $J_0 = -1$", EXEC),
            (r"a brief cue starts a bump of activity; \ when the cue goes, \ the bump stays", MEM),
            (r"any position on the ring is equally stable: \ a line of fixed points, \ a continuous memory", MODEL),
        ], 6.2, 23, 0.3).move_to([3.3, -0.7, 0])
        ptag = psyche_tag(r"\texttt{wm.ring\_attractor}: \ $\tau = 20$ ms, \ rectified tanh")
        with self.voiceover(
            "Here is the classic answer, built and run. <bookmark mark='a'/> Ninety-six model neurons sit on a ring, "
            "each preferring one angle: one direction, or one colour. <bookmark mark='b'/> Each excites its "
            "neighbours and, through the uniform term, inhibits the rest. Connection strength depends only on the "
            "difference between preferred angles: a cosine. <bookmark mark='c'/> A brief cue at one angle starts a "
            "bump of activity there. When the cue is switched off, the bump doesn't decay: the neurons in it keep "
            "each other going, and the inhibition keeps it from spreading. Each neuron forgets in twenty "
            "milliseconds; the circuit remembers for seconds. <bookmark mark='d'/> Because the connections depend "
            "only on differences, the bump is equally stable at every position. The circuit has a continuous line of "
            "resting states, and it can hold any angle. That is an attractor, and it has a weakness."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ring), FadeIn(units), FadeIn(ptag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(right), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(bump), FadeIn(rows[2]), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def drift(self):
        d = load("ring")
        head = heading(r"The bump diffuses, \ so memory blurs with time")
        t = d["t"] / 1000
        A = axes([0, 4], [-40, 40], x_length=5.6, y_length=3.0, xticks=[0, 1, 2, 3, 4], yticks=[-40, 0, 40],
                 xlabel=r"seconds of delay", ylabel=r"remembered angle $-$ cue, \ degrees", center=[-3.4, 0.6, 0],
                 font_size=17)
        paths = VGroup(*[curve_in(A.ax, t, np.clip(p_, -40, 40), MEM, 2) for p_ in d["paths"]])
        paths.set_stroke(opacity=0.7)
        B = axes([0, 4], [0, float(np.ceil(d["var"].max() * 1.1 * 1e3) / 1e3) if d["var"].max() > 0 else 0.1],
                 x_length=5.0, y_length=3.0, xticks=[0, 1, 2, 3, 4], yticks=[], xlabel=r"seconds of delay",
                 ylabel=r"variance of the memory", center=[3.2, 0.6, 0], font_size=17)
        v = curve_in(B.ax, t, d["var"], MODEL, 4)
        fit = DashedLine(B.ax.c2p(0, 0), B.ax.c2p(4, d["slope"] * 4), color=GREY_B, stroke_width=2)
        fl = label(r"a straight line: \ diffusion", font_size=19, color=GREY_B).next_to(B.ax.c2p(2.0, d["slope"] * 2.6),
                                                                                         UL, buff=0.05)
        sd2 = float(np.interp(2000, d["t"], d["sd_deg"]))
        rows = rows_of([
            (r"noise nudges the bump, \ and nothing pulls it back: \ a random walk along the ring", WHITE),
            (rf"variance grows in proportion to the delay; \ after 2 s the s.d. is about {sd2:.0f} degrees", MODEL),
            (r"Wimmer, \ Nykamp, \ Constantinidis and Compte, \ 2014: \ in monkeys, \ errors grow with delay, \ and "
             r"the drift shows in the neurons' firing", DATA),
            (r"more items, \ more bumps competing in one network: \ one route to precision falling with load", GREY_A),
        ], 12.4, 23, 0.2).to_edge(DOWN, buff=0.75)
        ptag = psyche_tag(r"\texttt{wm.ring\_attractor}: \ 300 trials, \ noise 0.06")
        tag = published_tag(archive.WIMMER_2014.cite)
        with self.voiceover(
            "The weakness is the same property that makes it work. <bookmark mark='a'/> Since every position is "
            "equally stable, a little noise nudges the bump, and nothing pushes it back. Over a delay, the "
            "remembered angle takes a random walk along the ring. Here are twelve trials, all cued at zero. "
            "<bookmark mark='b'/> Across three hundred trials, the variance of the remembered angle grows in a "
            f"straight line with the delay, which is the signature of diffusion. After two seconds the spread is "
            f"about {sd2:.0f} degrees. <bookmark mark='c'/> In 2014 Klaus Wimmer, Duane Nykamp, Christos "
            "Constantinidis and Albert Compte showed that monkeys' errors grow with delay in just this way, and that "
            "trial-by-trial drift in the reported location could be read from the tuning of prefrontal firing during "
            "the delay. <bookmark mark='d'/> Load several items into one such network and their bumps compete and "
            "interfere, which is one way a circuit could produce precision that falls as more is held."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(B), FadeIn(ptag))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(p_) for p_ in paths], lag_ratio=0.15), FadeIn(rows[0]), run_time=3.0)
            vo.wait_until("b")
            self.play(Create(v), Create(fit), FadeIn(fl), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def silent(self):
        head = heading(r"Or held in the synapses, \ silently")
        rows = rows_of([
            (r"some items are held without sustained firing: \ the activity drops to baseline during the delay", WHITE),
            (r"2008: \ Mongillo, \ Barak and Tsodyks: \ short-term facilitation leaves a trace in the synapses for a "
             r"second or more", EXEC),
            (r"a brief burst refreshes it; \ a nonspecific pulse can read it out", MEM),
            (r"2016: \ Rose and colleagues: \ a magnetic pulse brings back a decodable trace of an item not in focus", DATA),
            (r"perhaps the item in focus is held in firing, \ and the others are held silently, \ in the weights", MODEL),
        ], 12.0, 27, 0.38).move_to([0, -0.2, 0])
        tag = historical_tag(archive.MONGILLO_2008.cite)
        with self.voiceover(
            "Persistent firing is not the only candidate. <bookmark mark='a'/> In some studies the information about "
            "a remembered item can't be decoded from activity during parts of the delay, and yet it's recalled "
            "perfectly afterwards. <bookmark mark='b'/> Gianluigi Mongillo, Omri Barak and Misha Tsodyks proposed in "
            "2008 that the memory can sit in the synapses: a burst of firing leaves the connections among the active "
            "neurons temporarily strengthened, by short-term facilitation, for a second or more. "
            "<bookmark mark='c'/> Occasional bursts refresh the trace, and a nonspecific input can read it out. "
            "<bookmark mark='d'/> In 2016 Nathan Rose, Bradley Postle and colleagues found that a pulse of "
            "transcranial magnetic stimulation could briefly bring back a decodable trace of an item that was being "
            "held but was not the current focus. <bookmark mark='e'/> One reconciliation: the item in the focus of "
            "attention is held in firing, and the others are held silently, in the weights. Which one is right is "
            "still argued, and we'll come back to it at the frontier."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
