from __future__ import annotations

from videos.psychology.psych40.common import *  # noqa: F403


class Stress(VoiceoverScene):
    def construct(self):
        self.card()
        self.events()
        self.gene()

    def card(self):
        card = chapter_card(11, r"Stress, \ life events and genes", r"Who becomes depressed after a loss?",
                            lit={1978: r"Brown \& Harris", 2003: r"Caspi et al.", 2019: r"Border et al."}, part=PART,
                            scale=("gene", "person"), marr=("why",))
        with self.voiceover("Chapter eleven. Stress, life events and genes."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def events(self):
        head = heading(r"Social origins")
        rows = rows_of([
            (r"Brown and Harris, \ 1978: \ interviews with women in a London borough", WHITE),
            (r"severe life events, \ above all losses and humiliations, \ often came before the onset of "
             r"depression", AUTH),
            (r"vulnerability factors, \ such as lacking a close confiding relationship, \ made a depression after "
             r"such an event more likely", PERSON),
            (r"the diathesis-stress frame of Part 39, \ in a community: \ who the stress lands on matters as much "
             r"as the stress", YOU),
        ], 12.4, 23, 0.46).move_to([0, -0.3, 0])
        tag = historical_tag(r"Brown \& Harris (1978)")
        with self.voiceover(
            "Depression often follows something. <bookmark mark='a'/> In 1978 George Brown and Tirril Harris "
            "reported interviews with women in a London borough. <bookmark mark='b'/> Severe life events, above all "
            "losses and humiliations, often came before the onset of depression. <bookmark mark='c'/> And "
            "vulnerability factors, such as lacking a close confiding relationship, made depression after such an "
            "event more likely. <bookmark mark='d'/> It's the diathesis-stress frame of Part 39, in a community. Who "
            "the stress lands on matters as much as the stress."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def gene(self):
        head = heading(r"A gene, \ stress, \ and a failed interaction")
        A = axes([-0.4, 3.4], [0, 1.0], x_length=4.6, y_length=3.0, xticks=[0, 1, 2, 3], yticks=None,
                 xfmt=lambda v: f"{v:.0f}", xlabel=r"stressful life events", ylabel=r"chance of depression",
                 center=[-3.6, -0.2, 0], font_size=13)
        x = np.linspace(0, 3, 30)
        fan = VGroup(curve(A.ax, x, 0.15 + 0.17 * x, AUTH, stroke_width=4),
                     curve(A.ax, x, 0.15 + 0.06 * x, SYMP, stroke_width=4))
        par = VGroup(curve(A.ax, x, 0.17 + 0.09 * x, GREY_A, stroke_width=3),
                     curve(A.ax, x, 0.15 + 0.09 * x, GREY_A, stroke_width=3))
        lf = label(r"2003: \ the lines fan out", font_size=13, color=AUTH).move_to(A.ax.c2p(1.0, 0.85))
        lp = label(r"later: \ they run together", font_size=13, color=GREY_A).move_to(A.ax.c2p(2.3, 0.2))
        note = label(r"schematic", font_size=13, color=GREY_B).next_to(A, DOWN, buff=0.35)
        rows = rows_of([
            (r"Caspi and colleagues, \ 2003: \ in the Dunedin cohort, \ stressful events predicted depression more "
             r"strongly in carriers of a short variant of the serotonin transporter gene", WHITE),
            (r"a celebrated gene-by-environment interaction, \ cited thousands of times", PERSON),
            (r"Culverhouse and colleagues, \ 2018, \ pooling over 38{,}000 people, \ and Border and colleagues, \ "
             r"2019, \ found no support for it", AUTH),
            (r"Part 9's lesson: \ depression is highly polygenic, \ and single candidate genes of large effect did "
             r"not survive large samples", YOU),
        ], 6.0, 19, 0.36).move_to([3.4, -0.2, 0])
        tag = published_tag(r"Caspi et al.\ (2003); \ Culverhouse et al.\ (2018); \ Border et al.\ (2019)")
        with self.voiceover(
            "Then came a gene. <bookmark mark='a'/> In 2003 Avshalom Caspi and colleagues reported from the Dunedin "
            "cohort that stressful events predicted depression more strongly in carriers of a short variant of the "
            "serotonin transporter gene. <bookmark mark='b'/> It became a celebrated gene-by-environment "
            "interaction, cited thousands of times. <bookmark mark='c'/> But in 2018 Robert Culverhouse and "
            "colleagues pooled data on more than thirty-eight thousand people, and in 2019 Richard Border and "
            "colleagues tested the candidate genes in large samples. Neither found support. <bookmark mark='d'/> "
            "It's Part 9's lesson. Depression is highly polygenic, and single candidate genes of large effect didn't "
            "survive large samples."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(note))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), Create(fan), FadeIn(lf))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeOut(fan), FadeOut(lf), Create(par), FadeIn(lp))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
