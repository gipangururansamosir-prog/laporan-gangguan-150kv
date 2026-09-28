import urllib.parse
from datetime import datetime
import streamlit as st

st.set_page_config(page_title="Form Laporan Gangguan PHT 150 kV", layout="centered")

st.title("⚡ Form Pelaporan Gangguan Penghantar GI PANGURURAN 150 kV")
st.markdown("Isi form di bawah ini untuk mengenerate format laporan otomatis.")
st.markdown("PASTIKAN ANDA SUDAH FOTO RELAY TERLEBIH DAHULU")

# Inisialisasi session state untuk menyimpan laporan
if "teks_laporan" not in st.session_state:
    st.session_state.teks_laporan = ""

# Daftar indikasi LED Annunciator dari Relay Distance GE D60
DAFTAR_LED = [
    # STATUS
    "IN SERVICE", "TROUBLE", "TEST MODE", "TRIP", "ALARM", "PICKUP", 
    "VOLTAGE", "CURRENT", "FREQUENCY", "OTHER", 
    "PHASE A", "PHASE B", "PHASE C", "NEUTRAL / GROUND",
    
    # GROUP 1
    "CB CLOSE", "CB PHASE R OPEN", "CB PHASE S OPEN", "CB PHASE T OPEN", 
    "POTT ECHO ON", "POWER SWING BLOCK", "LINE PICKUP OP", 
    "TRIP 1-POLE", "TRIP 3-POLE", "BREAKER FAIL", "MANUAL CLOSE",
    
    # GROUP 2
    "DISTANCE OP", "ZONE 1 OP", "ZONE 2 OP", "ZONE 3 OP", "ZONE 4 OP", 
    "PUTT OP", "AIDED DEF OP", "CR SEND POTT ECHO", "CR SEND DIST", 
    "CR RECV DIST/POTT", "PLC ALARM/TROUBLE", "AR BLOCK",
    
    # GROUP 3
    "AR ENABLED", "AR DISABLED", "CB AR LOCKOUT", "AR LOCKOUT", 
    "AR IN PROGRESS", "AR SUCCESS", "SYNCRON ON", "CR SEND DEF", 
    "CR RECV DEF", "VT LINE FAIL", "VT BUS FAIL", "AR NOT READY",
    
    # GROUP 4
    "BACKUP PROT FAIL", "TCS 1 PHASE R FAIL", "TCS 1 PHASE S FAIL", 
    "TCS 1 PHASE T FAIL", "TCS 2 PHASE R FAIL", "TCS 2 PHASE S FAIL", 
    "TCS 2 PHASE T FAIL", "PRI ETHERNET FAIL", "SEC ETHERNET FAIL", "SNTP FAILURE"
]

