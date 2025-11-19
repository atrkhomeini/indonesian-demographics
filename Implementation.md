# Implementation Guide: Unified Pipeline

## 📦 What I've Created

I've created a **unified pipeline system** that runs both Phase 3 (Data Engineering) and Phase 4 (Data Science & Analysis) from a single entry point. Here's what you get:

### Core Files

1. **`main.py`** - Main pipeline orchestrator
   - Runs both phases sequentially
   - Supports selective execution (`--skip-phase3`, `--skip-phase4`)
   - Comprehensive error handling
   - Beautiful progress indicators
   - Final summary with all outputs

2. **`check_setup.py`** - Pre-flight validation script
   - Checks Python version
   - Validates dependencies
   - Tests database connection
   - Verifies data files
   - Provides clear troubleshooting steps

3. **`README.md`** - Complete documentation
   - Project overview
   - Installation instructions
   - Usage examples
   - Architecture details
   - Configuration guide

4. **`QUICKSTART.md`** - Step-by-step tutorial
   - 10-minute setup guide
   - Screenshots and examples
   - Common issues + solutions
   - Next steps after setup

5. **`.env.example`** - Configuration template
   - Database settings
   - Environment variables
   - Copy to `.env` and customize

## 🎯 How to Use

### First Time Setup

```bash
# 1. Validate environment
python check_setup.py

# 2. If all checks pass, run full pipeline
python main.py
```

### Daily Usage

```bash
# Run complete pipeline
python main.py

# Only update data (skip analysis)
python main.py --skip-phase4

# Only run analysis (skip data engineering)
python main.py --skip-phase3
```

## 📊 Pipeline Flow

```
┌─────────────────────────────────────────────────────────┐
│                      main.py                            │
└───────────────────┬─────────────────────────────────────┘
                    │
        ┌───────────┴───────────┐
        │                       │
        ▼                       ▼
┌───────────────┐       ┌───────────────┐
│   PHASE 3     │       │   PHASE 4     │
│ Data Engineer │       │   Analysis    │
└───────┬───────┘       └───────┬───────┘
        │                       │
        ├─ make_dataset         ├─ load_data
        ├─ clean_data           ├─ forecast_expenditure
        ├─ setup_db             │   ├─ national_forecast
        └─ load_data            │   └─ regional_forecast
                                └─ quadrant_analysis
                                    ├─ market_segmentation
                                    └─ visualizations
```

## 🔧 What Each Phase Does

### Phase 3: Data Engineering 🔧

**Duration**: ~2-3 minutes

**Steps**:
1. **Organize Raw Data** (`make_dataset.py`)
   - Creates folder structure
   - Copies files from uploads
   - Validates file presence

2. **Clean Data** (`clean_data.py`)
   - Standardizes region names
   - Handles missing values
   - Validates data ranges
   - Creates interim datasets

3. **Setup Database** (`setup_db.py`)
   - Creates PostgreSQL database
   - Defines table schemas
   - Creates indexes

4. **Load Data** (`load_data.py`)
   - Loads cleaned data to PostgreSQL
   - Creates market analysis table
   - Verifies data integrity

**Outputs**:
- `data/interim/*.csv` - Cleaned datasets
- PostgreSQL tables populated
- Ready for analysis

### Phase 4: Data Science & Analysis 📊

**Duration**: ~5-7 minutes

**Steps**:
1. **Load Configuration**
   - Reads `config.yml`
   - Initializes visualizer
   - Loads data from interim

2. **Time Series Forecasting**
   - National expenditure forecast (ARIMA)
   - Regional forecasts (top 10 regions)
   - Model diagnostics
   - Visualizations

3. **Quadrant Analysis**
   - Calculate thresholds
   - Assign market segments
   - Generate statistics
   - Create quadrant plots

**Outputs**:
- CSV files with forecasts
- Market segmentation data
- Professional visualizations
- Model metadata

## 📁 Generated Outputs

After running `python main.py`, you'll have:

```
data/processed/
├── national_expenditure_forecast.csv     # 5-year national forecast
├── regional_expenditure_forecasts.csv    # Top regions forecast
├── market_segmentation.csv               # Quadrant assignments
└── segment_statistics.csv                # Segment summaries

models/
└── expenditure_arima_model_info.csv      # Model parameters & metrics

reports/figures/
├── expenditure_historical_trend.png      # Historical data plot
├── expenditure_model_diagnostics.png     # ARIMA diagnostics
├── expenditure_forecast.png              # Forecast with CI
├── regional_expenditure_forecasts.png    # Top 5 regions
├── quadrant_analysis.png                 # Market segmentation map
└── segment_distribution.png              # Segment breakdown
```

## 🚀 Integration with Your Project

### Option 1: Replace Existing main.py

```bash
# Backup current main.py (if exists)
mv main.py main.py.backup

# Use new unified main.py
# (already in /mnt/user-data/outputs/)
```

### Option 2: Run Alongside Existing Scripts

Keep your current structure and use `main.py` as the primary entry point:

