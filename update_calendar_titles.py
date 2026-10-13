import os
import re
from datetime import datetime

BASE_DIR = "/Users/shubhayu/Documents/antigravity/splendid-raman"
DOWNLOADS_DIR = os.path.join(BASE_DIR, "downloads")
os.makedirs(DOWNLOADS_DIR, exist_ok=True)

UNIFIED_COLOR = "#BDBDBD"

def write_master_ics(filepath, cal_name, prod_id, color, events):
    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        f"PRODID:{prod_id}",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        f"X-WR-CALNAME:{cal_name}",
        "X-WR-TIMEZONE:Asia/Kolkata",
        f"X-APPLE-CALENDAR-COLOR:{color}",
        f"COLOR:{color}",
        "BEGIN:VTIMEZONE",
        "TZID:Asia/Kolkata",
        "X-LIC-LOCATION:Asia/Kolkata",
        "BEGIN:STANDARD",
        "TZOFFSETFROM:+0530",
        "TZOFFSETTO:+0530",
        "TZNAME:IST",
        "DTSTART:19700101T000000",
        "END:STANDARD",
        "END:VTIMEZONE"
    ]

    events_sorted = sorted(events, key=lambda x: x['dtstart'])
    now_utc = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')

    for ev in events_sorted:
        lines.append("BEGIN:VEVENT")
        lines.append(f"UID:{ev['uid']}")
        lines.append(f"DTSTAMP:{now_utc}")
        lines.append(f"DTSTART;TZID=Asia/Kolkata:{ev['dtstart']}")
        lines.append(f"DTEND;TZID=Asia/Kolkata:{ev['dtend']}")
        lines.append(f"SUMMARY:{ev['summary']}")
        if 'location' in ev and ev['location']:
            lines.append(f"LOCATION:{ev['location']}")
        if 'description' in ev and ev['description']:
            desc = ev['description'].replace("\n", "\\n")
            lines.append(f"DESCRIPTION:{desc}")
        lines.append("STATUS:CONFIRMED")
        lines.append("TRANSP:OPAQUE")
        lines.append("BEGIN:VALARM")
        lines.append("ACTION:DISPLAY")
        lines.append("DESCRIPTION:Class in 15 minutes")
        lines.append("TRIGGER:-PT15M")
        lines.append("END:VALARM")
        lines.append("END:VEVENT")

    lines.append("END:VCALENDAR")
    lines.append("")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\r\n".join(lines))
    print(f"Generated {filepath} with {len(events_sorted)} events.")

# ==========================================
# GENERAL SCHEDULE (Roll 1-202)
# ==========================================
all_gen_events = []

