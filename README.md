# The Unofficial CS Student Guide

A RAG system that answers questions about CS student experiences — imposter syndrome, difficult courses, internship hunting, grad school, and career transitions — using 13 real Hacker News threads and dev.to articles.

---

## Domain

CS student experiences and career advice shared on Hacker News and dev.to. This knowledge is hard to find through official channels because career centers give generic guidance, while honest firsthand student experiences — including failures and what actually worked — are scattered across community forums.

---

## Document Sources

| # | Source | Type | URL |
|---|--------|------|-----|
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

**Chunk size:** 600 characters maximum (~120 tokens), minimum 100 characters.

**Overlap:** 50 characters, applied only when a long paragraph is split into sub-chunks.

**Why these choices fit the documents:**

The natural semantic unit in this corpus is the individual forum comment or blog paragraph. HN comments are typically 100–500 characters and represent one complete piece of advice. Splitting on `\n\n` paragraph boundaries preserves these units intact. The 600-character cap handles the rare long comment by splitting at the nearest sentence boundary. The 100-character minimum filters out header lines (`TITLE:`, `SOURCE:`) and markdown separators that carry no retrievable content.

The overlap is small because HN comments are independent — carrying text from one commenter into the next would falsely imply a connection between unrelated opinions. Overlap only applies within a single long paragraph split into multiple sub-chunks.

**Final chunk count:** 485 chunks across 13 documents. Average length: 252 characters.

---

## Sample Chunks

**Chunk 1** — `hn_imposter_syndrome_maybe_not_smart_enough.txt`
> [commandlinefan]: I suspect that, with the exception of the truly mentally handicapped, there's nobody that's literally not smart enough to produce good, solid working software. There are, however, people who give up because there's so much that you have to not just learn, but truly internalize. I'm smart enough to solve calculus problems, but not smart enough to make revolutionary advances in mathematics. Similarly, I probably won't invent the next PageRank, but there's plenty of room for people who can study the techniques, grind through the examples and apply them.

**Chunk 2** — `hn_advice_difficult_cs_courses.txt`
> [bankim]: Don't worry too much about grades. Take on the challenge. Before taking up OS course, make sure you become proficient in C and understanding pointers.

**Chunk 3** — `hn_cs_grad_school_advice.txt`
> [lbrandy]: Just FYI, I have an MS in EE and I work at a pattern-rec startup. So, no PhD not really required to get a job in that field. That being said, having a PhD helps a lot if you want to take on the 'scientist' role right off the bat.

**Chunk 4** — `hn_advice_frustrated_cs_student.txt`
> [mknappen]: "Nobody tells this to people who are beginners, I wish someone told me. All of us who do creative work, we get into it because we have good taste. But there is this gap. For the first couple years you make stuff, it's just not that good. It's trying to be good, it has potential, but it's not. But your taste, the thing that got you into the game, is still killer. And your taste is why your work disappoints you."

**Chunk 5** — `devto_build_online_presence_developer.txt`
> Take a junior engineer trying to stand out. They build a simple weather application. On GitHub, it is just a README and a folder of code. But on their personal site, they write a post detailing their thought process. They explain why they chose a specific weather API, how they handled asynchronous state, and how they deployed it using GitHub Actions.

---

## Embedding Model

**Model used:** `all-MiniLM-L6-v2` via `sentence-transformers` — local inference, no API key required.

Produces 384-dimensional embeddings with a 256-token input limit. Our chunks average ~100 tokens, fitting comfortably within the window. Runs on CPU in under 50ms per chunk.

**Production tradeoff reflection:**

| Tradeoff | Option A | Option B |
|----------|----------|----------|
| Accuracy vs. cost | `all-MiniLM-L6-v2` — free, local, good for English | `text-embedding-3-small` (OpenAI) — higher accuracy, 8191-token window, ~$0.02/1M tokens |
| Quality vs. speed | `all-MiniLM-L6-v2` — fast on CPU | `all-mpnet-base-v2` — better quality, 768-dim, slower on CPU |
| Multilingual | Not supported | `multilingual-e5-base` or `LaBSE` — handles 100+ languages |
| Domain-specific | General English (works for this corpus) | `specter2` — better for academic CS papers |

