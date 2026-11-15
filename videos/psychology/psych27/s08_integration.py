from __future__ import annotations

from videos.psychology.psych27.common import *  # noqa: F403


def ring_picture(n, center, radius=1.1, col=IIT, cut=None):
    """Nodes on a circle with arrows to the next node (a copy ring); ``cut`` draws the bipartition line."""
    c = np.array(center, float)
    pts = [c + radius * np.array([np.cos(2 * PI * k / n + PI / 2), np.sin(2 * PI * k / n + PI / 2), 0])
           for k in range(n)]
    g = VGroup()
    for k in range(n):
        a, b = pts[k], pts[(k + 1) % n]
        g.add(Arrow(a, b, buff=0.22, color=GREY_B, stroke_width=3, max_tip_length_to_length_ratio=0.2))
    for k, p in enumerate(pts):
        g.add(VGroup(Circle(radius=0.2, color=col, fill_opacity=0.35), label(str(k), font_size=18)).move_to(p))
    if cut is not None:
        g.add(DashedLine(c + np.array([-radius * 1.5, 0, 0]), c + np.array([radius * 1.5, 0, 0]), color=LOST,
                         stroke_width=3).rotate(cut, about_point=c))
    return g


class Integration(VoiceoverScene):
    def construct(self):
        self.card()
        self.idea()
        self.compute_phi()
        self.table()
        self.critics()

    def card(self):
        card = chapter_card(7, r"Integrated information", r"Is consciousness what a system is, \ not what it does?",
                            lit={2004: r"Tononi", 2014: r"Oizumi, \ Albantakis \& Tononi", 2023: r"open letter"},
                            part=PART, scale=("mind", "brain"), marr=("what",))
        with self.voiceover("Chapter seven. Integrated information."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def idea(self):
        head = heading(r"Start from experience")
        boxes = VGroup()
        for name, txt in [(r"it exists", r"for itself"), (r"it is structured", r"many distinctions at once"),
                          (r"it is specific", r"this experience, \ not another"),
                          (r"it is unified", r"not two half-experiences"), (r"it is definite", r"of this, \ no more")]:
            box = RoundedRectangle(corner_radius=0.1, width=2.35, height=1.6, stroke_color=IIT, stroke_width=2,
                                   fill_color=BLACK, fill_opacity=0.5)
            boxes.add(VGroup(box, VGroup(label(name, font_size=20, color=IIT),
                                         label(txt, font_size=16, color=GREY_A)).arrange(DOWN, buff=0.15).move_to(box)))
        boxes.arrange(RIGHT, buff=0.15).move_to([0, 1.5, 0])
        rows = rows_of([
            (r"Tononi: \ take these as axioms, \ and ask what a physical system must be like to have them", WHITE),
            (r"the answer: \ it must have cause--effect power over itself that cannot be reduced to its parts; \ "
             r"$\Phi$ measures how much", IIT),
            (r"consciousness is then a property of the system's structure, \ not of what it computes or reports: \ "
             r"a system can be conscious and do nothing", MODEL),
        ], 12.0, 24, 0.34).move_to([0, -1.2, 0])
        tag = historical_tag(r"Tononi (2004); \ Oizumi, \ Albantakis \& Tononi (2014); \ Tononi et al.\ (2016)")
        with self.voiceover(
            "The second leading theory starts from the other end. <bookmark mark='a'/> Giulio Tononi's integrated "
            "information theory begins with what any experience is like: it exists for itself, it is structured, it "
            "is specific, it is unified, and it is definite. <bookmark mark='b'/> Then it asks what a physical system "
            "must be like to have those properties. The answer is that it must have cause-and-effect power over "
            "itself, as a whole, that can't be reduced to the power of its parts. A quantity called phi measures how "
            "much. <bookmark mark='c'/> On this view consciousness is a property of a system's causal structure, not "
            "of what it computes or reports. A system could be conscious while doing nothing at all, and a system "
            "that behaves just like us might not be."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.1) for b in boxes], lag_ratio=0.5), run_time=4)
            for m, r in zip("bc", rows[1:]):
                vo.wait_until(m)
                if m == "b":
                    self.play(FadeIn(rows[0]))
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def compute_phi(self):
        d = load("phi")
        head = heading(r"Derivation: \ $\Phi$ for a small network")
        ring = ring_picture(6, [-3.6, 0.3, 0], cut=0.0)
        eqs = VGroup(
            MathTex(r"\mathrm{EI}(A \to B) = I\big(A^{H_{\max}}_{t}\,;\, B_{t+1}\big)", font_size=34, color=IIT),
            MathTex(r"\Phi = \mathrm{EI}(A \to B) + \mathrm{EI}(B \to A) \ \text{at the weakest cut}", font_size=30,
                    color=WHITE),
        ).arrange(DOWN, buff=0.35).move_to([3.2, 1.6, 0])
        rows = rows_of([
            (r"perturb part A at random, \ every state equally likely, \ and measure how much B's next state "
             r"reveals about it: \ effective information", WHITE),
            (rf"try every way to cut the system in two \ ({d['n_bipartitions_6']} for six nodes) \ and keep the "
             r"cut that loses least, \ the minimum information bipartition", MODEL),
            (rf"a ring of six that passes its state along: \ the weakest cut crosses two links, \ "
             rf"{d['ring_ei_ab']:.0f} bit each way, \ $\Phi = {d['ring_ei_ab'] + d['ring_ei_ba']:.0f}$ bits", IIT),
        ], 6.0, 22, 0.3).move_to([3.3, -1.3, 0])
        tag = psyche_tag(r"\texttt{workspace.ei}, \ \texttt{phi}: \ Tononi's 2004 measure")
        with self.voiceover(
            "Here is phi, in the simplest of its versions, from Tononi's 2004 paper, computed by Psyche. "
            "<bookmark mark='a'/> Take a part A of a system and set it to random states, every state equally likely. "
            "Measure how much the next state of the rest, B, reveals about what A was. That's the effective "
            "information from A to B. <bookmark mark='b'/> Now try every way of cutting the system in two, thirty-one "
            "ways for six nodes, and find the cut across which the least information flows, relative to the size of "
            "the smaller part. Phi is the information that crosses that weakest cut, in both directions. "
            "<bookmark mark='c'/> For a ring of six nodes, each copying its neighbour, the weakest cut crosses two "
            "links, one bit flows each way, and phi is two bits. However you cut it, the ring is more than its "
            "halves."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(ring[:-1]))
            vo.wait_until("a")
            self.play(Write(eqs[0]), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(ring[-1]), Write(eqs[1]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def table(self):
        d = load("phi")
        head = heading(r"$\Phi$ for six small networks")
        rows_t = VGroup()
        for r in d["rows"]:
            col = IIT if r["phi"] > 0 else UNSEEN
            rows_t.add(VGroup(label(rf"{r['label']} \ ({r['n']} nodes)", font_size=24, color=WHITE),
                              label(rf"$\Phi = {r['phi']:.2f}$", font_size=26, color=col)).arrange(RIGHT, buff=0.6))
        for r in rows_t:
            r[1].shift(RIGHT * (7.2 - r[0].width - 0.6))
        rows_t.arrange(DOWN, aligned_edge=LEFT, buff=0.28).move_to([-1.4, 0.7, 0])
        foot = rows_of([
            (r"disconnected parts: \ zero, \ however busy each part is", UNSEEN),
            (r"this early measure gives a feed-forward chain some $\Phi$, \ and a ring of XOR gates none; \ the 2014 "
             r"and 2023 versions measure differently, \ and a feed-forward system has zero by construction", LOST),
            (r"for a real brain the number of cuts is astronomical: \ $\Phi$ cannot be computed, \ only "
             r"approximated", GREY_A),
        ], 12.2, 22, 0.25).to_edge(DOWN, buff=0.6)
        tag = psyche_tag(r"\texttt{workspace.phi}, \ \texttt{network}")
        with self.voiceover(
            "Here's the same measure for six small networks. <bookmark mark='a'/> Loops that aren't connected to "
            "each other have zero phi, however much each loop does: there's no single system there, just two. "
            "Rings have two bits; five nodes that each compute the OR of the others have less. "
            "<bookmark mark='b'/> But notice two oddities. This early measure gives a feed-forward chain some phi, "
            "and a ring of XOR gates none at all. The theory's later versions, from 2014 and 2023, measure "
            "differently, and in them a purely feed-forward system has zero phi by construction. The numbers depend "
            "on which version you compute. <bookmark mark='c'/> And for a real brain the number of cuts to try is "
            "astronomical, so phi can't be computed at all, only approximated."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rows_t], lag_ratio=0.4), FadeIn(foot[0]), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(foot[1]))
            vo.wait_until("c")
            self.play(FadeIn(foot[2]))
        self.clear_scene()

    def critics(self):
        head = heading(r"Predictions, \ and an open letter")
        rows = rows_of([
            (r"the seat of experience: \ a posterior hot zone of cortex, \ dense with recurrent connections; \ the "
             r"prefrontal cortex is not needed", IIT),
            (r"an inactive but well-connected cortex could still be conscious; \ a perfect simulation of a brain on a "
             r"conventional computer would not be", IIT),
            (r"Aaronson, \ 2014: \ a large grid of simple logic gates, \ doing nothing interesting, \ would have "
             r"enormous $\Phi$", LOST),
            (r"2023: \ an open letter signed by 124 researchers called the theory pseudoscience; \ many others "
             r"replied that the label was unwarranted", LOST),
            (r"what all agree: \ it makes bold predictions, \ and some of them have now been tested \ (chapter nine)",
             MODEL),
        ], 12.2, 24, 0.36).move_to([0, -0.2, 0])
        tag = published_tag(r"Tononi et al.\ (2016); \ Aaronson (2014); \ Fleming et al.\ (2023)")
        with self.voiceover(
            "Integrated information makes bold predictions. <bookmark mark='a'/> The seat of experience should be a "
            "posterior hot zone of cortex, rich in recurrent connections; the prefrontal cortex isn't needed. "
            "<bookmark mark='b'/> A well-connected cortex could be conscious while almost silent, and a perfect "
            "simulation of a brain on an ordinary computer would not be conscious, because its causal structure is "
            "the computer's, not the brain's. <bookmark mark='c'/> Critics find some consequences absurd. The computer "
            "scientist Scott Aaronson showed in 2014 that a large grid of simple logic gates, doing nothing "
            "interesting, would have enormous phi, and so on the theory a rich inner life. <bookmark mark='d'/> In "
            "2023 an open letter signed by a hundred and twenty-four researchers called the theory pseudoscience. "
            "Many others replied that the label was unwarranted. <bookmark mark='e'/> What everyone agrees on is that "
            "it makes risky predictions, and that some of them have now been tested against the workspace's."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
