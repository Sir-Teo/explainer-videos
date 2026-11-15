from __future__ import annotations

from videos.psychology.psych28.common import *  # noqa: F403


class Replication(VoiceoverScene):
    def construct(self):
        self.card()
        self.protocol()
        self.forest()
        self.after()

    def card(self):
        card = chapter_card(9, r"Twenty-three laboratories", r"What happens when everyone runs the same study?",
                            lit={2014: r"Sripada et al.", 2016: r"Hagger et al.", 2021: r"Vohs et al."},
                            part=PART, scale=("mind", "group"), marr=("what",))
        with self.voiceover("Chapter nine. Twenty-three laboratories."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def protocol(self):
        head = heading(r"A registered replication")
        strip = trial_strip([
            (r"easy: \ one rule", wrapped_label(r"cross out every e", 3.0, 22, CTRL), ""),
            (r"depleting: \ break the habit", wrapped_label(r"cross out every e, \ except next to a vowel or one "
                                                              r"letter away", 3.0, 20, LOST), ""),
            (r"how variable are the responses?", wrapped_label(r"the multi-source interference task", 3.0, 20, WANT),
             ""),
        ], frame_w=3.6, frame_h=1.6, font_size=18).move_to([0, 1.0, 0])
        rows = rows_of([
            (r"the protocol: \ Sripada, \ Kessler and Jonides's 2014 study; \ first a letter-crossing task, \ easy "
             r"or depleting, \ then a test of control; \ the outcome, \ reaction-time variability", WHITE),
            (r"written and registered before any data, \ reviewed in advance, \ run in 23 laboratories in many "
             r"countries", INTR),
            (r"the result was to be published whatever it was", BODY),
        ], 12.2, 25, 0.36).move_to([0, -1.9, 0])
        tag = published_tag(r"Sripada, \ Kessler \& Jonides (2014); \ Hagger et al.\ (2016)")
        with self.voiceover(
            "In 2016 the journal Perspectives on Psychological Science published a Registered Replication Report "
            "on ego depletion, led by Martin Hagger and Nikos Chatzisarantis. <bookmark mark='a'/> The protocol "
            "came from a 2014 study by Chandra Sripada, Daniel Kessler and John Jonides. First, a letter-crossing "
            "task: cross out every e, which is easy, or cross out every e except when it's next to a vowel or one "
            "letter away from one, which means breaking the habit you just formed. Then a test of control, the "
            "multi-source interference task. The outcome: how variable the reaction times were. "
            "<bookmark mark='b'/> The protocol was written and registered before any data were collected, reviewed "
            "in advance, and run in twenty-three laboratories in many countries. <bookmark mark='c'/> And the "
            "result was to be published whatever it turned out to be."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(strip))
            for m, r in zip("abc", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def forest(self):
        d = load("rrr")
        n_people = f"{d['N']:,}"
        head = heading(r"The forest plot")
        k = d["k"]
        x0, x1 = -1.2, 1.4
        A = axes([x0, x1], [0, k + 3.5], x_length=6.6, y_length=5.6, xticks=[-1, -0.5, 0, 0.5, 1],
                 yticks=None, xfmt=lambda v: f"{v:g}", xlabel=r"Hedges's $g$: \ depleted minus control",
                 center=[-2.6, -0.35, 0], font_size=15)
        zero = DashedLine(A.ax.c2p(0, 0), A.ax.c2p(0, k + 3.5), color=GREY_B, stroke_width=2)
        rows_ = VGroup()
        for i in range(k):
            y = k - i + 1.5
            col = INTR if d["english"][i] else BODY
            lo, hi = max(float(d["lo"][i]), x0), min(float(d["hi"][i]), x1)
            rows_.add(VGroup(Line(A.ax.c2p(lo, y), A.ax.c2p(hi, y), color=col, stroke_width=2),
                             Square(side_length=0.05 + 0.0006 * float(d["n"][i]), color=col, fill_opacity=1,
                                    stroke_width=0).move_to(A.ax.c2p(float(d["g"][i]), y))))
        oy = k + 2.6
        orig = VGroup(Line(A.ax.c2p(d["orig_lo"], oy), A.ax.c2p(min(d["orig_hi"], x1), oy), color=EXTR, stroke_width=3),
                      Square(side_length=0.12, color=EXTR, fill_opacity=1, stroke_width=0).move_to(
                          A.ax.c2p(d["orig_g"], oy)))
        ol = label(r"the original study", font_size=15, color=EXTR).next_to(A.ax.c2p(x1, oy), RIGHT, buff=0.1)
        dy = 0.6
        diamond = Polygon(A.ax.c2p(d["re_lo"], dy), A.ax.c2p(d["re"], dy + 0.45), A.ax.c2p(d["re_hi"], dy),
                          A.ax.c2p(d["re"], dy - 0.45), color=WANT, fill_opacity=0.9, stroke_width=0)
        dl = label(r"all 23, \ pooled", font_size=15, color=WANT).next_to(A.ax.c2p(x1, dy), RIGHT, buff=0.1)
        key = legend([(INTR, r"English-speaking labs"), (BODY, r"other languages")], font_size=15)
        key.next_to(A.ax.c2p(x1, k - 3), RIGHT, buff=0.1)
        info = rows_of([
            (rf"the original: \ $g = {d['orig_g']:.2f}$, \ {d['orig_n']} people", EXTR),
            (rf"{d['k']} laboratories, \ {num(d['N'])} people: \ {d['n_positive']} estimates above zero, \ "
             rf"{d['n_sig']} significant", WHITE),
            (rf"pooled: \ $d = {d['re']:.2f}$ \ [{d['re_lo']:.2f}, \ {d['re_hi']:.2f}]", WANT),
            (rf"the labs disagree little more than chance predicts: \ $I^2 = {100 * d['I2']:.0f}\%$", BODY),
        ], 4.2, 20, 0.3).move_to([4.6, -1.3, 0])
        tag = published_tag(r"Hagger et al.\ (2016): \ data from osf.io/jymhe, \ recomputed")
        with self.voiceover(
            "Here are the results, recomputed from the report's own table of laboratories. "
            f"<bookmark mark='a'/> At the top, the study the protocol came from: an effect of {d['orig_g']:.2f}, "
            f"from {d['orig_n']} people, with a wide interval. <bookmark mark='b'/> Below it, the twenty-three "
            f"laboratories, {n_people} people in all, each with its estimate and interval, the squares sized by the "
            f"sample. {d['n_positive']} estimates are above zero and the rest below; {d['n_sig']} are individually "
            "significant. <bookmark mark='c'/> Pooled by a random-effects meta-analysis, the effect is "
            f"{d['re']:.2f}, with an interval from {d['re_lo']:.2f} to {d['re_hi']:.2f}. The published "
            "report gave the same estimate, point oh four. <bookmark mark='d'/> And the laboratories disagree with one another "
            "little more than chance alone predicts. Twenty-three teams found, together, almost nothing."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(zero))
            vo.wait_until("a")
            self.play(FadeIn(orig), FadeIn(ol), FadeIn(info[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in rows_], lag_ratio=0.15), FadeIn(key), FadeIn(info[1]),
                      run_time=3.0)
            vo.wait_until("c")
            self.play(FadeIn(diamond, scale=0.5), FadeIn(dl), FadeIn(info[2]))
            vo.wait_until("d")
            self.play(FadeIn(info[3]))
        self.clear_scene()

    def after(self):
        head = heading(r"After the report")
        rows = rows_of([
            (r"Baumeister and Vohs replied that the letter task was too weak to deplete anyone, \ and that the "
             r"protocol should not have been run in so many countries and languages", EXTR),
            (r"so a second multisite test was designed with the theory's proponents, \ using tasks they chose; "
             r"\ published in 2021, \ it also found an effect close to zero", LOST),
            (r"what remains: \ people do feel tired after effort, \ and do then prefer easier things; \ what "
             r"failed is a resource that one act uses up and the next runs short of", WHITE),
            (r"what changed: \ a famous effect checked in a way its advocates had agreed to, \ and a field that "
             r"now registers its big tests", INTR),
        ], 12.2, 26, 0.42).move_to([0, -0.2, 0])
        tag = published_tag(r"Baumeister \& Vohs (2016); \ Vohs et al.\ (2021)")
        with self.voiceover(
            "The original authors did not accept the result. <bookmark mark='a'/> Roy Baumeister and Kathleen Vohs "
            "replied that the letter-crossing task was too weak to deplete anyone, and that running one protocol in "
            "so many countries and languages was a mistake. <bookmark mark='b'/> So a second multisite test was "
            "designed with the theory's proponents, using tasks they chose, and led by Vohs herself. Published in "
            "2021, it too found an effect close to zero. <bookmark mark='c'/> What remains is real enough. People "
            "do feel tired after sustained effort, and do then prefer easier things. What failed is the specific "
            "claim: a resource that one act of self-control uses up and the next runs short of. "
            "<bookmark mark='d'/> And something changed. A famous effect was checked in a way its own advocates had "
            "agreed to, and the field now registers its big tests before running them."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