# 1. OPHTHALMOLOGY ([OPTHA])
ophth_raw = [
    ("20261008", "Dr. Arpita G", "Anatomy of Eye & Physiology of Vision", "OP1.1"),
    ("20261015", "Dr. Daisy V", "Refractive errors, Refractive surgeries, Amblyopia", "OP1.2, OP1.4, OP1.5"),
    ("20261022", "Dr. Rohini D K", "Lids & its Anomalies", "OP2.1"),
    ("20261029", "Dr. Rohini D K", "Congenital & Acquired Dacryocystitis", "OP2.2"),
    ("20261105", "Dr. Bhagyajyothi B K", "Proptosis, Thyroid eye disease, Orbital cellulitis", "OP2.6, OP2.3, OP2.4"),
    ("20261112", "Dr. Bhagyajyothi B K", "Cavernous sinus thrombosis, Orbital Tumours", "OP2.5, OP2.7, OP2.8"),
    ("20261119", "Dr. Samyakta S", "Trachoma, Allergic conjunctivitis, Vernal catarrh", "OP3.3, OP3.4"),
    ("20261126", "Dr. S C Bubanale", "Anatomy, Physiology, Anomalies & Inflammations of Cornea", "OP4.1, OP4.2"),
    ("20261203", "Dr. S C Bubanale", "Infective Keratitis", "OP4.3"),
    ("20261210", "Dr. Samyakta S", "Corneal opacity, Corneal blindness, Keratoplasty", "OP4.4, OP4.6, OP4.7"),
    ("20261217", "Dr. Daisy V", "Dry eyes, Vitamin A deficiency", "OP4.5, OP10.4"),
    ("20270107", "Dr. Chethana W", "Uveitis: Classification, Features, Diagnosis & Treatment", "OP6.1, OP6.2"),
    ("20270128", "Dr. Chethana W", "Systemic conditions associated with Uveitis", "OP6.4"),
    ("20270204", "Dr. Rekha R Mudhol", "Congenital glaucoma, Primary open angle glaucoma", "OP7.1, OP7.2"),
    ("20270211", "Dr. Rekha R Mudhol", "Primary angle closure glaucoma", "OP7.3"),
    ("20270218", "Dr. Farheen", "Secondary glaucoma", "OP7.4"),
    ("20270225", "Dr. A L Tenagi", "Anatomy of lens & Senile cataract", "OP8.1, OP8.2"),
    ("20270304", "Dr. A L Tenagi", "Cataract surgery", "OP8.4"),
    ("20270311", "Dr. Mounesh P", "Anatomy of Normal Retina, Direct & indirect Ophthalmoscopy", "OP9.1"),
    ("20270318", "Dr. Deepashri M", "Diabetic Retinopathy", "OP9.2"),
    ("20270325", "Dr. Deepashri M", "Vascular occlusions of retina", "OP9.3"),
    ("20270401", "Dr. Mounesh P", "Hypertensive retinopathy & other retinal diseases", "OP9.4"),
    ("20270408", "Dr. Zarafshan J", "Diseases of the optic nerve", "OP9.5"),
    ("20270429", "Dr. Farheen M", "Diseases of the visual pathway", "OP9.5"),
    ("20270506", "Dr. Smitha K. S.", "Extraocular Muscles & Binocular single vision", "OP10.1"),
    ("20270513", "Dr. Smitha K. S.", "Diagnosis of Heterotropia / Strabismus", "OP10.2"),
    ("20270520", "Dr. Anjanabai O", "Enucleation, evisceration and exenteration", "OP10.5"),
    ("20270527", "Dr. Anjanabai O", "Ocular injuries", "OP10.6"),
    ("20270603", "Dr. Arpita G", "NPCB, Vision 2020", "OP10.7"),
    ("20270610", "Dr. Zarafshan J", "Ocular Pharmacology", "")
]
for idx, (dt, fac, top, code) in enumerate(ophth_raw, start=1):
    c_str = f" {code}" if code else ""
    all_gen_events.append({
        "uid": f"jnmc-ophth-ph3-1-{idx}-{dt}@jnmc.edu",
        "dtstart": f"{dt}T120000",
        "dtend": f"{dt}T130000",
        "summary": f"[OPTHA] {fac} // {top}{c_str}",
        "location": "JNMC Belagavi",
        "description": f"Subject: Ophthalmology (Theory)\nFaculty: {fac}\nTopic: {top}\nCompetency: {code}\nTime: 12:00 PM - 1:00 PM"
    })

