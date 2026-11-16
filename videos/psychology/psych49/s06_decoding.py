from __future__ import annotations

from videos.psychology.psych49.common import *  # noqa: F403


class Decoding(VoiceoverScene):
    def construct(self):
        self.card()
        self.haxby()
        self.leak()
        self.meaning()

    def card(self):
        card = chapter_card(5, r"Patterns", r"What can be read from many voxels at once?", lit=(), part=PART,
                            scale=("brain",), marr=("what",))
        with self.voiceover("Chapter five. Patterns."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def haxby(self):
        head = heading(r"From blobs to patterns")
        rows = rows_of([
            (r"2001: \ James Haxby and colleagues showed people faces, \ houses, \ chairs, \ shoes and four other "
             r"categories", WHITE),
            (r"they split each person's data in half, \ and asked whether the pattern for a category in one half "
             r"matched the same category in the other better than the rest", MODEL),
            (r"it did, \ across ventral temporal cortex, \ and still did with the most selective voxels removed", GOOD),
            (r"the information was spread out: \ a pattern, \ not only a blob", PERSON),
            (r"modern decoders train a classifier on some trials and test it on others: \ cross-validation", YOU),
        ], 12.4, 22, 0.4).move_to([0, -0.3, 0])
        tag = published_tag(r"Haxby et al.\ (2001)")
        with self.voiceover(
            "Mass-univariate maps test each voxel alone. Patterns ask what many voxels say together. "
            "<bookmark mark='a'/> In 2001 James Haxby and colleagues showed people faces, houses, chairs, shoes, and "
            "four other categories. <bookmark mark='b'/> They split each person's data in half, and asked whether a "
            "category's pattern in one half matched the same category in the other half better than the rest. "
            "<bookmark mark='c'/> It did, across ventral temporal cortex, and it still did with the most selective "
            "voxels taken out. <bookmark mark='d'/> The information was spread out, a pattern and not only a blob. "
            "<bookmark mark='e'/> Modern decoders train a classifier on some trials and test it on others. That's "
            "cross-validation, and it's where the trouble starts."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def leak(self):
        d = load("decoding")
        head = heading(r"Decoding noise at 94\%")
        A = axes([0.3, 6.7], [0.4, 1.0], x_length=6.0, y_length=3.0, xticks=None, yticks=[0.5, 0.75, 1.0],
                 yfmt=lambda v: f"{100 * v:.0f}\\%", ylabel=r"cross-validated accuracy", center=[-3.0, 0.3, 0],
                 font_size=12)
        vals = [d["null_all"], d["null_nested"], d["null_leaky"], d["sig_all"], d["sig_nested"], d["sig_leaky"]]
        cols = [GREY_B, GOOD, AUTH, GREY_B, GOOD, AUTH]
        b = bars(A.ax, [1, 2, 3, 4.6, 5.6, 6.6], vals, cols, width=0.6)
        chance = DashedLine(A.ax.c2p(0.3, 0.5), A.ax.c2p(6.7, 0.5), color=GREY_B, stroke_width=1.5)
        grp = VGroup(label(r"pure noise", font_size=15, color=WHITE).next_to(A.ax.c2p(2, 0.4), DOWN, buff=0.45),
                     label(r"a weak signal", font_size=15, color=WHITE).next_to(A.ax.c2p(5.6, 0.4), DOWN, buff=0.45))
        key = VGroup(label(r"all voxels", font_size=13, color=GREY_B), label(r"selected inside each fold", font_size=13,
                                                                           color=GOOD),
                     label(r"selected on all the data first", font_size=13, color=AUTH)).arrange(RIGHT, buff=0.3)
        key.next_to(A, UP, buff=0.25)
        rows = rows_of([
            (r"two categories, \ 40 trials each, \ 1,000 voxels; \ a nearest-centroid decoder, \ five-fold "
             r"cross-validation", WHITE),
            (rf"on pure noise, \ all voxels give {100 * d['null_all']:.0f}\%: \ chance", GREY_B),
            (rf"pick the 50 most different voxels using all the trials, \ then cross-validate: \ "
             rf"{100 * d['null_leaky']:.0f}\%, \ from nothing", AUTH),
            (rf"pick them inside each training fold only: \ {100 * d['null_nested']:.0f}\%; \ with a real weak "
             rf"signal, \ {100 * d['sig_nested']:.0f}\%", GOOD),
        ], 5.4, 18, 0.34).move_to([3.7, -0.1, 0])
        tag = psyche_tag(r"\texttt{neurodata.decoding}, \ 100 datasets each")
        with self.voiceover(
            "Here's how a decoder can read noise. <bookmark mark='a'/> Two categories, forty trials each, a thousand "
            "voxels, and a simple decoder tested by five-fold cross-validation. <bookmark mark='b'/> On pure noise, "
            "using every voxel, it scores about fifty percent: chance. <bookmark mark='c'/> Now pick the fifty voxels "
            "that differ most between the categories, using all the trials, and only then cross-validate. Ninety-four "
            "percent, from nothing. The test trials helped choose the voxels. <bookmark mark='d'/> Pick them inside "
            "each training fold only, and it's back to chance. With a real but weak signal, the honest decoder finds "
            "about two thirds. Any step that sees the test data, selection, scaling or tuning, belongs inside the loop."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(chance), FadeIn(grp), FadeIn(key))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(b[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(b[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]), FadeIn(b[1]), FadeIn(b[3]), FadeIn(b[4]), FadeIn(b[5]))
        self.clear_scene()

    def meaning(self):
        head = heading(r"What decoding shows, \ and what it does not")
        left = rows_of([
            (r"shows", GOOD),
            (r"the information is present in the region's activity, \ in a form a linear readout can use", WHITE),
            (r"how it generalizes: \ across runs, \ people, \ or from seeing to imagining", WHITE),
        ], 5.8, 21, 0.32).move_to([-3.3, 0.0, 0])
        right = rows_of([
            (r"does not show", AUTH),
            (r"that the brain uses it: \ a confound such as eye movements or reaction time can carry the label", WHITE),
            (r"that the region computes it: \ the information may be inherited from elsewhere", WHITE),
            (r"what the representation is: \ that is the next chapter's question", WHITE),
        ], 5.8, 21, 0.32).move_to([3.3, 0.0, 0])
        with self.voiceover(
            "So what does decoding show? <bookmark mark='a'/> That the information is present in the region's "
            "activity, in a form a linear readout can use, and how far it generalizes: across runs, across people, or "
            "from seeing to imagining. <bookmark mark='b'/> It doesn't show that the brain uses the information. A "
            "confound such as eye movements or reaction time can carry the label. It doesn't show that the region "
            "computes it, since the information may be inherited from elsewhere. And it doesn't show what the "
            "representation is. That's the next chapter's question."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(left))
            vo.wait_until("b")
            self.play(FadeIn(right))
        self.wait(1.0)
        self.clear_scene()
