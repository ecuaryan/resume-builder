from pathlib import Path

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, ListFlowable, ListItem, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch

OUTPUT_DIR = Path(__file__).resolve().parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)
pdf_path = OUTPUT_DIR / "Ryan_Willmore_Resume.pdf"

doc = SimpleDocTemplate(
    str(pdf_path),
    pagesize=letter,
    rightMargin=0.55 * inch,
    leftMargin=0.55 * inch,
    topMargin=0.55 * inch,
    bottomMargin=0.55 * inch,
)

styles = getSampleStyleSheet()

name_style = ParagraphStyle(
    "Name",
    parent=styles["Heading1"],
    fontSize=24,
    leading=28,
    textColor=colors.HexColor("#1E293B"),
    spaceAfter=4,
)

contact_style = ParagraphStyle(
    "Contact",
    parent=styles["BodyText"],
    fontSize=9.5,
    leading=12,
    textColor=colors.HexColor("#475569"),
)

section_style = ParagraphStyle(
    "Section",
    parent=styles["Heading2"],
    fontSize=11,
    leading=14,
    textColor=colors.HexColor("#0F172A"),
    spaceBefore=12,
    spaceAfter=6,
)

summary_style = ParagraphStyle(
    "Summary",
    parent=styles["BodyText"],
    fontSize=10,
    leading=15,
    textColor=colors.HexColor("#334155"),
)

job_title_style = ParagraphStyle(
    "JobTitle",
    parent=styles["BodyText"],
    fontSize=11,
    leading=14,
    textColor=colors.HexColor("#111827"),
)

body_style = ParagraphStyle(
    "Body",
    parent=styles["BodyText"],
    fontSize=9.5,
    leading=14,
    textColor=colors.HexColor("#374151"),
)

tech_style = ParagraphStyle(
    "Tech",
    parent=styles["BodyText"],
    fontSize=8.8,
    leading=12,
    textColor=colors.HexColor("#475569"),
)

story = []

story.append(Paragraph("Ryan Willmore", name_style))
story.append(
    Paragraph(
        "Rexburg, Idaho &nbsp;&nbsp;•&nbsp;&nbsp; ryanwillmore@gmail.com &nbsp;&nbsp;•&nbsp;&nbsp; (208) 360-9649<br/>"
        "linkedin.com/in/ryan-willmore &nbsp;&nbsp;",
        contact_style,
    )
)

story.append(Spacer(1, 10))
story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#CBD5E1")))

story.append(Paragraph("PROFESSIONAL SUMMARY", section_style))

summary = """
Senior Software Engineer with 10+ years of experience building scalable full-stack applications across insurtech, SaaS, and enterprise platforms. 
Experienced in TypeScript, React, Node.js, AWS serverless architectures, GraphQL, and distributed systems. 
Strong collaborator who enjoys working closely with product and design teams to deliver reliable, polished software that creates meaningful value for users.
"""

story.append(Paragraph(summary, summary_style))

story.append(Paragraph("CORE TECHNOLOGIES", section_style))

skills_data = [
    ["Languages", "TypeScript, JavaScript, C#, SQL"],
    ["Frontend", "React, HTML, CSS, Angular"],
    ["Backend & APIs", "Node.js, Express.js, .NET, GraphQL, REST APIs, Microservices"],
    ["Cloud & Infrastructure", "AWS, Lambda, DynamoDB, API Gateway, Azure Functions, Cosmos DB, Postgres"],
    ["Tools", "Datadog, Jest, Git, CI/CD"],
]

skills_table = Table(skills_data, colWidths=[1.6 * inch, 5.5 * inch])
skills_table.setStyle(
    TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("TEXTCOLOR", (0, 0), (-1, -1), colors.HexColor("#334155")),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
    ])
)

story.append(skills_table)

story.append(Paragraph("PROFESSIONAL EXPERIENCE", section_style))

