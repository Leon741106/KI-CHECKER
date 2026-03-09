import re
import math
import tkinter as tk
from tkinter import scrolledtext

LANGUAGE_PROFILES = {
    "English": {
        "ai_signature_words": {
            "delve", "delves", "delved", "delving",
            "crucial", "pivotal", "paramount", "imperative",
            "multifaceted", "multidimensional", "nuanced", "nuance",
            "comprehensive", "holistic", "robust", "leveraging", "leverage",
            "streamline", "streamlined", "streamlining",
            "facilitate", "facilitates", "facilitated", "facilitating",
            "utilize", "utilizes", "utilized", "utilizing",
            "endeavor", "endeavors", "endeavored", "endeavoring",
            "mitigate", "mitigates", "mitigated", "mitigating",
            "underscore", "underscores", "underscored", "underscoring",
            "emphasize", "emphasizes", "emphasized", "emphasizing",
            "elucidate", "elucidates", "elucidated", "elucidating",
            "pertaining", "pertain", "pertains", "aforementioned",
            "synergy", "synergies", "synergistic",
            "proactive", "actionable", "scalable", "impactful",
            "transformative", "groundbreaking", "innovative",
            "foundational", "cornerstone", "paradigm", "paradigms",
            "intersection", "interplay", "dynamics",
            "navigate", "navigates", "navigated", "navigating",
            "foster", "fosters", "fostered", "fostering",
            "cultivate", "cultivates", "cultivated", "cultivating",
            "harness", "harnessing", "harnessed",
            "tapestry", "landscape", "ecosystem",
            "realm", "realms", "domain", "domains",
            "intricate", "intricately", "intrinsic", "inherently",
            "notably", "importantly", "significantly",
            "ultimately", "fundamentally", "essentially",
            "accordingly", "subsequently", "consequently",
            "nevertheless", "nonetheless", "notwithstanding",
            "heretofore", "hitherto", "thereby", "therein", "thereof",
            "whilst", "amidst",
        },
        "ai_filler_phrases": [
            "it is important to note", "it's important to note",
            "it is worth noting", "it's worth noting",
            "it is crucial to", "it's crucial to",
            "it is essential to", "it's essential to",
            "needless to say", "it goes without saying",
            "as previously mentioned", "as mentioned earlier", "as noted above",
            "in conclusion", "in summary", "to summarize", "to conclude",
            "in the realm of", "in the context of",
            "it is worth mentioning", "one must consider",
            "we can see that", "it can be argued", "it should be noted",
            "as an ai language model", "as a large language model",
            "i hope this helps", "feel free to ask", "let me know if",
            "certainly, here", "of course, here", "absolutely, here", "sure, here",
            "great question", "excellent question", "that's a great",
            "a comprehensive overview", "a detailed explanation", "a wide range of",
            "plays a crucial role", "plays a vital role",
            "plays a key role", "plays an important role",
        ],
        "ai_opener_patterns": [
            r"^certainly[,!]", r"^absolutely[,!]", r"^of course[,!]",
            r"^sure[,!]", r"^great[,!]",
            r"^thank you for", r"^thanks for",
            r"^i('d| would) be happy to", r"^i('d| would) be glad to",
            r"^i('ll| will) help",
            r"^let('s| us) (explore|dive|look|start|begin|consider|examine)",
            r"^when (it comes to|considering|thinking about)",
            r"^in today's (world|society|age|era|landscape|digital)",
            r"^in the (modern|contemporary|current) (world|era|age|landscape)",
        ],
        "human_slang_words": {
            "gonna", "wanna", "gotta", "kinda", "sorta", "dunno", "lemme",
            "gimme", "ain't", "y'all", "nope", "yep", "yeah", "nah", "yup",
            "btw", "tbh", "imo", "imho", "lol", "lmao", "omg", "wtf", "smh",
            "bruh", "dude", "ugh", "hmm", "huh", "whoops", "oops", "oof", "meh",
        },
        "human_hedging_phrases": [
            "i think", "i believe", "i feel", "i guess", "i suppose",
            "maybe", "perhaps", "probably", "might be", "could be",
            "not sure", "not certain", "honestly", "to be honest",
            "to be fair", "kind of", "sort of", "a bit", "a little",
        ],
        "formal_connector_words": [
            "furthermore", "moreover", "additionally", "in addition",
            "however", "therefore", "thus", "hence", "accordingly",
            "consequently", "subsequently", "in contrast", "on the other hand",
            "on the contrary", "in spite of", "despite", "although",
            "nevertheless", "nonetheless", "notwithstanding",
            "in particular", "specifically", "notably",
            "for instance", "for example", "such as",
            "in conclusion", "to summarize", "in summary",
        ],
        "passive_voice_patterns": [
            r'\b(is|are|was|were|be|been|being)\s+(being\s+)?\w+ed\b',
            r'\b(has|have|had)\s+been\s+\w+ed\b',
        ],
        "hedged_claim_patterns": [
            r'\bit\s+(can|could|may|might|should|would)\s+be\b',
            r'\bone\s+(can|could|may|might|should|would)\b',
            r'\bthis\s+(can|could|may|might|should|would)\b',
        ],
    },
    "Deutsch": {
        "ai_signature_words": {
            "hervorzuheben", "herauszustellen", "hervorzuheben",
            "entscheidend", "maßgeblich", "ausschlaggebend", "grundlegend",
            "vielschichtig", "facettenreich", "nuanciert", "komplex",
            "umfassend", "ganzheitlich", "robust", "nachhaltig",
            "optimieren", "optimiert", "optimierung",
            "erleichtern", "ermöglichen", "begünstigen", "fördern",
            "nutzen", "nutzbarmachen", "einsetzen", "verwenden",
            "bemühen", "bestreben", "anstreben",
            "abmildern", "minimieren", "reduzieren", "eindämmen",
            "unterstreichen", "betonen", "hervorheben", "verdeutlichen",
            "veranschaulichen", "darlegen", "erläutern", "erklären",
            "betreffend", "bezüglich", "hinsichtlich", "diesbezüglich",
            "aforementioned", "obengenannt", "obenerwähnt",
            "synergie", "synergien", "synergistisch",
            "proaktiv", "umsetzbar", "skalierbar", "wirkungsvoll",
            "transformativ", "wegweisend", "innovativ",
            "grundlegend", "eckpfeiler", "paradigma", "paradigmen",
            "schnittstelle", "zusammenspiel", "dynamik",
            "navigieren", "steuern", "lenken",
            "fördern", "kultivieren", "pflegen",
            "nutzen", "einsetzen", "erschließen",
            "geflecht", "landschaft", "ökosystem",
            "bereich", "bereiche", "domäne", "domänen",
            "vielschichtig", "tiefgründig", "inhärent", "wesenhaft",
            "bemerkenswert", "wichtig", "bedeutsam",
            "letztendlich", "grundlegend", "im wesentlichen",
            "entsprechend", "anschließend", "infolgedessen",
            "nichtsdestotrotz", "dennoch", "gleichwohl",
            "hierdurch", "hierin", "hiervon", "dadurch",
            "wobei", "inmitten", "währenddessen",
        },
        "ai_filler_phrases": [
            "es ist wichtig zu beachten", "es ist wichtig anzumerken",
            "es ist erwähnenswert", "es sei darauf hingewiesen",
            "es ist entscheidend", "es ist wesentlich",
            "es ist unerlässlich", "es versteht sich von selbst",
            "wie bereits erwähnt", "wie zuvor erwähnt", "wie oben genannt",
            "abschließend lässt sich sagen", "zusammenfassend",
            "um es zusammenzufassen", "zum abschluss",
            "im bereich von", "im kontext von",
            "man muss berücksichtigen", "wir können sehen dass",
            "es kann argumentiert werden", "es sollte beachtet werden",
            "als ki-sprachmodell", "als großes sprachmodell",
            "ich hoffe das hilft", "fühlen sie sich frei",
            "lassen sie mich wissen",
            "natürlich, hier", "selbstverständlich, hier",
            "gute frage", "ausgezeichnete frage",
            "ein umfassender überblick", "eine detaillierte erklärung",
            "eine breite palette von", "spielt eine entscheidende rolle",
            "spielt eine wichtige rolle", "spielt eine zentrale rolle",
        ],
        "ai_opener_patterns": [
            r"^natürlich[,!]", r"^selbstverständlich[,!]",
            r"^sicher[,!]", r"^gerne[,!]",
            r"^vielen dank für", r"^danke für",
            r"^ich (würde|helfe) (gerne|ihnen)",
            r"^lass(en sie)? (uns)? (erkunden|eintauchen|beginnen|betrachten)",
            r"^wenn es (darum geht|um)",
            r"^in der heutigen (welt|gesellschaft|zeit|ära|digitalen)",
            r"^in der (modernen|zeitgenössischen|aktuellen) (welt|ära|zeit)",
        ],
        "human_slang_words": {
            "krass", "alter", "digga", "bruder", "bro", "ne", "nö", "jo",
            "joa", "naja", "echt", "halt", "mal", "irgendwie", "sozusagen",
            "quasi", "btw", "tbh", "lol", "omg", "wtf", "imo", "aka",
            "absolut", "genau", "klar", "stimmt", "achso", "ach so",
            "hm", "hmm", "äh", "ähm", "tja", "nee",
        },
        "human_hedging_phrases": [
            "ich denke", "ich glaube", "ich finde", "ich schätze",
            "ich vermute", "vielleicht", "wahrscheinlich", "könnte sein",
            "nicht sicher", "ehrlich gesagt", "um ehrlich zu sein",
            "irgendwie", "ein bisschen", "ein wenig", "quasi", "sozusagen",
        ],
        "formal_connector_words": [
            "außerdem", "darüber hinaus", "zusätzlich", "des weiteren",
            "jedoch", "daher", "deshalb", "folglich", "infolgedessen",
            "dennoch", "gleichwohl", "nichtsdestotrotz",
            "im gegensatz dazu", "andererseits", "auf der anderen seite",
            "insbesondere", "vor allem", "nämlich", "zwar",
            "zum beispiel", "beispielsweise", "wie etwa",
            "abschließend", "zusammenfassend", "insgesamt",
        ],
        "passive_voice_patterns": [
            r'\b(wird|werden|wurde|wurden|worden)\s+\w+\b',
            r'\b(ist|sind|war|waren)\s+\w+(t|en)\b',
        ],
        "hedged_claim_patterns": [
            r'\bes\s+(kann|könnte|darf|mag|sollte|würde)\s+\w+\b',
            r'\bman\s+(kann|könnte|darf|mag|sollte|würde)\b',
            r'\bdies\s+(kann|könnte|darf|mag|sollte|würde)\b',
        ],
    },
}

