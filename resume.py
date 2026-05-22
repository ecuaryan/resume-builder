from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_RIGHT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    HRFlowable,
    KeepTogether,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

OUTPUT_DIR = Path(__file__).resolve().parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)
pdf_path = OUTPUT_DIR / "Ryan_Willmore_Resume.pdf"

# ~1/8" page margin. Asymmetric insets: right gutter matches left visually.
PAGE_MARGIN = 0.125 * inch
CONTENT_INSET_LEFT = 6
CONTENT_INSET_RIGHT = 16

styles = getSampleStyleSheet()


def _base_style(name: str, **kwargs) -> ParagraphStyle:
    text_color = kwargs.pop("textColor", colors.black)
    return ParagraphStyle(
        name,
        parent=styles["Normal"],
        textColor=text_color,
        leftIndent=kwargs.pop("leftIndent", CONTENT_INSET_LEFT),
        rightIndent=kwargs.pop("rightIndent", CONTENT_INSET_RIGHT),
        firstLineIndent=kwargs.pop("firstLineIndent", 0),
        **kwargs,
    )


def _page_header_name_style() -> ParagraphStyle:
    return _base_style(
        name="PageHeaderName",
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=22,
        leftIndent=0,
        rightIndent=0,
    )


def _page_header_contact_style() -> ParagraphStyle:
    return _base_style(
        name="PageHeaderContact",
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=22,
        alignment=TA_RIGHT,
        leftIndent=0,
        rightIndent=0,
    )


SECTION_TITLE_LARGE = 11
SECTION_TITLE_SMALL = 8  # small caps: rest of letters ~73% of first
# HRFlowable ignores spaceBefore/spaceAfter; control gaps via table padding instead.
SECTION_TITLE_TO_RULE = 4  # pt between section title and horizontal rule
SECTION_RULE_TO_CONTENT = 3  # pt between rule and content below (e.g. first job)

section_style = _base_style(
    name="Section",
    fontName="Helvetica-Bold",
    fontSize=SECTION_TITLE_LARGE,
    leading=13,
    spaceBefore=2,
    spaceAfter=0,
    leftIndent=0,
    rightIndent=0,
)


def format_section_title(title: str) -> str:
    """Uppercase with first letter full size, remaining letters smaller (small caps)."""
    title = title.upper().strip()
    if len(title) <= 1:
        return (
            f'<font size="{SECTION_TITLE_LARGE}"><b>{title}</b></font>'
        )
    return (
        f'<font size="{SECTION_TITLE_LARGE}"><b>{title[0]}</b></font>'
        f'<font size="{SECTION_TITLE_SMALL}"><b>{title[1:]}</b></font>'
    )

skills_style = _base_style(
    name="Skills",
    fontName="Helvetica",
    fontSize=9.5,
    leading=10.5,
    spaceAfter=1,
)

BULLET_MARKER_WIDTH = 14
BULLET_TEXT_GAP = 8


def _bullet_marker_style() -> ParagraphStyle:
    return _base_style(
        name="BulletMarker",
        fontName="Helvetica",
        fontSize=9.5,
        leading=10.5,
        alignment=TA_RIGHT,
        leftIndent=0,
        rightIndent=0,
    )


def _bullet_text_style() -> ParagraphStyle:
    return _base_style(
        name="BulletText",
        fontName="Helvetica",
        fontSize=9.5,
        leading=10.5,
        leftIndent=0,
        rightIndent=0,
        spaceAfter=3,
    )


def _bullet_row(frame_width: float, text: str) -> Table:
    """Bullet column + text column so wrapped lines share one vertical text edge."""
    inner_w = _inner_width(frame_width)
    text_w = inner_w - BULLET_MARKER_WIDTH
    row = Table(
        [[
            Paragraph("&bull;", _bullet_marker_style()),
            Paragraph(text, _bullet_text_style()),
        ]],
        colWidths=[BULLET_MARKER_WIDTH, text_w],
        hAlign="LEFT",
    )
    row.setStyle(
        TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (0, -1), BULLET_TEXT_GAP),
            ("RIGHTPADDING", (1, 0), (1, -1), 0),
            ("TOPPADDING", (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ])
    )
    return _inset_wrapper(row, frame_width)


