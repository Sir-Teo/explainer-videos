from __future__ import annotations

from videos.psychology.psych57.common import *  # noqa: F403


class Gap(VoiceoverScene):
    def construct(self):
        card_section(self, 9, r"The treatment gap", r"How many people who need help get it?", scale=("society",))
        self.gap()
        self.sim()
        self.iapt()

    def gap(self):
        rows_section(self, r"Prevalence against capacity", [
            (r"Part 39: \ in a year, \ roughly one adult in five has a diagnosable mental disorder", WHITE),
            (r"the World Mental Health surveys: \ a minority of them receive any treatment, \ and in low-income "
             r"countries, \ a small minority", AUTH),
            (r"treatments that work exist (Part 42); \ the bottleneck is trained people, \ money and access", MODEL),
            (r"the question becomes logistics: \ who gets what, \ when, \ and how do we know it worked?", YOU),
        ], "How many people who need help get it? <bookmark mark='a'/> From Part 39: in a year, roughly one adult in "
           "five has a diagnosable mental disorder. <bookmark mark='b'/> The World Mental Health surveys found that a "
           "minority of them receive any treatment, and in low-income countries, a small minority. "
           "<bookmark mark='c'/> Treatments that work exist, as Part 42 showed. The bottleneck is trained people, "
           "money and access. <bookmark mark='d'/> So the question becomes logistics: who gets what, when, and how do "
           "we know it worked?")

    def sim(self):
        d = load("care")
        head = heading(r"Three ways to run a service")
        A = axes([0.3, 4.7], [0, 0.85], x_length=5.4, y_length=3.0, xticks=None, yticks=[0, 0.4, 0.8],
                 yfmt=lambda v: f"{100 * v:.0f}\\%", ylabel=r"recovered within 26 weeks", center=[-3.3, 0.3, 0],
                 font_size=12)
        cols = [AUTH, MODEL, PERSON, GOOD]
        b = bars(A.ax, [1, 2, 3, 4], d["recovered_26"], cols, width=0.6)
        names = VGroup(*[label(s, font_size=12, color=c).next_to(A.ax.c2p(i + 1, 0), DOWN, buff=0.12)
                         for i, (s, c) in enumerate(zip([r"therapy only", r"matched", r"stepped", r"stepped, "
                                                                                                 r"rebalanced"], cols))])
        waits = VGroup(*[label(rf"wait {w:.0f} wk", font_size=12, color=GREY_A).next_to(A.ax.c2p(i + 1, r), UP,
                                                                                           buff=0.08)
                         for i, (w, r) in enumerate(zip(d["mean_wait"], d["recovered_26"]))])
        rows = rows_of([
            (r"Psyche's service: \ 100 referrals a week; \ 70 start guided self-help (6 weeks) and 30 start therapy "
             r"(12 weeks) each week; \ 30\% are severe", WHITE),
            (rf"therapy for everyone: \ a waiting list that grows, \ an average wait of {d['mean_wait'][0]:.0f} weeks, "
             rf"\ {100 * d['recovered_26'][0]:.0f}\% recovered within six months", AUTH),
            (rf"matched (severe to therapy): \ {100 * d['recovered_26'][1]:.0f}\%; \ stepped (everyone starts with "
             rf"self-help; \ non-responders step up): \ {100 * d['recovered_26'][2]:.0f}\%, \ but with a {d['mean_wait'][2]:.0f}-week "
             rf"wait for the first step", PERSON),
            (rf"give self-help 100 places and therapy 60, \ enough for the six in ten who step up: \ the first wait "
             rf"falls below a week, \ and {100 * d['recovered_26'][3]:.0f}\% recover within six months", GOOD),
        ], 6.0, 18, 0.32).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{work.stepped\_care}, \ illustrative capacities")
        with self.voiceover(
            "Here are three ways to run a service. <bookmark mark='a'/> Psyche's service gets a hundred referrals a "
            "week. Each week, seventy can start six weeks of guided self-help and thirty can start twelve weeks of "
            "therapy. Thirty percent of people are severe. <bookmark mark='b'/> If everyone waits for therapy, the "
            "waiting list grows, the average wait is almost a year, and only about three in ten recover within six "
            "months. <bookmark mark='c'/> Matched care, with the severe going to therapy, gets about half. Stepped care, "
            "where everyone starts with self-help and non-responders step up, gets a little more, but now people wait "
            "fourteen weeks for the first step. <bookmark mark='d'/> Give self-help a hundred places and therapy "
            "sixty, enough for the six in ten who step up, and the first wait falls below a week, with about three "
            "quarters recovered within six months. Capacity has to match the flow at every step."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(names))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(b[0]), FadeIn(waits[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(b[1]), FadeIn(waits[1]), FadeIn(b[2]), FadeIn(waits[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]), FadeIn(b[3]), FadeIn(waits[3]))
        self.clear_scene()

    def iapt(self):
        rows_section(self, r"A national programme that counts", [
            (r"2008: \ England's Improving Access to Psychological Therapies, \ now NHS Talking Therapies, \ built "
             r"on the economist Richard Layard's case and David Clark's design", WHITE),
            (r"stepped care for depression and anxiety disorders, \ with thousands of newly trained therapists", MODEL),
            (r"its distinguishing rule: \ symptom questionnaires at every session, \ so outcomes are known for "
             r"nearly every patient, \ not a sample", GOOD),
            (r"about half of those who finish treatment are reported as recovered; \ the data also expose the "
             r"services and groups that do worse", PERSON),
            (r"no control group: \ the recovery rate includes natural recovery (chapter three), \ and comparing "
             r"services needs care", AUTH),
        ], "One country built this at scale. <bookmark mark='a'/> In 2008 England began Improving Access to "
           "Psychological Therapies, now NHS Talking Therapies, built on the economist Richard Layard's case and the "
           "psychologist David Clark's design. <bookmark mark='b'/> It offers stepped care for depression and anxiety "
           "disorders, with thousands of newly trained therapists. <bookmark mark='c'/> Its distinguishing rule: "
           "symptom questionnaires at every session, so outcomes are known for nearly every patient, not a sample. "
           "<bookmark mark='d'/> About half of those who finish treatment are reported as recovered, and the data "
           "also expose the services and groups that do worse. <bookmark mark='e'/> There's no control group, so the "
           "recovery rate includes natural recovery, and comparing services needs care.",
           tag=published_tag(r"Clark (2018)"))
