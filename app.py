import streamlit as st

st.set_page_config(
    page_title="房產試算工具",
    page_icon="🏠",
    layout="wide"
)

st.title("🏠 房產試算工具")
st.caption("房仲專業試算工具｜僅供參考，實際金額以銀行/政府核定為準")

tabs = st.tabs([
    "房貸試算",
    "購屋能力",
    "坪數換算",
    "車位拆算",
    "賣方實拿"
])

with tabs[0]:
    st.header("房貸試算")

    loan = st.number_input("貸款金額（萬）", min_value=0.0, value=1000.0)
    rate = st.number_input("年利率（%）", min_value=0.0, value=2.5)
    years = st.number_input("貸款年限", min_value=1, value=30)

    monthly_rate = rate / 100 / 12
    months = years * 12

    if monthly_rate > 0:
        monthly_payment = loan * 10000 * monthly_rate * (1 + monthly_rate) ** months / ((1 + monthly_rate) ** months - 1)
    else:
        monthly_payment = loan * 10000 / months

    st.metric("每月應繳", f"${monthly_payment:,.0f}")
    st.metric("總還款金額", f"${monthly_payment * months:,.0f}")

with tabs[1]:
    st.header("購屋能力")

    income = st.number_input("月收入（萬）", min_value=0.0, value=10.0)
    down_payment = st.number_input("自備款（萬）", min_value=0.0, value=300.0)
    ratio = st.slider("負債比上限", 0.2, 0.7, 0.4)
    years2 = st.selectbox("貸款年限", [20, 30, 40])
    rate2 = st.number_input("試算利率（%）", value=2.5)

    affordable_monthly = income * 10000 * ratio
    r = rate2 / 100 / 12
    n = years2 * 12

    loan_amount = affordable_monthly * ((1 + r) ** n - 1) / (r * (1 + r) ** n) if r > 0 else affordable_monthly * n
    total_price = loan_amount / 10000 + down_payment

    st.metric("建議房屋總價上限", f"{total_price:,.0f} 萬")
    st.metric("建議貸款金額", f"{loan_amount / 10000:,.0f} 萬")

with tabs[2]:
    st.header("坪數換算")

    ping = st.number_input("坪數", min_value=0.0, value=30.0)
    sqm = ping * 3.30579

    st.metric("平方公尺", f"{sqm:,.2f} m²")

with tabs[3]:
    st.header("車位拆算")

    total_price = st.number_input("總價含車位（萬）", value=2000.0)
    total_ping = st.number_input("權狀坪數含車位", value=40.0)
    parking_price = st.number_input("車位價格（萬）", value=200.0)
    parking_ping = st.number_input("車位坪數", value=10.0)

    house_price = total_price - parking_price
    house_ping = total_ping - parking_ping
    unit_price = house_price / house_ping if house_ping > 0 else 0

    st.metric("扣車位後單價", f"{unit_price:,.2f} 萬/坪")
    st.metric("房屋價格", f"{house_price:,.0f} 萬")
    st.metric("房屋坪數", f"{house_ping:,.2f} 坪")

with tabs[4]:
    st.header("賣方實拿速算")

    sell_price = st.number_input("成交總價（萬）", value=2000.0)
    service_rate = st.number_input("服務費率（%）", value=4.0)
    land_tax = st.number_input("土增稅（萬）", value=0.0)
    loan_balance = st.number_input("剩餘貸款（萬）", value=800.0)
    other_fee = st.number_input("其他費用（萬）", value=1.0)

    service_fee = sell_price * service_rate / 100
    net = sell_price - service_fee - land_tax - loan_balance - other_fee

    st.metric("服務費", f"{service_fee:,.2f} 萬")
    st.metric("屋主實拿", f"{net:,.2f} 萬")
