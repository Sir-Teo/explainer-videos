from __future__ import annotations

from videos.psychology.psych53.common import *  # noqa: F403


class Teams(VoiceoverScene):
    def construct(self):
        card_section(self, 12, r"Satisfaction, \ teams and where people work", r"Is a happy worker a productive one?",
                     scale=("person", "society"))
        self.satisfaction()
        self.safety()
        self.leaders()
        self.home()

    def satisfaction(self):
        rows_section(self, r"Satisfaction and performance", [
            (r"the ``happy worker'' hypothesis is old, \ and was once declared dead: \ early reviews found tiny "
             r"correlations", WHITE),
            (r"Timothy Judge and colleagues, \ 2001: \ correcting for unreliability across 312 samples, \ the "
             r"correlation is about 0.3", MODEL),
            (r"which direction? \ doing well can make people satisfied as much as the reverse; \ a correlation cannot "
             r"say (Part 2)", AUTH),
            (r"engagement surveys measure the same territory, \ with Part 46's cautions about how questions are "
             r"answered", PERSON),
        ], "Is a happy worker a productive one? <bookmark mark='a'/> The hypothesis is old, and it was once declared "
           "dead, because early reviews found tiny correlations. <bookmark mark='b'/> In 2001 Timothy Judge and "
           "colleagues corrected for unreliability across three hundred and twelve samples, and found a correlation "
           "of about zero point three. <bookmark mark='c'/> But which way does it run? Doing well can make people "
           "satisfied as much as the reverse, and a correlation can't say. <bookmark mark='d'/> Engagement surveys "
           "measure the same territory, with Part 46's cautions about how questions get answered.",
           tag=published_tag(r"Judge et al.\ (2001)"))

    def safety(self):
        rows_section(self, r"Psychological safety", [
            (r"Amy Edmondson, \ 1999: \ in a manufacturing company's teams, \ a shared belief that the team is safe "
             r"for interpersonal risk predicted learning behaviour and performance", WHITE),
            (r"in hospital units she found the better teams reported more errors: \ not because they made more, \ "
             r"but because they were willing to say so", GOOD),
            (r"the link to Part 51: \ crew resource management is psychological safety, \ trained", MODEL),
            (r"most of the evidence is correlational and from surveys; \ interventions that raise it are harder to "
             r"test", PERSON),
        ], "Teams have their own psychology. <bookmark mark='a'/> In 1999 Amy Edmondson found that in a "
           "manufacturing company's teams, a shared belief that the team was safe for interpersonal risk predicted "
           "learning behaviour and performance. <bookmark mark='b'/> In hospital units, she had earlier found that "
           "the better teams reported more errors, not because they made more, but because they were willing to say "
           "so. <bookmark mark='c'/> It's the link to Part 51: crew resource management is psychological safety, "
           "trained. <bookmark mark='d'/> Most of the evidence is correlational and from surveys, and interventions "
           "that raise it are harder to test.", tag=published_tag(r"Edmondson (1999)"))

    def leaders(self):
        head = heading(r"Leaders")
        q = quadrant([
            (r"structure, \ little care", r"tasks and deadlines", AUTH),
            (r"both", r"what the Ohio studies hoped for", GOOD),
            (r"neither", r"absent", GREY_B),
            (r"care, \ little structure", r"warm, \ supportive", CARE),
        ], xlabel=r"consideration", ylabel=r"initiating structure", size=4.4, font_size=19)
        q.move_to([-4.0, -0.15, 0])
        checks = verdict_row([
            (r"Lewin, \ Lippitt and White, \ 1939: \ boys' clubs under autocratic, \ democratic and laissez-faire "
             r"leaders", "story and record"),
            (r"traits: \ the Big Five predict who emerges and who is rated effective \ (Judge and colleagues, \ "
             r"2002)", "replicated"),
            (r"consideration and structure both relate to outcomes \ (Judge, \ Piccolo and Ilies, \ 2004)",
             "replicated"),
            (r"transformational leadership causes performance: \ the questionnaires mix leading with its effects \ "
             r"(van Knippenberg and Sitkin, \ 2013)", "contested"),
        ], width=7.6, font_size=18)
        checks.move_to([2.75, -0.2, 0])
        tag = published_tag(r"Lewin, \ Lippitt \& White (1939); \ Judge et al.\ (2002); \ Judge, \ Piccolo \& Ilies "
                            r"(2004); \ van Knippenberg \& Sitkin (2013)")
        with self.voiceover(
            "Every team has someone in charge, and leadership is one of the largest literatures in work psychology. "
            "<bookmark mark='a'/> It began with an experiment. In 1939 Kurt Lewin, Ronald Lippitt and Ralph White "
            "ran after-school clubs for ten-year-old boys, with adults trained to lead in an autocratic, a "
            "democratic or a laissez-faire style. The autocratic clubs turned either aggressive or apathetic; the "
            "democratic ones were the boys' favourites. It was a few small groups, and it's remembered more than "
            "it's repeated. <bookmark mark='b'/> The search for a leader's traits was declared a failure in the "
            "nineteen-forties, and then revived: in 2002 Timothy Judge and colleagues found that the Big Five "
            "predict who emerges as a leader and who is rated effective, extraversion most of all. "
            "<bookmark mark='c'/> Studies at Ohio State described leaders on two dimensions: consideration, care "
            "for the people, and initiating structure, care for the task. In 2004 Judge, Ronald Piccolo and Remus "
            "Ilies found both related to outcomes, consideration more to satisfaction and structure more to "
            "performance. <bookmark mark='d'/> The idea of the last forty years is transformational leadership: "
            "leaders who inspire, and change what followers want. Its questionnaires correlate well with outcomes. "
            "But in 2013 Daan van Knippenberg and Sim Sitkin argued that the questionnaires mix the leader's "
            "behaviour with its effects, and are usually filled in by the same people who rate the results, so "
            "the correlations say less than they seem to. <bookmark mark='e'/> A measure that contains its own "
            "outcome is Part 3's validity problem, at the top of the organisation."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(checks.rows[0], shift=RIGHT * 0.15))
            vo.wait_until("b")
            self.play(FadeIn(checks.rows[1], shift=RIGHT * 0.15))
            vo.wait_until("c")
            self.play(FadeIn(q.axes), LaggedStart(*[FadeIn(c_) for c_ in q.cells], lag_ratio=0.25),
                      FadeIn(checks.rows[2], shift=RIGHT * 0.15), run_time=2.2)
            vo.wait_until("d")
            self.play(FadeIn(checks.rows[3], shift=RIGHT * 0.15))
            vo.wait_until("e")
            self.play(Indicate(checks.rows[3].chip, scale_factor=1.1))
        self.clear_scene()

    def home(self):
        rows_section(self, r"Working from home, \ randomized", [
            (r"Nicholas Bloom and colleagues, \ 2015: \ a Chinese travel company's call-centre staff who volunteered "
             r"were randomized to work from home for nine months", WHITE),
            (r"performance rose by about 13\%, \ mostly more calls from fewer breaks and sick days; \ quitting fell by "
             r"about half", GOOD),
            (r"but promotion rates fell for the home workers, \ and many chose to return to the office afterwards", AUTH),
            (r"later trials of hybrid work found little change in performance and lower quitting: \ the answer "
             r"depends on the job and the arrangement", MODEL),
        ], "And where people work can be randomized. <bookmark mark='a'/> In 2015 Nicholas Bloom and colleagues "
           "reported a trial at a Chinese travel company. Call-centre staff who volunteered were randomized to work "
           "from home for nine months. <bookmark mark='b'/> Performance rose by about thirteen percent, mostly more "
           "calls from fewer breaks and sick days, and quitting fell by about half. <bookmark mark='c'/> But "
           "promotion rates fell for the home workers, and many chose to return to the office afterwards. "
           "<bookmark mark='d'/> Later trials of hybrid work found little change in performance and lower quitting. "
           "The answer depends on the job and the arrangement.", tag=published_tag(r"Bloom et al.\ (2015)"))