# 2. GENERAL MEDICINE ([MED])
med_raw = [
    ("20261005", "Dr. Rakesh Noubade", "Parasitic Infections - Hook & Roundworm", "GM 16.9, 16.13", "Block I: Fever and Febrile Syndrome"),
    ("20261012", "Dr. Rakesh Noubade", "Tape Worm & Filariasis", "GM 16.3, 16.9", "Block I: Fever and Febrile Syndrome"),
    ("20261019", "Dr. Rakesh Noubade", "Amoebiasis & Giardiasis", "GM 16.3, 16.9", "Block I: Fever and Febrile Syndrome"),
    ("20261026", "Dr. Rakesh Noubade", "Fat Soluble Vitamins (Vit A & D)", "GM 24.1", "Block I: Nutrition and Vitamin Deficiencies"),
    ("20261102", "Dr. Rakesh Noubade", "Fat Soluble Vitamins (Vit E & K)", "GM 24.2", "Block I: Nutrition and Vitamin Deficiencies"),
    ("20261109", "Dr. Rakesh Noubade", "Water Soluble Vitamins (Vit B1, B2 & B6)", "GM 24.3", "Block I: Nutrition and Vitamin Deficiencies"),
    ("20261116", "Dr. Rakesh Noubade", "Total Parenteral Nutrition", "GM 24.4", "Block I: Nutrition and Vitamin Deficiencies"),
    ("20261123", "Dr. Vijay Kaveri", "Obesity", "GM 14.1-14.5, 14.13, 14.14", "Block I: Obesity"),
    ("20261130", "Dr. Vijay Kaveri", "GERD", "GM 15.6", "Block I: GIT / Liver Disease"),
    ("20261207", "Dr. Vijay Kaveri", "Acid Peptic Disease & H Pylori", "GM 15.10, 15.15, 15.16", "Block I: GIT / Liver Disease"),
    ("20261214", "Dr. Vijay Kaveri", "Physiological basis of hyperbilirubinemia", "GM 5.1", "Block I: GIT / Liver Disease"),
    ("20261221", "Dr. Vijay Kaveri", "Viral Hepatitis (A+E)", "GM 5.2, 5.3", "Block I: GIT / Liver Disease"),
    ("20270104", "Dr. Vijay Kaveri", "Viral Hepatitis (B+D)", "GM 5.2, 5.3", "Block I: GIT / Liver Disease"),
    ("20270125", "Dr. Vijay Kaveri", "Hepatitis C & HCC", "GM 5.2, 5.3, 5.5, 5.15", "Block II"),
    ("20270201", "Dr. Vijay Kaveri", "Drug Induced Liver Injury (DILI)", "GM 5.6", "Block II"),
    ("20270208", "Dr. Prashant Rathod", "Alcoholic Liver Disease (Fatty Liver & Hepatitis)", "GM 5.2, 5.4", "Block II"),
    ("20270215", "Dr. Prashant Rathod", "Cirrhosis of Liver (C/F, Etiology & Pathogenesis)", "GM 5.2, 5.6, 5.15", "Block II"),
    ("20270222", "Dr. Prashant Rathod", "NAFLD", "GM 5.2, 5.15", "Block II"),
    ("20270301", "Dr. Prashant Rathod", "Portal Hypertension", "GM 5.2, 5.15", "Block II"),
    ("20270308", "Dr. Prashant Rathod", "SBP, Hepatic Encephalopathy & Hepatorenal Syndrome", "GM 5.5, 5.15", "Block II"),
    ("20270315", "Dr. Prashant Rathod", "Wilson's Disease & Hemochromatosis", "GM 5.2, 5.8", "Block II"),
    ("20270322", "Dr. Prashant Rathod", "Cholelithiasis & Cholecystitis", "GM 5.7", "Block II"),
    ("20270329", "Dr. Faisal Jamadar", "Upper GI Bleed", "GM 15.1-15.3, 15.6, 15.8, 15.11-15.16", "Block II: GI Bleeding"),
    ("20270405", "Dr. Faisal Jamadar", "Lower GI Bleed", "GM 15.1, 15.3, 15.6, 15.11, 15.16", "Block II: GI Bleeding"),
    ("20270426", "Dr. Faisal Jamadar", "Acute Diarrhea", "GM 16.1, 16.2, 16.11, 16.14", "Block III: Diarrheal Disorders"),
    ("20270503", "Dr. Faisal Jamadar", "Chronic Diarrhea", "GM 16.2, 16.3, 16.12, 16.14", "Block III: Diarrheal Disorders"),
    ("20270510", "Dr. Faisal Jamadar", "Malabsorption Syndrome (MAS)", "GM 16.3", "Block III: Diarrheal Disorders"),
    ("20270517", "Dr. Faisal Jamadar", "Irritable Bowel Syndrome (IBS)", "GM 16.3, 16.12", "Block III: Diarrheal Disorders"),
    ("20270524", "Dr. Faisal Jamadar", "Inflammatory Bowel Disease (IBD)", "GM 16.15, 16.16, 16.17", "Block III: Diarrheal Disorders"),
    ("20270531", "Dr. Faisal Jamadar", "Revision / MCQ", "", "Block III")
]
for idx, (dt, fac, top, code, blk) in enumerate(med_raw, start=1):
    c_str = f" {code}" if code else ""
    all_gen_events.append({
        "uid": f"jnmc-gm-ph3-1-{idx}-{dt}@jnmc.edu",
        "dtstart": f"{dt}T080000",
        "dtend": f"{dt}T090000",
        "summary": f"[MED] {fac} // {top}{c_str}",
        "location": "Pharmacology Lecture Hall, JNMC Belagavi",
        "description": f"Subject: General Medicine (Theory)\nFaculty: {fac}\nTopic: {top}\nCompetency: {code}\nSection: {blk}\nTime: 8:00 AM - 9:00 AM"
    })

