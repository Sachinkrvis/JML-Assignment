from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
import os

train_number = "12309"
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = os.path.dirname(BASE_PATH)
output_base = os.path.join(ROOT_PATH, "processed_video", f"{train_number}")

pdf_path = os.path.join(output_base, f"{train_number}_wagon_report.pdf")

doc = SimpleDocTemplate(pdf_path)
styles = getSampleStyleSheet()
elements = []

# Title
elements.append(Paragraph(f"Train {train_number} – Side View Report", styles['Title']))
elements.append(Spacer(1, 20))

# Collect coach folders and sort numerically
coach_folders = [
    folder for folder in os.listdir(output_base)
    if folder.startswith(train_number + "_") and os.path.isdir(os.path.join(output_base, folder))
]

# Sort by numeric part after the underscore
coach_folders.sort(key=lambda f: int(f.split("_")[-1]))

# Loop over sorted coach folders
# Loop over sorted coach folders
for folder in coach_folders:
    coach_id = folder.split("_")[-1]
    coach_folder = os.path.join(output_base, folder)

    # Special case: if coach_id == "1" → Engine
    if coach_id == "1":
        heading = "Engine"
    else:
        heading = f"Wagon {int(coach_id) - 1}"

    elements.append(Paragraph(heading, styles['Heading2']))
    elements.append(Spacer(1, 10))

    # Add up to 2 screenshots
    for i in range(1, 3):
        img_path = os.path.join(coach_folder, f"{train_number}_{coach_id}_{i}.jpg")
        if os.path.exists(img_path):
            elements.append(Image(img_path, width=400, height=200))
            elements.append(Spacer(1, 5))

    elements.append(Spacer(1, 20))

# for folder in coach_folders:
#     coach_id = folder.split("_")[-1]
#     coach_folder = os.path.join(output_base, folder)

#     elements.append(Paragraph(f"Wagon {coach_id}", styles['Heading2']))
#     elements.append(Spacer(1, 10))

#     # Add up to 2 screenshots
#     for i in range(1, 3):
#         img_path = os.path.join(coach_folder, f"{train_number}_{coach_id}_{i}.jpg")
#         if os.path.exists(img_path):
#             elements.append(Image(img_path, width=400, height=200))
#             elements.append(Spacer(1, 5))

#     elements.append(Spacer(1, 20))

# Build the PDF
doc.build(elements)
print(f"✅ Wagon Report PDF generated: {pdf_path}")