with st.form("form_gangguan", clear_on_submit=False):
    st.subheader("📌 Informasi Umum")
    col0, col1, col2 = st.columns(3)
    with col0:
        tanggal = st.date_input("Tanggal", value=datetime.now())
    with col1:
        jam = st.text_input("Jam (WIB)", value="", placeholder="Contoh: 20:35")
        gi = st.text_input("Gardu Induk (GI)", value="", placeholder="Contoh: Pangururan")
    with col2:
        bay_pht = st.selectbox(
            "Bay Penghantar (PHT)", 
            [
                "-- Pilih Bay PHT --",
                "PGRUN - TELE #1",
                "PGRUN - TELE #2"
            ]
        )
        kondisi = st.selectbox("Kondisi", ["-- Pilih Kondisi --", "AR SUCCES", "TRIP / UNSUCCESS", "MANUAL TRIP"])

    st.subheader("📋 Relay Distance & Parameter Relay")
    
    led_terpilih = st.multiselect(
        "Pilih LED Distance yang Menyala / Active:",
        options=DAFTAR_LED,
        placeholder="Ketik atau pilih LED yang menyala..."
    )
    
    col3, col4, col5 = st.columns(3)
    with col3:
        zone = st.text_input("Zone", value="", placeholder="Contoh: 4")
    with col4:
        jarak = st.text_input("Jarak (KM)", value="", placeholder="Contoh: 66.7")
    with col5:
        cuaca = st.text_input("Cuaca", value="", placeholder="Contoh: HUJAN PETIR")

    st.subheader("⚡ Beban Sebelum Gangguan")
    col6, col7, col8, col9 = st.columns(4)
    with col6:
        mw = st.text_input("MW", value="")
    with col7:
        mvar = st.text_input("MVar", value="")
    with col8:
        i_amp = st.text_input("I (A)", value="")
    with col9:
        e_kv = st.text_input("E (kV)", value="")

    st.subheader("🔢 Counter Meter LA (Lightning Arrester)")
    st.markdown("**Counter LA Sebelum**")
    col_la_seb_r, col_la_seb_s, col_la_seb_t = st.columns(3)
    with col_la_seb_r:
        la_seb_r = st.text_input("R (Sebelum)", value="")
    with col_la_seb_s:
        la_seb_s = st.text_input("S (Sebelum)", value="")
    with col_la_seb_t:
        la_seb_t = st.text_input("T (Sebelum)", value="")

    st.markdown("**Counter LA Sesudah**")
    col_la_ses_r, col_la_ses_s, col_la_ses_t = st.columns(3)
    with col_la_ses_r:
        la_ses_r = st.text_input("R (Sesudah)", value="")
    with col_la_ses_s:
        la_ses_s = st.text_input("S (Sesudah)", value="")
    with col_la_ses_t:
        la_ses_t = st.text_input("T (Sesudah)", value="")

    st.subheader("🔢 Counter Meter PMT (Pemutus Tenaga)")
    st.markdown("**Counter PMT Sebelum**")
    col_pmt_seb_r, col_pmt_seb_s, col_pmt_seb_t = st.columns(3)
    with col_pmt_seb_r:
        pmt_seb_r = st.text_input("PMT R (Sebelum)", value="")
    with col_pmt_seb_s:
        pmt_seb_s = st.text_input("PMT S (Sebelum)", value="")
    with col_pmt_seb_t:
        pmt_seb_t = st.text_input("PMT T (Sebelum)", value="")

    st.markdown("**Counter PMT Sesudah**")
    col_pmt_ses_r, col_pmt_ses_s, col_pmt_ses_t = st.columns(3)
    with col_pmt_ses_r:
        pmt_ses_r = st.text_input("PMT R (Sesudah)", value="")
    with col_pmt_ses_s:
        pmt_ses_s = st.text_input("PMT S (Sesudah)", value="")
    with col_pmt_ses_t:
        pmt_ses_t = st.text_input("PMT T (Sesudah)", value="")

    st.subheader("👤 Petugas")
    col12, col13 = st.columns(2)
    with col12:
        operator = st.selectbox(
            "Operator", 
            [
                "-- Pilih Operator --",
                "DANI LUMBAN RAJA", 
                "DARIMAN BOIMO SOLIN", 
                "IMAM RIZKY SIREGAR", 
                "LEO NAINGGOLAN"
            ]
        )
    with col13:
        upb = st.text_input("UPB", value="")

    submitted = st.form_submit_button("Generate Format Laporan")

if submitted:
    bay_pht_teks = "" if bay_pht == "-- Pilih Bay PHT --" else bay_pht
    kondisi_teks = "" if kondisi == "-- Pilih Kondisi --" else kondisi
    operator_teks = "" if operator == "-- Pilih Operator --" else operator

    tgl_formatted = tanggal.strftime("%d-%m-%Y")

    if led_terpilih:
        distance_formatted = "\n".join([f"- {led}" for led in led_terpilih])
    else:
        distance_formatted = "-"

    st.session_state.teks_laporan = f"""*INFO Gangguan bay PHT {bay_pht_teks.upper()}*

_Tanggal_ : *{tgl_formatted}*
_Jam_ :  *{jam}* _WIB_
GI : *{gi}*
Gangguan By PHT {bay_pht_teks.upper()}: 
Kondisi : {kondisi_teks}
Distance
{distance_formatted}
Zone : {zone}
Jarak : {jarak} KM
Cuaca = {cuaca.upper()}

 Beban sebelum  : 
 Mw : {mw}
 Mvar : {mvar}
 I : {i_amp} A
 E : {e_kv}
 
Counter LA sebelum : R={la_seb_r} | S={la_seb_s} | T={la_seb_t}
Counter LA sesudah : R={la_ses_r} | S={la_ses_s} | T={la_ses_t}

Counter PMT sebelum : R={pmt_seb_r} | S={pmt_seb_s} | T={pmt_seb_t}
Counter PMT sesudah   : R={pmt_ses_r} | S={pmt_ses_t if 'pmt_ses_t' in locals() else ''} | T={pmt_ses_t}

Operator : {operator_teks.upper()}
Upb : {upb.upper()}

_Terimakasih_"""

if st.session_state.teks_laporan:
    st.success("Laporan Berhasil Dibuat!")
    
    st.code(st.session_state.teks_laporan, language="markdown")

    teks_encoded = urllib.parse.quote(st.session_state.teks_laporan)
    url_wa = f"https://api.whatsapp.com/send?text={teks_encoded}"

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