def _inner_width(frame_width: float) -> float:
    return frame_width - CONTENT_INSET_LEFT - CONTENT_INSET_RIGHT


def _inset_wrapper(flowable, frame_width: float):
    """Gutter columns so flowables share the same horizontal box as section rules."""
    left_pad = CONTENT_INSET_LEFT
    right_pad = CONTENT_INSET_RIGHT
    if left_pad <= 0 and right_pad <= 0:
        return flowable
    inner_w = _inner_width(frame_width)
    wrapper = Table(
        [["", flowable, ""]],
        colWidths=[left_pad, inner_w, right_pad],
        hAlign="LEFT",
    )
    wrapper.setStyle(
        TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ("TOPPADDING", (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ])
    )
    return wrapper


def _job_col_widths(content_width: float) -> tuple[float, float]:
    w = int(content_width)
    left = int(w * 0.55)
    return left, w - left


def _job_header_left_style() -> ParagraphStyle:
    return _base_style(
        name="JobHeaderLeft",
        fontName="Helvetica-Bold",
        fontSize=10.5,
        leading=12,
        leftIndent=0,
        rightIndent=0,
    )


def _job_header_right_style() -> ParagraphStyle:
    return _base_style(
        name="JobHeaderRight",
        fontName="Helvetica-Bold",
        fontSize=10.5,
        leading=12,
        alignment=TA_RIGHT,
        leftIndent=0,
        rightIndent=0,
    )


def _job_tech_style() -> ParagraphStyle:
    return _base_style(
        name="JobTech",
        fontName="Helvetica",
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#475569"),
        leftIndent=0,
        rightIndent=0,
        spaceAfter=2,
    )


def _header_table_style() -> TableStyle:
    return TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ])


def _job_header_table(
    inner_width: float,
    company: str,
    location: str,
    role: str,
    dates: str,
) -> Table:
    left_w, right_w = _job_col_widths(inner_width)
    left_style = _job_header_left_style()
    right_style = _job_header_right_style()
    table = Table(
        [
            [
                Paragraph(f"<b>{company}</b>", left_style),
                Paragraph(location or "", right_style),
            ],
            [
                Paragraph(f"<b>{role}</b>", left_style),
                Paragraph(dates or "", right_style),
            ],
        ],
        colWidths=[left_w, right_w],
        hAlign="LEFT",
    )
    table.setStyle(_header_table_style())
    return table


def add_page_header(story, frame_width: float) -> None:
    inner_w = _inner_width(frame_width)
    left_w = min(2.25 * inch, int(inner_w * 0.32))
    right_w = int(inner_w) - left_w
    contact = (
        "(208) 360-9649 &middot; ryanwillmore@gmail.com &middot; "
        "linkedin.com/in/ryan-willmore"
    )
    contact_markup = f"<b>{contact}</b>"
    row = Table(
        [[
            Paragraph("<b>Ryan Willmore</b>", _page_header_name_style()),
            Paragraph(contact_markup, _page_header_contact_style()),
        ]],
        colWidths=[left_w, right_w],
        rowHeights=[22],
        hAlign="LEFT",
    )
    row.setStyle(
        TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("TOPPADDING", (0, 0), (0, 0), 0),
            ("TOPPADDING", (1, 0), (1, 0), 7),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ])
    )
    story.append(_inset_wrapper(row, frame_width))
    story.append(Spacer(1, 5))


