# 🚆 Train Wagon Video Processing Pipeline  

This project processes train side-view/bottom-view videos to automatically:  
1. Split the full train video into smaller videos of individual coaches.  
2. Detect gaps between wagons using a dark rectangular region.  
3. Capture representative screenshots (first & mid frame) of each coach.  
4. Generate a structured PDF report summarizing all wagons with their images.  

---

## 📂 Project Structure  
Assignment/
│── app.py # Main pipeline runner
│── requirements.txt # Python dependencies
│── scripts/
│ ├── rect_selector.py # GUI tool to select black region (ROI)
│ ├── rect.json # Saved rectangle coordinates
│ ├── split_by_black_region.py # Splits video by coach & saves screenshots
│ └── generate_report.py # Builds PDF report of wagons
│── Raw_video/
│ └── input_video.mp4 # Input train video
│── Processed_Video/
│ └── 12309/ # Output: split videos + screenshots + PDF


---

## ⚙️ Setup  

1. Clone/download this repository.  
2. Install dependencies (preferably in a virtual environment):  

```bash
pip install -r requirements.txt


python scripts/rect_selector.py


python app.py


Processed_Video/12309/
│── 12309_1/
│   ├── 12309_1.mp4
│   ├── 12309_1_1.jpg   # first frame
│   └── 12309_1_2.jpg   # mid frame
│── 12309_2/ ...
│── 12309_3/ ...
│── 12309_wagon_report.pdf   # compiled PDF
