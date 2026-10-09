import urllib.parse
import streamlit as st

# ตั้งค่าหน้าตาเว็บ
st.set_page_config(
    page_title="Hangout Planner", page_icon="🍻", layout="centered"
)

# Custom CSS จัดสไตล์ข้อความและการ์ดตั๋ว
st.markdown(
    """
    <style>
    .main-header {
        text-align: center;
        font-size: 2.2rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .center-text {
        text-align: center;
    }
    .section-title-center {
        text-align: center;
        font-size: 1.8rem;
        font-weight: 800;
        margin-top: 15px;
        margin-bottom: 8px;
    }
    .section-title-left {
        text-align: left;
        font-size: 1.8rem;
        font-weight: 800;
        margin-top: 15px;
        margin-bottom: 8px;
    }
    
    /* สไตล์การ์ดตั๋วตอบรับ (Ticket Pass) */
    .ticket-card {
        padding: 24px;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 10px 25px rgba(0,0,0,0.15);
        margin-top: 20px;
        margin-bottom: 15px;
        color: white;
    }
    .ticket-header {
        font-size: 1.4rem;
        font-weight: 800;
        letter-spacing: 2px;
        border-bottom: 2px dashed rgba(255,255,255,0.4);
        padding-bottom: 12px;
        margin-bottom: 16px;
    }
    .ticket-body {
        font-size: 1.15rem;
        margin: 8px 0;
        line-height: 1.6;
    }
    .ticket-status {
        font-size: 1.4rem;
        font-weight: bold;
        margin-top: 16px;
        padding: 10px;
        background: rgba(255, 255, 255, 0.2);
        border-radius: 12px;
        display: inline-block;
        width: 100%;
    }
    
    div[data-testid="stTextInput"]:nth-of-type(1) input,
    div[data-testid="stTextInput"]:nth-of-type(2) input {
        text-align: center;
    }
    </style>
""",
    unsafe_allow_html=True,
)

query_params = st.query_params
title = query_params.get("title", None)
location = query_params.get("location", None)
invitees = query_params.get("invitees", None)

