# 📊 Predictive Analytics Features

## Overview

MediAlert now includes an **AI-powered predictive analytics system** that helps policymakers make data-driven decisions for pandemic response. The system provides 7-day forecasts, rapid growth alerts, and resource demand predictions.

## 🎯 Key Features

### 1. **7-Day Case Forecasting**
- Predicts pneumonia case trends for the next 7 days
- Uses time-series analysis (Prophet or Linear Regression)
- Provides confidence intervals for predictions
- Identifies peak dates and case velocities

### 2. **Rapid Growth Detection**
- Automatically detects regions with exponential case growth
- Calculates key metrics:
  - **Growth Rate**: % increase in cases over 3 days
  - **Doubling Time**: How quickly cases are doubling
  - **Daily Velocity**: Average daily increase in cases
  - **Trend Classification**: Rapid Growth, Growing, Stable, or Declining

### 3. **Resource Demand Forecasting**
- Predicts hospital resource needs based on case forecasts:
  - **ICU Beds**: Estimated beds needed per day
  - **Ventilators**: Ventilator requirements based on severe cases
  - **Oxygen Supply**: Daily oxygen unit consumption
- Compares predicted demand vs. current capacity
- Identifies resource gaps and shortages

### 4. **Automated Alert System**
Generates alerts for:
- 🔴 **Critical Surge Alerts**: >100% growth in 3 days
- 🟠 **Rapid Growth Alerts**: >20% growth in 3 days
- 🏥 **Capacity Warnings**: ICU utilization >80%
- 💨 **Resource Depletion**: Oxygen supply <7 days
- ⏱️ **Doubling Time Alerts**: Cases doubling in <5 days

### 5. **Policymaker Recommendations**
Each alert includes actionable recommendations:
- Emergency procurement needs
- Resource allocation suggestions
- Population prioritization (high-risk demographics)
- Testing and surveillance scaling

---

## 🖥️ User Interface

### Predictions Dashboard
**URL**: `/surveillance/predictions`

**Features:**
- Alert summary cards (Critical, High, Medium priority)
- Rapid growth alerts with detailed metrics
- Regional growth analysis table
- Sortable by growth rate, doubling time, velocity
- Color-coded trend indicators

**How to Access:**
1. Go to Surveillance Dashboard: `/surveillance`
2. Click on **"Predictions"** tab or the featured card
3. View real-time predictions and alerts

---

## 🔌 API Endpoints

### 1. Regional Predictions
```http
GET /api/v1/predictions/region/{region_id}?region_type=country&forecast_days=7
```

**Response:**
```json
{
  "success": true,
  "region_name": "United States",
  "case_forecast": [
    {
      "date": "2026-02-11",
      "predicted_cases": 850,
      "lower_bound": 680,
      "upper_bound": 1020,
      "confidence_interval": "±170"
    }
  ],
  "resource_forecast": {
    "timeline": [...],
    "summary": {
      "peak_date": "2026-02-17",
      "peak_cases": 1200,
      "peak_icu_beds_needed": 360,
      "max_icu_utilization": 120.5
    }
  },
  "growth_analysis": {
    "growth_rate_3day": 45.2,
    "doubling_time_days": 5.3,
    "daily_velocity": 85.4,
    "trend": "rapid_growth"
  },
  "recommendations": [
    "🔴 CRITICAL: Implement immediate lockdown measures...",
    "🏥 URGENT: Procure 150 additional ICU beds..."
  ]
}
```

### 2. Hospital Predictions
```http
GET /api/v1/predictions/hospital/{hospital_id}?forecast_days=7
```

### 3. Growth Alerts
```http
GET /api/v1/alerts/growth?region_type=country&threshold=50.0
```

**Response:**
```json
{
  "success": true,
  "alerts": [
    {
      "region_id": "IN",
      "region_name": "India",
      "alert_type": "surge_detected",
      "severity": "critical",
      "title": "🚨 Case Surge Detected: India",
      "description": "Cases increased by 85.3% in the last 3 days...",
      "metrics": {
        "growth_rate": 85.3,
        "current_cases": 145000,
        "trend": "rapid_growth"
      },
      "recommendations": [...]
    }
  ],
  "summary": {
    "total_alerts": 5,
    "by_severity": {
      "critical": 2,
      "high": 2,
      "medium": 1
    }
  }
}
```

### 4. Capacity Alerts
```http
GET /api/v1/alerts/capacity?region_type=country&forecast_days=7
```

### 5. Growth Metrics
```http
GET /api/v1/analytics/growth-metrics?region_type=country
```

**Response:**
```json
{
  "success": true,
  "metrics": [
    {
      "region_id": "IN",
      "region_name": "India",
      "current_cases": 145000,
      "growth_rate_3day": 85.3,
      "doubling_time_days": 3.2,
      "daily_velocity": 12400.5,
      "trend": "rapid_growth"
    }
  ]
}
```

---

## 🧠 How It Works

