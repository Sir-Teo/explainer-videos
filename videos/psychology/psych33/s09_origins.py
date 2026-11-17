from __future__ import annotations

from videos.psychology.psych33.common import *  # noqa: F403


class Origins(VoiceoverScene):
    def construct(self):
        self.card()
        self.genes()
        self.temperament()
        self.biology()
        self.two_tests()

    def card(self):
        card = chapter_card(8, r"Where traits come from", r"Genes, \ families, \ and the brain?",
                            lit={1970: r"Gray", 2015: r"Vukasovi\'c \& Bratko"}, part=PART,
                            scale=("gene", "brain", "person"), marr=("what", "how"))
        with self.voiceover("Chapter eight. Where traits come from."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def genes(self):
        head = heading(r"Heritability, \ about .4")
        A = axes([-0.6, 2.6], [0, 0.6], x_length=5.2, y_length=3.8, xticks=None, yticks=[0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6],
                 yfmt=lambda v: f"{v:g}", ylabel=r"heritability", center=[-3.4, -0.4, 0], font_size=15)
        vals = [(0, 0.40, r"all 62 estimates", A_), (1, 0.47, r"twin studies", GOOD), (2, 0.22, r"family and adoption",
                                                                                           C_)]
        bs = VGroup()
        for x, v, t, c in vals:
            bs.add(VGroup(bars(A.ax, [x], [v], c, width=0.6), label(f"{v:.2f}", font_size=17, color=c)
                          .next_to(A.ax.c2p(x, v), UP, buff=0.08),
                          wrapped_label(t, 1.6, 16, GREY_A).next_to(A.ax.c2p(x, 0), DOWN, buff=0.15)))
        rows = rows_of([
            (r"Vukasovi\'c and Bratko, \ 2015: \ 62 estimates, \ more than 100{,}000 people: \ about 40\% "
             r"of the differences in personality traits come with differences in genes", WHITE),
            (r"twin studies give more than family and adoption studies: \ the estimate depends on the design, \ as "
             r"Part 9 showed", GOOD),
            (r"what remains is mostly not the family people share: \ adoptive siblings grow up together and end up "
             r"barely more alike than strangers \ (Part 9)", C_),
            (r"so the environment that matters is the one each person meets on their own", YOU),
        ], 6.4, 20, 0.36).move_to([3.0, -0.3, 0])
        tag = published_tag(r"Vukasovi\'c \& Bratko (2015)")
        with self.voiceover(
            "Where do traits come from? Start with genes. <bookmark mark='a'/> In 2015 Vukasović and Bratko pooled"
            " sixty-two estimates from more than a hundred thousand people. About forty percent of the "
            "differences between people in personality traits come with differences in their genes. That's your "
            "fourth number. <bookmark mark='b'/> Twin studies give more, point four seven, than family and adoption "
            "studies, point two two. The estimate depends on the design, as Part 9 showed. <bookmark mark='c'/> And "
            "what remains is mostly not the family people share. Adoptive siblings, raised together, end up barely "
            "more alike than strangers, as Part 9 showed. <bookmark mark='d'/> The environment that matters "
            "is the one each person meets on their own."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(bs[0]), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(bs[1:]), FadeIn(rows[1]))
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def temperament(self):
        head = heading(r"Temperament: \ a trait before experience")
        chain = flow_chain([
            (r"about 1 baby in 5 thrashes and cries at new sights, \ sounds and smells", N_),
            (r"inhibited: \ quiet with a stranger, \ slow to touch a new toy", N_),
            (r"as a group, \ still quieter and more cautious", AGE),
            (r"more often subdued and anxious; \ few had become bold", COHORT),
        ], box_w=3.0, box_h=1.45, buff=0.42, font_size=20,
            notes=[r"4 months: \ high-reactive", r"1 to 2 years", r"7\textonehalf\ years", r"adolescence"],
            note_size=19)
        chain.move_to([0, 1.25, 0])
        who = label(r"Jerome Kagan's children, \ followed from infancy", font_size=21, color=GREY_A)
        who.next_to(chain, UP, buff=0.22)
        checks = verdict_row([
            (r"Caspi and Silva, \ 1995: \ about 1{,}000 Dunedin children; \ inhibited at three, \ more cautious "
             r"and less forceful at eighteen", "replicated, smaller"),
            (r"Clauss and Blackford, \ 2012: \ a meta-analysis; \ inhibited children had more than seven times "
             r"the odds of later social anxiety disorder", "replicated"),
        ], width=12.4, font_size=20)
        checks.move_to([0, -1.65, 0])
        moral = label(r"a narrower range of outcomes, \ not a destiny", font_size=22, color=YOU)
        moral.next_to(checks, DOWN, buff=0.3)
        tag = published_tag(r"Kagan, \ Reznick \& Snidman (1988); \ Caspi \& Silva (1995); \ Clauss \& Blackford "
                            r"(2012)")
        with self.voiceover(
            "If traits are partly inherited, something like them should show before life has had much say. Part 30 "
            "met Alexander Thomas and Stella Chess's easy, difficult and slow-to-warm-up babies, sorted from what "
            "their parents reported. <bookmark mark='a'/> Jerome Kagan brought temperament into the laboratory. At "
            "four months he showed babies moving mobiles, recorded voices and new smells. About one in five "
            "thrashed and cried, and he called them high-reactive. <bookmark mark='b'/> As toddlers, many of these "
            "children were inhibited: quiet with a stranger, slow to touch a new toy, staying close to their "
            "mothers. In 1988 Kagan, Steven Reznick and Nancy Snidman reported that children picked out near the "
            "age of two as extremely inhibited or uninhibited still differed, as groups, at seven and a half. "
            "<bookmark mark='c'/> Followed into adolescence, high-reactive infants were more often subdued and "
            "anxious, and few had become bold. But many had moved toward the middle. <bookmark mark='d'/> Other "
            "cohorts agree. In New Zealand's Dunedin study of about a thousand children, Avshalom Caspi and Phil "
            "Silva found that inhibited three-year-olds were more cautious and less forceful at eighteen. And a "
            "2012 meta-analysis by Jacqueline Clauss and Jennifer Blackford found that behaviourally inhibited "
            "children had more than seven times the odds of a later social anxiety disorder. "
            "<bookmark mark='e'/> So temperament narrows the range of outcomes rather than fixing one. And "
            "inhibition, the clearest early form of a trait, looks like the anxious end of the systems that the "
            "next theories describe."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(who))
            vo.wait_until("a")
            self.play(FadeIn(chain.boxes[0]), FadeIn(chain.notes[0]))
            vo.wait_until("b")
            self.play(GrowArrow(chain.arrows[0]), FadeIn(chain.boxes[1]), FadeIn(chain.notes[1]))
            self.play(GrowArrow(chain.arrows[1]), FadeIn(chain.boxes[2]), FadeIn(chain.notes[2]))
            vo.wait_until("c")
            self.play(GrowArrow(chain.arrows[2]), FadeIn(chain.boxes[3]), FadeIn(chain.notes[3]))
            vo.wait_until("d")
            self.play(FadeIn(checks.rows[0], shift=RIGHT * 0.15))
            self.play(FadeIn(checks.rows[1], shift=RIGHT * 0.15))
            vo.wait_until("e")
            self.play(FadeIn(moral, shift=UP * 0.1))
        self.clear_scene()

    def biology(self):
        head = heading(r"Biological theories")
        left = VGroup(label(r"Hans Eysenck", font_size=28, color=E_),
                      wrapped_label(r"three dimensions: \ extraversion, \ neuroticism, \ and psychoticism \ (a poor "
                                    r"name for a tough-minded, \ impulsive streak)", 5.6, 21, WHITE),
                      wrapped_label(r"extraverts, \ he proposed, \ have a lower resting arousal and seek stimulation "
                                    r"to make it up", 5.6, 21, E_)).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        right = VGroup(label(r"Jeffrey Gray", font_size=28, color=N_),
                       wrapped_label(r"two systems: \ a behavioural inhibition system, \ sensitive to punishment, \ "
                                     r"and a behavioural activation system, \ sensitive to reward", 5.6, 21, WHITE),
                       wrapped_label(r"anxiety as a sensitive inhibition system; \ impulsivity as a sensitive "
                                     r"activation system: \ roughly neuroticism and extraversion, \ rotated", 5.6, 21,
                                     N_)).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        VGroup(left, right).arrange(RIGHT, buff=0.8, aligned_edge=UP).move_to([0, 0.6, 0])
        foot = wrapped_label(r"Part 17's reward learning and Part 29's fear circuits are where these theories meet the "
                             r"brain; \ the links found so far are real but small", 12.0, 22, YOU).to_edge(DOWN, buff=0.8)
        tag = historical_tag(r"Eysenck; \ Gray (1970)")
        with self.voiceover(
            "Two biological theories set the agenda. <bookmark mark='a'/> Hans Eysenck proposed three dimensions: "
            "extraversion, neuroticism, and psychoticism, a poor name for a tough-minded, impulsive streak. "
            "Extraverts, he argued, have a lower resting arousal, and seek stimulation to make it up. "
            "<bookmark mark='b'/> From 1970 Jeffrey Gray proposed two systems: a behavioural inhibition system, "
            "sensitive to punishment, and a behavioural activation system, sensitive to reward. Anxiety is a "
            "sensitive inhibition system, impulsivity a sensitive activation system: roughly neuroticism and "
            "extraversion, rotated. <bookmark mark='c'/> Part 17's reward learning and Part 29's fear circuits are "
            "where these theories meet the brain. The links found so far are real, but small."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in left], lag_ratio=0.5), run_time=2.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in right], lag_ratio=0.5), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()

    def two_tests(self):
        d = load("eysenck")
        head = heading(r"Two tests, \ two traits")
        names = [r"EPI extraversion", r"EPI neuroticism", r"BFI extraversion", r"BFI neuroticism"]
        hm = heatmap(d["R"], names=names, cell=1.0, font_size=20, lo=0.0, hi=0.8).move_to([-2.2, -0.4, 0])
        R = d["R"]
        rows = rows_of([
            (rf"{d['n']} people took Eysenck's inventory and the SAPA items", WHITE),
            (rf"the same trait by two methods agrees: \ extraversion {R[0, 2]:.2f}, \ neuroticism {R[1, 3]:.2f}", GOOD),
            (rf"different traits barely agree, \ by either method: \ {R[0, 3]:.2f} to {R[1, 2]:.2f}", GREY_A),
            (r"Part 3's multitrait-multimethod logic: \ convergent and discriminant validity, \ in one small table", MODEL),
        ], 4.8, 21, 0.38).move_to([4.1, -0.3, 0])
        tag = published_tag(r"data: \ psychTools \texttt{epi.bfi}, \ recomputed")
        with self.voiceover(
            "Eysenck's dimensions and the five can be checked against each other. <bookmark mark='a'/> Here "
            f"{d['n']} people took both Eysenck's inventory and the SAPA items. <bookmark mark='b'/> The same trait "
            f"measured two ways agrees: extraversion at {R[0, 2]:.2f}, neuroticism at {R[1, 3]:.2f}. "
            "<bookmark mark='c'/> Different traits barely agree, whichever method measures them. "
            "<bookmark mark='d'/> That's Part 3's multitrait-multimethod logic, convergent and discriminant validity, "
            "in one small table."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(hm))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
