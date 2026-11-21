from __future__ import annotations

from videos.economics.econ64.common import *  # noqa: F403


def courtroom(n=24, seed=64, released_mask=None, outcomes=None, show_outcomes=True):
    """A row of defendants before a bench: the released walk out (green, their outcome then seen: a tick for coming
    back to court, a cross for failing to); the detained stay (grey, a question mark: what they would have done is
    never seen)."""
    rng = np.random.default_rng(seed)
    rel = rng.random(n) < 0.7 if released_mask is None else np.asarray(released_mask)
    out = rng.random(n) < 0.15 if outcomes is None else np.asarray(outcomes)
    bench = VGroup(RoundedRectangle(width=2.4, height=0.6, corner_radius=0.1, stroke_color=JUDGE, stroke_width=2,
                                    fill_color=JUDGE, fill_opacity=0.15),
                   label(r"the judge", font_size=18, color=JUDGE))
    bench[1].move_to(bench[0])
    people = VGroup()
    marks = VGroup()
    for k in range(n):
        col = GAIN if rel[k] else GREY_C
        d = Circle(radius=0.17, stroke_color=col, stroke_width=2, fill_color=col, fill_opacity=0.3)
        d.move_to([(k % 12 - 5.5) * 0.62, -0.9 - (k // 12) * 0.75, 0])
        people.add(d)
        if not show_outcomes:
            continue
        if rel[k]:
            m = label(r"$\times$" if out[k] else r"$\checkmark$", font_size=20, color=COST if out[k] else GAIN)
        else:
            m = label(r"?", font_size=20, color=GREY_B)
        marks.add(m.move_to(d))
    bench.next_to(people, UP, buff=0.6)
    return VGroup(bench, people, marks), rel, out


class Hook(VoiceoverScene):
    def construct(self):
        self.story()
        self.court()
        self.question()
        self.title()
        self.objectives()

    def story(self):
        cards = VGroup(
            history_card(r"every day", r"a judge's decision", r"for each person arrested, \ a judge decides whether "
                         r"they wait for trial at home or in jail, \ guessing who would not come back to court",
                         color=JUDGE, width=11.2, font_size=21),
            history_card(r"2008--13", r"New York City, \ 758,027 cases", r"economists train boosted decision trees on "
                         r"the same records the judges saw, \ and predict who will fail to appear", color=ALGO,
                         width=11.2, font_size=21),
            history_card(r"a quarter", r"less crime, \ or two fifths fewer jailed", r"releasing in the algorithm's "
                         r"order: \ up to 25\% less crime with the same number jailed, \ or up to 42\% fewer jailed "
                         r"with no more crime", color=GAIN, width=11.2, font_size=21),
        ).arrange(DOWN, buff=0.35).move_to(UP * 0.3)
        tag = published_tag(r"Kleinberg, \ Lakkaraju, \ Leskovec, \ Ludwig and Mullainathan, \ Quarterly Journal of "
                            r"Economics 133(1) (2018)", corner=DL, font_size=12)
        with self.voiceover(
            "Every day, in courts across the United States, a judge looks at a person who has just been arrested "
            "and decides whether they will wait for their trial at home or in jail. The law asks the judge, in "
            "effect, to guess: will this person come back to court? <bookmark mark='a'/> Jon Kleinberg, Himabindu "
            "Lakkaraju, Jure Leskovec, Jens Ludwig and Sendhil Mullainathan took seven hundred and fifty-eight "
            "thousand such decisions in New York City, from 2008 to 2013, and trained an algorithm on the same "
            "records the judges had seen, to predict who would fail to appear. <bookmark mark='b'/> Releasing "
            "people in the order of its predictions, they estimated, could cut crime by up to a quarter with the "
            "same number jailed, or jail up to two fifths fewer people with no more crime."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.1), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(cards[2], shift=UP * 0.1))
        self.clear_scene()

    def court(self):
        g, rel, out = courtroom()
        bench, people, marks = g
        head = label(r"the Island's bail court", font_size=26, color=E.ACCENT).to_edge(UP, buff=0.4)
        rel_marks = VGroup(*[m for m, r in zip(marks, rel) if r])
        det_marks = VGroup(*[m for m, r in zip(marks, rel) if not r])
        note1 = label(r"released: \ we see whether they came back", font_size=21, color=GAIN)
        note2 = label(r"detained: \ we never see what they would have done", font_size=21, color=GREY_B)
        VGroup(note1, note2).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(DOWN, buff=0.5)
        tag = island_tag(r"the Island: \ an illustration", corner=DR, font_size=12)
        with self.voiceover(
            "That sounds like a triumph of prediction, and in part it is. But look at what the data contain. "
            "<bookmark mark='a'/> The Island's bail court sees a line of defendants. The judge releases most of "
            "them. <bookmark mark='b'/> For the released, we later see whether they came back to court: a tick, or "
            "a cross. <bookmark mark='c'/> For the detained, we see nothing. What they would have done is never "
            "recorded, and the judge may have detained them for reasons the records do not show. Any algorithm is "
            "trained, and judged, on the people the judges let go. The hard part is not the prediction. It is "
            "knowing what would have happened."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(bench), FadeIn(people))
            vo.wait_until("a")
            self.play(*[people[k].animate.shift(DOWN * 0.15) for k in range(len(people)) if rel[k]], run_time=1.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(m, scale=1.3) for m in rel_marks], lag_ratio=0.08), FadeIn(note1))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(m) for m in det_marks], lag_ratio=0.1), FadeIn(note2))
        self.clear_scene()

    def question(self):
        q = wrapped_label(ASK, 12.0, 34, E.ACCENT).to_edge(UP, buff=0.8)
        rows = VGroup(
            label(r"when is a decision a prediction problem, \ and when a causal one?", font_size=26, color=ALGO),
            label(r"how can an algorithm be judged on outcomes the decision hid?", font_size=26, color=JUDGE),
            label(r"can machine learning estimate causal effects honestly?", font_size=26, color=CAUSE),
            label(r"can it solve models, \ play markets, \ or stand in for people?", font_size=26, color=NET),
            label(r"and what does it owe to fairness?", font_size=26, color=GROUPB),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(q, DOWN, buff=0.6)
        with self.voiceover(
            "The question: what does machine learning change in how economics is done? <bookmark mark='a'/> When "
            "is a decision a prediction problem, and when a causal one? <bookmark mark='b'/> How can an algorithm be "
            "judged on outcomes the decision itself hid? <bookmark mark='c'/> Can machine learning estimate causal "
            "effects without fooling us? <bookmark mark='d'/> Can it solve our models, play in our markets, or "
            "stand in for the people we study? <bookmark mark='e'/> And what does it owe to fairness?"
        ) as vo:
            self.play(FadeIn(q, shift=DOWN * 0.2))
            for mk, r_ in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
        self.clear_scene()

    def title(self):
        g, _, _ = courtroom(show_outcomes=False)
        g = g[:2].scale(0.5)
        tt = label(r"Economics, Built", font_size=60)
        sub = label(r"Part 64 \ $\cdot$ \ Machines that Learn", font_size=34, color=E.ACCENT)
        VGroup(g, tt, sub).arrange(DOWN, buff=0.45)
        with self.voiceover("Economics, Built. Part sixty-four: machines that learn."):
            self.play(FadeIn(g), run_time=1.4)
            self.play(Write(tt), run_time=1.2)
            self.play(FadeIn(sub, shift=UP * 0.15))
        self.wait(1.0)
        self.clear_scene()

    def objectives(self):
        head = label(r"Act XII \ $\cdot$ \ The Frontier", font_size=40, color=E.ACCENT)
        obj = objectives_card([
            r"prediction policy problems, \ selective labels, \ and why a forecast is not a policy",
            r"double machine learning, \ causal forests and policy learning",
            r"text and images as data, \ and inference with predicted labels",
            r"neural networks that solve models, \ and agents that learn to price",
            r"language models as subjects and assistants, \ and fairness",
        ], color=E.ACCENT, font_size=28, width=13.0)
        with self.voiceover(
            "Part sixty-three followed shocks along networks. This part turns to the machines that learn from data. "
            "By the end you will know <bookmark mark='a'/> which decisions are prediction problems, why the labels a "
            "decision hides make evaluation hard, and why a good forecast can be a bad policy; <bookmark mark='b'/> "
            "how double machine learning and causal forests estimate effects without letting the learner's errors "
            "leak in; <bookmark mark='c'/> how text and images become data, and how to do inference when the labels "
            "are predicted; <bookmark mark='d'/> how a neural network can solve an economic model, and what happens "
            "when learning agents set prices; <bookmark mark='e'/> and what language models can and cannot do for "
            "economists, and why no score can be fair in every sense at once."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(head), FadeIn(obj.head), FadeIn(obj.rows[0], shift=RIGHT * 0.2))
            for mk, r_ in zip("bcde", obj.rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
        self.clear_scene()
