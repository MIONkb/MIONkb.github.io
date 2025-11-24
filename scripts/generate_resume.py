"""Generate a PDF resume from site content.

This script pulls data from the existing markdown sources (about page,
experience posts, publications, awards) and renders a compact resume-style
PDF that also includes a profile photo. It is intended to be run locally,
for example:

    python scripts/generate_resume.py --output files/resume.pdf \
        --photo images/bio-photo.jpg

Dependencies are listed in ``scripts/requirements-resume.txt``.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import re
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

try:
    from fpdf import FPDF
except ImportError as exc:  # pragma: no cover - import guard
    raise SystemExit("Please install dependencies with `pip install -r scripts/requirements-resume.txt`.") from exc

import yaml

ROOT = Path(__file__).resolve().parents[1]
ABOUT_PAGE = ROOT / "_pages" / "about.md"
EXPERIENCE_DIR = ROOT / "_experience"
AWARDS_DIR = ROOT / "_awards"
PUBLICATIONS_DIR = ROOT / "_publications"


class ResumePDF(FPDF):
    def header(self) -> None:  # pragma: no cover - simple layout code
        # Override the parent header to remove default page numbering.
        return

    def section_title(self, title: str) -> None:
        self.set_font("Helvetica", "B", 16)
        self.cell(0, 10, title, ln=True)
        self.ln(2)

    def paragraph(self, text: str) -> None:
        self.set_font("Helvetica", size=11)
        self.multi_cell(0, 7, text)
        self.ln(1)

    def bullet_list(self, items: Iterable[str]) -> None:
        self.set_font("Helvetica", size=11)
        for item in items:
            self.cell(6)
            self.multi_cell(0, 6, f"• {item}")
        self.ln(1)


def load_markdown_body(path: Path) -> List[str]:
    """Read markdown file without front matter."""
    with path.open("r", encoding="utf-8") as f:
        lines = f.read().splitlines()
    if lines and lines[0].strip() == "---":
        try:
            end_idx = lines[1:].index("---") + 1
            return lines[end_idx + 1 :]
        except ValueError:
            pass
    return lines


def read_front_matter(path: Path) -> Dict[str, object]:
    """Return YAML front matter as a dictionary."""
    with path.open("r", encoding="utf-8") as f:
        lines = f.read().splitlines()
    if lines and lines[0].strip() == "---":
        try:
            end_idx = lines[1:].index("---") + 1
        except ValueError:
            return {}
        data = yaml.safe_load("\n".join(lines[1:end_idx]))
        return data or {}
    return {}


def parse_about(content: List[str]) -> Tuple[List[str], List[str]]:
    """Return (about_paragraphs, research_interest list)."""
    paragraphs: List[str] = []
    research: List[str] = []
    in_about = False
    in_research = False

    for line in content:
        heading_match = re.match(r"^## +(.+)$", line)
        if heading_match:
            heading = heading_match.group(1).strip().lower()
            in_about = heading.startswith("about")
            in_research = False
            continue

        if line.strip().startswith("- Research Interests"):
            in_research = True
            in_about = False
            continue

        if line.strip().startswith("##"):
            in_about = False
            in_research = False

        if in_about:
            clean = line.strip()
            if clean:
                paragraphs.append(clean)
        elif in_research:
            stripped = line.strip()
            if stripped.startswith("-"):
                research.append(stripped.lstrip("-* "))
            elif stripped.startswith("•"):
                research.append(stripped.lstrip("• "))
            elif stripped == "":
                continue
            else:
                # Stop if we've left the bullet list
                in_research = False

    return paragraphs, research


def parse_bullet_section(lines: Iterable[str]) -> List[str]:
    items: List[str] = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("-"):
            items.append(stripped.lstrip("- "))
    return items


def parse_experiences() -> Dict[str, List[str]]:
    experiences: Dict[str, List[str]] = {}
    for path in sorted(EXPERIENCE_DIR.glob("*.md")):
        body = load_markdown_body(path)
        if not body:
            continue
        meta = read_front_matter(path)
        title = meta.get("title") or path.stem.replace("-", " ").title()
        bullets = parse_bullet_section(body)
        if bullets:
            experiences[title] = bullets
    return experiences


def parse_awards() -> Dict[str, List[str]]:
    awards: Dict[str, List[str]] = {}
    for path in sorted(AWARDS_DIR.glob("*.md")):
        body = load_markdown_body(path)
        bullets = parse_bullet_section(body)
        if bullets:
            meta = read_front_matter(path)
            title = meta.get("title") or path.stem.title()
            awards[title] = bullets
    return awards


def parse_publications(limit: int | None = None) -> List[Dict[str, str]]:
    publications: List[Dict[str, str]] = []
    for path in PUBLICATIONS_DIR.glob("*.md"):
        with path.open("r", encoding="utf-8") as f:
            lines = f.read().splitlines()
        if not lines or lines[0].strip() != "---":
            continue
        try:
            end_idx = lines[1:].index("---") + 1
        except ValueError:
            continue
        meta_text = "\n".join(lines[1:end_idx])
        meta = yaml.safe_load(meta_text) or {}
        description = "\n".join(lines[end_idx + 1 :]).strip()
        publications.append(
            {
                "title": meta.get("title", path.stem.replace("-", " ")), 
                "venue": meta.get("venue", meta.get("journal", "")),
                "date": meta.get("date", ""),
                "excerpt": re.sub(r"<[^>]+>", "", meta.get("excerpt", "")),
                "description": description,
            }
        )

    def parse_date(date_str: str) -> _dt.date:
        try:
            return _dt.date.fromisoformat(str(date_str))
        except Exception:
            return _dt.date.min

    publications.sort(key=lambda item: parse_date(item.get("date", "")), reverse=True)
    if limit:
        publications = publications[:limit]
    return publications


def build_resume(output: Path, photo: Path, pub_limit: int) -> None:  # pragma: no cover - CLI glue
    about_meta = read_front_matter(ABOUT_PAGE)
    about_content = load_markdown_body(ABOUT_PAGE)
    about_paras, research = parse_about(about_content)
    name = str(about_meta.get("title", "")).strip()
    experiences = parse_experiences()
    awards = parse_awards()
    publications = parse_publications(limit=pub_limit)

    pdf = ResumePDF()
    pdf.add_page()

    # Header with name and photo
    if photo.exists():
        pdf.image(str(photo), x=10, y=10, w=30)
        pdf.set_xy(45, 12)
    else:
        pdf.set_xy(10, 12)
    pdf.set_font("Helvetica", "B", 20)
    pdf.cell(0, 10, name or "Curriculum Vitae", ln=True)
    pdf.ln(5)

    if about_paras:
        pdf.section_title("About")
        for para in about_paras:
            pdf.paragraph(para)

    if research:
        pdf.section_title("Research Interests")
        pdf.bullet_list(research)

    if experiences:
        pdf.section_title("Experience")
        for title, bullets in experiences.items():
            pdf.set_font("Helvetica", "B", 12)
            pdf.cell(0, 8, title, ln=True)
            pdf.bullet_list(bullets)

    if publications:
        pdf.section_title("Publications")
        for pub in publications:
            pdf.set_font("Helvetica", "B", 12)
            pdf.cell(0, 7, pub["title"], ln=True)
            if pub["venue"]:
                pdf.set_font("Helvetica", "I", 11)
                pdf.cell(0, 6, pub["venue"], ln=True)
            if pub["date"]:
                pdf.set_font("Helvetica", size=10)
                pdf.cell(0, 5, str(pub["date"]), ln=True)
            if pub["excerpt"]:
                pdf.paragraph(pub["excerpt"])
            pdf.ln(2)

    if awards:
        pdf.section_title("Awards")
        for title, bullets in awards.items():
            pdf.set_font("Helvetica", "B", 12)
            pdf.cell(0, 7, title, ln=True)
            pdf.bullet_list(bullets)

    output.parent.mkdir(parents=True, exist_ok=True)
    pdf.output(str(output))


def main() -> None:  # pragma: no cover - CLI entrypoint
    parser = argparse.ArgumentParser(description="Generate a PDF resume from site content.")
    parser.add_argument(
        "--output", "-o", type=Path, default=ROOT / "files" / "resume.pdf", help="Where to write the PDF"
    )
    parser.add_argument(
        "--photo",
        type=Path,
        default=ROOT / "images" / "bio-photo.jpg",
        help="Path to a profile photo to include in the header.",
    )
    parser.add_argument(
        "--max-publications", type=int, default=10, help="Maximum number of publications to include."
    )
    args = parser.parse_args()
    build_resume(args.output, args.photo, args.max_publications)
    print(f"Resume saved to {args.output}")


if __name__ == "__main__":  # pragma: no cover - script guard
    main()
