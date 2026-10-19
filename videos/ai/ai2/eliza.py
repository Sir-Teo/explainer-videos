"""A small ELIZA for Part 2, built the way Weizenbaum's 1966 paper describes it (CACM 9(1), 36-45).

The input is split into words; pronouns are swapped (I <-> YOU, MY <-> YOUR, AM -> ARE ...). The words are scanned
for keywords, each with a rank; a comma, a period or BUT ends the scan once a keyword has been found (and throws away
what came before if none had). The highest-ranked keyword's decomposition patterns are tried in order; the first that
matches picks the next of its reassembly rules, in rotation, and the pieces the pattern matched are spliced in.
Pattern elements: 0 (any number of words), a word, ('*', words) (one of them), ('/', group) (a word of a group, like
FAMILY). A reassembly may also be ('=', key) (use that keyword's rules), ('PRE', words, key) (rewrite the text, then
use key's rules) or ('NEWKEY',) (try the next keyword). The keyword MY also stores a rewritten copy of the sentence in
a memory, first in first out, which ELIZA brings back when nothing in a later input matches.

The script below is our own short DOCTOR-style script, following the rules quoted in the paper; it is not
Weizenbaum's script verbatim.
"""

from __future__ import annotations

import re

SWAP = {"I": "YOU", "ME": "YOU", "MY": "YOUR", "YOU": "I", "YOUR": "MY", "AM": "ARE", "I'M": "YOU'RE",
        "YOU'RE": "I'M", "MYSELF": "YOURSELF", "YOURSELF": "MYSELF", "DONT": "DON'T", "CANT": "CAN'T",
        "WONT": "WON'T", "DREAMT": "DREAMED", "DREAMS": "DREAM", "WERE": "WAS", "MAYBE": "PERHAPS", "HOW": "WHAT",
        "WHEN": "WHAT", "CERTAINLY": "YES", "MACHINE": "COMPUTER", "COMPUTERS": "COMPUTER"}
GROUPS = {"FAMILY": {"MOTHER", "FATHER", "SISTER", "BROTHER", "WIFE", "CHILDREN", "HUSBAND", "MOM", "DAD"},
          "BELIEF": {"FEEL", "THINK", "BELIEVE", "WISH"}}
SAD = ("*", ["SAD", "UNHAPPY", "DEPRESSED", "SICK"])
HAPPY = ("*", ["HAPPY", "ELATED", "GLAD", "BETTER"])
DIT = [([0], [["IN", "WHAT", "WAY"], ["WHAT", "RESEMBLANCE", "DO", "YOU", "SEE"],
              ["WHAT", "DOES", "THAT", "SIMILARITY", "SUGGEST", "TO", "YOU"],
              ["WHAT", "OTHER", "CONNECTIONS", "DO", "YOU", "SEE"],
              ["COULD", "THERE", "REALLY", "BE", "SOME", "CONNECTION"], ["HOW"]])]

