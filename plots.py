from datetime import datetime

import pandas as pd

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import EngFormatter

import plotly.express as px


DATA = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv'

df = pd.read_csv(DATA)
df['date'] = pd.to_datetime(df['date'])
first_date = min(df.dropna(subset=['total_cases'])['date'])
last_date = datetime.fromisoformat('2022-07-31')

# ----------------------------- Matplotlib -----------------------------------

plt.style.use('fivethirtyeight')

params = {
    'lines.linewidth': 2.0,
    'axes.labelsize': 16,
    'axes.titlesize': 16,
    'axes.spines.top': False,
    'axes.spines.right': False,
    'axes.facecolor': 'white',
    'axes.edgecolor': 'white',
    'xtick.labelsize': 16,
    'ytick.labelsize': 16,
    'figure.facecolor': 'white',
    'figure.edgecolor': 'white',
    'figure.autolayout': True,
    'figure.titlesize': 24,
    'figure.figsize': (14, 8),
    'legend.shadow': False,
    'legend.fontsize': 13,
    'hatch.linewidth': 3,
    'grid.alpha': 0.3,
}

plt.rcParams.update(params)

myFmt = mdates.DateFormatter("%Y-%m")
eng_format = EngFormatter(places=2)
eng_format_k = EngFormatter(places=0)

variants = {
    'alfa': '2020-09-01',
    'beta': '2020-05-01',
    'gama': '2020-11-01',
    'delta': '2020-10-01',
    'lambda': '2020-12-01',
    'mu': '2021-01-01',
    'omicron': '2021-11-01',
}

variants = {key: datetime.fromisoformat(
    value) for (key, value) in variants.items()}

colors = plt.cm.Dark2.colors  # cores para as linhas das variantes


def linear_log_scales(x, y, y_axis_name, sup_title, y_label='',
                      y_smooth=None, y_smooth_label='',
                      text='', variants_lines=False,
                      x_rotation=70, fill_alpha=0.25, date_month_interval=2,
                      linear_title='Линейная',
                      log_title='Логарифмическая',
                      legend=False, legend_bbox=(0.5, 0.885),
                      limit_dates=True):

    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2)

    for ax in (ax1, ax2):
        ax.xaxis.set_major_locator(
            mdates.MonthLocator(interval=date_month_interval))
        ax.xaxis.set_major_formatter(myFmt)
        ax.tick_params(axis='x', rotation=x_rotation)
        ax.set_ylabel(y_axis_name)
        ax.fill_between(x, y, alpha=fill_alpha)

    ax1.plot(x, y, label=y_label)
    ax1.set_title(linear_title)
    ax1.yaxis.set_major_formatter(EngFormatter())

    ax2.plot(x, y, label=y_label)
    ax2.set_yscale('log')
    ax2.yaxis.set_major_formatter(EngFormatter())
    ax2.set_title(log_title)

    if limit_dates:
        ax1.set_xlim(first_date, last_date)
        ax2.set_xlim(first_date, last_date)

    if y_smooth is not None:
        for ax in (ax1, ax2):
            ax.plot(x, y_smooth, label=y_smooth_label)

        handles, labels = ax1.get_legend_handles_labels()

    if variants_lines:

        for color, var in zip(colors, variants):
            for ax in (ax1, ax2):
                ax.axvline(x=variants[var], label=var, linestyle='dotted',
                           linewidth=2.5, color=color)

        handles, labels = ax.get_legend_handles_labels()

    if legend:
        fig.legend(bbox_to_anchor=legend_bbox, loc='upper center', ncol=9,
                   handles=handles, labels=labels, fontsize=12)

    plt.suptitle(sup_title, color='dimgray')
    plt.gcf().text(0.025, 0.865, text, fontsize=18, color='gray')

    plt.show()


