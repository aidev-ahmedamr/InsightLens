import requests
import gradio as gr
import html
import re


# ============================================================
# INSIGHTLENS CONFIGURATION
# ============================================================

NGROK_URL = "xxxxxxxx"
API_KEY = "xxxxxxxx"


# ============================================================
# BACKEND
# ============================================================

def call_backend(topic):

    if not topic or not topic.strip():
        return {
            "status": "error",
            "message": "Please enter a topic first."
        }

    url = NGROK_URL.rstrip("/") + "/intelligence"

    try:

        response = requests.post(
            url,
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "topic": topic.strip()
            },
            timeout=300
        )

        if response.status_code != 200:

            try:
                data = response.json()
                message = data.get(
                    "detail",
                    f"Backend error: {response.status_code}"
                )
            except:
                message = (
                    f"Backend error: {response.status_code}"
                )

            return {
                "status": "error",
                "message": message
            }

        return response.json()

    except requests.exceptions.Timeout:

        return {
            "status": "error",
            "message": (
                "The request timed out. "
                "Make sure the Kaggle notebook is still running."
            )
        }

    except requests.exceptions.ConnectionError:

        return {
            "status": "error",
            "message": (
                "Could not connect to the AI backend. "
                "Check that Kaggle and ngrok are still running."
            )
        }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }


# ============================================================
# TEXT PARSING
# ============================================================

def extract_section(text, section_name, next_sections):

    if not text:
        return ""

    if next_sections:

        pattern = (
            rf"{re.escape(section_name)}\s*:?\s*"
            rf"(.*?)"
            rf"(?=\n(?:{'|'.join(map(re.escape, next_sections))})\s*:|\Z)"
        )

    else:

        pattern = (
            rf"{re.escape(section_name)}\s*:?\s*(.*)"
        )

    match = re.search(
        pattern,
        text,
        flags=re.IGNORECASE | re.DOTALL
    )

    if match:
        return match.group(1).strip()

    return ""


def markdown_to_html(text):

    if not text:
        return """
        <span class="empty-text">
            No information available.
        </span>
        """

    escaped = html.escape(str(text))

    escaped = re.sub(
        r"\*\*(.*?)\*\*",
        r"<strong>\1</strong>",
        escaped
    )

    lines = escaped.splitlines()

    output = []
    in_list = False

    for line in lines:

        line = line.strip()

        if line.startswith("- "):

            if not in_list:
                output.append("<ul>")
                in_list = True

            output.append(
                f"<li>{line[2:]}</li>"
            )

        elif line:

            if in_list:
                output.append("</ul>")
                in_list = False

            output.append(
                f"<p>{line}</p>"
            )

    if in_list:
        output.append("</ul>")

    return "\n".join(output)


# ============================================================
# EVIDENCE
# ============================================================

def build_evidence_html(evidence):

    if not evidence:

        return """
        <div class="empty-box">
            No evidence was retrieved.
        </div>
        """

    cards = []

    for item in evidence:

        rank = item.get("rank", "-")
        document_id = item.get("document_id", "-")
        similarity = item.get("similarity", 0)
        category = item.get("category", "-")
        text = item.get("text", "")

        try:
            similarity_value = float(similarity)
        except:
            similarity_value = 0.0

        percentage = max(
            0,
            min(
                100,
                similarity_value * 100
            )
        )

        cards.append(
            f"""
            <div class="evidence-card">

                <div class="evidence-top">

                    <div>
                        <div class="evidence-label">
                            EVIDENCE {rank}
                        </div>

                        <div class="document-id">
                            Document #{html.escape(str(document_id))}
                        </div>
                    </div>

                    <div class="score-pill">
                        {similarity_value:.3f}
                    </div>

                </div>

                <div class="score-track">
                    <div
                        class="score-progress"
                        style="width:{percentage:.1f}%"
                    ></div>
                </div>

                <div class="evidence-info">

                    <span>
                        Category
                        <b>{html.escape(str(category))}</b>
                    </span>

                    <span>
                        Similarity
                        <b>{similarity_value:.3f}</b>
                    </span>

                </div>

                <div class="evidence-content">
                    {html.escape(str(text))}
                </div>

            </div>
            """
        )

    return "".join(cards)