# keyword (as typed, before the swap): (rank, rules); a rule is (pattern, [reassembly, ...]) over the swapped words
SCRIPT = {
    "SORRY": (0, [([0], [["PLEASE", "DON'T", "APOLOGIZE"], ["APOLOGIES", "ARE", "NOT", "NECESSARY"],
                         ["WHAT", "FEELINGS", "DO", "YOU", "HAVE", "WHEN", "YOU", "APOLOGIZE"]])]),
    "REMEMBER": (5, [([0, "YOU", "REMEMBER", 0], [["DO", "YOU", "OFTEN", "THINK", "OF", 4],
                                                   ["DOES", "THINKING", "OF", 4, "BRING", "ANYTHING", "ELSE", "TO",
                                                    "MIND"]]),
                     ([0, "DO", "I", "REMEMBER", 0], [["DID", "YOU", "THINK", "I", "WOULD", "FORGET", 5],
                                                       ["WHY", "DO", "YOU", "THINK", "I", "SHOULD", "RECALL", 5,
                                                        "NOW"]]),
                     ([0], [("NEWKEY",)])]),
    "IF": (3, [([0, "IF", 0], [["DO", "YOU", "THINK", "ITS", "LIKELY", "THAT", 3], ["DO", "YOU", "WISH", "THAT", 3],
                                ["WHAT", "DO", "YOU", "THINK", "ABOUT", 3], ["REALLY,", 2, 3]])]),
    "DREAM": (3, [([0], [["WHAT", "DOES", "THAT", "DREAM", "SUGGEST", "TO", "YOU"],
                         ["DO", "YOU", "DREAM", "OFTEN"], ["WHAT", "PERSONS", "APPEAR", "IN", "YOUR", "DREAMS"]])]),
    "PERHAPS": (0, [([0], [["YOU", "DON'T", "SEEM", "QUITE", "CERTAIN"], ["WHY", "THE", "UNCERTAIN", "TONE"],
                           ["CAN'T", "YOU", "BE", "MORE", "POSITIVE"], ["YOU", "AREN'T", "SURE"]])]),
    "HELLO": (0, [([0], [["HOW", "DO", "YOU", "DO.", "PLEASE", "STATE", "YOUR", "PROBLEM"]])]),
    "COMPUTER": (50, [([0], [["DO", "COMPUTERS", "WORRY", "YOU"], ["WHY", "DO", "YOU", "MENTION", "COMPUTERS"],
                             ["WHAT", "DO", "YOU", "THINK", "MACHINES", "HAVE", "TO", "DO", "WITH", "YOUR", "PROBLEM"],
                             ["DON'T", "YOU", "THINK", "COMPUTERS", "CAN", "HELP", "PEOPLE"]])]),
    "AM": (0, [([0, "ARE", "YOU", 0], [["DO", "YOU", "BELIEVE", "YOU", "ARE", 4],
                                       ["WOULD", "YOU", "WANT", "TO", "BE", 4]]),
               ([0], [["WHY", "DO", "YOU", "SAY", "'AM'"], ["I", "DON'T", "UNDERSTAND", "THAT"]])]),
    "ARE": (0, [([0, "ARE", "I", 0], [["WHY", "ARE", "YOU", "INTERESTED", "IN", "WHETHER", "I", "AM", 4, "OR", "NOT"],
                                      ["WOULD", "YOU", "PREFER", "IF", "I", "WEREN'T", 4]]),
                ([0, "ARE", 0], [["DID", "YOU", "THINK", "THEY", "MIGHT", "NOT", "BE", 3],
                                 ["POSSIBLY", "THEY", "ARE", 3]])]),
    "YOUR": (0, [([0, "MY", 0], [["WHY", "ARE", "YOU", "CONCERNED", "OVER", "MY", 3],
                                 ["WHAT", "ABOUT", "YOUR", "OWN", 3]])]),
    "WAS": (2, [([0, "WAS", "YOU", 0], [["WHAT", "IF", "YOU", "WERE", 4], ["DO", "YOU", "THINK", "YOU", "WERE", 4]]),
                ([0], [("NEWKEY",)])]),
    "I'M": (0, [([0, "YOU'RE", 0], [("PRE", ["YOU", "ARE", 3], "I")])]),
    "YOU'RE": (0, [([0, "I'M", 0], [("PRE", ["I", "ARE", 3], "YOU")])]),
    "I": (0, [([0, "YOU", ("*", ["WANT", "NEED"]), 0], [["WHAT", "WOULD", "IT", "MEAN", "TO", "YOU", "IF", "YOU", "GOT",
                                                       4],
                                                      ["WHY", "DO", "YOU", "WANT", 4],
                                                      ["SUPPOSE", "YOU", "GOT", 4, "SOON"]]),
              ([0, "YOU", "ARE", 0, SAD, 0], [["I", "AM", "SORRY", "TO", "HEAR", "YOU", "ARE", 5],
                                              ["DO", "YOU", "THINK", "COMING", "HERE", "WILL", "HELP", "YOU", "NOT",
                                               "TO", "BE", 5],
                                              ["I'M", "SURE", "ITS", "NOT", "PLEASANT", "TO", "BE", 5],
                                              ["CAN", "YOU", "EXPLAIN", "WHAT", "MADE", "YOU", 5]]),
              ([0, "YOU", "ARE", 0, HAPPY, 0], [["HOW", "HAVE", "I", "HELPED", "YOU", "TO", "BE", 5],
                                                ["HAS", "YOUR", "TREATMENT", "MADE", "YOU", 5],
                                                ["WHAT", "MAKES", "YOU", 5, "JUST", "NOW"]]),
              ([0, "YOU", ("/", "BELIEF"), "YOU", 0], [["DO", "YOU", "REALLY", "THINK", "SO"],
                                                     ["BUT", "YOU", "ARE", "NOT", "SURE", "YOU", 5],
                                                     ["DO", "YOU", "REALLY", "DOUBT", "YOU", 5]]),
              ([0, "YOU", 0, ("/", "BELIEF"), 0, "I", 0], [("=", "YOU")]),
              ([0, "YOU", "ARE", 0], [["IS", "IT", "BECAUSE", "YOU", "ARE", 4, "THAT", "YOU", "CAME", "TO", "ME"],
                                      ["HOW", "LONG", "HAVE", "YOU", "BEEN", 4],
                                      ["DO", "YOU", "BELIEVE", "IT", "NORMAL", "TO", "BE", 4],
                                      ["DO", "YOU", "ENJOY", "BEING", 4]]),
              ([0, "YOU", ("*", ["CAN'T", "CANNOT"]), 0], [["HOW", "DO", "YOU", "KNOW", "YOU", "CAN'T", 4],
                                                          ["HAVE", "YOU", "TRIED"],
                                                          ["PERHAPS", "YOU", "COULD", 4, "NOW"]]),
              ([0, "YOU", "DON'T", 0], [["DON'T", "YOU", "REALLY", 4], ["WHY", "DON'T", "YOU", 4],
                                        ["DO", "YOU", "WISH", "TO", "BE", "ABLE", "TO", 4]]),
              ([0, "YOU", "FEEL", 0], [["TELL", "ME", "MORE", "ABOUT", "SUCH", "FEELINGS"],
                                       ["DO", "YOU", "OFTEN", "FEEL", 4], ["DO", "YOU", "ENJOY", "FEELING", 4]]),
              ([0, "YOU", 0, "I", 0], [["PERHAPS", "IN", "YOUR", "FANTASY", "WE", 3, "EACH", "OTHER"],
                                       ["DO", "YOU", "WISH", "TO", 3, "ME"], ["YOU", "SEEM", "TO", "NEED", "TO", 3,
                                                                              "ME"]]),
              ([0], [["YOU", "SAY", 1], ["CAN", "YOU", "ELABORATE", "ON", "THAT"],
                     ["DO", "YOU", "SAY", 1, "FOR", "SOME", "SPECIAL", "REASON"],
                     ["THAT'S", "QUITE", "INTERESTING"]])]),
    "YOU": (0, [([0, "I", "REMIND", "YOU", "OF", 0], [("=", "DIT")]),
                ([0, "I", "ARE", 0], [["WHAT", "MAKES", "YOU", "THINK", "I", "AM", 4],
                                      ["DOES", "IT", "PLEASE", "YOU", "TO", "BELIEVE", "I", "AM", 4],
                                      ["DO", "YOU", "SOMETIMES", "WISH", "YOU", "WERE", 4],
                                      ["PERHAPS", "YOU", "WOULD", "LIKE", "TO", "BE", 4]]),
                ([0, "I", 0, "YOU"], [["WHY", "DO", "YOU", "THINK", "I", 3, "YOU"],
                                      ["YOU", "LIKE", "TO", "THINK", "I", 3, "YOU", "DON'T", "YOU"],
                                      ["WHAT", "MAKES", "YOU", "THINK", "I", 3, "YOU"],
                                      ["REALLY,", "I", 3, "YOU"]]),
                ([0, "I", 0], [["WE", "WERE", "DISCUSSING", "YOU", "NOT", "ME"], ["OH,", "I", 3],
                               ["YOU'RE", "NOT", "REALLY", "TALKING", "ABOUT", "ME", "ARE", "YOU"]])]),
    "YES": (0, [([0], [["YOU", "SEEM", "QUITE", "POSITIVE"], ["YOU", "ARE", "SURE"], ["I", "SEE"],
                       ["I", "UNDERSTAND"]])]),
    "NO": (0, [([0], [["ARE", "YOU", "SAYING", "'NO'", "JUST", "TO", "BE", "NEGATIVE"],
                      ["YOU", "ARE", "BEING", "A", "BIT", "NEGATIVE"], ["WHY", "NOT"], ["WHY", "'NO'"]])]),
    "MY": (2, [([0, "YOUR", 0, ("/", "FAMILY"), 0], [["TELL", "ME", "MORE", "ABOUT", "YOUR", "FAMILY"],
                                                    ["WHO", "ELSE", "IN", "YOUR", "FAMILY", 5],
                                                    ["YOUR", 4],
                                                    ["WHAT", "ELSE", "COMES", "TO", "MIND", "WHEN", "YOU", "THINK", "OF",
                                                     "YOUR", 4]]),
               ([0, "YOUR", 0], [["YOUR", 3], ["WHY", "DO", "YOU", "SAY", "YOUR", 3],
                                 ["DOES", "THAT", "SUGGEST", "ANYTHING", "ELSE", "WHICH", "BELONGS", "TO", "YOU"],
                                 ["IS", "IT", "IMPORTANT", "TO", "YOU", "THAT", 2, 3]])]),
    "CAN": (0, [([0, "CAN", "I", 0], [["YOU", "BELIEVE", "I", "CAN", 4, "DON'T", "YOU"], ("=", "WHAT"),
                                      ["YOU", "WANT", "ME", "TO", "BE", "ABLE", "TO", 4]]),
                ([0, "CAN", "YOU", 0], [["WHETHER", "OR", "NOT", "YOU", "CAN", 4, "DEPENDS", "ON", "YOU", "MORE",
                                         "THAN", "ON", "ME"], ["DO", "YOU", "WANT", "TO", "BE", "ABLE", "TO", 4],
                                        ["PERHAPS", "YOU", "DON'T", "WANT", "TO", 4]]),
                ([0], [("=", "WHAT")])]),
    "WHAT": (0, [([0], [["WHY", "DO", "YOU", "ASK"], ["DOES", "THAT", "QUESTION", "INTEREST", "YOU"],
                        ["WHAT", "IS", "IT", "YOU", "REALLY", "WANT", "TO", "KNOW"],
                        ["ARE", "SUCH", "QUESTIONS", "MUCH", "ON", "YOUR", "MIND"],
                        ["WHAT", "ANSWER", "WOULD", "PLEASE", "YOU", "MOST"], ["WHAT", "DO", "YOU", "THINK"],
                        ["WHAT", "COMES", "TO", "YOUR", "MIND", "WHEN", "YOU", "ASK", "THAT"],
                        ["HAVE", "YOU", "ASKED", "SUCH", "QUESTION", "BEFORE"],
                        ["HAVE", "YOU", "ASKED", "ANYONE", "ELSE"]])]),
    "BECAUSE": (0, [([0], [["IS", "THAT", "THE", "REAL", "REASON"], ["DON'T", "ANY", "OTHER", "REASONS", "COME", "TO",
                                                                     "MIND"],
                           ["DOES", "THAT", "REASON", "SEEM", "TO", "EXPLAIN", "ANYTHING", "ELSE"],
                           ["WHAT", "OTHER", "REASONS", "MIGHT", "THERE", "BE"]])]),
    "WHY": (0, [([0, "WHY", "DON'T", "I", 0], [["DO", "YOU", "BELIEVE", "I", "DON'T", 5],
                                               ["PERHAPS", "I", "WILL", 5, "IN", "GOOD", "TIME"],
                                               ["SHOULD", "YOU", 5, "YOURSELF"], ["YOU", "WANT", "ME", "TO", 5]]),
                ([0, "WHY", "CAN'T", "YOU", 0], [["DO", "YOU", "THINK", "YOU", "SHOULD", "BE", "ABLE", "TO", 5],
                                                 ["DO", "YOU", "WANT", "TO", "BE", "ABLE", "TO", 5],
                                                 ["DO", "YOU", "BELIEVE", "THIS", "WILL", "HELP", "YOU", "TO", 5]]),
                ([0], [("=", "WHAT")])]),
    "EVERYONE": (2, [([0, ("*", ["EVERYONE", "EVERYBODY", "NOBODY", "NOONE"]), 0],
                      [["REALLY,", 2], ["SURELY", "NOT", 2], ["CAN", "YOU", "THINK", "OF", "ANYONE", "IN", "PARTICULAR"],
                       ["WHO,", "FOR", "EXAMPLE"], ["YOU", "ARE", "THINKING", "OF", "A", "VERY", "SPECIAL", "PERSON"]])]),
    "ALWAYS": (1, [([0], [["CAN", "YOU", "THINK", "OF", "A", "SPECIFIC", "EXAMPLE"], ["WHEN"],
                          ["WHAT", "INCIDENT", "ARE", "YOU", "THINKING", "OF"], ["REALLY,", "ALWAYS"]])]),
    "LIKE": (10, [([0, ("*", ["AM", "IS", "ARE", "WAS"]), 0, "LIKE", 0], [("=", "DIT")]), ([0], [("NEWKEY",)])]),
    "ALIKE": (10, [([0], [("=", "DIT")])]),
    "SAME": (10, [([0], [("=", "DIT")])]),
}
for k, a in (("DREAMT", "DREAM"), ("DREAMS", "DREAM"), ("MAYBE", "PERHAPS"), ("HOW", "WHAT"), ("WHEN", "WHAT"),
             ("CERTAINLY", "YES"), ("MACHINE", "COMPUTER"), ("COMPUTERS", "COMPUTER"), ("ME", "I"),
             ("EVERYBODY", "EVERYONE"), ("NOBODY", "EVERYONE"), ("NOONE", "EVERYONE"), ("WERE", "WAS")):
    SCRIPT[k] = SCRIPT[a]