PLACEHOLDER_TEXT = "Text hier einfügen oder eintippen..."

COLOR_BG     = "#0f0f0f"
COLOR_PANEL  = "#1a1a1a"
COLOR_BORDER = "#2a2a2a"
COLOR_TEXT   = "#f0f0f0"
COLOR_MUTED  = "#888888"
COLOR_ACCENT = "#00d4aa"
COLOR_ERROR  = "#e74c3c"


def get_tokens(text):
    return re.findall(r"\b[a-zA-ZäöüÄÖÜß']+\b", text.lower())

def get_sentences(text):
    parts = re.split(r'(?<=[.!?])\s+', text.strip())
    return [s.strip() for s in parts if len(s.strip()) > 3]

def get_words(text):
    return re.findall(r"\b\w+\b", text)


def check_ai_vocabulary(tokens, profile):
    matched_words = [t for t in tokens if t in profile["ai_signature_words"]]
    hit_rate = len(matched_words) / max(len(tokens), 1) * 100
    points = min(25, hit_rate * 5)
    unique_matches = list(set(matched_words))[:8]
    return points, len(matched_words), unique_matches

def check_filler_phrases(text, profile):
    lowered = text.lower()
    found = [phrase for phrase in profile["ai_filler_phrases"] if phrase in lowered]
    points = min(20, len(found) * 4)
    return points, len(found), found[:5]

