from __future__ import annotations

from videos.philosophy.philosophy14.common import *  # noqa: F403


class Defaults(VoiceoverScene):
    def construct(self):
        card = chapter_card(10, r"Jumping to conclusions", r"How can more information mean fewer conclusions?",
                            lit=(1980,), part=PART)
        with self.voiceover("Chapter ten. Jumping to conclusions."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.tweety()
        self.reiter()
        self.nixon()
        self.circumscription()
        self.frame()

    def tweety(self):
        head = label(r"Tweety", font_size=32, color=CONN).to_edge(UP, buff=0.35)
        a = VGroup(label(r"Tweety is a bird", font_size=26), MathTex(r"\Rightarrow", font_size=34),
                   label(r"Tweety flies", font_size=26, color=OK)).arrange(RIGHT, buff=0.4)
        b = VGroup(label(r"Tweety is a bird, \ and a penguin", font_size=26), MathTex(r"\Rightarrow", font_size=34),
                   label(r"Tweety does not fly", font_size=26, color=BAD)).arrange(RIGHT, buff=0.4)
        VGroup(a, b).arrange(DOWN, buff=0.6).next_to(head, DOWN, buff=0.6)
        mono = MathTex(r"\text{classical logic is monotonic:}\quad \Gamma \vDash C \ \Rightarrow\ \Gamma \cup \Delta "
                       r"\vDash C", font_size=30, color=GREY_A).next_to(b, DOWN, buff=0.6)
        rows = stack([(r"everyday reasoning is not: \ more premises, \ fewer conclusions", GOAL),
                      (r"`birds fly' is not `all birds fly': \ it is a default, \ with exceptions", BEL)],
                     font_size=24).next_to(mono, DOWN, buff=0.4)
        with self.voiceover(
            "Artificial intelligence met belief revision from another direction. <bookmark mark='a'/>Told that Tweety "
            "is a bird, you conclude that Tweety flies. <bookmark mark='b'/>Told also that Tweety is a penguin, you "
            "conclude that Tweety does not. <bookmark mark='c'/>Classical logic cannot do this. It is monotonic: adding "
            "premises never removes a conclusion. <bookmark mark='d'/>Ordinary reasoning is non-monotonic. "
            "<bookmark mark='e'/>Birds fly is not the false generalization that all birds fly; it is a default, which "
            "holds unless something says otherwise. In 1980 a special issue of Artificial Intelligence launched three "
            "logics of defaults."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(a))
            vo.wait_until("b")
            self.play(FadeIn(b))
            vo.wait_until("c")
            self.play(FadeIn(mono))
            for mk, r in zip("de", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def reiter(self):
        d = load("defaults")["tweety"]
        hc = history_card(1980, r"Raymond Reiter", r"`A Logic for Default Reasoning'", width=5.2,
                          color=HIST).to_corner(UL, buff=0.35)
        rule = MathTex(r"\frac{\text{bird} : \text{flies}}{\text{flies}}", font_size=46, color=BEL).move_to(
            [-3.6, 0.4, 0])
        rl = label(r"if bird, \ and flying is consistent with what you believe, \ conclude flies", font_size=20,
                   color=GREY_A).next_to(rule, DOWN, buff=0.3)
        ext = stack([
            (r"an \textit{extension}: \ a fixed point, \ a belief set that justifies exactly the defaults it uses",
             WHITE),
            (r"facts: \ bird; \ \ penguins are birds; \ \ penguins don't fly", GREY_A),
            (r"extension: \ $\{\text{bird},\ \text{flies}\}$", OK),
            (r"add: \ penguin \ $\Rightarrow$ \ $\lnot$flies is now derived; \ the default is blocked", BAD),
            (r"extension: \ $\{\text{penguin},\ \text{bird},\ \lnot\text{flies}\}$", OK),
        ], font_size=21, aligned_edge=LEFT, width=6.2).move_to([3.6, -0.4, 0])
        if rl.width > 5.0:
            rl.width = 5.0
        assert d["penguin_flies"] == [False]
        with self.voiceover(
            "Raymond Reiter's default logic is the best known. <bookmark mark='a'/>A default rule says: if bird, and "
            "if flies is consistent with what you believe, conclude flies. <bookmark mark='b'/>The consistency check "
            "refers to the final belief set, so the conclusions are a fixed point, called an extension: a set of "
            "beliefs that justifies exactly the defaults it used to get there. <bookmark mark='c'/>The Reasoner finds "
            "the extensions by trying every set of defaults. With facts that Tweety is a bird, that penguins are "
            "birds, and that penguins don't fly, <bookmark mark='d'/>there is one extension, in which Tweety flies. "
            "<bookmark mark='e'/>Add that Tweety is a penguin. Now not flying is derived, the default is blocked, "
            "<bookmark mark='f'/>and the one extension has Tweety grounded."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(Write(rule), FadeIn(rl))
            for mk, r in zip("bcdef", ext):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def nixon(self):
        d = load("defaults")["nixon"]
        head = label(r"The Nixon diamond", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        top = label(r"Nixon", font_size=26, color=BEL).move_to([-3.2, 1.6, 0])
        q = label(r"Quaker", font_size=24).move_to([-4.8, 0.0, 0])
        r = label(r"Republican", font_size=24).move_to([-1.6, 0.0, 0])
        pa = label(r"pacifist", font_size=24, color=OK).move_to([-4.8, -1.8, 0])
        npa = label(r"not pacifist", font_size=24, color=BAD).move_to([-1.6, -1.8, 0])
        arrows = VGroup(Arrow(top.get_bottom(), q.get_top(), buff=0.15, color=GREY_B),
                        Arrow(top.get_bottom(), r.get_top(), buff=0.15, color=GREY_B),
                        DashedLine(q.get_bottom(), pa.get_top(), buff=0.15, color=OK),
                        DashedLine(r.get_bottom(), npa.get_top(), buff=0.15, color=BAD))
        rows = stack([
            (r"two defaults: \ Quakers are pacifists; \ Republicans are not", WHITE),
            (rf"the Reasoner: \ {len(d['extensions'])} extensions, \ one for each default", BEL),
            (r"credulous reasoning: \ pick an extension", GREY_A),
            (r"skeptical reasoning: \ believe only what all extensions share", GREY_A),
            (r"here, \ skeptically: \ nothing about pacifism", GOAL),
        ], font_size=22, aligned_edge=LEFT, width=6.6).move_to([3.3, -0.2, 0])
        with self.voiceover(
            "Defaults can conflict. <bookmark mark='a'/>Richard Nixon was a Quaker and a Republican. Quakers are, by "
            "default, pacifists; Republicans, by default, are not. <bookmark mark='b'/>The Reasoner finds two "
            "extensions: in one the Quaker default fires and blocks the other; in the second, the reverse. "
            "<bookmark mark='c'/>A credulous reasoner picks one. <bookmark mark='d'/>A skeptical reasoner believes only "
            "what every extension shares, <bookmark mark='e'/>and so concludes nothing about Nixon's pacifism. This "
            "choice returns when arguments attack each other, two chapters on."
        ) as vo:
            self.play(FadeIn(head), FadeIn(top), FadeIn(q), FadeIn(r), FadeIn(pa), FadeIn(npa), Create(arrows))
            for mk, rr in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(rr))
        self.clear_scene()

    def circumscription(self):
        head = label(r"Two more ways to be normal", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        left = VGroup(label(r"circumscription \ (McCarthy, \ 1980)", font_size=24, color=BEL),
                      MathTex(r"\text{bird}(x) \land \lnot \text{ab}(x) \to \text{flies}(x)", font_size=28),
                      label(r"keep only the models with as few abnormal things as possible", font_size=20,
                            color=GREY_A),
                      label(r"penguins must be abnormal; \ Tweety the bird need not be", font_size=20)).arrange(
            DOWN, buff=0.22)
        right = VGroup(label(r"negation as failure", font_size=24, color=BEL),
                       label(r"`no flight from Boston to Tokyo is listed: \ so there is none'", font_size=20),
                       label(r"the closed-world assumption \ (Reiter, \ 1978)", font_size=20, color=GREY_A),
                       label(r"every database and Prolog program reasons this way", font_size=20, color=GOAL)).arrange(
            DOWN, buff=0.22)
        for g in (left, right):
            for m in g:
                if m.width > 6.2:
                    m.width = 6.2
        VGroup(left, right).arrange(RIGHT, buff=0.8, aligned_edge=UP).next_to(head, DOWN, buff=0.7)
        foot = label(r"all of them jump to conclusions that new information can retract", font_size=24,
                     color=GOAL).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Two other logics from 1980 are still in use. <bookmark mark='a'/>John McCarthy's circumscription: write "
            "birds that are not abnormal fly, and then keep only the models in which as few things as possible are "
            "abnormal. Penguins must be abnormal; Tweety, merely a bird, need not be, so Tweety flies. "
            "<bookmark mark='b'/>And negation as failure, with Reiter's closed-world assumption: if no flight from "
            "Boston to Tokyo is listed, conclude there is none. Every database query, and every Prolog program, "
            "reasons like this. <bookmark mark='c'/>All of them jump to conclusions that new information can retract."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(m) for m in left], lag_ratio=0.3), run_time=2.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(m) for m in right], lag_ratio=0.3), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()

    def frame(self):
        d = load("yale")
        hc = history_card(1986, r"Hanks and McDermott", r"`Nonmonotonic Logic and Temporal Projection'", width=6.4,
                          color=HIST).to_corner(UL, buff=0.35)
        lead = label(r"the frame problem \ (McCarthy and Hayes, \ 1969): \ how to say that most things stay the same",
                     font_size=22, color=GREY_A).next_to(hc, DOWN, buff=0.3).set_x(0)
        steps = VGroup(*[VGroup(RoundedRectangle(width=2.2, height=0.7, corner_radius=0.12, color=BEL,
                                                 stroke_width=2.5), label(t, font_size=22)).arrange(ORIGIN)
                         for t in (r"load", r"wait", r"shoot")]).arrange(RIGHT, buff=0.9).next_to(lead, DOWN, buff=0.4)
        arrows = VGroup(*[Arrow(steps[i].get_right(), steps[i + 1].get_left(), buff=0.1, color=GREY_B)
                          for i in range(2)])
        names = {"alive at the shot": r"Fred dies at the shot", "loaded during wait": r"the gun unloads while we wait"}
        models = VGroup()
        for i, m in enumerate(d["minimal"]):
            ok = m["loaded2"]
            models.add(VGroup(label(r"intended" if ok else r"anomalous", font_size=23, color=OK if ok else BAD),
                              label(r"the one abnormality: \ " + names[m["changes"][0]], font_size=20),
                              label(r"Fred is dead" if not m["alive3"] else r"Fred is alive", font_size=20,
                                    color=OK if ok else BAD)).arrange(DOWN, buff=0.12))
        models.arrange(RIGHT, buff=1.4).next_to(steps, DOWN, buff=0.5)
        foot = stack([(r"minimizing change finds both: \ circumscription cannot tell which is meant", BAD),
                      (r"repairs: \ chronological minimization; \ causal theories; \ and Gottlob \ (1992): \ "
                       r"default reasoning is $\Sigma_2^p$-complete", GREY_A)], font_size=21, width=12.4).to_edge(
            DOWN, buff=0.3)
        with self.voiceover(
            "Defaults were meant to solve the frame problem of John McCarthy and Patrick Hayes: how to say, without "
            "endless axioms, that most things stay the same when you act. <bookmark mark='a'/>Steve Hanks and Drew "
            "McDermott's Yale shooting problem tested it. Load a gun, wait, and shoot Fred. Assume that things "
            "normally don't change, and minimize the changes. <bookmark mark='b'/>The Reasoner finds two minimal "
            "models. In the intended one, the gun stays loaded and Fred dies at the shot. <bookmark mark='c'/>In the "
            "other, the gun mysteriously unloads while we wait, and Fred lives. Each has exactly one abnormality, so "
            "minimizing cannot choose. <bookmark mark='d'/>Repairs followed: prefer later changes to earlier ones, or "
            "build causal laws into the logic. And Georg Gottlob proved that reasoning with Reiter's defaults is "
            "harder than any NP problem, unless the polynomial hierarchy collapses. Jumping to conclusions is not "
            "cheap."
        ) as vo:
            self.play(FadeIn(hc), FadeIn(lead))
            vo.wait_until("a")
            self.play(FadeIn(steps), GrowArrow(arrows[0]), GrowArrow(arrows[1]))
            vo.wait_until("b")
            self.play(FadeIn(models[0]))
            vo.wait_until("c")
            self.play(FadeIn(models[1]))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()
