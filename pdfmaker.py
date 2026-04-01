import json
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4

# Load JSON
with open("story.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Extract values
story_title = data["story_title"]["0"]
story_overview = data["story_overview"]["0"]
story_phases = data["story_phases"]["0"]
world_building = data["world_building"]["0"]
characters = data["character"]["0"]
prompts = data["comic_page_image_prompts"]["0"]

# Create PDF
doc = SimpleDocTemplate("story_output.pdf", pagesize=A4)
styles = getSampleStyleSheet()

# ✅ Custom style for prompts
code_style = ParagraphStyle(
    name="PromptStyle",
    parent=styles["BodyText"],
    fontName="Courier",
    fontSize=8,
    leading=10,
    backColor="#f5f5f5",
    borderPadding=5
)

content = []

# Title
content.append(Paragraph(f"<b>{story_title}</b>", styles["Title"]))
content.append(Spacer(1, 12))

# Overview
content.append(Paragraph("<b>Story Overview</b>", styles["Heading2"]))
content.append(Paragraph(story_overview, styles["BodyText"]))
content.append(Spacer(1, 12))

# World Building
content.append(Paragraph("<b>World Building</b>", styles["Heading2"]))
content.append(Paragraph(world_building, styles["BodyText"]))
content.append(Spacer(1, 12))

# Characters
content.append(Paragraph("<b>Characters</b>", styles["Heading2"]))
for char in characters:
    char_text = f"""
    <b>Name:</b> {char['name']}<br/>
    <b>Age:</b> {char['age']}<br/>
    <b>Gender:</b> {char['gender']}<br/>
    <b>Description:</b> {char['description']}<br/>
    <b>Looks:</b> {char['looks']}<br/>
    <b>Personality:</b> {char['personality']}
    """
    content.append(Paragraph(char_text, styles["BodyText"]))
    content.append(Spacer(1, 10))

# Story Phases
content.append(Paragraph("<b>Story Phases</b>", styles["Heading2"]))
for phase in story_phases:
    phase_text = f"""
    <b>Phase {phase['phase_number']}: {phase['phase_title']}</b><br/>
    {phase['description']}<br/>
    <b>Characters:</b> {", ".join(phase['characters'])}
    """
    content.append(Paragraph(phase_text, styles["BodyText"]))
    content.append(Spacer(1, 10))

# New Page
content.append(PageBreak())

# Comic Prompts
content.append(Paragraph("<b>Comic Page Prompts</b>", styles["Heading2"]))
content.append(Spacer(1, 10))

for i, prompt in enumerate(prompts):
    formatted_prompt = prompt.replace("\n", "<br/>")

    content.append(Paragraph(f"<b>Page {i+1}</b>", styles["Heading3"]))
    content.append(Spacer(1, 6))

    content.append(Paragraph(formatted_prompt, code_style))
    content.append(Spacer(1, 12))

# Build PDF
doc.build(content)

print("✅ PDF generated successfully: story_output.pdf")