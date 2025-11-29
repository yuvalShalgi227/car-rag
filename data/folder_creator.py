import os
from pathlib import Path

def write_readme(path: Path, text: str):
    (path / "README.txt").write_text(text, encoding="utf-8")


def create_kb_structure(base_path: str):
    base = Path(base_path)

    # Definitions of top-level folders and their explanations
    folders = {
        "manuals": (
            "This folder stores full car manuals.\n"
            "Structure: manufacturer → model → year.\n"
            "Each file is a complete manual (PDF). Useful for deep technical lookup."
        ),
        "specs": (
            "This folder stores technical specifications.\n"
            "Structure: manufacturer → model.\n"
            "Each file contains structured JSON with key vehicle specs such as oil type, capacities, pressures, etc."
        ),
        "manufacturers": (
            "This folder contains manufacturer-level data.\n"
            "Each manufacturer folder stores general information, known issues, special warning indicators,\n"
            "and metadata shared across all models."
        )
    }

    # Example subfolders for demonstration
    examples = {
        "manuals": ["Toyota/Corolla/2018", "Mazda/3/2016"],
        "specs": ["Toyota/Corolla", "Mazda/3"],
        "manufacturers": ["Toyota", "Mazda"]
    }

    # Create top-level folders and README files
    for folder, description in folders.items():
        folder_path = base / folder
        folder_path.mkdir(parents=True, exist_ok=True)
        write_readme(folder_path, description)

        # Create example subfolders + README inside each, to show structure
        for sub in examples[folder]:
            sub_path = folder_path / sub
            sub_path.mkdir(parents=True, exist_ok=True)

            write_readme(
                sub_path,
                (
                    f"This is an example subfolder for the '{folder}' category.\n"
                    f"Folder path: {sub_path}\n\n"
                    "Place real files here following this structure.\n"
                    "LLM Note: Files placed here should be domain-specific and consistent."
                )
            )

    print("Knowledge Base structure rebuilt successfully.")


# Run:
create_kb_structure("knowledge_base")
