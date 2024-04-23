import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.dates as mdates
import matplotlib.lines as mlines
import streamlit as st

def mapper(row, col, mapping_file):

    filtered_mapping = mapping_file[mapping_file["Placement"] == row]

    try:
        val_to_return = filtered_mapping[col].iloc[0]
    except:
        return None

    return val_to_return



def mapping_placements(dcm_data, mapping_file):

    # dcm_data = pd.read_csv(dcm_data)
    # mapping_placements = pd.read_csv(mapping_file)

    for col in list(mapping_file.columns):

        if col != "Placement":

            if mapping_file[col].notnull().sum() != 0:

                dcm_data[col] = dcm_data["Placement"].apply(lambda row: mapper(row, col, mapping_file))


    return dcm_data


def data_pivot_table(data, cols=[], values=[]):

    pivoted_table = data.pivot_table(index=cols, values=values, aggfunc="sum").reset_index()

    return pivoted_table


def provide_notes(pivoted_data, col, values=[]):

    notes = []
    
    for val in pivoted_data[col]:

        filtered_pivot = pivoted_data[pivoted_data[col] == val]
        
        note = [(col, val)]
        for value in values:

            more_notes = (value, filtered_pivot[value].iloc[0])
            note.append(more_notes)
        
        notes.append(note)

    return notes


def write_insights(notes=[]):
    insights = []

    for note in notes:
        insight = []

        for idx, val in enumerate(note):
            if idx == 0:
                words = f"{val[1]} {val[0]}"
            else:
                words = f"-{val[1]} {val[0]}"

            insight.append(words)

        insights.append(insight)

    return insights


def create_chart(data, y_axis_1, y_axis_2, start_date, end_date, title="My Chart"):


    data["Date"] = pd.to_datetime(data["Date"])

    plot_data = data[(data["Date"] >= pd.to_datetime(start_date)) & (data["Date"] <= pd.to_datetime(end_date))].copy()

    # Create a figure and axis
    fig, ax1 = plt.subplots(figsize=(15, 8))

    # Create a line plot for CPA on the primary y-axis with purple color
    sns.lineplot(x='Date', y=y_axis_1, data=plot_data, ax=ax1, marker='o', label=y_axis_1, color='purple')
    ax1.set_xlabel('Date')
    ax1.set_ylabel(y_axis_1, color='purple')  # Add dollar sign to the y-axis label
    ax1.tick_params(axis='y', labelcolor='purple')

    # Create a bar plot for Cost on the secondary y-axis
    ax2 = ax1.twinx()
    ax2.bar(plot_data['Date'], plot_data[y_axis_2], alpha=0.5, color='tab:orange', label=y_axis_2)
    ax2.set_ylabel(y_axis_2, color='tab:orange')
    ax2.tick_params(axis='y', labelcolor='tab:orange')

    # Explicitly set the x-ticks and labels for each date from '11-01' to '11-30'
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    # print(date_range)
    ax1.set_xticks(mdates.date2num(date_range))  # Convert dates to numerical format
    ax1.set_xticklabels(date_range.strftime('%m-%d'), rotation=45)


    # Annotate the line graph with CPA values including a dollar sign
    for index, row in plot_data.iterrows():
        ax1.text(row['Date'], row[y_axis_1], f'{row[y_axis_1]:.2f}', ha='center', va='bottom', fontsize=8, color='purple')

    # Set labels and title
    plt.title(title, fontsize=20, pad=20)
    plt.legend(loc='center left')

    # # Show the plot
    # plt.tight_layout()

    st.pyplot(fig)