---

## Retrieval Test Results

**Query: "What advice do people give for surviving a difficult Operating Systems course at university?"**

| Rank | Distance | File | Chunk excerpt |
|------|----------|------|---------------|
| 1 | 0.327 | hn_advice_difficult_cs_courses.txt | "If anyone did well in their respective OS courses could you provide some advices?" |
| 2 | 0.374 | hn_advice_difficult_cs_courses.txt | "The CS program in my University only offers three programming courses..." |
| 3 | 0.527 | hn_advice_for_new_cs_student.txt | "I got a small part of knowledge from studying and a large parts in a laboratory..." |
| 4 | 0.538 | hn_how_did_you_become_software_engineer.txt | "[elohssa]: I was into computers as a kid..." |
| 5 | 0.538 | hn_advice_difficult_cs_courses.txt | "[bankim]: Don't worry too much about grades. Take on the challenge..." |

Three of the five results come from the correct document. Result 5 (bankim) contains the core advice — C proficiency, take the challenge, grades secondary. Results 1–2 are the question body of the same thread, which are relevant context even though they contain no advice themselves. Results 3–4 are weaker matches about systems learning.

---

**Query: "Do experienced engineers say a CS PhD is required to work in AI or machine learning?"**

| Rank | Distance | File | Chunk excerpt |
|------|----------|------|---------------|
| 1 | 0.355 | hn_cs_grad_school_advice.txt | "I'm interested in AI/machine learning research, which practically require a PhD..." |
| 2 | 0.365 | hn_cs_grad_school_advice.txt | "[lbrandy]: ...no PhD not really required to get a job in that field..." |
| 3 | 0.411 | hn_cs_grad_school_advice.txt | "[DaniFong]: I can show that you don't need to finish a PhD in AI to do research..." |
| 4 | 0.465 | devto_aiml_student_to_genai_engineer.txt | "My name is Anupam, and I am currently pursuing a B.Tech in CS with a specialization in AI & ML." |
| 5 | 0.483 | hn_cs_grad_school_advice.txt | "[ahsonwardak]: My friend, I think you're more than set to get into CS grad school..." |

Four of five results come from the exact right document. Results 1–3 together present both sides: PhD "practically required" for pure research, but an MS is sufficient for industry AI roles and you can do research without finishing a PhD. Retrieval is precise here because the query vocabulary — PhD, AI, machine learning — matches the document directly.

---

**Query: "How do students and developers recommend building a visible portfolio and online presence while still in school?"**

| Rank | Distance | File | Chunk excerpt |
|------|----------|------|---------------|
| 1 | 0.418 | hn_advice_frustrated_cs_student.txt | "[tmwhtkr]: ...try your hand at some other aspects of programming...building websites or apps..." |
| 2 | 0.488 | hn_how_did_you_become_software_engineer.txt | "I spent time on projects and solving problems I had. I wrote many different web apps..." |
| 3 | 0.518 | hn_how_did_you_become_software_engineer.txt | "I hated my thesis and went to a coding bootcamp..." |
| 4 | 0.531 | hn_advice_frustrated_cs_student.txt | "I'm a 21-year-old CS junior undergraduate..." |
| 5 | 0.538 | hn_how_did_you_become_software_engineer.txt | "In high school my server grew more and more..." |

Results 1 and 2 are relevant — the first advises building websites and apps as a portfolio; the second describes a student who built web apps during college to demonstrate skill. The dedicated dev.to online-presence article ranks at position 10 (distance 0.603) because the query uses student framing ("while in school") while the article uses professional framing ("professional home on the internet", "SEO"), creating a vocabulary mismatch in the embedding space.

---

## Grounded Generation

**System prompt grounding instruction:**

```
You are an assistant that answers questions about computer science student
experiences using only the documents provided to you.

Rules you must follow without exception:
1. Answer using ONLY the information that appears in the numbered context blocks below.
2. Do not use any knowledge from your training data.
3. For every claim you make, cite the source number in square brackets, e.g. [1] or [2].
4. If the provided context does not contain enough information to answer the question,
   respond with exactly this sentence and nothing else:
   "I don't have enough information on that in my documents."
5. Do not speculate, infer, or fill gaps with outside knowledge.
```

