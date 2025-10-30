# Real-time Stock Analysis with Apache Flink and AWS

This project demonstrates a real-time stock price analysis pipeline using **Apache Flink**, **AWS Kinesis**, **S3**, and **Lambda functions**. The pipeline computes technical indicators and detects anomalies in stock prices.

---

## Project Overview

- **Objective:** Compute CMGR (Compound Monthly Growth Rate), 10-day EMA (Exponential Moving Average), and detect anomalous price drops (≥8%) in real-time stock data.
- **Data:** Historical AMD stock prices (2021–2022) stored in CSV format.
- **Pipeline Flow:**
  1. Historical CSV data is loaded into a **Kinesis stream** via `parse_csv_lambda`.
  2. **Flink application** processes the stream to compute indicators and detect anomalies.
  3. Results are stored in **S3** (`part_a`, `part_b`, `part_c`) and can be accessed via `output_lambda`.
  4. `input_lambda` can simulate real-time stock price updates for testing the pipeline.

---

## System Architecture

```
CSV (AMDprices2021-2022.csv)
        │
        ▼
parse CSV lambda / input lambda
        │
        ▼
Kinesis Data Stream (mp10-new-data-stream)
        │
        ▼
Flink Managed Job
 ┌─────────────┬──────────────┬─────────────┐
 │ Exercise A  │ Exercise B   │ Exercise C  │
 │  CMGR       │  EMA         │ Anomaly     │
 └─────────────┴──────────────┴─────────────┘
        │          │              │
        ▼          ▼              ▼
     S3/part_a   S3/part_b      S3/part_c
        │          │              │
        └──────────┴──────────────┘
                   │
                   ▼
              output lambda
```

---

## Folder Structure

```
project/
├─ notebooks/
│ ├─ Exercise_A.ipynb # CMGR calculation
│ ├─ Exercise_B.ipynb # 10-day EMA calculation
│ ├─ Exercise_C.ipynb # Anomaly detection using MATCH_RECOGNIZE
│ ├─ Exercise_D.ipynb # Integrated Flink pipeline (A+B+C)
├─ lambda/
│ ├─ parse_csv_lambda.py # Load historical CSV into Kinesis
│ ├─ input_lambda.py # Simulate real-time stock data into Kinesis
│ └─ output_lambda.py # Read results from S3
├─ example_data/
│ └─ AMDprices2021-2022_sample.csv # Sample data
```

---

## Key Contributions

- Implemented **CMGR UDF** in PyFlink to compute compound monthly growth rates.
- Developed **10-day EMA** calculation in Flink SQL with sliding window.
- Designed **anomaly detection** using `MATCH_RECOGNIZE` for sudden price drops.
- Integrated all analyses into a single **Flink pipeline** (`exercise_d.ipynb`) writing results to S3.
- Configured **Lambda functions** to simulate real-time stock data and retrieve analysis results.

---

## How to Run

1. Upload sample CSV to S3.
2. Deploy Lambda functions (`parse_csv_lambda`, `input_lambda`, `output_lambda`) with appropriate IAM permissions.
3. Submit the Flink pipeline (`exercise_d.ipynb`) to **AWS Kinesis Managed Flink**.
4. Use `input_lambda` to push real-time data for testing.
5. Access results via `output_lambda` or S3 JSON files.

---

## Notes

- Historical data is used to **initialize the pipeline and compute baseline indicators**.
- `input_lambda` simulates **real-time data**, allowing Flink to update indicators and detect anomalies dynamically.
- This project demonstrates **stream processing, UDF creation, window functions, and anomaly detection** with Apache Flink on AWS.