def check_ai_openers(text, profile):
    opening_text = text[:500].lower()
    hit_count = sum(1 for pattern in profile["ai_opener_patterns"] if re.search(pattern, opening_text))
    points = min(10, hit_count * 5)
    return points, hit_count

def check_formal_connectors(tokens, profile):
    joined = " ".join(tokens)
    hit_count = sum(1 for connector in profile["formal_connector_words"] if connector in joined)
    density = hit_count / max(len(tokens) / 100, 1)
    points = min(10, density * 2)
    return points, hit_count

def check_passive_voice(text, profile):
    hit_count = sum(len(re.findall(p, text.lower())) for p in profile["passive_voice_patterns"])
    sentence_count = len(get_sentences(text))
    ratio = hit_count / max(sentence_count, 1)
    points = min(10, ratio * 20)
    return points, hit_count

def check_hedged_claims(text, profile):
    hit_count = sum(len(re.findall(p, text.lower())) for p in profile["hedged_claim_patterns"])
    sentence_count = len(get_sentences(text))
    ratio = hit_count / max(sentence_count, 1)
    points = min(8, ratio * 16)
    return points, hit_count

def check_sentence_uniformity(text):
    sentences = get_sentences(text)
    if len(sentences) < 3:
        return 0, 0
    lengths = [len(get_words(s)) for s in sentences]
    mean_length = sum(lengths) / len(lengths)
    std_dev = math.sqrt(sum((x - mean_length) ** 2 for x in lengths) / len(lengths))
    variation = std_dev / mean_length if mean_length else 1
    uniformity = max(0, 1 - variation)
    points = min(10, uniformity * 12)
    return points, round(std_dev, 1)

