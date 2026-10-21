# French Municipal Elections 2026 – Second Round


## Live Dashboard

The Streamlit dashboard is available online:

https://french-municipal-elections-2026-hpyeu7oyxa4zqtpvfr8xny.streamlit.app/

## GitHub Repository

https://github.com/Lucie123456789/french-municipal-elections-2026

## Demo Video

Watch the dashboard demonstration here :

https://drive.google.com/file/d/1pawzmkdCyulFnY7M67RLO5SPcWZ_Bsf5/view?usp=sharing

## 1. Project Overview

This project is an interactive data storytelling dashboard developed with Python and Streamlit.

It analyzes voter participation during the second round of the 2026 French municipal elections.

The main goal is to explore differences in voter turnout between French departments, municipalities and polling stations.

### Main Research Question

**Do people vote more in some French cities and departments than in others ?**

The dashboard uses interactive maps, rankings and statistical charts to compare voter participation and highlight the main differences.

## 2. Project Objectives

The main objectives are to :

- Calculate voter turnout and abstention rates.
- Compare participation between French departments and municipalities.
- Identify areas with the highest and lowest turnout rates.
- Explore how turnout rates are distributed across polling stations.
- Compare participation differences within departments.
- Check data quality and identify unusual values.
- Interpret the results and explain the limitations of the analysis.

## 3. Dataset

### Data Source

The project uses public election data from the second round of the 2026 French municipal elections.

