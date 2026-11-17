from __future__ import annotations

import numpy as np

from videos.psychology.psych16.common import *  # noqa: F403


class Extinction(VoiceoverScene):
    def construct(self):
        self.card()
        self.failures()
        self.latent()
        self.renewal()
        self.recovery()

    def card(self):
        card = chapter_card(8, r"What the rule gets wrong", r"Does extinction erase what was learned?",
                            lit={1959: r"Lubow \& Moore", 1979: r"Bouton \& Bolles"}, part=PART, scale=("mind",),
                            marr=("what", "how"))
        with self.voiceover("Chapter eight. What the rule gets wrong."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def failures(self):
        head = heading(r"Three facts the rule cannot produce")
        rows = rows_of([
            (r"a cue seen often, \ with nothing following, \ is later learned about slowly: \ latent inhibition", CS),
            (r"an extinguished response returns with time: \ spontaneous recovery", YOU),
            (r"and when the context changes: \ renewal", CONTEXT),
            (r"in the rule, \ a cue with $V = 0$ is a cue with $V = 0$: \ it has no memory of its history", BAD),
        ], 12.4, 30, 0.45).move_to([0, -0.1, 0])
        with self.voiceover(
            "The rule's successes are real, and so are its failures, and the failures taught the field as much. "
            "<bookmark mark='a'/> First: show a rat a tone many times with nothing following, then pair it with "
            "shock. It learns more slowly than a rat that never heard the tone. <bookmark mark='b'/> Second: an "
            "extinguished response comes back with time, as Pavlov's dogs showed. <bookmark mark='c'/> Third: it also "
            "comes back when the animal is moved to a different place. <bookmark mark='d'/> In the rule, all three "
            "are impossible for the same reason. A cue's whole state is one number. A tone that has never been "
            "trained and a tone that was trained and then extinguished both sit at zero, and the rule can't tell "
            "them apart. Animals can."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def latent(self):
        d = load("extinction")
        head = heading(r"Latent inhibition, \ 1959")
        A = axes([0, 12], [0, 1.0], x_length=6.6, y_length=3.6, xticks=[0, 4, 8, 12], yticks=[0, 0.5, 1],
                 xlabel=r"pairings with the outcome", ylabel=r"$V$", center=[-2.6, 0.4, 0])
        ax = A.ax
        x = np.arange(13)
        rw = curve(ax, x, d["rw_new"], GREY_B, stroke_width=4)
        ph_new = curve(ax, x, d["ph_new"], CS, stroke_width=4)
        ph_pre = curve(ax, x, d["ph_pre"], INHIB, stroke_width=4)
        lg = legend([(GREY_B, r"Rescorla-Wagner: \ preexposed or not, \ the same"),
                     (CS, r"Pearce-Hall: \ a new cue"), (INHIB, r"Pearce-Hall: \ after 40 empty presentations")],
                    font_size=19)
        lg.next_to(A, DOWN, buff=0.25)
        rows = rows_of([
            (r"Lubow and Moore: \ sheep and goats, \ a preexposed signal, \ slower conditioning", WHITE),
            (r"Rescorla-Wagner: \ preexposure leaves $V$ at zero, \ so it changes nothing", GREY_B),
            (r"a cue followed by nothing, \ predictably, \ loses attention; \ chapter nine", INHIB),
        ], 4.4, 25, 0.34).move_to([4.5, 0.4, 0])
        keep_in_frame(rows)
        tag = historical_tag(archive.LUBOW_MOORE_1959.cite)
        tag2 = psyche_tag(r"computed: \ \texttt{rescorla\_wagner} and \texttt{pearce\_hall}")
        with self.voiceover(
            "Take the first. <bookmark mark='a'/> In 1959 Robert Lubow and Ulrich Moore preexposed sheep and goats "
            "to a signal, unpaired with anything, and then conditioned them with it. Conditioning came more slowly "
            "than to a fresh signal. They named it latent inhibition. <bookmark mark='b'/> In Rescorla-Wagner, "
            "preexposure does nothing at all: with no outcome and no prediction, the error is zero, and the grey "
            "curve is the same either way. <bookmark mark='c'/> Something else changed during preexposure: the animal "
            "learned to ignore a cue that predicts nothing. The red curve is a model in which attention is learned, "
            "and it comes in the next chapter."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(tag), FadeIn(tag2))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(rw), FadeIn(lg[0]), FadeIn(rows[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(Create(ph_new), Create(ph_pre), FadeIn(lg[1]), FadeIn(lg[2]), FadeIn(rows[2]), run_time=2.0)
        self.clear_scene()

    def renewal(self):
        d = load("extinction")
        r = d["renewal"]
        head = heading(r"Renewal: \ Bouton and Bolles, \ 1979")
        designs = ["AAA", "ABA", "ABC", "AAB"]
        A = axes([-0.5, 3.5], [0, 1.05], x_length=5.6, y_length=3.4, xticks=[], yticks=[0, 0.5, 1],
                 ylabel=r"response at test", center=[-3.4, 0.2, 0])
        ax = A.ax
        bars = VGroup()
        labs = VGroup()
        for k, des in enumerate(designs):
            v = float(r[des])
            col = GREY_B if des == "AAA" else CONTEXT
            b = Rectangle(width=0.7, height=max(ax.c2p(0, v)[1] - ax.c2p(0, 0)[1], 0.02), stroke_width=0,
                          fill_color=col, fill_opacity=0.85).move_to(ax.c2p(k, 0), aligned_edge=DOWN)
            bars.add(b)
            labs.add(label(des, font_size=24, color=col).next_to(ax.c2p(k, 0), DOWN, buff=0.15))
        cap = label(r"contexts of training, \ extinction, \ test", font_size=20, color=GREY_A).next_to(labs, DOWN,
                                                                                                    buff=0.15)
        model = VGroup(
            label(r"Psyche's two memories", font_size=26, color=YOU),
            MathTex(r"R = E - \textstyle\sum_k s(\text{test}, k)\, I_k", font_size=38),
            label(r"$E$: \ the first learning, \ good everywhere", font_size=22, color=CR),
            label(r"$I_k$: \ extinction, \ stored with its context $k$", font_size=22, color=INHIB),
            label(r"$s$: \ 1 in the same context, \ 0.15 in another", font_size=22, color=CONTEXT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([3.4, 1.1, 0])
        rows = rows_of([
            (r"fear trained in box A, \ extinguished in box B, \ tested back in A: \ it returns in full", CONTEXT),
            (r"extinction is new learning, \ and it is the second meaning of the cue that depends on context", INHIB),
            (r"the model makes AAB as strong as ABC; \ in the data it is usually weaker", BAD),
        ], 6.0, 23, 0.26).move_to([3.4, -1.9, 0])
        keep_in_frame(rows)
        tag = historical_tag(archive.BOUTON_BOLLES_1979.cite)
        tag2 = psyche_tag(r"computed: \ \texttt{conditioning.renewal}")
        with self.voiceover(
            "The third failure turned into a theory. <bookmark mark='a'/> In 1979 Mark Bouton and Robert Bolles "
            "trained fear of a tone in one box, A, extinguished it completely in a different box, B, and then tested "
            "the tone back in A. The fear came back, at the level of rats that had never been extinguished. "
            "<bookmark mark='b'/> Bouton's reading: extinction doesn't erase the first learning. It adds a second "
            "memory, the cue now means nothing, and it's that second meaning which depends on the context where it "
            "was learned. <bookmark mark='c'/> Psyche's version keeps two memories. An excitatory one, from training, "
            "that holds everywhere, and inhibitory ones, from extinction, each tagged with its context and expressed "
            "fully only there. <bookmark mark='d'/> Extinguish and test in the same box, and the response stays "
            "gone. Test anywhere else, and it comes back. <bookmark mark='e'/> And here's where Psyche is wrong. It "
            "predicts the same return when training and extinction share a box and the test is somewhere new. Real "
            "animals show that too, but usually less: some of the first learning is tied to its context as well."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(tag2), FadeIn(A), FadeIn(labs), FadeIn(cap))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), GrowFromEdge(bars[1], DOWN))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(model))
            vo.wait_until("d")
            self.play(GrowFromEdge(bars[0], DOWN), GrowFromEdge(bars[2], DOWN), GrowFromEdge(bars[3], DOWN),
                      run_time=2.0)
            vo.wait_until("e")
            self.play(FadeIn(rows[2]), Indicate(labs[3], color=BAD))
        self.clear_scene()

    def recovery(self):
        d = load("extinction")
        head = heading(r"Time is a context too")
        A = axes([0, 96], [0, 1.0], x_length=7.0, y_length=3.6, xticks=[0, 24, 48, 72, 96], yticks=[0, 0.5, 1],
                 xlabel=r"hours between extinction and test", ylabel=r"response", center=[-2.4, 0.4, 0])
        ax = A.ax
        c = curve(ax, d["delays"], d["recovery"], YOU, stroke_width=4)
        rows = rows_of([
            (r"as time passes, \ the test drifts away from the moment of extinction", WHITE),
            (r"so the extinction memory is expressed less, \ and the response recovers", YOU),
            (r"why fears treated in a clinic can return weeks later, \ and at home: \ chapter fourteen", INHIB),
        ], 4.4, 25, 0.36).move_to([4.6, 0.4, 0])
        keep_in_frame(rows)
        tag = psyche_tag(r"computed: \ the same model, \ its context drifting with a time constant of 48 hours")
        with self.voiceover(
            "Spontaneous recovery fits the same idea. <bookmark mark='a'/> Bouton argued that time works like a "
            "context: the longer the gap, the less the moment of the test resembles the moment of extinction. "
            "<bookmark mark='b'/> In Psyche, the extinction memory is expressed less as that resemblance fades, and "
            "the response climbs back toward its trained level. <bookmark mark='c'/> This matters far beyond the "
            "laboratory. A fear extinguished in a therapist's office, this week, is extinguished there and then. "
            "That it can come back later, and at home, isn't a failure of the patient. It's what extinction is."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(c), FadeIn(rows[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()
