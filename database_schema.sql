-- MediAlert Database Schema for Supabase

-- Hospitals table
CREATE TABLE hospitals (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  name TEXT NOT NULL,
  city TEXT NOT NULL,
  state TEXT NOT NULL,
  country TEXT NOT NULL,
  latitude FLOAT NOT NULL,
  longitude FLOAT NOT NULL,
  registration_number TEXT UNIQUE NOT NULL,
  total_beds INTEGER NOT NULL,
  icu_beds INTEGER NOT NULL,
  created_at TIMESTAMP DEFAULT NOW(),
  api_key TEXT UNIQUE,
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Users table (radiologists, admins, etc.)
CREATE TABLE users (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  hospital_id UUID REFERENCES hospitals(id),
  email TEXT UNIQUE NOT NULL,
  password_hash TEXT NOT NULL,
  full_name TEXT,
  role TEXT CHECK (role IN ('radiologist', 'admin', 'doctor', 'public_health_officer')),
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Uploads table
CREATE TABLE uploads (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  hospital_id UUID NOT NULL REFERENCES hospitals(id),
  user_id UUID NOT NULL REFERENCES users(id),
  image_count INTEGER NOT NULL,
  status TEXT CHECK (status IN ('processing', 'completed', 'failed')) DEFAULT 'processing',
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Analyses table
CREATE TABLE analyses (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  upload_id UUID NOT NULL REFERENCES uploads(id),
  image_path TEXT NOT NULL,
  ai_prediction TEXT CHECK (ai_prediction IN ('NORMAL', 'PNEUMONIA', 'UNCERTAIN')) NOT NULL,
  confidence FLOAT NOT NULL CHECK (confidence >= 0 AND confidence <= 1),
  severity TEXT CHECK (severity IN ('mild', 'moderate', 'severe')) NOT NULL,
  processing_time_ms INTEGER,
  model_version TEXT,
  heatmap_path TEXT,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Patient metadata (anonymized)
CREATE TABLE patient_metadata (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  analysis_id UUID NOT NULL REFERENCES analyses(id),
  age_range TEXT CHECK (age_range IN ('0-18', '18-35', '35-60', '60+', 'unknown')),
  gender TEXT CHECK (gender IN ('M', 'F', 'Other', 'Unknown')),
  vaccination_status TEXT CHECK (vaccination_status IN ('vaccinated', 'unvaccinated', 'unknown')),
  symptoms TEXT[] DEFAULT ARRAY[]::TEXT[],
  outcome TEXT CHECK (outcome IN ('admitted', 'discharged', 'deceased', 'unknown')) DEFAULT 'unknown',
  created_at TIMESTAMP DEFAULT NOW()
);

-- Case summary (aggregated daily by hospital)
CREATE TABLE case_summary (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  hospital_id UUID NOT NULL REFERENCES hospitals(id),
  date DATE NOT NULL,
  case_count INTEGER DEFAULT 0,
  normal_count INTEGER DEFAULT 0,
  pneumonia_count INTEGER DEFAULT 0,
  severe_count INTEGER DEFAULT 0,
  deaths INTEGER DEFAULT 0,
  avg_confidence FLOAT DEFAULT 0,
  created_at TIMESTAMP DEFAULT NOW(),
  UNIQUE(hospital_id, date)
);

-- Regional summary (aggregated by geography)
CREATE TABLE regional_summary (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  region_type TEXT NOT NULL CHECK (region_type IN ('country', 'state', 'city', 'district', 'block')),
  region_id TEXT NOT NULL,
  region_name TEXT,
  latitude FLOAT,
  longitude FLOAT,
  date DATE NOT NULL,
  case_count INTEGER DEFAULT 0,
  normal_count INTEGER DEFAULT 0,
  pneumonia_count INTEGER DEFAULT 0,
  severe_count INTEGER DEFAULT 0,
  deaths INTEGER DEFAULT 0,
  hospitals_reporting INTEGER DEFAULT 0,
  population INTEGER,
  case_density FLOAT,
  created_at TIMESTAMP DEFAULT NOW(),
  UNIQUE(region_type, region_id, date)
);

-- Alerts
CREATE TABLE alerts (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  region_id TEXT NOT NULL,
  alert_type TEXT NOT NULL CHECK (alert_type IN ('threshold_exceeded', 'surge_detected', 'variant_detected')),
  severity TEXT NOT NULL CHECK (severity IN ('low', 'medium', 'high', 'critical')),
  description TEXT,
  triggered_at TIMESTAMP DEFAULT NOW(),
  resolved_at TIMESTAMP,
  recipients TEXT[] DEFAULT ARRAY[]::TEXT[],
  created_at TIMESTAMP DEFAULT NOW()
);

-- Resources (hospital capacity tracking)
CREATE TABLE resources (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  hospital_id UUID NOT NULL REFERENCES hospitals(id),
  date DATE NOT NULL,
  icu_beds_available INTEGER,
  ventilators_available INTEGER,
  oxygen_supply_days FLOAT,
  staff_available INTEGER,
  created_at TIMESTAMP DEFAULT NOW(),
  UNIQUE(hospital_id, date)
);

-- Indexes for performance
CREATE INDEX idx_uploads_hospital_id ON uploads(hospital_id);
CREATE INDEX idx_uploads_user_id ON uploads(user_id);
CREATE INDEX idx_uploads_created_at ON uploads(created_at);
CREATE INDEX idx_analyses_upload_id ON analyses(upload_id);
CREATE INDEX idx_analyses_created_at ON analyses(created_at);
CREATE INDEX idx_patient_metadata_analysis_id ON patient_metadata(analysis_id);
CREATE INDEX idx_case_summary_hospital_id ON case_summary(hospital_id);
CREATE INDEX idx_case_summary_date ON case_summary(date);
CREATE INDEX idx_regional_summary_region_type ON regional_summary(region_type);
CREATE INDEX idx_regional_summary_date ON regional_summary(date);
CREATE INDEX idx_regional_summary_case_count ON regional_summary(case_count DESC);
CREATE INDEX idx_alerts_region_id ON alerts(region_id);
CREATE INDEX idx_alerts_resolved_at ON alerts(resolved_at);
CREATE INDEX idx_resources_hospital_id ON resources(hospital_id);
CREATE INDEX idx_resources_date ON resources(date);

-- Enable real-time subscriptions on key tables
ALTER TABLE analyses REPLICA IDENTITY FULL;
ALTER TABLE case_summary REPLICA IDENTITY FULL;
ALTER TABLE regional_summary REPLICA IDENTITY FULL;
ALTER TABLE alerts REPLICA IDENTITY FULL;

-- Insert sample data for testing
INSERT INTO hospitals (name, city, state, country, latitude, longitude, registration_number, total_beds, icu_beds)
VALUES
  ('Mount Sinai Medical Center', 'New York', 'NY', 'USA', 40.7912, -73.9776, 'NY-001', 150, 30),
  ('Johns Hopkins Hospital', 'Baltimore', 'MD', 'USA', 39.2970, -76.5898, 'MD-001', 120, 25),
  ('UCLA Medical Center', 'Los Angeles', 'CA', 'USA', 34.0750, -118.2435, 'CA-001', 200, 40),
  ('Max Healthcare', 'Delhi', 'DL', 'India', 28.5244, 77.2066, 'IN-001', 500, 100),
  ('Apollo Hospitals', 'Mumbai', 'MH', 'India', 19.1136, 72.8697, 'IN-002', 400, 80);

-- Generate dummy data for regional summary (last 30 days)
INSERT INTO regional_summary (region_type, region_id, region_name, latitude, longitude, date, case_count, normal_count, pneumonia_count, severe_count, deaths, hospitals_reporting, population, case_density)
SELECT
  'country',
  'US',
  'United States',
  37.0902,
  -95.7129,
  CURRENT_DATE - (INTERVAL '1 day' * generate_series(0, 29)),
  450000 + (generate_series(0, 29) * 15200),
  (450000 + (generate_series(0, 29) * 15200)) * 0.78,
  (450000 + (generate_series(0, 29) * 15200)) * 0.15,
  (450000 + (generate_series(0, 29) * 15200)) * 0.07,
  (450000 + (generate_series(0, 29) * 15200)) * 0.0073,
  250,
  331000000,
  ((450000 + (generate_series(0, 29) * 15200)) * 100.0) / 331000000;

INSERT INTO regional_summary (region_type, region_id, region_name, latitude, longitude, date, case_count, normal_count, pneumonia_count, severe_count, deaths, hospitals_reporting, population, case_density)
SELECT
  'country',
  'IN',
  'India',
  20.5937,
  78.9629,
  CURRENT_DATE - (INTERVAL '1 day' * generate_series(0, 29)),
  800000 + (generate_series(0, 29) * 26000),
  (800000 + (generate_series(0, 29) * 26000)) * 0.75,
  (800000 + (generate_series(0, 29) * 26000)) * 0.18,
  (800000 + (generate_series(0, 29) * 26000)) * 0.07,
  (800000 + (generate_series(0, 29) * 26000)) * 0.0065,
  450,
  1393409038,
  ((800000 + (generate_series(0, 29) * 26000)) * 100.0) / 1393409038;

INSERT INTO regional_summary (region_type, region_id, region_name, latitude, longitude, date, case_count, normal_count, pneumonia_count, severe_count, deaths, hospitals_reporting, population, case_density)
SELECT
  'city',
  'NYC',
  'New York City',
  40.7128,
  -74.0060,
  CURRENT_DATE - (INTERVAL '1 day' * generate_series(0, 29)),
  89000 + (generate_series(0, 29) * 1200),
  (89000 + (generate_series(0, 29) * 1200)) * 0.78,
  (89000 + (generate_series(0, 29) * 1200)) * 0.15,
  (89000 + (generate_series(0, 29) * 1200)) * 0.07,
  890,
  45,
  8335897,
  ((89000 + (generate_series(0, 29) * 1200)) * 100.0) / 8335897;

INSERT INTO regional_summary (region_type, region_id, region_name, latitude, longitude, date, case_count, normal_count, pneumonia_count, severe_count, deaths, hospitals_reporting, population, case_density)
SELECT
  'city',
  'LA',
  'Los Angeles',
  34.0522,
  -118.2437,
  CURRENT_DATE - (INTERVAL '1 day' * generate_series(0, 29)),
  67500 + (generate_series(0, 29) * 950),
  (67500 + (generate_series(0, 29) * 950)) * 0.78,
  (67500 + (generate_series(0, 29) * 950)) * 0.15,
  (67500 + (generate_series(0, 29) * 950)) * 0.07,
  620,
  35,
  3990456,
  ((67500 + (generate_series(0, 29) * 950)) * 100.0) / 3990456;