# ============================================================
# MAIN ANALYSIS
# ============================================================

def analyze_topic(topic):

    result = call_backend(topic)

    if result.get("status") != "success":

        error_message = result.get(
            "message",
            "Something went wrong."
        )

        return (
            f"""
            <div class="error-box">

                <div class="error-title">
                    Connection Error
                </div>

                <div class="error-text">
                    {html.escape(str(error_message))}
                </div>

            </div>
            """,
            "",
            "",
            ""
        )

    brief = result.get(
        "brief",
        ""
    )

    evidence = result.get(
        "evidence",
        []
    )

    sections = [
        "EXECUTIVE SUMMARY",
        "KEY FINDINGS",
        "SUPPORTING SIGNALS",
        "CONFLICTING OR DIFFERENT SIGNALS",
        "RISKS / OPPORTUNITIES",
        "CONFIDENCE",
        "CONFIDENCE REASON",
        "EVIDENCE USED"
    ]

    executive_summary = extract_section(
        brief,
        "EXECUTIVE SUMMARY",
        sections[1:]
    )

    key_findings = extract_section(
        brief,
        "KEY FINDINGS",
        sections[2:]
    )

    supporting_signals = extract_section(
        brief,
        "SUPPORTING SIGNALS",
        sections[3:]
    )

    conflicting_signals = extract_section(
        brief,
        "CONFLICTING OR DIFFERENT SIGNALS",
        sections[4:]
    )

    risks = extract_section(
        brief,
        "RISKS / OPPORTUNITIES",
        sections[5:]
    )

    confidence = extract_section(
        brief,
        "CONFIDENCE",
        sections[6:]
    )

    confidence_reason = extract_section(
        brief,
        "CONFIDENCE REASON",
        sections[7:]
    )

    evidence_used = extract_section(
        brief,
        "EVIDENCE USED",
        []
    )

    confidence_clean = confidence.strip().upper()

    if "HIGH" in confidence_clean:
        confidence_class = "high"

    elif "MEDIUM" in confidence_clean:
        confidence_class = "medium"

    else:
        confidence_class = "low"

    # --------------------------------------------------------
    # Statistics
    # --------------------------------------------------------

    similarities = []

    for item in evidence:

        try:
            similarities.append(
                float(item.get("similarity", 0))
            )
        except:
            pass

    if similarities:

        average_similarity = (
            sum(similarities) /
            len(similarities)
        )

        average_similarity = (
            f"{average_similarity:.3f}"
        )

    else:
        average_similarity = "—"

    evidence_count = len(evidence)

    stats_html = f"""

    <div class="stats-grid">

        <div class="stat">
            <div class="stat-number">
                {evidence_count}
            </div>

            <div class="stat-name">
                Evidence Sources
            </div>
        </div>


        <div class="stat">
            <div class="stat-number">
                {average_similarity}
            </div>

            <div class="stat-name">
                Avg. Similarity
            </div>
        </div>


        <div class="stat">
            <div class="stat-number">
                RAG
            </div>

            <div class="stat-name">
                Retrieval
            </div>
        </div>


        <div class="stat">
            <div class="stat-number">
                LLM
            </div>

            <div class="stat-name">
                Intelligence
            </div>
        </div>

    </div>

    """

    # --------------------------------------------------------
    # Intelligence Brief
    # --------------------------------------------------------

    brief_html = f"""

    <div class="result-wrapper">

        <div class="result-card featured">

            <div class="result-heading">
                <span class="heading-dot"></span>
                Executive Summary
            </div>

            <div class="summary">
                {markdown_to_html(executive_summary)}
            </div>

        </div>


        <div class="result-card">

            <div class="result-heading">
                Key Findings
            </div>

            <div class="result-content">
                {markdown_to_html(key_findings)}
            </div>

        </div>


        <div class="result-card">

            <div class="result-heading">
                Supporting Signals
            </div>

            <div class="result-content">
                {markdown_to_html(supporting_signals)}
            </div>

        </div>


        <div class="result-card">

            <div class="result-heading">
                Conflicting / Different Signals
            </div>

            <div class="result-content">
                {markdown_to_html(conflicting_signals)}
            </div>

        </div>


        <div class="result-card">

            <div class="result-heading">
                Risks / Opportunities
            </div>

            <div class="result-content">
                {markdown_to_html(risks)}
            </div>

        </div>


        <div class="confidence-panel">

            <div>

                <div class="small-label">
                    CONFIDENCE
                </div>

                <div class="confidence {confidence_class}">
                    {html.escape(
                        confidence_clean or "UNKNOWN"
                    )}
                </div>

            </div>

            <div class="confidence-reason">
                {markdown_to_html(confidence_reason)}
            </div>

        </div>


        <div class="result-card">

            <div class="result-heading">
                Evidence Used
            </div>

            <div class="result-content">
                {markdown_to_html(evidence_used)}
            </div>

        </div>

    </div>

    """

    evidence_html = build_evidence_html(
        evidence
    )

    return (
        brief_html,
        evidence_html,
        stats_html,
        "Analysis completed successfully."
    )


