from pathlib import Path
from urllib.parse import quote

import streamlit as st

from src.chatbot import ask_chatbot
from src.rag import (
    DEFAULT_INDEX_PATH,
    format_chunks_for_prompt,
    get_or_build_vector_index,
    retrieve_relevant_chunks,
)


PROJECT_ROOT = Path(__file__).resolve().parent.parent
CV_FILE_NAME = "CV Thiago Braganca.pdf"
CV_PATH = PROJECT_ROOT / "src" / "static" / CV_FILE_NAME
CONTACT_EMAIL = "thiago.braganca.carvalho@gmail.com"
CONTACT_PHONE = "+41 78 825 74 28"
CONTACT_LOCATION = "Dübendorf, Zürich"
CONTACT_BIRTHDATE = "04.10.2001"
LINKEDIN_URL = "https://www.linkedin.com/in/thiago-bragan%C3%A7a-574399203"


SUGGESTED_QUESTIONS = [
    "Tell me about Thiago.",
    "Why is Thiago a good fit for an AI Engineer role?",
    "What healthcare AI experience does Thiago have?",
    "Tell me about the DXC ICD-10 validation project.",
    "Tell me about the iMove project.",
    "What are Thiago's strongest technical skills?",
]


ANSWER_STYLE_OPTIONS = [
    "Recruiter-friendly",
    "Technical detail",
    "STAR interview format",
]

UNANSWERED_ANSWER_PHRASES = [
    "not available in the knowledge base",
    "not available in the provided context",
    "i don't have enough information",
    "i cannot answer based on the available information",
]

TECHNICAL_ERROR_PHRASES = [
    "technical error",
    "api quota",
    "connectivity",
    "configuration",
    "connection",
]


