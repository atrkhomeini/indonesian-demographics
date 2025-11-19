# 🇮🇩 Indonesia Demographics - Market Intelligence

> Transforming demographic data into actionable business insights

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13+-316192.svg)](https://www.postgresql.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 📋 Overview

A data science project that analyzes Indonesian demographic trends (TFR, ASFR, expenditure) to provide market intelligence for business decision-making. The project uses time series forecasting and quadrant analysis to identify high-potential markets.

### Key Features

- 📊 **Time Series Forecasting**: ARIMA models for expenditure prediction (2010-2030)
- 🎯 **Market Segmentation**: Quadrant analysis (Stars, Cash Cows, Developing, Saturated)
- 🗺️ **Granular Analysis**: Kabupaten/Kota level insights (500+ regions)
- 🗄️ **PostgreSQL Backend**: Structured data storage and efficient querying
- 📈 **Professional Visualizations**: Publication-ready plots and charts

## 🚀 Quick Start

### 🛠️ Tech Stack

| Category          | Technologies |
|-------------------|--------------|
| **Core Language** | [![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/) |
| **Database**      | [![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13+-316192.svg)](https://www.postgresql.org/) |
| **Data Science**  | [![Pandas](https://img.shields.io/badge/Pandas-1.5+-150458.svg)](https://pandas.pydata.org/) [![NumPy](https://img.shields.io/badge/NumPy-1.24+-013243.svg)](https://numpy.org/) [![Scikit-learn](https://img.shields.io/badge/scikit--learn-1.3+-F7931E.svg)](https://scikit-learn.org/) [![Statsmodels](https://img.shields.io/badge/Statsmodels-0.14+-8A2BE2.svg)](https://www.statsmodels.org/) |
| **Visualization** | [![Matplotlib](https://img.shields.io/badge/Matplotlib-3.7+-11557c.svg)](https://matplotlib.org/) [![Seaborn](https://img.shields.io/badge/Seaborn-0.12+-882255.svg)](https://seaborn.pydata.org/) [![Plotly](https://img.shields.io/badge/Plotly-5.14+-3F4F75.svg)](https://plotly.com/) |
| **Development**   | [![Git](https://img.shields.io/badge/Git-2.34+-F05032.svg)](https://git-scm.com/) [![Jupyter](https://img.shields.io/badge/Jupyter-1.0+-F37626.svg)](https://jupyter.org/) [![VSCode](https://img.shields.io/badge/VSCode-1.85+-007ACC.svg)](https://code.visualstudio.com/) |
| **Code Quality**  | [![Black](https://img.shields.io/badge/Black-23.3+-000000.svg)](https://github.com/psf/black) [![Flake8](https://img.shields.io/badge/Flake8-6.0+-2076B2.svg)](https://flake8.pycqa.org/) [![Mypy](https://img.shields.io/badge/Mypy-1.3+-124A58.svg)](http://mypy-lang.org/) |
| **Dashboard**     | [![Streamlit](https://img.shields.io/badge/Streamlit-1.25+-FF4B4B.svg)](https://streamlit.io/) |


### Prerequisites

```bash
# Required
- Python 3.8+
- PostgreSQL 13+
- pip or conda

# Optional
- DBeaver (database management)
- Jupyter Notebook (exploration)
```

### Installation

```bash
# 1. Clone repository
git clone <repository-url>
cd indonesia-demographics

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure database
# Create .env file with your PostgreSQL credentials
cp .env.example .env
# Edit .env with your database settings
```

### Configuration

Create a `.env` file in the project root:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=indonesia_demographics
DB_USER=postgres
DB_PASSWORD=your_password
```

## 🎯 Usage

### Run Complete Pipeline

```bash
# Run both Phase 3 (Data Engineering) and Phase 4 (Analysis)
python main.py
```

### Run Individual Phases

```bash
# Run only Data Engineering (Phase 3)
python main.py --skip-phase4

# Run only Analysis (Phase 4)
python main.py --skip-phase3
```

### What Each Phase Does

**Phase 3: Data Engineering** 🔧
1. Organizes raw data files into proper structure
2. Cleans and standardizes datasets (TFR, ASFR, expenditure)
3. Creates PostgreSQL database and tables
4. Loads cleaned data into database

**Phase 4: Data Science & Analysis** 📊
1. Performs ARIMA time series forecasting
2. Generates national and regional expenditure predictions
3. Conducts quadrant analysis for market segmentation
4. Creates visualizations and exports results

## 📁 Project Structure

```
indonesia-demographics/
├── main.py                     # Main pipeline orchestrator
├── requirements.txt            # Python dependencies
├── .env                        # Database configuration (create this)
│
├── data/
│   ├── raw/                    # Original data from BPS
│   │   ├── TFR/
│   │   ├── ASFR/
│   │   └── Pengeluaran/
│   ├── interim/                # Cleaned datasets
│   └── processed/              # Final analysis outputs
│
├── src/
│   ├── data/                   # Data preparation scripts
│   │   ├── make_dataset.py     # Organize raw data
│   │   └── clean_data.py       # Clean and standardize
│   │
│   ├── database/               # Database operations
│   │   ├── setup_db.py         # Create database & tables
│   │   ├── load_data.py        # Load data to PostgreSQL
│   │   └── config.py           # Database configuration
│   │
│   ├── analysis/               # Analysis modules
│   │   ├── config_loader.py    # Load YAML configuration
│   │   ├── arima_forecaster.py # Time series forecasting
│   │   ├── forecast_expenditure.py  # Main forecasting script
│   │   ├── quadrant_analysis.py     # Market segmentation
│   │   └── forecast_visualizer.py   # Plotting functions
│   │
│   └── models/
│       └── config.yml          # Analysis configuration
│
├── models/                     # Trained models and metadata
├── reports/
│   └── figures/                # Generated visualizations
│
└── notebooks/                  # Jupyter notebooks (exploration)
```

## 📊 Data Sources

All data sourced from **Badan Pusat Statistik (BPS)**:

| Data | Source | Granularity | Period |
|------|--------|-------------|--------|
| TFR | SP2020 Long Form | Kabupaten/Kota | 2020 |
| ASFR | SP2020 Long Form | Kabupaten/Kota | 2020 |
| Expenditure | Susenas | Kabupaten/Kota | 2010-2025 |

**Links:**
- [Expenditure Data](https://www.bps.go.id/id/statistics-table/2/NDE2IzI=/-metode-baru--pengeluaran-per-kapita-disesuaikan.html)
- [TFR Data](https://www.bps.go.id/id/statistics-table?subject=519&global-keyword=TFR)
- [ASFR Data](https://www.bps.go.id/id/statistics-table?subject=519&global-keyword=asfr)

## 🎯 Analysis Methods

### Quadrant Analysis

Segments regions into 4 categories based on TFR (market volume) and expenditure (market value):

| Quadrant | TFR | Expenditure | Business Strategy |
|----------|-----|-------------|-------------------|
| ⭐ Stars | High | High | Primary expansion target |
| 🐮 Cash Cows | Low | High | Premium products |
| 🌱 Developing | High | Low | Mass market products |
| ⚠️ Saturated | Low | Low | Challenging market |

### Time Series Forecasting

- **Model**: ARIMA (Auto-Regressive Integrated Moving Average)
- **Grid Search**: Optimal (p, d, q) parameters via AIC/BIC
- **Validation**: Stationarity tests, residual diagnostics
- **Output**: 5-year forecast with 95% confidence intervals

## 📈 Outputs

### Files Generated

**Data Files:**
```
data/processed/
├── national_expenditure_forecast.csv      # National forecast
├── regional_expenditure_forecasts.csv     # Top regions forecast
├── market_segmentation.csv                # Quadrant classification
└── segment_statistics.csv                 # Segment summaries

models/
└── expenditure_arima_model_info.csv       # Model parameters
```

**Visualizations:**
```
reports/figures/
├── expenditure_historical_trend.png       # Historical pattern
├── expenditure_model_diagnostics.png      # ARIMA diagnostics
├── expenditure_forecast.png               # Forecast with CI
├── regional_expenditure_forecasts.png     # Top 5 regions
├── quadrant_analysis.png                  # Market segmentation
└── segment_distribution.png               # Segment breakdown
```

### Database Tables

PostgreSQL database contains:

- `regions`: Master region list (500+ regions)
- `tfr`: Total Fertility Rate by region
- `asfr`: Age-Specific Fertility Rates
- `expenditure`: Per capita expenditure (time series)
- `market_analysis`: Quadrant classifications with scores

## 🔧 Configuration

Edit `src/models/config.yml` to customize:

```yaml
forecasting:
  forecast_horizon_years: 5        # Forecast period
  
  statsmodels:
    max_p: 3                        # ARIMA AR order
    max_d: 2                        # Differencing
    max_q: 3                        # MA order

quadrant:
  tfr_threshold_method: 'median'   # or 'mean', 'fixed'
  expenditure_threshold_method: 'median'

outputs:
  plot_dpi: 300                    # Figure resolution
  top_n_regions: 10                # Regions to analyze
```

## 🛠️ Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html
```

### Code Style

```bash
# Format code
black src/

# Check style
flake8 src/

# Type checking
mypy src/
```

### Database Management

```bash
# Check database structure
python -m src.database.check_db

# Clear specific table
python -m src.database.clear_table

# Re-setup database
python -m src.database.setup_db
```

## 📚 Documentation

- **Project Charter**: See `business.pdf` for detailed project overview
- **Folder Structure**: See `references/folder_structure.txt`
- **Code Documentation**: Docstrings in all Python modules

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📝 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file.

## 👤 Author

**Data Science Team**
- 📧 Email: dkhomeini79@gmail.com
- 🔗 LinkedIn: [Ayat Tulloh RK](https://linkedin.com/in/ayat-tulloh-rk)
- 🐙 GitHub: [@atrkhomeini](https://github.com/atrkhomeini)

## 🙏 Acknowledgments

- Badan Pusat Statistik (BPS) for providing comprehensive demographic data
- Cookie Cutter Data Science for project structure inspiration
- Python data science community for excellent libraries

---

**Built with ❤️ using Python, PostgreSQL, and Open Data**