def check_lexical_diversity(tokens):
    if len(tokens) < 10:
        return 0, 1.0
    type_token_ratio = len(set(tokens)) / len(tokens)
    if type_token_ratio < 0.45:
        points = 8
    elif type_token_ratio < 0.55:
        points = 4
    else:
        points = 0
    return points, round(type_token_ratio, 3)

def check_human_signals(text, tokens, profile):
    token_set = set(tokens)
    slang_count = sum(1 for word in profile["human_slang_words"] if word in token_set)
    hedge_count = sum(1 for phrase in profile["human_hedging_phrases"] if phrase in text.lower())
    exclamation_count = len(re.findall(r'[!?]{2,}', text))
    ellipsis_count = len(re.findall(r'\.{3,}', text))
    personal_pronoun_count = len(re.findall(r'\b(i|ich)\b', text.lower()))
    total_human_points = slang_count * 3 + hedge_count * 2 + exclamation_count + ellipsis_count + min(personal_pronoun_count, 5)
    return total_human_points, slang_count, hedge_count

def check_markdown_structure(text):
    bullet_count = len(re.findall(r'^\s*[-*•]\s+\S', text, re.MULTILINE))
    numbered_count = len(re.findall(r'^\s*\d+[.)]\s+\S', text, re.MULTILINE))
    header_count = len(re.findall(r'^#{1,3}\s+\S', text, re.MULTILINE))
    bold_count = len(re.findall(r'\*\*[^*]+\*\*', text))
    total_structure = bullet_count + numbered_count + header_count * 2 + bold_count
    points = min(7, total_structure)
    return points, bullet_count + numbered_count, header_count, bold_count


