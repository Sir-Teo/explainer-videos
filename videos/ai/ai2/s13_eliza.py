from __future__ import annotations

import textwrap

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai2.common import FAIL, FCOL, GCOST, HEUR, HIST, LEARN, MONO, PART, PATH, SYMBOL, load, node_box, said


class Eliza(VoiceoverScene):
    def construct(self):
        self.card()
        self.how()
        self.transcript()
        self.limits()
        self.effect()

    def card(self):
        card = chapter_card(12, r"ELIZA", r"How little does it take to seem to understand?", lit=(1966,), part=PART)
        with self.voiceover("Chapter twelve. ELIZA."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def how(self):
        hc = history_card(1966, r"Joseph Weizenbaum, MIT: \ \textit{ELIZA}, \textit{Communications of the ACM}",
                          r"keywords, \ decomposition patterns, \ reassembly rules; \ its DOCTOR script plays a "
                          r"psychotherapist who turns your words back into questions", width=7.0, color=HIST,
                          font_size=20).to_edge(UP, buff=0.3)
        inp = said("My mother takes care of me.", "user", chars=40, font_size=22).move_to([-4.0, 0.9, 0])
        sw = Text("YOUR MOTHER TAKES CARE OF YOU", font=MONO, font_size=20, color=WHITE).move_to([-4.0, -0.3, 0])
        swl = label(r"swap pronouns: \ my $\to$ your, \ me $\to$ you", font_size=20, color=GREY_A).next_to(sw, DOWN,
                                                                                                      buff=0.12)
        pat = VGroup(label(r"keyword MY \ (rank 2): \ pattern", font_size=20, color=FCOL),
                     Text("(0 YOUR 0 (/FAMILY) 0)", font=MONO, font_size=22, color=FCOL)).arrange(DOWN, buff=0.1)
        pat.move_to([2.6, 0.9, 0])
        parts = Text("1:''  2:YOUR  3:''  4:MOTHER  5:TAKES CARE OF YOU", font=MONO, font_size=18, color=GREY_A)
        parts.next_to(pat, DOWN, buff=0.2)
        reas = VGroup(Text("TELL ME MORE ABOUT YOUR FAMILY", font=MONO, font_size=18, color=GREY_B),
                      Text("WHO ELSE IN YOUR FAMILY 5", font=MONO, font_size=18, color=PATH),
                      Text("YOUR 4", font=MONO, font_size=18, color=GREY_B),
                      Text("WHAT ELSE COMES TO MIND WHEN YOU THINK OF YOUR 4", font=MONO, font_size=18,
                           color=GREY_B)).arrange(DOWN, buff=0.1, aligned_edge=LEFT).move_to([2.6, -1.4, 0])
        rl = label(r"reassembly rules, \ used in turn", font_size=20, color=GREY_A).next_to(reas, UP, buff=0.12)
        out = said("WHO ELSE IN YOUR FAMILY TAKES CARE OF YOU", "machine", chars=44, font_size=22).to_edge(DOWN,
                                                                                                     buff=0.3)
        script = VGroup(node_box(r"keywords, \ ranked", FCOL, font_size=26), node_box(r"decomposition patterns",
                                                                                     SYMBOL, font_size=26),
                        node_box(r"reassembly rules", PATH, font_size=26)).arrange(RIGHT, buff=0.8).move_to(DOWN * 0.6)
        script.add(*[Arrow(script[k].get_right(), script[k + 1].get_left(), buff=0.1, color=GREY_B) for k in range(2)])
        script.add(label(r"a script, \ such as DOCTOR:", font_size=26, color=GREY_A).next_to(script, UP, buff=0.4))
        arrows = VGroup(Arrow(inp.get_bottom(), sw.get_top(), buff=0.1, color=GREY_B, stroke_width=2),
                        Arrow(sw.get_right(), pat.get_left(), buff=0.15, color=GREY_B, stroke_width=2))
        with self.voiceover(
            "In 1966 Joseph Weizenbaum at MIT published a program that held conversations: ELIZA, named after the flower girl "
            "in Pygmalion. Its famous script, DOCTOR, plays a psychotherapist who turns your statements into questions. "
            "<bookmark mark='a'/> Type: my mother takes care of me. <bookmark mark='b'/> ELIZA swaps the pronouns, "
            "<bookmark mark='c'/> and finds its highest-ranked keyword, here my, with a pattern: anything, your, anything, a "
            "family word, anything. <bookmark mark='d'/> It takes the next of that pattern's reassembly rules, and splices the "
            "matched pieces in. <bookmark mark='e'/> Who else in your family takes care of you. No grammar, no meaning: pattern "
            "matching and a few hundred lines of script."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.2))
            self.play(FadeIn(script[5]), LaggedStart(*[FadeIn(script[k]) for k in (0, 3, 1, 4, 2)], lag_ratio=0.4),
                      run_time=3.0)
            vo.wait_until("a")
            self.play(FadeOut(script), run_time=0.5)
            self.play(FadeIn(inp))
            vo.wait_until("b")
            self.play(GrowArrow(arrows[0]), FadeIn(sw), FadeIn(swl))
            vo.wait_until("c")
            self.play(GrowArrow(arrows[1]), FadeIn(pat), FadeIn(parts))
            vo.wait_until("d")
            self.play(FadeIn(rl), FadeIn(reas))
            vo.wait_until("e")
            self.play(FadeIn(out, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def transcript(self):
        d = load("eliza")
        convo = d["convo"]
        n_same = d["matches"]
        diff = [c for c in convo if not c["same"]]

        def row(c):
            u = said(c["user"], "user", chars=40, font_size=17, max_lines=2)
            o = said(c["ours"], "machine", chars=40, font_size=17, max_lines=2)
            mark = MathTex(r"\checkmark" if c["same"] else r"\ne", font_size=30, color=PATH if c["same"] else FAIL)
            g = VGroup(u, o, mark)
            u.move_to(ORIGIN, aligned_edge=RIGHT).shift(LEFT * 0.25)
            o.move_to(ORIGIN, aligned_edge=LEFT).shift(RIGHT * 0.25)
            mark.next_to(o, RIGHT, buff=0.25)
            if not c["same"]:
                # Keep the quoted data verbatim, adding only visual line breaks.
                # Shrinking a full reply to one line made the comparison unreadable.
                original = "\n".join(textwrap.wrap(c["1966"], width=40, expand_tabs=False, replace_whitespace=False,
                                                drop_whitespace=False, break_long_words=False,
                                                break_on_hyphens=False))
                t = data_text(original, font=MONO, font_size=17, color=GREY_B, line_spacing=0.8)
                t.next_to(o, DOWN, buff=0.08, aligned_edge=LEFT)
                g.add(t)
            return g

        pages = [convo[:8], convo[8:]]
        head = VGroup(label(r"the user's lines, \ as printed in $1966$", font_size=22, color=C.USER),
                      label(r"our ELIZA's replies \ ($\checkmark$: \ the same as ELIZA's in $1966$)", font_size=22,
                            color=C.ASSISTANT))
        head[0].move_to([-3.4, 3.35, 0])
        head[1].move_to([3.6, 3.35, 0])
        blocks = []
        for pg in pages:
            rows = VGroup(*[row(c) for c in pg]).arrange(DOWN, buff=0.16)
            for r in rows:
                r.shift(RIGHT * (0 - (r[0].get_right()[0] + r[1].get_left()[0]) / 2))
            if rows.height > 6.1:
                rows.height = 6.1
            rows.next_to(head, DOWN, buff=0.25).set_x(0)
            for r in rows:
                r.shift(RIGHT * (0.0 - (r[0].get_right()[0] + r[1].get_left()[0]) / 2))
            blocks.append(rows)
        tag = note(rf"computed: \ our ELIZA, \ ${n_same}$ of ${len(convo)}$ replies identical").to_corner(DR, buff=0.12)
        if diff:
            why_ = ("The one difference is in the last line, where no keyword matches and ELIZA falls back on its "
                    "memory: both bring back the boyfriend, in different words." if len(diff) == 1 and
                    "BOYFRIEND" in diff[0]["ours"] and "BOYFRIEND" in diff[0]["1966"] else
                    f"{len(diff)} replies differ, where our short script has no rule like Weizenbaum's.")
        else:
            why_ = "Every reply matches."
        with self.voiceover(
            "Weizenbaum's paper printed a conversation with DOCTOR. We wrote a small ELIZA from the paper's description, with "
            "our own short script, and gave it the user's side, line by line. <bookmark mark='a'/> "
            f"{n_same} of its {len(convo)} replies come out word for word as in 1966. <bookmark mark='b'/> " + why_ + " Note the "
            "trick: when nothing matches, ELIZA brings back something you said earlier. It reads as attention, even memory."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            self.play(LaggedStart(*[FadeIn(r[0]) for r in blocks[0]], lag_ratio=0.15), run_time=2.0)
            self.play(LaggedStart(*[AnimationGroup(FadeIn(r[1]), FadeIn(r[2])) for r in blocks[0]], lag_ratio=0.25),
                      run_time=4.0)
            vo.wait_until("a")
            self.play(FadeOut(blocks[0], shift=UP * 0.3))
            self.play(LaggedStart(*[FadeIn(r[0]) for r in blocks[1]], lag_ratio=0.15), run_time=1.6)
            self.play(LaggedStart(*[AnimationGroup(*[FadeIn(m) for m in r[1:]]) for r in blocks[1]], lag_ratio=0.25),
                      run_time=3.5)
            vo.wait_until("b")
            self.play(Indicate(blocks[1][-1], color=FCOL, scale_factor=1.03))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def limits(self):
        d = load("eliza")
        pairs = d["new"]
        items = VGroup()
        for u, r in pairs:
            items.add(VGroup(said(u, "user", chars=46, font_size=18, max_lines=2),
                             said(r, "machine", chars=46, font_size=18, max_lines=3)).arrange(RIGHT, buff=0.35,
                                                                                            aligned_edge=UP))
        items.arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        if items.height > 6.0:
            items.height = 6.0
        if items.width > 13.2:
            items.width = 13.2
        items.move_to(DOWN * 0.4)
        top = label(r"new lines, \ typed to our ELIZA", font_size=28, color=GREY_A).to_edge(UP, buff=0.35)
        tag = note(r"computed: \ our ELIZA on new lines").to_corner(DR, buff=0.12)
        with self.voiceover(
            "Step outside the therapist's frame and the trick shows. <bookmark mark='a'/> Ask a fact, and it asks why you ask. "
            "Ask for a proof, and it hands your sentence back, pronouns turned around. Mention a computer, and a rule written "
            "for exactly that fires. Nothing is understood; the illusion lives in the reader."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(top))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(it, shift=UP * 0.1) for it in items], lag_ratio=0.4),
                      run_time=max(3.0, vo.duration - 3.0))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def effect(self):
        quote = label(r"Weizenbaum's secretary, who had watched him build it, \\ asked him to leave the room so she "
                      r"could talk to it in private", font_size=28, color=GREY_A).move_to(UP * 2.4)
        src = note(r"his account, \ \textit{Computer Power and Human Reason} (1976), \ paraphrased").next_to(quote, DOWN,
                                                                                                        buff=0.15)
        eff = definition_card(r"the ELIZA effect", r"reading understanding, \ even care, \ into a program's output "
                              r"because it uses our words", width=6.0, font_size=22, color=FCOL).move_to([-3.5, -1.5, 0])
        book = history_card(1976, r"Joseph Weizenbaum, \textit{Computer Power and Human Reason}",
                            r"the program's author, \ alarmed at how readily people confided in it", width=6.0,
                            color=HIST, font_size=21).move_to([-3.5, 0.45, 0])
        then = VGroup(
            history_card(2021, r"the original code found", r"in Weizenbaum's papers at MIT; \ run again on an "
                         r"emulated IBM 7094 in 2024", width=5.6, color=HIST, font_size=18),
            history_card(2025, r"Jones \& Bergen", r"a Python DOCTOR implementation: \ judged human $23\%$ of the "
                         r"time in five-minute Turing tests", width=5.6, color=SYMBOL, font_size=18),
        ).arrange(DOWN, buff=0.25).move_to([3.5, -0.55, 0])
        with self.voiceover(
            "What disturbed Weizenbaum was how people responded. <bookmark mark='a'/> In his 1976 book, Computer Power and Human "
            "Reason, he recalled his secretary, who had watched him write the program, asking him to leave the room so she could "
            "talk to it in private, and wrote that he had not imagined so short an exposure to so simple a program could produce "
            "such powerful delusions in normal people. <bookmark mark='b'/> Reading understanding into fluent output became "
            "known as the ELIZA effect. <bookmark mark='c'/> His original code was found at MIT in 2021 and run again in 2024. "
            "A separate Python implementation of the DOCTOR script was used in the 2025 Turing tests, and people took it for "
            "human in twenty-three percent of conversations. Does fluency mean "
            "understanding? Every chatbot raises the question again."
        ) as vo:
            self.play(FadeIn(book, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(quote), FadeIn(src))
            vo.wait_until("b")
            self.play(FadeIn(eff, shift=UP * 0.2))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.15) for c in then], lag_ratio=0.5))
        self.wait(0.3)
        self.clear_scene()
