from __future__ import annotations

from videos.philosophy.philosophy28.common import *  # noqa: F403


class Acts(VoiceoverScene):
    def construct(self):
        card = chapter_card(7, r"Doing things with words", r"Is every sentence true or false?", lit=(1962, 1969),
                            part=PART)
        with self.voiceover("Chapter seven. Doing things with words."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.performatives()
        self.layers()
        self.taxonomy()

    def performatives(self):
        hc = history_card(1962, r"J. L. Austin", r"\textit{How to Do Things with Words} \ (William James lectures, 1955)",
                          width=7.4, color=HIST).to_corner(UL, buff=0.3)
        ex = stack([(r"`I name this ship the \textit{Queen Elizabeth}.'", WORD),
                    (r"`I do.' \ (in a wedding)", WORD), (r"`I bet you sixpence it will rain tomorrow.'", WORD)],
                   font_size=24, aligned_edge=LEFT, buff=0.25).move_to([-2.6, 0.8, 0])
        ex_tag = label(r"not true or false: \ saying it \textit{is} doing it", font_size=21, color=USE).next_to(
            ex, DOWN, buff=0.3).align_to(ex, LEFT)
        hd = [r"\text{felicity condition}", r"\text{if it fails}"]
        cells = [[label(r"an accepted procedure, \ the right persons", font_size=19), label(r"a misfire: \ void", font_size=19, color=BAD)],
                 [label(r"carried out correctly and completely", font_size=19), label(r"a misfire", font_size=19, color=BAD)],
                 [label(r"the right thoughts and intentions", font_size=19), label(r"an abuse: \ insincere", font_size=19,
                                                                                    color=USE)]]
        grid = ValueGrid(hd, cells, col_w=[5.6, 3.0], cell_h=0.5, font_size=20).move_to([2.0, -2.0, 0])
        with self.voiceover(
            "J. L. Austin, lecturing at Harvard in 1955, noticed sentences that do not describe anything. "
            "<bookmark mark='a'/>I name this ship the Queen Elizabeth, said while smashing a bottle against the bow. "
            "I do, said in a wedding. I bet you sixpence it will rain tomorrow. <bookmark mark='b'/>None of these is "
            "true or false. To say it, in the right circumstances, is to do it: to name, to marry, to bet. He called "
            "them performatives. <bookmark mark='c'/>Instead of truth they have felicity conditions. There must be an "
            "accepted procedure, invoked by the right persons; if not, the act misfires and is void. It must be "
            "carried out correctly and completely. And the participants must have the right thoughts and intentions; "
            "a promise you do not mean to keep is not void, but an abuse."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(e) for e in ex], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(FadeIn(ex_tag))
            vo.wait_until("c")
            self.play(FadeIn(grid.head), Create(grid.rule))
            for r in range(len(cells)):
                self.play(*[FadeIn(c) for c in grid.cell[r]], run_time=0.5)
        self.clear_scene()

    def layers(self):
        head = label(r"Three acts in one utterance", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        said = label(r"`Shoot her!'", font_size=34, color=WORD).move_to([0, 2.0, 0])
        levels = [(r"locutionary", r"saying `shoot her', \ meaning by `shoot' shoot and referring by `her' to her",
                   WORD), (r"illocutionary", r"in saying it, \ urging, \ advising or ordering me to shoot her", USE),
                  (r"perlocutionary", r"by saying it, \ persuading me to shoot her, \ or frightening me", HEAR)]
        bands = VGroup()
        for i, (a, b, c) in enumerate(levels):
            box = RoundedRectangle(width=11.6, height=0.95, corner_radius=0.12, color=c, fill_opacity=0.08).move_to(
                [0, 0.6 - 1.15 * i, 0])
            t = VGroup(label(a, font_size=23, color=c), label(b, font_size=20)).arrange(RIGHT, buff=0.5).move_to(box)
            bands.add(VGroup(box, t))
        foot = label(r"Austin's discovery: \ every utterance has a force, \ even a statement", font_size=22,
                     color=GOAL).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Austin then dissolved his own distinction. <bookmark mark='a'/>Take an utterance: shoot her! "
            "<bookmark mark='b'/>The locutionary act is saying those words with their meaning: shoot meaning shoot, "
            "her referring to her. <bookmark mark='c'/>The illocutionary act is what is done in saying them: urging, "
            "advising, or ordering me to shoot her. <bookmark mark='d'/>The perlocutionary act is what is brought "
            "about by saying them: persuading me to shoot her, or frightening me. <bookmark mark='e'/>Every "
            "utterance has all three layers. Even a plain statement is an act, with a force; describing the world is "
            "one thing among many that words do."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(said))
            for mk, b in zip("bcd", bands):
                vo.wait_until(mk)
                self.play(FadeIn(b))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()

    def taxonomy(self):
        head = label(r"Searle's taxonomy", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        hd = [r"\text{class}", r"\text{example}", r"\text{direction of fit}"]
        rows = [(r"assertives", r"`it is raining'", r"words to world: \ $\downarrow$ fit the facts", WORD),
                (r"directives", r"`close the door'", r"world to words: \ the hearer is to make it so", USE),
                (r"commissives", r"`I promise to come'", r"world to words: \ the speaker is to make it so", HEAR),
                (r"expressives", r"`thank you'", r"none: \ the fit is presupposed", RULE_C),
                (r"declarations", r"`you're fired'", r"both: \ saying it makes it so", TRUTH)]
        cells = [[label(a, font_size=20, color=c), label(b, font_size=20), label(d_, font_size=19, color=GREY_A)]
                 for a, b, d_, c in rows]
        grid = ValueGrid(hd, cells, col_w=[2.8, 3.4, 5.8], cell_h=0.52, font_size=21).move_to([0, 0.4, 0])
        foot = stack([(r"Searle \ (1975): \ five basic things we do with sentences", HIST),
                      (r"indirect speech acts: \ `can you pass the salt?' \ is a question in form, \ a request in force",
                       GOAL)], font_size=21, aligned_edge=LEFT, width=12.0, buff=0.22).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "John Searle, Austin's student, systematized the forces in 1975. <bookmark mark='a'/>Assertives, like it "
            "is raining, aim to fit the world: words to world. <bookmark mark='b'/>Directives, like close the door, "
            "aim to make the world fit the words, by the hearer's action. <bookmark mark='c'/>Commissives, like a "
            "promise, do the same by the speaker's action. <bookmark mark='d'/>Expressives, like thank you, have no "
            "direction of fit: they presuppose it. <bookmark mark='e'/>And declarations, like you're fired, make it "
            "so by saying it: both directions at once. <bookmark mark='f'/>Searle also studied indirect speech acts. "
            "Can you pass the salt is a question in form and a request in force. Explaining how a hearer gets from "
            "one to the other is the work of the next chapter."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), Create(grid.rule))
            for mk, r in zip("abcde", range(5)):
                vo.wait_until(mk)
                self.play(*[FadeIn(c) for c in grid.cell[r]])
            self.play(FadeIn(foot[0]))
            vo.wait_until("f")
            self.play(FadeIn(foot[1]))
        self.clear_scene()