# 3. GENERAL SURGERY ([SURG])
surg_raw = [
    ("20261006", "Dr. S.I. Neeli (Urology)", "Congenital anomalies of genitourinary tract", "SU 29.2, AN 29.2"),
    ("20261013", "Dr. Vikram Prabha (Urology)", "Urinary tract infection", "SU 29.3"),
    ("20261027", "Dr. Vishal Kadeli (Urology)", "Urolithiasis", "SU 29.5"),
    ("20261103", "Dr. R.B. Nerli (Urology)", "Renal tumors", "SU 29.6"),
    ("20261117", "Dr. S.I. Neeli (Urology)", "Diseases of prostate", "SU 29.9"),
    ("20261124", "Dr. Vikram Prabha (Urology)", "Testis & Scrotum", "SU 30.2-30.6, AN 46.1"),
    ("20261201", "Dr. Shivagouda Patil (Urology)", "Diseases of the Penis", "SU 30.1"),
    ("20261208", "Dr. Darshan D.S. (CTVS)", "Coronary artery diseases", "SU 26.1"),
    ("20261215", "Dr. Abhishek Prabhu (CTVS)", "Chest Injury 1: Pneumothorax, Fracture ribs", "SU 17.10"),
    ("20261222", "Dr. Pariswanath Patil (CTVS)", "Chest Injury 2: Cardiac tamponade & mediastinal injury", "SU 17.8"),
    ("20270105", "Dr. Tarun Raina Ramman (CTVS)", "Congenital & Valvular heart diseases", "SU 26.1, PE 23.1, 23.2"),
    ("20270202", "Dr. Kiran Kurkure (CTVS)", "Peripheral arterial diseases", "SU 27.3"),
    ("20270209", "Dr. M.G. Dhorigol (Anaesthesiology)", "Pre-operative assessment", "SU 11.1, AS 3.1"),
    ("20270216", "Dr. C.S. Sanikop (Anaesthesiology)", "General, regional, spinal & epidural anesthesia", "SU 11.2, AS 5.1"),
    ("20270223", "Dr. Santosh Kurbet (Pediatric Surgery)", "Congenital Anomalies: Hepatobiliary system & Pancreas", "SU 28.10, 28.12"),
    ("20270302", "Dr. Bharath Naik (Plastic Surgery)", "Skin grafting", "SU 5.3"),
    ("20270309", "Dr. Manoj D Togale", "Basic concepts of transplantation", "SU 13.1-13.3"),
    ("20270316", "Dr. Ramesh S Koujalagi", "Mass Casualties", "SU 17.3"),
    ("20270323", "Dr. Prashant Hombal", "Management of Musculoskeletal disorders", "SU 17.3"),
    ("20270330", "Dr. Shrishail C Metgud", "Abdominal Tuberculosis", "SU 6.1"),
    ("20270406", "Dr. Ravi Kerur (Anesthesiology)", "Pain management", "SU 11.5"),
    ("20270427", "Dr. Rahul Kenawadekar", "Day care surgery", "SU 11.4"),
    ("20270504", "Dr. Swapnil Pattanshetti (Pediatric Surgery)", "Anorectal anomalies", "SU 28.16"),
    ("20270511", "Dr. Santosh Kurbet (Pediatric Surgery)", "Congenital anomalies of GIT", "SU 28.14"),
    ("20270518", "Dr. Prakash Mahantshetti (Neurosurgery)", "EDH, SDH, SAH", "SU 17.6"),
    ("20270525", "Dr. S.I. Neeli (Urology)", "Investigation of Urological Disorders", "SU 29.1, PE 21.4"),
    ("20270601", "Dr. Vikram Prabha (Urology)", "Hematuria", "SU 29.1, PE 21.4"),
    ("20270608", "Dr. Swapnil Pattanshetti (Pediatric Surgery)", "Pediatric intestinal obstruction", "SU 28.14")
]
for idx, (dt, fac, top, code) in enumerate(surg_raw, start=1):
    c_str = f" {code}" if code else ""
    all_gen_events.append({
        "uid": f"jnmc-surg-ph3-1-{idx}-{dt}@jnmc.edu",
        "dtstart": f"{dt}T080000",
        "dtend": f"{dt}T090000",
        "summary": f"[SURG] {fac} // {top}{c_str}",
        "location": "Pharmacology Lecture Hall, JNMC Belagavi",
        "description": f"Subject: General Surgery (Theory)\nFaculty: {fac}\nTopic: {top}\nCompetency: {code}\nTime: 8:00 AM - 9:00 AM"
    })

