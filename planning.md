# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

CS student experiences and career advice shared publicly on Hacker News and dev.to — covering imposter syndrome, navigating difficult courses, internship hunting, open-source contribution, and transitioning from school to industry. This knowledge is hard to find through official channels because university career centers and department websites offer generic guidance, while honest, firsthand student experiences — including failures, self-doubt, and what actually worked — are scattered across community forums and personal blogs.

---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | Hacker News | Ask HN: Maybe I'm just not smart enough? (104 pts) — imposter syndrome, interview failures, community encouragement | https://news.ycombinator.com/item?id=26902219 |
| 2 | Hacker News | Ask HN: Is it possible for someone to not be cut out for software engineering? (183 pts, 186 comments) — aptitude doubts, persistence | https://news.ycombinator.com/item?id=12516611 |
| 3 | Hacker News | Ask HN: How did you become a software engineer? (58 pts, 61 comments) — diverse paths from student to professional | https://news.ycombinator.com/item?id=28457499 |
| 4 | Hacker News | Ask HN: Advice for a frustrated CS student (12 pts) — burnout, motivation, staying on track | https://news.ycombinator.com/item?id=6008850 |
| 5 | Hacker News | Ask HN: What advice do you have for new CS students? (7 pts) — first-year tips from practitioners | https://news.ycombinator.com/item?id=36664044 |
| 6 | Hacker News | Ask HN: Advice for taking difficult CS programming courses? — OS course strategies, study habits | https://news.ycombinator.com/item?id=2749231 |
| 7 | Hacker News | Ask HN: Career advice after graduating undergrad — first job search, navigating the job market | https://news.ycombinator.com/item?id=45131312 |
| 8 | Hacker News | Ask HN: International student in Canada struggling to find a CS internship — resume feedback, internship search | https://news.ycombinator.com/item?id=37374626 |
| 9 | Hacker News | Ask HN: Thoughts on grad school? (CS PhD) — whether grad school is worth it, alternatives | https://news.ycombinator.com/item?id=244100 |
| 10 | dev.to | I'm a 21-Year-Old Student Who Shipped 7 AI Apps and 7 Open Source Libraries — project-building strategy | https://dev.to/iamadhitya/im-a-21-year-old-student-who-shipped-7-ai-apps-and-7-open-source-libraries-heres-the-strategy-3cpi |
| 11 | dev.to | From AI/ML Student to GenAI Engineer: My 6-Month Learning Plan for 2026 — career transition roadmap | https://dev.to/procoder_45/from-aiml-student-to-genai-engineer-my-6-month-learning-plan-for-2026-298e |
| 12 | dev.to | GSoC 2026 Week 1 — What Happens When a Student Clicks "Open Assignment"? — open-source contribution experience | https://dev.to/magic-peach/gsoc-2026-week-1-what-happens-when-a-student-clicks-open-assignment-1jk4 |
| 13 | dev.to | Why You Should Build an Online Presence as a Developer — personal branding for students | https://dev.to/kislay/why-you-should-build-an-online-presence-as-a-developer-3j95 |

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:**

**Overlap:**

**Reasoning:**

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:**

**Top-k:**

**Production tradeoff reflection:**

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | | |
| 2 | | |
| 3 | | |
| 4 | | |
| 5 | | |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1.

2.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:**

**Milestone 4 — Embedding and retrieval:**

**Milestone 5 — Generation and interface:**