def analyze(text, language):
    profile = LANGUAGE_PROFILES[language]
    tokens = get_tokens(text)
    word_count = len(tokens)

    if word_count < 20:
        return None, "Text zu kurz (mindestens 20 Wörter erforderlich)." if language == "Deutsch" else "Text too short (minimum 20 words required)."

    vocab_points,     vocab_hit_count,   vocab_matched_words = check_ai_vocabulary(tokens, profile)
    filler_points,    filler_hit_count,  filler_found        = check_filler_phrases(text, profile)
    opener_points,    opener_hit_count                       = check_ai_openers(text, profile)
    connector_points, connector_hit_count                    = check_formal_connectors(tokens, profile)
    passive_points,   passive_hit_count                      = check_passive_voice(text, profile)
    hedged_points,    hedged_hit_count                       = check_hedged_claims(text, profile)
    uniform_points,   sentence_std_dev                       = check_sentence_uniformity(text)
    diversity_points, type_token_ratio                       = check_lexical_diversity(tokens)
    human_points,     slang_count,        hedge_count        = check_human_signals(text, tokens, profile)
    struct_points,    bullet_count,       header_count, bold_count = check_markdown_structure(text)

    total_ai_points = (
        vocab_points + filler_points + opener_points +
        connector_points + passive_points + hedged_points +
        uniform_points + diversity_points + struct_points
    )

    human_reduction = min(30, human_points * 3)
    final_score = max(1, min(100, int(total_ai_points - human_reduction)))

    details = {
        "Word count":           word_count,
        "AI vocab hits":        f"{vocab_hit_count}  ({', '.join(vocab_matched_words) if vocab_matched_words else '—'})",
        "Filler phrases":       f"{filler_hit_count}  ({filler_found[0] if filler_found else '—'})",
        "AI opener detected":   "Yes" if opener_hit_count else "No",
        "Formal connectors":    connector_hit_count,
        "Passive constructs":   passive_hit_count,
        "Hedged claims":        hedged_hit_count,
        "Sentence uniformity":  f"std={sentence_std_dev}",
        "Lexical diversity":    f"TTR={type_token_ratio}",
        "Human signals":        f"slang={slang_count}  hedges={hedge_count}",
        "Markdown structure":   f"bullets={bullet_count}  headers={header_count}  bold={bold_count}",
        "Sub-scores":           f"{int(total_ai_points)} AI  −{human_reduction} human",
    }

    return final_score, details


def get_verdict(score):
    if score >= 80:
        return "Almost certainly AI-generated", "#e74c3c"
    elif score >= 60:
        return "Very likely AI-generated", "#e67e22"
    elif score >= 40:
        return "Possibly AI-generated", "#f1c40f"
    elif score >= 20:
        return "Possibly human-written", "#3498db"
    else:
        return "Very likely human-written", "#2ecc71"


