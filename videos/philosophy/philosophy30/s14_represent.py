from __future__ import annotations

from videos.philosophy.philosophy30.common import *  # noqa: F403


class Represent(VoiceoverScene):
    def construct(self):
        card = chapter_card(13, r"Representation in networks", r"When does a direction in a network mean something?",
                            lit=(1998, 2018), part=PART)
        with self.voiceover("Chapter thirteen. Representation in networks."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.extended()
        self.shea()
        self.probe()
        self.lessons()

    def extended(self):
        head = label(r"Where the mind stops", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"Otto and Inga \ (1998)", r"Clark and Chalmers: \ Otto's notebook plays the role of Inga's memory \ "
                                        r"(Part 29)", FUNC),
            (r"the parity principle", r"if a process in the world does what we would call cognitive in the head, \ it "
                                      r"is cognitive", MIND),
            (r"the phone", r"always carried, \ automatically trusted, \ easily consulted: \ Clark and Chalmers's "
                           r"conditions, \ met daily", PHYS),
            (r"the model", r"a language model consulted like a notebook: \ does it extend the mind of its user?", SYM),
        ]
        g = rows_table(rows, top=1.6, gap=0.55)
        with self.voiceover(
            "If functionalism is right, minds are defined by roles, and roles need not stop at the skull. "
            "<bookmark mark='a'/>Part 29 met Otto, whose notebook plays the role that memory plays for Inga. "
            "<bookmark mark='b'/>Andy Clark and David Chalmers's parity principle: if a process in the world does "
            "what we would without hesitation call cognitive if it happened in the head, it is part of the cognitive "
            "process. <bookmark mark='c'/>Their conditions were that the resource be reliably available, "
            "automatically trusted and easily consulted, which a phone now meets for most people every day. "
            "<bookmark mark='d'/>A language model consulted the same way raises the same question. But first, a "
            "prior one: what is it for a network's internal state to represent anything?"
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def shea(self):
        hc = history_card(2018, r"Nicholas Shea", r"\textit{Representation in Cognitive Science}", width=6.4,
                          color=HIST).to_corner(UL, buff=0.3)
        rows = [
            (r"carried information", r"the state correlates with something in the world", SYM),
            (r"a task function", r"the system was trained, \ or selected, \ to achieve an outcome", FUNC),
            (r"exploitation", r"the system \textit{uses} the correlation to achieve it", OK),
            (r"varitel semantics", r"content is the correlation that explains the system's success at its task", GOAL),
        ]
        g = rows_table(rows, top=1.0, gap=0.5)
        with self.voiceover(
            "Nicholas Shea's book of 2018 combines Dretske and Millikan. <bookmark mark='a'/>A state carries "
            "information if it correlates with something in the world. <bookmark mark='b'/>The system has a task "
            "function: it was trained, or selected, to achieve some outcome. <bookmark mark='c'/>And the crucial "
            "condition: the system exploits the correlation to achieve it. <bookmark mark='d'/>The content of a "
            "representation is then the correlation that explains how the system succeeds. On this view, carrying "
            "information is not enough: the information must be used."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def probe(self):
        d = load("probe")
        head = label(r"Decodable is not used, \ built", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        rows_d = d["rows"]
        assert d["hidden"] == 32 and d["n_test"] == 2000 and len(rows_d) == 2
        assert rows_d[0]["probe_x"] == 1.0 and rows_d[0]["task_y"] == 1.0
        assert rows_d[1]["probe_x"] == 0.493 and rows_d[1]["task_y"] == 1.0
        net = VGroup()
        ins = VGroup(*[VGroup(Circle(radius=0.26, color=c), MathTex(t, font_size=24, color=c)) for t, c in
                       ((r"x", SYM), (r"y", FUNC))]).arrange(DOWN, buff=0.7).move_to([-5.4, 0.6, 0])
        hid = VGroup(*[Circle(radius=0.13, color=PHYS, fill_opacity=0.3) for _ in range(8)]).arrange(DOWN, buff=0.12
                                                                                                   ).move_to(
            [-3.6, 0.6, 0])
        out = VGroup(Circle(radius=0.26, color=FUNC), MathTex(r"\hat y", font_size=24, color=FUNC)).move_to(
            [-1.8, 0.6, 0])
        for c in ins:
            c[1].move_to(c[0])
        out[1].move_to(out[0])
        for a in ins:
            for h in hid:
                net.add(Line(a.get_right(), h.get_left(), color=GREY_D, stroke_width=0.8))
        for h in hid:
            net.add(Line(h.get_right(), out.get_left(), color=GREY_D, stroke_width=0.8))
        hl = label(r"32 hidden units \ $h = \mathrm{relu}(W[x, y] + b)$", font_size=16, color=PHYS).next_to(hid, DOWN,
                                                                                                         buff=0.2)
        hd = [r"", r"\text{probe reads } x", r"\text{network computes } y"]
        hd[0] = r"\text{directions removed}"
        cells = [[MathTex(str(r["removed"]), font_size=24), MathTex(f"{100 * r['probe_x']:.1f}\\%", font_size=24,
                                                                    color=SYM if r["probe_x"] > 0.9 else BAD),
                  MathTex(f"{100 * r['task_y']:.1f}\\%", font_size=24, color=OK)] for r in rows_d]
        grid = ValueGrid(hd, cells, col_w=[2.6, 2.4, 2.8], cell_h=0.55, font_size=18).move_to([3.0, 0.6, 0])
        foot = stack([(r"a linear probe reads $x$ off the hidden layer perfectly, \ though the output ignores $x$", SYM),
                      (r"remove the probe's direction: \ the probe falls to chance, \ the network is untouched", OK),
                      (r"amnesic probing \ (Elazar et al., \ 2021): \ information that is there is not thereby used",
                       GOAL)], font_size=20, aligned_edge=LEFT, width=12.0, buff=0.2).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The Reasoner builds the distinction. <bookmark mark='a'/>A small network takes two binary inputs, x and "
            "y, mixes them in thirty-two hidden units, and outputs y. It has no use for x. "
            "<bookmark mark='b'/>Train a linear probe to read x from the hidden layer, and it succeeds on all two "
            "thousand test cases: one hundred percent. The information about x is there. "
            "<bookmark mark='c'/>Now remove from the hidden layer the one direction the probe relied on, and train a "
            "fresh probe. It falls to chance, forty-nine percent. The network's output is untouched: still one "
            "hundred percent right about y. <bookmark mark='d'/>This is the idea behind amnesic probing, from Yanai "
            "Elazar and colleagues in 2021: information that can be decoded from a network is not thereby "
            "information the network uses. By Shea's standard, x is carried, but not represented."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(ins), FadeIn(hid), FadeIn(out), Create(net), FadeIn(hl))
            vo.wait_until("b")
            self.play(FadeIn(grid.head), Create(grid.rule), *[FadeIn(c) for c in grid.cell[0]], FadeIn(foot[0]))
            vo.wait_until("c")
            self.play(*[FadeIn(c) for c in grid.cell[1]], FadeIn(foot[1]))
            vo.wait_until("d")
            self.play(FadeIn(foot[2]))
        self.clear_scene()

    def lessons(self):
        head = label(r"What interpretability inherits", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"from Dretske", r"a feature direction carries information about inputs", SYM),
            (r"from Millikan and Shea", r"it represents only if the network's success depends on using it", FUNC),
            (r"from Searle", r"is any of this \textit{intrinsic} meaning, \ or only meaning to us?", BAD),
            (r"from Kim", r"if the weights do all the causing, \ do representations do any?", PHYS),
            (r"ahead", r"consciousness, \ Part 31; \ aligned systems, \ Part 42", GOAL),
        ]
        g = rows_table(rows, top=1.6, gap=0.45)
        with self.voiceover(
            "Interpretability research on neural networks inherits this whole part. <bookmark mark='a'/>From Dretske, "
            "the idea that a feature direction carries information about inputs. <bookmark mark='b'/>From Millikan "
            "and Shea, the requirement that it represents only if the network's success depends on using it, which is "
            "why ablation and intervention matter more than probes alone. <bookmark mark='c'/>From Searle, the "
            "question whether any of this is meaning the network has, or only meaning it has for us. "
            "<bookmark mark='d'/>And from Kim, the exclusion problem again: if the weights do all the causal work, do "
            "representations do any? <bookmark mark='e'/>Consciousness comes next, in Part 31; aligned systems at the "
            "end, in Part 42."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