# ============================================================
# CSS
# ============================================================

CSS = """

/* ============================================================
   MAIN BACKGROUND
   ============================================================ */

html,
body {

    margin: 0;
    padding: 0;

    background: #090b12 !important;

}

.gradio-container {

    max-width: none !important;

    min-height: 100vh;

    margin: 0 !important;

    padding: 0 !important;

    background:
        radial-gradient(
            circle at 10% 10%,
            rgba(255, 100, 55, 0.75),
            transparent 24%
        ),
        radial-gradient(
            circle at 85% 5%,
            rgba(80, 160, 255, 0.75),
            transparent 25%
        ),
        radial-gradient(
            circle at 55% 35%,
            rgba(170, 70, 230, 0.60),
            transparent 28%
        ),
        radial-gradient(
            circle at 15% 75%,
            rgba(255, 150, 55, 0.50),
            transparent 28%
        ),
        linear-gradient(
            135deg,
            #13152b,
            #090b13
        ) !important;

}


/* ============================================================
   MAIN APP
   ============================================================ */

.app-shell {

    max-width: 1250px;

    min-height: 100vh;

    margin: auto;

    padding: 35px 45px 60px;

}


/* ============================================================
   NAVBAR
   ============================================================ */

.navbar {

    height: 58px;

    display: flex;

    align-items: center;

    justify-content: space-between;

    padding: 0 25px;

    margin-bottom: 35px;

    border-radius: 18px;

    background:
        rgba(255,255,255,0.10);

    backdrop-filter: blur(25px);

    -webkit-backdrop-filter: blur(25px);

    border: 1px solid
        rgba(255,255,255,0.16);

}

.logo {

    font-size: 18px;

    font-weight: 800;

    letter-spacing: -0.5px;

    color: white;

}

.logo span {

    opacity: 0.55;

    font-weight: 500;

}

.nav-links {

    display: flex;

    gap: 28px;

    align-items: center;

}

.nav-link {

    color:
        rgba(255,255,255,0.75);

    font-size: 13px;

    font-weight: 500;

}


/* ============================================================
   HERO
   ============================================================ */

.hero {

    min-height: 470px;

    display: flex;

    flex-direction: column;

    justify-content: center;

    align-items: center;

    text-align: center;

    padding: 40px 20px;

}

.hero-kicker {

    padding: 8px 16px;

    border-radius: 100px;

    background:
        rgba(255,255,255,0.15);

    border:
        1px solid
        rgba(255,255,255,0.20);

    color:
        rgba(255,255,255,0.90);

    font-size: 11px;

    font-weight: 700;

    letter-spacing: 1.5px;

    backdrop-filter: blur(15px);

    margin-bottom: 22px;

}

.hero-title {

    max-width: 1000px;

    margin: 0;

    color: white;

    font-size: clamp(
        48px,
        7vw,
        86px
    );

    line-height: 0.98;

    font-weight: 800;

    letter-spacing: -4px;

    text-shadow:
        0 8px 40px
        rgba(0,0,0,0.20);

}

.hero-description {

    max-width: 720px;

    margin-top: 25px;

    color:
        rgba(255,255,255,0.76);

    font-size: 17px;

    line-height: 1.7;

}


/* ============================================================
   TAGS
   ============================================================ */

.tag-row {

    display: flex;

    justify-content: center;

    flex-wrap: wrap;

    gap: 10px;

    margin-top: 27px;

}

.tag {

    padding: 10px 17px;

    border-radius: 100px;

    background: white;

    color: #222534;

    font-size: 12px;

    font-weight: 700;

    box-shadow:
        0 8px 30px
        rgba(0,0,0,0.13);

}


/* ============================================================
   INPUT AREA
   ============================================================ */

.input-wrapper {

    max-width: 900px;

    margin: 0 auto 50px;

    padding: 9px;

    border-radius: 25px;

    background:
        rgba(255,255,255,0.12);

    border:
        1px solid
        rgba(255,255,255,0.18);

    backdrop-filter: blur(25px);

    -webkit-backdrop-filter: blur(25px);

    box-shadow:
        0 25px 70px
        rgba(0,0,0,0.20);

}

.input-inner {

    padding: 23px;

    border-radius: 19px;

    background:
        rgba(8,10,18,0.68);

}

.input-title {

    color: white;

    font-size: 13px;

    font-weight: 800;

    letter-spacing: 1px;

    margin-bottom: 12px;

}

textarea {

    min-height: 105px !important;

    border-radius: 16px !important;

    border:
        1px solid
        rgba(255,255,255,0.10) !important;

    background:
        rgba(255,255,255,0.055) !important;

    color: white !important;

    font-size: 16px !important;

    line-height: 1.6 !important;

}

textarea::placeholder {

    color:
        rgba(255,255,255,0.38) !important;

}


/* ============================================================
   BUTTON
   ============================================================ */

.generate-btn {

    margin-top: 13px;

    min-height: 53px;

    border-radius: 14px !important;

    border: none !important;

    background:
        white !important;

    color:
        #161824 !important;

    font-size: 14px !important;

    font-weight: 800 !important;

    transition:
        transform 0.2s,
        box-shadow 0.2s;

}

.generate-btn:hover {

    transform:
        translateY(-2px);

    box-shadow:
        0 12px 35px
        rgba(255,255,255,0.20);

}


/* ============================================================
   SECTION TITLE
   ============================================================ */

.section-title {

    color: white;

    font-size: 32px;

    font-weight: 800;

    letter-spacing: -1.5px;

    margin:
        40px 0 20px;

}


/* ============================================================
   STATS
   ============================================================ */

.stats-grid {

    display: grid;

    grid-template-columns:
        repeat(4, 1fr);

    gap: 13px;

    margin:
        15px 0 30px;

}

.stat {

    padding: 20px;

    border-radius: 19px;

    background:
        rgba(255,255,255,0.09);

    border:
        1px solid
        rgba(255,255,255,0.11);

    backdrop-filter: blur(20px);

    text-align: center;

}

.stat-number {

    color: white;

    font-size: 25px;

    font-weight: 800;

}

.stat-name {

    color:
        rgba(255,255,255,0.50);

    font-size: 11px;

    margin-top: 5px;

}


/* ============================================================
   RESULT CARDS
   ============================================================ */

.result-wrapper {

    display: flex;

    flex-direction: column;

    gap: 14px;

}

.result-card {

    padding: 27px;

    border-radius: 22px;

    background:
        rgba(12,15,25,0.72);

    border:
        1px solid
        rgba(255,255,255,0.10);

    backdrop-filter: blur(25px);

    -webkit-backdrop-filter: blur(25px);

}

.result-card.featured {

    background:
        linear-gradient(
            135deg,
            rgba(255,255,255,0.16),
            rgba(255,255,255,0.06)
        );

}

.result-heading {

    display: flex;

    align-items: center;

    gap: 9px;

    color: white;

    font-size: 14px;

    font-weight: 800;

    margin-bottom: 15px;

}

.heading-dot {

    width: 7px;

    height: 7px;

    border-radius: 50%;

    background: white;

}

.summary,
.result-content {

    color:
        rgba(255,255,255,0.72);

    font-size: 15px;

    line-height: 1.8;

}

.summary p,
.result-content p {

    margin-top: 0;

}

.result-content ul,
.summary ul {

    padding-left: 22px;

}

.result-content li,
.summary li {

    margin-bottom: 8px;

}

.empty-text {

    color:
        rgba(255,255,255,0.35);

}


/* ============================================================
   CONFIDENCE
   ============================================================ */

.confidence-panel {

    padding: 25px;

    border-radius: 21px;

    background:
        rgba(255,255,255,0.08);

    border:
        1px solid
        rgba(255,255,255,0.11);

    display: flex;

    justify-content: space-between;

    gap: 30px;

    align-items: center;

}

.small-label {

    color:
        rgba(255,255,255,0.40);

    font-size: 10px;

    letter-spacing: 1.4px;

    font-weight: 800;

    margin-bottom: 8px;

}

.confidence {

    display: inline-block;

    padding: 8px 15px;

    border-radius: 100px;

    font-size: 12px;

    font-weight: 800;

}

.confidence.high {

    background:
        rgba(80,220,150,0.16);

    color:
        #78e8ae;

}

.confidence.medium {

    background:
        rgba(255,200,70,0.16);

    color:
        #ffd76b;

}

.confidence.low {

    background:
        rgba(255,90,90,0.16);

    color:
        #ff8585;

}

.confidence-reason {

    max-width: 650px;

    color:
        rgba(255,255,255,0.55);

    font-size: 13px;

    line-height: 1.6;

}


/* ============================================================
   EVIDENCE
   ============================================================ */

.evidence-card {

    margin-bottom: 14px;

    padding: 23px;

    border-radius: 21px;

    background:
        rgba(10,13,22,0.72);

    border:
        1px solid
        rgba(255,255,255,0.09);

    backdrop-filter: blur(20px);

}

.evidence-top {

    display: flex;

    justify-content: space-between;

    align-items: center;

}

.evidence-label {

    color: white;

    font-size: 11px;

    font-weight: 800;

    letter-spacing: 1.2px;

}

.document-id {

    color:
        rgba(255,255,255,0.38);

    font-size: 11px;

    margin-top: 5px;

}

.score-pill {

    padding: 7px 11px;

    border-radius: 9px;

    background:
        rgba(255,255,255,0.10);

    color: white;

    font-size: 12px;

    font-weight: 800;

}

.score-track {

    height: 4px;

    margin:
        18px 0 15px;

    border-radius: 100px;

    background:
        rgba(255,255,255,0.07);

    overflow: hidden;

}

.score-progress {

    height: 100%;

    border-radius: 100px;

    background:
        linear-gradient(
            90deg,
            #ff6c4d,
            #a86cff,
            #43c9ff
        );

}

.evidence-info {

    display: flex;

    gap: 25px;

    color:
        rgba(255,255,255,0.38);

    font-size: 11px;

    margin-bottom: 15px;

}

.evidence-info b {

    color:
        rgba(255,255,255,0.72);

    margin-left: 5px;

}

.evidence-content {

    color:
        rgba(255,255,255,0.63);

    font-size: 13px;

    line-height: 1.7;

}


/* ============================================================
   ERROR
   ============================================================ */

.error-box {

    padding: 25px;

    margin-top: 20px;

    border-radius: 20px;

    background:
        rgba(255,70,70,0.10);

    border:
        1px solid
        rgba(255,100,100,0.18);

}

.error-title {

    color:
        #ff8a8a;

    font-weight: 800;

    margin-bottom: 8px;

}

.error-text {

    color:
        rgba(255,255,255,0.60);

    font-size: 13px;

}


/* ============================================================
   FOOTER
   ============================================================ */

.footer {

    text-align: center;

    padding: 60px 0 20px;

    color:
        rgba(255,255,255,0.35);

    font-size: 11px;

}


/* ============================================================
   RESPONSIVE
   ============================================================ */

@media (max-width: 800px) {

    .app-shell {

        padding:
            20px 18px 40px;

    }

    .navbar {

        padding:
            0 17px;

    }

    .nav-links {

        gap: 12px;

    }

    .nav-link {

        font-size: 11px;

    }

    .hero-title {

        font-size: 48px;

        letter-spacing: -2px;

    }

    .stats-grid {

        grid-template-columns:
            repeat(2, 1fr);

    }

    .confidence-panel {

        flex-direction: column;

        align-items: flex-start;

    }

}


/* ============================================================
   REMOVE DEFAULT GRADIO EXCESS
   ============================================================ */

footer {

    display: none !important;

}

"""


