# Import python packages
import streamlit as st
#特定の列を選択するために使用
from snowflake.snowpark.functions import col

# Write directly to the app
st.title("🥤 Customize Your Smoothie! 🥤")
st.write(
    """Choose the frits you want in your custom Smoothie!
    """
)


name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be ", name_on_order)


#Snowflake データベースからデータを取得し、それをウェブアプリケーション上に表示する
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME')) #FRUIT_NAME列だけを選択
#st.dataframe(data=my_dataframe, use_container_width=True)←コメントアウトすることでデータフレームの表示をなくした


#ユーザーが複数の果物（スムージーの材料）を選択できるように、multiselect ウィジェットを追加
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    ,my_dataframe
    , max_selections = 5
    )


#ユーザーが選択したスムージーの材料（果物）を処理し、表示するためのロジック
if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

    #smoothies.public.orders テーブルの ingredients カラムに、選択された果物の名前を挿入する
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order) 
            values ('""" + ingredients_string + """','"""+name_on_order+""""')"""  #ユーザーが選択した果物の名前が SQL 文の値として使用される

    #st.write(my_insert_stmt)
    #st.stop()
    
    time_to_insert = st.button('Submit Order')
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect() #、選択された果物の名前が orders テーブルに挿入される
        
        st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")   

# New section to display smoothiefroot nutrition information
import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
st.text(smoothiefroot_response).json()
