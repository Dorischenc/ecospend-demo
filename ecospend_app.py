import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 模擬的碳排係數資料表
carbon_factors = {
    '飲食': 0.02,
    '交通': 0.05,
    '購物': 0.03,
    '娛樂': 0.015
}

# 頁面標題
st.title("🌱 EcoSpend：個人碳足跡理財助理")
st.markdown("請輸入你本週的日常消費，我們將估算碳排放並進行可視化分析。")

# 建立空的資料記錄
if 'expenses' not in st.session_state:
    st.session_state.expenses = []

# 表單輸入區
with st.form("input_form"):
    date = st.date_input("消費日期")
    category = st.selectbox("消費類別", list(carbon_factors.keys()))
    amount = st.number_input("消費金額（NT$）", min_value=1)
    submitted = st.form_submit_button("新增記錄")
    if submitted:
        st.session_state.expenses.append({
            'date': str(date),
            'category': category,
            'amount': amount
        })

# 資料表與圖表呈現
if st.session_state.expenses:
    df = pd.DataFrame(st.session_state.expenses)
    df['carbon_kg'] = df.apply(lambda x: x['amount'] * carbon_factors.get(x['category'], 0), axis=1)

    st.subheader("📋 消費與碳足跡記錄")
    st.dataframe(df)

    # 每日碳排圖
    st.subheader("📈 每日碳排放趨勢")
    daily_carbon = df.groupby('date')['carbon_kg'].sum().reset_index()
    fig1, ax1 = plt.subplots()
    ax1.plot(daily_carbon['date'], daily_carbon['carbon_kg'], marker='o')
    ax1.set_title('每日碳足跡排放 (kg CO₂)')
    ax1.set_xlabel('日期')
    ax1.set_ylabel('碳排放 (kg CO₂)')
    ax1.grid(True)
    st.pyplot(fig1)

    # 類別碳排圓餅圖
    st.subheader("📊 類別碳足跡佔比")
    category_carbon = df.groupby('category')['carbon_kg'].sum().reset_index()
    fig2, ax2 = plt.subplots()
    ax2.pie(category_carbon['carbon_kg'], labels=category_carbon['category'], autopct='%1.1f%%', startangle=140)
    ax2.set_title('一週碳足跡類別佔比')
    st.pyplot(fig2)

    # 總碳排提示
    total = df['carbon_kg'].sum()
    st.success(f"🌍 你本週總碳足跡為：**{total:.2f} kg CO₂**")
else:
    st.info("尚未輸入任何消費紀錄。")
