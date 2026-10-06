# Alcohol Detection & Real-Time Alert System

This is a hardware-integrated IoT project designed for real-time alcohol detection and remote monitoring.

## About the Project

The system uses an **MQ-2 gas sensor** connected to an **Arduino Uno** to monitor the presence of alcohol. When the sensor detects high alcohol levels, the hardware triggers a local buzzer alarm to provide an immediate alert.

Simultaneously, the Arduino transmits the sensor readings over a serial connection to a Python bridge script. This script securely uploads the data to a **Supabase** backend database. The data is then visualized in real-time on a modern, glassmorphism-styled web dashboard, providing a seamless remote monitoring experience.

## Components

1.  **`bridge.py`**: A Python script that reads data from the Arduino (Serial port `COM7`) and syncs it to Supabase.
2.  **`index.html`**: A "Vanishingly Modern" dashboard with real-time updates and glassmorphism design.

## Setup Instructions

### 1. Supabase Setup
Create a table in your Supabase project with the following structure:

```sql
create table alcohol_logs (
  id bigint primary key generated always as identity,
  created_at timestamptz default now(),
  level int4
);

-- Enable Realtime for this table
alter publication supabase_realtime add table alcohol_logs;
```

### 2. Python Bridge Setup
1.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
2.  Create a `.env` file in the same directory (you can copy `.env.example` to `.env`) and add your credentials:
    ```env
    SUPABASE_URL="YOUR_SUPABASE_URL"
    SUPABASE_KEY="YOUR_SERVICE_ROLE_KEY"
    SERIAL_PORT="COM7"
    ```
3.  Run the bridge:
    ```bash
    python bridge.py
    ```

### 3. Dashboard Setup
1.  Open `index.html` and replace placeholders:
    - `YOUR_SUPABASE_URL`
    - `YOUR_SUPABASE_ANON_KEY`
2.  Open `index.html` in any modern web browser.

## Features
- **Central Aura**: Glows **Emerald Green** (Safe) or pulses **Neon Red** (Danger > 600).
- **Real-Time Gauge**: Minimalist numeric display of raw PPM level.
- **Incident History**: Sliding side panel showing "Intoxication Events" with timestamps.
- **Glassmorphism**: Modern, translucent UI elements.
- **Interactive**: Hover effects and smooth transitions.
