import base64
import textwrap
import uuid

import requests
import streamlit as st

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from pydantic import ValidationError

from models.schemas import ProjectBlueprint
from rag.retrieve import retrieve_context
from utils.markdown_export import generate_markdown

load_dotenv()

# ==============================
# LLM
# ==============================

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
)

# ==============================
# Page Config
# ==============================

st.set_page_config(
    page_title="AI Project Architect",
    page_icon="🏗️",
    layout="wide",
)

st.title("🏗️ AI Project Architect")

st.write(
    "Turn your project idea into a complete technical blueprint."
)

# ==============================
# Helper: render a Mermaid diagram reliably
# ==============================

def render_mermaid(diagram_code: str):
    """Render a Mermaid diagram as a static image via the mermaid.ink API.

    This avoids all client-side JS / iframe timing issues that make
    in-browser Mermaid rendering unreliable inside Streamlit components
    (blocked CDN requests, module-script timing, blank canvases, etc).
    mermaid.ink renders the diagram server-side and returns a PNG, which
    we just display with st.image().
    """
    diagram_code = textwrap.dedent(diagram_code).strip()
    encoded = base64.urlsafe_b64encode(diagram_code.encode("utf8")).decode("ascii")
    url = f"https://mermaid.ink/img/{encoded}?type=png&bgColor=ffffff"

    response = requests.get(url, timeout=15)
    if response.status_code != 200 or not response.content:
        raise RuntimeError(f"mermaid.ink returned status {response.status_code}")

    st.image(response.content, width=500)


# ==============================
# User Inputs
# ==============================

project_idea = st.text_area(
    "Describe your project idea",
    placeholder="Example: I want to build an AI system that detects fake news..."
)

project_type = st.selectbox(
    "Project Type",
    [
        "AI / Machine Learning",
        "Generative AI",
        "Web Application",
        "Mobile Application",
        "Data Science",
        "Other",
    ],
)

target_users = st.text_input(
    "Who will use this project?"
)

constraints = st.text_area(
    "Project Constraints",
    placeholder="Example: Limited budget, 3 months, small team..."
)

# ==============================
# Generate Blueprint
# ==============================

