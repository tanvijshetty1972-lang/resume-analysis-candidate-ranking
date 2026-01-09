# Automated Resume Analysis, Scoring, and Candidate Ranking using AI & NLP

## Project Overview
Manual resume screening is time-consuming and prone to human bias. This project automates the process using AI and NLP by:

- Extracting skills, experience, certifications, projects, and extra-curricular activities from resumes
- Comparing resumes with job descriptions to calculate a weighted AI score
- Providing AI-based recommendations and visual dashboards
- Supporting any resume format (PDF/DOCX) and any job description format (TXT/DOCX)

The system helps recruiters save time and ensures objective candidate evaluation.

## Features
- **Universal File Support:** PDF, DOCX, TXT  
- **Skills Extraction:** Predefined skill set with multi-word matching  
- **Experience Calculation:** Total experience computed automatically  
- **Project & Internship Detection**  
- **Extra-Curricular & Certifications Detection**  
- **Semantic Similarity Matching:** Using BERT embeddings  
- **Weighted AI Score Calculation:** Skills, experience, certifications, projects, semantic similarity  
- **Visual Dashboard:** Charts, scorecards, and recommendations  

## Installation & Setup
1. Clone the repository:
    ```bash
    git clone https://github.com/YourUsername/AI-Resume-Screening.git
    cd AI-Resume-Screening
    ```
2. Create a virtual environment (optional but recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/Mac
    venv\Scripts\activate     # Windows
    ```
3. Install required packages:
    ```bash
    pip install -r requirements.txt
    ```
4. Run the Streamlit app:
    ```bash
    streamlit run dashboard/dashboard.py
    ```

## Folder Structure
````

AI-Resume-Screening/
│
├─ dashboard/
│   └─ dashboard.py           # Streamlit dashboard
│
├─ utils/
│   ├─ resume_parser.py       # Extract text from resumes & JDs
│   ├─ skill_extractor.py     # Extract skills
│   ├─ skill.py               # Skill list & helpers
│   ├─ ai_matcher.py          # Semantic similarity & AI score
│
├─ requirements.txt           # Python dependencies
└─ README.md                  # Project documentation

````

## Usage
1. Upload a candidate resume (PDF/DOCX)  
2. Upload a job description (TXT/DOCX)  

The app extracts:

- Skills  
- Experience  
- Certifications  
- Projects  
- Extra-curricular activities  

AI Score is computed and displayed along with recommendations.  
Interactive dashboard shows charts for easy interpretation.

## AI Scoring System
| Component             | Weight |
|----------------------|--------|
| Skills Match          | 35%    |
| Semantic Similarity   | 25%    |
| Experience            | 20%    |
| Certifications        | 10%    |
| Projects              | 5%     |
| Extra-Curricular      | 5%     |

**Score Interpretation:**

- ≥75% → Strong Match  
- 50–74% → Partial Match  
- <50% → Not suitable  

**Sample Output:**

- Skills Extracted: ["python", "java", "aws"]  
- Experience: 3.7 years  
- Certifications: ["AWS", "Power BI"]  
- Projects: 3 projects detected  
- Extra-Curricular: 2 achievements  
- AI Score: 78% → Strong Match  
- Suggestions: Gain experience in missing skills (React, TensorFlow)  

## Dependencies
- Python 3.12  
- Streamlit  
- pdfplumber  
- python-docx  
- pandas, numpy, matplotlib  
- regex, dateutil  
- sentence-transformers  
- Plotly  

Install all dependencies using:
```bash
pip install -r requirements.txt
````

## Future Enhancements

* Batch resume processing
* PDF report generation for candidates
* Multi-language resume support
* Integration with ATS (Applicant Tracking Systems)

## Contributors

* **Tanvi J Shetty** – Developer

## License

This project is licensed under the MIT License – see the LICENSE file for details.



