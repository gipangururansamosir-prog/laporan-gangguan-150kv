import urllib.parse
import streamlit as st

st.set_page_config(page_title="Sistem Laporan Operasional 150 kV", layout="centered")

# ==========================================
# DATA BERSAMA (SHARED DROPDOWN & CONSTANTS)
# ==========================================
LIST_OPERATOR = [
    "-- Pilih Operator --",
    "DANI LUMBAN RAJA", 
    "DARIMAN BOIMO SOLIN", 
    "IMAM RIZKY SIREGAR", 
    "LEO NAINGGOLAN",

]

LIST_BAY = [
    "-- Pilih Bay --",
    "PGRAN - TELE #1",
    "PGRAN - TELE #2",
    "TRAFO DAYA #1 (30 MVA)"
]

DAFTAR_LED = [
    "IN SERVICE", "TROUBLE", "TEST MODE", "TRIP", "ALARM", "PICKUP", 
    "VOLTAGE", "CURRENT", "FREQUENCY", "OTHER", 
    "PHASE A", "PHASE B", "PHASE C", "NEUTRAL / GROUND",
    "CB CLOSE", "CB PHASE R OPEN", "CB PHASE S OPEN", "CB PHASE T OPEN", 
    "POTT ECHO ON", "POWER SWING BLOCK", "LINE PICKUP OP", 
    "TRIP 1-POLE", "TRIP 3-POLE", "BREAKER FAIL", "MANUAL CLOSE",
    "DISTANCE OP", "ZONE 1 OP", "ZONE 2 OP", "ZONE 3 OP", "ZONE 4 OP", 
    "PUTT OP", "AIDED DEF OP", "CR SEND POTT ECHO", "CR SEND DIST", 
    "CR RECV DIST/POTT", "PLC ALARM/TROUBLE", "AR BLOCK",
    "AR ENABLED", "AR DISABLED", "CB AR LOCKOUT", "AR LOCKOUT", 
    "AR IN PROGRESS", "AR SUCCESS", "SYNCRON ON", "CR SEND DEF", 
    "CR RECV DEF", "VT LINE FAIL", "VT BUS FAIL", "AR NOT READY",
    "BACKUP PROT FAIL", "TCS 1 PHASE R FAIL", "TCS 1 PHASE S FAIL", 
    "TCS 1 PHASE T FAIL", "TCS 2 PHASE R FAIL", "TCS 2 PHASE S FAIL", 
    "TCS 2 PHASE T FAIL", "PRI ETHERNET FAIL", "SEC ETHERNET FAIL", "SNTP FAILURE"
]

# ==========================================
# SIDEBAR NAVIGATION
# ==========================================
st.sidebar.title("📌 Menu Laporan")
menu_pilihan = st.sidebar.radio(
    "Pilih Jenis Laporan:",
    ["⚡ Laporan Gangguan PHT", "🔄 Laporan Manuver Tegangan"]
)