# ============================================================
# GRADIO APP
# ============================================================

with gr.Blocks(
    title="InsightLens — Evidence-Backed AI Intelligence",
    css=CSS
) as demo:

    # --------------------------------------------------------
    # APP SHELL
    # --------------------------------------------------------

    gr.HTML(
        """
        <div class="app-shell">

            <div class="navbar">

                <div class="logo">
                    InsightLens
                    <span>AI</span>
                </div>

                <div class="nav-links">

                    <div class="nav-link">
                        Home
                    </div>

                    <div class="nav-link">
                        RAG
                    </div>

                    <div class="nav-link">
                        Evidence
                    </div>

                    <div class="nav-link">
                        About
                    </div>

                </div>

            </div>


            <div class="hero">

                <div class="hero-kicker">
                    EVIDENCE-BACKED AI INTELLIGENCE
                </div>

                <div class="hero-title">
                    Turn Information<br>
                    Into Intelligence.
                </div>

                <div class="hero-description">
                    InsightLens analyzes your topic using semantic
                    retrieval, FAISS and a quantized language model
                    to create a structured, evidence-grounded
                    intelligence brief.
                </div>

                <div class="tag-row">

                    <div class="tag">
                        RAG
                    </div>

                    <div class="tag">
                        FAISS
                    </div>

                    <div class="tag">
                        AI-Driven Analysis
                    </div>

                    <div class="tag">
                        Evidence Retrieval
                    </div>

                </div>

            </div>

        </div>
        """
    )


    # --------------------------------------------------------
    # INPUT
    # --------------------------------------------------------

    with gr.Column(
        elem_classes=["input-wrapper"]
    ):

        with gr.Column(
            elem_classes=["input-inner"]
        ):

            gr.HTML(
                """
                <div class="input-title">
                    WHAT DO YOU WANT TO ANALYZE?
                </div>
                """
            )

            topic_input = gr.Textbox(
                show_label=False,
                lines=4,
                placeholder=(
                    "Example: Artificial intelligence is "
                    "transforming the technology industry."
                )
            )

            analyze_button = gr.Button(
                "Generate Intelligence Brief  →",
                elem_classes=["generate-btn"]
            )


    # --------------------------------------------------------
    # OUTPUT
    # --------------------------------------------------------

    gr.HTML(
        """
        <div class="section-title">
            Intelligence Brief
        </div>
        """
    )

    stats_output = gr.HTML()

    brief_output = gr.HTML()


    gr.HTML(
        """
        <div class="section-title">
            Retrieved Evidence
        </div>
        """
    )

    evidence_output = gr.HTML()


    status_output = gr.Markdown()


    gr.HTML(
        """
        <div class="footer">
            InsightLens · Evidence-Backed AI Intelligence
            <br>
            RAG · FAISS · Mistral Nemo · FastAPI · Gradio
        </div>
        """
    )


    # --------------------------------------------------------
    # EVENTS
    # --------------------------------------------------------

    analyze_button.click(
        fn=analyze_topic,
        inputs=topic_input,
        outputs=[
            brief_output,
            evidence_output,
            stats_output,
            status_output
        ]
    )

    topic_input.submit(
        fn=analyze_topic,
        inputs=topic_input,
        outputs=[
            brief_output,
            evidence_output,
            stats_output,
            status_output
        ]
    )


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    print("=" * 65)
    print("INSIGHTLENS")
    print("Evidence-Backed AI Intelligence")
    print("=" * 65)

    print()
    print("Backend:")
    print(NGROK_URL)

    print()
    print("Starting Gradio...")
    print()

    demo.launch(
        inbrowser=True,
        show_error=True
    )