# 4. ENT ([ENT])
ent_raw = [
    ("20261006", "Dr. A.S. Harugop", "Diseases of external ear & otalgia", "EN 4.1, 4.2"),
    ("20261013", "Dr. Apoorva P", "Acute otitis media & OME", "EN 4.3, 4.5"),
    ("20261027", "Dr. Prashant H. Patil", "CSOM & Cholesteatoma", "EN 4.6, 4.8"),
    ("20261103", "Dr. Akash P", "Otosclerosis & Meniere's disease", "EN 4.13, 4.20"),
    ("20261117", "Dr. Priti Hajare", "Deafness", "EN 4.12, 4.14, 4.15"),
    ("20261124", "Dr. N.R. Ankle", "Tinnitus & Evaluation of dizzy patient", "EN 4.19, 4.21"),
    ("20261201", "Dr. Vinita Metgudmath", "Facial nerve and its disorders", "EN 4.18"),
    ("20261208", "Dr. Shama Bellad", "Disorders of nasal septum", "EN 4.23"),
    ("20261215", "Dr. A.S. Harugop", "Nasal polyps", "EN 4.25"),
    ("20261222", "Dr. Shilpa Mallapur", "Allergic & vasomotor rhinitis", "EN 4.27, 4.28, PE 31.1, 31.3"),
    ("20270105", "Dr. Suprita Savadatti", "Acute & chronic Rhinosinusitis", "EN 4.29, 4.33"),
    ("20270202", "Dr. Shama Bellad", "Epistaxis & Trauma to face and neck", "EN 4.30, 4.31"),
    ("20270209", "Dr. R.B. Metgudmath", "Tumors of nose, PNS & nasopharynx", "EN 4.32, 4.34, 4.35"),
    ("20270216", "Dr. A.S. Harugop", "Disease of salivary glands", "EN 4.36"),
    ("20270223", "Dr. Gouri Lingaraddi", "Deep neck space infections", "EN 4.37, 4.41"),
    ("20270309", "Dr. Shubham Malawadi", "Vestibular schwannoma", "EN 4.21"),
    ("20270316", "Dr. Gouri Lingaraddi", "Granulomatous Diseases of Nose", "EN 2.9"),
    ("20270323", "Dr. Shubham Malawadi", "Anatomy of Oral cavity, Oropharynx & Larynx", "EN 1.1, AN 36.4, 38.1"),
    ("20270330", "Dr. Suprita Savadatti", "Pharyngitis & Adenotonsillar disease", "EN 4.26, 4.39, PE 28.1-28.3"),
    ("20270406", "Dr. Shilpa Mallapur", "Lesions of Oral cavity & Oropharynx", "EN 2.11, 4.1-4.3, 20.1"),
    ("20270427", "Dr. Apoorva P", "Acute & chronic laryngitis", "EN 4.43"),
    ("20270504", "Dr. N.R. Ankle", "Benign lesions of vocal cord", "EN 4.44"),
    ("20270511", "Dr. Priti Hajare", "Neurological disorder of larynx", "EN 4.45, AN"),
    ("20270518", "Dr. R.B. Metgudmath", "Malignancy of larynx & hypopharynx", "EN 4.46"),
    ("20270525", "Dr. Prashant H. Patil", "Stridor & Hoarseness of Voice", "EN 4.47, 4.42, CE 28.7"),
    ("20270601", "Dr. Akash P", "Airway emergencies & Tracheostomy", "EN 4.48, 2.13, 3.6, 4.5, 4.51"),
    ("20270608", "ENT Faculty", "Foreign bodies in ear, nose & throat", "EN 4.49"),
    ("20270615", "Dr. Vinita Metgudmath", "Anatomy & Physiology of Pharynx and Esophagus", "EN 1.1, 1.2"),
    ("20270622", "ENT Faculty", "Dysphagia & disorders of oesophagus", "EN 4.38, 4.52"),
    ("20270629", "Dr. Gouri Lingaraddi", "Pollution, National programmes & HIV in ENT", "EN 4.53, CM 3.1, EN 2.15")
]
for idx, (dt, fac, top, code) in enumerate(ent_raw, start=1):
    c_str = f" {code}" if code else ""
    all_gen_events.append({
        "uid": f"jnmc-ent-ph3-1-{idx}-{dt}@jnmc.edu",
        "dtstart": f"{dt}T120000",
        "dtend": f"{dt}T130000",
        "summary": f"[ENT] {fac} // {top}{c_str}",
        "location": "Anatomy Lecture Hall, JNMC Belagavi",
        "description": f"Subject: Oto-Rhino-Laryngology & HNS (ENT Theory)\nFaculty: {fac}\nTopic: {top}\nCompetency: {code}\nTime: 12:00 PM - 1:00 PM"
    })

