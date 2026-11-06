from __future__ import annotations

from videos.philosophy.philosophy11.common import *  # noqa: F403


def _target(center, r=0.55):
    return VGroup(*[Circle(radius=r * k, stroke_color=c, stroke_width=3) for k, c in
                    ((1.0, WHITE), (0.62, BAD), (0.28, GOAL))]).move_to(center)


class Virtue(VoiceoverScene):
    def construct(self):
        card = chapter_card(8, r"The archer", r"Is knowledge an achievement?", lit=(), part=PART)
        with self.voiceover("Chapter eight. The archer."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.aaa()
        self.levels()
        self.credit()

    def aaa(self):
        head = label(r"Accurate, \ adroit, \ apt", font_size=32, color=CONN).to_edge(UP, buff=0.35)
        who = label(r"Ernest Sosa, \ \textit{A Virtue Epistemology} (2007)", font_size=22, color=GREY_B).next_to(
            head, DOWN, buff=0.2)
        ys = [1.3, -0.5, -2.3]
        shots = []
        specs = [(r"a skilled shot", [[-1.6, 0.25], [0.4, 0.15]], True, True, True),
                 (r"skilled, \ two gusts", [[-1.8, 0.6], [0.0, -0.5], [1.2, 0.3]], True, True, False),
                 (r"a wild shot", [[-2.2, -0.5], [-0.4, 0.55], [1.0, 0.2]], True, False, False)]
        for (name, mids, acc, adr, apt), y in zip(specs, ys):
            start = np.array([-4.6, y, 0])
            tc = np.array([2.2, y, 0])
            tg = _target(tc)
            pts = [start] + [np.array([x, y + dy, 0]) for x, dy in mids] + [tc]
            path = VMobject(color=OK if apt else LUCK, stroke_width=3)
            path.set_points_smoothly(pts)
            nm = label(name, font_size=21, color=WHITE).next_to(start, LEFT, buff=0.2)
            marks = VGroup(mark(acc, 26), mark(adr, 26), mark(apt, 26)).arrange(RIGHT, buff=0.75).move_to(
                [4.9, y, 0])
            shots.append((tg, path, nm, marks, Dot(start, radius=0.06, color=WHITE)))
        hdr = VGroup(label(r"accurate", font_size=20, color=P.CLAIM), label(r"adroit", font_size=20,
                                                                             color=P.CLAIM),
                     label(r"apt", font_size=20, color=P.CLAIM))
        for h, m in zip(hdr, shots[0][3]):
            h.move_to([m.get_x(), ys[0] + 0.75, 0])
        key = label(r"apt: \ accurate \textit{because} adroit", font_size=24, color=GOAL).to_edge(DOWN, buff=0.2)
        with self.voiceover(
            "Another family of theories borrows from the ethics of virtue. <bookmark mark='a'/>Ernest Sosa's model "
            "is the archer. A shot can be assessed in three ways. Accurate: did it hit the target? Adroit: did it "
            "show skill? Apt: was it accurate because it was adroit? <bookmark mark='b'/>A skilled archer looses a "
            "good shot, and it flies true to the centre. Accurate, adroit, and apt. <bookmark mark='c'/>The same "
            "skilled shot meets a gust that blows it off course, and a second gust that blows it back. It hits. "
            "Accurate and adroit, but not apt: it hit by luck, not by skill. That is a Gettier case. "
            "<bookmark mark='d'/>A novice's wild shot that happens to land in the centre is accurate, but neither "
            "adroit nor apt. <bookmark mark='e'/>A belief is like a shot. Its aim is truth. Knowledge, for Sosa, is "
            "apt belief: belief that is true because it is competent."
        ) as vo:
            self.play(FadeIn(head), FadeIn(who), FadeIn(hdr))
            for mk, (tg, path, nm, marks, dot) in zip("bcd", shots):
                vo.wait_until(mk)
                self.play(FadeIn(tg), FadeIn(nm), FadeIn(dot))
                self.play(Create(path), run_time=1.6, rate_func=linear)
                self.play(LaggedStart(*[FadeIn(m) for m in marks], lag_ratio=0.3))
            vo.wait_until("e")
            self.play(FadeIn(key))
        self.clear_scene()

    def levels(self):
        head = label(r"Two levels of knowledge", font_size=32, color=CONN).to_edge(UP, buff=0.4)
        a = VGroup(label(r"animal knowledge", font_size=27, color=KNOW),
                   label(r"apt belief:", font_size=22, color=GREY_A),
                   label(r"true because competent", font_size=22, color=GREY_A),
                   label(r"a hunter's shot that hits by skill", font_size=20, color=GREY_B)).arrange(DOWN, buff=0.14)
        b = VGroup(label(r"reflective knowledge", font_size=27, color=BEL),
                   label(r"apt belief, \ aptly endorsed:", font_size=22, color=GREY_A),
                   label(r"the believer also aptly judges it apt", font_size=22, color=GREY_A),
                   label(r"a hunter who also judged \ the shot worth taking", font_size=20, color=GREY_B)).arrange(
            DOWN, buff=0.14)
        cols = VGroup(a, b).arrange(RIGHT, buff=1.8, aligned_edge=UP).move_to([0, 0.7, 0])
        arr = Arrow(a.get_right() + RIGHT * 0.1, b.get_left() + LEFT * 0.1, buff=0.1, color=GREY_B)
        foot = VGroup(label(r"a second-order competence, \ but not KK:", font_size=23, color=GOAL),
                      label(r"reflective knowledge is rarer, \ and can be missing where animal knowledge is present",
                            font_size=22, color=GREY_A)).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Sosa adds a second level. <bookmark mark='a'/>Animal knowledge is apt belief: belief that is true "
            "because it is competent, like a hunter's shot that hits through skill. <bookmark mark='b'/>Reflective "
            "knowledge is apt belief aptly endorsed: the believer also judges, competently and correctly, that her "
            "first-order belief is apt, like a hunter who also judged rightly that the shot was worth taking. "
            "<bookmark mark='c'/>This is a second-order competence, but it is not the KK principle. Reflective "
            "knowledge is rarer than animal knowledge, and can be missing when animal knowledge is present, as "
            "chapter ten will show it must be, for some knowledge, near any boundary."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(a))
            vo.wait_until("b")
            self.play(GrowArrow(arr), FadeIn(b))
            vo.wait_until("c")
            self.play(FadeIn(foot[0]))
            self.play(FadeIn(foot[1]))
        self.clear_scene()

    def credit(self):
        head = label(r"Knowledge as credit for success", font_size=32, color=CONN).to_edge(UP, buff=0.35)
        rows = VGroup(
            label(r"Greco (2010): \ to know is to succeed in believing truly \ through one's own ability", font_size=24,
                  color=KNOW),
            label(r"so one deserves credit for the truth", font_size=23, color=GREY_A),
            label(r"Barn County: \ Henry sees a real barn, \ by his own ability: \ credit, \ and knowledge?",
                  font_size=23, color=BAD),
            label(r"testimony (Lackey): \ a stranger in Chicago gives me directions; \ I know the way,", font_size=23,
                  color=BEL),
            label(r"but the credit is mostly hers", font_size=23, color=BEL),
            label(r"Pritchard (2012): \ knowledge needs both: \ ability, \ \textit{and} safety", font_size=26,
                  color=GOAL)).arrange(DOWN, buff=0.3).move_to([0, -0.2, 0])
        with self.voiceover(
            "Virtue theories make knowledge an achievement. <bookmark mark='a'/>John Greco: to know is to succeed in "
            "believing the truth through one's own cognitive ability, <bookmark mark='b'/>so that one deserves "
            "credit for getting it right, as an archer deserves credit for an apt shot. <bookmark mark='c'/>But Barn "
            "County is hard for this view. Henry sees a real barn with his own working eyes. His success seems to "
            "come from his ability, yet most people judge that he does not know. <bookmark mark='d'/>Testimony is "
            "hard in the other direction. Jennifer Lackey's example: I arrive in Chicago and ask a stranger the way "
            "to the Sears Tower. She tells me, and I know the way. <bookmark mark='e'/>But the credit for my true "
            "belief belongs mostly to her. <bookmark mark='f'/>Duncan Pritchard concluded that knowledge needs two "
            "things: the ability, and safety, the anti-luck condition of the last chapter. Neither alone is enough."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcdef", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()
