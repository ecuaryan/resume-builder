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


BODY_FONT_SIZE = 10
BODY_LEADING = 11.5
BULLET_SPACE_AFTER = 3
JOB_BLOCK_SPACER = 7
SECTION_PRE_SPACER = 3
SKILLS_TAIL_SPACER = 2
# Roles that ended before this year get no bullets (see PRIOR_EXPERIENCE_JOBS).
# 2019 ≈ 10-year window in 2026; raises cutoff to move older roles (e.g. Premier) to prior-only.
BULLET_CUTOFF_YEAR = 2019

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
    fontSize=BODY_FONT_SIZE,
    leading=BODY_LEADING,
    spaceAfter=1,
)

BULLET_MARKER_WIDTH = 14
BULLET_TEXT_GAP = 8


def _bullet_marker_style() -> ParagraphStyle:
    return _base_style(
        name="BulletMarker",
        fontName="Helvetica",
        fontSize=BODY_FONT_SIZE,
        leading=BODY_LEADING,
        alignment=TA_RIGHT,
        leftIndent=0,
        rightIndent=0,
    )


def _bullet_text_style() -> ParagraphStyle:
    return _base_style(
        name="BulletText",
        fontName="Helvetica",
        fontSize=BODY_FONT_SIZE,
        leading=BODY_LEADING,
        leftIndent=0,
        rightIndent=0,
        spaceAfter=BULLET_SPACE_AFTER,
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
        fontSize=BODY_FONT_SIZE,
        leading=BODY_LEADING,
        textColor=colors.HexColor("#475569"),
        leftIndent=0,
        rightIndent=0,
        spaceAfter=2,
    )


def _job_links_style() -> ParagraphStyle:
    return _base_style(
        name="JobLinks",
        fontName="Helvetica",
        fontSize=BODY_FONT_SIZE,
        leading=BODY_LEADING,
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
    contact_markup = (
        "<b>"
        '<a href="tel:+12083609649" color="black">(208) 360-9649</a>'
        " &middot; "
        '<a href="mailto:ryanwillmore@gmail.com" color="black">ryanwillmore@gmail.com</a>'
        " &middot; "
        '<a href="https://www.linkedin.com/in/ryan-willmore" color="black">'
        "linkedin.com/in/ryan-willmore</a></b>"
    )
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
    story.append(Spacer(1, SECTION_PRE_SPACER))
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
    links_line: str | None = None,
) -> list:
    inner_w = _inner_width(frame_width)
    header = _job_header_table(inner_w, company, location, role, dates)
    block = [_inset_wrapper(header, frame_width)]
    if links_line:
        block.append(
            _inset_wrapper(Paragraph(links_line, _job_links_style()), frame_width)
        )
    if tech_stack:
        block.append(
            _inset_wrapper(Paragraph(tech_stack, _job_tech_style()), frame_width)
        )
    for text in bullets:
        block.append(_bullet_row(frame_width, text))
    block.append(Spacer(1, JOB_BLOCK_SPACER))
    return block


def build_prior_experience_line(
    frame_width: float,
    company: str,
    role: str,
    dates: str,
) -> Table:
    """Single line: Company — Title (left), dates (right). No bullets."""
    inner_w = _inner_width(frame_width)
    left_w, right_w = _job_col_widths(inner_w)
    left_style = _job_header_left_style()
    right_style = _job_header_right_style()
    row = Table(
        [[
            Paragraph(f"<b>{company}</b> — {role}", left_style),
            Paragraph(dates, right_style),
        ]],
        colWidths=[left_w, right_w],
        hAlign="LEFT",
    )
    row.setStyle(
        TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ("TOPPADDING", (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ])
    )
    return _inset_wrapper(row, frame_width)


SKILL_CATEGORIES = {
    "Languages": "TypeScript, JavaScript, C#, SQL",
    "Frontend": "React, HTML, CSS, Angular",
    "Backend & APIs": "Node.js, Express.js, REST APIs, Microservices, GraphQL, .NET",
    "Cloud & Infrastructure": (
        "Amazon Bedrock AgentCore, AWS (Lambda, API Gateway), Azure Functions, Serverless"
    ),
    "Databases": "DynamoDB, Postgres, MongoDB, Cosmos DB",
    "Tools": "Datadog, Jest, Git, CI/CD",
}