# 5. OBG THEORY ([OBG])
obg_raw = [
    ("20261007", "Dr. Manjunath Hukkeri", "Vaginal Discharge", "OG 22.1"),
    ("20261014", "Dr. Manjunath Hukkeri", "Abortions", "OG 9.2"),
    ("20261028", "Dr. Manjunath Hukkeri", "Infertility", "OG 28.1"),
    ("20261104", "Dr. Manjunath Hukkeri", "Gestational Trophoblastic Disease", "OG 9.5"),
    ("20261111", "Dr. Manjunath Hukkeri", "Ectopic Pregnancy", "OG 9.4"),
    ("20261118", "Dr. Manjunath Hukkeri", "Multiple Pregnancy 1", "OG 11.1"),
    ("20261125", "Dr. Manjunath Hukkeri", "VIA, VILI, PAP Smear, Colposcopy", "OG 33.4"),
    ("20261202", "Dr. Manjunath Hukkeri", "Abnormal Labour 1", "OG 14.2"),
    ("20261209", "Dr. Manjunath Hukkeri", "Abnormal Labour 2", "OG 14.3"),
    ("20261216", "Dr. Manjunath Hukkeri", "Normal Puberty", "OG 23.1"),
    ("20261223", "Dr. Manjunath Hukkeri", "Primary Amenorrhea", "OG 25.1"),
    ("20270106", "Dr. Manjunath Hukkeri", "Pelvic Inflammatory Disease (PID)", "OG 27.3"),
    ("20270127", "Dr. Manjunath Hukkeri", "Abnormal Uterine Bleeding (AUB)", "OG 24.1"),
    ("20270203", "Dr. Manjunath Hukkeri", "PCOD", "OG 30.1"),
    ("20270210", "Dr. Manjunath Hukkeri", "Genital Tuberculosis", "OG 27.2"),
    ("20270217", "Dr. Farzana Begaum", "Genital Tract Infections & STDs", "OG 27.1"),
    ("20270224", "Dr. Farzana Begaum", "Preterm Labour", "OG 13.4"),
    ("20270303", "Dr. Farzana Begaum", "Premature Rupture of Membranes (PROM)", "OG 13.4"),
    ("20270310", "Dr. Farzana Begaum", "Postpartum Hemorrhage 1 (PPH 1)", "OG 16.1"),
    ("20270317", "Dr. Farzana Begaum", "Postpartum Hemorrhage 2 (PPH 2)", "OG 16.1")
]
for idx, (dt, fac, top, code) in enumerate(obg_raw, start=1):
    c_str = f" {code}" if code else ""
    all_gen_events.append({
        "uid": f"jnmc-obg-ph3-1-{idx}-{dt}@jnmc.edu",
        "dtstart": f"{dt}T080000",
        "dtend": f"{dt}T090000",
        "summary": f"[OBG] {fac} // {top}{c_str}",
        "location": "Pathology Big Hall, JNMC Belagavi",
        "description": f"Subject: Obstetrics & Gynaecology (Theory)\nFaculty: {fac}\nTopic: {top}\nCompetency: {code}\nTime: 8:00 AM - 9:00 AM"
    })

