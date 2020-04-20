import plotly.graph_objects as go 
import pandas as pd
import numpy as np
from ipywidgets import widgets

#What in the hell
df = pd.read_csv('Dice_Rolls.csv')
df = df.drop(['Unnamed: 0'], axis = 1)
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


### Begin to make plotly widgets ###
test_len = 20
fig = go.Figure()
r = range(test_len)

# Add all the traces in the range #
# used to work
# for j in r:
#     row = df.iloc[j]
#     M = (row['M_atk_dice'])
#     mPhr = row.Phr
#     mhits = np.arange(M+1)

#     fig.add_trace(
#         go.Bar(x = mhits, 
#         y = mPhr,
#         visible = False)
#     )

# toggle the i'th trace to visible
steps = []
for j in r:
    step = dict(
        method="restyle",
        args=["visible", [False] * test_len],
    )
    step["args"][1][j] = True  # Toggle i'th trace to "visible"
    steps.append(step)


atk_dice = widgets.IntSlider(
    value = 1.0,
    min = 1.0,
    max = 6.0,
    step = 1.0,
    description = 'Number of Attack Dice',
    continuous_update = False)

def_dice = widgets.IntSlider(
    value = 1.0,
    min = 1.0,
    max = 6.0,
    step = 1.0,
    description = 'Number of Defense Dice',
    continuous_update = False)

tgt_lk = widgets.Checkbox(
    description = 'Target Lock',
    value = False)

container = widgets.HBox(children = [atk_dice, def_dice, tgt_lk])

j = 1
row = df.iloc[j]
M = (row['M_atk_dice'])
mPhr = row.Phr
mhits = np.arange(M+1)
trace1 = go.Bar(x = mhits, y = mPhr, opacity= 0.8, name = 'pdf')
g = go.FigureWidget(data = trace1, layout = go.Layout(
    title = dict(text = 'PDF')
))

widgets.VBox([container])


fig.show()






## # make sliders, part of used to work
# sliders = [
#     dict(
#         active=10,
#         currentvalue={"prefix": "Frequency: "},
#         pad={"t": 10},
#         steps=steps
#     ),
#     dict(
#         active=5,
#         currentvalue={"prefix": "Test: "},
#         pad={"t": 100},
#         steps=steps
#     )
# ]



# def response(change):
#     if use_date.value:
#         filter_list = [i and j and k for i, j, k in
#                         zip(df['month'] == month.value, df['carrier'] == textbox.value,
#                             df['origin'] == origin.value)]
#         temp_df = df[filter_list]

#     else:
#         filter_list = [i and j for i, j in
#                         zip(df['carrier'] == 'DL', df['origin'] == origin.value)]
#         temp_df = df[filter_list]
#     x1 = temp_df['arr_delay']
#     x2 = temp_df['dep_delay']
#     with g.batch_update():
#         g.data[0].x = x1
#         g.data[1].x = x2
#         g.layout.barmode = 'overlay'
#         g.layout.xaxis.title = 'Delay in Minutes'
#         g.layout.yaxis.title = 'Number of Delays'

## This part used to work and is commented out
#update the figure with sliders
# fig.update_layout(
#     sliders = sliders,
#     yaxis = dict(
#         title_text = "Probability",
#     )
# )

# fig.update_yaxes(automargin = True)



# updatemenus = []
# for j in r:
#     b = [False]*test_len
#     b[j] = True
#     updatemenus.append(
#         dict(
#             dict(label = str(j),
#             method = "update",
#             args = [ {"visible": b} ]
#             )
#         )
#     )


# fig.update_layout(
#     updatemenus = updatemenus
# )

#now how do I make it so I have 6 drop downs:
# M atk dice (1:6)
# N def dice (1:6)
# atk_tl    (Yes, No)
# atk_f     (Yes, No)
# def_f     (Yes, No)
# def_evades (0:2)

# and then these correctly combine to index the appropriate bar trace

# fig.show()