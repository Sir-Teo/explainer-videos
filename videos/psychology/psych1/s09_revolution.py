from __future__ import annotations

import numpy as np

from videos.psychology.psych1.common import *  # noqa: F403

OPS = (r"encode", r"store", r"compare", r"decide")
OP_COLOR = (SENSE, "#7BD88F", DISC, CHOOSE)


def op_box(text, color, font_size=28) -> VGroup:
    t = label(text, font_size=font_size, color=color)
    box = RoundedRectangle(width=t.width + 0.5, height=0.75, corner_radius=0.12, stroke_color=color, stroke_width=2,
                           fill_color=color, fill_opacity=0.12)
    t.move_to(box)
    return VGroup(box, t)


class Revolution(VoiceoverScene):
    def construct(self):
        self.card()
        self.machine()
        self.birthday()
        self.hick()
        self.name()

    def card(self):
        card = chapter_card(8, r"The mind comes back", r"What made it respectable to talk about what happens inside?",
                            lit={1948: r"Shannon's information", 1952: r"Hick's law", 1956: r"the cognitive "
                                 r"revolution", 1967: r"\emph{Cognitive Psychology}"},
                            part=PART, scale=("mind",), marr=("how",))
        with self.voiceover(
            "Chapter eight. The mind comes back."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    # ------------------------------------------------------------------
    def machine(self):
        bb = black_box(w=8.4, h=3.0).move_to([0, -0.4, 0])
        bb.inp.put_start_and_end_on(bb.box.get_left() + LEFT * 1.7, bb.box.get_left() + LEFT * 0.08)
        bb.out.put_start_and_end_on(bb.box.get_right() + RIGHT * 0.08, bb.box.get_right() + RIGHT * 1.7)
        bb[3].next_to(bb.inp, UP, buff=0.12)
        bb[4].next_to(bb.out, UP, buff=0.12)
        ops = VGroup(*[op_box(t, c) for t, c in zip(OPS, OP_COLOR)]).arrange(RIGHT, buff=0.55).move_to(bb.box)
        flows = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.06, color=GREY_B, stroke_width=3,
                               max_tip_length_to_length_ratio=0.35) for a, b in zip(ops, ops[1:])])
        machine = VGroup(label(r"the 1950s: \ a machine that", font_size=34, color=WHITE),
                         label(r"stores, \ retrieves, \ compares, \ decides", font_size=40, color=P.ACCENT))
        machine.arrange(DOWN, buff=0.18).to_edge(UP, buff=0.55)
        with self.voiceover(
            "What changed was a machine. By the nineteen-fifties there were computers. And a computer is a "
            "physical object, entirely mechanical, of which it makes perfect sense to say: it stores, it "
            "retrieves, it compares, it decides. Nobody calls that unscientific. <bookmark mark='a'/> So talk "
            "about what happens inside the box stopped sounding like mysticism, and started sounding like "
            "engineering. <bookmark mark='b'/> You could draw it: a box for each operation, and arrows for the "
            "flow of information between them."
        ) as vo:
            self.play(FadeIn(bb), FadeIn(machine[0]))
            self.play(FadeIn(machine[1], shift=UP * 0.15))
            vo.wait_until("a")
            self.play(bb.box.animate.set_fill("#101726").set_stroke(P.ACCENT))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(o, shift=RIGHT * 0.15) for o in ops], lag_ratio=0.4), run_time=2.5)
            self.play(LaggedStart(*[GrowArrow(f) for f in flows], lag_ratio=0.3), run_time=1.5)
        self.clear_scene()

    def paper(self, who, title, what, color):
        return history_card(who, title, what, color=color, width=4.25, font_size=22)

    def birthday(self):
        day = VGroup(label(r"11 September 1956", font_size=54, color=P.ACCENT),
                     label(r"a symposium on information theory, MIT", font_size=30, color=GREY_A))
        day.arrange(DOWN, buff=0.18).to_edge(UP, buff=0.5)
        papers = VGroup(
            self.paper(r"Newell \& Simon", r"the Logic Theory Machine", r"a program that proves theorems of logic",
                       "#7EC8F5"),
            self.paper(r"Chomsky", r"three models of language", r"a grammar that no chain of stimulus and response "
                       r"can produce", "#F28FB8"),
            self.paper(r"Miller", r"the bottleneck of memory", r"the limit of short-term memory: \ his "
                       r"``magical number seven'' appeared the same year", "#7BD88F"),
        ).arrange(RIGHT, buff=0.35, aligned_edge=UP).move_to([0, -0.35, 0])
        src = note(r"G. A. Miller, \emph{Trends in Cognitive Sciences} 7 (2003)").to_corner(DL, buff=0.3)
        hall = VGroup(*[little_person(0.55, color=GREY_C, fill=0.75) for _ in range(17)]).arrange(RIGHT, buff=0.22)
        hall = VGroup(hall, label(r"the symposium's audience", font_size=26, color=GREY_B))
        hall.arrange(DOWN, buff=0.2).move_to([0, -2.75, 0])
        with self.voiceover(
            "If you want a birthday, George Miller offered one: the eleventh of September, 1956, the second day "
            "of a symposium on information theory at MIT. <bookmark mark='a'/> That day Allen Newell and Herbert "
            "Simon presented a program that proved theorems of logic. <bookmark mark='b'/> Noam Chomsky presented "
            "a theory of grammar that no chain of stimulus and response could produce. <bookmark mark='c'/> And "
            "Miller himself talked about the bottleneck of short-term memory, the subject of his paper of the "
            "same year, The Magical Number Seven. <bookmark mark='d'/> A reasoning machine, a grammar, a memory "
            "limit. Three things inside the box, in one day."
        ) as vo:
            self.play(FadeIn(day, shift=UP * 0.2), FadeIn(src))
            self.play(FadeIn(hall[0], lag_ratio=0.08), FadeIn(hall[1]), run_time=2.0)
            for mark, pp in zip("abc", papers):
                vo.wait_until(mark)
                self.play(FadeIn(pp, shift=UP * 0.2))
            vo.wait_until("d")
            self.play(LaggedStart(*[pp.animate(rate_func=there_and_back).scale(1.05) for pp in papers],
                                 lag_ratio=0.3), run_time=2.0)
        self.clear_scene()

    def hick(self):
        d = load("hick")
        n, bits, pred = (np.asarray(d[k]) for k in ("n", "bits", "predicted"))
        table = VGroup()
        for k, b in ((2, 1), (4, 2), (8, 3)):
            dots = VGroup(*[Dot(radius=0.12, color=WHITE) for _ in range(k)]).arrange(RIGHT, buff=0.14)
            eq = MathTex(rf"\log_2 {k} = {b}\ \text{{bit{'s' if b > 1 else ''}}}", font_size=46, color=P.ACCENT)
            row = VGroup(dots, eq)
            dots.move_to([-1.6, 0, 0], aligned_edge=RIGHT)
            eq.move_to([-1.0, 0, 0], aligned_edge=LEFT)
            table.add(row)
        table.arrange(DOWN, buff=0.55).move_to([0, -0.2, 0])
        for row in table:
            row[0].set_x(-0.6 - row[0].width / 2)
            row[1].set_x(0.1 + row[1].width / 2)
        # Hick's apparatus in outline: lamps in a ring, one of them lit
        lamps = VGroup(*[Circle(radius=0.2, stroke_color=GREY_A, stroke_width=2, fill_color=GREY_D, fill_opacity=1)
                         .move_to(1.25 * np.array([np.cos(TAU * k / 8), np.sin(TAU * k / 8), 0])) for k in range(8)])
        lamps[2].set_fill(P.ACCENT)
        which = label(r"which lamp? \ three bits", font_size=28, color=GREY_A).next_to(lamps, DOWN, buff=0.3)
        lamp_pic = VGroup(lamps, which).move_to([-3.6, -0.4, 0])
        rate = VGroup(MathTex(r"\text{time to choose}", r"=", r"a", r"+", r"\frac{\text{bits}}{\text{rate}}",
                              font_size=46),
                      label(r"a steady rate of gaining information", font_size=28, color=GREY_A))
        rate.arrange(DOWN, buff=0.35).move_to([2.7, -0.3, 0])
        rate[0][4].set_color(P.ACCENT)
        t_head = label(r"Shannon, 1948: \ information, in yes-or-no questions", font_size=34).to_edge(UP, buff=0.5)
        ask = label(r"?", font_size=96, color=WHITE)
        yes, no = label(r"yes", font_size=44, color=P.SIGNAL), label(r"no", font_size=44, color=P.ERR)
        yes.move_to([2.3, 0.75, 0])
        no.move_to([2.3, -0.75, 0])
        fork = VGroup(*[Arrow(ask.get_right() + RIGHT * 0.2, t.get_left() + LEFT * 0.15, buff=0, color=GREY_B,
                              stroke_width=4, max_tip_length_to_length_ratio=0.15) for t in (yes, no)])
        one = label(r"one answer $=$ one bit", font_size=44, color=P.ACCENT).move_to([5.2, 0, 0])
        question = VGroup(ask, fork, yes, no, one).move_to([0, -0.3, 0])
        hyp = label(r"Hick, 1952: \ people take in information at a steady rate", font_size=34, color=P.ACCENT)
        hyp.to_edge(UP, buff=0.5)
        lo, hi = float(pred.min()) - 8, float(pred.max()) + 8
        A1 = axes([0.5, 10.5], [lo, hi], x_length=5.6, y_length=4.1, xlabel=r"number of alternatives",
                  ylabel=r"choice time (ms)", xticks=[1, 2, 4, 6, 8, 10], yticks=[240, 260, 280, 300],
                  center=[-3.5, -0.55, 0])
        A2 = axes([-0.2, 3.5], [lo, hi], x_length=5.6, y_length=4.1, xlabel=r"bits: \ $\log_2$ of the number",
                  xticks=[0, 1, 2, 3], yticks=[240, 260, 280, 300], center=[3.6, -0.55, 0])
        xs = np.linspace(1, 10, 100)
        c1 = curve(A1.ax, xs, d["base"] + d["per_bit"] * np.log2(xs), P.PSYCHE, 4)
        c2 = Line(A2.ax.c2p(0, pred[0]), A2.ax.c2p(bits[-1], pred[-1]), color=P.PSYCHE, stroke_width=4)
        p1 = VGroup(*[Dot(A1.ax.c2p(x, y), radius=0.06, color=P.PSYCHE) for x, y in zip(n, pred)])
        p2 = VGroup(*[Dot(A2.ax.c2p(x, y), radius=0.06, color=P.PSYCHE) for x, y in zip(bits, pred)])
        h1 = VGroup(*[Dot(A1.ax.c2p(x, y), radius=0.1, color=P.HUMAN) for x, y in ((1, d["base"]),
                                                                                    (d["donders_n"], d["donders_b"]))])
        h2 = VGroup(*[Dot(A2.ax.c2p(x, y), radius=0.1, color=P.HUMAN) for x, y in
                      ((0, d["base"]), (np.log2(d["donders_n"]), d["donders_b"]))])
        leg = legend([(P.HUMAN, r"Donders' two means, 1868"),
                      (P.PSYCHE, rf"Psyche: \ ${d['per_bit']:.0f}$ ms a bit, a prediction")], font_size=22)
        leg.next_to(A1.ax.c2p(3.2, lo + 30), RIGHT, buff=0.0)
        law = MathTex(r"\text{RT}", r"=", r"a", r"+", r"b\,\log_2 n", font_size=40, color=P.ACCENT)
        law.next_to(A2.ax.c2p(0.1, hi - 6), RIGHT, buff=0.0)
        tag = psyche_tag(r"a prediction, fixed by two of Donders' numbers; \ tested in Part 25")
        with self.voiceover(
            "The same years supplied a unit. Claude Shannon's theory of communication measures information in "
            "bits: one bit for each yes-or-no question you need answered. <bookmark mark='a'/> A choice between "
            "two things is one bit. Among four, two bits. Among eight, three. The logarithm of the number of "
            "alternatives. <bookmark mark='b'/> In 1952 William Hick put that together with Donders' discovery. "
            "Suppose a person takes in information at a steady rate. Then the time to choose should grow with "
            "the bits: with the logarithm of the number of alternatives, not with the number itself. "
            "<bookmark mark='c'/> Here's what that predicts for Psyche, with the rate set from Donders' own two "
            f"numbers: about {d['per_bit']:.0f} milliseconds a bit, for a task as natural as repeating a "
            "syllable. Against the number of alternatives, the line bends. <bookmark mark='d'/> Against bits, "
            "it's straight. <bookmark mark='e'/> That is Hick's law. It has held up in experiment after "
            "experiment, and Part 25 derives it from a model of how a decision gets made."
        ) as vo:
            self.play(FadeIn(t_head))
            self.play(FadeIn(ask), LaggedStart(*[GrowArrow(f) for f in fork], lag_ratio=0.3), FadeIn(yes), FadeIn(no))
            self.play(FadeIn(one, shift=LEFT * 0.15))
            vo.wait_until("a")
            self.play(FadeOut(question))
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in table], lag_ratio=0.7), run_time=5.0)
            vo.wait_until("b")
            self.play(FadeOut(table), ReplacementTransform(t_head, hyp))
            self.play(FadeIn(lamp_pic, shift=UP * 0.15))
            self.play(Write(rate[0]), FadeIn(rate[1]))
            for k in (5, 0, 6, 3):
                self.play(*[lamps[j].animate.set_fill(P.ACCENT if j == k else GREY_D) for j in range(8)],
                          run_time=0.5)
            vo.wait_until("c")
            self.play(FadeOut(lamp_pic), FadeOut(rate))
            self.play(FadeIn(A1), FadeIn(tag))
            self.play(GrowFromCenter(h1[0]), GrowFromCenter(h1[1]))
            self.play(Create(c1), FadeIn(p1, lag_ratio=0.1), FadeIn(leg), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(A2))
            self.play(ReplacementTransform(p1.copy(), p2), ReplacementTransform(h1.copy(), h2), run_time=2.0)
            self.play(Create(c2))
            vo.wait_until("e")
            self.play(Write(law))
        self.clear_scene()

    def name(self):
        book = history_card(1967, r"Ulric Neisser", r"\emph{Cognitive Psychology}: \ the field gets its textbook, "
                            r"and its name", color=P.ARCHIVE, width=7.6, font_size=30).to_edge(UP, buff=0.5)
        ops = VGroup(*[op_box(t, c, 32) for t, c in zip(OPS, OP_COLOR)]).arrange(RIGHT, buff=0.6)
        flows = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.06, color=GREY_B, stroke_width=3,
                               max_tip_length_to_length_ratio=0.35) for a, b in zip(ops, ops[1:])])
        row = VGroup(ops, flows).scale(1.25).move_to([0, -0.6, 0])
        q = label(r"A real mechanism, \ or a label on something we don't understand?", font_size=34, color=KANT)
        q.to_edge(DOWN, buff=0.7)
        who = little_person(0.5, color=KANT).move_to(ops[2][0]).shift(UP * 0.85)
        between = VGroup(label(r"stimulus", font_size=38), MathTex(r"\longrightarrow", font_size=50, color=GREY_B),
                         label(r"what happens in between", font_size=42, color=P.ACCENT),
                         MathTex(r"\longrightarrow", font_size=50, color=GREY_B),
                         label(r"response", font_size=38, color=P.RESP)).arrange(RIGHT, buff=0.4)
        between.move_to([0, -0.6, 0])
        with self.voiceover(
            "By 1967 the new field had a textbook, and the textbook gave it a name: cognitive psychology. <bookmark mark='z'/> The "
            "study of what happens between the stimulus and the response. <bookmark mark='a'/> But notice what "
            "the revolution did not settle. Boxes and arrows are easy to draw. <bookmark mark='b'/> How do you "
            "know there's really a compare operation in there, and not just a label for something you don't "
            "understand? Who is doing the comparing? <bookmark mark='c'/> Answering that takes two more ideas, "
            "and they're the next two chapters."
        ) as vo:
            self.play(FadeIn(book, shift=UP * 0.2))
            vo.wait_until("z")
            self.play(FadeIn(between, shift=UP * 0.15))
            vo.wait_until("a")
            self.play(FadeOut(between), FadeIn(row))
            vo.wait_until("b")
            self.play(Indicate(ops[2], color=WHITE, scale_factor=1.15), FadeIn(who, shift=DOWN * 0.2))
            self.play(FadeIn(q, shift=UP * 0.15))
        self.clear_scene()