if st.button("🚀 Architect My Project"):

    if not project_idea.strip():
        st.warning("Please enter a project idea.")
        st.stop()

    # Retrieve documentation
    docs = retrieve_context(project_idea, k=8)

    context = "\n\n".join(
        [
            f"Source: {doc.metadata.get('source')}\n{doc.page_content}"
            for doc in docs
        ]
    )

    SYSTEM_PROMPT = f"""
        You are a Principal Software Architect, Senior AI Engineer,
        Cloud Solutions Architect, DevOps Engineer, Database Architect,
        and Technical Product Manager.

        Your task is to design a COMPLETE production-ready software architecture
        for the user's project.

        Return ONLY valid JSON.

        The JSON MUST exactly match the ProjectBlueprint Pydantic schema.

        ==================================================
        STRICT RULES
        ==================================================

        - Return ONLY valid JSON.
        - Do NOT wrap JSON inside markdown.
        - Do NOT explain your reasoning.
        - Do NOT add comments.
        - Do NOT create extra fields.
        - Populate EVERY field.
        - Never leave any field empty.
        - Use realistic production-ready technologies.
        - Prefer scalable, maintainable, and secure architectures.
        - Use industry best practices.

        ==================================================
        PROJECTBLUEPRINT SCHEMA
        ==================================================

        The JSON MUST contain EXACTLY these fields:

        basic_info
        functional_requirements
        non_functional_requirements
        architecture
        components
        data_flow
        technology_stack
        database_type
        database_tables
        apis
        folder_structure
        roadmap
        risks
        future_features

        ==================================================
        FIELD REQUIREMENTS
        ==================================================

        basic_info contains:

        - project_name
        - overview
        - project_type
        - target_users
        - estimated_complexity

        --------------------------------------------------

        architecture contains:

        - pattern
        - reason
        - mermaid_diagram

        The mermaid_diagram field MUST contain ONLY valid Mermaid Flowchart syntax.

        Example:

        flowchart TD
        A[User] --> B[Frontend]
        B --> C[FastAPI Backend]
        C --> D[(PostgreSQL)]
        C --> E[Vector Database]
        E --> F[LLM]

        Do NOT wrap Mermaid inside markdown.

        Do NOT leave mermaid_diagram empty.

        --------------------------------------------------

        components

        Return a list of major software components.

        Each component contains:

        - name
        - purpose
        - technologies

        --------------------------------------------------

        technology_stack

        Each item contains:

        - category
        - name
        - reason

        Explain WHY each technology is selected.

        --------------------------------------------------

        database_tables

        Each table contains:

        - name
        - fields

        Fields should be realistic.

        --------------------------------------------------

        apis

        Each API contains:

        - method
        - endpoint
        - description

        Use realistic REST endpoints.

        --------------------------------------------------

        folder_structure

        IMPORTANT:

        folder_structure MUST be a SINGLE MULTILINE STRING.

        DO NOT return a JSON object.

        Example:

        project/
        ├── app/
        │   ├── api/
        │   ├── services/
        │   ├── models/
        │   └── main.py
        ├── data/
        ├── tests/
        ├── requirements.txt
        └── README.md

        Return ONLY the folder tree as text.

        --------------------------------------------------

        roadmap

        Return multiple implementation phases.

        Each phase contains:

        - phase
        - duration
        - tasks

        --------------------------------------------------

        risks

        Each risk contains:

        - risk
        - mitigation

        --------------------------------------------------

        future_features

        IMPORTANT:

        future_features MUST be an array of STRINGS.

        Correct:

        [
        "Multi-language support",
        "LinkedIn integration",
        "Real-time analytics",
        "Role-based dashboards"
        ]

        Incorrect:

        [
        {{
        "feature":"LinkedIn Integration",
        "description":"..."
        }}
        ]

        ==================================================
        ARCHITECTURE GUIDELINES
        ==================================================

        Select the architecture pattern that best fits the project.

        Possible choices include:

        - Layered Architecture
        - Clean Architecture
        - Microservices
        - Event Driven
        - Serverless
        - Modular Monolith
        - MVC

        Explain why it is appropriate.

        ==================================================
        TECHNOLOGY GUIDELINES
        ==================================================

        Recommend production-ready technologies.

        Examples:

        Frontend
        - React
        - Next.js
        - Flutter
        - Streamlit

        Backend
        - FastAPI
        - Django
        - Flask
        - Node.js

        Databases
        - PostgreSQL
        - MySQL
        - MongoDB

        Vector Database
        - FAISS
        - Chroma
        - Pinecone
        - PGVector

        Caching
        - Redis

        Authentication
        - JWT
        - OAuth2
        - Firebase Authentication

        Cloud
        - AWS
        - Azure
        - Google Cloud

        Containers
        - Docker

        CI/CD
        - GitHub Actions

        Monitoring
        - Prometheus
        - Grafana

        ==================================================
        REFERENCE DOCUMENTATION (RAG)
        ==================================================

        Use the following retrieved documentation as your primary technical reference whenever applicable.

        {context}

        If the documentation contains:

        - Best practices
        - API usage
        - Folder structures
        - Deployment recommendations
        - Configuration guidance
        - Database recommendations
        - Framework conventions

        then follow those recommendations.

        If the documentation does not contain the required information,
        use your own professional software engineering knowledge.

        Never invent documentation that is not present.

        ==================================================
        FINAL GOAL
        ==================================================

        Generate a complete production-ready software architecture blueprint.

        The response MUST strictly match the ProjectBlueprint schema.

        Return ONLY valid JSON.
        """
    USER_PROMPT = f"""
    Design a complete software architecture for the following project.

    Project Idea:
    {project_idea}

    Project Type:
    {project_type}

    Target Users:
    {target_users}

    Constraints:
    {constraints}

    Generate a complete ProjectBlueprint JSON.
    """

    with st.spinner("🏗️ Designing your architecture..."):

        try:
            structured_llm = llm.with_structured_output(ProjectBlueprint)

            blueprint = structured_llm.invoke(
                [
                    ("system", SYSTEM_PROMPT),
                    ("human", USER_PROMPT),
                ]
            )

            # Keep the blueprint around across reruns (e.g. tab clicks)
            st.session_state["blueprint"] = blueprint
            st.session_state["docs"] = docs

        except ValidationError as e:
            st.error("Schema Validation Error")
            st.exception(e)
            st.stop()

        except Exception as e:
            st.error("Architecture generation failed.")
            st.exception(e)
            st.stop()

# ==============================
# Display Blueprint (if one has been generated)
# ==============================