LINKS = {"DIT": DIT}
MEMORY = [["LETS", "DISCUSS", "FURTHER", "WHY", "YOUR", 3], ["EARLIER", "YOU", "SAID", "YOUR", 3],
          ["BUT", "YOUR", 3], ["DOES", "THAT", "HAVE", "ANYTHING", "TO", "DO", "WITH", "THE", "FACT", "THAT", "YOUR", 3]]
NONE = [["I", "AM", "NOT", "SURE", "I", "UNDERSTAND", "YOU", "FULLY"], ["PLEASE", "GO", "ON"],
        ["WHAT", "DOES", "THAT", "SUGGEST", "TO", "YOU"],
        ["DO", "YOU", "FEEL", "STRONGLY", "ABOUT", "DISCUSSING", "SUCH", "THINGS"]]


def _match(pat, words):
    """Match a decomposition pattern; returns the list of matched pieces (each a list of words) or None."""
    def go(pi, wi):
        if pi == len(pat):
            return [] if wi == len(words) else None
        p = pat[pi]
        if p == 0:
            for k in range(wi, len(words) + 1):
                rest = go(pi + 1, k)
                if rest is not None:
                    return [words[wi:k]] + rest
            return None
        if wi == len(words):
            return None
        w = words[wi]
        ok = (w == p) if isinstance(p, str) else (w in p[1]) if p[0] == "*" else (w in GROUPS[p[1]])
        if not ok:
            return None
        rest = go(pi + 1, wi + 1)
        return None if rest is None else [[w]] + rest
    return go(0, 0)


