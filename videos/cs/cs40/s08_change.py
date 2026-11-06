from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs40.common import (DATA, HEAD, KERN, LAM, NO, PART, YES, axes, code_block, load, trace)

RC = {"0.0": NO, "0.1": HEAD, "0.2": YES, "0.3": LAM}


class Change(VoiceoverScene):
    def construct(self):
        self.card()
        self.refactoring()
        self.debt()
        self.evidence()

    def card(self):
        card = chapter_card(7, r"Changing code that works", r"How do you improve code without breaking it?",
                            lit=(1992, 2016), extra=((1992, r"Opdyke: \ refactoring; \ Cunningham: \ technical debt"),
                                                     (2004, r"Feathers: \ legacy code"),
                                                     (2016, r"Menzies et al.: \ the cost of delay")), part=PART)
        with self.voiceover("Chapter seven. Changing code that works."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def refactoring(self):
        head = label(r"Refactoring", font_size=36).to_edge(UP, buff=0.3)
        before = code_block([
            "def price(order):",
            "    t = 0",
            "    for i in order.items:",
            "        t += i.qty * i.unit",
            "    if order.customer.vip:",
            "        t *= 0.9",
            "    return round(t, 2)",
        ], size=16)
        after = code_block([
            "def subtotal(order):",
            "    return sum(i.qty * i.unit for i in order.items)",
            "",
            "def discount(customer):",
            "    return 0.9 if customer.vip else 1.0",
            "",
            "def price(order):",
            "    return round(subtotal(order) * discount(order.customer), 2)",
        ], size=16)
        pair = VGroup(before, after).arrange(RIGHT, buff=0.8, aligned_edge=UP).next_to(head, DOWN, buff=0.5)
        arrow = Arrow(before.get_right(), after.get_left(), buff=0.1, color=YES, stroke_width=3)
        arrow.set_y(pair.get_y())
        al = label(r"extract function, \ twice", font_size=17, color=YES).next_to(arrow, UP, buff=0.05)
        lines = VGroup(
            wrapped_label(r"\textbf{refactoring} \ (Opdyke, 1992; \ Fowler, 1999): \ a change of structure that "
                          r"provably preserves behaviour, \ in small named steps \ (extract function, \ rename, \ "
                          r"move, \ inline)", 12.4, font_size=21, color=WHITE),
            wrapped_label(r"\textbf{characterization tests} \ (Feathers, 2004): \ before touching code nobody "
                          r"understands, \ record what it does now, \ right or wrong, \ and keep that fixed", 12.4,
                          font_size=21, color=HEAD),
            wrapped_label(r"\textbf{code smells}: \ long functions, \ duplicated logic, \ a class that knows "
                          r"everyone: \ symptoms, \ not proofs", 12.4, font_size=21, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Most of a programmer's working life is spent changing code that already works. "
            "<bookmark mark='a'/> William Opdyke's thesis of 1992 defined refactorings: changes of structure that "
            "provably preserve behaviour, done in small named steps. Here a price calculation is split by extracting "
            "two functions. Nothing a caller can observe has changed; the next change, a new kind of discount, now "
            "touches one small function. <bookmark mark='b'/> For code nobody understands, Michael Feathers' first "
            "step is to write characterization tests: record what the code does now, right or wrong, and keep that "
            "fixed while you restructure. <bookmark mark='c'/> Code smells, long functions, duplicated logic, a "
            "class that knows about everything, are hints of where to start; they are symptoms, not proofs."
        ) as vo:
            self.play(FadeIn(head), FadeIn(before))
            vo.wait_until("a")
            self.play(GrowArrow(arrow), FadeIn(al), FadeIn(after), FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(FadeIn(lines[2]))
        self.wait(0.4)
        self.clear_scene()

    def debt(self):
        d = load("debt")
        head = label(r"Technical debt, \ as a model", font_size=36).to_edge(UP, buff=0.3)
        top = max(v[-1]["delivered"] for v in d.values())
        g = axes([0, 104, 26], [0, top * 1.05, 200], x_length=6.6, y_length=3.8, x_label=r"weeks",
                 y_label=r"features delivered", xticks=(0, 26, 52, 78, 104), yticks=range(200, int(top) + 1, 200)
                 ).move_to([-2.8, -0.5, 0])
        ax = g.ax
        curves = {k: trace(ax, [(r["week"], r["delivered"]) for r in v], RC[k], width=3) for k, v in d.items()}
        leg = VGroup(*[label(rf"refactor {float(k) * 100:.0f}\% of the time: \ {v[-1]['delivered']:.0f}",
                             font_size=19, color=RC[k]) for k, v in d.items()]).arrange(DOWN, aligned_edge=LEFT,
                                                                                         buff=0.14)
        leg.move_to([4.0, 1.4, 0])
        notes = VGroup(
            wrapped_label(r"every careless feature adds debt; \ debt slows all later work \ (the interest); \ "
                          r"refactoring pays it back", 5.2, font_size=19, color=GREY_A),
            wrapped_label(r"never refactoring wins the first quarter and loses the second year; \ refactoring too "
                          r"much also loses", 5.2, font_size=19, color=HEAD),
            wrapped_label(r"a model of Ward Cunningham's metaphor \ (1992), \ not data: \ the shape is the lesson, \ "
                          r"the numbers are ours", 5.2, font_size=19, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([4.0, -1.3, 0])
        with self.voiceover(
            "Ward Cunningham compared shipping code you know is not right to borrowing money. "
            "<bookmark mark='a'/> We turned the metaphor into a small model. A team ships ten points of features a "
            "week on clean code. Every feature shipped in haste adds debt, and debt slows all later work: that is "
            "the interest. Time spent refactoring pays it back. <bookmark mark='b'/> A team that never refactors is "
            "ahead after a quarter and far behind after two years, crawling at a third of its first speed. Spending "
            "a fifth of the time on cleanup delivers the most. Spending more also loses. <bookmark mark='c'/> This "
            "is a model of a metaphor, not data. The shape is the lesson: debt is a loan, and like a loan it can be "
            "worth taking, if you know the rate and plan to repay."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g), FadeIn(notes[0]))
            vo.wait_until("a")
            self.play(Create(curves["0.0"]), FadeIn(leg[0]), run_time=2)
            vo.wait_until("b")
            self.play(*[Create(curves[k]) for k in ("0.1", "0.2", "0.3")], *[FadeIn(x) for x in leg[1:]],
                      FadeIn(notes[1]), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    def evidence(self):
        head = label(r"How much does a late fix cost?", font_size=36).to_edge(UP, buff=0.3)
        lines = VGroup(
            wrapped_label(r"the textbook curve: \ a defect fixed in production costs 100 times one fixed in "
                          r"design \ (Boehm, 1970s--80s, \ from a few large government projects)", 12.4,
                          font_size=23, color=NO),
            wrapped_label(r"Menzies, Nichols, Shull and Layman \ (2016): \ 171 projects, \ tens of thousands of "
                          r"issues: \ \textbf{no} such effect in modern development; \ the time to fix did not grow "
                          r"with the phase", 12.4, font_size=23, color=YES),
            wrapped_label(r"Bossavit, \ \textit{The Leprechauns of Software Engineering} \ (2015): \ several "
                          r"famous figures, \ traced back, \ rest on very little", 12.4, font_size=23, color=HEAD),
            wrapped_label(r"the habit to keep: \ ask for the data behind a claim about software, \ as we did for "
                          r"Brooks' law", 12.4, font_size=23, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(head, DOWN, buff=0.6)
        with self.voiceover(
            "Much of what the field knows about change rests on surprisingly little. <bookmark mark='a'/> A famous "
            "curve says a defect fixed in production costs a hundred times as much as one fixed in design. It goes "
            "back to Barry Boehm's data from a few large projects of the nineteen seventies. "
            "<bookmark mark='b'/> In 2016 Tim Menzies and colleagues looked at a hundred and seventy-one modern "
            "projects and found no such effect: the effort to fix an issue did not grow with the phase in which it "
            "was found. <bookmark mark='c'/> Laurent Bossavit traced several of the field's most quoted numbers back "
            "to their sources and found very little underneath. <bookmark mark='d'/> The habit to keep is to ask for "
            "the data behind any claim about how software is built, including the claims in this part."
        ) as vo:
            self.play(FadeIn(head))
            for mk, l in zip("abcd", lines):
                vo.wait_until(mk)
                self.play(FadeIn(l))
        self.wait(0.4)
        self.clear_scene()


_ = (DATA, KERN)
