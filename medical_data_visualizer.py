import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# 1
df = pd.read_csv("medical_examination.csv")

# 2
df['overweight'] = (( df['weight'] / (df['height']/100)**2 ) > 25 ).astype(int)

# 3
df['cholesterol'] = (df['cholesterol'] != 1).astype(int)
df['gluc'] = (df['gluc'] != 1).astype(int)

# 4
def draw_cat_plot():
    # 5
    df_cat = pd.melt(
        df, 'cardio',
        ['active', 'alco', 'cholesterol', 'gluc', 'overweight', 'smoke'],
    )

    # 6
    df_cat = df_cat.value_counts().reset_index().sort_values('variable').rename(columns={0:'total'})

    # 7
    sns_plot = sns.catplot(
        df_cat, x='variable', y='total', 
        kind='bar', col='cardio', hue='value'
    )

    # 8
    fig = sns_plot.figure

    # 9
    fig.savefig('catplot.png')
    return fig

# 10
def draw_heat_map():
    # 11
    df_heat = df[
        (df['ap_lo'] <= df['ap_hi']) &
        (df['height'] >= df['height'].quantile(0.025)) &
        (df['height'] <= df['height'].quantile(0.975)) &
        (df['weight'] >= df['weight'].quantile(0.025)) &
        (df['weight'] <= df['weight'].quantile(0.975))
    ]

    # 12
    corr = df_heat.corr()

    # 13
    mask = np.triu(corr).astype(bool)

    # 14
    fig, ax = plt.subplots(figsize=(12,9))

    # 15
    sns.heatmap(
        corr, mask = mask, ax=ax,
        annot=True, fmt='.1f',
        linewidths='0.5', square=True,
        center=0,
        vmax=0.3, vmin=-.15,
        cbar_kws=dict(
            ticks = [0.24, 0.16, 0.08, 0, -0.08], 
            shrink=0.5
        )
    )

    # 16
    fig.savefig('heatmap.png')
    return fig
