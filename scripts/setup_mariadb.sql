-- MariaDB setup for AirRouteIQ
-- Creates database, tables with ColumnStore and Vector columns

CREATE DATABASE IF NOT EXISTS airrouteiq;
USE airrouteiq;

-- Enable ColumnStore engine if available; fallback to InnoDB for dev
-- Note: ColumnStore requires MariaDB ColumnStore plugin installed and configured.

-- Countries (reference)
CREATE TABLE IF NOT EXISTS countries (
  id INT PRIMARY KEY,
  name VARCHAR(255),
  iso_code CHAR(2),
  iso3_code CHAR(3)
) ENGINE=InnoDB;

-- Airports (from OpenFlights)
CREATE TABLE IF NOT EXISTS airports (
  airport_id INT PRIMARY KEY,
  name VARCHAR(255),
  city VARCHAR(255),
  country VARCHAR(255),
  iata CHAR(3),
  icao CHAR(4),
  latitude DOUBLE,
  longitude DOUBLE,
  altitude INT,
  timezone DOUBLE,
  dst VARCHAR(8),
  tz_db VARCHAR(64),
  type VARCHAR(64),
  source VARCHAR(64)
) ENGINE=ColumnStore;

-- Airlines
CREATE TABLE IF NOT EXISTS airlines (
  airline_id INT PRIMARY KEY,
  name VARCHAR(255),
  alias VARCHAR(255),
  iata VARCHAR(8),
  icao VARCHAR(8),
  callsign VARCHAR(255),
  country VARCHAR(255),
  active CHAR(1)
) ENGINE=ColumnStore;

-- Routes (OpenFlights routes)
CREATE TABLE IF NOT EXISTS routes (
  route_id BIGINT PRIMARY KEY AUTO_INCREMENT,
  airline VARCHAR(8),
  airline_id INT,
  source_airport VARCHAR(8),
  source_airport_id INT,
  dest_airport VARCHAR(8),
  dest_airport_id INT,
  codeshare VARCHAR(8),
  stops INT,
  equipment VARCHAR(64)
) ENGINE=ColumnStore;

-- Synthetic passenger stats (ColumnStore for analytics)
CREATE TABLE IF NOT EXISTS passenger_stats (
  stat_id BIGINT PRIMARY KEY AUTO_INCREMENT,
  route_id BIGINT,
  year INT,
  month INT,
  passengers INT,
  load_factor DECIMAL(5,2),
  avg_delay_minutes DECIMAL(6,2)
) ENGINE=ColumnStore;

-- Delay risk scores per route (ColumnStore)
CREATE TABLE IF NOT EXISTS delay_risks (
  risk_id BIGINT PRIMARY KEY AUTO_INCREMENT,
  route_id BIGINT,
  weather_risk DECIMAL(5,2),
  congestion_risk DECIMAL(5,2),
  infra_risk DECIMAL(5,2),
  overall_risk DECIMAL(5,2)
) ENGINE=ColumnStore;

-- Vector table for route semantic descriptions
-- Requires MariaDB Vector (10.11+ with vector plugin), else fallback: store as TEXT and a FLOAT array columns
CREATE TABLE IF NOT EXISTS route_embeddings (
  route_id BIGINT PRIMARY KEY,
  description TEXT,
  embedding VECTOR(384)
);

-- Helpful indexes
CREATE INDEX IF NOT EXISTS idx_routes_src ON routes (source_airport_id);
CREATE INDEX IF NOT EXISTS idx_routes_dst ON routes (dest_airport_id);
CREATE INDEX IF NOT EXISTS idx_passenger_route ON passenger_stats (route_id);
CREATE INDEX IF NOT EXISTS idx_delay_route ON delay_risks (route_id);