# 6. PEDIATRICS ([PEDS])
peds_raw = [
    ("20261007", "Faculty", "Revision", ""),
    ("20261014", "Dr. Supriya Patil", "Fat-soluble vitamins", "PE 12.1, 12.2, 12.4, 12.5"),
    ("20261028", "Dr Shreya Rotti", "Breast Feeding", "PE 7.1-7.8"),
    ("20261104", "Dr Reena", "Protein Energy Malnutrition", "PE 10.1-10.6"),
    ("20261111", "Dr Mrunal Kelkar", "Obesity in children", "PE 11.1-11.4"),
    ("20261125", "Dr Yashaswini", "Growth and Development", "PE 1.1-2.3"),
    ("20261202", "Dr. Mahantesh Patil", "Fluid and electrolytes in Children", "PE 15.1"),
    ("20261209", "Dr. Zeeshan Desai", "Poisoning in children", "PE 14.1-14.3"),
    ("20270203", "Dr. Roopa Bellad", "Adolescent Health", "PE 10.6"),
    ("20270210", "Dr Santosh", "Failure to thrive", "PE 2.1-2.2"),
    ("20270217", "Dr Smruthi R", "Universal Immunization Programme (UIP)", "PE 18.6-18.11, CM 10.5"),
    ("20270224", "Dr. S.M. Dhaded", "Newborn Care & Classification in Neonatology", "PE 19.1"),
    ("20270303", "Dr. Manisha Bhandankar", "Thermoregulation in Newborn", "PE 19.3, 19.9"),
    ("20270317", "Dr. Ramchandra Bhat", "Management of LBW newborns", "PE 19.8"),
    ("20270324", "Dr. Dnyanesh D K", "Childhood Asthma", "PE 28.2, 28.3"),
    ("20270331", "Dr. Tanmaya Metgud", "Shock in children", "PE 24.12, 24.14"),
    ("20270407", "Dr. Deepanjali G", "Diarrhea in Children", "PE 23.4"),
    ("20270519", "Dr. Sujata Jali", "TB in children & Adolescents", "PE 31.1-31.4"),
    ("20270526", "Dr. Smruthi R", "Chromosomal Abnormalities", "PE 29.1-29.5"),
    ("20270609", "Dr. Vineeta G", "Fever & Viral Exanthemata (Measles, Rubella, etc.)", "PE 31.10"),
    ("20270616", "Dr Shreya Patted", "Diphtheria, Pertussis, Tetanus", "PE 31.11"),
    ("20270623", "Dr. Zeeshan", "Enteric Fever", "PE 31.12")
]
for idx, (dt, fac, top, code) in enumerate(peds_raw, start=1):
    c_str = f" {code}" if code else ""
    all_gen_events.append({
        "uid": f"jnmc-peds-ph3-1-{idx}-{dt}@jnmc.edu",
        "dtstart": f"{dt}T120000",
        "dtend": f"{dt}T130000",
        "summary": f"[PEDS] {fac} // {top}{c_str}",
        "location": "Pathology Gallery Hall, JNMC Belagavi",
        "description": f"Subject: Pediatrics (Theory)\nFaculty: {fac}\nTopic: {top}\nCompetency: {code}\nTime: 12:00 PM - 1:00 PM"
    })

# 7. COMMUNITY MEDICINE ([COMED])
comm_ref_path = "/Users/shubhayu/Library/Containers/ru.keepcoder.Telegram/Data/tmp/Community_Medicine_Schedule_v3.ics"
with open(comm_ref_path, "r", encoding="utf-8") as f:
    comm_content = f.read()

vevent_matches = re.findall(r"BEGIN:VEVENT(.*?)END:VEVENT", comm_content, re.DOTALL)
for block in vevent_matches:
    uid_m = re.search(r"UID:(.+?)(?:\r?\n)", block)
    dtstart_m = re.search(r"DTSTART;TZID=Asia/Kolkata:(\d+T\d+)", block)
    dtend_m = re.search(r"DTEND;TZID=Asia/Kolkata:(\d+T\d+)", block)
    summary_m = re.search(r"SUMMARY:(.+?)(?:\r?\n)", block)
    desc_m = re.search(r"DESCRIPTION:(.+?)(?:\r?\nSTATUS|\r?\nTRANSP|\r?\nEND)", block, re.DOTALL)
    
    if uid_m and dtstart_m and dtend_m and summary_m:
        desc = desc_m.group(1).replace("\\n", "\n").strip() if desc_m else ""
        s_val = summary_m.group(1).strip()
        # Clean any existing prefixes
        s_val = re.sub(r"^Community Medicine:\s*", "", s_val)
        all_gen_events.append({
            "uid": uid_m.group(1).strip(),
            "dtstart": dtstart_m.group(1).strip(),
            "dtend": dtend_m.group(1).strip(),
            "summary": f"[COMED] {s_val}",
            "location": "Pathology Gallery Hall, JNMC Belagavi",
            "description": desc
        })

# Write updated General Schedule ICS
general_ics_path = os.path.join(DOWNLOADS_DIR, "MBBS_Phase_III_Schedule.ics")
write_master_ics(general_ics_path, "MBBS Phase III/I Schedule", "-//JNMC Belagavi//MBBS Phase III/I Schedule//EN", UNIFIED_COLOR, all_gen_events)

# ==========================================
# BATCH B ADDITIONAL SCHEDULE
# ==========================================
batch_b_events = []

