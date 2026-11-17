from __future__ import annotations

from videos.psychology.psych39.common import *  # noqa: F403


class Structure(VoiceoverScene):
    def construct(self):
        self.card()
        self.manifold()
        self.pfactor()

    def card(self):
        card = chapter_card(7, r"Comorbidity is the rule", r"One disorder, \ or many at once?",
                            lit={2010: r"RDoC", 2014: r"Caspi et al.", 2017: r"Kotov et al."}, part=PART,
                            scale=("person",), marr=("what",))
        with self.voiceover("Chapter seven. Comorbidity is the rule."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def manifold(self):
        d = load("comorbid")
        head = heading(r"Every diagnosis goes with every other")
        R = np.asarray(d["R"], float)
        hm = heatmap(R, names=list(d["names"]), cell=0.48, font_size=11, values=True, lo=0.0, hi=0.4)
        hm.move_to([-2.6, -0.4, 0])
        rows = rows_of([
            (r"in surveys, \ people with one diagnosis often meet criteria for others: \ comorbidity is the rule, "
             r"\ not the exception", WHITE),
            (rf"Psyche: \ nine diagnoses built from a general factor and three domains, \ in 20{{,}}000 people; \ "
             rf"{pct(d['share_comorbid'])} of those with any diagnosis have two or more", MODEL),
            (r"every correlation is positive: \ a positive manifold, \ as with intelligence tests in Part 32; \ the "
             r"bright blocks are the domains", SYMP),
            (rf"the first principal component carries {pct(d['pc1'])} of the variance", YOU),
        ], 5.0, 19, 0.36).move_to([4.0, -0.2, 0])
        tag = psyche_tag(r"\texttt{clinic.comorbidity}")
        with self.voiceover(
            "Categories have a third problem: people rarely fit just one. <bookmark mark='a'/> In surveys, people "
            "with one diagnosis often meet criteria for others. Comorbidity is the rule, not the exception. "
            "<bookmark mark='b'/> Psyche builds nine diagnoses from a general factor and three domains, in twenty "
            f"thousand people. {spct(d['share_comorbid'])} of those with any diagnosis have two or more. "
            "<bookmark mark='c'/> Every correlation is positive: a positive manifold, like intelligence tests in "
            "Part 32. The bright blocks are the domains: internalizing, externalizing and thought. "
            f"<bookmark mark='d'/> The first principal component carries {spct(d['pc1'])} of the variance."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(hm[1]))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), LaggedStart(*[FadeIn(c) for c in hm[0]], lag_ratio=0.01), run_time=2.0)
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def pfactor(self):
        head = heading(r"A p factor")
        p = word_chip(r"p", color=PERSON, font_size=30, width=1.2).move_to([-3.6, 1.8, 0])
        doms = VGroup(*[word_chip(t, color=c, font_size=16, width=2.0) for t, c in (
            (r"internalizing", SYMP), (r"externalizing", AUTH), (r"thought", MODEL))]).arrange(RIGHT, buff=0.15)
        doms.move_to([-3.6, 0.3, 0])
        dx = VGroup(*[Dot(radius=0.06, color=GREY_A) for _ in range(9)]).arrange(RIGHT, buff=0.5).move_to([-3.6, -1.2, 0])
        lines = VGroup(*[Line(p.get_bottom(), d_.get_top(), color=GREY_D) for d_ in doms])
        lines2 = VGroup(*[Line(doms[k].get_bottom(), dx[j].get_top(), color=GREY_D, stroke_width=1.5)
                          for k, js in enumerate(((0, 1, 2, 3), (4, 5, 6), (7, 8))) for j in js])
        rows = rows_of([
            (r"Caspi and colleagues, \ 2014: \ in the Dunedin cohort, \ followed from 18 to 38, \ one general "
             r"dimension fitted better than three separate domains; \ they called it p, \ after g", WHITE),
            (r"higher p went with more impairment, \ family history and difficult childhoods", PERSON),
            (r"HiTOP, \ 2017: \ a hierarchy from symptoms to syndromes to spectra to p, \ built from data rather "
             r"than committees; \ RDoC, \ 2010: \ research organized by functions across disorders", SYMP),
            (r"Part 32's question returns: \ is a general factor a cause, \ or a summary of things that go "
             r"together?", YOU),
        ], 6.4, 19, 0.36).move_to([3.3, -0.2, 0])
        tag = published_tag(r"Caspi et al.\ (2014); \ Kotov et al.\ (2017)")
        with self.voiceover(
            "In people, the same structure appears. <bookmark mark='a'/> In 2014 Avshalom Caspi and colleagues "
            "analysed the Dunedin cohort, followed from eighteen to thirty-eight, and found one general dimension "
            "fitted better than three separate domains. They called it p, after the g of intelligence. "
            "<bookmark mark='b'/> Higher p went with more impairment, more family history, and more difficult "
            "childhoods. <bookmark mark='c'/> The hierarchical taxonomy, HiTOP, builds a ladder from symptoms to "
            "syndromes to spectra to p, from data rather than committees, and the research domain criteria organize "
            "research by functions that cut across disorders. <bookmark mark='d'/> Part 32's question returns. Is a "
            "general factor a cause, or a summary of things that go together?"
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(dx))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(doms), Create(lines2), FadeIn(p), Create(lines))
            for m, r in zip("bcd", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
