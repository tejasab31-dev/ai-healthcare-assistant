from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime


def generate_pdf(disease, confidence, ai_advice):

    filename = "health_report.pdf"

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    story = []

    story.append(
        Paragraph(
            "Healthcare AI Prediction Report",
            styles["Title"]
        )
    )

    story.append(Spacer(1, 12))

    story.append(
        Paragraph(
            f"Generated On: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            styles["Normal"]
        )
    )

    story.append(Spacer(1, 12))

    story.append(
        Paragraph(
            f"<b>Predicted Disease:</b> {disease}",
            styles["Heading2"]
        )
    )

    story.append(Spacer(1, 8))

    story.append(
        Paragraph(
            f"<b>Confidence Score:</b> {confidence}%",
            styles["Heading2"]
        )
    )

    story.append(Spacer(1, 12))

    story.append(
        Paragraph(
            "<b>AI Health Advice</b>",
            styles["Heading2"]
        )
    )

    story.append(Spacer(1, 8))

    story.append(
        Paragraph(
            ai_advice.replace("\n", "<br/>"),
            styles["BodyText"]
        )
    )

    doc.build(story)

    return filename