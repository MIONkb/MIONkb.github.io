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
    from fpdf.enums import XPos, YPos
except ImportError as exc:  # pragma: no cover - import guard
    raise SystemExit("Please install dependencies with `pip install -r scripts/requirements-resume.txt`.") from exc

import yaml

# [text](url) -> text
_MD_LINK_RE = re.compile(r"\[([^\]]+)\]\([^)]+\)")
# `code` -> code
_MD_CODE_RE = re.compile(r"`([^`]+)`")
# **em** / *em* / __em__ / _em_ -> em
_MD_EMPH_RE = re.compile(r"(\*\*|__|\*|_)(.*?)\1")
# <tag> -> 空
_HTML_TAG_RE = re.compile(r"<[^>]+>")


def md_inline_to_text(text: str) -> str:
    """Strip basic inline markdown + HTML to plain text for PDF rendering."""
    text = _MD_LINK_RE.sub(r"\1", text)
    text = _MD_CODE_RE.sub(r"\1", text)
    text = _MD_EMPH_RE.sub(r"\2", text)
    text = _HTML_TAG_RE.sub("", text)
    return text.strip()

ROOT = Path(__file__).resolve().parents[1]
ABOUT_PAGE = ROOT / "_pages" / "about.md"
EXPERIENCE_DIR = ROOT / "_experience"
AWARDS_DIR = ROOT / "_awards"
PUBLICATIONS_DIR = ROOT / "_publications"


