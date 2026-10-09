import urllib.parse
import streamlit as st

# ตั้งค่าหน้าตาเว็บ
st.set_page_config(
    page_title="Hangout Planner", page_icon="🍻", layout="centered"
)

# ดึงข้อมูลจาก URL Query Parameters
query_params = st.query_params

title = query_params.get("title", None)
location = query_params.get("location", None)
invitees = query_params.get("invitees", None)

# ----------------------------------------------------
# Dynamic Theme / Header
# ----------------------------------------------------
st.title("🍻 Hangout Inviter")

# ====================================================
# MODE 1: ลิงก์สำหรับผู้ตอบรับ ( Guest Mode )
# ====================================================
if title and location:
    st.subheader(f"📌 {title}")
    st.write(f"📍 **สถานที่:** {location}")

    if invitees:
        people_list = [p.strip() for p in invitees.split(",") if p.strip()]
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
        if st.button("✅ ไปแน่นอน!", use_container_width=True, type="primary"):
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
    st.info("สร้างการนัดหมายใหม่ แล้วส่งลิงก์ให้เพื่อนๆ ได้เลย!")

    # ฟอร์มรับข้อมูล 3 ส่วนหลัก
    input_title = st.text_input(
        "1. หัวข้อการนัดหมาย", placeholder="เช่น ดื่มเบียร์หลังเลิกงาน, หมูกระทะเย็ดยอด"
    )
    input_location = st.text_input(
        "2. สถานที่ / ร้าน", placeholder="เช่น ร้าน ลาบอุบล, Rooftop Bar"
    )
    input_invitees = st.text_area(
        "3. รายชื่อผู้ถูกเชิญ (คั่นด้วยเครื่องหมายคำพูด หรือ comma ,)",
        placeholder="เช่น บอส, ต้า, นัด, แบงค์",
    )

    if st.button("🔗 สร้างลิงก์สำหรับส่งให้เพื่อน", type="primary"):
        if input_title and input_location:
            # แปลงข้อความให้ปลอดภัยสำหรับใช้ใน URL (URL Encoding)
            encoded_title = urllib.parse.quote(input_title)
            encoded_location = urllib.parse.quote(input_location)
            encoded_invitees = urllib.parse.quote(input_invitees)

            # URL สำหรับเครื่อง local (หรือเปลี่ยนเป็น URL โดเมนจริงถ้าเอาขึ้น Cloud)
            base_url = "http://localhost:8501"
            share_url = f"{base_url}/?title={encoded_title}&location={encoded_location}&invitees={encoded_invitees}"

            st.divider()
            st.success("สร้างลิงก์สำเร็จแล้ว! ก๊อปปี้ลิงก์ด้านล่างไปส่งในแชทกลุ่มได้เลย:")
            st.code(share_url, language="text")
        else:
            st.error("กรุณากรอกข้อมูล 'หัวข้อ' และ 'สถานที่' ให้ครบถ้วนครับ")
