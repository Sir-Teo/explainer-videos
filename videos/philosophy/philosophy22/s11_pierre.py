from __future__ import annotations

from videos.philosophy.philosophy22.common import *  # noqa: F403


class Pierre(VoiceoverScene):
    def construct(self):
        card = chapter_card(10, r"A puzzle about belief", r"Does Pierre believe that London is pretty?",
                            lit=(1979, 1986), part=PART)
        with self.voiceover("Chapter ten. A puzzle about belief."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.story()
        self.price()
        self.paderewski()

    def story(self):
        hc = history_card(1979, r"Saul Kripke", r"`A Puzzle about Belief'", width=5.6, color=HIST).to_corner(
            UL, buff=0.3)
        fr = island([-3.6, 0.3, 0], w=3.6, h=1.9, seed=170, color=WORLD, name=r"France, \ as a boy")
        en = island([2.6, 0.3, 0], w=3.6, h=1.9, seed=171, color=DESC, name=r"London, \ years later")
        pf = person([-3.6, 0.55, 0], color=NAME, name=r"Pierre", font_size=16)
        pe = person([2.6, 0.55, 0], color=NAME, name=r"Pierre", font_size=16)
        s1 = label(r"`Londres est jolie.'", font_size=21, color=WORLD).move_to([-3.6, -0.35, 0])
        s2 = label(r"`London is not pretty.'", font_size=21, color=DESC).move_to([2.6, -0.35, 0])
        arr = Arrow([-1.6, 0.3, 0], [0.6, 0.3, 0], buff=0.05, color=GREY_B, stroke_width=3)
        rows = stack([(r"he learns English by immersion, \ in an unattractive part of the city, \ and never "
                       r"connects `London' with `Londres'", WHITE),
                      (r"he sincerely assents to both, \ and he is no worse a logician than you", GOAL),
                      (r"does Pierre believe that London is pretty? \ every answer seems wrong", BAD)],
                     font_size=21, aligned_edge=LEFT, width=12.0).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Kripke's puzzle about belief, from 1979. <bookmark mark='a'/>Pierre grows up in France, speaking only "
            "French. From pictures and stories he comes to believe that London is beautiful, and he says: Londres est "
            "jolie. <bookmark mark='b'/>Later he moves to London, to an unattractive part of the city, and learns "
            "English from the people around him, not by translation. He comes to say, sincerely: London is not "
            "pretty. <bookmark mark='c'/>He never realizes that London is the city he called Londres. "
            "<bookmark mark='d'/>He assents sincerely to both sentences, and he is a competent logician. "
            "<bookmark mark='e'/>Does Pierre believe that London is pretty? Yes seems wrong, because he believes it "
            "is not. No seems wrong, because he has never given up his French belief."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(fr), FadeIn(pf), FadeIn(s1))
            vo.wait_until("b")
            self.play(GrowArrow(arr), FadeIn(en), FadeIn(pe), FadeIn(s2))
            for mk, r in zip("cde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def price(self):
        d = load("pierre")
        claims = [(c["key"], c["text"]) for c in d["claims"]]
        assert d["mcs"] == [["D"], ["T"], ["R"], ["M"]]
        pl = PriceList(claims, mus=[tuple(m) for m in d["mus"]], radius=2.9, width=3.7, font_size=19,
                       center=[0, -0.5, 0], title=r"The Price List: \ Pierre")
        positions = [(("D",), r"Kripke", r"our practice of reporting belief breaks down here: \ the question has "
                                         r"no clear answer"),
                     (("T",), r"no translation", r"the French belief cannot be reported in English: \ but see "
                                                 r"Paderewski"),
                     (("R",), r"Salmon; \ Soames", r"Pierre believes both, \ under two guises: \ he cannot detect the "
                                                  r"clash, \ so he is not irrational"),
                     (("M",), r"Frege; \ two dimensions", r"`Londres' and `London' differ in sense, \ or in primary "
                                                          r"intension, \ for Pierre")]
        with self.voiceover(
            "The puzzle is a Price List. <bookmark mark='a'/>Disquotation: a sincere, reflective speaker who assents "
            "to a sentence believes what it says. Translation: what is true in French stays true translated into "
            "English. Pierre is rational: he holds no contradictory beliefs that reflection would reveal. And "
            "Millianism: Londres and London say the same, since a name contributes only its bearer. "
            "<bookmark mark='b'/>Together they make Pierre believe that London is pretty and that it is not, while "
            "being rational. All four cannot hold. <bookmark mark='c'/>Kripke himself concluded that our practice of "
            "reporting beliefs is strained to the breaking point in such cases, and the question may have no clear "
            "answer. <bookmark mark='d'/>One might deny translation, but the next example "
            "shows that translation is not the culprit. <bookmark mark='e'/>Millians such as Nathan Salmon and "
            "Scott Soames keep the names and give up the rationality principle as stated: Pierre believes both, "
            "under two different guises, and since he cannot detect the clash, he is not irrational. "
            "<bookmark mark='f'/>Fregeans deny Millianism: for Pierre the two names differ in sense, or, in this "
            "part's terms, in primary intension."
        ) as vo:
            self.play(FadeIn(pl.title))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c) for c in pl.cards], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(Create(pl.conflict))
            first = True
            for mk, (mcs, name, who) in zip("cdef", positions):
                vo.wait_until(mk)
                if not first:
                    self.play(*pl.reset())
                first = False
                anims, centre = pl.position(mcs, name, who, width=3.0)
                self.play(*anims)
        self.clear_scene()

    def paderewski(self):
        head = label(r"Paderewski: \ the puzzle without translation", font_size=30, color=CONN).to_edge(UP,
                                                                                                    buff=0.35)
        p = person([0, 1.3, 0], color=NAME, name=r"Ignacy Paderewski", font_size=19, r=0.22)
        l1 = label(r"`Paderewski the pianist had musical talent'", font_size=20, color=WORLD).move_to([-3.5, 0.0, 0])
        l2 = label(r"`Paderewski the statesman had none'", font_size=20, color=DESC).move_to([3.5, 0.0, 0])
        a1 = Arrow(p.dot.get_left(), l1.get_top() + UP * 0.12, buff=0.2, color=WORLD, stroke_width=2.5)
        a2 = Arrow(p.dot.get_right(), l2.get_top() + UP * 0.12, buff=0.2, color=DESC, stroke_width=2.5)
        rows = stack([(r"Peter hears of a pianist and of a Polish prime minister, \ both called Paderewski, \ and "
                       r"thinks them two men", WHITE),
                      (r"one language, \ one name: \ only disquotation is needed, \ and the puzzle returns", GOAL),
                      (r"so belief reports are hyperintensional: \ they distinguish what is necessarily the same "
                       r"\ (chapter 12)", ABS),
                      (r"and the theory of names meets the theory of mind: \ Parts 27 and 29", GREY_A)],
                     font_size=21, aligned_edge=LEFT, width=12.0).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Kripke gave a second case to show that translation is not to blame. <bookmark mark='a'/>Peter hears of "
            "Paderewski the pianist, and of Paderewski the Polish statesman, and takes them to be two men; in fact "
            "they are one. <bookmark mark='b'/>He says Paderewski had musical talent, and also, sincerely, that "
            "Paderewski had none. <bookmark mark='c'/>One language, one name. Only disquotation is needed, and the "
            "puzzle returns. <bookmark mark='d'/>The lesson most take is that belief reports are hyperintensional: "
            "they can distinguish contents that are necessarily equivalent, which chapter twelve makes room for. "
            "<bookmark mark='e'/>And it is where the theory of names meets the theory of mind, in Parts 27 and 29."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(p), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(GrowArrow(a1), FadeIn(l1), GrowArrow(a2), FadeIn(l2))
            for mk, r in zip("cde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
