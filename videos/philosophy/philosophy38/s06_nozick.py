from __future__ import annotations

from videos.philosophy.philosophy38.common import *  # noqa: F403


class Nozick(VoiceoverScene):
    def construct(self):
        card = chapter_card(5, r"Entitlement", r"Can a just distribution be upset by free exchange?", lit=(1974,), part=PART)
        with self.voiceover("Chapter five. Entitlement."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.entitlement()
        self.wilt()
        self.price()
        self.proviso()
        self.leftlib()

    def entitlement(self):
        head = history_card(1974, r"Robert Nozick", r"\textit{Anarchy, \ State, \ and Utopia}", width=6.0, color=HIST).to_corner(UL, buff=0.3)
        rows = [
                (r"historical, \ not patterned", r"a distribution is just if it arose by just steps, \ whatever pattern it makes", LIB),
                (r"acquisition", r"how unowned things may come to be owned: \ Locke's mixing, \ under a proviso", MKT),
                (r"transfer", r"holdings justly held may be given or exchanged by consent", MKT),
                (r"rectification", r"past injustice in either must be corrected", FAIR),
                (r"the minimal state", r"protection against force, \ theft and fraud, \ and enforcement of contracts: \ nothing more is justified", BAD)]
        g = rows_table(rows, top=1.0, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Robert Nozick's Anarchy, State, and Utopia, of 1974, answered Rawls from the libertarian side. <bookmark "
            "mark='a'/>Justice in holdings is historical, not patterned: a distribution is just if it arose by just "
            "steps, whatever pattern it happens to make. <bookmark mark='b'/>There are principles of just "
            "acquisition, how unowned things come to be owned, following Locke with a proviso; <bookmark mark='c'/>of "
            "just transfer, by gift or exchange; <bookmark mark='d'/>and of rectification, correcting past injustice "
            "in either. <bookmark mark='e'/>Only a minimal state is justified: protection against force, theft and "
            "fraud, and the enforcement of contracts. Taxation of earnings for redistribution, he said, is on a par "
            "with forced labour."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def wilt(self):
        d = load("wilt")
        head = label(r"Wilt Chamberlain, \ as a toy economy", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        assert (d["n"], d["start"], d["fee"], d["games"]) == (1000000, 1000.0, 0.25, 40)
        assert (d["wilt"], d["others"], d["gini_after"], d["share_of_wilt"]) == (10001000.0, 990.0, 0.01, 0.01)
        hd = [r"", r"\text{everyone else}", r"\text{Wilt}", r"\text{Gini}"]
        cells = [[label(r"D1: \ the pattern you favour", font_size=18, color=FAIR), label(r"\$1,000", font_size=18),
                  label(r"\$1,000", font_size=18), label(r"0", font_size=18)],
                 [label(r"D2: \ after one season", font_size=18, color=MKT), label(r"\$990", font_size=18),
                  label(r"\$10,001,000", font_size=18, color=MKT), label(r"0.01", font_size=18)]]
        grid = ValueGrid(hd, cells, col_w=[4.2, 2.6, 2.8, 1.4], cell_h=0.6, font_size=18).move_to([0, 1.0, 0])
        foot = stack([(r"a million fans each drop 25 cents in a box for Wilt at each of 40 home games", GREY_A),
                      (r"every transfer is voluntary, \ and no one else's holdings are touched", LIB),
                      (r"Wilt now holds 1\% of all wealth, \ ten thousand times anyone else", MKT),
                      (r"liberty upsets patterns: \ to keep D1, \ forbid capitalist acts between consenting adults",
                       BAD)],
                     font_size=19, buff=0.2).move_to([0, -1.5, 0])
        with self.voiceover(
            "Nozick's most famous argument is a story, which the Reasoner runs as a toy economy. <bookmark "
            "mark='a'/>Start with whatever distribution you think just, say equality: a million people with a "
            "thousand dollars each. One of them is the basketball player Wilt Chamberlain. <bookmark mark='b'/>Wilt "
            "signs a contract: at each home game, every fan who wants to watch drops twenty five cents in a box for "
            "him. Over forty games, a million fans each pay ten dollars. <bookmark mark='c'/>Every transfer is "
            "voluntary, and no one else's holdings are touched. <bookmark mark='d'/>At the end of the season Wilt has "
            "ten million and one thousand dollars, ten thousand times anyone else, and one percent of all the wealth "
            "there is. <bookmark mark='e'/>Liberty upsets patterns, Nozick concluded: to preserve any favoured "
            "distribution, a state would have to forbid capitalist acts between consenting adults."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), Create(grid.rule))
            vo.wait_until("a")
            self.play(*[FadeIn(c) for c in grid.cell[0]])
            vo.wait_until("b")
            self.play(FadeIn(foot[0]))
            vo.wait_until("c")
            self.play(FadeIn(foot[1]))
            vo.wait_until("d")
            self.play(*[FadeIn(c) for c in grid.cell[1]], FadeIn(foot[2]))
            vo.wait_until("e")
            self.play(FadeIn(foot[3]))
        self.clear_scene()

    def price(self):
        d = load("tetrad")
        claims = [(c["key"], c["text"]) for c in d["claims"]]
        assert d["mus"] == [["ARISES", "D1", "TRANSFER", "UNJUST"]]
        assert sorted(d["mcs"]) == [["ARISES"], ["D1"], ["TRANSFER"], ["UNJUST"]]
        pl = PriceList(claims, mus=[tuple(m) for m in d["mus"]], radius=2.6, width=3.8, font_size=19,
                       center=[0, -0.6, 0], title=r"The Price List: \ Wilt Chamberlain")
        positions = [(("UNJUST",), r"accept D2", r"Nozick: \ justice is historical, \ not patterned"),
                     (("TRANSFER",), r"transfers can corrupt", r"Cohen \ (1995): \ the fans did not foresee the power "
                                                              r"they handed Wilt"),
                     (("ARISES",), r"not truly voluntary", r"background inequality and taxation as part of the deal: \ "
                                                          r"Murphy and Nagel \ (2002)"),
                     (("D1",), r"no pattern was just", r"only entitlements: \ again Nozick's view, \ from the other "
                                                        r"side")]
        with self.voiceover(
            "Four claims cannot all be true. <bookmark mark='a'/>D1, the distribution you favour, is just. Whatever "
            "arises from a just situation by voluntary exchange is just. D2 arises from D1 by voluntary exchange. And "
            "D2, with Wilt's fortune, is unjust. <bookmark mark='b'/>Something must go. <bookmark mark='c'/>Nozick "
            "accepts D2: justice is historical, a matter of how holdings came about, not of the pattern they make. "
            "<bookmark mark='d'/>G. A. Cohen denied that voluntary transfers always preserve justice: the fans did "
            "not foresee the power over others they were handing to Wilt and his heirs. <bookmark mark='e'/>Others "
            "deny that the transfers are fully voluntary against a background of unequal power, or note, with Liam "
            "Murphy and Thomas Nagel, that taxation is part of the deal under which any property is held. <bookmark "
            "mark='f'/>And one can deny that D1 was ever just in the patterned sense, which is Nozick's view again, "
            "approached from the other side."
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

    def proviso(self):
        head = label(r"The proviso, \ and history", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"the Lockean proviso", r"an appropriation is just only if it leaves others no worse off than they would be without it", LIB),
                (r"the baseline problem", r"worse off than what? \ a state of nature, \ or a fair share? \ the proviso can be weak or very strong", BAD),
                (r"rectification", r"most present holdings descend from conquest and expropriation: \ Nozick allowed that rectifying them might need large transfers", FAIR),
                (r"self-ownership", r"Cohen, \ \textit{Self-Ownership, \ Freedom, \ and Equality} \ (1995): \ the premise the left must answer", COM)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "The theory's weak points are at its foundations. <bookmark mark='a'/>The Lockean proviso, as Nozick "
            "reads it, says an appropriation is just only if it leaves others no worse off than they would have been "
            "without it. <bookmark mark='b'/>But worse off than what? Compared with a state of nature, almost any "
            "appropriation passes; compared with a fair share, almost none does. <bookmark mark='c'/>And since most "
            "present holdings descend from conquest and expropriation, Nozick himself allowed that rectifying them "
            "might require large transfers, perhaps even something like the difference principle as a rule of thumb. "
            "<bookmark mark='d'/>G. A. Cohen's Self-Ownership, Freedom, and Equality, of 1995, argued that the real "
            "premise is self-ownership, and that the left must answer it directly."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def leftlib(self):
        head = label(r"Libertarianism, \ from the left", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"Paine \ (1797)", r"\textit{Agrarian Justice}: \ the earth was common property; \ pay everyone \pounds15 at 21, \ from a tax on inheritance", HIST),
                (r"George \ (1879)", r"\textit{Progress and Poverty}: \ tax the value of land, \ which no one made", MKT),
                (r"left-libertarians", r"Steiner \ (1994); \ Vallentyne; \ Otsuka \ (2003): \ full self-ownership, \ and an equal share in natural resources", LIB),
                (r"Van Parijs \ (1995)", r"\textit{Real Freedom for All}: \ an unconditional basic income, \ as high as can be sustained", FAIR)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Self-ownership need not lead where Nozick took it. <bookmark mark='a'/>Thomas Paine's Agrarian Justice, "
            "of 1797, argued that the earth was originally common property, so those who own land owe a ground rent "
            "to everyone else; he proposed paying every person fifteen pounds at the age of twenty one, from a tax on "
            "inheritance. <bookmark mark='b'/>Henry George's Progress and Poverty, of 1879, proposed taxing the value "
            "of land, which no one made. <bookmark mark='c'/>Left-libertarians such as Hillel Steiner, Peter "
            "Vallentyne and Michael Otsuka combine full self-ownership with an equal claim to natural resources, "
            "which can justify substantial redistribution. <bookmark mark='d'/>And Philippe Van Parijs's Real Freedom "
            "for All, of 1995, defended an unconditional basic income, as high as can be sustained, as what real "
            "freedom requires."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
