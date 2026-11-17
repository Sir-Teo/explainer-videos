from __future__ import annotations

from videos.psychology.psych22.common import *  # noqa: F403

GROUPS = {"family": (CAT_A, ("sister", "brother", "mother", "father", "aunt", "uncle", "daughter", "son")),
          "time": (CAT_B, ("monday", "tuesday", "thursday", "saturday", "morning", "evening")),
          "feeling": (PROTO, ("happy", "pleased", "cheerful", "unhappy", "miserable", "wretched"))}


def group_of(w: str) -> str:
    return next(g for g, (_, ws) in GROUPS.items() if w in ws)


class Meaning(VoiceoverScene):
    def construct(self):
        self.card()
        self.company()
        self.derive()
        self.austen()
        self.map()
        self.limits()

    def card(self):
        card = chapter_card(11, r"Meaning from company", r"Can the meaning of a word be learned from the words around "
                            r"it?", lit={1954: r"Harris", 1957: r"Firth", 1997: r"Landauer \& Dumais",
                                         2017: r"Caliskan et al."},
                            part=PART, scale=("mind", "world"), marr=("what", "how"))
        with self.voiceover("Chapter eleven. Meaning from company."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def company(self):
        head = heading(r"You shall know a word by the company it keeps")
        sent = VGroup(*[label(t, font_size=28, color=c) for t, c in (
            (r"she poured the \emph{tezg\"{u}ino} into a cup", GREY_A),
            (r"everyone likes \emph{tezg\"{u}ino}", GREY_A),
            (r"\emph{tezg\"{u}ino} makes you drunk", GREY_A),
            (r"they make \emph{tezg\"{u}ino} out of corn", GREY_A))]).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        sent.move_to([-3.0, 0.9, 0])
        rows = rows_of([
            (r"you have never seen the word, \ yet you already know roughly what it means: \ a drink, \ alcoholic, \ "
             r"made from corn", WHITE),
            (r"Harris, \ 1954: \ words that occur in similar contexts tend to have similar meanings", MODEL),
            (r"Firth, \ 1957: \ \emph{you shall know a word by the company it keeps}", CAT_A),
            (r"most of the words you know, \ you learned this way: \ from reading, \ not from definitions", PROTO),
        ], 5.6, 21, 0.3).move_to([3.5, 0.3, 0])
        tag = historical_tag(r"Harris (1954); \ Firth (1957); \ the \emph{tezg\"{u}ino} example: \ Nida (1975), \ Lin (1998)")
        with self.voiceover(
            "Concepts aren't only learned from things. Most are learned from words. <bookmark mark='a'/> Here's a "
            "word you have probably never seen: tezgüino. She poured the tezgüino into a cup. Everyone likes "
            "tezgüino. Tezgüino makes you drunk. They make tezgüino out of corn. <bookmark mark='b'/> You already "
            "know roughly what it is: a drink, alcoholic, made from corn. And no one defined it for you. "
            "<bookmark mark='c'/> The linguist Zellig Harris put the idea in 1954: words that occur in similar "
            "contexts tend to have similar meanings. <bookmark mark='d'/> John Firth said it more memorably: you "
            "shall know a word by the company it keeps. <bookmark mark='e'/> Most of the tens of thousands of words "
            "an adult knows were learned this way, from reading and listening, not from definitions."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(s) for s in sent], lag_ratio=0.5), run_time=3)
            for m, r in zip("bcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def derive(self):
        head = heading(r"Derivation: \ from counts to a space of meanings")
        eqs = VGroup(
            MathTex(r"C_{wc} = \#\{\, c \text{ within 4 words of } w \,\}", font_size=36),
            MathTex(r"\mathrm{PPMI}_{wc} = \max\Big(0,\ \log \frac{P(w, c)}{P(w)\, P(c)}\Big)", font_size=36,
                    color=SPACE),
            MathTex(r"M \approx U_k \Sigma_k V_k^\top, \qquad \mathbf{v}_w = (U_k \Sigma_k^{1/2})_w", font_size=36,
                    color=MODEL),
            MathTex(r"\mathrm{sim}(w, u) = \cos(\mathbf{v}_w, \mathbf{v}_u)", font_size=36, color=CAT_A),
        ).arrange(DOWN, buff=0.38).move_to([-2.9, 0.6, 0])
        rows = rows_of([
            (r"count how often each word appears near each other word", WHITE),
            (r"keep only the surprise: \ how much more often than chance; \ \emph{the} and \emph{of} tell you nothing",
             SPACE),
            (r"compress the table to 100 dimensions with the SVD: \ words that share company end up close", MODEL),
            (r"the cosine of the angle between two words' vectors is their similarity", CAT_A),
        ], 5.2, 21, 0.3).move_to([3.8, 0.4, 0])
        ptag = psyche_tag(r"\texttt{concepts.cooccurrence}, \ \texttt{ppmi\_svd}, \ \texttt{neighbours}")
        with self.voiceover(
            "Turn that idea into arithmetic in four steps. <bookmark mark='a'/> First, count. For every word, count "
            "how often each other word appears within four words of it. <bookmark mark='b'/> Second, keep only the "
            "surprise. Pointwise mutual information compares how often two words appear together with how often "
            "they would by chance. Words like the and of appear near everything, so they tell you nothing and score "
            "zero. <bookmark mark='c'/> Third, compress. The singular value decomposition squeezes the huge table "
            "down to a hundred dimensions, and words that share company end up close together. "
            "<bookmark mark='d'/> Fourth, compare. The similarity of two words is the cosine of the angle between "
            "their vectors. Latent semantic analysis, in 1997, used a version of these steps."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ptag))
            for m, e, r in zip("abcd", eqs, rows):
                vo.wait_until(m)
                self.play(Write(e), FadeIn(r))
        self.clear_scene()

    def austen(self):
        d = load("austen")
        head = heading(r"Psyche reads Jane Austen")
        words = ("letter", "morning", "walk", "money", "house")
        table = VGroup()
        for k, w in enumerate(words):
            y = 1.2 - 0.62 * k
            nb = d["nb_" + w][:4]
            table.add(VGroup(label(w, font_size=24, color=CAT_A).move_to([-5.6, y, 0], aligned_edge=LEFT),
                             label(r", \ ".join(str(x) for x in nb), font_size=21, color=WHITE).move_to(
                                 [-3.9, y, 0], aligned_edge=LEFT)))
        hdr = VGroup(label(r"word", font_size=19, color=GREY_A).move_to([-5.6, 1.85, 0], aligned_edge=LEFT),
                     label(r"nearest neighbours", font_size=19, color=GREY_A).move_to([-3.9, 1.85, 0],
                                                                                    aligned_edge=LEFT))
        rows = rows_of([
            (rf"six novels, \ {num(d['tokens'])} words; \ the {num(d['vocab'])} commonest words after dropping the "
             r"commonest function words", WHITE),
            (r"nobody told Psyche what any word means: \ only which words stood near which", MODEL),
            (r"neighbours share meaning, \ or at least use: \ a letter is \emph{written} and \emph{read}; \ a walk "
             r"goes \emph{along} the \emph{gravel}", CAT_A),
        ], 4.8, 21, 0.3).move_to([4.2, 0.2, 0])
        ptag = psyche_tag(r"open data: \ janeaustenr; \ \texttt{concepts.ppmi\_svd}")
        assert list(d["nb_letter"][:4]) == ["note", "written", "letters", "read"]  # named in the narration
        with self.voiceover(
            "Let's try it. <bookmark mark='a'/> Psyche reads Jane Austen's six novels, about seven hundred and thirty "
            "thousand words, and builds vectors for the four thousand commonest words, after dropping the "
            "commonest function words. <bookmark mark='b'/> Nobody told it what any word means, only which words "
            "stood near which. <bookmark mark='c'/> Here are the nearest neighbours of some words. Letter: "
            "note, written, letters, read. Morning sits near day, next, and the days of the week. Walk sits "
            "near gravel and along. <bookmark mark='d'/> Neighbours share meaning, or at least use. A letter is "
            "written and read, and in Austen a walk goes along the gravel."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ptag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(hdr), LaggedStart(*[FadeIn(r) for r in table], lag_ratio=0.3), run_time=2.5)
            vo.wait_until("d")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def map(self):
        d = load("austen")
        head = heading(r"A map of twenty words")
        X = d["map_X"] * 2.6
        cx, cy = -2.6, -0.2
        words = [str(w) for w in d["map_words"]]
        pts = VGroup()
        for (x, y), w in zip(X, words):
            col = GROUPS[group_of(w)][0]
            pts.add(VGroup(Dot([cx + x, cy + y, 0], radius=0.08, color=col)))
        # the clusters are tight, so each is named by one list of its words, placed outside it
        centre = np.array([cx, cy]) + X.mean(0)
        names = VGroup()
        for g, (col, ws) in GROUPS.items():
            idx = [words.index(w) for w in ws if w in words and w != "unhappy"]
            c = np.array([cx, cy]) + X[idx].mean(0)
            out = c - centre
            out = out / (np.linalg.norm(out) + 1e-9)
            lab = wrapped_label(r", \ ".join(words[i] for i in idx), 2.3, 17, col)
            lab.move_to([c[0] + 1.25 * out[0], c[1] + 0.95 * out[1], 0])
            names.add(lab)
        ui = words.index("unhappy")
        upos = np.array([cx + X[ui, 0], cy + X[ui, 1], 0])
        ulab = label(r"unhappy", font_size=19, color=LOST).next_to(upos, DOWN + LEFT, buff=0.35)
        uarrow = Arrow(ulab.get_corner(UR), upos, buff=0.08, color=LOST, stroke_width=2.5,
                       max_tip_length_to_length_ratio=0.25)
        for m in (*names, ulab):
            keep_in_frame(m)
        rows = rows_of([
            (r"twenty words, \ placed by classical scaling of their cosine distances", WHITE),
            (r"three clusters emerge: \ family, \ times of the week and day, \ feelings", MODEL),
            (r"but \emph{unhappy} sits among the happy words: \ opposites keep the same company, \ so "
             r"co-occurrence alone puts them together", LOST),
        ], 4.8, 21, 0.3).move_to([4.2, 0.0, 0])
        ptag = psyche_tag(r"\texttt{concepts.classical\_mds} \ on Austen's vectors")
        with self.voiceover(
            "Here are twenty words placed on a map by their similarity, using the scaling from chapter five. "
            "<bookmark mark='a'/> Three clusters emerge, with no labels supplied: the family words, the times of the "
            "week and the day, and the feelings. <bookmark mark='b'/> But look where unhappy sits: among the happy "
            "words. Opposites keep the same company. Both are said of the same people, in the same kinds of "
            "sentence, so co-occurrence alone pushes them together. A meaning built from company can confuse a word "
            "with its opposite."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ptag), FadeIn(rows[0]),
                      LaggedStart(*[FadeIn(p) for p in pts], lag_ratio=0.05), run_time=2.5)
            vo.wait_until("a")
            self.play(FadeIn(names, lag_ratio=0.3), FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(ulab), GrowArrow(uarrow), Indicate(pts[ui], color=LOST, scale_factor=1.8),
                      FadeIn(rows[2]))
        self.clear_scene()

    def limits(self):
        d = load("austen")
        a = archive.LANDAUER_DUMAIS_1997.data
        head = heading(r"How far does company go?")
        an0, an1 = d["analogy_0"], d["analogy_1"]
        assert an0[0] == "mother" and an1[0] == "permission" and list(an1).index("aunt") == 3  # named in the narration
        cols = VGroup(
            VGroup(label(r"a vocabulary test", font_size=26, color=MODEL),
                   rows_of([(rf"LSA, \ trained on an encyclopaedia, \ took 80 items of the TOEFL synonym test: \ "
                             rf"{a['lsa_pct']:.1f}\% correct", WHITE),
                            (rf"applicants to US colleges from non-English-speaking countries averaged "
                             rf"{a['applicants_pct']:.1f}\%", GREY_A)], 3.7, 19, 0.28)),
            VGroup(label(r"analogies", font_size=26, color=CAT_A),
                   rows_of([(rf"brother : sister :: father : \ \textbf{{{an0[0]}}}", WHITE),
                            (rf"son : daughter :: uncle : \ {', '.join(str(x) for x in an1[:4])}", GREY_A),
                            (r"Austen is too small a corpus: \ word vectors trained on billions of words do far "
                             r"better", GREY_A)], 3.7, 19, 0.28)),
            VGroup(label(r"and our prejudices", font_size=26, color=LOST),
                   rows_of([(r"Caliskan, \ Bryson \& Narayanan, \ 2017: \ vectors trained on the web reproduce the "
                             r"associations of the Implicit Association Test", WHITE),
                            (r"flowers with pleasant, \ insects with unpleasant; \ and the same for race and gender",
                             GREY_A)], 3.7, 19, 0.28)),
        )
        for k, c in enumerate(cols):
            c.arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to([-4.4 + 4.4 * k, 0.3, 0])
        rows = rows_of([
            (r"what company cannot give is \emph{grounding}: \ a word's link to the things it is about \ "
             r"(Harnad, \ 1990)", PROTO)], 12.4, 22, 0.3).to_edge(DOWN, buff=0.65)
        tag = published_tag(r"Landauer \& Dumais (1997); \ Caliskan et al. (2017); \ Harnad (1990)")
        with self.voiceover(
            "How far can company go? <bookmark mark='a'/> In 1997 Thomas Landauer and Susan Dumais trained latent "
            "semantic analysis on an encyclopaedia and gave it eighty items from the TOEFL synonym test. It got "
            f"{a['lsa_pct']:.1f} percent right. Applicants to American colleges from non-English-speaking countries "
            f"averaged {a['applicants_pct']:.1f}. <bookmark mark='b'/> Analogies are harder. On Austen, brother is to "
            "sister as father is to mother: right. But son is to daughter as uncle is to permission. The right "
            "answer, aunt, comes in fourth. "
            "Austen is a small corpus. Vectors trained on billions of words get far more analogies right. "
            "<bookmark mark='c'/> And they learn our prejudices. Aylin Caliskan, Joanna Bryson and Arvind Narayanan "
            "showed in 2017 that vectors trained on text from the web reproduce the associations measured by the "
            "Implicit Association Test: flowers go with pleasant words and insects with unpleasant ones, and the same "
            "holds for associations about race and gender. The vectors are a mirror of the language they read. "
            "<bookmark mark='d'/> What company can't supply is grounding. Stevan Harnad asked how symbols defined "
            "only by other symbols could ever be about the world. That question, for minds and for machines, is the "
            "frontier."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, c in zip("abc", cols):
                vo.wait_until(m)
                self.play(FadeIn(c, shift=UP * 0.15))
            vo.wait_until("d")
            self.play(FadeIn(rows[0]))
        self.clear_scene()
