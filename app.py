import urllib.parse
import streamlit as st

# ตั้งค่าหน้าตาเว็บ
st.set_page_config(
    page_title="Hangout Planner", page_icon="🍻", layout="centered"
)

# Custom CSS จัดข้อความและ input ให้อยู่ตรงกลาง
st.markdown(
    """
    <style>
    /* จัด Title และ Header ให้อยู่ตรงกลาง */
    .main-header {
        text-align: center;
        font-size: 2.2rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .center-text {
        text-align: center;
    }
    
    /* จัดข้อความในช่องกรอก 1 และ 2 ให้อยู่ตรงกลาง */
    div[data-testid="stTextInput"]:nth-of-type(1) input,
    div[data-testid="stTextInput"]:nth-of-type(2) input {
        text-align: center;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# ดึงข้อมูลจาก URL Query Parameters
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
        f'<p class="center-text" style="font-size: 1.2rem;">📍 <b>สถานที่:</b> {location}</p>',
        unsafe_allow_html=True,
    )

    if invitees:
        people_list = [p.strip() for p in invitees.split(",") if p.strip()]
        st.markdown("<br>", unsafe_allow_html=True)
        st.write("👥 **เพื่อนๆ ที่ถูกชวน:**")
        st.write(", ".join([f"`{p}`" for p in people_list]))

    st.divider()

    # ส่วนตอบรับของเพื่อน
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
                st.balloons()
                st.success(
                    f"เย้! บันทึกแล้วว่า **{guest_name}** ไปร่วมงานนี้ 🥳"
                )
            else:
                st.warning("กรุณากรอกชื่อก่อนกดตอบรับครับ")

    with col2:
        if st.button("❌ ไม่สะดวกไป", use_container_width=True):
            if guest_name:
                st.info(f"เสียดายจัง ไว้เจอกันงานหน้านะ **{guest_name}** 🥲")
            else:
                st.warning("กรุณากรอกชื่อก่อนกดตอบรับครับ")

# ====================================================
# MODE 2: ลิงก์สำหรับผู้สร้างกิจกรรม ( Organizer Mode )
# ====================================================
else:
    st.markdown(
        '<h1 class="main-header">🍻 Hangout Inviter</h1>',
        unsafe_allow_html=True,
    )

    # กล่องข้อความแจ้งเตือนตรงกลาง
    st.markdown(
        """
        <div style="background-color: #E8F4F8; padding: 12px; border-radius: 8px; text-align: center; color: #1E3A8A; font-weight: 500; margin-bottom: 25px;">
            สร้างการนัดหมายใหม่ แล้วส่งลิงก์ให้เพื่อนๆ ได้เลย!
        </div>
    """,
        unsafe_allow_html=True,
    )

    # 1. หัวข้อ (ตรงกลาง)
    st.markdown(
        "<p class='center-text' style='font-weight: 600; margin-bottom: 4px;'>1. หัวข้อการนัดหมาย</p>",
        unsafe_allow_html=True,
    )
    input_title = st.text_input(
        "title",
        placeholder="เช่น ดื่มเบียร์หลังเลิกงาน, หมูกระทะ",
        label_visibility="collapsed",
    )

    st.write("")  # เว้นระยะ

    # 2. สถานที่ (ตรงกลาง)
    st.markdown(
        "<p class='center-text' style='font-weight: 600; margin-bottom: 4px;'>2. สถานที่ / ร้าน</p>",
        unsafe_allow_html=True,
    )
    input_location = st.text_input(
        "location",
        placeholder="เช่น ร้าน ลาบอุบล, Rooftop Bar",
        label_visibility="collapsed",
    )

    st.divider()

    # 3. รายชื่อผู้ถูกเชิญ (ชิดซ้าย + ปุ่มเพิ่มลิส)
    st.markdown("### 3. รายชื่อผู้ถูกเชิญ")

    # เก็บจำนวนช่องกรอกชื่อใน Session State
    if "invitee_count" not in st.session_state:
        st.session_state.invitee_count = 1

    invitee_names = []

    # แสดงช่องกรอกชื่อตามจำนวนที่มี
    for i in range(st.session_state.invitee_count):
        name = st.text_input(
            f"คนที่ {i+1}",
            key=f"invitee_{i}",
            placeholder=f"ชื่อเพื่อนคนที่ {i+1}",
            label_visibility="collapsed",
        )
        if name.strip():
            invitee_names.append(name.strip())

    # ปุ่มเพิ่ม / ลบ ช่องกรอกชื่อ
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

    # ปุ่มสร้างลิงก์
    if st.button(
        "🔗 สร้างลิงก์สำหรับส่งให้เพื่อน",
        type="primary",
        use_container_width=True,
    ):
        if input_title and input_location:
            # รวมรายชื่อที่กรอกคั่นด้วย comma
            combined_invitees = ", ".join(invitee_names)

            encoded_title = urllib.parse.quote(input_title)
            encoded_location = urllib.parse.quote(input_location)
            encoded_invitees = urllib.parse.quote(combined_invitees)

            # โดเมนจริงของบอส
            base_url = "https://hangout-planner.streamlit.app"
            share_url = f"{base_url}/?title={encoded_title}&location={encoded_location}&invitees={encoded_invitees}"

            st.success("สร้างลิงก์สำเร็จแล้ว! ก๊อปปี้ลิงก์ด้านล่างไปส่งให้เพื่อนได้เลย:")
            st.code(share_url, language="text")
        else:
            st.error("กรุณากรอกข้อมูล 'หัวข้อ' และ 'สถานที่' ให้ครบถ้วนครับ")