if "blueprint" in st.session_state:

    blueprint = st.session_state["blueprint"]
    docs = st.session_state.get("docs", [])

    # ==========================================================
    # Header
    # ==========================================================

    st.divider()
    st.title(f" {blueprint.basic_info.project_name}")
    st.info(blueprint.basic_info.overview)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Project Type", blueprint.basic_info.project_type)

    with col2:
        st.metric("Complexity", blueprint.basic_info.estimated_complexity)

    with col3:
        st.metric("Target Users", blueprint.basic_info.target_users)

    st.divider()

    # ==========================================================
    # Tabs
    # ==========================================================

    (
        overview_tab,
        architecture_tab,
        components_tab,
        tech_tab,
        database_tab,
        api_tab,
        roadmap_tab,
        risks_tab,
        future_tab,
    ) = st.tabs(
        [
            " Requirements",
            " Architecture",
            " Components",
            " Tech Stack",
            " Database",
            " APIs",
            " Roadmap",
            " Risks",
            " Future",
        ]
    )

    # ==========================================================
    # Requirements
    # ==========================================================

    with overview_tab:
        st.subheader("Functional Requirements")

        for req in blueprint.functional_requirements:
            st.markdown(f"### ✅ {req.title}")
            st.write(req.description)

        st.divider()

        st.subheader("Non Functional Requirements")

        for req in blueprint.non_functional_requirements:
            st.markdown(f"###  {req.title}")
            st.write(req.description)

    # ==========================================================
    # Architecture
    # ==========================================================

    with architecture_tab:
        st.subheader("Architecture Pattern")
        st.success(blueprint.architecture.pattern)
        st.write(blueprint.architecture.reason)

        st.subheader("Architecture Diagram")

        try:
            render_mermaid(blueprint.architecture.mermaid_diagram)
        except Exception as e:
            st.warning("Could not render the diagram image — showing raw source instead.")
            st.caption(f"Details: {e}")

        with st.expander("View raw Mermaid source"):
            st.code(
                textwrap.dedent(blueprint.architecture.mermaid_diagram).strip(),
                language="mermaid",
            )

        st.subheader("Data Flow")

        for step in blueprint.data_flow:
            st.write(f"{step}")

    # ==========================================================
    # Components
    # ==========================================================

    with components_tab:
        for component in blueprint.components:
            with st.container(border=True):
                st.subheader(component.name)
                st.write(f"**Purpose:** {component.purpose}")
                st.write("**Technologies:** " + ", ".join(component.technologies))

    # ==========================================================
    # Technology Stack
    # ==========================================================

    with tech_tab:
        for tech in blueprint.technology_stack:
            with st.container(border=True):
                st.subheader(tech.category)
                st.write(f"**Technology:** {tech.name}")
                st.caption(tech.reason)

    # ==========================================================
    # Database
    # ==========================================================

    with database_tab:
        st.success(f"Database Type: {blueprint.database_type}")

        for table in blueprint.database_tables:
            with st.container(border=True):
                st.subheader(table.name)
                for field in table.fields:
                    st.write(f"• {field}")

    # ==========================================================
    # APIs
    # ==========================================================

    with api_tab:
        for api in blueprint.apis:
            with st.container(border=True):
                st.code(f"{api.method} {api.endpoint}", language="text")
                st.write(api.description)

    # ==========================================================
    # Roadmap
    # ==========================================================

    with roadmap_tab:
        for phase in blueprint.roadmap:
            with st.container(border=True):
                st.subheader(phase.phase)
                st.write(f" Duration: {phase.duration}")
                for task in phase.tasks:
                    st.write(f" {task}")

    # ==========================================================
    # Risks
    # ==========================================================

    with risks_tab:
        for risk in blueprint.risks:
            with st.container(border=True):
                st.error(risk.risk)
                st.write(f"**Mitigation:** {risk.mitigation}")

    # ==========================================================
    # Future Features
    # ==========================================================

    with future_tab:
        for feature in blueprint.future_features:
            st.success(feature)

    st.subheader("Folder Structure")
    st.code(blueprint.folder_structure, language="text")

    if docs:
        with st.expander("📚 Retrieved Documentation"):
            for i, doc in enumerate(docs, 1):
                st.markdown(f"### Document {i}")
                st.caption(doc.metadata.get("source"))
                st.write(doc.page_content[:800])
                st.divider()

    markdown = generate_markdown(blueprint)

    st.download_button(
        "📥 Download Blueprint (.md)",
        data=markdown,
        file_name=f"{blueprint.basic_info.project_name}.md",
        mime="text/markdown",
    )