class ResumePDF(FPDF):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        # 默认字体名，可以被外面覆盖（build_resume 里已经设置 pdf.base_font = "CJK"）
        self.base_font = "Helvetica"

    def section_title(self, title: str) -> None:
        self.set_font(self.base_font, size=15)
        self.set_x(self.l_margin)
        self.cell(0, 10, title, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(1)

    def paragraph(self, text: str) -> None:
        self.set_font(self.base_font, size=11)
        self.set_x(self.l_margin)
        effective_w = self.w - self.l_margin - self.r_margin
        self.multi_cell(effective_w, 6, text)
        self.ln(0.5)

    def bullet_list(self, items: list[str]) -> None:
        self.set_font(self.base_font, size=11)
        effective_w = self.w - self.l_margin - self.r_margin
        for item in items:
            self.set_x(self.l_margin)
            text = f"- {item}"
            self.multi_cell(effective_w, 6, text)
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
    current_para: List[str] = []

    for line in content:
        heading_match = re.match(r"^## +(.+)$", line)
        if heading_match:
            # 遇到二级标题，看看是不是 About
            heading = heading_match.group(1).strip().lower()
            # 先把正在累积的段落收尾
            if current_para:
                paragraphs.append(md_inline_to_text(" ".join(current_para)))
                current_para = []
            in_about = heading.startswith("about")
            in_research = False
            continue

        # 特殊标记，开始 Research Interests 区域
        if line.strip().startswith("- Research Interests"):
            if current_para:
                paragraphs.append(md_inline_to_text(" ".join(current_para)))
                current_para = []
            in_research = True
            in_about = False
            continue

        # 遇到新的 section（## 开头）就退出当前区域
        if line.strip().startswith("##"):
            if current_para:
                paragraphs.append(md_inline_to_text(" ".join(current_para)))
                current_para = []
            in_about = False
            in_research = False
            continue

        if in_about:
            clean = line.strip()
            if clean:
                current_para.append(clean)
            else:
                # 空行视作段落结束
                if current_para:
                    paragraphs.append(md_inline_to_text(" ".join(current_para)))
                    current_para = []
        elif in_research:
            stripped = line.strip()
            if stripped.startswith(("-", "*", "•")):
                item = stripped.lstrip("-*• ").strip()
                if item:
                    research.append(md_inline_to_text(item))
            elif stripped == "":
                # 空行：继续等待下一条 bullet
                continue
            else:
                # 碰到非 bullet 的内容，说明 research section 结束
                in_research = False

    # 文件结束时把最后一个段落收掉
    if current_para:
        paragraphs.append(md_inline_to_text(" ".join(current_para)))

    return paragraphs, research


def parse_bullet_section(lines: Iterable[str]) -> List[str]:
    """Parse a markdown bullet list (allowing multi-line items)."""
    items: List[str] = []
    current: List[str] = []

    for line in lines:
        stripped = line.rstrip()

        if not stripped:
            # 空行结束当前 bullet
            if current:
                text = md_inline_to_text(" ".join(current))
                if text and text.lower() != "link":
                    items.append(text)
                current = []
            continue

        if stripped.lstrip().startswith("- "):
            # 新 bullet，先收掉旧的
            if current:
                text = md_inline_to_text(" ".join(current))
                if text and text.lower() != "link":
                    items.append(text)
                current = []
            text = stripped.lstrip()[2:].strip()
            if text:
                current.append(text)
        else:
            # 不是 "-" 开头，如果有 current，当作续行
            if current:
                current.append(stripped.strip())

    if current:
        text = md_inline_to_text(" ".join(current))
        if text and text.lower() != "link":
            items.append(text)

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

        body_text = "\n".join(lines[end_idx + 1 :]).strip()
        # description 里同样清理 markdown / HTML
        description = md_inline_to_text(body_text)

        raw_title = meta.get("title", path.stem.replace("-", " "))
        raw_venue = meta.get("venue", meta.get("journal", ""))
        raw_excerpt = meta.get("excerpt", "")

        publications.append(
            {
                "title": md_inline_to_text(raw_title),
                "venue": md_inline_to_text(raw_venue),
                "date": meta.get("date", ""),
                "excerpt": md_inline_to_text(re.sub(r"<[^>]+>", "", raw_excerpt)),
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


def build_resume(output: Path, photo: Path, pub_limit: int) -> None:
    about_meta = read_front_matter(ABOUT_PAGE)
    about_content = load_markdown_body(ABOUT_PAGE)
    about_paras, research = parse_about(about_content)
    name = str(about_meta.get("title", "")).strip()
    experiences = parse_experiences()
    awards = parse_awards()
    publications = parse_publications(limit=pub_limit)

    # 使用 Windows 自带的微软雅黑作为 Unicode 字体
    BASE_FONT = "CJK"  # PDF 内部字体名，随便起
    FONT_PATH = r"C:\Windows\Fonts\msyh.ttc"  # 微软雅黑

    pdf = ResumePDF()
    pdf.base_font = BASE_FONT      # 🟡 告诉自定义类用哪种字体
    pdf.add_page()

    # 注册 Unicode 字体（fpdf2 新版可以不写 uni 参数，避免 warning）
    pdf.add_font(BASE_FONT, "", FONT_PATH)

    # Header with name and photo
    if photo.exists():
        pdf.image(str(photo), x=10, y=10, w=30)
        pdf.set_xy(45, 12)
    else:
        pdf.set_xy(10, 12)

    pdf.set_font(BASE_FONT, size=20)
    pdf.cell(0, 10, name or "Curriculum Vitae", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)

    # About
    if about_paras:
        pdf.section_title("About")
        for para in about_paras:
            pdf.paragraph(para)

    # Research Interests
    if research:
        pdf.section_title("Research Interests")
        pdf.bullet_list(research)

    # Experience
    if experiences:
        pdf.section_title("Experience")
        for title, bullets in experiences.items():
            pdf.set_font(BASE_FONT, size=12)
            pdf.cell(0, 8, title, new_x="LMARGIN", new_y="NEXT")
            pdf.bullet_list(bullets)

    # Publications
    if publications:
        pdf.section_title("Publications")
        for pub in publications:
            pdf.set_font(BASE_FONT, size=12)
            pdf.cell(0, 7, pub["title"], new_x="LMARGIN", new_y="NEXT")

            if pub["venue"]:
                pdf.set_font(BASE_FONT, size=11)
                pdf.cell(0, 6, pub["venue"], new_x="LMARGIN", new_y="NEXT")

            if pub["date"]:
                pdf.set_font(BASE_FONT, size=10)
                pdf.cell(0, 5, str(pub["date"]), new_x="LMARGIN", new_y="NEXT")

            if pub["excerpt"]:
                pdf.set_font(BASE_FONT, size=11)
                pdf.paragraph(pub["excerpt"])

            pdf.ln(2)

    # Awards
    if awards:
        pdf.section_title("Awards")
        for title, bullets in awards.items():
            pdf.set_font(BASE_FONT, size=12)
            pdf.cell(0, 7, title, new_x="LMARGIN", new_y="NEXT")
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
        default=ROOT / "images" / "mionhead_bluebackground.jpg",
        help="Path to a profile photo to include in the header.",
    )
    parser.add_argument(
        "--max-publications", type=int, default=100, help="Maximum number of publications to include."
    )
    args = parser.parse_args()
    build_resume(args.output, args.photo, args.max_publications)
    print(f"Resume saved to {args.output}")


if __name__ == "__main__":  # pragma: no cover - script guard
    main()