**How source attribution works:**

Retrieved chunks are passed to the model as numbered blocks:

```
[1] Source: https://news.ycombinator.com/item?id=26902219
<chunk text>

[2] Source: https://news.ycombinator.com/item?id=244100
<chunk text>
```

The model cites `[1]`, `[2]`, etc. inline for every claim. After generation, `query.py` also appends a deduplicated list of retrieved source URLs programmatically — ensuring attribution even if the model omits a citation.

---

## Example Responses

**Example 1 — Grounded response with citations**

Query: *"Do experienced engineers say a CS PhD is required to work in AI or machine learning?"*

> No, experienced engineers do not universally say a CS PhD is required to work in AI or machine learning. According to [2], having a PhD is not required to get a job in the field, although it can be helpful for taking on a 'scientist' role. Additionally, [3] states that it is possible to do research and create AI without finishing a PhD. [1] mentions that a PhD is practically required for AI/machine learning research, but this is not a universal opinion.

Retrieved from:
- https://news.ycombinator.com/item?id=244100
- https://dev.to/procoder_45/from-aiml-student-to-genai-engineer-my-6-month-learning-plan-for-2026-298e

---

**Example 2 — Grounded response with citations**

Query: *"What advice do people give for surviving a difficult Operating Systems course at university?"*

> To survive a difficult Operating Systems course, people advise to not worry too much about grades and take on the challenge [5]. It is also recommended to become proficient in C and understand pointers before taking the OS course [5]. Additionally, hands-on experience, such as laboratory work or dabbling in topics of interest, can be beneficial [3].

Retrieved from:
- https://news.ycombinator.com/item?id=2749231
- https://news.ycombinator.com/item?id=36664044
- https://news.ycombinator.com/item?id=28457499

---

**Example 3 — Out-of-scope refusal**

Query: *"What is the capital of France?"*

> I don't have enough information on that in my documents.

---

## Query Interface

Run with `python app.py`, open `http://localhost:7860`.

**Inputs:** Text box for the question. Submit with the Ask button or Enter key.

**Outputs:**
- **Answer** — LLM response with inline `[N]` citations referencing retrieved chunks.
- **Retrieved from** — deduplicated list of source URLs consulted.

Five example questions are pre-loaded as clickable chips below the input.

**Sample interaction:**

```
Question:
  Should I pursue a CS PhD or go into industry after finishing my bachelor's?

Answer:
  According to [2], most PhD students in CS are focused on academics, and it is not
  typically a path for entrepreneurs. However, [3] mentions that a CS PhD can provide
  fully funded research projects and strong career possibilities. On the other hand,
  [4] suggests that a CS degree may not be necessary for a successful career, and [5]
  recommends studying broadly outside of CS. Pursuing a CS PhD may be beneficial for
  those interested in research [1, 3], but going into industry is also a viable path [5].

Retrieved from:
  • https://news.ycombinator.com/item?id=244100
  • https://news.ycombinator.com/item?id=28457499
  • https://news.ycombinator.com/item?id=6008850
  • https://news.ycombinator.com/item?id=36664044
```

---

## Evaluation Report

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | What do people suggest to CS students who feel they are not smart enough to succeed? | Mentions separating interview failure from intelligence, value of persistence, ADHD as a possible factor, and practicing interview questions specifically. | "Don't give up — it's likely persistence not intelligence [5]. With enough effort, anyone can produce solid software [5]. Cultivate peer relationships and experiment to learn from mistakes [2]. Study broadly outside CS [4]." Three sources. | Relevant | Partially accurate |
| 2 | What advice do people give for surviving a difficult Operating Systems course at university? | Become proficient in C and pointers before the course; take on the challenge; don't worry excessively about grades. | "Don't worry about grades, take on the challenge [5]. Become proficient in C and pointers before the OS course [5]. Hands-on lab experience also helps [3]." Three sources. | Relevant | Accurate |
| 3 | Do experienced engineers say a CS PhD is required to work in AI or machine learning? | PhD required for pure research; MS or strong industry background sufficient for most industry AI roles; can do research without finishing a PhD. | "No, not universally required. No PhD needed for industry AI engineering [2]. Can do research and create AI without finishing a PhD [3]. PhD helps for scientist role [2]." Two sources. | Relevant | Accurate |
| 4 | What do people recommend for CS students who lose motivation and can't finish side projects? | The Ira Glass taste gap — your taste exceeds your skill, fix is high-volume output; get a job with smart people to force project completion. | "I don't have enough information on that in my documents." | Partially relevant | Inaccurate |
| 5 | How do students and developers recommend building a visible portfolio and online presence while still in school? | Build a personal website you own; write about your projects; ship publicly rather than announcing; extract reusable code into open-source libraries. | "Try different programming aspects — build websites, apps, teach yourself Ruby on Rails [1]. Set up a portfolio website and server [1]. Build web apps and improve school interfaces [2]. Create NodeJS apps and freelance [3]." Two source URLs, three retrieved chunks. | Partially relevant | Partially accurate |