EXPERIENCE_JOBS = [
    {
        "company": "Pie Insurance",
        "location": "Remote",
        "role": "Senior Software Engineer",
        "dates": "January 2025 – May 2026",
        "end_year": 2026,
        "tech_stack": (
            "Amazon Bedrock AgentCore &middot; AWS &middot; TypeScript &middot; GraphQL "
            "&middot; Node.js &middot; Express.js &middot; DynamoDB "
            "&middot; Datadog &middot; Postgres"
        ),
        "bullets": [
            (
                "Led development of an AI-powered Rate Update Agent using Amazon Bedrock AgentCore to "
                "automate rate file processing and GitHub PR generation from Jira tickets, replacing 40+ "
                "manual updates per year that each consumed days of developer time with ~4-minute automated runs"
            ),
            (
                "Senior engineer on pricing team, owning TypeScript/AWS serverless "
                "services, GraphQL APIs, and production pricing workflows in Kanban delivery cadence"
            ),
            (
                "Oversaw migration of Go-based microservice to TypeScript/Node.js with API Gateway "
                "integration, DynamoDB caching, smoke tests, SDK generation, and migration documentation, "
                "reducing operational complexity across pricing services"
            ),
            (
                "Managed pricing infrastructure for Workers' Comp and Commercial Auto on TypeScript/AWS "
                "serverless stack, supporting rate changes, billing integrations, and production observability "
                "via Datadog"
            ),
            (
                "Implemented pricing enhancements across multiple repositories, REST/GraphQL APIs, "
                "and schemas under tight delivery timelines, unblocking a billing effort that would "
                "save the company thousands of dollars per day"
            ),
        ],
    },
    {
        "company": "Retrium",
        "location": "Remote",
        "role": "Software Engineer",
        "dates": "August 2022 – November 2024",
        "end_year": 2024,
        "tech_stack": (
            "React &middot; TypeScript &middot; MongoDB &middot; Node.js "
            "&middot; Express.js &middot; Figma"
        ),
        "bullets": [
            (
                "Full-stack engineer on SaaS retrospective and agile collaboration product, delivering "
                "React/TypeScript UI and Node.js/Express/MongoDB features with product and design partners "
                "through discovery, delivery, and production support"
            ),
            (
                "Partnered with product manager and designer on end-to-end feature delivery, translating "
                "user research into scoped stories, UI specs, and shippable increments across core workflow "
                "surfaces"
            ),
            (
                "Drove migration to updated design system by replacing legacy React components, improving "
                "UI consistency and reducing design-debt friction for new feature development"
            ),
            (
                "Reduced recurring application defects through targeted refactors, test coverage, and "
                "component standardization, improving stability and customer-facing reliability"
            ),
        ],
    },
    {
        "company": "Ryan LLC - Global Tax Services",
        "location": "Remote",
        "role": "Full Stack Developer",
        "dates": "October 2019 – August 2022",
        "end_year": 2022,
        "tech_stack": (
            "TypeScript &middot; Node.js &middot; Azure Functions &middot; C# "
            "&middot; .NET &middot; Cosmos DB"
        ),
        "bullets": [
            (
                "Full-stack developer on RyanMail event-driven microservices platform for enterprise tax "
                "services, building TypeScript Node.js Azure Functions, C#/.NET services, and Cosmos DB "
                "integrations supporting high-volume physical mail workflows"
            ),
            (
                "Designed, built, tested, and deployed RyanMail capabilities end-to-end, coordinating REST APIs, "
                "queue-driven processing, and third-party mail provider integrations used by internal operations "
                "teams"
            ),
            (
                "Built Node.js Azure Functions REST API and PDF pipeline using Queue Storage and Blob Storage, "
                "enabling reliable document generation, storage, and retrieval across distributed mail batches"
            ),
            (
                "Integrated RyanMail client with adjacent product teams and platforms, aligning authentication, "
                "configuration, and deployment patterns for cross-product adoption"
            ),
            (
                "Authored Azure ARM templates for repeatable RyanMail infrastructure provisioning and deployment, "
                "shortening environment setup and reducing manual configuration errors"
            ),
        ],
    },
    {
        "company": "Docutech",
        "location": "Remote",
        "role": "Software Engineer",
        "dates": "January 2018 – October 2019",
        "end_year": 2019,
        "tech_stack": "React &middot; TypeScript &middot; .NET Core &middot; C#",
        "bullets": [
            (
                "Software engineer on mortgage document technology platform, building React/TypeScript frontends "
                "and C#/.NET Core microservices for document generation, email delivery, and lender integrations "
                "in Agile team"
            ),
            (
                "Delivered user story-driven features with product and engineering peers across React UI, service "
                "layer APIs, and PDF document workflows, participating in code reviews, sprint planning, and "
                "retrospectives on compliance-sensitive releases"
            ),
            (
                "Architected email and document generation microservices, decomposing legacy monolith capabilities "
                "into independently deployable services and improving platform maintainability"
            ),
            (
                "Built comparison tooling for legacy vs. new document generation outputs, accelerating defect "
                "detection during migrations and reducing production document mismatches"
            ),
        ],
    },
    {
        "company": "Premier Performance Products",
        "location": "Remote",
        "role": "Software Developer",
        "dates": "January 2012 – January 2018",
        "end_year": 2018,
        "tech_stack": None,
        "bullets": [],
    },
]

