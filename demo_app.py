import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
from IPython.display import HTML


with st.echo(code_location='below'):
    url = 'https://mkb-10.com/index.php?pid=4001'
    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    heading = soup.find_all("h1")
    cod = soup.find_all("div", {"class": "code"})
    cat = soup.find_all("a", {"style": "font-weight:bold;"})
    codes = []
    for item in cod:
        codes.append(item.text)
    linkss = []
    for item in cat:
        linkss.append(f'<a href="{"https://mkb-10.com" + item.get("href")}">{item.text}</a>')
    d = {'Коды': codes, 'Категория': linkss}
    classification_categories = pd.DataFrame(data=d)
    classification_categories.index = classification_categories["Коды"]
    classification_categories = classification_categories.drop("Коды", axis=1)
    classification_categories_html=HTML(classification_categories.to_html(escape=False))
    print(classification_categories)

    classification = pd.DataFrame()
    for elem in cat:
        new = requests.get("https://mkb-10.com" + elem.get("href"))
        soup2 = BeautifulSoup(new.text)
        cat2 = soup2.find_all("div", {"class": "h2"})
        linkss2 = []
        codes2 = []
        for el in cat2:
            divide = el.text.index(" ")
            co = el.text[0: divide]
            cl = el.text[divide + 1:]
            try:
                link = el.find("a", {"style": "font-weight:bold;"}).get('href')
                codes2.append(co)
                linkss2.append(f'<a href="{"https://mkb-10.com" + link}">{cl}</a>')
            except AttributeError:
                codes2.append(co)
                linkss2.append(cl)
        d2 = {'Код': codes2, 'Расстройство': linkss2}
        classification_category = pd.DataFrame(data=d2)
        classification_category
        classification = pd.concat([classification, classification_category])
    classification.index = classification["Код"]
    classification = classification.drop("Код", axis=1)
    classification_html = HTML(classification.to_html(escape=False))
    print(classification_html)


    def pure_code(full_code):
        return (int(full_code.replace("F", "").replace("*", "")))


    def drop_extra_columns(df):
        df = df.drop(['Код'], axis=1)
        df = df.rename(columns={'Полный код': 'Код'})
        df.index = df["Код"]
        return (df.drop(['Код'], axis=1))


    temp = pd.DataFrame(columns=["Код", "Категория"])
    for index, element in classification_categories.reset_index().iterrows():
        group_of_codes = element["Коды"].replace("F", "").replace("*", "")
        divide_gr = group_of_codes.index("-")
        start_gr = group_of_codes[0: divide_gr]
        end_gr = group_of_codes[divide_gr + 1:]
        for i in range(int(end_gr) - int(start_gr) + 1):
            temp = temp.append({"Код": int(start_gr) + i, "Категория": element["Категория"]}, ignore_index=True)
    classification_temp = classification.reset_index().rename(columns={'Код': 'Полный код'})
    classification_temp["Код"] = classification_temp["Полный код"].apply(pure_code)
    full_classification = classification_temp.reset_index().merge(temp, how="left", on='Код')
    full_classification_for_search = full_classification.drop(["index"], axis=1)
    full_classification = drop_extra_columns(full_classification_for_search)
    full_classification_html = HTML(full_classification.to_html(escape=False))
    st.dataframe(data=full_classification)

    # here you can find information about diseases based on their' codes. You can print full codes (F02*) or only numbers.
    # Divide codes using space. If you want a series of codes you can print them via "-" (15-F18).
    find_code_raw = list(input().split(" "))
    find_code = []
    no_diseases = ""
    count_no = 0
    for element in find_code_raw:
        if "-" in element:
            find_code_raw.remove(element)
            divide_el = element.index("-")
            start_el = element[0: divide_el]
            end_el = element[divide_el + 1:]
            for i in range(int(end_el) - int(start_el) + 1):
                find_code_raw.append(str(int(start_el) + i))
    for element in find_code_raw:
        one_code = int(element.replace("F", "").replace("*", ""))
        if one_code in full_classification_for_search["Код"]:
            find_code.append(one_code)
        else:
            no_diseases = no_diseases + element + ", "
            count_no = count_no + 1
    if not len(find_code) == 0:
        find_classification = full_classification_for_search[
            full_classification_for_search['Код'].astype("int").isin(find_code)]
        find_classification = drop_extra_columns(find_classification)
        find_classification_html = HTML(find_classification.to_html(escape=False))
        print(find_classification)
        print(find_classification_html)
    if not no_diseases == "" and count_no > 1:
        print("Расстройств с кодами", no_diseases[:-2], "не существует.")
    if not no_diseases == "" and count_no == 1:
        print("Расстройства с кодом", no_diseases[:-2], "не существует.")







    df = pd.read_csv('gdp_csv.csv')
    function_country = []
    function_yearmin = []
    function_yearmax = []
    choose_type = []
    function_plus_field = []
    function_show_df = []
    i = 0
    function_plus_field_to_func = {
        'Yes :)': 'yes',
        'No, I am tired': 'no'
    }
    choose_type_to_func = {
        'Annual GDP': 'GDP',
        'Annual GDP2': 'GDP2'
    }
    function_show_df_to_func = {
        'Yes!': 'yes',
        'O.o No...': 'no'
    }

    def plotGDP(fr):
        fig, ax = plt.subplots()
        for country in fr['Country Name'].unique():
            countryfr = fr.loc[fr['Country Name'] == country]
            countryfr.plot(y='Value', x='Year', ax=ax, xlabel='Year', ylabel='GDP', label=country)
        st.pyplot(fig)

    def any_graph(i):
        st.sidebar.write(f'Graph №{i+1}')
        st.write(f'Graph №{i+1}')
        st.write('There you can choose, what data to visualize and how to do it.'
                 ' Remember that there will not be correct visualization if you choose non-existing combination of parameters.')
        function_country.append(' ')
        function_yearmin.append(' ')
        function_yearmax.append(' ')
        function_country[i]=st.sidebar.multiselect('Choose regions', df['Country Name'].unique(), key=f"chooseregion_{i}")
        function_yearmin[i]=st.sidebar.slider('What year you want to start from?', 1960, 2016, 1960, 1, key=f"choosemin_{i}")
        function_yearmax[i]=st.sidebar.slider('What year you want to end with?', function_yearmin[i], 2016, 2016, 1, key=f"choosemax_{i}")
        year = list(range(function_yearmin[i], function_yearmax[i] + 1))
        ndf0 = df.loc[df['Country Name'].isin(function_country[i])]
        ndf0['Year'] = pd.to_numeric(ndf0['Year'])
        ndf1 = ndf0.loc[ndf0['Year'].isin(year)]
        ndf = ndf1.dropna()
        function_show_df.append(' ')
        function_show_df[i + 1]=st.selectbox('Do you want to show the dataframe?', ('Yes!', 'O.o No...'), key=f"chooseshow_{i+1}")
        if function_show_df_to_func[function_show_df[i + 1]] == 'yes':
            st.write(ndf)
        choose_type.append(' ')
        choose_type[i]=st.sidebar.selectbox('What type of graph do you want?', ('Annual GDP', 'Annual GDP2'), key=f"choosetype_{i}")
        if choose_type_to_func[choose_type[i]] == 'GDP':
            plotGDP(ndf)
        if choose_type_to_func[choose_type[i]] == 'GDP2':
            plotGDP(ndf)
        i = i + 1
        function_plus_field.append(' ')
        function_plus_field[i-1]=st.selectbox('Do you want one more graph?', ('Yes :)', 'No, I am tired'), index=1, key=f"choosefield_{i-1}")
        if function_plus_field_to_func[function_plus_field[i-1]] == 'no':
            st.write("Thank you for using me! (c) The app")
        if function_plus_field_to_func[function_plus_field[i-1]] == 'yes':
            any_graph(i)

    st.title("Welcome to GDP visualizer!!")
    st.write("In this app you can visualize data on country, regional and world GDP from 1960 to 2016 year."
             " The data is taken from Kaggle, where it is sourced from the World Bank."
             " You can find the source on Kaggle here: https://www.kaggle.com/tunguz/country-regional-and-world-gdp")
    function_show_df.append(' ')
    function_show_df[0] = st.selectbox('Do you want to show the original dataframe?', ('Yes!', 'O.o No...'), key=f"chooseshow_{0}")
    if function_show_df_to_func[function_show_df[0]]=='yes':
        st.write(df)
    any_graph(i)