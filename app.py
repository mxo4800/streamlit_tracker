import pandas as pd
import streamlit as st
from data import mapping_placements, provide_notes, write_insights, create_chart


st.header("Campaign Tracker")

mapping_file = st.file_uploader("Upload mapping file", type=["csv"])
dcm_file = st.file_uploader("Upload dcm file", type=["csv"])

if mapping_file and dcm_file:

    mapping_file = pd.read_csv(mapping_file)
    dcm_file = pd.read_csv(dcm_file)


    new_data = mapping_placements(dcm_data=dcm_file, mapping_file=mapping_file)

    st.subheader("Mapping File")
    st.write(mapping_file)

    st.subheader("DCM File")
    st.write(dcm_file)


    st.subheader("DCM File with added Columns")
    st.write(new_data)

    st.subheader("Generate Cost File")
    cost = st.checkbox("Click to create cost")

    if cost:

        if "CPM" not in new_data.columns or "Impressions" not in new_data.columns:
            st.write("No cpm column")
        else:
            new_data["Total Spend"] = new_data["Impressions"] * new_data["CPM"] / 1000

            st.write(new_data)



    st.subheader("Generate Notes")
    camp_col = st.selectbox("Choose a column", new_data.columns)
    values = st.multiselect("Choose your values", new_data.columns)
    kpis = st.multiselect("Choose kpis to generate", ["CTR", "CPA", "CVR", "VCR", "None"])

    if camp_col and values and kpis:

        pivot_table = new_data.pivot_table(index=camp_col, values=values, aggfunc="sum").reset_index()


        if "None" not in kpis:

            for kpi in kpis:

                values.append(kpi)

                if kpi == "CTR":

                    try:
                        pivot_table["CTR"] = pivot_table["Clicks"] / pivot_table["Impressions"]
                    except Exception:
                        st.write("Clicks or Impressions not selected in values selection")

                elif kpi == "CPA":

                    try:

                        pivot_table["CPA"] = pivot_table["Total Spend"] / pivot_table["Total Conversions"]
                    
                    except Exception:

                        st.write("Total Spend or Total Conversions not selected in values selection")

                elif kpi == "CVR":

                    try:

                        pivot_table["CVR"] = pivot_table["Total Conversions"] / pivot_table["Impressions"]

                    except Exception:

                        st.write("Total Conversions or Impressions not selected in values selection")

                elif kpi == "VCR":

                    try:

                        pivot_table["VCR"] = pivot_table["Video Completions"] / pivot_table["Video Plays"]

                    except Exception:

                        st.write("Video Completions or Video Plays not selected in values selection")
        
        
        notes = provide_notes(pivot_table, camp_col, values=values)
        insights = write_insights(notes)


        words = ""

        for insight in insights:
            words+= "<br>"
            for note in insight:
                words += note + "<br>"

        st.write(words, unsafe_allow_html=True)

    st.subheader("Graph")
    graph = st.checkbox("Click to create graph")
    if graph:
        
        values_two  = st.multiselect("Choose  values", new_data.columns)
        kpis_two  = st.multiselect("Choose kpis ", ["CTR", "CPA", "CVR", "VCR", "None"])

        if values_two and kpis_two:


            pivot_table_two = new_data.pivot_table(index=["Date"], values=values_two, aggfunc="sum").reset_index()


            if "None" not in kpis_two:

                for kpi in kpis_two:

                    values_two.append(kpi)

                    if kpi == "CTR":

                        try:
                            pivot_table_two["CTR"] = pivot_table_two["Clicks"] / pivot_table_two["Impressions"]
                        except Exception:
                            st.write("Clicks or Impressions not selected in values selection")

                    elif kpi == "CPA":

                        try:

                            pivot_table_two["CPA"] = pivot_table_two["Total Spend"] / pivot_table_two["Total Conversions"]
                        
                        except Exception:

                            st.write("Total Spend or Total Conversions not selected in values selection")

                    elif kpi == "CVR":

                        try:

                            pivot_table_two["CVR"] = pivot_table_two["Total Conversions"] / pivot_table_two["Impressions"]

                        except Exception:

                            st.write("Total Conversions or Impressions not selected in values selection")

                    elif kpi == "VCR":

                        try:

                            pivot_table_two["VCR"] = pivot_table_two["Video Completions"] / pivot_table_two["Video Starts"]

                        except Exception:

                            st.write("Video Completions or Video Plays not selected in values selection")

            y_axis_one = st.selectbox("Select a KPI: ", pivot_table_two.columns)
            y_axis_two = st.selectbox("Select a value: ", pivot_table_two.columns)
            start_date = st.date_input("Select a start date")
            end_date = st.date_input("Select an end date")
            chart_title = st.text_input("Enter the title of your chart: ")

            if y_axis_one and y_axis_two and start_date and end_date and chart_title:

                start_date = pd.to_datetime(start_date)
                end_date = pd.to_datetime(end_date)

                create_chart(pivot_table_two, y_axis_one, y_axis_two, start_date, end_date, title=chart_title)
                st.write("Success")


            








