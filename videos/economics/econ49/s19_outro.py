from __future__ import annotations

from videos.economics.econ49.common import *  # noqa: F403

PROBLEMS = [
    r"Deterrence: \ potential offenders' gains are uniform on $[0, 10]$, \ the chance of being caught is 0.2 and the "
    r"sentence 5. \ What share of risk-neutral offenders offend? \ With the chance doubled? \ With the sentence "
    r"doubled?",
    r"Becker's planner: \ with those gains, \ harm 1 per offence, \ catching costing $p$ per potential offender and "
    r"fines up to 20, \ show that the fine should be the largest and find the best $p$.",
    r"The household: \ he earns 20 an hour, \ she 15; \ he makes 1 unit of home output an hour, \ she 2. \ Who has "
    r"the comparative advantage at home, \ and what does it cost to make 10 units each way?",
    r"Choo and Siow: \ 400 marriages between two types, \ 100 single men and 64 single women of those types. \ "
    r"What is the surplus $\Phi$?",
    r"Same-sex siblings: \ the first stage is 0.067 and the reduced form $-0.40$ weeks. \ Find the Wald estimate, "
    r"\ and say what it measures and for whom.",
    r"Quantity and quality: \ with $a = 0.3$, \ $b = 0.15$, \ full income 4 and $\pi = 0.2$, \ find $c$, \ $n$ "
    r"and $q$. \ What happens to $q$ if $\pi$ doubles?",
    r"Value added: \ estimates from two years have a spread of 0.156; \ one year's noise variance is 0.0185. \ "
    r"Find the reliability, \ and shrink a raw estimate of $+0.3$.",
    r"$\bigstar$ \ Rational addiction in two periods: \ $u = a c_1 - c_1^2/2 + \beta\,[a c_2 - c_2^2/2 + \gamma c_1 "
    r"c_2] - p_1 c_1 - \beta p_2 c_2$. \ Show that an announced rise in $p_2$ lowers $c_1$ when $\gamma > 0$.",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.answer()
        self.recap()
        self.problems()
        self.references()
        self.next_part()

    def answer(self):
        q = wrapped_label(ASK, 12.0, 40, E.ACCENT).move_to(UP * 2.2)
        a = wrapped_label(r"Far: \ penalties, \ marriages, \ children, \ schooling, \ health and even addiction "
                          r"respond to prices and constraints, \ measurably. \ But the measuring is hard, \ certainty "
                          r"deters more than severity, \ and where a price changes what an act means, \ the model "
                          r"breaks until those meanings are put into it.", 11.6, 25, WHITE)
        a.next_to(q, DOWN, buff=0.5)
        F = load("film")
        mini = plane([1950, 2023], [0, 1], x_length=4.2, y_length=1.3)
        v = np.array(F["v"])
        v = (v - v.min()) / (v.max() - v.min())
        logo = path(mini, F["t"], v, CHILD, 2.4, smooth=False).next_to(a, DOWN, buff=0.35)
        with self.voiceover(
            "So: how far can the model of choice under constraint be pushed into the rest of life? <bookmark "
            "mark='a'/> Far. Offenders respond to the chance of being caught; marriages sort by the gains they "
            "produce; families have fewer children as women's time grows dearer, and spend differently depending "
            "on whose purse the money reaches; smaller classes and better teachers raise scores; smokers respond to "
            "prices. But the measuring is hard, and it is where most of the work lies. The chance of being caught "
            "deters more than the length of the sentence. And where a price changes what an act means, a fine for "
            "lateness or a payment for blood, the simple model breaks, until those meanings are put into it."
        ) as vo:
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(a, shift=UP * 0.1), run_time=2)
            self.play(Create(logo), run_time=16.0, rate_func=linear)
            self.play(Indicate(a, color=E.ACCENT, scale_factor=1.0), run_time=2.0)
        self.clear_scene()

    def recap(self):
        O, Pl, Po, P, M, F, A, B, S, C, D, Ci = (load(x) for x in (
            "offenders", "planner", "police", "participation", "marriage", "fertility", "angrist", "bargain", "star",
            "caschools", "doctors", "cigarettes"))
        rn, ra, pm = O["play"]["risk-neutral"], O["play"]["risk-averse"], O["play"]["present-minded"]
        Ed = tables.EARLY_49.data

        def sg(x, k=2):
            return f"{x:+.{k}f}".replace("-", "{-}")

        Cr = tables.CRITICS_49.data
        items = [
            (rf"crime: \ offend if the gain beats $p \times S$; \ {100 * rn['start']:.0f}\% do on the Island", CRIME),
            (rf"Becker's planner: \ the largest fine, \ the smallest chance: \ {Pl['f_star']:.0f} and "
             rf"{100 * Pl['p_star']:.0f}\%, \ {100 * Pl['offences_star']:.1f}\% offend", FINE),
            (rf"chance or sentence: \ the same, \ the sentence ({100 * ra['double_s']:.0f}\%), \ the chance "
             rf"({100 * pm['double_p']:.0f}\%); \ the data: \ the chance", CHANCE),
            (rf"police: \ naive {sg(Po['naive'])}, \ noisy {sg(Po['fd_noisy'])}, \ random "
             rf"{sg(Po['experiment'])}; \ London {{-}}0.3 to {{-}}0.4", POLICE),
            (rf"the household: \ comparative advantage; \ women at work {P['w_first']:.0f}\% $\to$ "
             rf"{P['w_last']:.0f}\%", WOMEN),
            (rf"marriage: \ like marries like, \ {M['sorting']:.2f} times chance; \ the gains read from counts", CHILD),
            (rf"children: \ China {F['china_1970']:.1f} $\to$ {F['china_1979']:.1f} before 1980; \ a third child, \ "
             rf"about {abs(A['wald']['wald']):.0f} weeks less work", WOMEN),
            (rf"whose purse: \ a tenth to her, \ child spending {100 * B['rise']:+.0f}\%; \ the UK's child benefit",
             GAIN),
            (rf"schools: \ STAR {S['small']:+.1f} percentile points; \ California {sg(C['naive'])} $\to$ "
             rf"{sg(C['controls'])}; \ teachers 0.10--0.14", SCHOOL),
            (rf"early childhood: \ Perry {Ed['perry_lo']}--{Ed['perry_hi']}\%; \ scaled up, \ less; \ cover and "
             rf"visits: \ $\times${D['rr']['private']:.2f}, \ unsure", HEALTH),
            (rf"addiction: \ cigarettes {sg(Ci['cross'][0])}, \ ten years {sg(Ci['diff_both'][0])}; \ "
             r"forward-looking", DRUG),
            (rf"the critics: \ a fine raised lateness; \ pay cut women's blood giving {Cr['blood_before']}\% $\to$ "
             rf"{Cr['blood_paid']}\%", HOLD),
        ]
        rows = VGroup(*[label(rf"{n + 1}.\ \ {txt}", font_size=28, color=col) for n, (txt, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        head = label(r"Part 49, \ in twelve lines", font_size=42).to_edge(UP, buff=0.3)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.35 + 3.75
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.35)
        with self.voiceover(
            "Part forty-nine in twelve lines. <bookmark mark='r1'/> Crime is a choice: offend when the gain beats "
            "the expected punishment. <bookmark mark='r2'/> If fines cost nothing to impose, the cheapest deterrent "
            "is the largest fine and the thinnest enforcement. <bookmark mark='r3'/> Whether the chance or the "
            "sentence deters more depends on the offenders, and the data say the chance. <bookmark mark='r4'/> "
            "Police reduce crime, but only designs that move them for other reasons can show it. <bookmark "
            "mark='r5'/> Households divide work by comparative advantage, and women's work rose with their wages. "
            "<bookmark mark='r6'/> Like marries like, and the gains from each match can be read from who marries "
            "whom. <bookmark mark='r7'/> Fertility falls as women's time grows dearer, and a third child costs its "
            "mother weeks of work. <bookmark mark='r8'/> Who receives the money matters. <bookmark mark='r9'/> "
            "Smaller classes and better teachers raise scores. <bookmark mark='r10'/> Small early programmes can "
            "pay well, and scaling them is hard; health is chosen, in part, and its markets are not like others. "
            "<bookmark mark='r11'/> Smokers "
            "respond to prices, and look ahead. <bookmark mark='r12'/> And a price can change the meaning of an "
            "act, and break the model."
        ) as vo:
            self.play(FadeIn(head))
            for i, r_ in enumerate(rows):
                vo.wait_until(f"r{i + 1}")
                self.play(FadeIn(r_, shift=RIGHT * 0.15), run_time=0.8)
            self.play(Indicate(rows, color=WHITE, scale_factor=1.0), run_time=2.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=19, width=13.0)
        with self.voiceover(
            "The problems. Deterrence with uniform gains; Becker's planner; comparative advantage at home; reading "
            "a marriage surplus from counts; the Wald estimate for same-sex siblings; quantity and quality; "
            "shrinking a teacher's value added; and a starred problem on why a rational addict cuts back before a "
            "price rise. Full solutions are in the part's notes."
        ):
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0], shift=UP * 0.1), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r) for r in ps.rows[1:]], lag_ratio=0.4), run_time=6)
        self.wait(4)
        self.clear_scene()

    def references(self):
        rc = reference_card(
            [r"Gary Becker, \emph{The Economic Approach to Human Behavior} (1976) and \emph{A Treatise on the Family} "
             r"(1981)",
             r"Steven Levitt and Stephen Dubner, \emph{Freakonomics} (2005), \ for the stories, \ read critically",
             r"Claudia Goldin, \emph{Career and Family} (2021)",
             r"Anne Case and Angus Deaton, \emph{Deaths of Despair and the Future of Capitalism} (2020)"],
            [r"Becker (1965, 1968, 1973); \ Becker and Lewis (1973); \ Grossman (1972); \ Becker and Murphy (1988)",
             r"Levitt (1997); \ Angrist and Evans (1998); \ Krueger (1999); \ Angrist and Lavy (1999, 2019)",
             r"Lazear (2000); \ Gneezy and Rustichini (2000); \ Goldin and Katz (2002); \ Di Tella and Schargrodsky "
             r"(2004)",
             r"Choo and Siow (2006); \ Heckman et al. (2010); \ Draca et al. (2011); \ Wei and Zhang (2011)",
             r"Nagin (2013); \ Chetty et al. (2014); \ Case and Deaton (2015); \ Lee and McCrary (2017)",
             r"Chalfin and McCrary (2018); \ Cooper et al. (2019); \ Alpert et al. (2022); \ Durkin et al. (2022)"])
        with self.voiceover(
            "The reading: Becker's own The Economic Approach to Human Behavior and A Treatise on the Family; "
            "Freakonomics, for its stories, read critically; Claudia Goldin's Career and Family; and Anne Case and "
            "Angus Deaton's Deaths of Despair. Then the papers, from Becker's to the newest experiments."
        ):
            self.play(FadeIn(rc))
        self.wait(1.5)
        self.clear_scene()

    def next_part(self):
        hc = history_card(2021, r"the expanded Child Tax Credit", r"for six months, \ most American families receive "
                          r"a monthly payment for each child; \ then Congress lets it lapse", color=E.ACCENT,
                          width=10.4, font_size=24)
        nxt = VGroup(label(r"Next: \ Part 50 \ $\cdot$ \ Act IX, \ The Fields", font_size=30, color=GREY_B),
                     label(r"The Policy Memo", font_size=46),
                     label(r"a minister asks whether to do it: \ what do you write?", font_size=24,
                           color=E.ACCENT)).arrange(DOWN, buff=0.22)
        head = label(r"from the family \ to the minister's desk", font_size=26, color=GREY_A).to_edge(UP, buff=0.5)
        steps = VGroup(*[VGroup(RoundedRectangle(width=2.7, height=0.9, corner_radius=0.12, stroke_color=c_,
                                                 stroke_width=2.0), label(t_, font_size=18, color=c_))
                         for t_, c_ in ((r"the question", GREY_A), (r"the evidence", SCHOOL), (r"the Island", CHILD),
                                        (r"the memo", E.ACCENT))])
        for s_ in steps:
            s_[1].move_to(s_[0])
        steps.arrange(RIGHT, buff=0.35)
        VGroup(hc, steps, nxt).arrange(DOWN, buff=0.45).next_to(head, DOWN, buff=0.4)
        with self.voiceover(
            "Next time, the capstone of this act. <bookmark mark='a'/> In 2021 the United States paid most families "
            "a monthly sum for each child, for six months, and then let the payments lapse. Should a country pay a "
            "child allowance, and how large? <bookmark mark='b'/> Part fifty takes one such proposal from the "
            "question to the evidence, runs it on the Island under the full range of the dials, <bookmark "
            "mark='c'/> and ends with the memo a minister would read: what to do, who gains and loses, and how sure "
            "we are."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.1))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(s_) for s_ in steps], lag_ratio=0.4), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(nxt, shift=UP * 0.1))
        self.wait(9.5)
