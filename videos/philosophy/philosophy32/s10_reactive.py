from __future__ import annotations

from videos.philosophy.philosophy32.common import *  # noqa: F403


class Reactive(VoiceoverScene):
    def construct(self):
        card = chapter_card(9, r"Freedom and resentment", r"Is responsibility a fact to be discovered, \ or a practice "
                                                          r"we live in?", lit=(1962,), part=PART)
        with self.voiceover("Chapter nine. Freedom and resentment."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.attitudes()
        self.stances()
        self.faces()
        self.since()

    def attitudes(self):
        hc = history_card(1962, r"P. F. Strawson", r"`Freedom and Resentment'", width=5.2, color=HIST).to_corner(
            UL, buff=0.3)
        centre = VGroup(Circle(radius=0.6, color=BLAME, fill_opacity=0.12), label(r"you", font_size=20,
                                                                                 color=BLAME)).move_to([-2.6, -0.4, 0])
        names = [(r"resentment", BAD), (r"gratitude", OK), (r"indignation", BAD), (r"love", BLAME),
                 (r"forgiveness", OK), (r"hurt feelings", BAD)]
        ring = VGroup()
        for k, (n, c) in enumerate(names):
            ang = PI / 2 + k * TAU / 6
            ring.add(label(n, font_size=19, color=c).move_to(centre.get_center() + 2.1 * np.array(
                [np.cos(ang), np.sin(ang), 0])))
        rows = stack([(r"reactive attitudes: \ responses to the good or ill will others show us", GREY_A),
                      (r"not theories we hold, \ but part of what it is to live among persons", BLAME),
                      (r"responsibility is not answerable to metaphysics: \ it is constituted by these attitudes", GOAL)],
                     font_size=20, aligned_edge=LEFT, width=6.0, buff=0.3).move_to([3.5, -0.4, 0])
        with self.voiceover(
            "In 1962 Peter Strawson changed the subject. <bookmark mark='a'/>Look, he said, at the attitudes we "
            "actually take to one another: resentment when someone wrongs us, gratitude when they help, "
            "indignation on another's behalf, love, forgiveness, hurt feelings. <bookmark mark='b'/>These reactive "
            "attitudes are responses to the good or ill will that others show us. <bookmark mark='c'/>They are not "
            "a theory we hold, which the discovery of determinism could refute. They are part of what it is to live "
            "among persons at all. <bookmark mark='d'/>And holding people responsible just is taking these "
            "attitudes to them. Responsibility is not answerable to metaphysics; it is constituted by the practice."
        ) as vo:
            self.play(FadeIn(hc), FadeIn(centre))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in ring], lag_ratio=0.2), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def stances(self):
        head = label(r"Two stances toward a person", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        left = VGroup(RoundedRectangle(width=5.4, height=2.8, corner_radius=0.2, color=BLAME, fill_opacity=0.08),
                      VGroup(label(r"the participant stance", font_size=23, color=BLAME),
                             wrapped_label(r"engaged: \ we resent, \ thank, \ forgive; \ the default among adults", 4.8,
                                           19, GREY_A)).arrange(DOWN, buff=0.25)).move_to([-3.2, 0.1, 0])
        right = VGroup(RoundedRectangle(width=5.4, height=2.8, corner_radius=0.2, color=FUNC, fill_opacity=0.08),
                       VGroup(label(r"the objective stance", font_size=23, color=FUNC),
                              wrapped_label(r"someone to be managed, \ treated, \ or avoided: \ apt for small children, "
                                            r"\ or in illness", 4.8, 19, GREY_A)).arrange(DOWN, buff=0.25)
                       ).move_to([3.2, 0.1, 0])
        foot = stack([(r"excuses work inside the practice: \ `he didn't mean it', \ `he wasn't himself'", WILL),
                      (r"could we take the objective stance to everyone, \ always? \ not, \ Strawson thinks, \ as "
                       r"humans", GOAL)], font_size=20, buff=0.22).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Strawson contrasted two stances. <bookmark mark='a'/>The participant stance is engaged: we resent, "
            "thank and forgive. It is our default toward other adults. <bookmark mark='b'/>The objective stance "
            "sees a person as something to be managed, treated, or avoided, and we take it to small children, or "
            "to someone in the grip of illness. <bookmark mark='c'/>Excuses work inside the participant stance: he "
            "did not mean it, he was pushed, he was not himself. Determinism is not an excuse of that kind. "
            "<bookmark mark='d'/>Could we take the objective stance toward everyone, all the time, if determinism "
            "were proved? Strawson thought that was not a real option for creatures like us."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(left))
            vo.wait_until("b")
            self.play(FadeIn(right))
            vo.wait_until("c")
            self.play(FadeIn(foot[0]))
            vo.wait_until("d")
            self.play(FadeIn(foot[1]))
        self.clear_scene()

    def faces(self):
        head = label(r"The faces of responsibility \ (Watson, \ 1996; \ Shoemaker, \ 2015)", font_size=30,
                     color=CONN).to_edge(UP, buff=0.3)
        rows = [(r"attributability", r"does the act express who you are, \ your values and cares? \ response: \ "
                                     r"admiration, \ disdain", SELF),
                (r"answerability", r"may you be asked for your reasons, \ and must you answer? \ response: \ "
                                   r"demands for justification \ (Scanlon; \ A. Smith)", FUNC),
                (r"accountability", r"is it fair to hold you to a demand, \ with blame and sanction? \ response: \ "
                                    r"resentment, \ indignation, \ punishment", BLAME),
                (r"they come apart", r"a cruel act may be wholly yours, \ yet if you could not grasp why it matters to "
                                     r"others, \ resentment may be unfair \ (Shoemaker on psychopathy)", GOAL)]
        g = rows_table(rows, top=1.6, gap=0.45, width=8.6)
        with self.voiceover(
            "Strawson's picture has been refined by asking what, exactly, responsibility is. "
            "<bookmark mark='a'/>Gary Watson distinguished two faces in 1996. One is attributability: does the act "
            "express who you are, your values and what you care about? Admiration and disdain respond to that. "
            "<bookmark mark='b'/>Thomas Scanlon and Angela Smith stressed answerability: may you be asked for your "
            "reasons, and must you give them? <bookmark mark='c'/>And accountability: is it fair to hold you to a "
            "demand, and to blame or sanction you for failing it? That is the face Strawson's resentment belongs "
            "to, and the one free will debates usually mean. <bookmark mark='d'/>David Shoemaker argued in 2015 that "
            "the faces come apart at the margins of agency. A cruel act may be wholly attributable to someone who "
            "cannot grasp why it matters to others, and yet resentment, which demands that they feel its force, may "
            "be unfair. Which face determinism threatens may differ: the hard incompatibilist's target is "
            "accountability."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def since(self):
        head = label(r"After Strawson", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [(r"Wallace \ (1994)", r"responsibility as the fairness of holding someone to moral demands", SELF),
                (r"Watson \ (1987)", r"the case of Robert Harris: \ his crimes, \ then his childhood: \ our reactive "
                                     r"attitudes waver", BAD),
                (r"experimental philosophy", r"Nahmias and others: \ most people judge agents in a deterministic world "
                                             r"responsible; \ abstract framings reverse it", CHANCE),
                (r"the lesson", r"the practice is robust, \ but sensitive to how a life came to be", GOAL)]
        g = rows_table(rows, top=1.6, gap=0.5)
        with self.voiceover(
            "Strawson's approach has been developed and tested. <bookmark mark='a'/>R. Jay Wallace recast "
            "responsibility as a matter of when it is fair to hold someone to moral demands. "
            "<bookmark mark='b'/>Gary Watson studied the case of Robert Harris, a murderer whose crimes provoke "
            "outrage, until one reads of his childhood of abuse. Our reactive attitudes waver, and Watson asked "
            "what that wavering tracks. <bookmark mark='c'/>Experimental philosophers, Eddy Nahmias among them, have "
            "asked people directly. Most judge agents in a deterministic world to be responsible, when the case is "
            "concrete; abstract framings can reverse the verdict. <bookmark mark='d'/>The practice is robust, but it "
            "is sensitive to how a life came to be what it is, which is the topic of the next chapter's "
            "experiments too."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