def apply_custom_styles() -> None:
    st.markdown(
        """
        <style>
        :root {
            --primary: #2563EB;
            --dark-accent: #1E40AF;
            --light-background: #F8FAFC;
            --card: #FFFFFF;
            --soft-highlight: #EFF6FF;
            --text: #0F172A;
            --muted: #64748B;
            --line: #E2E8F0;
        }

        .stApp {
            background:
                linear-gradient(180deg, var(--soft-highlight) 0%, var(--light-background) 34%),
                var(--light-background) !important;
            color: var(--text) !important;
        }

        [data-testid="stHeader"] {
            background: rgba(248, 250, 252, 0.96) !important;
            color: var(--text) !important;
        }

        [data-testid="stDecoration"],
        [data-testid="stStatusWidget"] {
            display: none !important;
        }

        [data-testid="stToolbar"] {
            background: transparent !important;
            display: flex !important;
        }

        [data-testid="stAppDeployButton"],
        [data-testid="stMainMenu"] {
            display: none !important;
        }

        [data-testid="stExpandSidebarButton"] {
            align-items: center !important;
            background: var(--card) !important;
            border: 1px solid var(--line) !important;
            border-radius: 8px !important;
            box-shadow: 0 8px 20px rgba(15, 23, 42, 0.12);
            color: var(--primary) !important;
            height: 2.5rem !important;
            justify-content: center !important;
            margin: 0.5rem !important;
            width: 2.5rem !important;
        }

        [data-testid="stExpandSidebarButton"] span,
        [data-testid="stExpandSidebarButton"] svg {
            color: var(--primary) !important;
            fill: var(--primary) !important;
        }

        [data-testid="stSidebarCollapseButton"] {
            opacity: 1 !important;
        }

        [data-testid="stMainBlockContainer"] {
            max-width: 1180px;
            padding-top: 3rem;
            padding-bottom: 7rem;
        }

        [data-testid="stSidebar"] {
            background: var(--text) !important;
            border-right: 1px solid rgba(255, 255, 255, 0.14);
        }

        [data-testid="stSidebar"] * {
            color: var(--card);
        }

        [data-testid="stSidebar"] hr {
            border-color: rgba(255, 255, 255, 0.18);
        }

        h1, h2, h3 {
            color: var(--text);
            letter-spacing: 0;
        }

        p, li, label, span {
            letter-spacing: 0;
        }

        .hero {
            border-bottom: 1px solid var(--line);
            margin-bottom: 1.6rem;
            padding-bottom: 1.4rem;
        }

        .eyebrow {
            color: var(--primary);
            font-size: 0.8rem;
            font-weight: 700;
            letter-spacing: 0.08rem;
            margin-bottom: 0.35rem;
            text-transform: uppercase;
        }

        .hero h1 {
            color: var(--text);
            font-size: 2.75rem;
            line-height: 1.08;
            margin: 0;
        }

        .hero p {
            color: var(--muted);
            font-size: 1.05rem;
            line-height: 1.55;
            margin: 0.8rem 0 0;
            max-width: 820px;
        }

        .trust-strip {
            display: grid;
            gap: 0.75rem;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            margin: 1.2rem 0 1.4rem;
        }

        .trust-item {
            background: var(--card);
            border: 1px solid var(--line);
            border-radius: 8px;
            padding: 0.85rem 1rem;
        }

        .trust-label {
            color: var(--muted);
            font-size: 0.78rem;
            margin-bottom: 0.2rem;
        }

        .trust-value {
            color: var(--text);
            font-size: 0.95rem;
            font-weight: 700;
        }

        .section-title {
            color: var(--text);
            font-size: 1.15rem;
            font-weight: 750;
            margin: 1.4rem 0 0.35rem;
        }

        .section-copy {
            color: var(--muted);
            font-size: 0.92rem;
            margin-bottom: 0.75rem;
        }

        .sidebar-brand {
            border-bottom: 3px solid var(--primary);
            margin-bottom: 1rem;
            padding-bottom: 0.75rem;
        }

        .sidebar-brand h2 {
            color: var(--card);
            font-size: 1.35rem;
            margin: 0;
        }

        .sidebar-brand p,
        .sidebar-note {
            color: rgba(255, 255, 255, 0.76);
            font-size: 0.9rem;
            line-height: 1.5;
            margin: 0.55rem 0 0;
        }

        .sidebar-pill {
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.16);
            border-radius: 999px;
            display: inline-block;
            font-size: 0.78rem;
            margin: 0.2rem 0.25rem 0.2rem 0;
            padding: 0.28rem 0.65rem;
        }

        .sidebar-profile {
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.18);
            border-radius: 8px;
            margin-bottom: 1rem;
            padding: 0.9rem;
        }

        .sidebar-profile h3 {
            color: var(--card);
            font-size: 1.15rem;
            line-height: 1.25;
            margin: 0 0 0.75rem;
        }

        .sidebar-profile-row {
            color: rgba(255, 255, 255, 0.86);
            font-size: 0.88rem;
            line-height: 1.35;
            margin-top: 0.5rem;
            overflow-wrap: anywhere;
        }

        .sidebar-profile-label {
            color: rgba(255, 255, 255, 0.58);
            display: block;
            font-size: 0.72rem;
            font-weight: 700;
            letter-spacing: 0;
            margin-bottom: 0.08rem;
            text-transform: uppercase;
        }

        .quiet-note {
            border-top: 1px solid var(--line);
            color: var(--muted);
            font-size: 0.82rem;
            line-height: 1.5;
            margin-top: 2rem;
            padding-top: 1rem;
        }

        div[data-testid="stButton"] > button {
            background: var(--card);
            border: 1px solid var(--line);
            border-radius: 8px;
            color: var(--text);
            min-height: 2.75rem;
            text-align: left;
            transition: all 140ms ease;
        }

        div[data-testid="stButton"] > button:hover {
            background: var(--soft-highlight);
            border-color: var(--primary);
            color: var(--dark-accent);
            transform: translateY(-1px);
        }

        div[data-testid="stButton"] > button:focus {
            box-shadow: 0 0 0 0.18rem rgba(37, 99, 235, 0.18);
        }

        [data-testid="stSidebar"] div[data-testid="stButton"] > button {
            background: rgba(255, 255, 255, 0.08);
            border-color: rgba(255, 255, 255, 0.24);
            color: var(--card);
            text-align: center;
        }

        [data-testid="stSidebar"] div[data-testid="stButton"] > button:hover {
            background: var(--primary);
            border-color: var(--primary);
        }

        [data-testid="stSidebar"] div[data-testid="stDownloadButton"] > button {
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.24);
            border-radius: 8px;
            color: var(--card);
            min-height: 2.75rem;
            text-align: center;
            transition: all 140ms ease;
            width: 100%;
        }

        [data-testid="stSidebar"] div[data-testid="stDownloadButton"] > button:hover {
            background: var(--primary);
            border-color: var(--primary);
            color: var(--card);
            transform: translateY(-1px);
        }

        [data-testid="stSidebar"] div[data-testid="stLinkButton"] > a {
            align-items: center;
            background: var(--primary);
            border: 1px solid var(--primary);
            border-radius: 8px;
            color: var(--card);
            display: inline-flex;
            justify-content: center;
            min-height: 2.75rem;
            text-decoration: none;
            transition: all 140ms ease;
            width: 100%;
        }

        [data-testid="stSidebar"] div[data-testid="stLinkButton"] > a:hover {
            background: var(--dark-accent);
            border-color: var(--dark-accent);
            color: var(--card);
            transform: translateY(-1px);
        }

        .sidebar-action-link {
            align-items: center;
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.24);
            border-radius: 8px;
            color: var(--card) !important;
            display: inline-flex;
            justify-content: center;
            min-height: 2.75rem;
            text-decoration: none !important;
            transition: all 140ms ease;
            width: 100%;
        }

        .sidebar-action-link:hover {
            background: var(--primary);
            border-color: var(--primary);
            color: var(--card) !important;
            transform: translateY(-1px);
        }

        [data-testid="stChatMessage"] {
            background: var(--card);
            border: 1px solid var(--line);
            border-radius: 8px;
            margin-bottom: 0.8rem;
            padding: 0.35rem;
        }

        [data-testid="stChatMessage"] p,
        [data-testid="stChatMessage"] li,
        [data-testid="stChatMessage"] ol,
        [data-testid="stChatMessage"] ul,
        [data-testid="stChatMessage"] span,
        [data-testid="stChatMessage"] strong {
            color: var(--text) !important;
        }

        [data-testid="stExpander"] summary,
        [data-testid="stExpander"] summary p {
            color: #94A3B8 !important;
        }

        .sources-used,
        .sources-used li {
            color: #94A3B8 !important;
            font-size: 0.84rem;
        }

        [data-testid="stBottom"],
        [data-testid="stBottomBlockContainer"] {
            background: rgba(248, 250, 252, 0.96) !important;
        }

        [data-testid="stChatInput"] {
            max-width: 1180px;
        }

        [data-testid="stChatInput"] > div {
            background: var(--card) !important;
            border: 1px solid var(--line) !important;
            box-shadow: 0 8px 24px rgba(15, 23, 42, 0.08);
        }

        [data-testid="stChatInputTextArea"] {
            background: var(--card) !important;
            border: 0 !important;
            border-radius: 8px !important;
            color: var(--text) !important;
            caret-color: var(--primary) !important;
        }

        [data-testid="stChatInput"] [data-baseweb="base-input"],
        [data-testid="stChatInput"] [data-baseweb="textarea"] {
            background: var(--card) !important;
            border-radius: 8px !important;
        }

        [data-testid="stChatInputTextArea"]::placeholder {
            color: rgba(15, 23, 42, 0.5) !important;
        }

        [data-testid="stChatInputSubmitButton"] {
            background: var(--primary) !important;
            color: var(--card) !important;
        }

        [data-testid="stMarkdownContainer"] a {
            color: var(--primary);
        }

        @media (max-width: 900px) {
            [data-testid="stMainBlockContainer"] {
                padding-top: 1.6rem;
            }

            .hero h1 {
                font-size: 2.05rem;
            }

            .trust-strip {
                grid-template-columns: 1fr;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar() -> str:
    with st.sidebar:
        st.markdown(
            """
            <div class="sidebar-brand">
                <h2>Ask Thiago AI</h2>
                <p>Personal RAG assistant for interview and recruiting conversations.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        render_sidebar_profile()

        answer_style = st.radio("Answer style", ANSWER_STYLE_OPTIONS)

        st.divider()
        render_unanswered_questions_panel()

        st.divider()
        render_cv_download()

        st.divider()
        render_interview_email_button()

        st.divider()
        if st.button("Clear chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

        return answer_style


def initialize_session_state() -> None:
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "unanswered_questions" not in st.session_state:
        st.session_state.unanswered_questions = []


def is_unanswered_answer(answer: str) -> bool:
    normalized_answer = answer.lower()

    if any(phrase in normalized_answer for phrase in TECHNICAL_ERROR_PHRASES):
        return False

    return any(phrase in normalized_answer for phrase in UNANSWERED_ANSWER_PHRASES)


def add_unanswered_question(question: str) -> None:
    cleaned_question = question.strip()
    if not cleaned_question:
        return

    existing_questions = {
        saved_question.strip().lower()
        for saved_question in st.session_state.unanswered_questions
    }
    if cleaned_question.lower() not in existing_questions:
        st.session_state.unanswered_questions.append(cleaned_question)


def format_unanswered_questions() -> str:
    return "\n".join(
        f"{index}. {question}"
        for index, question in enumerate(st.session_state.unanswered_questions, start=1)
    )


def render_unanswered_questions_panel() -> None:
    st.markdown("#### Unanswered questions")
    st.caption(
        "If the assistant cannot answer something from the current knowledge base, "
        "the question is saved here. This helps Thiago improve the assistant after "
        "the interview."
    )

    unanswered_questions = st.session_state.unanswered_questions
    if not unanswered_questions:
        st.caption("No unanswered questions yet.")
        return

    formatted_questions = format_unanswered_questions()
    st.markdown(formatted_questions)
    st.text_area(
        "Copy unanswered questions",
        value=formatted_questions,
        height=130,
        key=f"copy_unanswered_questions_{len(unanswered_questions)}",
    )
    st.download_button(
        "Download unanswered questions",
        data=formatted_questions,
        file_name="unanswered_questions.txt",
        mime="text/plain",
        use_container_width=True,
    )

    if st.button("Clear unanswered questions", use_container_width=True):
        st.session_state.unanswered_questions = []
        st.rerun()


def render_sidebar_profile() -> None:
    st.markdown(
        f"""
        <div class="sidebar-profile">
            <h3>Thiago<br>Bragança Carvalho</h3>
            <div class="sidebar-profile-row">
                <span class="sidebar-profile-label">Born</span>
                {CONTACT_BIRTHDATE}
            </div>
            <div class="sidebar-profile-row">
                <span class="sidebar-profile-label">Location</span>
                {CONTACT_LOCATION}
            </div>
            <div class="sidebar-profile-row">
                <span class="sidebar-profile-label">Email</span>
                {CONTACT_EMAIL}
            </div>
            <div class="sidebar-profile-row">
                <span class="sidebar-profile-label">Phone</span>
                {CONTACT_PHONE}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.link_button("LinkedIn profile", LINKEDIN_URL, use_container_width=True)


def render_cv_download() -> None:
    st.markdown("#### CV")

    if not CV_PATH.exists():
        st.caption("CV file not found on this machine.")
        return

    st.download_button(
        "Download CV",
        data=CV_PATH.read_bytes(),
        file_name=CV_FILE_NAME,
        mime="application/pdf",
        use_container_width=True,
    )


def render_interview_email_button() -> None:
    st.markdown("#### Contact")

    subject = "Interview availability for Thiago Braganca Carvalho"
    body = """Hello Thiago,

I reviewed your profile and would like to schedule an interview with you.

Would one of the following time slots work for you?

- [Option 1: Date, time, timezone]
- [Option 2: Date, time, timezone]
- [Option 3: Date, time, timezone]

Best regards,
[Your name]
"""
    mailto_link = (
        f"mailto:{CONTACT_EMAIL}"
        f"?subject={quote(subject)}"
        f"&body={quote(body)}"
    )

    st.link_button(
        "Suggest interview time",
        mailto_link,
        use_container_width=True,
    )


def render_header() -> None:
    st.markdown(
        """
        <section class="hero">
            <div class="eyebrow">AI Engineering Portfolio Assistant</div>
            <h1>Ask Thiago AI</h1>
            <p>
                A focused interview assistant for quickly understanding Thiago
                Bragança Carvalho's background, healthcare AI experience,
                technical projects, and role fit.
            </p>
        </section>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="trust-strip">
            <div class="trust-item">
                <div class="trust-label">Audience</div>
                <div class="trust-value">Recruiters & interviewers</div>
            </div>
            <div class="trust-item">
                <div class="trust-label">Knowledge source</div>
                <div class="trust-value">Curated personal RAG files</div>
            </div>
            <div class="trust-item">
                <div class="trust-label">Focus</div>
                <div class="trust-value">AI, data, healthcare IT</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_suggested_questions() -> None:
    st.markdown('<div class="section-title">Start with a recruiter question</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-copy">Choose a prompt below, or ask your own question in the chat box.</div>',
        unsafe_allow_html=True,
    )

    cols = st.columns(2)
    for index, question in enumerate(SUGGESTED_QUESTIONS):
        with cols[index % 2]:
            if st.button(question, key=f"suggested_question_{index}", use_container_width=True):
                st.session_state["selected_question"] = question


def render_chat_history() -> None:
    if not st.session_state.messages:
        st.markdown(
            """
            <div class="quiet-note">
            No conversation yet. Suggested questions are designed to surface the
            most relevant interview context first.
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    st.markdown('<div class="section-title">Conversation</div>', unsafe_allow_html=True)
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message["role"] == "assistant":
                render_sources_used(message.get("sources", []))


def render_sources_used(sources: list[dict]) -> None:
    if not sources:
        return

    with st.expander("Sources used"):
        source_items = "\n".join(
            f"<li>{source['source']} - similarity: {source['similarity']:.3f}</li>"
            for source in sources
        )
        st.markdown(
            f'<ul class="sources-used">{source_items}</ul>',
            unsafe_allow_html=True,
        )


def render_footer() -> None:
    st.markdown(
        """
        <div class="quiet-note">
        Built by Thiago Bragança Carvalho as a personal AI Engineering portfolio project.
        The assistant answers from a prepared knowledge base; formal hiring details
        should still be verified directly with Thiago.
        </div>
        """,
        unsafe_allow_html=True,
    )


def sources_from_chunks(chunks: list[dict]) -> list[dict]:
    return [
        {
            "source": chunk["source"],
            "chunk_id": chunk["chunk_id"],
            "similarity": chunk.get("similarity", 0.0),
        }
        for chunk in chunks
    ]


@st.cache_resource
def load_vector_index() -> list[dict]:
    # Streamlit caching prevents rebuilding or reloading embeddings on every rerun.
    return get_or_build_vector_index()


def handle_user_question(user_question: str, vector_index: list[dict], answer_style: str) -> None:
    st.session_state.messages.append({"role": "user", "content": user_question})

    with st.chat_message("user"):
        st.markdown(user_question)

    with st.chat_message("assistant"):
        with st.spinner("Preparing a grounded answer..."):
            try:
                if not vector_index:
                    raise ValueError(
                        "The vector index is empty or unavailable. "
                        "Run `python -m src.build_index` and try again."
                    )

                relevant_chunks = retrieve_relevant_chunks(
                    question=user_question,
                    vector_index=vector_index,
                    top_k=5,
                )
                retrieved_context = format_chunks_for_prompt(relevant_chunks)
                answer = ask_chatbot(
                    question=user_question,
                    retrieved_context=retrieved_context,
                    answer_style=answer_style,
                )
                sources = sources_from_chunks(relevant_chunks)
            except Exception as error:
                answer = (
                    "Sorry, something went wrong while retrieving a grounded answer. "
                    "This may be related to API quota, connectivity, or configuration.\n\n"
                    f"Technical error: `{error}`"
                )
                sources = []

        st.markdown(answer)
        render_sources_used(sources)

    if is_unanswered_answer(answer):
        add_unanswered_question(user_question)

    st.session_state.messages.append(
        {"role": "assistant", "content": answer, "sources": sources}
    )


def run_app() -> None:
    st.set_page_config(page_title="Ask Thiago AI", page_icon="🤖", layout="wide")
    apply_custom_styles()

    initialize_session_state()

    answer_style = render_sidebar()
    saved_index_exists = (PROJECT_ROOT / DEFAULT_INDEX_PATH).exists()

    render_header()

    try:
        with st.spinner("Loading RAG index..."):
            vector_index = load_vector_index()
    except Exception as error:
        vector_index = []
        st.error(
            "The RAG vector index could not be loaded or built. "
            "Run `python -m src.build_index` after confirming your OpenAI API key is configured.\n\n"
            f"Technical error: `{error}`"
        )

    if not saved_index_exists and vector_index:
        st.warning(
            "Saved vector index was not found, so the app built embeddings dynamically. "
            "Run `python -m src.build_index` to save and reuse the index."
        )

    render_suggested_questions()

    selected_question = st.session_state.pop("selected_question", None)
    render_chat_history()

    user_question = st.chat_input("Ask about Thiago's skills, projects, experience, or role fit...")
    if selected_question:
        user_question = selected_question

    if user_question:
        handle_user_question(user_question, vector_index, answer_style)

    render_footer()
