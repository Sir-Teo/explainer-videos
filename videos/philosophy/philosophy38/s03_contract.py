from __future__ import annotations

from videos.philosophy.philosophy38.common import *  # noqa: F403


class Contract(VoiceoverScene):
    def construct(self):
        card = chapter_card(2, r"The social contract", r"Can authority rest on consent?", lit=(1651, 1689, 1762), part=PART)
        with self.voiceover("Chapter two. The social contract."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.hobbes()
        self.locke()
        self.rousseau()
        self.hume()

    def hobbes(self):
        head = label(r"Hobbes, \ again", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"Part 34's game", r"in the state of nature, \ attacking first is each one's best reply: \ the war of all against all", POW),
                (r"the sovereign", r"we authorize one power to keep us all in awe: \ peace becomes each one's best reply", COM),
                (r"the limit", r"the sovereign's power is nearly absolute: \ only self-preservation is kept back", BAD)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "The modern social contract begins with Hobbes, whose game Part 34 solved. <bookmark mark='a'/>In the "
            "state of nature, attacking first is each person's best reply, and the result is the war of all against "
            "all. <bookmark mark='b'/>So we authorize one power to keep us all in awe, and peace becomes each "
            "person's best reply. <bookmark mark='c'/>But Hobbes's sovereign is nearly absolute: the only right kept "
            "back is the right to defend one's own life."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abc", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def locke(self):
        head = label(r"Locke \ (1689)", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"natural rights", r"even before government, \ we have rights to life, \ liberty and estate, \ known by reason", LIB),
                (r"property", r"we own our labour, \ and mixing it with unowned things makes them ours: \ provided there is `enough, \ and as good, \ left in common for others'", MKT),
                (r"government", r"by consent, \ to protect those rights; \ a government that violates them may be resisted", COM),
                (r"tacit consent", r"enjoying the protection of a state's laws counts as consenting to them", GREY_A)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "John Locke's Second Treatise, of 1689, gave the contract a different shape. <bookmark mark='a'/>Even "
            "before government, he argued, we have natural rights to life, liberty and estate, known by reason. "
            "<bookmark mark='b'/>We own our own labour, and by mixing it with things no one owns we make them ours, "
            "provided there is, in his words, enough, and as good, left in common for others: the Lockean proviso. "
            "<bookmark mark='c'/>Government exists by consent, to protect those rights, and a government that "
            "violates them may be resisted. <bookmark mark='d'/>Since few of us ever explicitly consent, Locke said "
            "that enjoying the protection of a state's laws counts as tacit consent to them."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def rousseau(self):
        head = label(r"Rousseau \ (1762)", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"the opening", r"``Man is born free, \ and everywhere he is in chains.''", POW),
                (r"the problem", r"find a form of association in which each, \ uniting with all, \ still obeys only himself and remains as free as before", COM),
                (r"the general will", r"laws express the will of the citizens as citizens, \ aiming at the common good, \ not the sum of private wills", FAIR),
                (r"the danger", r"`forced to be free': \ the general will can be invoked against dissenters", BAD)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Jean-Jacques Rousseau's Social Contract, of 1762, opens with its most famous sentence. <bookmark "
            "mark='a'/>Man is born free, and everywhere he is in chains. <bookmark mark='b'/>The problem is to find a "
            "form of association in which each person, uniting with all, still obeys only himself and remains as free "
            "as before. <bookmark mark='c'/>The answer is the general will: laws that express the will of citizens as "
            "citizens, aiming at the common good, not the sum of their private wills. <bookmark mark='d'/>Its danger "
            "is a phrase of Rousseau's own: whoever refuses to obey the general will shall be forced to be free."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def hume(self):
        head = label(r"Hume against the contract \ (1748)", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"the history", r"almost every government was founded on usurpation or conquest, \ not consent", POW),
                (r"tacit consent", r"like a man carried on board a ship while asleep, \ who must leap into the ocean if he would leave", BAD),
                (r"the real basis", r"we obey because government is useful, \ and because we are used to it", GREY_A),
                (r"the modern turn", r"hypothetical consent: \ not what we agreed to, \ but what we would agree to: \ Rawls", FAIR)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "David Hume's essay Of the Original Contract, of 1748, was the classic critique. <bookmark "
            "mark='a'/>Almost every government in history, he observed, was founded on usurpation or conquest, not "
            "consent. <bookmark mark='b'/>And tacit consent is a fiction: a poor peasant who cannot leave his country "
            "is like a man carried on board a ship while asleep, who must leap into the ocean if he would leave. "
            "<bookmark mark='c'/>We obey, Hume thought, because government is useful and because we are used to it. "
            "<bookmark mark='d'/>The contract tradition survived by changing its question, from what we did agree to, "
            "to what we would agree to under fair conditions. That is Rawls."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
