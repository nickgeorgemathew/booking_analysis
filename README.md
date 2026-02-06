# Booking Analysis + Predictions

Problem
- Predict booking completion and identify top drivers to improve conversion.

Data
- Briefly describe dataset source and key fields (purchase_lead, length_of_stay, device_type, channel, booking_hour, flight_day, target booking_complete).

Success Metric
- Primary: F1-score on test set.
- Secondary: Accuracy and Confusion Matrix.

Project Structure
- data/: raw, processed, external
- notebooks/: 01_eda.ipynb, 02_model.ipynb
- src/: data (loading), features (engineering), models (training/eval), utils (helpers)


How to Run
1. Create and activate virtual environment
2. pip install -r requirements.txt
3. Open notebooks/01_eda.ipynb for EDA and feature creation
4. Open notebooks/02_model.ipynb to train and evaluate models


Key Results 
- Best model (Random Forest + SMOTE):  
  - F1 (completed class) ≈ 0.41  
  - Recall (completed class) ≈ 0.58  
  - ROC–AUC ≈ 0.77
  - View insights table for more info