def winter(x, y, y_axis_name, sup_title, y_label='',
           y_smooth=None, y_smooth_label='',
           text='', variants_lines=False,
           x_rotation=70, date_month_interval=1,
           legend=False, legend_bbox=(0.5, 0.885),
           limit_dates=True, south_hem=True, north_hem=True,
           south_label='Inverno Hem. Sul',
           north_label='Inverno Hem. Norte',
           engfmt=True):

    fig, ax = plt.subplots()
    ax.xaxis.set_major_locator(
        mdates.MonthLocator(interval=date_month_interval))
    ax.xaxis.set_major_formatter(myFmt)
    ax.tick_params(axis='x', rotation=x_rotation)
    ax.set_ylabel(y_axis_name)

    ax.plot(x, y, label=y_label)

    if engfmt:
        ax.yaxis.set_major_formatter(EngFormatter())

    if limit_dates:
        ax.set_xlim(first_date, last_date)

    if y_smooth is not None:
        ax.plot(x, y_smooth, label=y_smooth_label)

        handles, labels = ax.get_legend_handles_labels()

    if variants_lines:

        for color, var in zip(colors, variants):
            ax.axvline(x=variants[var], label=var, linestyle='dotted',
                       linewidth=2.5, color=color)

        handles, labels = ax.get_legend_handles_labels()

    if north_hem:
        ax.axvspan(*mdates.datestr2num(['2020-12-22', '2021-03-20']),
                   color='blue', alpha=0.15, label=north_label)
        ax.axvspan(*mdates.datestr2num(['2021-12-22', '2022-03-20']),
                   color='blue', alpha=0.15)
        handles, labels = ax.get_legend_handles_labels()

    if south_hem:
        ax.axvspan(*mdates.datestr2num(['2020-06-21', '2020-09-23']),
                   color='purple', alpha=0.15, label=south_label)
        ax.axvspan(*mdates.datestr2num(['2021-06-21', '2021-09-23']),
                   color='purple', alpha=0.15)
        handles, labels = ax.get_legend_handles_labels()

    if legend:
        fig.legend(bbox_to_anchor=legend_bbox, loc='upper center', ncol=9,
                   handles=handles, labels=labels, fontsize=12)

    plt.suptitle(sup_title, color='dimgray')
    plt.gcf().text(0.025, 0.865, text, fontsize=18, color='gray')

    plt.show()


def hbars_top10(dataframe, column_labels, column_values, sup_title,
                text='', korea_position=None, padding=-75, font_color='white',
                fmt_function=eng_format, star=False, star_position=(125, 0.2)):

    fig, ax = plt.subplots()
    bars = ax.barh(column_labels, column_values, data=dataframe)
    ax.invert_yaxis()
    labels = dataframe[column_values].values
    bars_labels = ax.bar_label(ax.containers[0], padding=padding,
                               labels=map(fmt_function, labels),
                               color=font_color, fontsize=16, weight='bold')

    ax.set_frame_on(False)
    ax.set_xlabel(None)
    ax.set_ylabel(None)
    ax.set_xticklabels([])
    ax.set_xticks([])
    ax.grid(False)

    if korea_position:
        bars[korea_position-1].set(color='green',
                                    edgecolor='yellow', hatch='/', alpha=0.7)
        bars_labels[korea_position-1].set(color='midnightblue')

    if star:
        ax.annotate('*', xy=star_position,
                    xytext=star_position, size=20, color='red')

    plt.suptitle(sup_title, color='dimgray')
    plt.gcf().text(0.025, 0.85, text, fontsize=18, color='gray')
    plt.show()


def comparing_locations(dataframe, column_x, column_values, y_axis_name,
                        locations, sup_title,
                        text='', x_rotation=70, date_month_interval=1,
                        legend=True, legend_bbox=(0.5, 0.885),
                        limit_dates=True,
                        engfmt=True, ylog=False):

    fig, ax = plt.subplots()
    ax.xaxis.set_major_locator(
        mdates.MonthLocator(interval=date_month_interval))
    ax.xaxis.set_major_formatter(myFmt)
    ax.tick_params(axis='x', rotation=x_rotation)
    ax.set_ylabel(y_axis_name)

    for location in locations:
        x = dataframe.loc[dataframe['location'] == location, column_x]
        y = dataframe.loc[dataframe['location'] == location, column_values]
        ax.plot(x, y, label=location)

    if engfmt:
        ax.yaxis.set_major_formatter(EngFormatter())

    if limit_dates:
        ax.set_xlim(first_date, last_date)

    if ylog:
        ax.set_yscale('log')

    if legend:
        handles, labels = ax.get_legend_handles_labels()
        fig.legend(bbox_to_anchor=legend_bbox, loc='upper center', ncol=9,
                   handles=handles, labels=labels, fontsize=12)

    plt.suptitle(sup_title, color='dimgray')
    plt.gcf().text(0.025, 0.865, text, fontsize=18, color='gray')

    plt.show()


