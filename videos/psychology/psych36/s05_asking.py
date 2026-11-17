from __future__ import annotations

from videos.psychology.psych36.common import *  # noqa: F403


class Asking(VoiceoverScene):
    def construct(self):
        self.card()
        self.desirability()
        self.listexp()

    def card(self):
        card = chapter_card(4, r"Measuring by asking", r"How do you ask a question people will not answer honestly?",
                            lit=(), part=PART, scale=("person",), marr=("what",))
        with self.voiceover("Chapter four. Measuring by asking."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def desirability(self):
        head = heading(r"What people will say")
        rows = rows_of([
            (r"the oldest measure of prejudice is a questionnaire: \ agree or disagree with statements about a group",
             WHITE),
            (r"over the second half of the twentieth century, \ the share of Americans endorsing openly prejudiced "
             r"statements fell steeply", GOOD),
            (r"but answers depend on what it is acceptable to say: \ social desirability, \ Part 3's problem for "
             r"self-report", AUTH),
            (r"so did prejudice fall, \ or only what people will admit? \ two routes around the problem: \ ask so "
             r"that nobody's answer is revealed, \ or stop asking", YOU),
        ], 12.4, 22, 0.42).move_to([0, -0.3, 0])
        with self.voiceover(
            "The oldest measure of prejudice is a questionnaire: agree or disagree with statements about a group. "
            "<bookmark mark='a'/> Over the second half of the twentieth century, the share of Americans endorsing "
            "openly prejudiced statements fell steeply. <bookmark mark='b'/> But answers depend on what it's "
            "acceptable to say. That's social desirability, Part 3's problem for every self-report. "
            "<bookmark mark='c'/> So did prejudice fall, or only what people will admit? There are two routes "
            "around the problem. Ask in a way that reveals nobody's answer, or stop asking."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0]))
            for m, r in zip("abc", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def listexp(self):
        d = load("listexp")
        ratio = d["sd"] / np.sqrt(0.2 * 0.8 / 1000)
        frac = {2: "half", 3: "third", 4: "quarter", 5: "fifth", 6: "sixth"}[round(ratio)]
        head = heading(r"The list experiment")
        ctrl = VGroup(*[label(t, font_size=17, color=GREY_A) for t in (
            r"I follow a football team", r"I have been abroad this year", r"I own a bicycle")]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.15)
        sens = label(r"+ \ the sensitive statement", font_size=17, color=AUTH)
        cards = VGroup(
            VGroup(label(r"half the sample", font_size=17, color=CROWD), ctrl.copy()).arrange(DOWN, aligned_edge=LEFT,
                                                                                              buff=0.2),
            VGroup(label(r"the other half", font_size=17, color=AUTH), ctrl.copy(), sens).arrange(
                DOWN, aligned_edge=LEFT, buff=0.2)).arrange(RIGHT, buff=0.6, aligned_edge=UP).move_to([-3.4, 1.4, 0])
        how = label(r"``how many of these are true for you?''", font_size=18, color=YOU).next_to(cards, DOWN, buff=0.3)
        A = axes([0.1, 0.3], [0, 1.0], x_length=4.6, y_length=1.7, xticks=[0.1, 0.2, 0.3], yticks=None,
                 xfmt=lambda v: f"{v:.1f}", xlabel=r"estimated prevalence", center=[-3.4, -2.0, 0], font_size=14)
        est = np.asarray(d["estimates"], float)
        edges = np.linspace(0.05, 0.35, 31)
        h, _ = np.histogram(est, bins=edges)
        mids = (edges[:-1] + edges[1:]) / 2
        keep = (mids >= 0.1) & (mids <= 0.3)
        hb = bars(A.ax, mids[keep], h[keep] / h.max() * 0.95, MODEL, width=0.009)
        true = DashedLine(A.ax.c2p(0.2, 0), A.ax.c2p(0.2, 1.0), color=GOOD)
        rows = rows_of([
            (r"nobody says which statements are true, \ only how many: \ no single answer reveals the sensitive one",
             WHITE),
            (r"the difference between the halves' average counts estimates how common the sensitive one is", CROWD),
            (rf"Psyche runs 2{{,}}000 surveys of 1{{,}}000 people, \ true prevalence 20\%: \ the estimates centre on "
             rf"the truth, \ with a spread of about {100 * d['sd']:.0f} points", MODEL),
            (rf"the price of privacy is precision: \ a direct question to the same 1{{,}}000 people would have about "
             rf"1/{ratio:.0f} of the uncertainty, \ if people answered it honestly", YOU),
        ], 6.0, 20, 0.36).move_to([3.4, -0.2, 0])
        tag = psyche_tag(r"simulated: \ the item-count technique")
        with self.voiceover(
            "Here's the first route, the list experiment. <bookmark mark='a'/> Half the sample sees a list of "
            "harmless statements and says how many are true for them. The other half sees the same list plus the "
            "sensitive statement. Nobody says which ones are true, only how many, so no single answer reveals the "
            "sensitive one. <bookmark mark='b'/> The difference between the two halves' average counts estimates "
            "how common the sensitive one is. <bookmark mark='c'/> Psyche runs two thousand surveys of a thousand "
            "people each, with a true prevalence of twenty percent. The estimates centre on the truth. "
            "<bookmark mark='d'/> The price of privacy is precision. A direct question to the same thousand people "
            f"would have about a {frac} of the "
            "uncertainty, if people answered it honestly."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(cards), FadeIn(how))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(A), FadeIn(hb), Create(true), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
