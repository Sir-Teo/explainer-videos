from __future__ import annotations

from videos.philosophy.philosophy29.common import *  # noqa: F403


class Habermas(VoiceoverScene):
    def construct(self):
        card = chapter_card(13, r"Reason in communication", r"What do we commit ourselves to when we argue?",
                            lit=(1947, 1981), part=PART)
        with self.voiceover("Chapter thirteen. Reason in communication."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.frankfurt()
        self.claims()
        self.ideal()
        self.critics()

    def frankfurt(self):
        hc = history_card(1947, r"Max Horkheimer and Theodor Adorno", r"\textit{Dialectic of Enlightenment}",
                          width=7.0, color=HIST).to_corner(UL, buff=0.3)
        rows = [
            (r"critical theory", r"Horkheimer \ (1937): \ theory that aims not only to describe society but to free "
                                 r"people within it", SIGN),
            (r"the dialectic", r"enlightenment, \ meant to free us from myth, \ reverts to myth: \ reason becomes "
                               r"instrumental, \ a tool for domination", BAD),
            (r"the culture industry", r"mass culture as standardized product, \ producing conformity", OBJ),
            (r"Marcuse \ (1964)", r"\textit{One-Dimensional Man}: \ a society that absorbs its own opposition", ACT),
        ]
        g = rows_table(rows, top=0.9, gap=0.5)
        with self.voiceover(
            "The Frankfurt school began at the Institute for Social Research, founded in 1923. "
            "<bookmark mark='a'/>Its director, Max Horkheimer, called its programme critical theory: theory that "
            "aims not only to describe society but to free the people in it. <bookmark mark='b'/>In exile in "
            "America during the war, Horkheimer and Theodor Adorno wrote Dialectic of Enlightenment, published in "
            "1947. Enlightenment, meant to free us from myth, reverts to myth: reason shrinks to instrumental "
            "reason, a tool for controlling nature and people, blind to ends. <bookmark mark='c'/>Its emblem is the "
            "culture industry, mass culture as a standardized product that produces conformity. "
            "<bookmark mark='d'/>Herbert Marcuse, in 1964, described a one-dimensional society that absorbs even its "
            "own opposition."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def claims(self):
        hc = history_card(1981, r"J\"urgen Habermas", r"\textit{The Theory of Communicative Action}", width=6.8,
                          color=HIST).to_corner(UL, buff=0.3)
        utt = VGroup(RoundedRectangle(width=4.6, height=0.8, corner_radius=0.15, color=WHITE),
                     label(r"`The window is open, \ please close it.'", font_size=20, color=WHITE)).move_to([0, 0.9, 0])
        claims = [(r"truth", r"the objective world: \ is it open?", WORLD, [-4.4, -1.0]),
                  (r"rightness", r"the social world: \ may you ask me?", SIGN, [0, -1.4]),
                  (r"sincerity", r"the subjective world: \ do you mean it?", BODY, [4.4, -1.0])]
        boxes, arrows = VGroup(), VGroup()
        for n, d, c, (x, y) in claims:
            b = VGroup(label(n, font_size=22, color=c), label(d, font_size=17, color=GREY_A)).arrange(DOWN,
                                                                                                buff=0.12)
            b.move_to([x, y, 0])
            boxes.add(b)
            arrows.add(Arrow(utt.get_bottom(), b.get_top(), buff=0.12, color=c, stroke_width=2.5))
        foot = stack([(r"communicative action aims at understanding; \ strategic action, \ at success", ACT),
                      (r"every claim can be challenged, \ and must then be redeemed with reasons", GOAL)],
                     font_size=20, buff=0.2).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Jürgen Habermas, once Adorno's assistant and later Horkheimer's successor, looked for a reason that was not "
            "merely "
            "instrumental, and found it in communication. His Theory of Communicative Action appeared in 1981. "
            "<bookmark mark='a'/>Take an ordinary request: the window is open, please close it. "
            "<bookmark mark='b'/>In saying it, a speaker raises three validity claims at once: a claim to truth, "
            "about the objective world, that the window is open; <bookmark mark='c'/>a claim to rightness, about the "
            "social world, that this is a request I may make of you; <bookmark mark='d'/>and a claim to sincerity, "
            "about the speaker's own world, that I mean it. It builds on the speech acts of Part 28. "
            "<bookmark mark='e'/>Action oriented to understanding, which relies on such claims, Habermas calls "
            "communicative; action oriented only to success, strategic. <bookmark mark='f'/>Any claim can be "
            "challenged, and then must be redeemed with reasons, or withdrawn."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(utt))
            for mk, i in zip("bcd", range(3)):
                vo.wait_until(mk)
                self.play(GrowArrow(arrows[i]), FadeIn(boxes[i]))
            vo.wait_until("e")
            self.play(FadeIn(foot[0]))
            vo.wait_until("f")
            self.play(FadeIn(foot[1]))
        self.clear_scene()

    def ideal(self):
        head = label(r"The ideal speech situation", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rules = stack([(r"1. \ everyone who can speak and act may take part", WHITE),
                       (r"2. \ everyone may question any assertion, \ and introduce any assertion", WHITE),
                       (r"3. \ everyone may express attitudes, \ desires and needs", WHITE),
                       (r"4. \ no one may be prevented, \ by coercion inside or outside, \ from using these rights",
                        WHITE)], font_size=21, aligned_edge=LEFT, width=11.0, buff=0.25).move_to([0, 1.0, 0])
        d_tex = MathTex(r"\text{(D)}\quad", r"\text{a norm is valid only if all affected could agree to it, \ as "
                                            r"participants in a practical discourse}", font_size=26).move_to([0, -1.1, 0])
        d_tex[0].set_color(GOAL)
        d_tex[1].set_color(SIGN)
        foot = stack([(r"not a description of real talk, \ but what arguing commits us to presupposing", ACT),
                      (r"democracy as deliberation: \ Part 39", GOAL)], font_size=20, buff=0.2).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "What does arguing commit us to? <bookmark mark='a'/>Following Robert Alexy, Habermas lists the rules of "
            "an ideal speech situation. Everyone who can speak and act may take part. Everyone may question any "
            "assertion, and introduce any assertion. Everyone may express attitudes, desires and needs. And no one "
            "may be prevented, by coercion from inside or outside the discourse, from using these rights. "
            "<bookmark mark='b'/>From this comes the principle of discourse ethics: a norm is valid only if all "
            "affected could agree to it, as participants in a practical discourse. <bookmark mark='c'/>The ideal "
            "speech situation is not a description of any real conversation. It is what we must presuppose, "
            "Habermas argues, whenever we argue seriously at all, because to argue is to try to convince by reasons "
            "rather than force. <bookmark mark='d'/>Its political version, democracy as deliberation, returns in "
            "Part 39."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rules], lag_ratio=0.5), run_time=4)
            vo.wait_until("b")
            self.play(Write(d_tex))
            vo.wait_until("c")
            self.play(FadeIn(foot[0]))
            vo.wait_until("d")
            self.play(FadeIn(foot[1]))
        self.clear_scene()

    def critics(self):
        head = label(r"Objections, \ and a machine", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"Lyotard \ (1979)", r"\textit{The Postmodern Condition}: \ `incredulity toward metanarratives', \ "
                                  r"consensus included", BAD),
            (r"Foucault", r"no discourse is free of power; \ the ideal hides the power that sets its rules", SIGN),
            (r"Tessler et al. \ (2024)", r"an AI mediator, \ nicknamed the `Habermas Machine', \ helped groups in "
                                         r"experiments find statements they could all endorse", ACT),
        ]
        g = rows_table(rows, top=1.6, gap=0.55)
        with self.voiceover(
            "Habermas's rationalism was challenged from several sides. <bookmark mark='a'/>Jean-François Lyotard, "
            "in The Postmodern Condition of 1979, defined the postmodern as incredulity toward metanarratives, the "
            "grand stories of emancipation through reason, and consensus among them. <bookmark mark='b'/>Foucault's "
            "followers replied that no discourse is free of power, and that an ideal of free discourse hides the "
            "power that sets its rules. <bookmark mark='c'/>And an epilogue. In 2024 Michael Henry Tessler and colleagues at Google DeepMind "
            "reported an AI mediator, nicknamed the Habermas Machine, that drafted group statements; in their "
            "experiments, participants preferred its statements to those of human mediators, and groups moved "
            "toward common ground."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abc", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