# ----------------------------- Plotly---- -----------------------------------
plotly_cont_scale = 'dense'


def treemap(df_locations, df_world_data, df_continents_data,
            column_values, sup_title, text):

    fig = px.treemap(df_locations.dropna(how='all', subset=[column_values]),
                     path=[px.Constant('World'), 'continent', 'location'],
                     values=column_values,
                     color=column_values,
                     color_continuous_scale=plotly_cont_scale,
                     custom_data=[column_values],
                     )

    fig.data[0].customdata[-1] = df_world_data.loc[df_world_data['date']
                                                   == last_date, column_values]
    fig.data[0].customdata[-7:-1] = df_continents_data[[column_values]].values

    fig.update_traces(hovertemplate='<b>%{label}</b><br>%{customdata:,.2f}')
    fig.update_layout(margin=dict(t=80, l=0, r=0, b=10),
                      coloraxis_colorbar=dict(title=None, thickness=30, len=1),
                      title={
        'text': sup_title,
        'font': {'size': 24, 'color': 'dimgray'},
        'y': 0.95,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
        annotations=[{
            'text': text,
            'font': {
                'size': 18,
                'color': 'gray',
            },
            'showarrow': False,
            'align': 'left',
            'x': 0.0,
            'y': 1.1,
            'xanchor': 'left',
            'yanchor': 'top',
        }])

    fig.show()


def animated_map(df_locations, column_id, column_values, column_hover,
                 sup_title, text, colorbar_title='',
                 width=900, height=550):

    fig = px.choropleth(df_locations, locations=column_id,
                        color=column_values,
                        hover_name=column_hover,
                        color_continuous_scale=plotly_cont_scale,
                        width=width,
                        height=height,
                        animation_frame=df_locations.index.astype(str),
                        animation_group=column_id
                        )

    fig.update_layout(
        geo=dict(
            showframe=False,
            showcoastlines=False,
            projection_type='equirectangular',
            resolution=110
        ),
        margin=dict(t=80, l=0, r=0, b=0),
        coloraxis_colorbar=dict(title=colorbar_title, thickness=30, len=1),
        title={
            'text': sup_title,
            'font': {'size': 24, 'color': 'dimgray'},
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        annotations=[{
            'text': text,
            'font': {
                'size': 18,
                'color': 'gray',
            },
            'showarrow': False,
            'align': 'left',
            'x': 0.0,
            'y': 1.1,
            'xanchor': 'left',
            'yanchor': 'top',
        }])

    fig.show()


def bubble_scatter(df_locations, column_x, column_y, column_size,
                   column_color, column_hover, x_label, y_label,
                   sup_title, text, legend_title='',
                   size_max=40, width=900, log_x=False):

    fig = px.scatter(df_locations.dropna(how='all', subset=[column_size]),
                     x=column_x,
                     y=column_y,
                     size=column_size,
                     color=column_color,
                     hover_name=column_hover,
                     size_max=size_max,
                     width=width,
                     log_x=log_x
                     )

    fig.update_layout(
        margin=dict(t=80, l=0, r=200, b=10),
        title={
            'text': sup_title,
            'font': {'size': 24, 'color': 'dimgray'},
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis={
            'title': x_label,
        },
        yaxis={
            'title': y_label,
        },
        legend={
            'title': legend_title
        },
        annotations=[{
            'text': text,
            'font': {
                'size': 18,
                'color': 'gray',
            },
            'showarrow': False,
            'align': 'left',
            'x': 0.0,
            'y': 1.1,
            'xanchor': 'left',
            'yanchor': 'top',
            'xref': 'paper',
            'yref': 'paper',
        }]
    )

    fig.show()
