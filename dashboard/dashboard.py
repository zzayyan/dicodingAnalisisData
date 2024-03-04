import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

def create_most_categoryProduct_ordered(df):
    most_order_categoryProduct_df = all_df.groupby(by="product_category_name").order_id.nunique().sort_values(ascending=False).head(5)
    return most_order_categoryProduct_df

def create_least_categoryProduct_ordered(df):
    least_order_categoryProduct_df = all_df.groupby(by="product_category_name").order_id.nunique().sort_values(ascending=True).head(5)
    return least_order_categoryProduct_df

def averageReviewScore(df):
    all_df['review_score'] = pd.to_numeric(all_df['review_score'], errors='coerce')
    average_review_score = all_df.groupby(by='product_category_name').agg({
    'review_score': ["max", "min", "mean", "std"]
})
    
    return average_review_score


def create_highAverage_review_score(df, average_review_score):
    highAverage_review_score_df = average_review_score.sort_values(by=('review_score', 'mean'), ascending=False)
    return highAverage_review_score_df

def create_lowAverage_review_score(df, average_review_score):
    lowAverage_review_score_df = average_review_score.sort_values(by=('review_score', 'mean'), ascending=True)
    return lowAverage_review_score_df

all_df =pd.read_csv("main_data.csv")
all_df.head()

most_order_categoryProduct_df = create_most_categoryProduct_ordered(all_df)
least_order_categoryProduct_df = create_least_categoryProduct_ordered(all_df)
average_review_score = averageReviewScore(all_df)
highAverage_review_score_df = create_highAverage_review_score(all_df, average_review_score)
lowAverage_review_score_df = create_lowAverage_review_score(all_df, average_review_score)

st.title('E-Commerce Public Dataset :sparkles:')
st.header('Explanatory Data Analysis')

# Ubah 'order_purchase_timestamp' menjadi tipe data datetime jika belum
all_df['order_purchase_timestamp'] = pd.to_datetime(all_df['order_purchase_timestamp'])

# Dapatkan tanggal minimum dan maksimum
min_date = all_df["order_purchase_timestamp"].min().date()
max_date = all_df["order_purchase_timestamp"].max().date()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Filter DataFrame berdasarkan rentang waktu yang dipilih
filtered_df = all_df[(all_df["order_purchase_timestamp"].dt.date >= start_date) & 
                     (all_df["order_purchase_timestamp"].dt.date <= end_date)]

# Hitung jumlah pembelian
num_purchases = filtered_df['order_id'].nunique()

# Tampilkan jumlah pembelian
st.metric("Purchase amount : ", value=num_purchases)




col1, col2= st.columns(2)
 
with col1:
    #1 
    st.subheader("Top 5 Most Ordered Product Categories")
    colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
    # Mengelompokkan data dan mengambil 5 kategori teratas
    top_5_ordered_categories = all_df.groupby(by="product_category_name").order_id.nunique().sort_values(ascending=False).head(5)

    # Membuat bar chart
    fig = plt.figure(figsize=(10, 5))  # Menentukan ukuran figure
    plt.bar(top_5_ordered_categories.index, top_5_ordered_categories.values, color=colors)  # Membuat bar chart vertikal
    plt.ylabel('Number of Orders')  # Menambahkan label pada sumbu y
    plt.xlabel('Product Category')  # Menambahkan label pada sumbu x
    plt.title('Top 5 Most Ordered Product Categories')  # Menambahkan judul
    plt.xticks(rotation=45)  # Memutar label sumbu x agar mudah dibaca
    plt.show()  # Menampilkan plot
    st.pyplot(fig)
 
with col2:
#2
    st.subheader("5 Least Ordered Product Categories")
    colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
    # Mengelompokkan data dan mengambil 5 kategori terbawah
    least_5_ordered_categories = all_df.groupby(by="product_category_name").order_id.nunique().sort_values(ascending=True).head(5)

    # Membuat bar chart
    fig = plt.figure(figsize=(10, 5))  # Menentukan ukuran figure
    plt.bar(least_5_ordered_categories.index, least_5_ordered_categories.values, color=colors)  # Membuat bar chart vertikal
    plt.ylabel('Number of Orders')  # Menambahkan label pada sumbu y
    plt.xlabel('Product Category')  # Menambahkan label pada sumbu x
    plt.title('5 Least Ordered Product Categories')  # Menambahkan judul
    plt.xticks(rotation=45)  # Memutar label sumbu x agar mudah dibaca
    plt.show()  # Menampilkan plot
    st.pyplot(fig)


#3
#Chart kategori produk yang memiliki nilai rata-rata tertinggi dan terendah
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 6)) # Membuat figure dengan 2 subplots
colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

# Mengurutkan dan memilih 5 kategori produk dengan rata-rata review tertinggi
top_5_categories = highAverage_review_score_df.sort_values(by=('review_score', 'mean'), ascending=False).head(5)

# Membuat bar chart
bars = ax[0].barh(top_5_categories.index, top_5_categories[('review_score', 'mean')], color=colors)  # data untuk bar chart
bars[0].set_color('#72BCD4')  # highlight bar dengan nilai tertinggi
ax[0].set_xlabel('Average Review Score')  # label sumbu x
ax[0].set_ylabel('Product Category')  # label sumbu y
ax[0].set_title('Top 5 Product Categories by High Average Review Score')  # judul
ax[0].invert_yaxis()

# Chart 2: Kategori produk dengan rata-rata review terendah
st.subheader("Best & Worst Review Category Product")
bottom_5_categories = lowAverage_review_score_df.sort_values(by=('review_score', 'mean'), ascending=True).head(5)

bars = ax[1].barh(bottom_5_categories.index, bottom_5_categories[('review_score', 'mean')], color=colors)  # data untuk bar chart
bars[0].set_color('#72BCD4')  # highlight bar dengan nilai terendah
ax[1].invert_xaxis()
ax[1].invert_yaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_xlabel('Average Review Score')  # label sumbu x
ax[1].set_ylabel('Product Category')  # label sumbu y
ax[1].set_title('Top 5 Product Categories by Lowest Average Review Score')  # judul
plt.tight_layout()  # Menyesuaikan jarak antara subplots
plt.show()
st.pyplot(fig)

st.caption('Copyright (c) Brillianta Zayyan M ML-38 2024')