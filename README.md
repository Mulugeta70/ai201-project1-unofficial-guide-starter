# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

CS student experiences and career advice shared publicly on Hacker News and dev.to — covering imposter syndrome, difficult courses, internship hunting, open-source contribution, and transitioning from school to industry. This knowledge is valuable because official channels (career centers, department websites) offer generic guidance, while the real, honest firsthand experiences of students — including failures, self-doubt, and what actually worked — are scattered across community forums and blogs that are hard to search systematically.

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | Ask HN: Maybe I'm just not smart enough? | Forum thread | https://news.ycombinator.com/item?id=26902219 |
| 2 | Ask HN: Is it possible for someone to not be cut out for software engineering? | Forum thread | https://news.ycombinator.com/item?id=12516611 |
| 3 | Ask HN: How did you become a software engineer? | Forum thread | https://news.ycombinator.com/item?id=28457499 |
| 4 | Ask HN: Advice for a frustrated CS student | Forum thread | https://news.ycombinator.com/item?id=6008850 |
| 5 | Ask HN: What advice do you have for new CS students? | Forum thread | https://news.ycombinator.com/item?id=36664044 |
| 6 | Ask HN: Advice for taking difficult CS programming courses? | Forum thread | https://news.ycombinator.com/item?id=2749231 |
| 7 | Ask HN: Career advice after graduating undergrad | Forum thread | https://news.ycombinator.com/item?id=45131312 |
| 8 | Ask HN: International student in Canada struggling to find a CS internship | Forum thread | https://news.ycombinator.com/item?id=37374626 |
| 9 | Ask HN: Thoughts on grad school? (CS PhD) | Forum thread | https://news.ycombinator.com/item?id=244100 |
| 10 | I'm a 21-Year-Old Student Who Shipped 7 AI Apps and 7 Open Source Libraries | Blog article | https://dev.to/iamadhitya/im-a-21-year-old-student-who-shipped-7-ai-apps-and-7-open-source-libraries-heres-the-strategy-3cpi |
| 11 | From AI/ML Student to GenAI Engineer: My 6-Month Learning Plan for 2026 | Blog article | https://dev.to/procoder_45/from-aiml-student-to-genai-engineer-my-6-month-learning-plan-for-2026-298e |
| 12 | GSoC 2026 Week 1 — What Happens When a Student Clicks "Open Assignment"? | Blog article | https://dev.to/magic-peach/gsoc-2026-week-1-what-happens-when-a-student-clicks-open-assignment-1jk4 |
| 13 | Why You Should Build an Online Presence as a Developer | Blog article | https://dev.to/kislay/why-you-should-build-an-online-presence-as-a-developer-3j95 |

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:**

**Overlap:**

**Why these choices fit your documents:**

**Final chunk count:**

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:**

**Production tradeoff reflection:**

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**

**How source attribution is surfaced in the response:**

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:**

**What the system returned:**

**Root cause (tied to a specific pipeline stage):**

**What you would change to fix it:**

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**

**One way your implementation diverged from the spec, and why:**

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*

**Instance 2**

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*