class Eliza:
    def __init__(self):
        self.turn = {}  # (rules id, rule index) -> how many times used: reassemblies rotate
        self.memory: list[list[str]] = []

    def _rules(self, key):
        if key in LINKS:
            return LINKS[key]
        return SCRIPT[key][1]

    def _apply(self, key, words, depth=0):
        rules = self._rules(key)
        for ri, (pat, reasm) in enumerate(rules):
            parts = _match(pat, words)
            if parts is None:
                continue
            tid = (id(rules), ri)
            k = self.turn.get(tid, 0)
            self.turn[tid] = k + 1
            r = reasm[k % len(reasm)]
            if isinstance(r, tuple):
                if r[0] == "=":
                    return self._apply(r[1], words, depth + 1) if depth < 5 else None
                if r[0] == "NEWKEY":
                    return None
                if r[0] == "PRE":
                    new = self._assemble(r[1], parts)
                    return self._apply(r[2], new, depth + 1) if depth < 5 else None
            return self._assemble(r, parts)
        return None

    @staticmethod
    def _assemble(r, parts):
        out = []
        for t in r:
            out += parts[t - 1] if isinstance(t, int) else [t]
        return out

    def respond(self, text: str) -> str:
        raw = re.sub(r"[?!;:]", "", text.upper())
        tokens = re.findall(r"[A-Z']+|[,.]", raw)
        keys, words = [], []
        for t in tokens:
            if t in (",", ".") or t == "BUT":
                if keys:
                    break
                words = []
                continue
            if t in SCRIPT:
                rank = SCRIPT[t][0]
                keys.append((rank, len(keys), t))
            words.append(SWAP.get(t, t))
        keys.sort(key=lambda x: (-x[0], x[1]))
        if keys and keys[0][2] == "MY":  # remember this sentence for later
            parts = _match([0, "YOUR", 0], words)
            if parts is not None:
                form = MEMORY[len(self.memory) % len(MEMORY)]
                self.memory.append(self._assemble(form, parts))
        for _, _, k in keys:
            out = self._apply(k, words)
            if out is not None:
                return " ".join(out)
        if self.memory:
            return " ".join(self.memory.pop(0))
        k = self.turn.get("none", 0)
        self.turn["none"] = k + 1
        return " ".join(NONE[k % len(NONE)])


