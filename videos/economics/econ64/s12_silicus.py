from __future__ import annotations

from videos.economics.econ64.common import *  # noqa: F403


class Silicus(VoiceoverScene):
    def construct(self):
        card(self, 10, r"Language models as subjects", r"Can a language model stand in for the people economists "
             r"study?", "Chapter ten. Language models as subjects.", lit={2023: r"Horton"}, scale=("person",),
             horizon=("a day",))
        self.idea()
        self.limits()

    def idea(self):
        steps = flow_chain([(r"give the model a persona: \ a renter, \ a libertarian, \ a retiree", NET),
                            (r"put a classic question to it: \ a dictator game, \ a fair price", NET),
                            (r"vary the endowment, \ the price, \ the framing", ALGO),
                            (r"compare its choices with the human results", TRUTHC)],
                           box_w=2.9, box_h=1.35, font_size=18).to_edge(UP, buff=0.8)
        if steps.width > 13.0:
            steps.width = 13.0
        cards = point_cards([
            (r"what Horton found", r"simulated subjects reproduced the direction of classic results: \ social "
             r"preferences in simple games, \ fairness judgements about price rises, \ status-quo bias", NET),
            (r"what it is for", r"a cheap pilot: \ which treatments are worth running, \ how a question reads, \ "
             r"where the effects might be", ALGO),
        ], cols=2, width=12.8, font_size=20).next_to(steps, DOWN, buff=0.7)
        tag = published_tag(r"Horton, \ NBER Working Paper 31122 (2023)", corner=DL, font_size=12)
        title_ = VGroup(label(r"homo silicus", font_size=48, color=NET),
                        label(r"a language model as a simulated subject", font_size=24, color=GREY_A)).arrange(
            DOWN, buff=0.25)
        with self.voiceover(
            "Language models answer questions the way people write about them. John Horton asked whether they "
            "could serve as simulated subjects, homo silicus. <bookmark mark='a'/> Give the model a persona, a "
            "renter, a libertarian, a retiree, <bookmark mark='b'/> put a classic question to it, <bookmark "
            "mark='c'/> vary the endowment, the price or the framing, <bookmark mark='d'/> and compare its choices "
            "with what people did. <bookmark mark='e'/> The simulated subjects reproduced the direction of several "
            "classic results: social preferences in simple games, judgements about whether a price rise is fair, "
            "and a preference for the status quo. <bookmark mark='f'/> Used this way, a model is a cheap pilot: "
            "which treatments are worth running on people, how a question reads, where effects might be."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(title_, shift=UP * 0.1))
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                anims = [FadeIn(steps.boxes[k])]
                if k == 0:
                    anims.append(FadeOut(title_))
                if k:
                    anims.append(GrowArrow(steps.arrows[k - 1]))
                self.play(*anims)
            vo.wait_until("e")
            self.play(FadeIn(cards.cards[0], shift=UP * 0.1))
            vo.wait_until("f")
            self.play(FadeIn(cards.cards[1], shift=UP * 0.1))
        self.clear_scene()

    def limits(self):
        head = label(r"what a simulated subject cannot replace", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.5)
        rows = VGroup(
            VGroup(label(r"1. \ It may have read the answer", font_size=26, color=NET),
                   label(r"classic experiments are in its training text: \ reproducing them may be memory, \ not "
                         r"behaviour", font_size=19, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.1),
            VGroup(label(r"2. \ Nothing is at stake", font_size=26, color=ALGO),
                   label(r"no money, \ no effort, \ no embarrassment: \ the things that make lab behaviour real",
                         font_size=19, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.1),
            VGroup(label(r"3. \ Whose voice?", font_size=26, color=JUDGE),
                   label(r"its average answer reflects the text it was trained on, \ not any population an "
                         r"economist samples", font_size=19, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.1),
            VGroup(label(r"4. \ Small changes, \ large swings", font_size=26, color=HOLD),
                   label(r"wording and model versions move the answers: \ report them, \ and check against people",
                         font_size=19, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.1),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(head, DOWN, buff=0.6)
        with self.voiceover(
            "And what it cannot replace. <bookmark mark='a'/> It may have read the answer: the classic experiments "
            "are in its training text, so reproducing them may be memory rather than behaviour. <bookmark "
            "mark='b'/> Nothing is at stake for it: no money, no effort, no embarrassment, which are what make "
            "behaviour in a laboratory real. <bookmark mark='c'/> Its average answer reflects the text it learned "
            "from, not any population an economist could sample. <bookmark mark='d'/> And small changes in wording, "
            "or a new version of the model, can move the answers a lot. So: report the prompts and versions, and "
            "check against people before believing anything new."
        ) as vo:
            self.play(FadeIn(head))
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.15))
        self.clear_scene()
