from __future__ import annotations

from videos.psychology.psych21.common import *  # noqa: F403


class Exceptional(VoiceoverScene):
    def construct(self):
        self.card()
        self.mnemonist()
        self.hsam()
        self.why_forget()

    def card(self):
        card = chapter_card(11, r"Remembering too much", r"What would a memory that never forgot be like?",
                            lit={1968: r"Luria", 2006: r"Parker, \ Cahill \& McGaugh", 2013: r"Patihis et al.",
                                 2017: r"Richards \& Frankland"},
                            part=PART, scale=("person",), marr=("what",))
        with self.voiceover("Chapter eleven. Remembering too much."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def mnemonist(self):
        head = heading(r"S., \ the mnemonist")
        rows = rows_of([
            (r"Moscow, \ from the 1920s: \ Alexander Luria studied a journalist, \ S., \ for thirty years", WHITE),
            (r"he repeated long tables of numbers and lists of nonsense, \ forwards or backwards, \ and recalled "
             r"them again years later", TRACE),
            (r"every word came with images, \ colours, \ tastes: \ a strong synaesthesia", CTX),
            (r"his trouble was forgetting: \ he wrote things down and burnt the paper, \ trying to be rid of them",
             LOST),
            (r"and abstraction: \ a story read aloud became a flood of images; \ a metaphor, \ a poem, \ a face that "
             r"changed its expression, \ were hard for him", FALSE),
        ], 12.4, 26, 0.38).move_to([0, -0.2, 0])
        tag = historical_tag(r"Luria (1968), \ \emph{The Mind of a Mnemonist}")
        with self.voiceover(
            "So far forgetting has been the enemy. What would a memory that didn't forget be like? "
            "<bookmark mark='a'/> In Moscow, from the 1920s, the neuropsychologist Alexander Luria studied a "
            "journalist he called S., for thirty years. <bookmark mark='b'/> S. could repeat long tables of numbers "
            "and lists of nonsense, forwards or backwards, and recall them again when Luria tested him years later. "
            "<bookmark mark='c'/> Every word arrived with images, colours, even tastes, a synaesthesia so strong "
            "that a voice could seem to him to have a colour. <bookmark mark='d'/> His problem was the opposite of "
            "ours. He tried to forget, writing things down and burning the paper, without success. "
            "<bookmark mark='e'/> And he found abstraction hard. A story read aloud became a crowd of images that "
            "got in each other's way; metaphors and poetry troubled him, and faces were hard to recognise because "
            "they kept changing expression. Remembering every particular, he struggled with the general."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def hsam(self):
        p = archive.PATIHIS_2013.data
        head = heading(r"Highly superior autobiographical memory")
        rows = rows_of([
            (r"Parker, \ Cahill and McGaugh, \ 2006: \ a woman, \ AJ, \ who could say what she did on almost every "
             r"day of her life since her teens, \ checked against her diaries", WHITE),
            (r"since then, \ a few dozen people found with the same ability; \ their memory for lists and "
             r"laboratory tasks is often ordinary", TRACE),
            (rf"Patihis and colleagues, \ 2013: \ {p['hsam']} people with this memory and {p['controls']} controls, "
             r"\ given the DRM lists and misinformation", CUE),
            (r"they were just as susceptible: \ as many false lures, \ as much taken in from misleading accounts",
             FALSE),
            (r"even the best autobiographical memories are reconstructed", MODEL),
        ], 12.4, 25, 0.36).move_to([0, -0.2, 0])
        tag = historical_tag(archive.PATIHIS_2013.cite)
        with self.voiceover(
            "There are people today with a different kind of exceptional memory. <bookmark mark='a'/> In 2006 "
            "Elizabeth Parker, Larry Cahill and James McGaugh described a woman, AJ, who could tell you what she had "
            "done on almost any date since she was a teenager, and what day of the week it was, details they "
            "checked against her diaries. <bookmark mark='b'/> A few dozen such people have been found since. "
            "Their memory for word lists and laboratory tasks is often quite ordinary: what's exceptional is "
            "memory for their own lives. <bookmark mark='c'/> Are their memories exact recordings? In 2013 Lawrence "
            f"Patihis and colleagues gave {p['hsam']} of them, and {p['controls']} people of ordinary memory, the "
            "DRM lists and a misinformation task. <bookmark mark='d'/> They were just as susceptible: as many false "
            "recognitions of lures, as many details taken in from a misleading account. <bookmark mark='e'/> Even "
            "the most remarkable autobiographical memories are reconstructed."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def why_forget(self):
        head = heading(r"Why a good memory forgets")
        rng = np.random.default_rng(21)
        f = lambda v: np.sin(2 * np.pi * v * 0.8)  # noqa: E731
        x = np.sort(rng.uniform(0, 1, 16))
        y = f(x) + rng.normal(0, 0.35, 16)
        xx = np.linspace(0, 1, 300)
        coef = np.polyfit(x, y, 3)
        every = np.interp(xx, x, y)
        gist = np.polyval(coef, xx)
        xt = rng.uniform(0, 1, 20000)
        yt = f(xt) + rng.normal(0, 0.35, 20000)
        err_every = float(np.mean((np.interp(xt, x, y) - yt) ** 2))
        err_gist = float(np.mean((np.polyval(coef, xt) - yt) ** 2))
        A = axes([0, 1], [-2, 2], x_length=5.4, y_length=3.2, xticks=[], yticks=[], center=[-3.5, 0.2, 0],
                 font_size=18, xlabel=r"an illustration: \ sixteen noisy experiences of one regularity")
        pts = scatter(A.ax, x, y, TRACE, 0.08, 1.0)
        c_every = curve(A.ax, xx, every, LOST, 3)
        c_gist = curve(A.ax, xx, gist, MODEL, 4)
        errs = label(rf"error on new experiences: \ every detail {err_every:.2f}, \ the gist {err_gist:.2f}",
                     font_size=19, color=GREY_A).next_to(A, DOWN, buff=0.45)
        key = legend([(LOST, r"keep every detail"), (MODEL, r"keep the gist")], font_size=20)
        key.arrange(RIGHT, buff=0.5).next_to(A, UP, buff=0.15)
        rows = rows_of([
            (r"Richards and Frankland, \ 2017: \ the goal of memory is not to transmit information through time "
             r"but to make good decisions", WHITE),
            (r"in a changing world, \ old details mislead; \ forgetting them lets newer ones count", CUE),
            (r"and keeping every detail fits the noise: \ the memory that generalises best has forgotten the "
             r"particulars", MODEL),
            (r"what machine learning calls regularisation, \ and the power law calls the odds of need", CTX),
        ], 6.2, 22, 0.32).move_to([3.4, -0.1, 0])
        tag = published_tag(r"Richards \& Frankland (2017)")
        with self.voiceover(
            "S.'s difficulties suggest that forgetting is not only a failure. <bookmark mark='a'/> In 2017 Blake "
            "Richards and Paul Frankland argued that the goal of memory is not to carry information through time, "
            "but to help you make good decisions. <bookmark mark='b'/> In a world that changes, old details "
            "mislead: where you parked last month, a colleague's old phone number. Forgetting them lets the new "
            "ones count. <bookmark mark='c'/> And a memory that keeps every detail fits the noise in its "
            "experiences. Here are sixteen noisy experiences of one regularity. A memory that keeps every particular "
            "joins up every point, noise and all; a memory that keeps only the gist smooths them. On new experiences "
            "of the same regularity, the gist makes the smaller error. "
            "<bookmark mark='d'/> Machine learning calls this regularisation. Ebbinghaus's power law, read through "
            "Anderson and Schooler, calls it the odds of need. Both say that a good memory forgets, and forgets "
            "the right things."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(A), FadeIn(pts), FadeIn(key), FadeIn(rows[2]))
            self.play(Create(c_every), Create(c_gist))
            self.play(FadeIn(errs))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