# ==========================================
# 1. FORM LAPORAN GANGGUAN PHT
# ==========================================
if menu_pilihan == "⚡ Laporan Gangguan PHT":
    st.title("⚡ Form Pelaporan Gangguan Penghantar 150 kV")

    with st.form("form_gangguan"):
        st.subheader("📌 Informasi Umum")
        col1, col2 = st.columns(2)
        with col1:
            jam = st.text_input("Jam (WIB)", placeholder="Contoh: 13:56")
            gi = st.text_input("Gardu Induk (GI)", value="Pangururan")
        with col2:
            bay_pht = st.selectbox("Bay Penghantar (PHT)", LIST_BAY)
            kondisi = st.selectbox("Kondisi", ["-- Pilih Kondisi --", "AR SUCCES", "TRIP / UNSUCCESS", "MANUAL TRIP"])

        st.subheader("📋 Annunciator & Parameter Relay")
        led_terpilih = st.multiselect("Pilih LED Annunciator Active:", options=DAFTAR_LED)
        
        col3, col4, col5 = st.columns(3)
        with col3:
            zone = st.text_input("Zone", placeholder="Contoh: 4")
        with col4:
            jarak = st.text_input("Jarak (KM)", placeholder="Contoh: 65.3")
        with col5:
            cuaca = st.selectbox("Cuaca", ["CERAH", "HUJAN", "MENDUNG", "BERAWAN"])

        st.subheader("⚡ Beban Sebelum Gangguan")
        col6, col7, col8, col9 = st.columns(4)
        mw = col6.text_input("MW")
        mvar = col7.text_input("MVar")
        i_amp = col8.text_input("I (A)")
        e_kv = col9.text_input("E (kV)")

        st.subheader("🔢 Counter Meter LA & PMT")
        col_la1, col_la2 = st.columns(2)
        la_seb = col_la1.text_input("Counter LA Sebelum (R|S|T)", placeholder="R=7 | S=8 | T=9")
        la_ses = col_la2.text_input("Counter LA Sesudah (R|S|T)", placeholder="R=8 | S=9 | T=10")

        col_pmt1, col_pmt2 = st.columns(2)
        pmt_seb = col_pmt1.text_input("Counter PMT Sebelum (R|S|T)", placeholder="R=234 | S=235 | T=236")
        pmt_ses = col_pmt2.text_input("Counter PMT Sesudah (R|S|T)", placeholder="R=235 | S=236 | T=237")

        st.subheader("👤 Petugas")
        col12, col13 = st.columns(2)
        operator = col12.selectbox("Operator", LIST_OPERATOR)
        upb = col13.text_input("UPB / Dispatcher")

        submitted_ggn = st.form_submit_button("Generate Laporan Gangguan")

    if submitted_ggn:
        bay_pht_teks = "" if bay_pht == "-- Pilih Bay --" else bay_pht
        kondisi_teks = "" if kondisi == "-- Pilih Kondisi --" else kondisi
        operator_teks = "" if operator == "-- Pilih Operator --" else operator
        annunciator_formatted = "\n".join([f"- {led}" for led in led_terpilih]) if led_terpilih else "-"

        teks_gangguan = f"""*INFO Gangguan bay PHT {bay_pht_teks}*

_Jam_ : *{jam}* _WIB_
GI : *{gi}*
Gangguan By PHT {bay_pht_teks}: 
Kondisi : {kondisi_teks}
Annunciator
{annunciator_formatted}
Zone : {zone}
Jarak : {jarak} KM
Cuaca = {cuaca}

Beban sebelum : 
Mw : {mw}
Mvar : {mvar}
I : {i_amp} A
E : {e_kv}

Counter LA sebelum : {la_seb}
Counter LA sesudah : {la_ses}

Counter PMT sebelum : {pmt_seb}
Counter PMT sesudah : {pmt_ses}

Operator : {operator_teks}
Upb : {upb}

_Terimakasih_"""

        st.success("Laporan Gangguan Berhasil Dibuat!")
        st.code(teks_gangguan, language="markdown")

        url_wa = f"https://api.whatsapp.com/send?text={urllib.parse.quote(teks_gangguan)}"
        st.markdown(f'<a href="{url_wa}" target="_blank"><button style="background-color:#25D366; color:white; border:none; padding:12px 20px; border-radius:8px; font-weight:bold; width:100%; cursor:pointer;">📲 Kirim Laporan Gangguan ke WhatsApp</button></a>', unsafe_allow_html=True)