class AIDetectorApp:

    def __init__(self, root):
        self.root = root
        self.root.title("AI Text Detector  v1.0")
        self.root.configure(bg=COLOR_BG)
        self.root.geometry("820x800")
        self.root.resizable(True, True)
        self.placeholder_active = True
        self.selected_language = tk.StringVar(value="")
        self._build_ui()

    def _build_ui(self):
        title_row = tk.Frame(self.root, bg=COLOR_BG)
        title_row.pack(fill="x", padx=28, pady=(22, 2))

        tk.Label(title_row, text="AI TEXT DETECTOR", bg=COLOR_BG, fg=COLOR_TEXT,
                 font=("Courier New", 20, "bold")).pack(side="left")
        tk.Label(title_row, text="v1.0  |  linguistic analysis", bg=COLOR_BG, fg=COLOR_MUTED,
                 font=("Courier New", 9)).pack(side="left", padx=(10, 0), pady=(7, 0))

        lang_row = tk.Frame(self.root, bg=COLOR_BG)
        lang_row.pack(fill="x", padx=28, pady=(10, 4))

        tk.Label(lang_row, text="SELECT TEXT LANGUAGE", bg=COLOR_BG, fg=COLOR_MUTED,
                 font=("Courier New", 8)).pack(anchor="w", pady=(0, 6))

        btn_frame = tk.Frame(lang_row, bg=COLOR_BG)
        btn_frame.pack(anchor="w")

        self.lang_buttons = {}
        for lang in LANGUAGE_PROFILES:
            btn = tk.Button(
                btn_frame, text=lang,
                command=lambda l=lang: self._select_language(l),
                bg=COLOR_PANEL, fg=COLOR_MUTED,
                activebackground=COLOR_ACCENT, activeforeground="#0f0f0f",
                font=("Courier New", 11), relief="flat",
                padx=20, pady=7, cursor="hand2",
            )
            btn.pack(side="left", padx=(0, 8))
            self.lang_buttons[lang] = btn

        self.lang_warning = tk.Label(self.root, text="⚠  Please select a language first.",
                                     bg=COLOR_BG, fg=COLOR_ERROR, font=("Courier New", 9))
        self.lang_warning.pack(anchor="w", padx=28, pady=(0, 4))
        self.lang_warning.pack_forget()

        input_border = tk.Frame(self.root, bg=COLOR_BORDER, padx=1, pady=1)
        input_border.pack(fill="both", expand=True, padx=28, pady=(4, 0))

        self.text_box = scrolledtext.ScrolledText(
            input_border, wrap=tk.WORD,
            bg=COLOR_PANEL, fg=COLOR_MUTED,
            insertbackground=COLOR_ACCENT,
            font=("Courier New", 11),
            relief="flat", padx=12, pady=12, bd=0,
        )
        self.text_box.pack(fill="both", expand=True)
        self.text_box.insert("1.0", PLACEHOLDER_TEXT)
        self.text_box.bind("<FocusIn>",  self._on_focus_in)
        self.text_box.bind("<FocusOut>", self._on_focus_out)
        self.text_box.bind("<<Paste>>",  self._on_paste)
        self.text_box.bind("<Key>",      self._on_key_press)

        btn_row = tk.Frame(self.root, bg=COLOR_BG)
        btn_row.pack(fill="x", padx=28, pady=8)

        tk.Button(btn_row, text="▶  ANALYZE", command=self._run_analysis,
                  bg=COLOR_ACCENT, fg="#0f0f0f", activebackground="#00b894",
                  activeforeground="#0f0f0f", font=("Courier New", 11, "bold"),
                  relief="flat", padx=20, pady=7, cursor="hand2",
                  ).pack(side="left")

        tk.Button(btn_row, text="✕  CLEAR", command=self._clear_all,
                  bg=COLOR_PANEL, fg=COLOR_MUTED, activebackground=COLOR_BORDER,
                  activeforeground=COLOR_TEXT, font=("Courier New", 11),
                  relief="flat", padx=16, pady=7, cursor="hand2",
                  ).pack(side="left", padx=(8, 0))

        score_panel = tk.Frame(self.root, bg=COLOR_PANEL, padx=20, pady=14)
        score_panel.pack(fill="x", padx=28, pady=(0, 6))

        score_left = tk.Frame(score_panel, bg=COLOR_PANEL)
        score_left.pack(side="left", fill="y", padx=(0, 22))

        self.score_label = tk.Label(score_left, text="--", bg=COLOR_PANEL,
                                    fg=COLOR_ACCENT, font=("Courier New", 52, "bold"))
        self.score_label.pack()
        tk.Label(score_left, text="/ 100", bg=COLOR_PANEL, fg=COLOR_MUTED,
                 font=("Courier New", 10)).pack()

        score_right = tk.Frame(score_panel, bg=COLOR_PANEL)
        score_right.pack(side="left", fill="both", expand=True)

        self.verdict_label = tk.Label(score_right, text="Awaiting analysis...",
                                      bg=COLOR_PANEL, fg=COLOR_MUTED,
                                      font=("Courier New", 13, "bold"), anchor="w")
        self.verdict_label.pack(anchor="w", pady=(10, 6))

        progress_track = tk.Frame(score_right, bg=COLOR_BORDER, height=7)
        progress_track.pack(fill="x")
        progress_track.pack_propagate(False)
        self.progress_bar = tk.Frame(progress_track, bg=COLOR_ACCENT, height=7)
        self.progress_bar.place(x=0, y=0, relheight=1, relwidth=0)

        detail_grid = tk.Frame(self.root, bg=COLOR_PANEL)
        detail_grid.pack(fill="x", padx=28, pady=(0, 6))

        self.detail_value_vars = {}
        detail_labels = [
            "Word count",        "AI vocab hits",       "Filler phrases",
            "AI opener detected","Formal connectors",   "Passive constructs",
            "Hedged claims",     "Sentence uniformity", "Lexical diversity",
            "Human signals",     "Markdown structure",  "Sub-scores",
        ]

        columns = 3
        for index, label in enumerate(detail_labels):
            cell = tk.Frame(detail_grid, bg=COLOR_PANEL, padx=10, pady=6)
            cell.grid(row=index // columns, column=index % columns, sticky="ew", padx=2, pady=2)
            detail_grid.columnconfigure(index % columns, weight=1)

            tk.Label(cell, text=label.upper(), bg=COLOR_PANEL, fg=COLOR_MUTED,
                     font=("Courier New", 7)).pack(anchor="w")

            value_var = tk.StringVar(value="—")
            self.detail_value_vars[label] = value_var
            tk.Label(cell, textvariable=value_var, bg=COLOR_PANEL, fg=COLOR_TEXT,
                     font=("Courier New", 11, "bold"), wraplength=220, justify="left",
                     ).pack(anchor="w")

        self.error_label = tk.Label(self.root, text="", bg=COLOR_BG, fg=COLOR_ERROR,
                                    font=("Courier New", 10))
        self.error_label.pack(pady=(0, 8))

    def _select_language(self, language):
        self.selected_language.set(language)
        self.lang_warning.pack_forget()
        for lang, btn in self.lang_buttons.items():
            if lang == language:
                btn.config(bg=COLOR_ACCENT, fg="#0f0f0f")
            else:
                btn.config(bg=COLOR_PANEL, fg=COLOR_MUTED)

    def _on_focus_in(self, event=None):
        if self.placeholder_active:
            self.text_box.delete("1.0", "end")
            self.text_box.config(fg=COLOR_TEXT)
            self.placeholder_active = False

    def _on_focus_out(self, event=None):
        if not self.text_box.get("1.0", "end-1c").strip():
            self.text_box.insert("1.0", PLACEHOLDER_TEXT)
            self.text_box.config(fg=COLOR_MUTED)
            self.placeholder_active = True

    def _on_paste(self, event=None):
        self.placeholder_active = False
        self.root.after(1, lambda: self.text_box.config(fg=COLOR_TEXT))

    def _on_key_press(self, event=None):
        pass

    def _clear_all(self):
        self.text_box.delete("1.0", "end")
        self.text_box.config(fg=COLOR_TEXT)
        self.placeholder_active = False
        self.score_label.config(text="--", fg=COLOR_ACCENT)
        self.verdict_label.config(text="Awaiting analysis...", fg=COLOR_MUTED)
        self.progress_bar.place(relwidth=0)
        self.error_label.config(text="")
        for value_var in self.detail_value_vars.values():
            value_var.set("—")

    def _run_analysis(self):
        if not self.selected_language.get():
            self.lang_warning.pack(anchor="w", padx=28, pady=(0, 4))
            return

        input_text = self.text_box.get("1.0", "end-1c").strip()

        if not input_text or self.placeholder_active:
            self.error_label.config(text="⚠  Please enter some text first.")
            return

        self.error_label.config(text="")
        score, details = analyze(input_text, self.selected_language.get())

        if score is None:
            self.error_label.config(text=f"⚠  {details}")
            return

        verdict_text, verdict_color = get_verdict(score)

        self.score_label.config(text=str(score), fg=verdict_color)
        self.verdict_label.config(text=verdict_text, fg=verdict_color)
        self.progress_bar.config(bg=verdict_color)
        self.progress_bar.place(relwidth=score / 100)

        for label, value_var in self.detail_value_vars.items():
            value_var.set(str(details.get(label, "—")))


def main():
    root = tk.Tk()
    AIDetectorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()