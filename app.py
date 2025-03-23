## code 
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
st.set_page_config(layout='wide')

df = pd.read_csv('/content/india_2011_census_data')

st.title("📊 2011 Census India Data Visualization")

list_of_state = list(df['State'].unique())
list_of_state.insert(0, 'Overall India')

list_of_district = list(df['District'].unique())
list_of_district.insert(0, 'Overall State')

st.sidebar.title("Data Exploration")
selected_state = st.sidebar.selectbox('Select a state', list_of_state)
selected_district = st.sidebar.selectbox('Select a district', list_of_district)

primary = st.sidebar.selectbox('Select primary parameter', sorted(df.columns[5:]))
secondary = st.sidebar.selectbox('Select secondary parameter', sorted(df.columns[5:]))

plot_state = st.sidebar.button('Plot State Graph')
plot_district = st.sidebar.button('Plot District Graph')

if plot_state:
    st.text('Size represents primary parameter')
    st.text('Color represents secondary parameter')

    if selected_state == 'Overall India':
        fig = px.scatter_map(
            df, lat="Latitude", lon="Longitude", color=primary, size=secondary,
            color_continuous_scale=px.colors.cyclical.IceFire, size_max=20, zoom=4,
            hover_name="State", hover_data={"District": True,'State':True, "Latitude": True, "Longitude": True, "Population": True},
            title="Population Distribution by State"
        )
    else:
        state_df = df[df['State'] == selected_state]
        fig = px.scatter_map(
            state_df, lat="Latitude", lon="Longitude", color=primary, size=secondary,
            color_continuous_scale=px.colors.cyclical.IceFire, size_max=20, zoom=4,
            hover_name="State", hover_data={"District": True, "Latitude": True, "Longitude": True, "Population": True},
            title=f"Population Distribution in {selected_state}"
        )

    fig.update_layout(mapbox_style="carto-positron", margin={"r": 0, "t": 50, "l": 0, "b": 0})
    st.plotly_chart(fig, use_container_width=True)

if plot_district:
    if selected_district != 'Overall State':
        district_df = df[df['District'] == selected_district]
        hover_data = {"District": True,
                  "Latitude": True,
                  "Longitude": True,
                  "Population": True,
                  "sex_ratio": True,  # Ensure lowercase
                  "Literate_rate": True,
                  "Male_Literate": True,
                  "Female_Literate": True,
                  "Higher_Education": True,
                  "Workers": True,"Primary_Education":True,
                  "Cultivator_Workers": True,
                  "Housholds_with_Electric_Lighting": True,  # Ensure exact match
                  "Households_with_Telephone_Mobile_Phone": True,"Power_Parity_Less_than_Rs_45000":True,
                  "Power_Parity_Above_Rs_545000": True}

        fig = px.scatter_map(
            district_df, lat="Latitude", lon="Longitude", color=primary, size=secondary,
            color_continuous_scale=px.colors.sequential.Turbo, size_max=20, zoom=6,
            hover_name="District", hover_data=hover_data,
            title=f"Population Distribution in {selected_district}"
        )
        fig.update_layout(mapbox_style="dark", margin={"r": 0, "t": 50, "l": 0, "b": 0})
        fig.update_traces(marker=dict(opacity=0.9))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Please select a specific district instead of 'Overall State'.")
# Advanced Data Insights Sidebar Section
st.sidebar.markdown('### Advanced Data Insights')
plot_additional=st.sidebar.button('Plot 10 Advanced Graphs')
if plot_additional:
  st.header("10 Advanced Interesting Graphs")
  # Graph 1: State-wise Income Distribution Heatmap
  power_parity_columns = [
    "Power_Parity_Less_than_Rs_45000",
    "Power_Parity_Rs_45000_90000",
    "Power_Parity_Rs_90000_150000",
    "Power_Parity_Rs_45000_150000",
    "Power_Parity_Rs_150000_240000",
    "Power_Parity_Rs_240000_330000",
    "Power_Parity_Rs_150000_330000",
    "Power_Parity_Rs_330000_425000",
    "Power_Parity_Rs_425000_545000",
    "Power_Parity_Rs_330000_545000",
    "Power_Parity_Above_Rs_545000"]

  ppp_across_district=df.groupby('State')[power_parity_columns].sum().reset_index()
  ppp_across_district=ppp_across_district.melt(id_vars='State',var_name='Income_range',value_name='Count')
  fig1= px.density_heatmap(
    ppp_across_district,
    x="State",
    y="Income_range",
    z="Count",
    color_continuous_scale="Viridis",
    title="State-wise Income Distribution Heatmap")
  st.plotly_chart(fig1, use_container_width=True)
  literacy_df = df.groupby('State')['Literate_rate'].mean().reset_index()
  # Graph 2: Bar Chart of Average Literacy Rate by State
  fig2 = px.bar(literacy_df, x='State', y='Literate_rate', title="Average Literacy Rate by State",
                  color='Literate_rate', color_continuous_scale=px.colors.sequential.Viridis)
  st.plotly_chart(fig2, use_container_width=True)

  # Graph 3: Histogram of Population Distribution
  fig3 = px.histogram(df, x='Population', nbins=50, title="Population Distribution Histogram")
  st.plotly_chart(fig3, use_container_width=True)

  # Graph 4: Box Plot of Population by State
  fig4 = px.box(df, x='State', y='Population', title="Population Distribution by State (Box Plot)")
  st.plotly_chart(fig4, use_container_width=True)

  # Graph 5: Scatter Plot of Male vs Female Literacy with Trendline
  fig5 = px.scatter(df, x='Male_Literate', y='Female_Literate', title="Male vs Female Literacy", trendline="ols",color='State',
    color_continuous_scale="Viridis")
  st.plotly_chart(fig5, use_container_width=True)

  # Graph 6: Pie Chart of Religion Distribution for Overall India
  religion_columns = ["Hindus", "Muslims", "Christians", "Sikhs", "Buddhists", "Jains", "Others_Religions", "Religion_Not_Stated"]
  religion_totals = df[religion_columns].sum().reset_index()
  religion_totals.columns = ["Religion", "Count"]
  fig6 = px.pie(religion_totals, names="Religion", values="Count", title="Religion Distribution in India")
  st.plotly_chart(fig6, use_container_width=True)

  # Graph 7: Bar Chart of Households with Internet by State
  internet_df = df.groupby('State')['Households_with_Internet'].sum().reset_index()
  fig7 = px.bar(internet_df, x='State', y='Households_with_Internet', title="Households with Internet by State",
                color='Households_with_Internet', color_continuous_scale=px.colors.sequential.Plasma)
  st.plotly_chart(fig7, use_container_width=True)

  # Graph 8: Scatter Plot of Workers vs Population with Trendline
  fig8 = px.scatter(df, x='Population', y='Workers', title="Workers vs Population",color_continuous_scale="Viridis" ,trendline="ols")
  st.plotly_chart(fig8, use_container_width=True)

  # Graph 9: Density Heatmap of Male vs Female Literacy
  fig9 = px.density_heatmap(df, x='Male_Literate', y='Female_Literate',
                            title="Density Heatmap: Male vs Female Literacy",color_continuous_scale="Viridis")
  st.plotly_chart(fig9, use_container_width=True)

  # Graph 10: Line Chart of Households with Television by State
  tv_df = df.groupby('State')['Households_with_Television'].sum().reset_index()
  fig10 = px.line(tv_df, x='State', y='Households_with_Television', title="Households with Television by State")
  st.plotly_chart(fig10, use_container_width=True)
