from __future__ import annotations

from videos.psychology.psych23.common import *  # noqa: F403

LEVELS = (
    (r"sounds \ (phonemes)", r"/b/ \ and \ /p/ \ make \emph{bat} and \emph{pat} differ", SOUND),
    (r"parts of words \ (morphemes)", r"\emph{un-} \ \emph{happi} \ \emph{-ness}", WORD),
    (r"words", r"about 40,000 known by an adult reader \ (a rough figure)", WORD),
    (r"sentences \ (syntax)", r"\emph{the dog bit the man} \ is not \ \emph{the man bit the dog}", RULE),
    (r"meaning \ (semantics)", r"what a sentence says about the world", STAT),
    (r"use \ (pragmatics)", r"\emph{can you pass the salt?} \ is not a question about ability", MODEL),
)


class Levels(VoiceoverScene):
    def construct(self):
        self.card()
        self.levels()
        self.wug()
        self.zipf()

    def card(self):
        card = chapter_card(1, r"Levels and productivity", r"What does it mean to know a language?",
                            lit={1949: r"Zipf", 1957: r"Miller", 1958: r"Berko"},
                            part=PART, scale=("mind",), marr=("what",))
        with self.voiceover("Chapter one. Levels and productivity."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def levels(self):
        head = heading(r"The levels of language")
        rows = VGroup()
        for k, (name, ex, col) in enumerate(LEVELS):
            rows.add(VGroup(label(name, font_size=26, color=col).move_to([-3.6, 2.0 - 0.75 * k, 0], aligned_edge=LEFT),
                            label(ex, font_size=22, color=GREY_A).move_to([0.6, 2.0 - 0.75 * k, 0], aligned_edge=LEFT)))
        for r in rows:
            r[0].align_to([-6.2, 0, 0], LEFT)
        note = rows_of([
            (r"at every level the units combine by rules into more than you could ever list: \ \emph{productivity}",
             MODEL)], 12.2, 24, 0.3).to_edge(DOWN, buff=0.65)
        with self.voiceover(
            "What do you know when you know a language? Linguists split it into levels. <bookmark mark='a'/> Sounds: "
            "a small set of contrasts, like the b and p that make bat and pat different words. Parts of words: "
            "unhappiness is un, happi and ness. Words: an adult reader knows tens of thousands. "
            "<bookmark mark='b'/> Sentences: the dog bit the man is not the man bit the dog, though the words are "
            "the same. Meaning: what a sentence says about the world. And use: can you pass the salt is not a "
            "question about your arm. <bookmark mark='c'/> At every level, units combine by rules into more than you "
            "could ever list. That is productivity, and it is what Chomsky meant."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows[:3]], lag_ratio=0.5), run_time=3)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows[3:]], lag_ratio=0.5), run_time=3)
            vo.wait_until("c")
            self.play(FadeIn(note))
        self.clear_scene()

    def wug(self):
        head = heading(r"Berko's wug test, \ 1958")
        one = VGroup(Ellipse(width=1.3, height=0.9, color=SOUND, fill_opacity=0.35),
                     Dot([-0.25, 0.12, 0], radius=0.06, color=WHITE), Dot([0.25, 0.12, 0], radius=0.06, color=WHITE)
                     ).move_to([-3.8, 1.6, 0])
        two = VGroup(one.copy().move_to([2.0, 1.6, 0]), one.copy().move_to([3.6, 1.6, 0]))
        t1 = label(r"This is a \emph{wug}.", font_size=28).next_to(one, DOWN, buff=0.3)
        t2 = VGroup(label(r"Now there are two of them.", font_size=28),
                    label(r"There are two \underline{\hspace{1.2cm}}.", font_size=28)).arrange(DOWN, buff=0.32)
        t2.next_to(two, DOWN, buff=0.3)
        ans = label(r"\emph{wugs}", font_size=30, color=MODEL).move_to(t2[1].get_right() + LEFT * 0.75)
        ans.align_to(t2[1], DOWN).shift(UP * 0.1)
        rows = rows_of([
            (r"Jean Berko showed preschool and school children made-up creatures and actions they could never have "
             r"heard named", WHITE),
            (r"they supplied \emph{wugs}, \ \emph{ricked}, \ \emph{gutches}: \ rules applied to new words, \ not "
             r"forms remembered", RULE),
            (r"children also say \emph{goed} and \emph{mouses}, \ words no adult says: \ chapter eight", STAT),
        ], 12.0, 26, 0.36).move_to([0, -1.7, 0])
        tag = historical_tag(r"Berko (1958), \ \emph{Word} 14")
        with self.voiceover(
            "In 1958 Jean Berko found a way to see productivity in children. <bookmark mark='a'/> She showed them "
            "a picture of a made-up creature: this is a wug. Then two of them: now there are two of them. There are "
            "two what? <bookmark mark='b'/> Children answered wugs, with the right ending, for a word they had never "
            "heard. They did the same for verbs: a man who knows how to rick, did the same thing yesterday. He "
            "ricked. <bookmark mark='c'/> They were applying rules to new words, not repeating forms they had heard. "
            "And children also make forms no adult says, like goed and mouses, which will matter in chapter eight."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(one), FadeIn(t1))
            vo.wait_until("a")
            self.play(FadeIn(two), FadeIn(t2), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(ans, scale=1.2), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def zipf(self):
        d = load("zipf")
        head = heading(r"Zipf's law, \ and a monkey")
        A = axes([0, 4.2], [0, 6], x_length=5.4, y_length=3.6, xticks=[0, 1, 2, 3, 4], yticks=[0, 2, 4, 6],
                 xfmt=lambda v: rf"10^{{{int(v)}}}", yfmt=lambda v: rf"10^{{{int(v)}}}",
                 xlabel=r"rank of the word", ylabel=r"how often it occurs", center=[-3.0, 0.0, 0], font_size=17)
        lr, lf = np.log10(d["rank"]), np.log10(d["freq"])
        pts = scatter(A.ax, lr, lf, WORD, 0.045, 0.9)
        x = np.linspace(0, 4.1, 50)
        fit = curve(A.ax, x, (d["logC"] - d["s"] * np.log(10 ** x)) / np.log(10), MODEL, 3)
        mpts = scatter(A.ax, np.log10(d["m_rank"]), np.log10(d["m_freq"]), STAT, 0.04, 0.9)
        top = ", ".join(str(w) for w in d["top"][:6])
        rows = rows_of([
            (rf"thirty novels, \ {num(d['tokens'])} words of {num(d['types'])} kinds: \ \emph{{{top}}} \dots", WHITE),
            (rf"frequency falls as a power of rank, \ exponent {d['s']:.2f}: \ Zipf's law", MODEL),
            (rf"a monkey typing letters and spaces at random: \ exponent {d['m_s']:.2f}, \ in steps", STAT),
            (r"Miller, \ 1957: \ a power law alone shows little about minds; \ what words are and how they are "
             r"used needs more", LOST),
        ], 5.6, 23, 0.33).move_to([3.6, 0.0, 0])
        ptag = psyche_tag(r"\texttt{language.zipf\_fit}, \ \texttt{random\_typing}; \ the novels of \emph{AI, Built} Part 1")
        with self.voiceover(
            "Words have statistics, and the most famous is Zipf's law. <bookmark mark='a'/> Here are thirty novels, "
            "about four million words of sixty thousand kinds. Rank the words by how often they occur: the, and, to, "
            "of, a. <bookmark mark='b'/> On logarithmic axes the frequencies fall on a straight line: frequency is "
            f"a power of rank, with exponent {d['s']:.2f}. George Kingsley Zipf found this in many languages and "
            "thought it revealed a principle of least effort. <bookmark mark='c'/> But in 1957 George Miller pointed "
            "out that a monkey typing letters and spaces at random produces a power law too. Here it is, exponent "
            f"{d['m_s']:.2f}, in steps. <bookmark mark='d'/> So the law by itself shows little about minds. What "
            "words are, and how people use them, needs more than a straight line on a log plot."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(ptag))
            vo.wait_until("a")
            self.play(FadeIn(pts), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(fit), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(mpts), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