# ==========================================
# 2. FORM LAPORAN MANUVER TEGANGAN
# ==========================================
elif menu_pilihan == "🔄 Laporan Manuver Tegangan":
    st.title("🔄 Form Pelaporan Manuver Tegangan")

    # Pilih Tipe Peralatan Manuver
    tipe_pilihan_manuver = st.radio(
        "Pilih Bay yang Bermanuver:",
        ["Bay PHT (Penghantar)", "Bay Trafo Daya (30 MVA)"],
        horizontal=True
    )

    st.markdown("---")

    # ------------------------------------------
    # SUB-FORM: MANUVER BAY TRAFO DAYA
    # ------------------------------------------
    if tipe_pilihan_manuver == "Bay Trafo Daya (30 MVA)":
        with st.form("form_manuver_trafo"):
            st.subheader("📌 Detail Pekerjaan Trafo Daya")
            col_t1, col_t2 = st.columns(2)
            with col_t1:
                tgl_manuver = st.text_input("Hari & Tanggal", value="SENIN, 22-09-2025")
                kegiatan_trafo = st.text_input("Nama Pekerjaan", value="PEMELIHARAAN 2 TAHUNAN BAY TRAFO DAYA #1")
                status_manuver = st.selectbox("Status Manuver", ["PEMBEBASAN TEGANGAN", "PEMBERIAN TEGANGAN"])
            with col_t2:
                pj = st.text_input("P.jwb P (Penanggung Jawab)", value="Andre Valen")
                k3 = st.text_input("Pngws K3 (Pengawas K3)", value="Ferlan A")
                pp = st.text_input("Pngws P (Pengawas Pekerjaan)", value="Zaka A P")
                pm = st.text_input("Pngws M (Pengawas Manuver)", value="Janisman Turnip")

            st.subheader("⏱️ Urutan Execution / Pukul")
            default_kronologi_trafo = "PUKUL : 07:47 PENYULANG DT-1 & DT-2 DILEPAS\nPUKUL : 07:48 PMT INC 20 KV DILEPAS\nPUKUL : 07:54 PMT 150KV TD-1 DILEPAS\nPUKUL : 07:00 PMS BUS B TD -1 DILEPAS"
            kronologi_trafo = st.text_area("Urutan Eksekusi Manuver Trafo:", value=default_kronologi_trafo, height=130)

            st.subheader("👤 Petugas")
            col_t3, col_t4 = st.columns(2)
            with col_t3:
                up2b_trafo = st.text_input("UP2B", value="")
            with col_t4:
                op_trafo = st.selectbox("OP (Operator)", LIST_OPERATOR, index=6) # Default: DAVID PANGGABEAN & IMAM R SIREGAR

            submitted_trafo = st.form_submit_button("Generate Laporan Manuver Trafo")

        if submitted_trafo:
            op_trafo_teks = "" if op_trafo == "-- Pilih Operator --" else op_trafo

            teks_manuver_trafo = f"""{tgl_manuver.upper()} 
{kegiatan_trafo.upper()}

P.jwb P : {pj}
Pngws K3: {k3}
Pngws P : {pp}
Pngws M : {pm}

{status_manuver.upper()} 

{kronologi_trafo}

UP2B : {up2b_trafo}
OP : {op_trafo_teks}"""

            st.success("Laporan Manuver Trafo Berhasil Dibuat!")
            st.code(teks_manuver_trafo, language="markdown")

            url_wa_trafo = f"https://api.whatsapp.com/send?text={urllib.parse.quote(teks_manuver_trafo)}"
            st.markdown(f'<a href="{url_wa_trafo}" target="_blank"><button style="background-color:#25D366; color:white; border:none; padding:12px 20px; border-radius:8px; font-weight:bold; width:100%; cursor:pointer;">📲 Kirim Laporan Trafo ke WhatsApp</button></a>', unsafe_allow_html=True)

    # ------------------------------------------
    # SUB-FORM: MANUVER BAY PHT (PENGHANTAR)
    # ------------------------------------------
    else:
        with st.form("form_manuver_pht"):
            st.subheader("📌 Detail Pekerjaan PHT")
            col_m1, col_m2 = st.columns(2)
            with col_m1:
                jenis_manuver = st.selectbox("Jenis Manuver", ["pemberian Tegangan", "pembebasan Tegangan"])
                bay_pht = st.selectbox("Bay / Equipment", [b for b in LIST_BAY if "TRAFO" not in b])
                rangka = st.text_input("Dalam Rangka", value="HAR 2 Tahunan Gi tele")
            with col_m2:
                penanggung_jawab = st.text_input("Penanggung Jawab", value="Andre valen")
                pengawas_k3 = st.text_input("Pengawas K3", value="Joel silver")
                pengawas_pekerjaan = st.text_input("Pengawas Pekerjaan", value="Nanda Bagus Sudarta")
                pengawas_manuver = st.text_input("Pengawas Manuver", value="Anggi simangunsong")

            st.subheader("⏱️ Kronologi Manuver (Urutan Pukul & Aksi)")
            default_kronologi = "Pukul 13:20 PMS GROUND PHT PGRAN-TELE-2 LEPAS\nPukul 13:23 PMS LINE PGRAN-TELE-2 MASUK\nPukul 13:23 PMS BUS 2 PGRAN-TELE-2 MASUK\nPukul 13:28 PMT 150 PGRAN-TELE-2 MASUK"
            kronologi = st.text_area("Tuliskan Jam dan Aksi Eksekusi:", value=default_kronologi, height=130)

            st.subheader("👤 Petugas Eksekusi & Kondisi")
            col_m3, col_m4, col_m5 = st.columns(3)
            with col_m3:
                operator_m = st.selectbox("Operator (OP)", LIST_OPERATOR)
            with col_m4:
                up2b_m = st.text_input("UP2B", value="UMAR")
            with col_m5:
                cuaca_m = st.selectbox("Cuaca", ["CERAH", "HUJAN", "MENDUNG", "BERAWAN"])

            submitted_mnv = st.form_submit_button("Generate Laporan Manuver PHT")

        if submitted_mnv:
            bay_m_teks = "" if bay_pht == "-- Pilih Bay --" else bay_pht
            op_m_teks = "" if operator_m == "-- Pilih Operator --" else operator_m

            teks_manuver = f"""*Manuver {jenis_manuver}  PHT  Pangururan-Tele #{bay_m_teks[-1] if '#' in bay_m_teks else bay_m_teks}*
Dalam rangka {rangka}

PENANGGUNG JAWAB : {penanggung_jawab}
PENGAWAS K3 : {pengawas_k3}
PENGAWAS PEKERJAAN : {penanggung_jawab}
PENGAWAS MANUVER : {pengawas_manuver}

{kronologi}

OP : {op_m_teks}
UP2B : {up2b_m}
CUACA : {cuaca_m}"""

            st.success("Laporan Manuver PHT Berhasil Dibuat!")
            st.code(teks_manuver, language="markdown")

            url_wa_mnv = f"https://api.whatsapp.com/send?text={urllib.parse.quote(teks_manuver)}"
            st.markdown(f'<a href="{url_wa_mnv}" target="_blank"><button style="background-color:#25D366; color:white; border:none; padding:12px 20px; border-radius:8px; font-weight:bold; width:100%; cursor:pointer;">📲 Kirim Laporan Manuver ke WhatsApp</button></a>', unsafe_allow_html=True)