# ====================================================
# MODE 1: ลิงก์สำหรับผู้ตอบรับ ( Guest Mode )
# ====================================================
if title and location:
    st.markdown(
        '<h1 class="main-header">🍻 Hangout Inviter</h1>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<h2 class="center-text" style="color: #FF4B4B;">📌 {title}</h2>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<p class="center-text" style="font-size: 1.3rem;">📍 <b>สถานที่:</b> {location}</p>',
        unsafe_allow_html=True,
    )

    if invitees:
        people_list = [p.strip() for p in invitees.split(",") if p.strip()]
        st.markdown("<br>", unsafe_allow_html=True)
        st.write("👥 **เพื่อนๆ ที่ถูกชวน:**")
        st.write(", ".join([f"`{p}`" for p in people_list]))

    st.divider()

    st.markdown("### ตอบรับการนัดหมาย")
    guest_name = st.text_input(
        "ใส่ชื่อของคุณก่อนกดตอบรับ:", placeholder="เช่น บอส, นัด"
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button(
            "✅ ไปแน่นอน!", use_container_width=True, type="primary"
        ):
            if guest_name:
                st.session_state["response"] = {
                    "name": guest_name,
                    "status": "✅ ไปแน่นอน! 🥳",
                    "color": "linear-gradient(135deg, #11998e 0%, #38ef7d 100%)",
                }
                st.balloons()
            else:
                st.warning("กรุณากรอกชื่อก่อนกดตอบรับครับ")

    with col2:
        if st.button("❌ ไม่สะดวกไป", use_container_width=True):
            if guest_name:
                st.session_state["response"] = {
                    "name": guest_name,
                    "status": "❌ ไม่สะดวกไป 🥲",
                    "color": "linear-gradient(135deg, #FF416C 0%, #FF4B2B 100%)",
                }
            else:
                st.warning("กรุณากรอกชื่อก่อนกดตอบรับครับ")

    # แสดงการ์ดตั๋วตอบรับเมื่อกดปุ่ม
    if "response" in st.session_state:
        res = st.session_state["response"]

        st.markdown(
            f"""
        <div class="ticket-card" style="background: {res['color']};">
            <div class="ticket-header">🎟️ HANGOUT PASS</div>
            <div class="ticket-body">📌 <b>หัวข้อ:</b> {title}</div>
            <div class="ticket-body">📍 <b>สถานที่:</b> {location}</div>
            <div class="ticket-body">👤 <b>ผู้ตอบรับ:</b> {res['name']}</div>
            <div class="ticket-status">{res['status']}</div>
            <p style="font-size: 0.85rem; margin-top: 18px; opacity: 0.9;">
                📸 แคปหน้าจอนี้ส่งให้ผู้เชิญในแชตได้เลย!
            </p>
        </div>
        """,
            unsafe_allow_html=True,
        )

# ====================================================
# MODE 2: ลิงก์สำหรับผู้สร้างกิจกรรม ( Organizer Mode )
# ====================================================
else:
    st.markdown(
        '<h1 class="main-header">🍻 Hangout Inviter</h1>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div style="background-color: #E8F4F8; padding: 12px; border-radius: 8px; text-align: center; color: #1E3A8A; font-weight: 500; margin-bottom: 25px;">
            สร้างการนัดหมายใหม่ แล้วส่งลิงก์ให้เพื่อนๆ ได้เลย!
        </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-title-center">หัวข้อการนัดหมาย</div>',
        unsafe_allow_html=True,
    )
    input_title = st.text_input(
        "title",
        placeholder="เช่น ดื่มเบียร์หลังเลิกงาน, หมูกระทะ",
        label_visibility="collapsed",
    )

    st.write("")

    st.markdown(
        '<div class="section-title-center">สถานที่ / ร้าน</div>',
        unsafe_allow_html=True,
    )
    input_location = st.text_input(
        "location",
        placeholder="เช่น ร้าน ลาบอุบล, Rooftop Bar",
        label_visibility="collapsed",
    )

    st.divider()

    st.markdown(
        '<div class="section-title-left">รายชื่อผู้ถูกเชิญ</div>',
        unsafe_allow_html=True,
    )

    if "invitee_count" not in st.session_state:
        st.session_state.invitee_count = 1

    invitee_names = []

    for i in range(st.session_state.invitee_count):
        name = st.text_input(
            f"คนที่ {i+1}",
            key=f"invitee_{i}",
            placeholder=f"ชื่อเพื่อนคนที่ {i+1}",
            label_visibility="collapsed",
        )
        if name.strip():
            invitee_names.append(name.strip())

    col_add, col_remove = st.columns([1, 1])
    with col_add:
        if st.button("➕ เพิ่มรายชื่อ", use_container_width=True):
            st.session_state.invitee_count += 1
            st.rerun()

    with col_remove:
        if st.session_state.invitee_count > 1:
            if st.button("➖ ลบช่องล่าสุด", use_container_width=True):
                st.session_state.invitee_count -= 1
                st.rerun()

    st.divider()

    if st.button(
        "🔗 สร้างลิงก์สำหรับส่งให้เพื่อน",
        type="primary",
        use_container_width=True,
    ):
        if input_title and input_location:
            combined_invitees = ", ".join(invitee_names)

            encoded_title = urllib.parse.quote(input_title)
            encoded_location = urllib.parse.quote(input_location)
            encoded_invitees = urllib.parse.quote(combined_invitees)

            base_url = "https://hangout-planner.streamlit.app"
            share_url = f"{base_url}/?title={encoded_title}&location={encoded_location}&invitees={encoded_invitees}"

            st.success("สร้างลิงก์สำเร็จแล้ว! ก๊อปปี้ลิงก์ด้านล่างไปส่งให้เพื่อนได้เลย:")
            st.code(share_url, language="text")
        else:
            st.error("กรุณากรอกข้อมูล 'หัวข้อ' และ 'สถานที่' ให้ครบถ้วนครับ")
