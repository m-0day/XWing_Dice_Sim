import plotly.graph_objects as go 
import pandas as pd
import numpy as np

#What in the hell
df = pd.read_csv('Dice_Rolls.csv')
str_cols = ['Phr', 'pe', 'ph']
for col in str_cols:
    df[col] = df[col].str.strip("[]")

i = 0
for i in range(len(df)):
    if i >= 24:
        print(round(i/599, 3)*100, "% done")
    df['Phr'][i] = " ".join(df['Phr'][i].split()) #this is so ridiculous
    df['Phr'][i] = [float(s) for s in df['Phr'][i].split(" ")]
    df['pe'][i] = " ".join(df['pe'][i].split())
    df['pe'][i] = [float(s) for s in df['pe'][i].split(" ")]
    df['ph'][i] = " ".join(df['ph'][i].split())
    df['ph'][i] = [float(s) for s in df['ph'][i].split(" ")]


row = df.iloc[303]
N = (row['M_atk_dice'])
nPhr = row.Phr
nhits = np.arange(M+1)


fig = go.Figure()

fig.add_trace(
    go.Bar(x = hits, 
    y = Phr)
)

fig.add_trace(
    go.Bar(x = nhits,
    y = nPhr)
)


fig.update_layout(
    updatemenus = [
        dict(
            active = 0,
            buttons = list([
                dict(labels = "M",
                method = "update",
                args = )
            ])
        )
    ]
)

fig.show()