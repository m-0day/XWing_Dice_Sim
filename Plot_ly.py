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

test_len = 20
fig = go.Figure()
r = range(test_len)

for j in r:
    row = df.iloc[j]
    M = (row['M_atk_dice'])
    mPhr = row.Phr
    mhits = np.arange(M+1)

    fig.add_trace(
        go.Bar(x = mhits, 
        y = mPhr,
        visible = False)
    )


c = []
for j in r:
    b = [False]*test_len
    b[j] = True
    c.append(
            dict(
                dict(label = str(j),
                method = "update",
                args = [ {"visible": b} ]
                )
            )
        )


fig.update_layout(
    updatemenus = [
        dict(
            active = 0,
            buttons = c
        )
    ]
)

#now how do I make it so I have 6 drop downs:
# M atk dice (1:6)
# N def dice (1:6)
# atk_tl    (Yes, No)
# atk_f     (Yes, No)
# def_f     (Yes, No)
# def_evades (0:2)

# and then these correctly combine to index the appropriate bar trace

fig.show()