jobs = [
    {
        "role": "Senior Software Engineer",
        "company": "Pie Insurance",
        "dates": "Jan 2025 – May 2026",
        "tech": "TypeScript • AWS • GraphQL • Node.js • Express.js • Serverless • DynamoDB • Datadog  • Postgres",
        "bullets": [
            "Led development of an AI-powered Rate Update Agent using Amazon Bedrock AgentCore to automate rate file processing and GitHub PR generation",
            "Managed pricing infrastructure for Workers' Comp and Commercial Auto using a TypeScript/AWS serverless stack",
            "Oversaw migration of a Go-based microservice to TypeScript/Node.js, including API Gateway integration, DynamoDB caching, smoke tests, SDK generation, and migration documentation",
            "Implemented rating and billing enhancements across multiple repositories, APIs, and GraphQL schemas under tight delivery timelines",
        ]
    },
    {
        "role": "Software Engineer",
        "company": "Retrium",
        "dates": "Aug 2022 – Nov 2024",
        "tech": "React • TypeScript • MongoDB • Node.js • Express.js • Figma",
        "bullets": [
            "Advocated for user-centric features throughout the discovery, design, and implementation phases",
            "Collaborated with product manager and designer to ensure end-to-end feature delivery",
            "Played a key role in the migration to an updated design system by replacing legacy components",
            "Achieved significant reduction in application bugs, enhancing stability and user experience",
            "Showcased front-end skills while contributing to back-end projects effectively",
        ]
    },
    {
        "role": "Full Stack Developer",
        "company": "Ryan LLC - Global Tax Services",
        "dates": "Oct 2019 – Aug 2022",
        "tech": "TypeScript • Node.js • Azure Functions • C# • .NET • Cosmos DB",
        "bullets": [
            "Contributed to the design, development, testing, and deployment of RyanMail, an event-driven microservices app facilitating mass physical mail sending through a third-party service",
            "Utilized NodeJS Azure Functions to establish a REST API for RyanMail",
            "Managed PDF storage and processing for RyanMail using Azure Functions, Azure Queue Storage, and Azure Blob Storage",
            "Collaborated with various teams to integrate the RyanMail client with another product",
            "Implemented Azure ARM Templates to efficiently create and deploy the RyanMail infrastructure",
        ]
    },
    {
        "role": "Software Engineer",
        "company": "Docutech",
        "dates": "Jan 2018 – Oct 2019",
        "tech": "React • TypeScript • .NET Core • C#",
        "bullets": [
            "Collaborated with product team and developers to execute user story-driven solutions",
            "Developed frontend using React and Typescript, and backend with C#",
            "Architected microservices like email and document generation for enhanced platform structure",
            "Designed tool to compare legacy and new document generation outputs for bug identification",
            "Engaged in agile team practices such as code reviews, stand-ups, planning, backlog grooming, and retrospectives",
        ]
    },
    {
        "role": "Software Developer",
        "company": "Premier Performance Products",
        "dates": "Jan 2012 – Jan 2018",
        "tech": "C# • ASP.NET • SQL • JavaScript • AWS • AngularJS",
        "bullets": [
            "Developed and implemented new API endpoints",
            "Evaluated project needs by collaborating with customers and stakeholders",
            "Mentored fellow developers to offer guidance",
            "Gathered feedback to improve customer satisfaction",
            "Designed applications for streamlined order processing on eBay and Amazon",
            "Assisted in website migrations and integrated tools/systems (Magento, PHP) after company acquisitions",
        ]
    },
]

for job in jobs:
    story.append(
        Paragraph(
            f"<b>{job['role']}</b> &nbsp;&nbsp;|&nbsp;&nbsp; {job['company']} &nbsp;&nbsp;<font color='#64748B'>{job['dates']}</font>",
            job_title_style
        )
    )
    story.append(Paragraph(job["tech"], tech_style))

    bullets = [ListItem(Paragraph(b, body_style)) for b in job["bullets"]]

    story.append(
        ListFlowable(
            bullets,
            bulletType="bullet",
            leftIndent=18,
        )
    )

    story.append(Spacer(1, 6))

story.append(Paragraph("PROJECTS", section_style))

project_text = """
<b>Willmore Lumber Website</b> — Designed and developed a responsive marketing website for a family-owned lumber business featuring custom product showcases, SEO optimization, and brand-aligned UI/UX.
"""

story.append(Paragraph(project_text, body_style))

story.append(Paragraph("EDUCATION", section_style))

education = """
<b>Brigham Young University–Idaho</b> — B.S. Computer Information Technology<br/>
<b>Utah State University</b> — Electrical Engineering and Computer Science coursework
"""

story.append(Paragraph(education, body_style))

doc.build(story)

print(f"Created refined resume PDF: {pdf_path}")