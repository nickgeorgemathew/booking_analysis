import numpy as np
import pandas as pd
def add_bins_dayparts(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    # Lead bins
    lead_bins=[-np.inf,3,7,14,30,90,np.inf]
    lead_bins_label=['0','1-3','4-7','8-14','15-30','31-90','90+']
    df['lead_bins']=pd.cut(df['purchase_lead'].clip(lower=0),bins=lead_bins,label=lead_bins_label,include_lowest=True)
    # length of stay bins
    stay_bins=[-np.inf,3,7,14,30,90,np.inf]
    stay_bins_label=['0-3','4-7','8-14','15-30','31-90','90+']
    df['stay_bin']=pd.cut(df['length_of_stay'].clip(lower=0),bins=stay_bins,label=stay_bins_label,include_lowest=True)
    #part of the day
    def day_part(h):
        if 0 <= h <= 5: return 'night'
        if 6 <= h <= 11: return 'morning'
        if 12 <= h <= 17: return 'afternoon'
        return 'evening'
    df['daypart'] = df['booking_hour'].apply(day_part)

    # Weekday mapping (if needed)
    weekday_map = {'Mon':1,'Tue':2,'Wed':3,'Thu':4,'Fri':5,'Sat':6,'Sun':7}
    df['flight_day_num'] = df['flight_day'].map(weekday_map)

