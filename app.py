"""
Gradio web interface for the Unofficial CS Student Guide.

Run with:  python app.py
Then open: http://localhost:7860
"""

import gradio as gr
from query import ask


def handle_query(question: str):
    if not question.strip():
        return "Please enter a question.", ""

    result  = ask(question)
    answer  = result["answer"]
    sources = "\n".join(f"• {s}" for s in result["sources"])
    return answer, sources


with gr.Blocks(title="Unofficial CS Student Guide") as demo:
    gr.Markdown(
        "## Unofficial CS Student Guide\n"
        "Ask questions about CS student experiences: imposter syndrome, "
        "surviving hard courses, internship hunting, grad school, career paths, "
        "and building a portfolio. Answers are drawn only from collected forum "
        "threads and blog posts — no outside knowledge."
    )

    with gr.Row():
        with gr.Column(scale=3):
            question_box = gr.Textbox(
                label="Your question",
                placeholder="e.g. What do people say about surviving a difficult OS course?",
                lines=2,
            )
        with gr.Column(scale=1):
            ask_btn = gr.Button("Ask", variant="primary")

    answer_box = gr.Textbox(label="Answer", lines=10, interactive=False)
    sources_box = gr.Textbox(label="Retrieved from", lines=4, interactive=False)

    ask_btn.click(
        fn=handle_query,
        inputs=question_box,
        outputs=[answer_box, sources_box],
    )
    question_box.submit(
        fn=handle_query,
        inputs=question_box,
        outputs=[answer_box, sources_box],
    )

    gr.Examples(
        examples=[
            ["What do people say about feeling like you're not smart enough for CS?"],
            ["What advice do students give for getting through a difficult OS course?"],
            ["Should I pursue a CS PhD or go straight into industry after my bachelor's?"],
            ["What strategies do students recommend for finishing side projects?"],
            ["How do developers recommend building an online presence while in school?"],
        ],
        inputs=question_box,
    )


if __name__ == "__main__":
    demo.launch()
