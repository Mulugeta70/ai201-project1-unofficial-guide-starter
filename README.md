# The Unofficial Guide — Project 1

---

## Domain

CS student experiences and career advice shared publicly on Hacker News and dev.to — covering imposter syndrome, navigating difficult courses, internship hunting, open-source contribution, and transitioning from school to industry. This knowledge is valuable because official channels (career centers, department websites) offer generic guidance, while the real, honest firsthand experiences of students — including failures, self-doubt, and what actually worked — are scattered across community forums and blogs that are hard to search systematically.

---

## Document Sources

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

**Chunk size:** 600 characters maximum (~120 tokens), with a minimum of 100 characters.

**Overlap:** 50 characters, applied only when a long paragraph is split into sub-chunks.

**Why these choices fit your documents:**

The corpus has two document types that share the same natural semantic unit: the individual paragraph or forum comment. HN threads are structured as a question body followed by a list of comments, each formatted as `[username]: text`. A single comment is typically 100–500 characters and represents one complete, self-contained piece of advice. Dev.to articles are broken into short paragraphs of 50–150 words under markdown headers.

Splitting on double-newline paragraph boundaries (`\n\n`) respects these natural units. The 600-character maximum handles the rare comment that runs long by forcing a split at the nearest sentence boundary. The 100-character minimum discards header metadata lines (`TITLE:`, `AUTHOR:`, `SOURCE:`) and markdown section separators (`---`) that would otherwise appear as meaningless zero-content chunks in the vector store.

The 50-character overlap is intentionally small because most chunks are self-contained comments. Large overlap (200+ characters) is more useful for documents where meaning accumulates across paragraphs, such as legal briefs. Here, a small overlap only guards against the edge case where a key sentence lands exactly at a chunk boundary.

**Final chunk count:** 485 chunks across 13 documents. Average length: 252 characters.

---

## Sample Chunks

Five representative chunks drawn from different documents, each self-contained enough to answer a specific question on its own:

**Chunk 1** — `hn_imposter_syndrome_maybe_not_smart_enough.txt` (https://news.ycombinator.com/item?id=26902219)
> [commandlinefan]: I suspect that, with the exception of the truly mentally handicapped, there's nobody that's literally not smart enough to produce good, solid working software. There are, however, people who give up because there's so much that you have to not just learn, but truly internalize. I'm smart enough to solve calculus problems, but not smart enough to make revolutionary advances in the field of mathematics. Similarly, I probably won't invent the next PageRank, but there's plenty of room for people who can study the techniques, grind through the examples and apply them.

**Chunk 2** — `hn_advice_difficult_cs_courses.txt` (https://news.ycombinator.com/item?id=2749231)
> [bankim]: Don't worry too much about grades. Take on the challenge. Before taking up OS course, make sure you become proficient in C and understanding pointers.

**Chunk 3** — `hn_cs_grad_school_advice.txt` (https://news.ycombinator.com/item?id=244100)
> [lbrandy]: Just FYI, I have an MS in EE and I work at a pattern-rec startup. So, no PhD not really required to get a job in that field. That being said, having a PhD helps a lot if you want to take on the 'scientist' role right off the bat (for example, my job duties have included things like optimizing the algorithm both computationally and algorithmically).

**Chunk 4** — `hn_advice_frustrated_cs_student.txt` (https://news.ycombinator.com/item?id=6008850)
> [mknappen]: "Nobody tells this to people who are beginners, I wish someone told me. All of us who do creative work, we get into it because we have good taste. But there is this gap. For the first couple years you make stuff, it's just not that good. It's trying to be good, it has potential, but it's not. But your taste, the thing that got you into the game, is still killer. And your taste is why your work disappoints you. A lot of people never get past this phase, they quit. Most people I know who do interesting, creative work went through years of this.

**Chunk 5** — `devto_build_online_presence_developer.txt` (https://dev.to/kislay/why-you-should-build-an-online-presence-as-a-developer-3j95)
> Take a junior engineer trying to stand out. They build a simple weather application. On GitHub, it is just a README and a folder of code. But on their personal site, they write a post detailing their thought process. They explain why they chose a specific weather API, how they handled asynchronous state, and how they deployed it using GitHub Actions.

---

## Embedding Model

**Model used:** `all-MiniLM-L6-v2` via `sentence-transformers` (local inference, no API key).

This model produces 384-dimensional embeddings with a 256-token input limit. Our chunks average around 100 tokens, so they fit comfortably within the window. The model runs on CPU in under 50ms per chunk and has strong performance on general English conversational text, which matches this corpus of forum comments and blog posts.

**Production tradeoff reflection:**

Choosing an embedding model for a real deployment involves at least four tradeoffs:

**Accuracy vs. cost.** OpenAI `text-embedding-3-small` consistently outperforms MiniLM on retrieval benchmarks and supports up to 8,191 tokens per input, allowing full short documents to be embedded without chunking. The cost is ~$0.02 per million tokens plus network latency on every embed call. For a high-traffic system this adds up; for a low-traffic internal tool the accuracy gain is likely worth it.

**Model size vs. quality.** `all-mpnet-base-v2` is a step up in quality from MiniLM with 768-dimensional embeddings and still runs locally, but is roughly twice the disk footprint and noticeably slower on CPU. On a machine with a GPU it would be the straightforward upgrade path.

**Multilingual support.** This corpus is entirely English. If the system served students writing in other languages, `multilingual-e5-base` or `LaBSE` would be required. Both degrade slightly on English versus a monolingual model but handle 100+ languages.

**Domain specificity.** Forum comments and personal blog posts are informal conversational English — a general model handles this well. If the corpus were academic CS papers, a fine-tuned model like `specter2` would retrieve more precisely on technical terminology.

---

## Retrieval Test Results

Three evaluation queries with their top returned chunks and relevance explanation:

**Query: "What advice do people give for surviving a difficult Operating Systems course at university?"**

| Rank | Distance | File | Chunk excerpt |
|------|----------|------|---------------|
| 1 | 0.327 | hn_advice_difficult_cs_courses.txt | "If anyone did well in their respective OS courses could you provide some advices?" |
| 2 | 0.374 | hn_advice_difficult_cs_courses.txt | "The CS program in my University only offers three programming courses..." |
| 3 | 0.527 | hn_advice_for_new_cs_student.txt | "I got a small part of knowledge from studying and a large parts in a laboratory..." |
| 4 | 0.538 | hn_how_did_you_become_software_engineer.txt | "[elohssa]: I was into computers as a kid, but in the days before the internet..." |
| 5 | 0.538 | hn_advice_difficult_cs_courses.txt | "[bankim]: Don't worry too much about grades. Take on the challenge..." |

The top two results are from the OS course thread, which is exactly the right document. Result 5 (the bankim comment) contains the core advice about C proficiency and taking the challenge. Results 3–4 are weaker matches from tangentially related documents about learning systems programming.

**Query: "Do experienced engineers say a CS PhD is required to work in AI or machine learning?"**

| Rank | Distance | File | Chunk excerpt |
|------|----------|------|---------------|
| 1 | 0.355 | hn_cs_grad_school_advice.txt | "I'm interested in AI/machine learning research, which practically require a PhD..." |
| 2 | 0.365 | hn_cs_grad_school_advice.txt | "[lbrandy]: Just FYI, I have an MS in EE and I work at a pattern-rec startup. So, no PhD not really required..." |
| 3 | 0.411 | hn_cs_grad_school_advice.txt | "[DaniFong]: I can show that you don't need to finish a PhD in AI to do research..." |
| 4 | 0.465 | devto_aiml_student_to_genai_engineer.txt | "My name is Anupam, and I am currently pursuing a B.Tech in CS with a specialization in AI & ML." |
| 5 | 0.483 | hn_cs_grad_school_advice.txt | "[ahsonwardak]: My friend, I think you're more than set to get into CS grad school..." |

Four of the five top chunks come from the grad school thread — the correct document. Results 1, 2, and 3 contain both sides of the argument (PhD "practically required" for research, but an MS is sufficient for industry). The retrieval here is highly targeted because the query vocabulary ("PhD", "AI", "machine learning") matches the document vocabulary precisely.

**Query: "How do students and developers recommend building a visible portfolio and online presence while still in school?"**

| Rank | Distance | File | Chunk excerpt |
|------|----------|------|---------------|
| 1 | 0.418 | hn_advice_frustrated_cs_student.txt | "[tmwhtkr]: ...try your hand at some other aspects of programming...building websites or apps..." |
| 2 | 0.488 | hn_how_did_you_become_software_engineer.txt | "I spent time on projects and solving problems I had. I wrote many different web apps..." |
| 3 | 0.518 | hn_how_did_you_become_software_engineer.txt | "I hated my thesis and went to a coding bootcamp..." |
| 4 | 0.531 | hn_advice_frustrated_cs_student.txt | "I'm a 21-year-old CS junior undergraduate..." |
| 5 | 0.538 | hn_how_did_you_become_software_engineer.txt | "In high school my server grew more and more..." |

Results 1 and 2 are relevant: the first chunk directly advises a student to build websites and apps as a portfolio alternative to games; the second describes a student who built personal web apps during college as a way to demonstrate skill. Both address the question from the angle of building visible work while in school. Results 3–5 are weaker matches that describe learning paths rather than portfolio-building specifically.

The dedicated dev.to online presence article ranks at position 10 (distance 0.603) rather than the top 5 despite being the most precisely on-topic document. The cause is a vocabulary mismatch: the query uses student framing ("while in school") while the article uses professional framing ("your professional home on the internet", "SEO", "silent recruiter"). MiniLM embeddings place these in somewhat different semantic regions, so the HN chunks that use "school," "student," and "projects" outrank the article that does not.

---

## Grounded Generation

**System prompt grounding instruction:**

The system passes the following instruction as the `system` message to every Groq API call, before any user content:

```
You are an assistant that answers questions about computer science student
experiences using only the documents provided to you.

Rules you must follow without exception:
1. Answer using ONLY the information that appears in the numbered context
   blocks below.
2. Do not use any knowledge from your training data.
3. For every claim you make, cite the source number in square brackets,
   e.g. [1] or [2].
4. If the provided context does not contain enough information to answer
   the question, respond with exactly this sentence and nothing else:
   "I don't have enough information on that in my documents."
5. Do not speculate, infer, or fill gaps with outside knowledge.
```

**How source attribution is surfaced in the response:**

Attribution is enforced through two mechanisms working together. First, the system prompt requires the model to cite source numbers `[1]` through `[5]` for every claim it makes. Second, the retrieved chunks are formatted as numbered blocks before being passed to the model:

```
[1] Source: https://news.ycombinator.com/item?id=26902219
<chunk text>

[2] Source: https://news.ycombinator.com/item?id=244100
<chunk text>
...
```

This gives the model a concrete list to cite from. After generation, `query.py` also appends a deduplicated list of all retrieved source URLs programmatically, so even if the model fails to include an inline citation the user still sees which documents were consulted.

---

## Example Responses

**Example 1 — Grounded response with inline citations:**

Query: *"Do experienced engineers say a CS PhD is required to work in AI or machine learning?"*

Response:
> No, experienced engineers do not universally say a CS PhD is required to work in AI or machine learning. According to [2], having a PhD is not required to get a job in the field, although it can be helpful for taking on a 'scientist' role. Additionally, [3] states that it is possible to do research and create AI without finishing a PhD. [1] mentions that a PhD is practically required for AI/machine learning research, but this is not a universal opinion among experienced engineers.

Retrieved from:
- https://news.ycombinator.com/item?id=244100
- https://dev.to/procoder_45/from-aiml-student-to-genai-engineer-my-6-month-learning-plan-for-2026-298e

**Example 2 — Grounded response with inline citations:**

Query: *"What advice do people give for surviving a difficult Operating Systems course at university?"*

Response:
> To survive a difficult Operating Systems course, people advise to not worry too much about grades and take on the challenge [5]. It is also recommended to become proficient in C and understand pointers before taking the OS course [5]. Additionally, hands-on experience, such as laboratory work or dabbling in topics of interest, can be beneficial [3].

Retrieved from:
- https://news.ycombinator.com/item?id=2749231
- https://news.ycombinator.com/item?id=36664044
- https://news.ycombinator.com/item?id=28457499

**Example 3 — Out-of-scope refusal:**

Query: *"What is the capital of France?"*

Response:
> I don't have enough information on that in my documents.

The system does not fall back to general knowledge. The response is the exact phrase specified in the system prompt.

---

## Query Interface

The interface is a Gradio web app launched with `python app.py` and accessed at `http://localhost:7860`.

**Input fields:**
- A multi-line text box labeled "Your question" with a placeholder example query.
- An "Ask" button (primary style). Pressing Enter in the text box also submits.

**Output fields:**
- "Answer" — a read-only 10-line text area showing the LLM's grounded response with inline `[N]` citations.
- "Retrieved from" — a read-only 4-line text area showing the deduplicated list of source URLs consulted.

**Pre-loaded examples:** Five clickable example questions appear below the input, drawn from the evaluation plan. Clicking one populates the question box.

**Sample interaction transcript:**

```
Question: Should I pursue a CS PhD or go into industry after finishing my bachelor's?

Answer: According to [2], most PhD students in CS are focused on academics, and it is
not typically a path for entrepreneurs. However, [3] mentions that a CS PhD can provide
fully funded research projects and strong career possibilities. On the other hand, [4]
suggests that a CS degree may not be necessary for a successful career in the field,
and [5] recommends studying broadly outside of CS for a successful career. Considering
these points, it seems that pursuing a CS PhD may be beneficial for those interested in
academics or research [1, 3], but going into industry after a bachelor's degree could
also be a viable option [5].

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
| 1 | What do people suggest to CS students who feel they are not smart enough to succeed in the field? | Mentions separating interview failure from intelligence, the value of persistence, ADHD as a possible factor, and practicing interview questions specifically. | "People suggest CS students should not give up, as it's likely not a matter of intelligence but perseverance [5]. With enough effort to internalize material, anyone can produce solid software [5]. Cultivate relationships with smart peers and experiment to learn from mistakes [2]. Study broadly outside of CS [4]." Cites three sources. | Relevant | Partially accurate |
| 2 | What advice do people give for surviving a difficult Operating Systems course at university? | Become proficient in C and pointers before the course; take on the challenge rather than avoiding it; don't worry excessively about grades. | "Don't worry too much about grades and take on the challenge [5]. Become proficient in C and understand pointers before the OS course [5]. Hands-on lab experience can also be beneficial [3]." Cites three sources. | Relevant | Accurate |
| 3 | Do experienced engineers say a CS PhD is required to work in AI or machine learning? | PhD is required for pure research roles; an MS or strong industry background is sufficient for most industry AI positions; can do research and create AI without finishing a PhD. | "No, not universally required. An MS is sufficient for industry AI engineering [2]. You can do research and create AI without finishing a PhD [3]. A PhD helps for a 'scientist' role from day one [2]." Cites two sources. | Relevant | Accurate |
| 4 | What do people recommend for CS students who lose motivation and can't finish side projects? | The Ira Glass taste gap — your taste exceeds your current skill, the fix is producing high volume; get a job with smart people to force project completion through external accountability. | "I don't have enough information on that in my documents." | Partially relevant | Inaccurate |
| 5 | How do students and developers recommend building a visible portfolio and online presence while still in school? | Build a personal website you own; write about your projects to explain your thought process; ship publicly rather than announcing; extract reusable code into open-source libraries. | "Work on side projects and showcase them [1][2]. Build websites and apps to demonstrate skills [1][2]. Set up a portfolio website and learn server setup [1]. Freelancing and building multiple projects such as NodeJS apps can also help [3]." Cites two distinct source URLs across three retrieved chunks. | Partially relevant | Partially accurate |

**Retrieval quality:** Relevant / Partially relevant / Off-target
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

**Question that failed:** "What do people recommend for CS students who lose motivation and can't finish side projects?"

**What the system returned:** "I don't have enough information on that in my documents."

**Root cause (tied to a specific pipeline stage):**

The failure occurs in the retrieval stage, not the generation stage. The generation is actually working correctly — it sees a retrieved context that does not contain actionable advice, and correctly refuses rather than hallucinating.

The retrieval stage returns the wrong chunks. The top result (distance 0.350) is the HN question body: "I'm a 21-year-old CS junior undergraduate, and it looks like I can't put my mind into working on side projects." This chunk describes the student's *problem* in the same vocabulary the query uses ("can't finish side projects", "motivation"). The embedding model correctly identifies it as semantically close to the query — the problem and the question are nearly identical in meaning. But this chunk contains no advice.

The chunk that does contain the relevant advice — the Ira Glass quote posted by commenter `mknappen` — uses entirely different vocabulary: "taste," "creative work," "gap," "volume of work," "fight your way through." None of these words appear in the query. The embedding for this chunk sits in a different region of the 384-dimensional space from a query about "motivation" and "side projects." With k=5, this chunk never enters the retrieved set; the Zergy comment about "get a job with smart people" makes it in at position 3 but is too short and context-dependent for the model to generate a useful answer from alone.

**What you would change to fix it:**

The cleanest fix is to separate question body chunks from answer/comment chunks at ingestion time, and either tag them with a `role` metadata field or exclude question body chunks from the vector store entirely. A user asking for advice is never served by retrieving a document that is itself asking the same question. An alternative is to rewrite the query at runtime before embedding it — replacing "motivation" with vocabulary closer to what advice-givers actually write ("how to persist," "taste gap," "creative frustration") — but this requires either a rewriting model or hand-tuned synonyms.

---

## Spec Reflection

**One way the spec helped you during implementation:**

The planning.md Anticipated Challenges section forced me to articulate the semantic bleed problem before writing any code — the observation that imposter syndrome, frustration, and new-student-advice threads all use similar vocabulary. That warning was correct and shaped how I wrote the system prompt: instead of instructing the model to answer from "the most relevant document," the prompt instructs it to synthesize across numbered sources and cite each claim separately. Without having named that risk upfront, I would likely have written a simpler prompt that caused the model to collapse multiple perspectives into a single uncited paragraph.

**One way your implementation diverged from the spec, and why:**

The spec stated that overlap would apply between separate paragraphs ("50 characters between adjacent chunks"). During implementation I discovered that HN comments are fully independent units — carrying the tail of one comment into the beginning of the next would create misleading context where the model might infer a relationship between two unrelated people's opinions. The implementation applies overlap only within a single long paragraph that gets split into sub-chunks, and not across paragraph boundaries. The planning.md Chunking Strategy section was updated to reflect this after the implementation was tested.

---

## AI Usage

**Instance 1**

- *What I gave the AI:* The Chunking Strategy section from planning.md, including the paragraph-split approach, 600-char max, 50-char overlap, and 100-char minimum, plus the raw text of `hn_advice_frustrated_cs_student.txt` as a concrete example document.
- *What it produced:* A working `chunk_text()` function that split on `\n\n`, applied a max-size filter, and discarded short chunks. It also produced `load_documents()` that read `.txt` files and returned a list of dicts.
- *What I changed or overrode:* The generated `_split_at_sentences()` function had a bug where adding a 50-character overlap tail to the start of a new sub-chunk could push the combined length above 600 characters when the first sentence of the new sub-chunk was already near-max. I identified this from the output showing `max length: 668 chars` and added a guard that skips the tail if `tail + sentence > max_size`. I also changed the overlap behavior to apply only within long-paragraph splits, not across independent paragraph boundaries.

**Instance 2**

- *What I gave the AI:* The Retrieval Approach section of planning.md, the output format of `load_documents()` (list of dicts with `text`, `source`, `filename`, `chunk_index`), and a description of the ChromaDB Python client API.
- *What it produced:* A `build_vector_store()` function that embedded all chunks in a single batch and upserted them into ChromaDB, and a `retrieve()` function that embedded the query and returned top-k results with metadata.
- *What I changed or overrode:* The generated code called `chromadb.Client()` (in-memory only). I changed it to `chromadb.PersistentClient(path="chroma_db")` so embeddings survive between runs and the app does not re-embed 485 chunks on every startup. I also added a count check (`collection.count() == len(chunks)`) to skip re-embedding if the collection is already fully populated, which reduced app startup time from ~5 seconds to under 1 second.
