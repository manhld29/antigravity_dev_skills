#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""devcycle-ui core — BM25 search over a PySide6/QML/QSS design knowledge base.

Adapted from the ui-ux-pro-max skill (MIT, (c) nextlevelbuilder): same BM25 +
CSV-per-domain architecture, retuned for Qt desktop (QML Quick Controls + QSS on
QWidgets). No external dependencies — standard library only.
"""

import csv
import re
from pathlib import Path
from math import log
from collections import defaultdict

DATA_DIR = Path(__file__).parent.parent / "data"
MAX_RESULTS = 3

# Each domain -> CSV + which columns to search (BM25 corpus) and to print.
CSV_CONFIG = {
    "style": {
        "file": "styles.csv",
        "search_cols": ["Style", "Keywords", "Best For", "QML Theme"],
        "output_cols": ["Style", "Keywords", "Best For", "Primary Colors",
                        "Effects", "QML Theme", "QSS Notes", "Light", "Dark",
                        "Complexity"],
    },
    "color": {
        "file": "colors.csv",
        "search_cols": ["Palette", "Keywords", "Notes"],
        "output_cols": ["Palette", "Keywords", "Primary", "On Primary", "Accent",
                        "Background", "Surface", "Text", "Muted", "Border",
                        "Danger", "Dark Variant", "Notes"],
    },
    "typography": {
        "file": "typography.csv",
        "search_cols": ["Pairing", "Keywords", "Best For", "Heading Font", "Body Font"],
        "output_cols": ["Pairing", "Keywords", "Best For", "Heading Font",
                        "Body Font", "Mono Font", "Sizes", "Qt Loading", "Notes"],
    },
    "component": {
        "file": "components.csv",
        "search_cols": ["Component", "Keywords", "QML Control", "QSS Selector"],
        "output_cols": ["Component", "Keywords", "QML Control", "QSS Selector",
                        "Key Properties", "States", "Accessibility", "Notes"],
    },
    "ux": {
        "file": "ux-guidelines.csv",
        "search_cols": ["Category", "Issue", "Keywords", "Description"],
        "output_cols": ["Category", "Issue", "Keywords", "Description", "Do",
                        "Don't", "Severity"],
    },
    "layout": {
        "file": "layout.csv",
        "search_cols": ["Topic", "Keywords", "Guideline"],
        "output_cols": ["Topic", "Keywords", "Guideline", "Do", "Don't",
                        "Qt API", "Notes"],
    },
}

STACK_CONFIG = {
    "qml": {"file": "stacks/qml.csv"},   # QML / Quick Controls 2
    "qss": {"file": "stacks/qss.csv"},   # QWidgets + Qt Style Sheets
}

_STACK_COLS = {
    "search_cols": ["Category", "Guideline", "Description", "Do", "Don't"],
    "output_cols": ["Category", "Guideline", "Description", "Do", "Don't",
                    "Code Good", "Code Bad", "Severity", "Docs URL"],
}

AVAILABLE_STACKS = list(STACK_CONFIG.keys())


class BM25:
    """BM25 ranking (k1/b defaults). Lifted from ui-ux-pro-max (MIT)."""

    def __init__(self, k1=1.5, b=0.75):
        self.k1, self.b = k1, b
        self.corpus, self.doc_lengths = [], []
        self.avgdl, self.N = 0, 0
        self.idf = {}
        self.doc_freqs = defaultdict(int)

    def tokenize(self, text):
        text = re.sub(r"[^\w\s]", " ", str(text).lower())
        return [w for w in text.split() if len(w) > 2]

    def fit(self, documents):
        self.corpus = [self.tokenize(d) for d in documents]
        self.N = len(self.corpus)
        if self.N == 0:
            return
        self.doc_lengths = [len(d) for d in self.corpus]
        self.avgdl = sum(self.doc_lengths) / self.N
        for doc in self.corpus:
            for word in set(doc):
                self.doc_freqs[word] += 1
        for word, freq in self.doc_freqs.items():
            self.idf[word] = log((self.N - freq + 0.5) / (freq + 0.5) + 1)

    def score(self, query):
        q = self.tokenize(query)
        scores = []
        for idx, doc in enumerate(self.corpus):
            doc_len = self.doc_lengths[idx]
            tf = defaultdict(int)
            for w in doc:
                tf[w] += 1
            s = 0.0
            for token in q:
                if token in self.idf:
                    f = tf[token]
                    num = f * (self.k1 + 1)
                    den = f + self.k1 * (1 - self.b + self.b * doc_len / self.avgdl)
                    s += self.idf[token] * num / den
            scores.append((idx, s))
        return sorted(scores, key=lambda x: x[1], reverse=True)


def _load_csv(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _search_csv(filepath, search_cols, output_cols, query, max_results):
    if not filepath.exists():
        return []
    data = _load_csv(filepath)
    documents = [" ".join(str(r.get(c, "")) for c in search_cols) for r in data]
    bm25 = BM25()
    bm25.fit(documents)
    out = []
    for idx, score in bm25.score(query)[:max_results]:
        if score > 0:
            row = data[idx]
            out.append({c: row.get(c, "") for c in output_cols if c in row})
    return out


def detect_domain(query):
    q = query.lower()
    domain_keywords = {
        "color": ["color", "colour", "palette", "hex", "theme color", "accent",
                  "qpalette", "background", "surface", "contrast"],
        "typography": ["font", "typography", "typeface", "heading", "body text",
                       "monospace", "qfont", "point size", "pairing"],
        "component": ["button", "dialog", "combobox", "checkbox", "table",
                      "treeview", "tab", "menu", "toolbar", "slider", "spinbox",
                      "list", "scrollbar", "groupbox", "lineedit", "control"],
        "layout": ["layout", "spacing", "margin", "anchor", "grid", "stretch",
                   "high-dpi", "hidpi", "scaling", "responsive", "alignment"],
        "ux": ["ux", "usability", "accessibility", "focus", "keyboard", "shortcut",
               "feedback", "loading", "thread", "freeze", "error"],
        "style": ["style", "fusion", "fluent", "material", "universal", "flat",
                  "dark mode", "minimal", "native", "qss", "qml theme", "skin"],
    }
    scores = {d: sum(1 for kw in kws if kw in q) for d, kws in domain_keywords.items()}
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "style"


def search(query, domain=None, max_results=MAX_RESULTS):
    if domain is None:
        domain = detect_domain(query)
    config = CSV_CONFIG.get(domain, CSV_CONFIG["style"])
    filepath = DATA_DIR / config["file"]
    if not filepath.exists():
        return {"error": f"File not found: {filepath}", "domain": domain}
    results = _search_csv(filepath, config["search_cols"], config["output_cols"],
                          query, max_results)
    return {"domain": domain, "query": query, "file": config["file"],
            "count": len(results), "results": results}


def search_stack(query, stack, max_results=MAX_RESULTS):
    if stack not in STACK_CONFIG:
        return {"error": f"Unknown stack: {stack}. Available: {', '.join(AVAILABLE_STACKS)}"}
    filepath = DATA_DIR / STACK_CONFIG[stack]["file"]
    if not filepath.exists():
        return {"error": f"Stack file not found: {filepath}", "stack": stack}
    results = _search_csv(filepath, _STACK_COLS["search_cols"],
                          _STACK_COLS["output_cols"], query, max_results)
    return {"domain": "stack", "stack": stack, "query": query,
            "file": STACK_CONFIG[stack]["file"], "count": len(results),
            "results": results}