### Forecasting Algorithm
1. **Data Collection**: Retrieves 30 days of historical case data
2. **Model Training**: Fits time-series model (Prophet or Linear Regression)
3. **Prediction**: Generates 7-14 day forecasts with confidence intervals
4. **Resource Mapping**: Converts case predictions to resource needs using ratios:
   - ICU Beds: 30% of pneumonia cases
   - Ventilators: 10% of pneumonia cases
   - Oxygen: 2 units per case per day

### Growth Detection
```
Growth Rate = ((Recent 3 days cases - Previous 3 days cases) / Previous 3 days cases) × 100

Doubling Time = (Days elapsed × log(2)) / log(Current cases / Initial cases)
```

### Alert Thresholds
| Alert Type | Threshold |
|-----------|----------|
| Surge | Growth rate >50% (3 days) |
| Rapid Growth | Growth rate >20% (3 days) |
| Critical Doubling | Doubling time <3 days |
| Capacity Critical | ICU utilization >90% |
| Capacity Warning | ICU utilization >80% |
| Oxygen Critical | Supply <3 days remaining |

---

## 📊 Sample Use Cases

### Use Case 1: Identifying Hotspots
**Problem**: A city shows rapid case increase but hasn't been flagged yet.

**Solution**:
1. Go to Predictions Dashboard
2. Check "Regional Growth Analysis" table
3. Sort by "Growth Rate" to see cities with highest increases
4. View alerts for cities exceeding thresholds

**Output**:
```
Mumbai: Growth Rate 78.5% | Doubling Time: 3.1 days | 🔴 CRITICAL
```

### Use Case 2: Resource Planning
**Problem**: Hospital capacity planning for next week.

**Solution**:
1. Call `/api/v1/predictions/hospital/{id}`
2. Review `resource_forecast.timeline`
3. Identify peak demand date
4. Compare with current capacity

**Output**:
```
Peak Date: Feb 17
ICU Beds Needed: 450
Current Capacity: 300
Gap: 150 beds (Need to procure immediately)
```

### Use Case 3: Policymaker Briefing
**Problem**: Weekly briefing for health minister.

**Solution**:
1. Access Predictions Dashboard
2. Review Alert Summary (Critical/High/Medium counts)
3. Export top 5 rapid growth regions
4. Show resource gap analysis

**Output**:
- 3 Critical Alerts (Mumbai, Delhi, Bangalore)
- Predicted bed shortage: 850 ICU beds across regions
- Recommended actions: Lockdown in Mumbai, Transfer patients from Delhi

---

## 🔧 Configuration

### Customizing Thresholds

Edit `/app/models/alerts.py`:

```python
alert_engine = AlertEngine(thresholds={
    'surge_growth_rate': 50.0,        # % growth to trigger surge
    'rapid_growth_rate': 20.0,        # % growth to trigger warning
    'doubling_time_critical': 3.0,    # days
    'icu_utilization_critical': 90.0, # % capacity
    'oxygen_days_critical': 3,        # days remaining
})
```

### Customizing Resource Ratios

Edit `/app/models/predictions.py`:

```python
predictor = ResourceDemandPredictor(custom_ratios={
    'severe_ratio': 0.20,        # 20% of cases are severe
    'icu_bed_ratio': 0.30,       # 30% need ICU beds
    'ventilator_ratio': 0.10,    # 10% need ventilators
    'oxygen_per_case': 2,        # Units per case per day
})
```

---

## 🧪 Testing

Run the test suite:

```bash
python test_predictions.py
```

**Tests Include:**
- ✅ Case forecasting (7-day predictions)
- ✅ Resource demand predictions
- ✅ Growth analysis and metrics
- ✅ Alert generation
- ✅ Full forecast report generation

---

## 📈 Performance

- **Forecast Generation**: <2 seconds per region
- **Growth Analysis**: <500ms per region
- **Alert Generation**: <1 second for all regions
- **API Response Time**: <3 seconds (with Prophet), <1 second (Linear Regression)

---

## 🚀 Future Enhancements

1. **Machine Learning Models**
   - LSTM neural networks for better accuracy
   - Ensemble models combining multiple approaches
   - Automatic hyperparameter tuning

2. **Advanced Analytics**
   - Variant detection from imaging patterns
   - Mortality risk scoring per patient
   - Hospital transfer optimization
   - Supply chain forecasting

3. **Integration**
   - Email/SMS alert notifications
   - Automated policy recommendations
   - Integration with WHO dashboards
   - Real-time data streaming

4. **Visualization**
   - Interactive forecast charts with Chart.js
   - Heatmaps showing predicted hotspots
   - Resource timeline Gantt charts
   - Animated growth trajectories

---

## 📚 References

- **Prophet**: Facebook's time-series forecasting library
- **Scikit-learn**: Machine learning for regression and classification
- **Pandas**: Data manipulation and time-series analysis
- **MediAlert PRD**: See Phase 2 (Advanced Analytics)

---

## 🤝 Support

For questions or issues:
- API Documentation: See `/api/v1/*` endpoints
- Dashboard Guide: See `/surveillance/predictions`
- Technical Support: Check console logs for detailed error messages

---

**Last Updated**: 2026-02-10
**Version**: 1.0.0
**Status**: Production Ready ✅
