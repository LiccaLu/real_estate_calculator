import streamlit as st
from datetime import date

st.set_page_config(
    page_title="中壢專業房仲Jhen 房產計算機",
    page_icon="🏠",
    layout="wide"
)

# ========= CSS 美化 =========
st.markdown("""
<style>
.stApp {
    background: #f5f6f8;
}

.main-card {
    background: white;
    padding: 26px 32px;
    border-radius: 18px;
    box-shadow: 0 4px 18px rgba(0,0,0,0.06);
    margin-bottom: 22px;
}

.title-box {
    background: white;
    padding: 26px 34px;
    border-radius: 18px;
    box-shadow: 0 4px 18px rgba(0,0,0,0.06);
    display: flex;
    align-items: center;
    gap: 18px;
    margin-bottom: 22px;
}

.logo {
    font-size: 48px;
}

.title-text {
    font-size: 30px;
    font-weight: 800;
    color: #111827;
}

.sub-text {
    color: #6b7280;
    font-size: 14px;
}

.section-title {
    font-size: 22px;
    font-weight: 800;
    color: #111827;
    border-left: 6px solid #c9a24a;
    padding-left: 12px;
    margin-bottom: 4px;
}

.info-box {
    background: #fff8cc;
    border: 1px solid #e6cd69;
    padding: 20px;
    border-radius: 14px;
    margin-bottom: 18px;
}

.normal-box {
    background: white;
    border: 1px solid #e5e7eb;
    padding: 20px;
    border-radius: 14px;
    margin-bottom: 18px;
}

.result-box {
    background: #caa548;
    color: white;
    padding: 24px;
    border-radius: 14px;
    margin-top: 16px;
}

.result-big {
    font-size: 36px;
    font-weight: 900;
}

.small-note {
    font-size: 13px;
    color: #6b7280;
}

hr {
    border: none;
    border-top: 1px dashed #ddd;
    margin: 18px 0;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 12px;
}

.stTabs [data-baseweb="tab"] {
    background: white;
    border-radius: 10px;
    padding: 10px 18px;
    font-weight: 700;
}

.stTabs [aria-selected="true"] {
    background: #caa548 !important;
    color: white !important;
}
</style>
""", unsafe_allow_html=True)


# ========= 小工具 =========
def money(v):
    return f"{v:,.2f} 萬"

def nt(v):
    return f"${v:,.0f}"

def loan_monthly_payment(loan_wan, annual_rate, years):
    principal = loan_wan * 10000
    r = annual_rate / 100 / 12
    n = int(years * 12)

    if principal <= 0 or n <= 0:
        return 0

    if r == 0:
        return principal / n

    return principal * r * (1 + r) ** n / ((1 + r) ** n - 1)

def loan_possible_by_monthly(monthly, annual_rate, years):
    r = annual_rate / 100 / 12
    n = int(years * 12)

    if r == 0:
        return monthly * n / 10000

    loan = monthly * ((1 + r) ** n - 1) / (r * (1 + r) ** n)
    return loan / 10000


# ========= Header =========
st.markdown("""
<div class="title-box">
    <div class="logo">🏆🏠</div>
    <div>
        <div class="title-text">中壢專業房仲Jhen 房產計算機</div>
        <div class="sub-text">房貸、購屋能力、坪數、車位拆算、賣方實拿速算</div>
    </div>
</div>
""", unsafe_allow_html=True)


tabs = st.tabs([
    "🏦 房貸試算",
    "💼 購屋能力",
    "📐 坪數換算",
    "🚗 車位拆算",
    "💰 賣方實拿",
    "✨ 新青安2.0"
])


# ========= 房貸試算 =========
with tabs[0]:
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">房貸試算</div>', unsafe_allow_html=True)
    st.caption("輸入貸款金額、利率、年限，快速計算每月本息攤還")

    col1, col2, col3 = st.columns(3)
    with col1:
        loan = st.number_input("貸款金額（萬）", min_value=0.0, value=1000.0, step=10.0)
    with col2:
        rate = st.number_input("年利率（%）", min_value=0.0, value=2.5, step=0.01)
    with col3:
        years = st.selectbox("貸款年限", [20, 25, 30, 35, 40], index=2)

    monthly = loan_monthly_payment(loan, rate, years)
    total_pay = monthly * years * 12
    total_interest = total_pay - loan * 10000

    c1, c2, c3 = st.columns(3)
    c1.metric("每月應繳", nt(monthly))
    c2.metric("總還款金額", nt(total_pay))
    c3.metric("總利息", nt(total_interest))

    st.markdown('<div class="info-box">', unsafe_allow_html=True)
    st.write(f"貸款 {money(loan)}，利率 {rate:.2f}%，{years} 年期，每月約繳 **{nt(monthly)}**。")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ========= 購屋能力 =========
