from __future__ import annotations

from videos.psychology.psych56.common import *  # noqa: F403


class Children(VoiceoverScene):
    def construct(self):
        card_section(self, 9, r"Children, \ suggestion and implanted memories", r"Can questioning create a memory?",
                     scale=("person", "society"))
        self.daycare()
        self.nichd()
        self.implanted()

    def daycare(self):
        rows_section(self, r"The day-care cases", [
            (r"1980s: \ a series of US day-care abuse prosecutions rested on children's accounts produced by "
             r"repeated, \ leading interviews", WHITE),
            (r"Ceci and Bruck's experiments: \ young children asked repeatedly about events that never happened came "
             r"to report them, \ with detail", AUTH),
            (r"the interviews in the cases used the techniques the experiments showed were dangerous: \ repetition, \ "
             r"rewards for answers, \ ``the other children told us''", PERSON),
            (r"most of the convictions were later overturned", MODEL),
            (r"preschoolers were the most suggestible; \ older children and adults less so, \ though not immune",
             GOOD),
        ], "Can questioning create a memory? <bookmark mark='a'/> In the nineteen eighties a series of American "
           "day-care abuse prosecutions rested on children's accounts, produced by repeated, leading interviews. "
           "<bookmark mark='b'/> In Stephen Ceci and Maggie Bruck's experiments, young children asked repeatedly "
           "about events that never happened came to report them, with detail. <bookmark mark='c'/> The interviews in "
           "the cases used exactly the techniques the experiments showed were dangerous: repetition, rewards for "
           "answers, and the other children told us. <bookmark mark='d'/> Most of the convictions were later "
           "overturned. <bookmark mark='e'/> Preschoolers were the most suggestible. Older children and "
           "adults are less so, though not immune.",
           tag=published_tag(r"Ceci \& Bruck (1995)"))

    def implanted(self):
        rows_section(self, r"The memory wars", [
            (r"Part 21's rows: \ the misinformation effect, \ and false memories for whole events, \ ``lost in a "
             r"shopping mall''", WHITE),
            (r"1990s: \ therapy that searched for repressed memories of abuse produced accusations, \ some later "
             r"retracted", AUTH),
            (r"the research does not show that real abuse is forgotten rarely, \ or remembered falsely often; \ it "
             r"shows that suggestive techniques can create detailed, \ confident, \ false memories", MODEL),
            (r"for a court: \ how the memory was obtained matters as much as how confident it is (chapter four's "
             r"lesson, \ again)", YOU),
        ], "This led to the memory wars. <bookmark mark='a'/> Part 21 entered the rows: the misinformation effect, "
           "and false memories for whole events, like being lost in a shopping mall as a child. "
           "<bookmark mark='b'/> In the nineteen nineties, therapy that searched for repressed memories of abuse "
           "produced accusations, some later retracted. <bookmark mark='c'/> The research doesn't show that real "
           "abuse is rarely forgotten, or often falsely remembered. It shows that suggestive techniques can create "
           "detailed, confident, false memories. <bookmark mark='d'/> For a court, how a memory was obtained matters "
           "as much as how confident it is. That's chapter four's lesson, again.")

    def nichd(self):
        rows_section(self, r"How to interview a child", [
            (r"the NICHD protocol (Lamb and colleagues): \ build rapport, \ practise telling a neutral event in "
             r"detail, \ then invite free recall: \ ``tell me everything that happened''", WHITE),
            (r"open prompts (``tell me more about...'') draw longer and more accurate accounts than yes-or-no and "
             r"option questions", GOOD),
            (r"no repeated questions, \ no rewards for answers, \ no ``other children told us'': \ the day-care "
             r"cases' errors, \ removed by design", MODEL),
            (r"field studies of trained interviewers found more information from open prompts, \ and young "
             r"children can give reliable accounts when asked this way", PERSON),
        ], "So how should a child be interviewed? <bookmark mark='a'/> The NICHD protocol, developed by Michael Lamb "
           "and colleagues, builds rapport, practises telling a neutral event in detail, and then invites free "
           "recall: tell me everything that happened. <bookmark mark='b'/> Open prompts, like tell me more about "
           "that, draw longer and more accurate accounts than yes-or-no and option questions. <bookmark mark='c'/> "
           "No repeated questions, no rewards for answers, and no other children told us. The day-care cases' errors "
           "are removed by design. <bookmark mark='d'/> Field studies of trained interviewers found more information "
           "from open prompts, and young children can give reliable accounts when they're asked this way.")
