from __future__ import annotations

import numpy as np

from videos.stats.stats44.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.quarrel()
        self.letters()
        self.chain()
        self.dispersion()
        self.upgrades()
        self.objectives()

    def quarrel(self):
        tl = timeline(lit=(1906, 1913)).to_edge(UP, buff=0.35)
        rows = fit_rows(VGroup(
            label(r"1902: \ Pavel Nekrasov, \ Moscow: \ the law of large numbers \emph{requires} independence", font_size=26, color=GREY_A),
            label(r"so, \ he argued, \ the regularity of social statistics proves free will", font_size=24, color=GREY_A),
            label(r"1906: \ Andrei Markov, \ St Petersburg: \ the law holds for dependent chains too", font_size=26, color=CHAINC),
            label(r"1913: \ to show it on real data, \ he counts the letters of a poem", font_size=26, color=S.ACCENT),
        ), 12.4, 0.55, [0, -0.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> In 1902 the Moscow mathematician Pavel Nekrasov argued that the law of large numbers "
            "requires independence, <bookmark mark='b'/> and concluded, because social statistics are regular, that human "
            "acts must be independent, a proof of free will. <bookmark mark='c'/> In St Petersburg, Andrei Markov was "
            "furious. In 1906 he proved the law of large numbers for sequences in which each variable depends on the one "
            "before, the chains that now bear his name. <bookmark mark='d'/> And in January 1913, at the two hundredth "
            "anniversary of Bernoulli's law, he showed it on real data, by counting the letters of a poem."
        ) as vo:
            self.play(FadeIn(tl))
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def letters(self):
        d = load("onegin")
        first = d["first"]
        text = "МОЙДЯДЯСАМЫХЧЕСТНЫХПРАВИЛКОГДАНЕВШУТКУЗАНЕМОГОНУВАЖАТЬСЕБЯЗАСТАВИЛ"
        # the 60 letters behind the first 60 bits (signs removed: the bits skip Ь and Ъ)
        letters = [c for c in text if c not in "ЬЪ"][:60]
        cells = VGroup()
        w = 0.4
        for i, (c, b) in enumerate(zip(letters, first)):
            row, col = divmod(i, 20)
            col_c = VOWC if b else CONC
            sq = Square(side_length=w * 0.9, stroke_width=0, fill_color=col_c, fill_opacity=0.75).move_to([-3.8 + col * w, 1.6 - row * 0.55, 0])
            t = Text(c, font_size=18, color=WHITE).move_to(sq)
            cells.add(VGroup(sq, t))
        quote = VGroup(label(r"``Moy dyadya samykh chestnykh pravil, \ kogda ne v shutku zanemog...''", font_size=24, color=GREY_A),
                       label(r"\emph{Eugene Onegin}, \ the opening line", font_size=20, color=GREY_B)).arrange(DOWN, buff=0.15).move_to([0, 2.8, 0])
        side = fit_rows(VGroup(
            label(rf"the first {d['n']:,} letters, \ hard and soft signs left out", font_size=24),
            label(rf"gold: \ vowels, \ {d['vowels']:,} \ (Markov: \ {d['markov']['vowels']:,})", font_size=24, color=VOWC),
            label(rf"blue: \ consonants, \ {d['n'] - d['vowels']:,}", font_size=24, color=CONC),
            label(r"recomputed here from the public-domain text", font_size=20, color=GREY_B),
        ), 12.4, 0.35, [0, -1.6, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> The poem was Pushkin's Eugene Onegin, which every Russian reader knew. Markov took its "
            f"first twenty thousand letters, leaving out the hard and soft signs, which are not sounds, and wrote each "
            f"as a vowel or a consonant. <bookmark mark='b'/> Here are the first sixty, in the original Russian: gold for "
            f"vowels, blue for consonants. <bookmark mark='c'/> We redid his count from the public-domain text. It gives "
            f"{d['vowels']:,} vowels, against Markov's {d['markov']['vowels']:,}, <bookmark mark='d'/> and "
            f"{d['n'] - d['vowels']:,} consonants. A hundred and thirteen years and a change of spelling later, the count "
            f"is off by one."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(quote), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(c) for c in cells], lag_ratio=0.03), run_time=3.0)
            vo.wait_until("c")
            self.play(FadeIn(side[1]), FadeIn(side[3]))
            vo.wait_until("d")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def chain(self):
        d = load("onegin")
        P = d["P"]
        c = d["counts"]
        vx, cx = np.array([-4.0, 0.2, 0]), np.array([-0.2, 0.2, 0])
        vn = VGroup(Circle(radius=0.75, color=VOWC, stroke_width=4, fill_color=VOWC, fill_opacity=0.2).move_to(vx),
                    label(r"vowel", font_size=26, color=VOWC).move_to(vx))
        cn = VGroup(Circle(radius=0.75, color=CONC, stroke_width=4, fill_color=CONC, fill_opacity=0.2).move_to(cx),
                    label(r"consonant", font_size=22, color=CONC).move_to(cx))
        a1 = CurvedArrow(vx + np.array([0.7, 0.35, 0]), cx + np.array([-0.7, 0.35, 0]), angle=-0.6, color=GREY_B)
        a2 = CurvedArrow(cx + np.array([-0.7, -0.35, 0]), vx + np.array([0.7, -0.35, 0]), angle=-0.6, color=GREY_B)
        l1 = label(rf"${P[1][0]:.3f}$", font_size=24).move_to((vx + cx) / 2 + np.array([0, 1.05, 0]))
        l2 = label(rf"${P[0][1]:.3f}$", font_size=24).move_to((vx + cx) / 2 + np.array([0, -1.05, 0]))
        s1 = label(rf"${P[1][1]:.3f}$", font_size=24, color=VOWC).next_to(vn, LEFT, buff=0.25)
        s2 = label(rf"${P[0][0]:.3f}$", font_size=24, color=CONC).next_to(cn, RIGHT, buff=0.25)
        side = fit_rows(VGroup(
            label(rf"vowel $\to$ vowel: \ {int(c[1][1]):,} \ (Markov: \ {d['markov']['vv']:,})", font_size=22, color=VOWC),
            label(rf"consonant $\to$ consonant: \ {int(c[0][0]):,} \ (Markov: \ {d['markov']['cc']:,})", font_size=22, color=CONC),
            label(rf"$P(\text{{vowel}} \mid \text{{vowel}}) = {P[1][1]:.3f}$, \ \ $P(\text{{vowel}} \mid \text{{consonant}}) = {P[0][1]:.3f}$", font_size=22),
            label(r"far from independence: \ the next letter depends on this one", font_size=22, color=S.ACCENT),
            label(rf"stationary share of vowels: \ {d['pi1']:.3f} \ (observed {d['share']:.3f})", font_size=22, color=GREY_A),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> Then he counted pairs. A vowel was followed by another vowel only "
            f"{int(c[1][1]):,} times, Markov's count was {d['markov']['vv']:,}, <bookmark mark='b'/> and two consonants "
            f"followed each other {int(c[0][0]):,} times, his {d['markov']['cc']:,}. <bookmark mark='c'/> So after a vowel "
            f"the next letter is a vowel with probability {say(P[1][1], 3)}; after a consonant, {say(P[0][1], 3)}. "
            f"<bookmark mark='d'/> Letters alternate: the sequence is strongly dependent, a two-state chain with these "
            f"transition probabilities. <bookmark mark='e'/> Yet the long-run share of vowels, the chain's stationary "
            f"probability, {say(d['pi1'], 3)}, matches the observed share: the law of large numbers holds."
        ) as vo:
            self.play(FadeIn(vn), FadeIn(cn), FadeIn(museum_tag(r"Pushkin, \ \emph{Eugene Onegin}; \ Markov (1913)")))
            vo.wait_until("a")
            self.play(FadeIn(s1), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(s2), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(a1), Create(a2), FadeIn(l1), FadeIn(l2), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def dispersion(self):
        d = load("onegin")
        blocks = np.asarray(d["blocks"])
        A = axes([28, 58], [0, 0.2], x_length=7.4, y_length=4.4, xlabel=r"vowels in a block of 100 letters", ylabel=r"share of the 200 blocks",
                 xticks=[30, 35, 40, 45, 50, 55], yticks=[0, 0.1, 0.2], center=[-2.5, 0.2, 0])
        ax = A.ax
        ks = np.arange(28, 59)
        h = np.array([np.mean(blocks == k) for k in ks])
        bars = bars_at(ax, ks, h, 0.85, VOWC, opacity=0.75)
        from scipy import stats as st
        p = d["share"]
        binom = VGroup(*[Dot(ax.c2p(k, st.binom.pmf(k, 100, p)), radius=0.05, color=GREY_B) for k in ks])
        sdc = np.sqrt(d["var_chain"])
        chainc = curve(ax, np.linspace(28, 58, 200), st.norm.pdf(np.linspace(28, 58, 200), 100 * p, sdc), LIMC, 3)
        side = fit_rows(VGroup(
            label(rf"variance of the 200 block counts: \ {d['var_block']:.2f}", font_size=22, color=VOWC),
            label(rf"if letters were independent: \ {d['var_iid']:.2f} \ (grey)", font_size=22, color=GREY_A),
            label(rf"under the chain: \ {d['var_chain']:.2f} \ (gold)", font_size=22, color=LIMC),
            label(rf"dispersion: \ {d['var_block'] / d['var_iid']:.3f} observed, \ {d['var_chain'] / d['var_iid']:.3f} for the chain", font_size=22, color=S.ACCENT),
            label(r"Markov's own: \ 0.208 \ and \ about 0.3", font_size=20, color=GREY_B),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> Markov went further. He cut the text into two hundred blocks of a hundred letters and "
            f"counted the vowels in each. <bookmark mark='b'/> The counts vary far less than independence would allow: "
            f"their variance is {say(d['var_block'], 2)}, <bookmark mark='c'/> against {say(d['var_iid'], 1)} for "
            f"independent letters. <bookmark mark='d'/> The chain explains most of the difference: alternation makes "
            f"blocks more alike, and its variance is {say(d['var_chain'], 1)}. <bookmark mark='e'/> The ratios, "
            f"{say(d['var_block'] / d['var_iid'], 3)} observed and {say(d['var_chain'] / d['var_iid'], 2)} for the chain, are "
            f"Markov's dispersion coefficients; he found point two oh eight, and about point three. Dependence changes the "
            f"variance, not the law of large numbers. That is the subject of this part."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(bars))
            vo.wait_until("b")
            self.play(FadeIn(side[0]))
            vo.wait_until("c")
            self.play(FadeIn(binom), FadeIn(side[1]))
            vo.wait_until("d")
            self.play(Create(chainc), FadeIn(side[2]))
            vo.wait_until("e")
            self.play(FadeIn(side[3]), FadeIn(side[4]))
        self.clear_scene()

    def upgrades(self):
        cards = [
            upgrade_card(43, r"the strong law and the CLT", r"independent summands", r"chapters 5--9: \ martingales and chains"),
            upgrade_card(27, r"MCMC standard errors from batch means and ESS", r"a CLT for the chain, \ on trust",
                         r"chapter 8: \ drift, \ minorization, \ the MCMC CLT"),
            upgrade_card(38, r"the Dickey--Fuller test's tables", r"limits that are functionals of Brownian motion",
                         r"chapters 10--11: \ Brownian motion and Donsker"),
        ]
        for c in cards:
            c.scale(0.86)
        VGroup(*cards).arrange(DOWN, buff=0.25).move_to(ORIGIN)
        with self.voiceover(
            "<bookmark mark='a'/> Three promises are now due. Part forty-three proved its laws for independent summands; "
            "chapters five to nine extend them to martingales and chains. <bookmark mark='b'/> Part twenty-seven computed "
            "MCMC standard errors by batch means, assuming a central limit theorem for the chain; chapter eight supplies "
            "it. <bookmark mark='c'/> And Part thirty-eight used the Dickey–Fuller tables, whose limits are functionals of "
            "Brownian motion; chapters ten and eleven build Brownian motion and explain them."
        ) as vo:
            for k, m_ in enumerate("abc"):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.15))
        self.wait(1.0)
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 44", font_size=34, color=GREY_B), label(r"Martingales, Markov Chains and Brownian Motion", font_size=48)).arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"conditional expectation, \ martingales, \ optional stopping, \ Ville's inequality",
            r"martingale convergence, \ concentration and the martingale CLT",
            r"Markov chains on general spaces, \ the MCMC CLT, \ coupling and mixing",
            r"Brownian motion, \ Donsker, \ the iterated logarithm, \ counting processes",
        ], color=S.ACCENT, font_size=26)
        prereq = note(r"prerequisites: \ Part 43").to_corner(DL, buff=0.3)
        built = note(r"built: \ \texttt{statkit.chains}, \ the coupling and mixing lab; \ betting paths").to_corner(DR, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Part forty-four: martingales, Markov chains and Brownian motion. <bookmark mark='b'/> We'll "
            "define conditional expectation properly, build martingales and their stopping, maximal and convergence "
            "theorems, with Ville's inequality, the root of anytime-valid testing; prove concentration and a central limit "
            "theorem for martingales; give Markov chains on general spaces their ergodic theory, with a coupling and mixing "
            "lab; and construct Brownian motion, the limit of every random walk."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeOut(head), FadeIn(obj, shift=UP * 0.2), FadeIn(prereq), FadeIn(built))
        self.wait(1.0)
        self.clear_scene()