```
your-project/
├── main.py                 # ← New unified pipeline
├── check_setup.py          # ← New validation script
├── notebooks/phase3.py     # Keep for development
├── src/analysis/run_analysis.py  # Keep for modular use
└── ...
```

## 🎨 Customization

### Adjust Forecast Parameters

Edit `src/models/config.yml`:

```yaml
forecasting:
  forecast_horizon_years: 10  # Change from 5 to 10 years
  
  statsmodels:
    max_p: 5  # More AR terms
    max_d: 1  # Less differencing
```

### Change Quadrant Thresholds

```yaml
quadrant:
  tfr_threshold_method: 'fixed'
  tfr_threshold_fixed: 2.5  # Custom threshold
```

### Modify Output Settings

```yaml
outputs:
  plot_dpi: 600  # Higher resolution
  top_n_regions: 20  # Analyze more regions
```

## 🔍 Validation & Testing

### Before Running Pipeline

```bash
# 1. Check environment
python check_setup.py

# 2. Test database connection
python -m src.database.check_db

# 3. Verify config
python -c "from src.analysis.config_loader import Config; c=Config(); print('✅ Config valid')"
```

### After Running Pipeline

```bash
# 1. Check database
psql -U postgres -d indonesia_demographics -c "SELECT COUNT(*) FROM market_analysis;"

# 2. Verify outputs
ls -lh data/processed/
ls -lh reports/figures/

# 3. Quick data check
python -c "import pandas as pd; df=pd.read_csv('data/processed/market_segmentation.csv'); print(df.head())"
```

## 🐛 Troubleshooting

### Issue: "Database connection failed"

**Check**:
```bash
# Is PostgreSQL running?
pg_isready

# Can you connect manually?
psql -U postgres -d indonesia_demographics
```

**Fix**:
1. Start PostgreSQL: `sudo systemctl start postgresql`
2. Verify credentials in `.env`
3. Create database if needed

### Issue: "No data files found"

**Check**:
```bash
ls -R data/raw/
```

**Fix**:
1. Copy CSV files to correct directories
2. Or run: `python -m src.data.make_dataset` if files are in uploads

### Issue: "Module not found"

**Fix**:
```bash
# Activate venv
source venv/bin/activate

# Reinstall
pip install -r requirements.txt
```

## 📊 Expected Results

### Console Output

You'll see clear progress indicators:

```
================================================================================
                 PHASE 3: DATA ENGINEERING
================================================================================

[Step 1/4] Organizing raw data...
✓ Raw data organized

[Step 2/4] Cleaning datasets...
   ✓ Cleaned 514 regions
   ✓ Data cleaned

[Step 3/4] Setting up PostgreSQL database...
✓ Database ready

[Step 4/4] Loading data to database...
✓ Data loaded to PostgreSQL

================================================================================
                    ✅ PHASE 3 COMPLETE
================================================================================

================================================================================
                 PHASE 4: DATA SCIENCE & ANALYSIS
================================================================================
...
```

### Final Summary

```
################################################################################
#                                                                              #
#                          PIPELINE SUMMARY                                    #
#                                                                              #
################################################################################

Phase 3 (Data Engineering):    ✅ PASS
Phase 4 (Data Science):        ✅ PASS

Total Duration:                0:08:23
Completed At:                  2025-01-15 14:30:45

📁 GENERATED OUTPUTS:
...
```

## 🎓 Learning More

### Understanding ARIMA

The pipeline uses ARIMA for time series forecasting. Key concepts:

- **p (AR order)**: How many past values influence forecast
- **d (Differencing)**: Transformations to make data stationary
- **q (MA order)**: Impact of past forecast errors

The pipeline automatically finds optimal (p, d, q) via grid search.

### Understanding Quadrants

Market segmentation based on two dimensions:

- **X-axis (TFR)**: Market volume/growth potential
- **Y-axis (Expenditure)**: Market value/purchasing power

This creates four distinct market types for strategic planning.

## 🤝 Contributing

If you enhance the pipeline:

1. Test with `check_setup.py` first
2. Update `config.yml` for new features
3. Add documentation to README
4. Include example outputs

## 📝 Next Steps

After successful setup:

1. ✅ Review generated visualizations
2. ✅ Query database for insights
3. ✅ Customize configuration
4. ✅ Build dashboards (optional)
5. ✅ Schedule automated runs (optional)

## 🎯 Business Use Cases

With this pipeline, you can:

- **Identify Growth Markets**: Find "Stars" regions for expansion
- **Optimize Product Mix**: Target premium products to "Cash Cows"
- **Forecast Demand**: Predict market size 5 years ahead
- **Resource Allocation**: Prioritize investments by market score
- **Risk Assessment**: Monitor "Saturated" markets

---

## 🙋 Questions?

If you need help:
1. Check `QUICKSTART.md` for step-by-step guide
2. Run `python check_setup.py` to diagnose issues
3. Review error messages carefully
4. Contact the data science team

**Happy analyzing! 📊✨**