# 1. Ophthalmology SDL & AETCOM ([OPTHA SDL])
ophth_b_raw = [
    ("20261006", "Refractive errors", "OP1.2", "Batch B-I: Dr. Chethana | Batch B-II: Dr. Arpita | Batch B-III: Dr. S C Bubanale"),
    ("20261027", "Allergic conjunctivitis & vernal catarrh", "OP3.4", "Batch B-I: Dr. Deepashri | Batch B-II: Dr. Anjana | Batch B-III: Dr. A L Tenagi"),
    ("20261117", "Pterygium", "OP3.5", "Batch B-I: Dr. Bhagyajyothi | Batch B-II: Dr. Mounesh | Batch B-III: Dr. Smitha K S"),
    ("20261201", "Corneal ulcer (infective Keratitis)", "OP4.3", "Batch B-I: Dr. Samyakta | Batch B-II: Dr. Daisy | Batch B-III: Dr. Rekha R Mudhol"),
    ("20261215", "Iridocyclitis", "OP6.2", "Batch B-I: Dr. Farheen | Batch B-II: Dr. Deepashri | Batch B-III: Dr. Rohini D K"),
    ("20270105", "Primary open angle glaucoma", "OP7.2", "Batch B-I: Dr. Daisy | Batch B-II: Dr. Samyakta | Batch B-III: Dr. Zarafshan"),
    ("20270209", "Cataract", "OP8.2", "Batch B-I: Dr. Anjana | Batch B-II: Dr. Farheen | Batch B-III: Dr. Rohini D K"),
    ("20270223", "Doctor-Patient Communication (Small group)", "AETCOM 3.1", "Batch B-I: Dr. Mounesh | Batch B-II: Dr. Chethana | Batch B-III: Dr. Deepashri"),
    ("20270316", "Doctor-Patient Communication (Skill lab role play)", "AETCOM 3.1", "Batch B-I: Dr. Arpita | Batch B-II: Dr. Farheen | Batch B-III: Dr. Anjana")
]
for idx, (dt, top, code, staff) in enumerate(ophth_b_raw, start=1):
    c_str = f" {code}" if code else ""
    batch_b_events.append({
        "uid": f"jnmc-ophth-batch-b-{idx}-{dt}@jnmc.edu",
        "dtstart": f"{dt}T140000",
        "dtend": f"{dt}T170000",
        "summary": f"[OPTHA SDL] Clinical Staff // {top}{c_str}",
        "location": "Dept. of Ophthalmology / Skill Lab, JNMC Belagavi",
        "description": f"Subject: Ophthalmology SDL & AETCOM (Batch B: Roll 101-202)\nTopic: {top}\nCompetency: {code}\nStaff Distribution:\n{staff}\nTime: 2:00 PM - 5:00 PM"
    })

# 2. FMT Batch B ([FMT])
fmt_b_raw = [
    ("20261013", "140000", "170000", "Dr. VVK, Dr. VB", "Medical Certificate of Cause of Death (MCCD)", "", "Dept. of FMT, JNMC Belagavi", "MCCD training for Batch B (2 PM - 5 PM). Faculty: Dr. VVK, Dr. VB."),
    ("20261015", "140000", "170000", "Dr. PSJ", "Skull Identification (SGT)", "", "Dept. of FMT, JNMC Belagavi", "Small Group Teaching (SGT): Skull Identification. Faculty: Dr. PSJ."),
    ("20261016", "140000", "170000", "Dr. PSJ", "Skeletal Remains & Identification (SGT)", "", "Dept. of FMT, JNMC Belagavi", "Small Group Teaching (SGT): Identification & Skeletal Remains. Faculty: Dr. PSJ."),
    ("20261017", "120000", "130000", "Dr. VVK", "Virginity and Defloration", "", "Dept. of FMT, JNMC Belagavi", "Lecture on Virginity and Defloration (12 PM - 1 PM). Faculty: Dr. VVK.")
]
for idx, (dt, tstart, tend, fac, top, code, loc, desc) in enumerate(fmt_b_raw, start=1):
    c_str = f" {code}" if code else ""
    batch_b_events.append({
        "uid": f"jnmc-fmt-batch-b-{idx}-{dt}@jnmc.edu",
        "dtstart": f"{dt}T{tstart}",
        "dtend": f"{dt}T{tend}",
        "summary": f"[FMT] {fac} // {top}{c_str}",
        "location": loc,
        "description": f"Subject: Forensic Medicine & Toxicology (Batch B)\n{desc}"
    })

# Write updated Batch B Schedule ICS
batch_b_ics_path = os.path.join(DOWNLOADS_DIR, "MBBS_Phase_III_Batch_B_Additional.ics")
write_master_ics(batch_b_ics_path, "MBBS Phase III/I Batch B Additional", "-//JNMC Belagavi//MBBS Phase III/I Batch B//EN", UNIFIED_COLOR, batch_b_events)

print("Regeneration complete!")