def add_section_heading(story, frame_width: float, title: str) -> None:
    inner_w = _inner_width(frame_width)
    story.append(Spacer(1, 4))
    title_para = Paragraph(format_section_title(title), section_style)
    rule = HRFlowable(
        width=inner_w,
        thickness=0.5,
        color=colors.black,
    )
    heading_block = Table(
        [[title_para], [rule]],
        colWidths=[inner_w],
        hAlign="LEFT",
    )
    heading_block.setStyle(
        TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ("TOPPADDING", (0, 0), (0, 0), 0),
            ("BOTTOMPADDING", (0, 0), (0, 0), 0),
            ("TOPPADDING", (0, 1), (0, 1), SECTION_TITLE_TO_RULE),
            ("BOTTOMPADDING", (0, 1), (0, 1), SECTION_RULE_TO_CONTENT),
        ])
    )
    story.append(_inset_wrapper(heading_block, frame_width))


def add_skills_section(story, categories: dict[str, str]) -> None:
    for label, items in categories.items():
        story.append(
            Paragraph(f"<b>{label}:</b> {items}", skills_style),
        )


def add_bullet(story, frame_width: float, text: str) -> None:
    story.append(_bullet_row(frame_width, text))


def build_job_block(
    frame_width: float,
    company: str,
    location: str,
    role: str,
    dates: str,
    bullets: list[str],
    tech_stack: str | None = None,
) -> list:
    inner_w = _inner_width(frame_width)
    header = _job_header_table(inner_w, company, location, role, dates)
    block = [_inset_wrapper(header, frame_width)]
    if tech_stack:
        block.append(
            _inset_wrapper(Paragraph(tech_stack, _job_tech_style()), frame_width)
        )
    for text in bullets:
        block.append(_bullet_row(frame_width, text))
    block.append(Spacer(1, 7))
    return block


SKILL_CATEGORIES = {
    "Languages": "TypeScript, JavaScript, C#, SQL",
    "Frontend": "React, HTML, CSS, Angular",
    "Backend & APIs": "Node.js, Express.js, .NET, GraphQL, REST APIs, Microservices",
    "Cloud & Infrastructure": (
        "AWS (Lambda, API Gateway, Amazon Bedrock AgentCore), Azure Functions, Serverless"
    ),
    "Databases": "Postgres, DynamoDB, MongoDB, Cosmos DB",
    "Tools": "Datadog, Jest, Git, CI/CD",
}

