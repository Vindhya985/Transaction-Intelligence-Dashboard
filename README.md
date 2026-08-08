Transaction Intelligence Dashboard

An end-to-end financial analytics and fraud detection platform. The system ingests raw transaction data, processes core financial metrics, and uses Machine Learning to detect potential anomalies or unauthorized transactions.

 Key Features & Division of Work-

Backend & Machine Learning Engine *(ML & Core Logic)*
* **Data Ingestion & Cleaning:** Standardizes raw transaction CSVs, cleans missing fields, and handles numerical formatting.
* **Financial Analytics Module:** Computes spending breakdowns, total transaction metrics, and category distributions.
* **ML Anomaly Detection:** Implements an unsupervised `IsolationForest` model to dynamically analyze transaction features (`Debit`, `Credit`, `Balance`) and tag outliers under `Anomaly_Status`.
* **Testing Pipeline:** Includes dedicated test suites (`test_analytics.py`, `test_anomaly.py`) for local verification.

Frontend & API Layer *(Interface & Services)*
* **FastAPI Backend:** Exposes RESTful API endpoints for seamless data flow between the ML engine and user interface.
* **Interactive Streamlit Dashboard:** Provides a responsive UI with real-time financial summaries, interactive charts, and flagged anomaly views.

Project Structure-
                                                                                                                                                                                                      
Transaction-Intelligence-Dashboard/                                                                                                                                                                   
├── Backend/                                                                                                                                                                                          
│   └── api.py                  # FastAPI server & REST API endpoints                                                                                                                                 
├── Frontend/                                                                                                                                                                                         
│   └── app.py                  # Streamlit dashboard & UI layout                                                                                                                                     
├── Data/                                                                                                                                                                                             
│   ├── sample-100-rows.csv     # Raw input datasets                                                                                                                                                  
│   └── cleaned_sample_...csv   # Preprocessed output datasets                                                                                                                                        
├── ML/                                                                                                                                                                                               
│   ├── main.py                 # Data preprocessing pipeline                                                                                                                                         
│   ├── analytics.py            # Financial metric calculation engine                                                                                                                                 
│   ├── anomaly.py              # Isolation Forest anomaly detection model                                                                                                                            
│   ├── test_analytics.py      # Test suite for analytics module                                                                                                                                      
│   └── test_anomaly.py        # Test suite for ML anomaly detection                                                                                                                                  
├── requirements.txt            # Project dependencies                                                                                                                                                
└── README.md                   # Project documentation                                                                                                                                               


Tech stack -
Language: Python 3.10+
Data Science & ML: pandas, numpy, scikit-learn (IsolationForest)
Backend API: FastAPI / Uvicorn
Frontend UI: Streamlit
Version Control: Git & GitHub


Machine Learning Architecture
The anomaly detection module (ML/anomaly.py) uses an Isolation Forest model designed for unsupervised outlier detection:
Dynamic Feature Selection: Pulls numerical fields (Debit, Credit, Balance) adaptively across different dataset schemas.
Model Training: Fits the model using a sensitivity threshold (contamination=0.05).
Output Mapping: Converts raw outputs (1 for normal, -1 for anomaly) into human-readable 'normal' and 'Anomaly' labels.
Data Filtering: Uses get_flagged_transactions() to deliver tagged anomalies directly to the FastAPI layer for Streamlit rendering.
