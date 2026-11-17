from __future__ import annotations

from videos.psychology.psych53.common import *  # noqa: F403


class History(VoiceoverScene):
    def construct(self):
        card_section(self, 2, r"Testing a nation", r"Where did psychology at work begin?", scale=("society",))
        self.early()
        self.army()

    def early(self):
        chips_section(self, r"Before the tests", [
            (r"Taylor", r"Frederick Taylor's scientific management: \ time each motion, \ find the one best way, \ pay "
                        r"by the piece", AUTH),
            (r"M\"unsterberg", r"Hugo M\"unsterberg's 1913 book applied laboratory psychology to work: \ tests for "
                             r"tram drivers and telephone operators", MODEL),
            (r"the Gilbreths", r"Frank and Lillian Gilbreth's motion studies, \ and Lillian's attention to fatigue and "
                               r"the worker", PERSON),
            (r"the gap", r"none of them could yet say how well a test predicted who would do the job well", YOU),
        ], "Psychology at work began before the tests. <bookmark mark='a'/> Frederick Taylor's scientific management "
           "timed each motion, looked for the one best way, and paid by the piece. <bookmark mark='b'/> In 1913 Hugo "
           "Munsterberg applied laboratory psychology to work, with tests for tram drivers and telephone operators. "
           "<bookmark mark='c'/> Frank and Lillian Gilbreth studied motions, and Lillian Gilbreth attended to fatigue "
           "and to the worker. <bookmark mark='d'/> But none of them could yet say how well a test predicted who "
           "would do the job well.", chip_w=3.2, text_w=9.0)

    def army(self):
        rows_section(self, r"1917: \ the Army tests", [
            (r"Part 32's story: \ when the US entered the war, \ Robert Yerkes's committee built group tests, \ Alpha "
             r"for those who read English and Beta for those who did not", WHITE),
            (r"about 1.75 million recruits were tested: \ the first mass testing", MODEL),
            (r"the tests sorted men into roles and officer training; \ their later use to rank national groups was "
             r"bad science and worse policy (Part 32)", AUTH),
            (r"after the war, \ testing moved into industry: \ personnel psychology began asking the question of this "
             r"part, \ with correlations", PERSON),
        ], "Then came a war. <bookmark mark='a'/> It's Part 32's story. When the United States entered the First "
           "World War, Robert Yerkes's committee built group tests: Alpha for recruits who read English, and Beta for "
           "those who didn't. <bookmark mark='b'/> About one and three quarter million recruits were tested, the "
           "first mass testing. <bookmark mark='c'/> The tests sorted men into roles and officer training. Their "
           "later use to rank national groups was bad science and worse policy. <bookmark mark='d'/> After the war, "
           "testing moved into industry, and personnel psychology began asking this part's question with "
           "correlations.")
