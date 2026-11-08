from __future__ import annotations

from videos.philosophy.philosophy23.common import *  # noqa: F403


class Evil(VoiceoverScene):
    def construct(self):
        card = chapter_card(9, r"The logical problem of evil", r"Can God and evil both exist?", lit=(1955, 1974),
                            part=PART)
        with self.voiceover("Chapter nine. The logical problem of evil."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.mackie()
        self.defence()
        self.depravity()
        self.natural()

    def mackie(self):
        d = load("mackie")
        hc = history_card(1955, r"J. L. Mackie", r"`Evil and Omnipotence', \ \textit{Mind}", width=5.8,
                          color=HIST).to_corner(UL, buff=0.3)
        rows = VGroup()
        for i, c in enumerate(d["claims"]):
            y = 1.3 - 0.52 * i
            a = label(c["text"], font_size=21, color=WHITE)
            a.move_to([-6.2 + a.width / 2, y, 0])
            b = MathTex(c["formula"].replace("->", r"\to").replace("&", r"\land").replace("~", r"\lnot "),
                        font_size=24, color=ABS)
            b.move_to([3.6 + b.width / 2, y, 0])
            rows.add(VGroup(a, b))
        verdict = label(r"the Reasoner: \ the six together are unsatisfiable; \ drop any one and they are consistent",
                        font_size=21, color=BAD).to_edge(DOWN, buff=1.1)
        p2 = label(r"Part 2's first Price List: \ each position gives up exactly one claim", font_size=19,
                   color=GREY_A).next_to(verdict, DOWN, buff=0.15)
        with self.voiceover(
            "Part 2 opened the series' first Price List with this problem. <bookmark mark='a'/>J. L. Mackie's "
            "version: God exists; God is omnipotent; omniscient; wholly good; a good being that knows and can will "
            "always prevent evil; and there is evil. <bookmark mark='b'/>The Reasoner confirms that the six are "
            "jointly unsatisfiable, and that dropping any one of them restores consistency. Mackie concluded that "
            "theism is not merely unsupported but positively irrational: its central beliefs contradict one "
            "another. <bookmark mark='c'/>The question is which claim a theist can give up at an acceptable price."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.25), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(verdict))
            vo.wait_until("c")
            self.play(FadeIn(p2), Indicate(rows[4], color=GOAL))
        self.clear_scene()

    def defence(self):
        d = load("mackie")
        hc = history_card(1974, r"Alvin Plantinga", r"\textit{God, Freedom, and Evil}", width=5.6,
                          color=HIST).to_corner(UL, buff=0.3)
        rows = VGroup()
        for i, c in enumerate(d["fwd"]):
            y = 1.3 - 0.6 * i
            a = wrapped_label(c["text"], 7.4, 21, WHITE)
            a.move_to([-6.2 + a.width / 2, y, 0])
            b = MathTex(c["formula"].replace("->", r"\to").replace("&", r"\land").replace("~", r"\lnot ").replace(
                "|", r"\lor"), font_size=22, color=ABS)
            b.move_to([2.0 + b.width / 2, y, 0])
            rows.add(VGroup(a, b))
        model = d["fwd_model"]
        mt = label(r"a model: \ " + r", \ ".join(f"${k}$" for k, v in model.items() if v) + r" \ all true",
                   font_size=21, color=OK).to_edge(DOWN, buff=1.0)
        note = label(r"a \textit{defence} needs only a possible story, \ not a true one: \ a theodicy claims the "
                     r"real reason", font_size=19, color=GOAL).next_to(mt, DOWN, buff=0.15)
        with self.voiceover(
            "Alvin Plantinga's free-will defence gives up Mackie's bridge principle and replaces it with a weaker "
            "one. <bookmark mark='a'/>A good being prevents every evil it can, unless preventing it would lose a "
            "greater good. A world with significantly free creatures, who freely do good, is better than a world "
            "without them. But it may be that in every world God could actualize containing free creatures, some of "
            "them do wrong. Plantinga called this transworld depravity: God cannot make free creatures freely do only "
            "good, since then they would not be free. <bookmark mark='b'/>Add that there is evil, and ask the Reasoner "
            "for a model. There is one: every claim true together. <bookmark mark='c'/>That is all a defence needs. "
            "It need not be true, only possible, to show that God and evil are consistent. A theodicy, by contrast, "
            "claims to give God's actual reason. Most philosophers, including many atheists, now agree that the "
            "logical problem, in Mackie's form, has been answered."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.3), run_time=3.5)
            vo.wait_until("b")
            self.play(FadeIn(mt))
            vo.wait_until("c")
            self.play(FadeIn(note))
        self.clear_scene()

    def depravity(self):
        head = label(r"Transworld depravity, \ pictured", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        spots = [(-4.6, 1.0), (-1.55, 1.3), (1.55, 1.0), (4.6, 1.3)]
        isl = VGroup()
        for i, p in enumerate(spots):
            I = island(p, w=2.7, h=1.6, seed=340 + i, color=ARG, name=rf"a world God could actualize", font_size=15)
            folk = VGroup(*[Dot([p[0] - 0.75 + 0.5 * k, p[1] - 0.1 + 0.25 * (k % 2), 0], radius=0.11,
                                color=BAD if k == (i + 1) % 4 else OK) for k in range(4)])
            isl.add(VGroup(I, folk))
        key = VGroup(VGroup(Dot(radius=0.1, color=OK), label(r"freely does right", font_size=17, color=OK)).arrange(
            RIGHT, buff=0.12), VGroup(Dot(radius=0.1, color=BAD), label(r"freely goes wrong at least once",
                                                                        font_size=17, color=BAD)).arrange(RIGHT,
                                                                                                          buff=0.12)
        ).arrange(RIGHT, buff=0.8).move_to([0, -0.4, 0])
        rows = stack([(r"which world is actual depends on what free creatures would freely do: \ counterfactuals "
                       r"of freedom", WHITE),
                      (r"God knows them \ (middle knowledge: \ Molina, \ 1588) \ but does not make them true", ABS),
                      (r"objection: \ what makes such counterfactuals true, \ before anyone exists? \ (Adams, \ "
                       r"1977)", BAD)], font_size=20, aligned_edge=LEFT, width=12.2).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Picture the idea. <bookmark mark='a'/>Each island is a world God could bring about by creating free "
            "people and putting them in circumstances. In every one of them, someone freely goes wrong at least "
            "once. <bookmark mark='b'/>Which of these worlds is actual depends on what the free creatures would "
            "freely do in each situation: on counterfactuals of freedom. <bookmark mark='c'/>On Luis de Molina's "
            "theory of middle knowledge, God knows these counterfactuals but does not make them true; if he did, "
            "the creatures would not be free. <bookmark mark='d'/>Robert Adams objected that nothing could make such "
            "counterfactuals true before the creatures exist, so there is nothing there for God to know. The defence "
            "is consistent; whether its metaphysics is coherent is still debated."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(i) for i in isl], lag_ratio=0.25), FadeIn(key))
            for mk, r in zip("bcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def natural(self):
        head = label(r"And natural evil?", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"the gap", r"earthquakes and cancers are not chosen by any creature", BAD),
            (r"Plantinga", r"perhaps they are caused by free non-human persons: \ consistent, \ if implausible", ABS),
            (r"Swinburne", r"regular natural laws are needed for free action to have known consequences", NAT),
            (r"Hick \ (1966)", r"soul-making: \ a world without suffering could not grow courage and compassion", HUM),
            (r"the evidential turn", r"perhaps consistency is not the issue: \ how \textit{probable} is God, \ "
                                     r"given this much evil?", GOAL),
        ]
        g = rows_table(rows, top=1.9, gap=0.48, width=8.8, x_text=-2.4, label_size=22, text_size=22)
        with self.voiceover(
            "Free will does not obviously cover everything. <bookmark mark='a'/>Earthquakes and cancers are not chosen "
            "by any creature. <bookmark mark='b'/>Plantinga noted that, for a defence, it is enough that they might be "
            "caused by free non-human persons: consistent, if not plausible. <bookmark mark='c'/>Richard Swinburne "
            "argued that a world of regular natural laws is needed for free action to have predictable consequences, "
            "and regular laws bring natural evils with them. <bookmark mark='d'/>John Hick's soul-making theodicy: a "
            "world without suffering could not grow courage, compassion or patience. <bookmark mark='e'/>And so the "
            "debate turned. Perhaps consistency is not the issue. How probable is God, given this much evil, and evil "
            "of these kinds?"
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