RECENT_JOBS = [
    {
        "company": "Pie Insurance",
        "location": "Remote",
        "role": "Senior Software Engineer",
        "dates": "January 2025 – May 2026",
        "tech_stack": (
            "TypeScript &middot; AWS &middot; GraphQL &middot; Node.js &middot; Express.js "
            "&middot; Serverless &middot; DynamoDB &middot; Datadog &middot; Postgres"
        ),
        "bullets": [
            (
                "Led development of an AI-powered Rate Update Agent using Amazon Bedrock AgentCore to "
                "automate rate file processing and GitHub PR generation from Jira tickets, replacing 40+ "
                "manual updates per year that each consumed days of developer time with ~10-minute automated runs"
            ),
            (
                "Oversaw migration of a Go-based microservice to TypeScript/Node.js, including API Gateway "
                "integration, DynamoDB caching, smoke tests, SDK generation, and migration documentation"
            ),
            (
                "Managed pricing infrastructure for Workers' Comp and Commercial Auto using a "
                "TypeScript/AWS serverless stack"
            ),
            (
                "Implemented rating and billing enhancements across multiple repositories, APIs, and "
                "GraphQL schemas under tight delivery timelines"
            ),
        ],
    },
    {
        "company": "Retrium",
        "location": "Remote",
        "role": "Software Engineer",
        "dates": "August 2022 – November 2024",
        "tech_stack": (
            "React &middot; TypeScript &middot; MongoDB &middot; Node.js "
            "&middot; Express.js &middot; Figma"
        ),
        "bullets": [
            (
                "Advocated for user-centric features throughout the discovery, design, and "
                "implementation phases"
            ),
            (
                "Collaborated with product manager and designer to ensure end-to-end feature delivery"
            ),
            (
                "Played a key role in the migration to an updated design system by replacing legacy components"
            ),
            (
                "Achieved significant reduction in application bugs, enhancing stability and user experience"
            ),
            (
                "Showcased front-end skills while contributing to back-end projects effectively"
            ),
        ],
    },
    {
        "company": "Ryan LLC - Global Tax Services",
        "location": "Remote",
        "role": "Full Stack Developer",
        "dates": "October 2019 – August 2022",
        "tech_stack": (
            "TypeScript &middot; Node.js &middot; Azure Functions &middot; C# "
            "&middot; .NET &middot; Cosmos DB"
        ),
        "bullets": [
            (
                "Contributed to the design, development, testing, and deployment of RyanMail, an "
                "event-driven microservices app facilitating mass physical mail sending through a "
                "third-party service"
            ),
            "Utilized NodeJS Azure Functions to establish a REST API for RyanMail",
            (
                "Managed PDF storage and processing for RyanMail using Azure Functions, Azure Queue "
                "Storage, and Azure Blob Storage"
            ),
            (
                "Collaborated with various teams to integrate the RyanMail client with another product"
            ),
            (
                "Implemented Azure ARM Templates to efficiently create and deploy the RyanMail infrastructure"
            ),
        ],
    },
    {
        "company": "Docutech",
        "location": "Remote",
        "role": "Software Engineer",
        "dates": "January 2018 – October 2019",
        "tech_stack": "React &middot; TypeScript &middot; .NET Core &middot; C#",
        "bullets": [
            (
                "Collaborated with product team and developers to execute user story-driven solutions"
            ),
            "Developed frontend using React and Typescript, and backend with C#",
            (
                "Architected microservices like email and document generation for enhanced platform structure"
            ),
            (
                "Designed tool to compare legacy and new document generation outputs for bug identification"
            ),
            (
                "Engaged in agile team practices such as code reviews, stand-ups, planning, backlog "
                "grooming, and retrospectives"
            ),
        ],
    },
    {
        "company": "Premier Performance Products",
        "location": "Remote",
        "role": "Software Developer",
        "dates": "January 2012 – January 2018",
        "tech_stack": "C# &middot; ASP.NET &middot; SQL &middot; JavaScript &middot; AWS &middot; AngularJS",
        "bullets": [
            (
                "Developed customer-facing C# and ASP.NET web application for aftermarket automotive parts "
                "ordering, displaying vehicle and product data and building and consuming REST APIs across "
                "customer and internal workflows"
            ),
            (
                "Built internal tooling for shipping operations and order processing, including REST API "
                "integrations streamlining eBay and Amazon orders into company order systems"
            ),
        ],
    },
]

PROJECTS_TEXT = (
    "Willmore Lumber Website — Designed and developed a responsive marketing website for a "
    "family-owned lumber business featuring custom product showcases, SEO optimization, and "
    "brand-aligned UI/UX."
)

doc = SimpleDocTemplate(
    str(pdf_path),
    pagesize=letter,
    leftMargin=PAGE_MARGIN,
    rightMargin=PAGE_MARGIN,
    topMargin=PAGE_MARGIN,
    bottomMargin=PAGE_MARGIN,
)

frame_width = doc.width

story = []

add_page_header(story, frame_width)

add_skills_section(story, SKILL_CATEGORIES)
story.append(Spacer(1, 2))

add_section_heading(story, frame_width, "EXPERIENCE")
for job in RECENT_JOBS:
    story.append(
        KeepTogether(
            build_job_block(
                frame_width,
                job["company"],
                job["location"],
                job["role"],
                job["dates"],
                job["bullets"],
                job.get("tech_stack"),
            )
        )
    )

add_section_heading(story, frame_width, "EDUCATION")
add_bullet(
    story,
    frame_width,
    "Brigham Young University–Idaho — B.S. Computer Information Technology",
)

add_section_heading(story, frame_width, "PROJECTS")
add_bullet(story, frame_width, PROJECTS_TEXT)

doc.build(story)

print(f"Created resume PDF: {pdf_path}")
