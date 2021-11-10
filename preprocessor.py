import pandas as pd


def preprocess(df, region_df): 
   # Filtering for summer olympics
   df = df[df['Season'] == 'Summer']
   # Merge with region_df
   df = df.merge(region_df, on='NOC', how='left')
   df.drop_duplicates(inplace=True)
   # One hot encoding medal
   df = pd.concat([df, pd.get_dummies(df['Medal'])], axis=1)
   return df