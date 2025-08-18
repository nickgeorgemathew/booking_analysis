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
- figures/: exported plots
- reports/: final visuals or markdown exports

How to Run
1. Create and activate virtual environment
2. pip install -r requirements.txt
3. Open notebooks/01_eda.ipynb for EDA and feature creation
4. Open notebooks/02_model.ipynb to train and evaluate models
5. Outputs will be saved to figures/ and reports/

Key Results (to update after Day 2)
- F1: …
- Accuracy: …
- Confusion Matrix: (insert image)
- Top 5 Features: …

Repo Images
- Insert 1–2 key plots (EDA rate plot, feature importance)

Next Steps
- A/B test timing/urgency nudges
- SHAP for local explanations
- Real-time scoring pipeline
