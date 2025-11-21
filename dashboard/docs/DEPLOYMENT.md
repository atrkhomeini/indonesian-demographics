# 🚀 Hugging Face Spaces Deployment Guide

Complete guide to deploy your Indonesia Demographics Dashboard to Hugging Face Spaces.

## 📋 Prerequisites

- Hugging Face account ([Sign up](https://huggingface.co/join))
- Git installed locally
- Data files prepared (run `python setup.py`)

## 🎯 Deployment Methods

### Method 1: Web Interface (Easiest)

**Step 1: Create Space**

1. Go to https://huggingface.co/spaces
2. Click "Create new Space"
3. Fill in details:
   - **Space name**: `indonesia-demographics` (or your choice)
   - **License**: MIT
   - **Select SDK**: Streamlit
   - **Hardware**: CPU Basic (free tier)
   - **Visibility**: Public

**Step 2: Upload Files**

Click "Files" tab, then "Add file" → "Upload files":

```
Required files:
✓ app.py
✓ requirements.txt
✓ README_HF.md → rename to README.md
✓ src/data_loader.py (create src/ folder first)
✓ src/visualizations.py
✓ .streamlit/config.toml (create .streamlit/ folder first)

Data files (if < 50MB):
✓ data/processed/national_expenditure_forecast.csv
✓ data/processed/regional_expenditure_forecasts.csv
✓ data/processed/market_segmentation.csv
✓ data/processed/segment_statistics.csv
✓ data/interim/expenditure_clean.csv
✓ data/interim/tfr_clean.csv
```

**Step 3: Deploy**

The Space will automatically build and deploy. Wait for:
- "Building" → "Running" status
- Check logs for any errors

**Step 4: Test**

Visit your Space URL: `https://huggingface.co/spaces/YOUR_USERNAME/indonesia-demographics`

---

### Method 2: Git (Recommended for Updates)

**Step 1: Initial Setup**

```bash
# Clone your Space repository
git clone https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME
cd YOUR_SPACE_NAME

# Configure git
git config user.email "your-email@example.com"
git config user.name "Your Name"
```

**Step 2: Copy Dashboard Files**

```bash
# From your project root
cd /path/to/indonesia-demographics

# Copy dashboard to Space directory
cp -r master/dashboard/* /path/to/YOUR_SPACE_NAME/

# Or if already in dashboard directory
cp -r * /path/to/YOUR_SPACE_NAME/
```

**Step 3: Prepare Data**

```bash
cd /path/to/YOUR_SPACE_NAME

# Run setup script
python setup.py
```

**Step 4: Commit and Push**

```bash
# Check files
git status

# Add all files
git add .

# Commit
git commit -m "Initial dashboard deployment"

# Push to Hugging Face
git push
```

**Step 5: Monitor Deployment**

- Go to your Space page
- Click "Logs" tab
- Watch build progress
- Verify no errors

---

### Method 3: Hugging Face CLI

**Step 1: Install CLI**

```bash
pip install huggingface_hub
```

**Step 2: Login**

```bash
huggingface-cli login
# Enter your access token from https://huggingface.co/settings/tokens
```

**Step 3: Create Space**

```bash
huggingface-cli repo create \
    --type space \
    --space_sdk streamlit \
    indonesia-demographics
```

**Step 4: Clone and Deploy**

```bash
# Clone
git clone https://huggingface.co/spaces/YOUR_USERNAME/indonesia-demographics
cd indonesia-demographics

# Copy files
cp -r /path/to/dashboard/* .

# Commit and push
git add .
git commit -m "Deploy dashboard"
git push
```

---

## 📊 Data Considerations

### Option 1: Include Data (< 50MB)

✅ **Pros**: Simple, works out of box
❌ **Cons**: Limited to 50MB, slower uploads

**Implementation**: Copy data files to `data/` directory before pushing.

### Option 2: External Storage (Recommended for Large Data)

✅ **Pros**: No size limit, faster deployments
✅ **Cons**: Requires setup, slightly more complex

**Storage Options**:
- Hugging Face Datasets Hub
- AWS S3
- Google Cloud Storage
- Azure Blob Storage

**Example: Using Hugging Face Datasets**

```python
# In data_loader.py
from datasets import load_dataset

def load_national_forecast(self):
    dataset = load_dataset(
        "YOUR_USERNAME/indonesia-demographics-data",
        split="national_forecast"
    )
    return dataset.to_pandas()
```

### Option 3: Database Connection

**Setup Environment Variables** in Space settings:

```
DB_HOST=your-database-host
DB_PORT=5432
DB_NAME=indonesia_demographics
DB_USER=your-username
DB_PASSWORD=your-password
```

**Modified data_loader.py**:

```python
import os
from sqlalchemy import create_engine

def load_from_database(self):
    connection_string = (
        f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )
    engine = create_engine(connection_string)
    return pd.read_sql("SELECT * FROM market_analysis", engine)
```

---

## 🔧 Configuration

### Environment Variables

Add in Space Settings → Variables:

```
# Optional: Database
DB_HOST=localhost
DB_PORT=5432
DB_NAME=indonesia_demographics

# Optional: API Keys (if needed)
API_KEY=your-api-key

# Optional: Feature Flags
ENABLE_FORECASTING=true
ENABLE_REGIONAL_ANALYSIS=true
```

### Secrets (Sensitive Data)

Add in Space Settings → Secrets:

```toml
# .streamlit/secrets.toml structure
[database]
host = "your-host"
port = 5432
database = "your-db"
user = "your-user"
password = "your-password"
```

Access in code:
```python
import streamlit as st
db_config = st.secrets["database"]
```

---

## 🐛 Troubleshooting

### Build Fails

**Check logs**:
1. Go to Space page
2. Click "Logs" tab
3. Look for error messages

**Common Issues**:

#### Missing Dependencies
```
Error: ModuleNotFoundError: No module named 'plotly'
```
**Fix**: Add to `requirements.txt`

#### Data Loading Errors
```
Error: FileNotFoundError: [Errno 2] No such file or directory: 'data/processed/...'
```
**Fix**: 
- Ensure data files are uploaded
- Check paths in `data_loader.py`
- Verify directory structure

#### Memory Issues
```
Error: Container killed due to OOM
```
**Fix**:
- Reduce data size
- Use external storage
- Upgrade to paid hardware tier

### App Crashes

**Check Streamlit logs**:
```python
import streamlit as st
st.write("Debug info:", your_variable)
```

**Enable debug mode** in config.toml:
```toml
[client]
showErrorDetails = true
```

### Slow Performance

**Solutions**:
1. Enable caching:
```python
@st.cache_data
def load_data():
    # ...
```

2. Reduce data size:
```python
# Sample data
df = df.sample(frac=0.5)
```

3. Optimize visualizations:
```python
# Reduce points
df_sampled = df[::10]  # Every 10th point
```

---

## 🔄 Updates and Maintenance

### Update Dashboard

```bash
# Pull latest changes
git pull

# Make changes locally
# ... edit files ...

# Test locally
streamlit run app.py

# Push to Hugging Face
git add .
git commit -m "Update: description of changes"
git push
```

### Monitor Usage

1. Go to Space page
2. View analytics:
   - Visitor count
   - Uptime
   - Resource usage

### Backup Data

```bash
# Clone Space repository
git clone https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE

# Backup entire directory
tar -czf dashboard-backup-$(date +%Y%m%d).tar.gz YOUR_SPACE/
```

---

## 📈 Optimization Tips

### 1. Lazy Loading

```python
# Load data only when needed
if st.session_state.get('show_forecasting'):
    data = load_forecast_data()
```

### 2. Pagination

```python
# For large tables
page_size = 50
page_number = st.number_input('Page', 1, max_pages)
start_idx = (page_number - 1) * page_size
end_idx = start_idx + page_size
st.dataframe(df[start_idx:end_idx])
```

### 3. Progressive Loading

```python
with st.spinner('Loading data...'):
    # Load critical data first
    core_data = load_core_data()
    
# Load additional data in background
if st.session_state.get('load_additional'):
    additional_data = load_additional_data()
```

---

## 🎨 Customization

### Change Theme

Edit `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#FF4B4B"  # Your brand color
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
```

### Add Logo

```python
st.sidebar.image("logo.png", width=200)
```

### Custom Domain (Pro feature)

Contact Hugging Face for custom domain setup.

---

## 📚 Additional Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Hugging Face Spaces Docs](https://huggingface.co/docs/hub/spaces)
- [Plotly Documentation](https://plotly.com/python/)
- [Python Dash Community](https://community.plotly.com/)

---

## ✅ Deployment Checklist

Before deploying:

- [ ] Run `python setup.py` to prepare data
- [ ] Test locally: `streamlit run app.py`
- [ ] Verify all data files present
- [ ] Check requirements.txt is complete
- [ ] Update README_HF.md with project info
- [ ] Test with sample data
- [ ] Check data size (< 50MB recommended)
- [ ] Configure environment variables if needed
- [ ] Review .gitignore

After deploying:

- [ ] Space builds successfully
- [ ] Dashboard loads without errors
- [ ] All pages render correctly
- [ ] Visualizations display properly
- [ ] Data downloads work
- [ ] No broken links
- [ ] Test on mobile device
- [ ] Share link with team

---

**Need Help?**

- Hugging Face Community: https://discuss.huggingface.co/
- Streamlit Forum: https://discuss.streamlit.io/
- Project Issues: [GitHub Issues](https://github.com/atrkhomeini/indonesia-demographics/issues)

**Good luck with your deployment! 🚀**