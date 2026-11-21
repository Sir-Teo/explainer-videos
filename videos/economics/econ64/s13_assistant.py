from __future__ import annotations

from videos.economics.econ64.common import *  # noqa: F403


class Assistant(VoiceoverScene):
    def construct(self):
        card(self, 11, r"Language models as research assistants", r"Can a model help find the hypothesis, \ not "
             r"just test it?", "Chapter eleven. Language models as research assistants.",
             lit={2024: r"Ludwig and Mullainathan"}, scale=("person",), horizon=("a year",))
        self.faces()
        self.uses()

    def faces(self):
        steps = flow_chain([(r"mugshots of defendants, \ and the judge's decision", JUDGE),
                            (r"a network predicts the decision from the face alone", ALGO),
                            (r"morph a face to move the prediction", NET),
                            (r"ask people what changed: \ well-groomed, \ heavy-faced", TEXT),
                            (r"a new hypothesis, \ tested on new data", TRUTHC)],
                           box_w=2.35, box_h=1.5, font_size=17).to_edge(UP, buff=0.9)
        if steps.width > 13.2:
            steps.width = 13.2
        rows = VGroup(
            label(r"Mecklenburg County, \ North Carolina: \ the face predicted the judge's decision, \ not the "
                  r"defendant's behaviour", font_size=21, color=WHITE),
            label(r"the features were not in any list of things judges were thought to respond to", font_size=21,
                  color=GREY_A),
            label(r"the algorithm proposes; \ people name it; \ a new sample tests it", font_size=21,
                  color=E.ACCENT),
        ).arrange(DOWN, buff=0.3).next_to(steps, DOWN, buff=0.8)
        tag = published_tag(r"Ludwig and Mullainathan, \ Quarterly Journal of Economics 139(2) (2024)", corner=DL,
                            font_size=12)
        with self.voiceover(
            "Machine learning can also help find what to test. Jens Ludwig and Sendhil Mullainathan returned to "
            "judges, in Mecklenburg County, North Carolina. <bookmark mark='a'/> They took defendants' mugshots and "
            "the judges' decisions, <bookmark mark='b'/> and trained a network to predict the decision from the "
            "face alone. It predicted well: something in faces moves judges. <bookmark mark='c'/> But a network's "
            "reasons are opaque, so they generated morphed faces that moved its prediction up or down, <bookmark "
            "mark='d'/> and asked people what had changed. Two answers stood out: how well-groomed the person "
            "looked, and how heavy-faced. <bookmark mark='e'/> Neither was on any list of things judges were "
            "thought to respond to; each became a hypothesis, tested on new data. <bookmark mark='f'/> The face "
            "predicted the judge, not the defendant: that is a finding about judges. The algorithm proposes, people "
            "name the idea, and a fresh sample tests it."
        ) as vo:
            self.play(FadeIn(tag))
            for k, mk in enumerate("abcde"):
                vo.wait_until(mk)
                anims = [FadeIn(steps.boxes[k])]
                if k:
                    anims.append(GrowArrow(steps.arrows[k - 1]))
                self.play(*anims)
            vo.wait_until("f")
            self.play(FadeIn(rows, shift=UP * 0.1))
        self.clear_scene()

    def uses(self):
        cards = point_cards([
            (r"measurement", r"coding open-ended answers, \ job ads, \ minutes and filings into categories, \ at the "
             r"scale of chapter seven", TEXT),
            (r"the craft", r"writing and checking code, \ cleaning data, \ reading a literature faster", ALGO),
            (r"the rule", r"validate on hand-labelled data, \ correct with prediction-powered inference, \ and report "
             r"the model and the prompts", CAUSE),
            (r"the limit", r"a model trained on past text proposes the likely; \ the surprising still needs a "
             r"design and data", HOLD),
        ], cols=2, width=12.8, font_size=20).move_to(DOWN * 0.2)
        head = label(r"language models in the research workflow", font_size=30, color=E.ACCENT).to_edge(UP,
                                                                                                    buff=0.5)
        with self.voiceover(
            "Language models now sit in many research workflows. <bookmark mark='a'/> In measurement: coding "
            "open-ended survey answers, job advertisements, minutes and filings into categories, at the scale of "
            "chapter seven. <bookmark mark='b'/> In the craft: writing and checking code, cleaning data, reading a "
            "literature faster. <bookmark mark='c'/> The rule is chapter seven's: validate against hand-labelled "
            "data, correct the estimates with prediction-powered inference, and report the model and the prompts, "
            "so others can check. <bookmark mark='d'/> And the limit: a model trained on past text proposes what "
            "is likely. What is surprising still needs a research design and data."
        ) as vo:
            self.play(FadeIn(head))
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                self.play(FadeIn(cards.cards[k], shift=UP * 0.1))
        self.clear_scene()
