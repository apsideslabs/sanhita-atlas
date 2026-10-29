# -*- coding: utf-8 -*-
"""Extracts the BNS 2023 text, section by section, from the Gazette PDF."""
import json
import re
import pymupdf as fitz

PDF = "/scratch/work/bns/bns.pdf"
ROMAN = {"I": 1, "II": 2, "III": 3, "IV": 4, "V": 5, "VI": 6, "VII": 7, "VIII": 8, "IX": 9,
         "X": 10, "XI": 11, "XII": 12, "XIII": 13, "XIV": 14, "XV": 15, "XVI": 16,
         "XVII": 17, "XVIII": 18, "XIX": 19, "XX": 20}

SEC_RE = re.compile(r"^(\d{1,3})\.\s*")
CHAP_RE = re.compile(r"^CHAPTER\s+([IVX]+)\b")
NOISE = re.compile(r"(THE GAZETTE OF INDIA EXTRAORDINARY|^\d+\s*$|^Sec\.\s*\d+\]|^______)")


def clean(s):
    s = s.replace("\u00ad", "")
    s = re.sub(r"-\n(?=[a-z])", "", s)          # de-hyphenate across line breaks
    s = re.sub(r"\s*\n\s*", " ", s)
    s = re.sub(r"\s{2,}", " ", s)
    return s.strip()


def main():
    doc = fitz.open(PDF)
    body, notes, chapters = [], [], []

    for pno, page in enumerate(doc):
        blocks = [b for b in page.get_text("blocks") if b[4].strip()]
        for b in blocks:
            x0, y0, x1, y1, txt = b[0], b[1], b[2], b[3], b[4]
            t = txt.strip()
            if NOISE.search(t.split("\n")[0]):
                continue
            if x0 >= 470:                        # right-margin marginal note
                notes.append((pno, y0, clean(t)))
                continue
            if x0 < 60:                          # left-margin marginal note (even pages)
                notes.append((pno, y0, clean(t)))
                continue
            body.append((pno, y0, t))

    # walk body in reading order; a line that starts a new number in sequence
    # opens a new section (sections run 1..358 with no gaps)
    sections, cur, expect = {}, None, 1
    for pno, y, t in body:
        lines = t.split("\n")
        for i, line in enumerate(lines):
            mc = CHAP_RE.match(line.strip())
            if mc:
                chapters.append((ROMAN.get(mc.group(1), 0), pno, y + i * 11.0))
                continue
            ms = SEC_RE.match(line.strip())
            if ms and int(ms.group(1)) == expect:
                cur = expect
                sections[cur] = {"n": cur, "text": line.strip(),
                                 "page": pno, "y": y + i * 11.0}
                expect += 1
                continue
            if cur is not None:
                sections[cur]["text"] += " " + line.strip()

    for sec in sections.values():
        sec["text"] = clean(sec["text"])

    # attach the nearest marginal note as the section title
    notes.sort(key=lambda x: (x[0], x[1]))
    for s in sections.values():
        best, bd = None, 1e9
        for pno, y, t in notes:
            if pno == s["page"]:
                d = abs(y - s["y"])
                if d < bd and 6 < len(t) < 140:
                    bd, best = d, t
        s["title"] = best if bd <= 120 else ""

    # chapter for each section
    chapters.sort()
    def chap_of(n):
        c = 0
        for num, pno, y in chapters:
            if (pno, y) <= (sections[n]["page"], sections[n]["y"]):
                c = num
        return c
    for n, s in sections.items():
        s["chapter"] = chap_of(n)

    missing = [i for i in range(1, 359) if i not in sections]
    print("sections found:", len(sections), "missing:", missing[:20], "count", len(missing))
    print("chapters found:", len(chapters))
    out = [sections[k] for k in sorted(sections)]
    with open("/scratch/work/bns/sections.json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    for n in (1, 103, 111, 152, 303, 356):
        s = sections.get(n)
        if s:
            print("\n--- %d [%s] (ch %s)" % (n, s["title"], s["chapter"]))
            print(s["text"][:240])


if __name__ == "__main__":
    main()
