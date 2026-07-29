def generate_markdown(blueprint):

    md = f"# {blueprint.basic_info.project_name}\n\n"

    md += f"## Overview\n"
    md += blueprint.basic_info.overview + "\n\n"

    md += "## Functional Requirements\n"

    for req in blueprint.functional_requirements:
        md += f"- **{req.title}**: {req.description}\n"

    md += "\n## Technology Stack\n"

    for tech in blueprint.technology_stack:
        md += f"- **{tech.category}**: {tech.name}\n"

    md += "## Architecture Diagram\n\n"

    md += "```mermaid\n"

    md += blueprint.architecture.mermaid_diagram

    md += "\n```\n"

    md += "\n## Roadmap\n"

    for phase in blueprint.roadmap:

        md += f"\n### {phase.phase}\n"

        md += f"Duration: {phase.duration}\n"

        for task in phase.tasks:
            md += f"- {task}\n"

    md += "\n## Risks\n"

    for risk in blueprint.risks:
        md += f"- **{risk.risk}**\n"
        md += f"  - Mitigation: {risk.mitigation}\n"

    return md