from __future__ import annotations

from videos.philosophy.philosophy23.common import *  # noqa: F403


class Experience(VoiceoverScene):
    def construct(self):
        card = chapter_card(13, r"Faith, \ experience and disagreement", r"Can belief in God be rational without "
                            r"proof?", lit=(1896, 1991), part=PART)
        with self.voiceover("Chapter thirteen. Faith, experience and disagreement."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.reformed()
        self.perception()
        self.hiddenness()
        self.disagreement()

    def reformed(self):
        head = label(r"Reformed epistemology", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"evidentialism", r"Clifford, \ and classical foundationalism: \ belief in God needs an argument", ARG),
            (r"Plantinga \ (2000)", r"\textit{Warranted Christian Belief}: \ belief in God can be properly basic, \ "
                                    r"like belief in other minds", DIV),
            (r"other minds", r"no proof that others are conscious \ (Part 30); \ yet the belief is rational", HUM),
            (r"warrant", r"produced by faculties working properly, \ aimed at truth \ (Part 11's reliabilism)", ABS),
            (r"the Great Pumpkin", r"objection: \ then any belief could be called basic; \ reply: \ only those formed "
                                   r"by working faculties", BAD),
        ]
        g = rows_table(rows, top=1.9, gap=0.45, width=8.8, x_text=-2.4, label_size=21)
        with self.voiceover(
            "Perhaps belief in God does not need an argument at all. <bookmark mark='a'/>The evidentialist, from "
            "Clifford on, says that it does: a rational belief in God must be based on good arguments. "
            "<bookmark mark='b'/>Plantinga's reformed epistemology replies that belief in God can be properly basic, "
            "like belief in other minds or in the past. <bookmark mark='c'/>No one has a proof that other people are "
            "conscious, as Part 30 will show; yet the belief is rational. <bookmark mark='d'/>On Plantinga's account a "
            "belief is warranted if it is produced by cognitive faculties working properly, in the right environment, "
            "aimed at truth: a cousin of Part 11's reliabilism. If God exists and made us to know him, belief in God "
            "may be warranted; if not, probably not. <bookmark mark='e'/>Critics ask why, then, belief in the Great "
            "Pumpkin could not be basic too. The reply is that only beliefs formed by properly working faculties "
            "count; which beliefs those are is the very question at issue."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def perception(self):
        hc = history_card(1991, r"William Alston", r"\textit{Perceiving God}", width=5.2, color=HIST).to_corner(
            UL, buff=0.3)
        rows = stack([(r"sense perception: \ we trust it without independent proof that it is reliable", NAT),
                      (r"mystical perception: \ millions report experiences of God's presence", DIV),
                      (r"Alston: \ a socially established practice of belief formation is rational to engage in, \ "
                       r"unless shown unreliable", ABS),
                      (r"Swinburne's principle of credulity: \ how things seem is evidence for how they are", WARM),
                      (r"the objections: \ no cross-checks like those of vision; \ rival traditions perceive rival "
                       r"gods", BAD)], font_size=21, aligned_edge=LEFT, width=12.2, buff=0.3).move_to([0, -0.4, 0])
        with self.voiceover(
            "A second line appeals to experience. <bookmark mark='a'/>We trust our senses without any independent "
            "proof that they are reliable; any such proof would itself use the senses. <bookmark mark='b'/>Millions "
            "of people report experiences of God's presence. <bookmark mark='c'/>William Alston argued that a "
            "socially established practice of forming beliefs is rational to engage in unless it has been shown to "
            "be unreliable, and that Christian mystical practice is such a practice. <bookmark mark='d'/>Richard "
            "Swinburne's principle of credulity says the same more simply: how things seem is evidence for how they "
            "are, unless there is reason for doubt. <bookmark mark='e'/>The objections: religious experience lacks "
            "the cross-checks that vision has, where others can look too; and rival traditions report experiences of "
            "rival gods, or of no god."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def hiddenness(self):
        hc = history_card(1993, r"J. L. Schellenberg", r"\textit{Divine Hiddenness and Human Reason}", width=6.8,
                          color=HIST).to_corner(UL, buff=0.3)
        steps = stack([(r"1. \ a perfectly loving God would always be open to a personal relationship with us", DIV),
                       (r"2. \ so such a God would ensure that no one who is not resisting fails to believe", ABS),
                       (r"3. \ but there are nonresistant nonbelievers: \ seekers, \ and whole cultures who never "
                        r"heard", WHITE),
                       (r"4. \ so there is no perfectly loving God", BAD)], font_size=21, aligned_edge=LEFT,
                      width=12.2, buff=0.32).move_to([0, 0.3, 0])
        rows = stack([(r"replies: \ freedom needs epistemic distance \ (Hick); \ belief is not yet relationship; \ "
                       r"goods beyond our ken again", GREY_A),
                      (r"an argument from absence: \ the evidence it needs is the debate itself", GOAL)],
                     font_size=20, aligned_edge=LEFT, width=12.2).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Experience cuts the other way too. J. L. Schellenberg's argument from divine hiddenness: "
            "<bookmark mark='a'/>a perfectly loving God would always be open to a personal relationship with each of "
            "us. <bookmark mark='b'/>So such a God would make sure that no one who is not resisting fails to believe "
            "that God exists, since belief is a precondition of the relationship. <bookmark mark='c'/>But there are "
            "nonresistant nonbelievers: honest seekers, and whole peoples who never heard of God. "
            "<bookmark mark='d'/>So there is no perfectly loving God. <bookmark mark='e'/>Replies say that freedom "
            "needs epistemic distance, as John Hick held; that belief is not yet relationship; or, again, that God "
            "may have reasons beyond our ken. <bookmark mark='f'/>It is an argument from absence: the evidence it "
            "appeals to is the persistence of reasonable unbelief, including the debates of this part."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abcd", steps):
                vo.wait_until(mk)
                self.play(FadeIn(r))
            for mk, r in zip("ef", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def disagreement(self):
        head = label(r"Religious disagreement", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        people = VGroup()
        cols = [DIV, ARG, NAT, HUM, WARM]
        for i in range(5):
            a = 2 * PI * i / 5 + PI / 2
            p = person([2.0 * np.cos(a) - 3.4, 1.7 * np.sin(a) + 0.3, 0], color=cols[i], r=0.2)
            people.add(p)
        links = VGroup(*[Line(people[i].dot.get_center(), people[j].dot.get_center(), color=GREY_D, stroke_width=1.5)
                         for i in range(5) for j in range(i + 1, 5)])
        links.set_z_index(-1)
        pl = label(r"epistemic peers, \ equally informed, \ disagreeing", font_size=18, color=GREY_A).next_to(
            people, DOWN, buff=0.3)
        rows = stack([(r"Part 12's question: \ when a peer disagrees, \ should you move towards them?", ABS),
                      (r"conciliationists: \ yes: \ suspend judgment, \ on God as on anything", WHITE),
                      (r"steadfast views: \ your evidence includes how things seem to you", DIV),
                      (r"Hick's pluralism \ (1989): \ the great traditions as responses to one Real", NAT),
                      (r"the exclusivist reply: \ disagreement does not make truth relative", BAD)],
                     font_size=20, aligned_edge=LEFT, width=6.0).move_to([3.5, -0.1, 0])
        with self.voiceover(
            "Finally, disagreement. <bookmark mark='a'/>Thoughtful, informed people, equally intelligent and equally "
            "sincere, disagree about God. Part 12 asked what you should do when an epistemic peer disagrees with you. "
            "<bookmark mark='b'/>Conciliationists say: move towards them; on a question this contested, suspend "
            "judgment. <bookmark mark='c'/>Steadfast views say that your evidence includes how things seem to you, "
            "which your peer lacks. <bookmark mark='d'/>John Hick proposed religious pluralism: the great traditions "
            "as different human responses to one ultimate reality. <bookmark mark='e'/>Exclusivists reply that the "
            "existence of disagreement does not make truth relative; someone may simply be right."
        ) as vo:
            self.play(FadeIn(head), Create(links), FadeIn(people), FadeIn(pl))
            for mk, r in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