# The user's side of the conversation printed in Weizenbaum (1966), and ELIZA's replies there.
WEIZENBAUM_1966 = [
    ("Men are all alike.", "IN WHAT WAY"),
    ("They're always bugging us about something or other.", "CAN YOU THINK OF A SPECIFIC EXAMPLE"),
    ("Well, my boyfriend made me come here.", "YOUR BOYFRIEND MADE YOU COME HERE"),
    ("He says I'm depressed much of the time.", "I AM SORRY TO HEAR YOU ARE DEPRESSED"),
    ("It's true. I am unhappy.", "DO YOU THINK COMING HERE WILL HELP YOU NOT TO BE UNHAPPY"),
    ("I need some help, that much seems certain.", "WHAT WOULD IT MEAN TO YOU IF YOU GOT SOME HELP"),
    ("Perhaps I could learn to get along with my mother.", "TELL ME MORE ABOUT YOUR FAMILY"),
    ("My mother takes care of me.", "WHO ELSE IN YOUR FAMILY TAKES CARE OF YOU"),
    ("My father.", "YOUR FATHER"),
    ("You are like my father in some ways.", "WHAT RESEMBLANCE DO YOU SEE"),
    ("You are not very aggressive but I think you don't want me to notice that.",
     "WHAT MAKES YOU THINK I AM NOT VERY AGGRESSIVE"),
    ("You don't argue with me.", "WHY DO YOU THINK I DON'T ARGUE WITH YOU"),
    ("You are afraid of me.", "DOES IT PLEASE YOU TO BELIEVE I AM AFRAID OF YOU"),
    ("My father is afraid of everybody.", "WHAT ELSE COMES TO MIND WHEN YOU THINK OF YOUR FATHER"),
    ("Bullies.", "DOES THAT HAVE ANYTHING TO DO WITH THE FACT THAT YOUR BOYFRIEND MADE YOU COME HERE"),
]