with tabs[1]:
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">購屋能力試算</div>', unsafe_allow_html=True)
    st.caption("用月收入、自備款、負債比，估算可負擔總價")

    col1, col2, col3 = st.columns(3)
    with col1:
        income = st.number_input("家庭月收入（萬）", min_value=0.0, value=10.0, step=0.5)
    with col2:
        down_payment = st.number_input("自備款（萬）", min_value=0.0, value=300.0, step=10.0)
    with col3:
        debt_ratio = st.slider("可接受房貸負擔比", 20, 60, 40) / 100

    col4, col5 = st.columns(2)
    with col4:
        ability_rate = st.number_input("試算利率（%）", min_value=0.0, value=2.5, step=0.01, key="ability_rate")
    with col5:
        ability_years = st.selectbox("貸款年限", [20, 25, 30, 35, 40], index=2, key="ability_years")

    max_monthly = income * 10000 * debt_ratio
    max_loan = loan_possible_by_monthly(max_monthly, ability_rate, ability_years)
    max_total_price = max_loan + down_payment

    c1, c2, c3 = st.columns(3)
    c1.metric("建議月付上限", nt(max_monthly))
    c2.metric("可貸款金額", money(max_loan))
    c3.metric("建議總價上限", money(max_total_price))

    st.markdown('<div class="info-box">', unsafe_allow_html=True)
    st.write(f"以月收入 {income:.1f} 萬、負擔比 {debt_ratio*100:.0f}% 估算，建議每月房貸不要超過 **{nt(max_monthly)}**。")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ========= 坪數換算 =========
with tabs[2]:
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">坪數換算</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        ping = st.number_input("坪數", min_value=0.0, value=30.0, step=0.1)
    with col2:
        sqm_input = st.number_input("平方公尺", min_value=0.0, value=99.17, step=0.1)

    sqm = ping * 3.30579
    ping_from_sqm = sqm_input / 3.30579

    c1, c2 = st.columns(2)
    c1.metric("坪 → 平方公尺", f"{sqm:,.2f} m²")
    c2.metric("平方公尺 → 坪", f"{ping_from_sqm:,.2f} 坪")

    st.markdown('</div>', unsafe_allow_html=True)


# ========= 車位拆算 =========
with tabs[3]:
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">車位拆算</div>', unsafe_allow_html=True)
    st.caption("總價含車位時，拆出房屋單價")

    col1, col2 = st.columns(2)
    with col1:
        total_price = st.number_input("總價含車位（萬）", value=2000.0, step=10.0)
        parking_price = st.number_input("車位價格（萬）", value=200.0, step=10.0)
    with col2:
        total_ping = st.number_input("權狀坪數含車位", value=40.0, step=0.1)
        parking_ping = st.number_input("車位坪數", value=10.0, step=0.1)

    house_price = total_price - parking_price
    house_ping = total_ping - parking_ping
    unit_price = house_price / house_ping if house_ping > 0 else 0

    c1, c2, c3 = st.columns(3)
    c1.metric("房屋價格", money(house_price))
    c2.metric("房屋坪數", f"{house_ping:,.2f} 坪")
    c3.metric("扣車位後單價", f"{unit_price:,.2f} 萬/坪")

    st.markdown('</div>', unsafe_allow_html=True)