- **Source :** French Government Open Data Portal (data.gouv.fr)
- **Website :** https://www.data.gouv.fr/
- **Dataset :** [French Municipal Elections 2026 – Second Round](https://explore.data.gouv.fr/fr/datasets/6481e741d4cf002ec0efec9d/?id_election__exact=2026_muni_t2#/resources/b8703c69-a18f-46ab-9e7f-3a8368dcb891)
- **Local file :** `data/elections_2026.csv`
- **Geographical boundaries :** `data/departements.geojson`
- **GeoJSON source :** https://github.com/gregoiredavid/france-geojson

The election dataset contains information about registered voters, total voters, abstentions, blank ballots, invalid ballots and valid votes.

**Important :** The dataset only covers the second round of the elections. Not all French municipalities are represented.

### Main Variables

| Variable | Description |
|---|---|
| `libelle_departement` | Department name |
| `code_departement` | Department code |
| `libelle_commune` | Municipality name |
| `code_commune` | Municipality code, when available |
| `inscrits` | Number of registered voters |
| `votants` | Number of voters |
| `abstentions` | Number of abstentions |
| `blancs` | Number of blank ballots |
| `nuls` | Number of invalid ballots |
| `exprimes` | Number of valid votes |

### Data License

The election data is published by the French Ministry of the Interior
under the Licence Ouverte / Open Licence version 2.0.

Source : https://www.data.gouv.fr/datasets/elections-municipales-2026-resultats-du-second-tour

## 4. Data Preparation

The dataset is loaded and cleaned using Pandas.

The cleaning process includes :

1. Removing duplicate rows.
2. Removing records with missing registered-voter or voter counts.
3. Removing records where the number of registered voters is zero or negative.
4. Removing records where the number of voters is negative or greater than the number of registered voters.
5. Calculating turnout and abstention rates.

### Calculated Variables

**Turnout Rate (%)**

Turnout Rate = (Voters / Registered Voters) × 100

**Abstention Rate (%)**

Abstention Rate = 100 − Turnout Rate

For departments and municipalities, turnout rates are calculated by dividing the total number of voters by the total number of registered voters.

This method takes into account differences in the number of registered voters between polling stations.

The original dataset is also used for data quality checks, independently of the sidebar filters.

## 5. Data Storytelling Approach

The dashboard follows a simple storytelling structure :

**Question → Exploration → Results → Conclusion**

Two main approaches are used.

### Geographical Comparisons

The map and rankings help compare turnout between departments and municipalities.

### Distribution and Variability

The density curve and box plots show how turnout varies between polling stations, including typical values and unusual results.

Each visualization includes a short interpretation to help users understand the results.

## 6. Dashboard Features

### Introduction

The introduction presents the election context, the importance of voter participation and the main research question.

It also includes information about the dataset and the project objectives.

### Election Overview

Four Key Performance Indicators (KPIs) are displayed :

- Registered Voters
- Total Voters
- Turnout Rate
- Abstention Rate

The dashboard also provides a short interpretation of overall participation.

A data preview and detailed quality checks are available in expandable sections.

### Geographical Analysis

An interactive map displays turnout rates across the departments represented in the dataset.

The map uses a purple color scale :

- Light purple represents lower turnout.
- Dark purple represents higher turnout.

Users can hover over departments to see their turnout rates and voting statistics.

The dashboard also displays :

- The Top 3 departments with the highest turnout.
- The Bottom 3 departments with the lowest turnout.
- The difference between the highest and lowest department turnout rates.
- The overall turnout rate for comparison.

### Department Ranking

A horizontal bar chart compares department turnout rates.

Three options are available :

- Top 10
- Bottom 10
- All Departments

The Key Insight changes automatically depending on the selected ranking.

For the Top 10 and Bottom 10, the analysis identifies the highest or lowest turnout and the range of results.

For All Departments, it compares department turnout rates with the overall participation rate.

### Municipality Ranking

An interactive lollipop chart compares municipality turnout rates.

Users can choose between :

- Top 10 municipalities
- Bottom 10 municipalities

The dashboard groups polling-station results by municipality before calculating turnout rates.

A dynamic Key Insight explains the results of the selected ranking.

### Turnout Distribution

A density curve shows how polling-station turnout rates are distributed.

The chart includes a vertical line representing the median turnout rate.

Three additional indicators are displayed :

- Median
- Minimum
- Maximum

The interpretation explains where most turnout rates are concentrated and highlights unusual values.

### Participation Variability

Horizontal box plots compare turnout rates between polling stations in different departments.

Users can select which departments they want to compare.

The dashboard calculates :

- Median turnout.
- First quartile
- Third quartile
- Interquartile range

The Key Insight identifies the department with the highest median turnout and the department with the greatest variation among the middle 50% of polling stations.

### Data Quality & Limitations

The dashboard checks :

- Missing values.
- Duplicate rows.
- Invalid voting records.

These checks use the original dataset before cleaning.

The dashboard also explains what the results mean and presents the main limitations in a single dark purple section.

### Key Findings

The final analysis summarizes three main results :

1. Differences in turnout between departments.
2. Overall participation and median polling-station turnout.
3. The distribution of turnout rates across polling stations.

The analysis uses simple explanations supported by the calculated statistics.

### Possible Explanations

The dashboard discusses factors that could influence participation, such as age, income, education and local political competition.

These are possible explanations, not confirmed causes, because the dataset does not contain enough information to test them.

### Conclusion

The conclusion answers the main research question and explains why looking at local turnout rates provides more information than the overall participation rate alone.

## 7. Interactive Filters

The sidebar contains two main filters :

- Department selection.
- Municipality selection.

Users can explore the complete dataset or focus on specific areas.

The dashboard automatically updates the KPIs, charts and relevant interpretations when filters are applied.

The Participation Variability section also includes a department comparison selector.

## 8. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Streamlit | Interactive dashboard |
| Pandas | Data loading, cleaning and grouping |
| NumPy | Numerical calculations and density estimation |
| Plotly | Interactive charts and geographical map |
| GeoJSON | Department boundaries |
| HTML/CSS | Custom purple insight and limitation sections |

Streamlit caching is used to avoid repeatedly loading and processing the same data.

## 9. Project Structure

```text
Streamlit_Project/
│
├── app.py
├── requirements.txt
├── README.md
│
├── assets/
│   └── efrei.png
│
├── data/
│   ├── elections_2026.csv
│   └── departements.geojson
│
├── sections/
│   ├── intro.py
│   ├── overview.py
│   ├── deep_dives.py
│   └── conclusions.py
│
└── utils/
    ├── io.py
    ├── prep.py
    ├── viz.py
    └── styles.py
```

### Main Python Files

| File | Purpose |
|---|---|
| `app.py` | Main application, sidebar filters and page layout |
| `sections/intro.py` | Introduction and research question |
| `sections/overview.py` | Election KPIs and dataset preview |
| `sections/deep_dives.py` | Interactive visualizations and their interpretations |
| `sections/conclusions.py` | Data quality, limitations, findings and conclusion |
| `utils/io.py` | Load the election CSV |
| `utils/prep.py` | Clean data and calculate turnout rates |
| `utils/viz.py` | Create maps, rankings, distribution charts and box plots |
| `utils/styles.py` | Create custom purple Key Insight and Data Limitation boxes |

## 10. Installation and Execution

### Step 1 : Download the Project

Download the project ZIP file and extract it.

### Step 2 : Open the Project Folder

Open the folder in VS Code.

### Step 3 : Create a Virtual Environment

```bash
python -m venv .venv
```

Activate the environment on Windows :

```powershell
.venv\Scripts\Activate.ps1
```

### Step 4 : Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### Step 5 : Run the Dashboard

```bash
python -m streamlit run app.py
```

The dashboard opens in a web browser.

## 11. Data Quality and Limitations

The analysis has several limitations.

- **Second-round coverage :** Not all French municipalities held a second round, so the dataset does not cover every municipality.
- **Missing values :** Some cells are empty. These values do not necessarily concern the columns used for turnout calculations.
- **Invalid records :** Records with missing or impossible voting numbers must be excluded from the analysis.
- **Polling-station size :** Small polling stations can have unusually high or low turnout rates.
- **Geographical differences :** Department-level results can hide differences between municipalities and polling stations.
- **Possible causes :** The dataset shows where participation differs but cannot explain why.
- **Filters :** When filters are applied, results only describe the selected areas.
- **Density curve :** The curve is a smoothed representation of turnout rates, not an exact count of polling stations.

These limitations are important when interpreting the results.

## 12. Key Takeaways

The dashboard shows that voter participation was not the same across the French departments and municipalities represented in the second-round dataset.

The geographical map and rankings highlight areas with higher and lower turnout rates.

The distribution curve shows where polling-station turnout rates are concentrated, while the box plots reveal differences within departments.

The overall turnout rate provides a general picture, but local comparisons help show differences that are not visible in a single percentage.

## 13. Future Improvements

Possible improvements include :

- Comparing the first and second election rounds.
- Adding demographic and economic data.
- Comparing turnout according to municipality population size.
- Investigating unusual turnout values.
- Improving geographical comparisons.

## 14. Author

**Lucie Ozgullu**

EFREI Paris – Engineering Student

Data Engineering – Class of 2028

Course : Data Analysis & Visualization

Professor : Mano Joseph Mathew

GitHub : https://github.com/Lucie123456789