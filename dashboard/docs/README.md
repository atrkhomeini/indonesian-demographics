# 🇮🇩 Indonesia Demographics Dashboard

Interactive Streamlit dashboard for market intelligence and demographic analysis.

[![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-FF4B4B.svg)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Hugging Face](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Spaces-yellow)](https://huggingface.co/spaces)

## 📊 Features

### 1. Executive Summary
- High-level KPIs and metrics
- Market segment distribution
- National expenditure trends
- Key insights at a glance

### 2. Market Segmentation
- Interactive quadrant analysis
- Filter by segment, TFR, and expenditure
- Detailed segment profiles
- Regional comparison

### 3. Time Series Forecasting
- National expenditure forecast (2026-2030)
- Regional forecasts for top markets
- ARIMA model details
- Confidence intervals

### 4. Regional Analysis
- Individual region profiles
- Historical trends
- Peer comparison
- Market insights

### 5. Data Explorer
- Browse raw datasets
- Download CSV files
- Data statistics

## 🚀 Quick Start

### Local Development

```bash
# 1. Navigate to dashboard directory
cd master/dashboard

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run dashboard
streamlit run app.py
```

The dashboard will open in your browser at `http://localhost:8501`

### With Docker

```bash
# Build image
docker build -t indonesia-demographics-dashboard .

# Run container
docker run -p 8501:8501 indonesia-demographics-dashboard
```

## 📁 Project Structure

```
master/dashboard/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── README.md                   # This file
│
├── src/
│   ├── data_loader.py          # Data loading utilities
│   └── visualizations.py       # Plotly visualization functions
│
├── .streamlit/
│   └── config.toml             # Streamlit configuration
│
└── data/                       # Data directory (gitignored)
    ├── processed/              # Analysis outputs
    │   ├── national_expenditure_forecast.csv
    │   ├── regional_expenditure_forecasts.csv
    │   ├── market_segmentation.csv
    │   └── segment_statistics.csv
    └── interim/                # Cleaned data
        ├── expenditure_clean.csv
        └── tfr_clean.csv
```

## 🎨 Dashboard Pages

### Executive Summary
Get a bird's-eye view of the market landscape with:
- Total regions analyzed
- Stars market count
- Current and projected expenditure
- Segment distribution pie chart
- National forecast preview

### Market Segmentation
Explore the quadrant-based market segmentation:
- **⭐ Stars**: High TFR + High Expenditure → Primary expansion targets
- **🐮 Cash Cows**: Low TFR + High Expenditure → Premium product focus
- **🌱 Developing**: High TFR + Low Expenditure → Mass market potential
- **⚠️ Saturated**: Low TFR + Low Expenditure → Challenging markets

Interactive features:
- Filter by segment, TFR range, expenditure range
- Hover for detailed region information
- Visual quadrant plot with threshold lines

### Forecasting
View ARIMA-based expenditure forecasts:
- National average forecast with 95% confidence interval
- Regional forecasts for top 10 markets
- Model specification and performance metrics
- Year-by-year forecast values

### Regional Analysis
Deep-dive into individual regions:
- Region profile card
- Historical expenditure trend (2010-2025)
- Comparison with segment peers
- Market-specific insights and strategies

### Data Explorer
Access and download raw data:
- Browse complete datasets
- View data statistics (rows, columns, memory)
- Download CSV files for further analysis

## 🔧 Configuration

### Data Sources

The dashboard expects data files in the following structure:

```
data/
├── processed/
│   ├── national_expenditure_forecast.csv
│   ├── regional_expenditure_forecasts.csv
│   ├── market_segmentation.csv
│   └── segment_statistics.csv
└── interim/
    ├── expenditure_clean.csv
    └── tfr_clean.csv
```

### Custom Styling

Edit the CSS in `app.py` to customize:
- Color schemes
- Segment colors
- Card layouts
- Typography

### Streamlit Configuration

Modify `.streamlit/config.toml` to adjust:
- Theme colors
- Server settings
- UI behavior

## 🌐 Deployment to Hugging Face Spaces

### Method 1: Via Web Interface

1. Create account on [Hugging Face](https://huggingface.co/)
2. Go to [Spaces](https://huggingface.co/spaces)
3. Click "Create new Space"
4. Select "Streamlit" as the SDK
5. Upload dashboard files:
   - `app.py`
   - `requirements.txt`
   - `src/` directory
   - `.streamlit/` directory
   - `data/` directory (if < 50MB)

### Method 2: Via Git

```bash
# 1. Clone your Space repository
git clone https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME
cd YOUR_SPACE_NAME

# 2. Copy dashboard files
cp -r /path/to/master/dashboard/* .

# 3. Commit and push
git add .
git commit -m "Initial dashboard deployment"
git push
```

### Environment Variables

If using PostgreSQL or sensitive data, add these in Space settings:
- `DB_HOST`
- `DB_PORT`
- `DB_NAME`
- `DB_USER`
- `DB_PASSWORD`

## 📊 Data Requirements

### Minimum Data Files

For the dashboard to work, you need at least:

1. **market_segmentation.csv** - Core segmentation data
   - Columns: `region_name`, `tfr`, `expenditure`, `segment`

2. **national_expenditure_forecast.csv** - National forecast
   - Columns: `year`, `expenditure`, `type`, `lower_ci`, `upper_ci`

### Optional Data Files

For full functionality:

3. **regional_expenditure_forecasts.csv** - Regional forecasts
4. **segment_statistics.csv** - Aggregated segment stats
5. **expenditure_clean.csv** - Historical expenditure data
6. **tfr_clean.csv** - TFR data by region

### Sample Data

If data files are missing, the dashboard will use generated sample data for demonstration purposes.

## 🔍 Troubleshooting

### Data Loading Errors

**Issue**: "Data file not found"

**Solution**:
1. Ensure data files are in correct directories
2. Check file names match exactly
3. Verify CSV format and encoding

### Visualization Errors

**Issue**: "Figure cannot be displayed"

**Solution**:
1. Check data has required columns
2. Verify no NaN values in key columns
3. Ensure data types are correct (numeric for TFR/expenditure)

### Performance Issues

**Issue**: Dashboard loads slowly

**Solution**:
1. Enable Streamlit caching (already implemented)
2. Reduce data file sizes
3. Use data sampling for very large datasets
4. Optimize visualizations (reduce points plotted)

## 🎨 Customization Guide

### Adding New Pages

1. Create new function in `app.py`:
```python
def show_my_new_page(data):
    st.header("My New Page")
    # Your page content here
```

2. Add to navigation:
```python
page = st.sidebar.radio(
    "Select Analysis",
    ["Executive Summary", "My New Page", ...]
)
```

3. Add routing:
```python
if page == "My New Page":
    show_my_new_page(data)
```

### Adding New Visualizations

1. Add method to `visualizations.py`:
```python
def create_my_chart(self, data_df):
    fig = go.Figure(...)
    return fig
```

2. Use in dashboard:
```python
viz = Visualizer()
fig = viz.create_my_chart(data)
st.plotly_chart(fig)
```

### Changing Color Schemes

Edit the `colors` dict in `Visualizer.__init__()`:
```python
self.colors = {
    'Stars': '#YOUR_COLOR',
    'Cash Cows': '#YOUR_COLOR',
    # ...
}
```

## 📈 Analytics & Monitoring

### Usage Tracking

For Hugging Face Spaces:
- View analytics in Space settings
- Monitor visitor count, usage patterns
- Track performance metrics

### Error Logging

Add logging to track issues:
```python
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Use in code
logger.info("Data loaded successfully")
logger.error(f"Error loading data: {e}")
```

## 🤝 Contributing

To contribute to the dashboard:

1. Fork the repository
2. Create feature branch
3. Make changes
4. Test locally
5. Submit pull request

## 📝 License

This dashboard is part of the Indonesia Demographics Market Intelligence project.
See main project LICENSE for details.

## 👤 Author

**Data Science Team**
- Email: dkhomeini79@gmail.com
- LinkedIn: [Ayat Tulloh RK](https://linkedin.com/in/ayat-tulloh-rk)
- GitHub: [@atrkhomeini](https://github.com/atrkhomeini)

## 🙏 Acknowledgments

- **Data**: Badan Pusat Statistik (BPS) Indonesia
- **Framework**: Streamlit
- **Hosting**: Hugging Face Spaces
- **Visualization**: Plotly

---

**Built with ❤️ using Streamlit and Python**