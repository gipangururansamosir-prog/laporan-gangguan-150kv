import urllib.parse
import streamlit as st

st.set_page_config(page_title="Form Laporan Gangguan PHT 150 kV", layout="centered")

st.title("⚡ Form Pelaporan Gangguan Penghantar 150 kV")
st.markdown("Isi form di bawah ini untuk mengenerate format laporan otomatis.")

with st.form("form_gangguan"):
    st.subheader("📌 Informasi Umum")
    col1, col2 = st.columns(2)
    with col1:
        jam = st.text_input("Jam (WIB)", value="20:35")
        gi = st.text_input("Gardu Induk (GI)", value="Pangururan")
    with col2:
        bay_pht = st.text_input("Bay Penghantar (PHT)", value="PGRAN - GTELE 2")
        kondisi = st.selectbox("Kondisi", ["AR SUCCES", "TRIP / UNSUCCESS", "MANUAL TRIP"])

    st.subheader("📋 Annunciator & Parameter")
    annunciator_default = (
        "-Other\n- Phasa B\n- Neutral / Ground\n- Cb Close\n- Trip 3 Pole\n"
        "- Manual Close\n- LED Gruop 2\n- Distance OP\n- ZONE 4 OP\n"
        "- Aideo OP\n- Cr Sen Pott\n- Cr Send Dist\n- Ar In Progres\n- Ar Succes"
    )
    annunciator = st.text_area("Annunciator (Pisahkan per baris)", value=annunciator_default, height=150)
    
    col3, col4, col5 = st.columns(3)
    with col3:
        zone = st.text_input("Zone", value="4")
    with col4:
        jarak = st.text_input("Jarak (KM)", value="66.7")
    with col5:
        cuaca = st.text_input("Cuaca", value="HUJAN PETIR")

    st.subheader("⚡ Beban Sebelum Gangguan")
    col6, col7, col8, col9 = st.columns(4)
    with col6:
        mw = st.text_input("MW", value="3.4")
    with col7:
        mvar = st.text_input("MVar", value="0.3")
    with col8:
        i_amp = st.text_input("I (A)", value="14")
    with col9:
        e_kv = st.text_input("E (kV)", value="153")

    st.subheader("🔢 Counter Meter")
    col10, col11 = st.columns(2)
    with col10:
        la_sebelum = st.text_input("Counter LA Sebelum", value="9.8.6")
        la_sesudah = st.text_input("Counter LA Sesudah", value="MENYUSUL CUACA HUJAN")
    with col11:
        pmt_sebelum = st.text_input("Counter PMT Sebelum", value="404.397.398")
        pmt_sesudah = st.text_input("Counter PMT Sesudah", value="MENYUSUL CUACA HUJAN")

    st.subheader("👤 Petugas")
    col12, col13 = st.columns(2)
    with col12:
        operator = st.text_input("Operator", value="DANI LUMBAN RAJA")
    with col13:
        upb = st.text_input("UPB", value="SINAGA")

    submitted = st.form_submit_button("Generate Format Laporan")

# Tampilkan Hasil dan Tombol Kirim ke WA jika form di-submit
if submitted:
    teks_laporan = f"""*INFO Gangguan bay PHT {bay_pht.upper()}*

_Jam_ :  *{jam}* _WIB_
GI : *{gi}*
Gangguan By PHT {bay_pht.upper()}: 
Kondisi : {kondisi}
Annunciator
{annunciator}
Zone : {zone}
Jarak : {jarak} KM
Cuaca = {cuaca.upper()}

 Beban sebelum  : 
 Mw : {mw}
 Mvar : {mvar}
 I : {i_amp} A
 E : {e_kv}
 
Counter LA sebelum : {la_sebelum}
Counter LA sesudah : {la_sesudah}

Counter PMT sebelum : {pmt_sebelum}
Counter PMT sesudah   : {pmt_sesudah}

Operator : {operator.upper()}
Upb : {upb.upper()}

_Terimakasih_"""

    st.success("Laporan Berhasil Dibuat!")
    
    # 1. Menampilkan Teks Hasil untuk Di-copy Manual
    st.code(teks_laporan, language="markdown")

    # 2. Membuat Link WhatsApp
    teks_encoded = urllib.parse.quote(teks_laporan)
    url_wa = f"https://api.whatsapp.com/send?text={teks_encoded}"

    # 3. Tombol Kirim ke WhatsApp
    st.markdown(
        f"""
        <a href="{url_wa}" target="_blank" style="text-decoration: none;">
            <div style="
                background-color: #25D366;
                color: white;
                padding: 12px 20px;
                border-radius: 8px;
                font-weight: bold;
                text-align: center;
                cursor: pointer;
                font-family: sans-serif;
                margin-top: 10px;">
                📲 Kirim Langsung ke WhatsApp
            </div>
        </a>
        """,
        unsafe_allow_html=True
    )