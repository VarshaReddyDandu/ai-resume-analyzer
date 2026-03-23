from typing import List


def generate_bullets(role: str, experience: str, tools: str) -> List[str]:
    role = role.title()
    tools_list = [t.strip().title() for t in tools.split(",")]

    bullets = [
        f"Designed and developed {role} solutions using {', '.join(tools_list)}.",
        f"Built and optimized systems for {experience}, improving efficiency and reliability.",
        f"Collaborated with cross-functional teams to deliver scalable and production-ready ML solutions."
    ]

    return bullets