# ========= 賣方實拿 =========
with tabs[4]:
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">賣方實拿速算</div>', unsafe_allow_html=True)
    st.caption("輸入欄位後即時計算，所有數字連動更新")

    st.markdown('<div class="info-box">', unsafe_allow_html=True)
    st.subheader("基礎資訊")

    col1, col2, col3 = st.columns(3)
    with col1:
        total_ping = st.number_input("總坪數（含車位）", value=50.23, step=0.01)
    with col2:
        parking_area = st.number_input("車位坪數", value=10.00, step=0.01)
    with col3:
        parking_price2 = st.number_input("車位價格（萬）", value=180.0, step=10.0)

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="normal-box">', unsafe_allow_html=True)
    st.subheader("取得資訊")
    col1, col2 = st.columns(2)
    with col1:
        buy_price = st.number_input("房屋取得價格（萬）", value=1052.0, step=10.0)
    with col2:
        buy_cost = st.number_input("取得相關成本（萬）", value=13.0, step=1.0)

    col3, col4 = st.columns(2)
    with col3:
        old_date = st.date_input("前次移轉日期", value=date(2020, 1, 1))
    with col4:
        sell_date = st.date_input("本次預計交易日期", value=date.today())

    self_use = st.toggle("自用住宅滿 6 年優惠")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="normal-box">', unsafe_allow_html=True)
    st.subheader("手動輸入項目")
    col1, col2 = st.columns(2)
    with col1:
        land_tax = st.number_input("土地增值稅（萬）", value=1.6, step=0.1)
    with col2:
        loan_balance = st.number_input("剩餘貸款餘額（萬）", value=840.0, step=10.0)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="normal-box">', unsafe_allow_html=True)
    st.subheader("服務費計算方式")
    service_mode = st.radio(
        "服務費",
        ["預設 4%", "手動輸入"],
        horizontal=True
    )

    if service_mode == "預設 4%":
        service_rate = 4.0
        manual_service = 0
    else:
        service_rate = st.number_input("服務費率（%）", value=4.0, step=0.1)
        manual_service = st.number_input("或直接輸入服務費（萬，若填寫則優先採用）", value=0.0, step=1.0)

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="normal-box">', unsafe_allow_html=True)
    st.subheader("房地合一可認列移轉費用")
    transfer_mode = st.radio(
        "移轉費用",
        ["同服務費", "手動輸入", "3% 上限 30萬"],
        horizontal=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="normal-box">', unsafe_allow_html=True)
    st.subheader("想賣的價格")
    col1, col2 = st.columns(2)
    with col1:
        sell_price = st.number_input("想賣的總價（萬）", value=1585.0, step=10.0)
    with col2:
        house_unit_price_input = st.number_input("房屋單價（萬/坪，可留 0）", value=0.0, step=0.1)

    house_area = total_ping - parking_area
    house_price2 = sell_price - parking_price2
    unit_price2 = house_price2 / house_area if house_area > 0 else 0

    if house_unit_price_input > 0:
        house_price2 = house_unit_price_input * house_area
        sell_price = house_price2 + parking_price2
        unit_price2 = house_unit_price_input

    service_fee = manual_service if service_mode == "手動輸入" and manual_service > 0 else sell_price * service_rate / 100

    if transfer_mode == "同服務費":
        transfer_fee = service_fee
    elif transfer_mode == "手動輸入":
        transfer_fee = st.number_input("可認列移轉費用（萬）", value=service_fee, step=1.0)
    else:
        transfer_fee = min(sell_price * 0.03, 30)

    agent_fee = 0.10
    registration_fee = 0.20

    taxable_gain = sell_price - buy_price - buy_cost - transfer_fee
    taxable_gain = max(taxable_gain, 0)

    if self_use:
        house_land_tax = max((taxable_gain - 400) * 0.10, 0)
    else:
        years_hold = (sell_date - old_date).days / 365
        if years_hold <= 2:
            tax_rate = 0.45
        elif years_hold <= 5:
            tax_rate = 0.35
        elif years_hold <= 10:
            tax_rate = 0.20
        else:
            tax_rate = 0.15
        house_land_tax = taxable_gain * tax_rate

    other_fee = agent_fee + registration_fee
    net = sell_price - service_fee - land_tax - loan_balance - house_land_tax - other_fee

    c1, c2 = st.columns(2)
    c1.metric("房屋單價（扣車位）", f"{unit_price2:,.2f} 萬/坪")
    c2.metric("房地合一稅", money(house_land_tax))

    st.markdown('<div class="result-box">', unsafe_allow_html=True)
    st.write("屋主實拿")
    st.markdown(f'<div class="result-big">{money(net)}</div>', unsafe_allow_html=True)
    st.caption("計算式：成交總價 - 服務費 - 土增稅 - 剩餘貸款 - 房地合一稅 - 其他費用")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("### 費用明細")
    st.write(f"代書費：**{money(agent_fee)}**")
    st.write(f"實價登錄費：**{money(registration_fee)}**")
    st.write(f"服務費：**{money(service_fee)}**")
    st.write(f"土地增值稅：**{money(land_tax)}**")
    st.write(f"剩餘貸款：**{money(loan_balance)}**")
    st.write(f"房地合一稅：**{money(house_land_tax)}**")
    st.write(f"可認列移轉費用：**{money(transfer_fee)}**")

    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ========= 新青安2.0 =========
with tabs[5]:

    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-title">新青安2.0 利率換算</div>',
        unsafe_allow_html=True
    )

    st.caption("依新青安2.0補貼碼數，自動換算每年優惠利率與每月月付。")

    col1, col2 = st.columns(2)

    with col1:
        loan = st.number_input(
            "貸款金額（萬）",
            min_value=0.0,
            value=1000.0,
            step=10.0,
            key="newloan"
        )

    with col2:
        years = st.selectbox(
            "貸款年限",
            [20,30,40],
            index=2,
            key="newyears"
        )

    rate_table = [
        ("第1年","2碼",1.775),
        ("第2年","2碼",1.775),
        ("第3年","2碼",1.775),
        ("第4年","1.5碼",1.900),
        ("第5年","1碼",2.025),
        ("第6年","0.5碼",2.150),
        ("第7年起","0碼",2.275),
    ]

    st.markdown("---")

    for year, code, rate in rate_table:

        monthly = loan_monthly_payment(
            loan,
            rate,
            years
        )

        st.markdown(f"""
        <div style="
            background:white;
            border-radius:14px;
            padding:18px;
            margin-bottom:12px;
            box-shadow:0 2px 8px rgba(0,0,0,.08);
            border-left:6px solid #caa548;
        ">
        <h4 style="margin:0;">{year}</h4>

        <div style="margin-top:10px;font-size:18px;">
        🏷️ <b>補貼：</b>{code}<br>
        📈 <b>優惠利率：</b>{rate:.3f}%<br>
        💰 <b>每月月付：</b>{monthly:,.0f} 元
        </div>
        </div>
        """, unsafe_allow_html=True)

    st.info("""
📌 新青安2.0補貼碼數

第1~3年：2碼（約1.775%）

第4年：1.5碼（約1.900%）

第5年：1碼（約2.025%）

第6年：0.5碼（約2.150%）

第7年起：恢復原利率（約2.275%）
""")

    st.markdown("</div>", unsafe_allow_html=True)