PRIOR_EXPERIENCE_JOBS = [
    job
    for job in EXPERIENCE_JOBS
    if job["end_year"] < BULLET_CUTOFF_YEAR
]

RECENT_JOBS = [
    job for job in EXPERIENCE_JOBS if job["end_year"] >= BULLET_CUTOFF_YEAR
]

PROJECT_JOB = {
    "company": "Willmore Lumber",
    "location": "Personal Project",
    "role": "Marketing Website",
    "links_line": (
        '<a href="https://willmorelumber.com" color="black">willmorelumber.com</a>'
        ' &middot; '
        '<a href="https://github.com/ecuaryan/willmore-lumber" color="black">'
        "github.com/ecuaryan/willmore-lumber</a>"
    ),
    "dates": "",
    "tech_stack": (
        "Next.js 15 &middot; React 19 &middot; TypeScript &middot; Material UI "
        "&middot; Swiper &middot; GitHub Pages &middot; GitHub Actions"
    ),
    "bullets": [
        (
            "Built marketing website for family-run lumber mill (50+ years in business per site content), using "
            "Next.js 15 App Router with static export, 17 routed pages across products, services, pricing, "
            "gallery, and contact, and responsive MUI navigation with drawer-based nested menus"
        ),
        (
            "Delivered custom MUI theme and shared layout components, home-page Swiper product showcase and "
            "testimonial carousels, lazy-loaded gallery with Google Photos link, and GitHub Actions pipeline "
            "deploying static build to GitHub Pages at willmorelumber.com"
        ),
        (
            "Configured root metadata, robots.txt, web app manifest, and mixed WebP/JPEG assets with lazy loading, "
            "producing maintainable static site without CMS or backend for customers browsing on mobile devices"
        ),
    ],
}

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
story.append(Spacer(1, SKILLS_TAIL_SPACER))

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

if PRIOR_EXPERIENCE_JOBS:
    add_section_heading(story, frame_width, "PRIOR EXPERIENCE")
    for job in PRIOR_EXPERIENCE_JOBS:
        story.append(
            build_prior_experience_line(
                frame_width,
                job["company"],
                job["role"],
                job["dates"],
            )
        )
    story.append(Spacer(1, 2))

add_section_heading(story, frame_width, "EDUCATION")
add_bullet(
    story,
    frame_width,
    "Brigham Young University–Idaho — B.S. Computer Information Technology",
)
story.append(Spacer(1, JOB_BLOCK_SPACER))

add_section_heading(story, frame_width, "PROJECTS")
story.append(
    KeepTogether(
        build_job_block(
            frame_width,
            PROJECT_JOB["company"],
            PROJECT_JOB["location"],
            PROJECT_JOB["role"],
            PROJECT_JOB["dates"],
            PROJECT_JOB["bullets"],
            PROJECT_JOB.get("tech_stack"),
            PROJECT_JOB.get("links_line"),
        )
    )
)

doc.build(story)

print(f"Created resume PDF: {pdf_path}")