**Retrieval quality:** Relevant / Partially relevant / Off-target
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

**Question:** "What do people recommend for CS students who lose motivation and can't finish side projects?"

**What the system returned:** "I don't have enough information on that in my documents."

**Root cause:**

The failure is in the retrieval stage, not generation. The top retrieved chunk (distance 0.350) is the HN question body: *"I'm a 21-year-old CS junior undergraduate, and it looks like I can't put my mind into working on side projects."* This chunk describes the student's problem using the same words as the query ("can't finish side projects", "motivation"), so the embedding model ranks it highest. But it contains no advice.

The chunk with the relevant advice — the Ira Glass taste-gap quote — uses completely different vocabulary: *taste, creative work, gap, volume of work, fight your way through.* None of those words appear in the query. The embedding for that chunk sits in a different region of the 384-dimensional space, so it never enters the top-5 retrieved set.

**Fix:** Separate question-body chunks from answer/comment chunks at ingestion time. Tag them with a `role` metadata field and exclude question-body chunks from retrieval — a user asking for advice is never helped by retrieving a document that is itself asking the same question.

---

## Spec Reflection

**One way the spec helped:**

The Anticipated Challenges section in planning.md named the semantic bleed problem before any code was written — the observation that imposter syndrome, frustration, and new-student-advice threads all use similar vocabulary. That warning shaped the system prompt: rather than instructing the model to answer from "the most relevant document," the prompt requires citing each claim by source number and synthesizing across sources. Without naming that risk upfront, the prompt would likely have collapsed multiple perspectives into a single uncited paragraph.

**One way implementation diverged from the spec:**

The spec stated overlap would apply between adjacent chunks. During implementation, HN comments turned out to be fully independent — carrying the tail of one commenter's opinion into the beginning of another's would suggest a false relationship between unrelated people. Overlap was changed to apply only within a single long paragraph split into sub-chunks, not across paragraph boundaries. The planning.md Chunking Strategy section was updated after testing confirmed this was the right behavior.

---

## AI Usage

**Instance 1 — Ingestion and chunking**

- *Input to AI:* The Chunking Strategy section from planning.md plus the raw text of `hn_advice_frustrated_cs_student.txt` as a concrete example.
- *What it produced:* Working `chunk_text()` and `load_documents()` functions matching the spec.
- *What I changed:* The `_split_at_sentences()` function had a bug — adding a 50-character overlap tail to a new sub-chunk could push total length above 600 characters when the first sentence was already near-max. I identified this from the output showing `max length: 668 chars` and added a guard that skips the tail if `tail + sentence > max_size`. I also restricted overlap to within-paragraph splits only.

**Instance 2 — Embedding and retrieval**

- *Input to AI:* The Retrieval Approach section, the `load_documents()` output format, and the ChromaDB Python client API.
- *What it produced:* `build_vector_store()` and `retrieve()` functions embedding chunks and querying ChromaDB.
- *What I changed:* The generated code used `chromadb.Client()` (in-memory only). I changed it to `chromadb.PersistentClient(path="chroma_db")` so embeddings survive between runs. I also added a count check (`collection.count() == len(chunks)`) to skip re-embedding on startup, reducing load time from ~5 seconds to under 1 second.
