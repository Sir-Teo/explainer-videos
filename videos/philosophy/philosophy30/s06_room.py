from __future__ import annotations

from videos.philosophy.philosophy30.common import *  # noqa: F403

CJK = "Noto Serif CJK SC"


def cjk(s, size=22, col=WHITE):
    return Text(s, font=CJK, font_size=size, color=col)


class Room(VoiceoverScene):
    def construct(self):
        card = chapter_card(5, r"The Chinese room", r"Is running the right program enough to understand?", lit=(1980,),
                            part=PART)
        with self.voiceover("Chapter five. The Chinese room."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.room()
        self.rulebook()
        self.replies()
        self.since()

    def room(self):
        hc = history_card(1980, r"John Searle", r"`Minds, Brains, and Programs'", width=5.6, color=HIST).to_corner(
            UL, buff=0.3)
        box = Rectangle(width=4.4, height=3.0, color=GREY_B).move_to([0, -0.4, 0])
        man = VGroup(Circle(radius=0.25, color=FEEL), Line([0, -0.25, 0], [0, -0.95, 0], color=FEEL)).move_to(
            [0, -0.4, 0])
        book = VGroup(Rectangle(width=0.9, height=0.6, color=SYM, fill_opacity=0.3),
                      label(r"rules", font_size=14, color=SYM)).move_to([1.2, -1.2, 0])
        slot_in = Arrow([-4.6, 0.3, 0], [-2.2, 0.3, 0], color=BEHAV)
        slot_out = Arrow([2.2, -0.9, 0], [4.6, -0.9, 0], color=BEHAV)
        qin = cjk("他吃了汉堡吗？", 22, BEHAV).next_to(slot_in, UP, buff=0.12)
        aout = cjk("没有。", 22, BEHAV).next_to(slot_out, UP, buff=0.12)
        rows = stack([(r"a man who knows no Chinese, \ a rulebook in English for matching shapes", FEEL),
                      (r"to those outside, \ the room answers questions in Chinese as well as a native speaker", OK),
                      (r"but he understands nothing: \ and a computer has only what he has, \ the program", BAD)],
                     font_size=20, aligned_edge=LEFT, width=12.0, buff=0.2).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "In 1980 John Searle answered Turing with a thought experiment. <bookmark mark='a'/>He imagines himself "
            "locked in a room with boxes of Chinese characters and a rulebook, written in English, that says which "
            "strings of shapes to send out in response to which strings come in. He knows no Chinese; to him the "
            "characters are just squiggles. <bookmark mark='b'/>Questions in Chinese are passed in through a slot. He "
            "looks up the shapes, follows the rules, and passes out answers. From outside, the room answers as well "
            "as a native speaker. <bookmark mark='c'/>But he understands nothing. And a computer running a program "
            "has nothing more than he has: the rules. So running the right program, however well, is not "
            "sufficient for understanding. Syntax is not sufficient for semantics."
        ) as vo:
            self.play(FadeIn(hc), Create(box))
            vo.wait_until("a")
            self.play(FadeIn(man), FadeIn(book), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(GrowArrow(slot_in), FadeIn(qin))
            self.play(GrowArrow(slot_out), FadeIn(aout), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def rulebook(self):
        d = load("rulebook")
        head = label(r"A rulebook, \ built", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        assert d["rules"] == 8 and d["narrow_right"] == 8 and len(d["narrow"]) == 8
        assert d["wide_unmatched"] == 2 and d["wide"][2]["answer"] == "没有。" and d["wide"][3]["answer"] == "一个男人。"
        story = cjk(d["story"], 22, GREY_A).move_to([0, 2.3, 0])
        sl = label(r"the story \ (`a man went into a restaurant and ordered a hamburger \dots')", font_size=16,
                   color=GREY_B).next_to(story, DOWN, buff=0.1)
        left = VGroup()
        for r in d["narrow"][:5]:
            left.add(VGroup(cjk(r["q"], 19, BEHAV), cjk(r["answer"], 19, OK),
                            MathTex(r"\checkmark", font_size=22, color=OK)).arrange(RIGHT, buff=0.3))
        left.arrange(DOWN, buff=0.22, aligned_edge=LEFT).move_to([-3.3, -0.4, 0])
        ll = label(r"the narrow test: \ 8 of 8", font_size=18, color=OK).next_to(left, UP, buff=0.2)
        right = VGroup()
        for r in d["wide"]:
            a = cjk(r["answer"], 19, BAD) if r["answer"] else label(r"(no rule)", font_size=17, color=BAD)
            right.add(VGroup(cjk(r["q"], 19, BEHAV), a).arrange(RIGHT, buff=0.3))
        right.arrange(DOWN, buff=0.22, aligned_edge=LEFT).move_to([3.3, -0.4, 0])
        rl = label(r"outside the script", font_size=18, color=BAD).next_to(right, UP, buff=0.2)
        gloss = label(r"`why didn't he eat?' \ $\to$ \ `no.' \quad `who are you?' \ $\to$ \ `a man.'", font_size=17,
                      color=GREY_A).next_to(right, DOWN, buff=0.25)
        foot = label(r"8 rules matching shapes: \ perfect on its script, \ helpless off it; \ Searle's point is that a "
                     r"perfect rulebook would be no different in kind", font_size=19, color=GOAL).to_edge(DOWN,
                                                                                               buff=0.35)
        with self.voiceover(
            "The Reasoner writes a rulebook of its own. <bookmark mark='a'/>The story, in Chinese: a man went into a "
            "restaurant and ordered a hamburger; when it came it was burnt, and he was angry and left without "
            "paying. Searle borrowed the example from Roger Schank's story-understanding programs. "
            "<bookmark mark='b'/>Eight rules, each of the form: if the question contains these shapes, send out "
            "those. Did he eat the hamburger? No. Did he pay? No. What did he order? A hamburger. On a narrow test "
            "about the story the rulebook is perfect: eight of eight. <bookmark mark='c'/>Outside the script it is "
            "helpless. Do you like hamburgers, and what is the weather today, match no rule. Why didn't he eat? "
            "matches the rule for eat, and gets the answer no. Who are you? gets: a man. "
            "<bookmark mark='d'/>Searle's claim is stronger than that this rulebook is bad. A perfect rulebook, one "
            "that never slipped, would still be shapes in and shapes out, and so would understand no more than this "
            "one."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(story), FadeIn(sl))
            vo.wait_until("b")
            self.play(FadeIn(ll), LaggedStart(*[FadeIn(x) for x in left], lag_ratio=0.3))
            vo.wait_until("c")
            self.play(FadeIn(rl), LaggedStart(*[FadeIn(x) for x in right], lag_ratio=0.3), FadeIn(gloss))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()

    def replies(self):
        head = label(r"The replies, \ and Searle's answers", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        rows = [
            (r"the systems reply", r"the man doesn't understand, \ but the whole system does", FUNC,
             r"let him memorize the rules: \ he is the system, \ and still understands nothing"),
            (r"the robot reply", r"put the program in a robot with cameras and arms", PHYS,
             r"the camera's output is more symbols"),
            (r"the brain simulator", r"simulate the firing of a Chinese speaker's neurons", MIND,
             r"water pipes and valves simulating neurons understand nothing either"),
            (r"other minds", r"how do you know anyone understands Chinese?", BEHAV,
             r"the question is what understanding \textit{is}, \ not how we know it"),
        ]
        g = VGroup()
        top = 1.7
        for a, b, c, ans in rows:
            x = label(a, font_size=20, color=c).move_to([-6.4, top, 0], aligned_edge=LEFT)
            y = wrapped_label(b, 4.6, 18, WHITE).move_to([-3.2, top, 0], aligned_edge=LEFT)
            z = wrapped_label(ans, 4.4, 18, BAD).move_to([2.0, top, 0], aligned_edge=LEFT)
            g.add(VGroup(VGroup(x, y), z))
            top -= max(x.height, y.height, z.height) + 0.55
        foot = label(r"Searle: \ minds have intrinsic intentionality; \ programs have only what we lend them",
                     font_size=20, color=GOAL).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Searle's paper was published with replies, and he answered them. <bookmark mark='a'/>The systems reply: "
            "the man does not understand, but the whole system, man plus rulebook plus paper, does. Searle: let him "
            "memorize the rules and do it all in his head. Now he is the whole system, and he still understands "
            "nothing. <bookmark mark='b'/>The robot reply: put the program in a robot, with cameras and arms, so its "
            "symbols connect to the world. Searle: what comes in from the camera is just more symbols. "
            "<bookmark mark='c'/>The brain simulator reply: let the program simulate the firing of every neuron in a "
            "Chinese speaker's brain. Searle: imagine the simulation done with water pipes and valves; the pipes "
            "understand nothing. <bookmark mark='d'/>The other minds reply: how do you know that anyone understands "
            "Chinese, except by their behaviour? Searle: the question is what understanding is, not how we know it is "
            "there. <bookmark mark='e'/>His conclusion: brains have intrinsic intentionality, caused by their specific "
            "biology; programs have only the meaning we lend them."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r[0]))
                self.play(FadeIn(r[1]))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()

    def since(self):
        head = label(r"Still argued", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"an intuition pump", r"Dennett and Hofstadter \ (1981): \ the room's slowness hides how much such a "
                                   r"system would be doing", FUNC),
            (r"the dilemma", r"if the room understands, \ understanding is cheap; \ if not, \ functionalism is "
                             r"incomplete", BAD),
            (r"language models", r"trained on text, \ not handed a rulebook: \ the octopus of Part 28, \ the same "
                                 r"question", SYM),
            (r"what grounds meaning?", r"causes, \ history, \ use: \ chapter 11 returns to it", GOAL),
        ]
        g = rows_table(rows, top=1.6, gap=0.55)
        with self.voiceover(
            "The argument is still argued over. <bookmark mark='a'/>Daniel Dennett and Douglas Hofstadter called it "
            "an intuition pump: picturing one slow man with a book hides how complex a system that really conversed "
            "would have to be. <bookmark mark='b'/>For functionalism it poses a dilemma. If the room understands, "
            "understanding is cheaper than we thought; if it does not, the functional role leaves something out. "
            "<bookmark mark='c'/>Language models revive it. They were not handed a rulebook; they learned from text, "
            "which is the situation of the octopus in Part 28. <bookmark mark='d'/>What, then, makes a state mean "
            "something? Chapter eleven returns to that question."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
