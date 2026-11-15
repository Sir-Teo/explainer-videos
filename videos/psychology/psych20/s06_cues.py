from __future__ import annotations

from videos.psychology.psych20.common import *  # noqa: F403

CONDS = (r"land, \ land", r"land, \ water", r"water, \ land", r"water, \ water")


class Cues(VoiceoverScene):
    def construct(self):
        self.card()
        self.specificity()
        self.divers()
        self.replication()
        self.state()

    def card(self):
        card = chapter_card(5, r"The cue and the trace", r"Why can a weak cue beat a strong one?",
                            lit={1973: r"Tulving \& Thomson", 1975: r"Godden \& Baddeley", 1980: r"Eich",
                                 2001: r"Smith \& Vela", 2021: r"Murre"},
                            part=PART, scale=("mind", "person"), marr=("what",))
        with self.voiceover("Chapter five. The cue and the trace."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def specificity(self):
        head = heading(r"Encoding specificity")
        study = VGroup(label(r"study:", font_size=24, color=GREY_B),
                       label(r"train \ \ BLACK", font_size=40)).arrange(RIGHT, buff=0.4)
        strong = VGroup(label(r"cue:", font_size=24, color=GREY_B),
                        label(r"white \ \ ?", font_size=40, color=LOST)).arrange(RIGHT, buff=0.4)
        weak = VGroup(label(r"cue:", font_size=24, color=GREY_B),
                      label(r"train \ \ ?", font_size=40, color=MODEL)).arrange(RIGHT, buff=0.4)
        col = VGroup(study, strong, weak).arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to([-3.6, 0.9, 0])
        ok = label(r"BLACK", font_size=34, color=MODEL).next_to(weak, RIGHT, buff=0.5)
        no = label(r"often not recognised", font_size=24, color=LOST).next_to(strong, RIGHT, buff=0.5)
        rows = rows_of([
            (r"Tulving and Thomson, \ 1973: \ study a word with a weak associate", WHITE),
            (r"the strong associate, \ white, \ fails to bring BLACK back; \ people may not even recognise it", LOST),
            (r"the weak cue from study, \ train, \ brings it back", MODEL),
            (r"a cue works if it was part of what was stored: \ not by its general strength", CUE),
            (r"memory is not a filing system searched by subject: \ the trace holds the moment of study", WORD),
        ], 6.0, 22, 0.3).move_to([3.5, -0.2, 0])
        tag = historical_tag(r"Tulving \& Thomson (1973)")
        with self.voiceover(
            "What makes a good cue? The obvious answer is a strong association: white is a much better reminder of "
            "black than train is. <bookmark mark='a'/> In 1973 Tulving and Donald Thomson had people study words "
            "beside weak associates: train, then black, in capitals. <bookmark mark='b'/> At test, the strong "
            "associate, white, often failed to bring the word back; people sometimes failed even to recognise black "
            "when they saw it again. <bookmark mark='c'/> The weak cue they had studied, train, brought it back. "
            "<bookmark mark='d'/> Tulving called this the encoding specificity principle. A cue helps to the extent "
            "that it was part of what was stored, whatever its strength in general. <bookmark mark='e'/> The trace "
            "is not a word in a filing cabinet, found by its subject heading. It is a record of a moment, and it's "
            "found again by things that were part of that moment."
        ) as vo:
            self.play(FadeIn(head), FadeIn(study), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(strong), FadeIn(no), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(weak), FadeIn(ok), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def _bars(self, A, means, se=None, color_same=MODEL, color_diff=LOST):
        ax = A.ax
        xs = [0.5, 1.5, 2.5, 3.5]
        cols = [color_same, color_diff, color_diff, color_same]
        g = VGroup()
        for x, m, col in zip(xs, means, cols):
            g.add(bars(ax, [x], [m], col, width=0.62)[0])
        errs = VGroup()
        if se is not None:
            for x, m, s in zip(xs, means, se):
                errs.add(Line(ax.c2p(x, m - s), ax.c2p(x, m + s), color=GREY_A, stroke_width=2.5))
        names = VGroup(*[label(t, font_size=16, color=GREY_A).move_to(ax.c2p(x, 0) + DOWN * 0.32)
                         for t, x in zip(CONDS, xs)])
        vals = VGroup(*[label(f"{m:.1f}", font_size=17, color=GREY_A).next_to(b, UP, buff=0.18)
                        for m, b in zip(means, g)])
        return g, errs, names, vals

    def divers(self):
        d = load("divers")
        head = heading(r"Words learnt on land and under water")
        A = axes([0, 4], [0, 16], x_length=5.6, y_length=3.6, xticks=[], yticks=[0, 4, 8, 12, 16], xlabel=r"",
                 ylabel=r"words recalled \ (of 36)", center=[-3.0, -0.2, 0], font_size=18)
        g, _, names, vals = self._bars(A, d["gb_means"])
        gm = d["gb_means"]
        gain = (gm[0] + gm[3]) / (gm[1] + gm[2])
        hd = label(r"learnt, \ then recalled:", font_size=17, color=GREY_B).next_to(names, DOWN, buff=0.12)
        rows = rows_of([
            (r"Godden and Baddeley, \ 1975: \ student divers near Oban, \ 36 words heard on the beach or about "
             r"7 metres down", WHITE),
            (r"recall 4 minutes later, \ in the same place or the other: \ all four combinations", WHITE),
            (rf"same place: \ {d['gb_means'][0]:.1f} and {d['gb_means'][3]:.1f} words; \ other place: \ "
             rf"{d['gb_means'][1]:.1f} and {d['gb_means'][2]:.1f}", MODEL),
            (rf"about {100 * (gain - 1):.0f}\% more recalled when the place matched: \ in every textbook since",
             WORD),
        ], 6.2, 22, 0.3).move_to([3.5, 0.2, 0])
        tag = historical_tag(archive.GODDEN_BADDELEY_1975.cite)
        with self.voiceover(
            "If the trace holds the moment, the place you were in should be a cue. <bookmark mark='a'/> In 1975 "
            "Duncan Godden and Alan Baddeley tested this with student divers, near Oban on the west coast of "
            "Scotland. The divers heard lists of thirty-six words, either on the beach or about seven metres under "
            "the sea. <bookmark mark='b'/> Four minutes later they wrote down what they remembered, in the same place "
            "or the other one, and every diver did all four combinations. <bookmark mark='c'/> Words learned on land "
            "were best recalled on land; words learned under water, under water. <bookmark mark='d'/> About "
            f"{100 * (gain - 1):.0f} percent more words when the places matched. It's one of the most famous experiments in psychology, in "
            "every introductory textbook. It had never been repeated."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(names), FadeIn(hd), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in g], lag_ratio=0.25), FadeIn(vals),
                      FadeIn(rows[2]), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def replication(self):
        d = load("divers")
        head = heading(r"The replication, \ 46 years later")
        A = axes([0, 4], [0, 16], x_length=5.0, y_length=3.0, xticks=[], yticks=[0, 4, 8, 12, 16], xlabel=r"",
                 ylabel=r"words recalled \ (of 36)", center=[-3.6, 0.8, 0], font_size=17)
        g, errs, names, vals = self._bars(A, d["means"], d["se"])
        B = axes([-6, 6], [0, 1], x_length=5.0, y_length=1.2, xticks=[-6, -3, 0, 3, 6], yticks=[], xlabel=r"each "
                 r"diver: \ same place minus other place, \ words", ylabel=r"", center=[-3.6, -2.45, 0], font_size=16,
                 xfmt=lambda v: f"{v:+.0f}" if v else "0")
        bx = B.ax
        eff = np.sort(d["effect"])
        ys = []
        seen = {}
        for v in eff:
            seen[v] = seen.get(v, 0) + 1
            ys.append(0.18 + 0.2 * (seen[v] - 1))
        dots = scatter(bx, eff, ys, DATA, radius=0.06, opacity=1.0)
        zero = DashedLine(bx.c2p(0, 0), bx.c2p(0, 1), color=GREY_B, stroke_width=2)
        orig = Triangle(color=MODEL, fill_opacity=1).scale(0.09).rotate(PI).move_to(bx.c2p(
            (d["gb_means"][0] + d["gb_means"][3] - d["gb_means"][1] - d["gb_means"][2]) / 2, 0.45))
        ol = label(r"1975", font_size=16, color=MODEL).next_to(orig, RIGHT, buff=0.08)
        rows = rows_of([
            (rf"Murre, \ 2021: \ {d['n']} divers, \ the same design, \ 36 words, \ 4 minutes; \ but a heated pool "
             r"1.8 m deep, \ and one session, \ not four days", WHITE),
            (r"land beat water at learning, \ whatever the place at recall", LOST),
            (rf"the context effect, \ diver by diver: \ {d['effect_mean']:+.2f} words, \ s.e.\ "
             rf"{d['effect_se']:.2f}: \ if anything the wrong way", DATA),
            (rf"an exact sign-flip test: \ $p = {d['p_signflip']:.3f}$; \ the 1975 effect was $+4$ words", DATA),
            (r"context effects are real but small: \ $d \approx 0.25$ across studies \ (Smith and Vela, \ 2001)",
             CUE),
            (r"they shrink when other cues are strong, \ and when people imagine the original place: \ thinking "
             r"yourself back is a cue", MODEL),
        ], 6.9, 21, 0.25).move_to([3.3, -0.15, 0])
        tag = published_tag(r"open data: \ Murre (2021), \ osf.io/q2vjk")
        with self.voiceover(
            "In 2021 Jaap Murre in Amsterdam ran it again. <bookmark mark='a'/> Sixteen divers, the same design: lists of "
            "thirty-six words heard on land or under water, and recall four minutes later in one place or the other. "
            "There were differences: the water was a heated pool less than two metres deep, not the cold open sea, "
            "and all four conditions were run in one session rather than over four days. His data are open, so these bars are computed from them. "
            "<bookmark mark='b'/> Words learned on land were remembered better than words learned under water, "
            "wherever they were recalled. <bookmark mark='c'/> But the effect the study was about isn't there. "
            "Here is each diver's own context effect: the average recall in the same place, minus the average in "
            f"the other. The mean is {d['effect_mean']:+.2f} words, slightly the wrong way. "
            f"<bookmark mark='d'/> An exact test that flips the sign of each diver's effect in all sixty-five "
            f"thousand ways gives a p of {d['p_signflip']:.3f}, for an effect in the opposite direction to 1975's "
            "four words. <bookmark mark='e'/> Does that mean context doesn't matter? No. Steven Smith and Edward "
            "Vela combined dozens of studies in 2001, and environmental context effects are real but small, around "
            "a quarter of a standard deviation. <bookmark mark='f'/> They shrink when other cues are strong, and "
            "they shrink again when people at test are asked to picture the room where they learned. Imagining "
            "yourself back does much of the work of going back. That fact is the basis of a police interview technique, in chapter "
            "fourteen."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(names), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), LaggedStart(*[GrowFromEdge(b, DOWN) for b in g], lag_ratio=0.25),
                      FadeIn(errs), FadeIn(vals), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(B), Create(zero), FadeIn(dots), FadeIn(rows[2]), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(orig), FadeIn(ol), FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
            vo.wait_until("f")
            self.play(FadeIn(rows[5]))
        self.clear_scene()

    def state(self):
        head = heading(r"The state you were in")
        rows = rows_of([
            (r"state dependence: \ what is learnt drunk is recalled better drunk than sober \ (Goodwin et al., "
             r"\ 1969)", WHITE),
            (r"Eich, \ 1980: \ the effect appears in free recall, \ and disappears when good cues are given", CUE),
            (r"mood works the same way, \ weakly: \ a state is one more part of the context", CTX),
            (r"the lesson of the chapter: \ remembering is a match between a cue and a trace, \ and the cue that "
             r"is always present is your own state of mind", WORD),
            (r"that suggests a model: \ let a slowly changing state of mind be stored with each item", MODEL),
        ], 12.4, 27, 0.4).move_to([0, -0.2, 0])
        tag = historical_tag(r"Goodwin et al.\ (1969); \ Eich (1980)")
        with self.voiceover(
            "The place you're in is one part of the context. Your own state is another. <bookmark mark='a'/> In "
            "1969 Donald Goodwin and his colleagues found that what people learned after drinking was recalled "
            "better when they had been drinking again than when sober: state-dependent memory. "
            "<bookmark mark='b'/> Eric Eich's review in 1980 found a telling pattern. "
            "State effects show up in free recall, when the person has to supply their own cues, and disappear when "
            "a good cue is supplied. <bookmark mark='c'/> Mood works the same way, weakly. "
            "<bookmark mark='d'/> So here's the lesson of the chapter. Remembering is a match between a cue and a "
            "trace, and the cue that is present every time, whether you like it or not, is your own state of mind "
            "at that moment. <bookmark mark='e'/> That suggests a model. Suppose a slowly changing internal state "
            "is stored along with everything you experience. Then the chapters ahead almost write themselves."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
