import streamlit as st
import plotly.express as px
from pandas import read_csv
import numpy as np

skip = [48, 89, 95, 108, 111, 126, 146, 149, 153, 156, 160, 163, 172, 175, 187, 
    220, 230, 251, 255, 258, 263, 267, 269, 270, 289, 291, 299, 318, 323, 328, 
    331, 335
] # rows where 1 subject participated multiple times according to the 
# authors' words

data = read_csv('participants_info.csv', 
    usecols = ['age_years', 'sex', 'diagnosis1', 'diagnosis2', 'diagnosis3'],
    skiprows = skip
)

data_diseases = data[['diagnosis1', 'diagnosis2', 'diagnosis3']].copy()
data_diseases.fillna(0, inplace = True)
x = np.array(data_diseases)
x[x == 'Normal'] = 0
x[x != 0] = 1
y = np.sum(x, axis = 1)

data['diseases'] = y
data = data[['age_years', 'sex', 'diseases']]

st.title("Visual Diseases")
st.write("""The dataset comprises information collected from 304 subjects 
    enrolled at IOBA, a University of Valladolid-affiliated institution in 
    Spain. The data collection spanned an extensive period, starting from 2003 
    and continuing until 2022. During this extended timeframe, 23 individuals 
    had multiple visits: 19 individuals had two visits each, 1 individual had 
    three, another had four visits and two subjects had five visits each. As a 
    part of the routine clinical evaluation, all subjects underwent diagnosis 
    by ophthalmology specialists. In this particular research multiple visits 
    are not counted."""
)

st.area_chart(data, x = "age_years", y = "diseases",
    x_label = "age of participants", y_label = "# of diseases",
    color = "sex"
)

st.bar_chart(data, x = "age_years", y = "diseases",
    x_label = "age of participants", y_label = "# of diseases",
    color = "diseases"
)

genders = st.radio("Choose a gender for the graph", ["Female", "Male"])


def chart2gender(g : str) -> object:
    return (
        px.box(
            data[data["sex"] == g],
            x = "diseases",
            y = "age_years",
            color = "diseases",
            title = f"Age distribution for diseases among {g}"
        )
    )


if genders == "Female":
    fig = chart2gender("Female")
    st.plotly_chart(fig)
else:
    fig = chart2gender("Male")
    st.plotly_chart(fig)

dfChart3 = data
dfChart3["sex"].replace({"Male" : 0, "Female" : 1}, inplace = True)
fig2 = px.imshow(
    dfChart3.corr(),
    title="Correlation matrix"
)
st.plotly_chart(fig2)
