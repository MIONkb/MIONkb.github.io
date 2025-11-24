from pathlib import Path
import markdown
from weasyprint import HTML

ROOT = Path(__file__).resolve().parents[1]

ABOUT_PAGE = ROOT / "_pages" / "about.md"
EXPERIENCE_DIR = ROOT / "_experience"
AWARDS_DIR = ROOT / "_awards"
PUBLICATIONS_DIR = ROOT / "_publications"
OUTPUT_PDF = ROOT / "files" / "resume_md.pdf"

CSS = """
body {
  font-family: "Microsoft YaHei", "Noto Sans", system-ui, sans-serif;
  font-size: 11pt;
  line-height: 1.4;
}
h1, h2, h3 {
  margin-top: 0.8em;
  margin-bottom: 0.3em;
}
h1 { font-size: 20pt; }
h2 { font-size: 16pt; border-bottom: 1px solid #ccc; padding-bottom: 0.1em; }
ul { margin-bottom: 0.4em; }
"""

def read_md(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    # 简单去掉 YAML front-matter
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) == 3:
            text = parts[2]
    return text.strip()

def main():
    sections = []

    # 1) About（你可以在 about.md 里用 # 楼佳杭 之类的标题）
    sections.append(read_md(ABOUT_PAGE))

    # 2) Experience / Awards / Publications 按你需要的顺序拼接
    def concat_dir(dir_path: Path, title: str) -> str:
        md_parts = [f"## {title}\n"]
        for path in sorted(dir_path.glob("*.md")):
            md_parts.append(read_md(path))
        return "\n\n".join(md_parts)

    sections.append(concat_dir(EXPERIENCE_DIR, "Experience"))
    sections.append(concat_dir(AWARDS_DIR, "Awards"))
    sections.append(concat_dir(PUBLICATIONS_DIR, "Publications"))

    full_md = "\n\n".join(sections)

    # Markdown -> HTML
    html_body = markdown.markdown(
        full_md,
        extensions=["extra", "toc", "tables", "sane_lists"],
        output_format="html5",
    )

    html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
{CSS}
</style>
</head>
<body>
{html_body}
</body>
</html>
"""

    OUTPUT_PDF.parent.mkdir(parents=True, exist_ok=True)
    HTML(string=html).write_pdf(str(OUTPUT_PDF))
    print("Saved:", OUTPUT_PDF)

if __name__ == "__main__":
    main()
