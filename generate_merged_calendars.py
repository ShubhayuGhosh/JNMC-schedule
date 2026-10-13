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

    # Sort events chronologically by dtstart
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

# Collect General Events (Roll 1-202)
all_gen_events = []

# 1. Medicine
med_raw = [
    ("20261005", "Dr. Rakesh Noubade", "GM 16.9, 16.13 Parasitic Infections- Hook + Roundworm", "Block I: Fever and Febrile Syndrome"),
    ("20261012", "Dr. Rakesh Noubade", "GM 16.3, 16.9 Tape Worm + Filariasis", "Block I: Fever and Febrile Syndrome"),
    ("20261019", "Dr. Rakesh Noubade", "GM 16.3, 16.9 Amoebiasis + Giardiasis", "Block I: Fever and Febrile Syndrome"),
    ("20261026", "Dr. Rakesh Noubade", "GM 24.1 Fat Soluble (Vit A & D)", "Block I: Nutrition and Vitamin Deficiencies"),
    ("20261102", "Dr. Rakesh Noubade", "GM 24.2 Fat Soluble (Vit E & K)", "Block I: Nutrition and Vitamin Deficiencies"),
    ("20261109", "Dr. Rakesh Noubade", "GM 24.3 Water Soluble (Vit B1, B2 & B6)", "Block I: Nutrition and Vitamin Deficiencies"),
    ("20261116", "Dr. Rakesh Noubade", "GM 24.4 Total Parental Nutrition", "Block I: Nutrition and Vitamin Deficiencies"),
    ("20261123", "Dr. Vijay Kaveri", "GM 14.1-14.5, 14.13, 14.14 Obesity", "Block I: Obesity"),
    ("20261130", "Dr. Vijay Kaveri", "GM 15.6 GERD", "Block I: GIT / Liver Disease"),
    ("20261207", "Dr. Vijay Kaveri", "GM 15.10, 15.15, 15.16 Acid Peptic Disease + H Pylori", "Block I: GIT / Liver Disease"),
    ("20261214", "Dr. Vijay Kaveri", "GM 5.1 Physiological basis of hyperbilirubinemia", "Block I: GIT / Liver Disease"),
    ("20261221", "Dr. Vijay Kaveri", "GM 5.2, 5.3 Viral Hepatitis (A+E)", "Block I: GIT / Liver Disease"),
    ("20270104", "Dr. Vijay Kaveri", "GM 5.2, 5.3 Viral Hepatitis (B+D)", "Block I: GIT / Liver Disease"),
    ("20270125", "Dr. Vijay Kaveri", "GM 5.2, 5.3, 5.5, 5.15 Hepatitis- C & HCC", "Block II"),
    ("20270201", "Dr. Vijay Kaveri", "GM 5.6 Drug Induced Liver Injury (DILI)", "Block II"),
    ("20270208", "Dr. Prashant Rathod", "GM 5.2, 5.4 Alcoholic Liver Disease (Fatty Liver + alcoholic hepatitis)", "Block II"),
    ("20270215", "Dr. Prashant Rathod", "GM 5.2, 5.6, 5.15 Cirrhosis of Liver (C/f + Etiology + Pathogenesis)", "Block II"),
    ("20270222", "Dr. Prashant Rathod", "GM 5.2, 5.15 NAFLD", "Block II"),
    ("20270301", "Dr. Prashant Rathod", "GM 5.2, 5.15 Portal Hypertension", "Block II"),
    ("20270308", "Dr. Prashant Rathod", "GM 5.5, 5.15 SBP + Hepatic Encephalopathy + Hepatorenal Syndrome", "Block II"),
    ("20270315", "Dr. Prashant Rathod", "GM 5.2, 5.8 Wilson's Disease - Hemochromatosis", "Block II"),
    ("20270322", "Dr. Prashant Rathod", "GM 5.7 Cholelithiasis + Cholecystitis", "Block II"),
    ("20270329", "Dr. Faisal Jamadar", "GM 15.1 to 15.3, 15.6, 15.8, 15.11, 15.12, 15.14 to 15.16 Upper GI Bleed", "Block II: GI Bleeding"),
    ("20270405", "Dr. Faisal Jamadar", "GM 15.1, 15.3, 15.6, 15.11, 15.16 Lower GI Bleed", "Block II: GI Bleeding"),
    ("20270426", "Dr. Faisal Jamadar", "GM 16.1, 16.2, 16.11, 16.14 Acute Diarrhea", "Block III: Diarrheal Disorders"),
    ("20270503", "Dr. Faisal Jamadar", "GM 16.2, 16.3, 16.12, 16.14 Chronic Diarrhea", "Block III: Diarrheal Disorders"),
    ("20270510", "Dr. Faisal Jamadar", "GM 16.3 MAS", "Block III: Diarrheal Disorders"),
    ("20270517", "Dr. Faisal Jamadar", "GM 16.3, 16.12 IBS", "Block III: Diarrheal Disorders"),
    ("20270524", "Dr. Faisal Jamadar", "GM 16.15, 16.16, 16.17 IBD", "Block III: Diarrheal Disorders"),
    ("20270531", "Dr. Faisal Jamadar", "Revision / MCQ", "Block III")
]
for idx, (dt, fac, top, blk) in enumerate(med_raw, start=1):
    all_gen_events.append({
        "uid": f"jnmc-gm-ph3-1-{idx}-{dt}@jnmc.edu",
        "dtstart": f"{dt}T080000",
        "dtend": f"{dt}T090000",
        "summary": f"Medicine: {fac} // {top}",
        "location": "Pathology Lecture Hall",
        "description": f"Subject: General Medicine (Theory)\nFaculty: {fac}\nTopic: {top}\nSection: {blk}\nTime: 8:00 AM - 9:00 AM"
    })

# 2. Surgery
surg_raw = [
    ("20261006", "Dr. S.I. Neeli (Urology)", "SU.29.2 AN 29.2 Congenital anomalies of genitourinary tract"),
    ("20261013", "Dr. Vikram Prabha (Urology)", "SU.29.3 Urinary tract infection"),
    ("20261027", "Dr. Vishal Kadeli (Urology)", "SU 29.5 Urolithiasis"),
    ("20261103", "Dr. R.B. Nerli (Urology)", "SU.29.6 Renal tumors"),
    ("20261117", "Dr. S.I. Neeli (Urology)", "SU 29.9 Diseases of prostate"),
    ("20261124", "Dr. Vikram Prabha (Urology)", "SU. 30.2, 30.3, 30.4, 30.5, 30.6 Testis & Scrotum AN 46.1"),
    ("20261201", "Dr. Shivagouda Patil (Urology)", "SU. 30.1 Diseases of the Penis"),
    ("20261208", "Dr. Darshan D.S. (CTVS)", "SU 26.1 Coronary artery diseases"),
    ("20261215", "Dr. Abhishek Prabhu (CTVS)", "SU 17.10 Chest Injury -1 Pneumothorax Fracture ribs"),
    ("20261222", "Dr. Pariswanath Patil (CTVS)", "SU 17.8 Chest Injury-2 Cardiac tamponade and mediastinal injury"),
    ("20270105", "Dr. Tarun Raina Ramman (CTVS)", "SU 26.1 PE23.1, 23.2 Congenital and Valvular heart diseases"),
    ("20270202", "Dr. Kiran Kurkure (CTVS)", "SU. 27.3 Peripheral arterial diseases"),
    ("20270209", "Dr. M.G. Dhorigol (Anaesthesiology)", "SU 11.1 AS 3.1 Pre-operative assessment"),
    ("20270216", "Dr. C.S. Sanikop (Anaesthesiology)", "SU 11.2 General, regional, local, spinal / epidural anesthesia AS 5.1"),
    ("20270223", "Dr. Santosh Kurbet (Pediatric Surgery)", "SU 28.10, 28.12 Congenital Anomalies Hepatobiliary system and Pancreas"),
    ("20270302", "Dr. Bharath Naik (Plastic Surgery)", "SU. 5.3 Skin grafting"),
    ("20270309", "Dr. Manoj D Togale (Surgery)", "SU. 13.1, 13.2 & 13.3 Introduction & Basic concepts of transplantation"),
    ("20270316", "Dr. Ramesh S Koujalagi (Surgery)", "SU 17.3 Mass Casualties"),
    ("20270323", "Dr. Prashant Hombal (Surgery)", "SU.17.3 Principles in Management of Musculoskeletal disorders"),
    ("20270330", "Dr. Shrishail C Metgud (Surgery)", "SU 6.1 Abdominal Tb"),
    ("20270406", "Dr. Ravi Kerur (Anesthesiology)", "SU.11.5 Pain management"),
    ("20270427", "Dr. Rahul Kenawadekar (Surgery)", "SU. 11.4 Day care surgery"),
    ("20270504", "Dr. Swapnil Pattanshetti (Pediatric Surgery)", "SU. 28.16 Anorectal anomalies"),
    ("20270511", "Dr. Santosh Kurbet (Pediatric Surgery)", "SU. 28.14 Congenital anomalies of GIT"),
    ("20270518", "Dr. Prakash Mahantshetti (Neuro-Surgery)", "SU. 17.6 EDH, SDH, SAH"),
    ("20270525", "Dr. S.I. Neeli (Urology)", "SU 29.1 PE21.4 Introduction & Investigation of Urological"),
    ("20270601", "Dr. Vikram Prabha (Urology)", "SU 29.1 PE21.4 Hematuria"),
    ("20270608", "Dr. Swapnil Pattanshetti (Pediatric Surgery)", "SU. 28.14 Pediatrics intestinal obstruction")
]
for idx, (dt, fac, top) in enumerate(surg_raw, start=1):
    all_gen_events.append({
        "uid": f"jnmc-surg-ph3-1-{idx}-{dt}@jnmc.edu",
        "dtstart": f"{dt}T080000",
        "dtend": f"{dt}T090000",
        "summary": f"Surgery: {fac} // {top}",
        "location": "Pathology Lecture Hall",
        "description": f"Subject: General Surgery (Theory)\nFaculty: {fac}\nTopic: {top}\nTime: 8:00 AM - 9:00 AM"
    })

# 3. ENT
ent_raw = [
    ("20261006", "Dr. A.S. Harugop", "EN 4.1, 4.2 Diseases of external ear/otalgia"),
    ("20261013", "Dr. Apoorva P", "EN 4.3, 4.5 Acute otitis media /otitis media with effusion"),
    ("20261027", "Dr. Prashant H. Patil", "EN 4.6, 4.8 Chronic suppurative otitis media and Cholesteatoma"),
    ("20261103", "Dr. Akash P", "EN 4.13, 4.20 Otosclerosis/ vestibular disorder including Meniere's disease"),
    ("20261117", "Dr. Priti Hajare", "EN 4.12, 4.14, 4.15/ IM/ PY Deafness"),
    ("20261124", "Dr. N.R. Ankle", "EN 4.19, 4.21 Tinnitus/evaluation of dizzy patient"),
    ("20261201", "Dr. Vinita Metgudmath", "EN 4.18 Facial nerve and its disorders"),
    ("20261208", "Dr. Shama Bellad", "EN 4.23 Disorders of nasal septum"),
    ("20261215", "Dr. A.S. Harugop", "EN 4.25 Nasal polyps"),
    ("20261222", "Dr. Shilpa Mallapur", "EN 4.27, 4.28, PE 31.1, 31.3 Allergic and vasomotor rhinitis/ atopic dermatitis"),
    ("20270105", "Dr. Suprita Savadatti", "EN 4.29, 4.33 Acute and chronic Rhinosinusitis"),
    ("20270202", "Dr. Shama Bellad", "EN 4.30, 4.31 Epistaxis/trauma to face and neck"),
    ("20270209", "Dr. R.B. Metgudmath", "EN 4.32, 4.34, 4.35 Tumors of nose & PNS, nasopharynx"),
    ("20270216", "Dr. A.S. Harugop", "EN 4.36 Disease of salivary glands"),
    ("20270223", "Dr. Gouri Lingaraddi", "EN 4.37, 4.41 Deep neck space infections"),
    ("20270309", "Dr. Shubham Malawadi", "EN 4.21 Vestibular schwannoma"),
    ("20270316", "Dr. Gouri Lingaraddi", "EN 2.9 Granulomatous Diseases of Nose"),
    ("20270323", "Dr. Shubham Malawadi", "EN 1.1 AN 36.4, 38.1 Anatomy of Oral cavity, Oropharynx, larynx"),
    ("20270330", "Dr. Suprita Savadatti", "EN 4.26, 4.39, PE 28.1, 28.2, 28.3 Pharyngitis and Adenotonsillar disease"),
    ("20270406", "Dr. Shilpa Mallapur", "EN 2.11, 4.1, 4.2, 4.3 20.1 Benign and Malignant lesions of Oral cavity and Oropharynx"),
    ("20270427", "Dr. Apoorva P", "EN 4.43 Acute and chronic laryngitis"),
    ("20270504", "Dr. N.R. Ankle", "EN 4.44 Benign lesions of vocal cord"),
    ("20270511", "Dr. Priti Hajare", "EN 4.45/ AN Neurological disorder of larynx"),
    ("20270518", "Dr. R.B. Metgudmath", "EN 4.46 Malignancy of larynx and hypopharynx"),
    ("20270525", "Dr. Prashant H. Patil", "EN 4.47, 4.42 CE 28.7 Stridor, Evaluation of Hoarseness of Voice"),
    ("20270601", "Dr. Akash P", "EN 4.48, 2.13, 3.6, 4.5, 4.51 Airway emergencies, Tracheostomy, other airway management"),
    ("20270608", "ENT Faculty", "EN 4.49 Foreign bodies in ear, nose and throat"),
    ("20270615", "Dr. Vinita Metgudmath", "EN 1.1, 1.2 Anatomy of pharynx, Esophagus and Physiology of esophagus"),
    ("20270622", "ENT Faculty", "EN 4.38, 4.52 Dysphagia/disorders of oesophagus"),
    ("20270629", "Dr. Gouri Lingaraddi", "EN 4.53, CM 3.1, EN 2.15 Health hazards of pollution/ national programme in ENT / HIV in ENT")
]
for idx, (dt, fac, top) in enumerate(ent_raw, start=1):
    all_gen_events.append({
        "uid": f"jnmc-ent-ph3-1-{idx}-{dt}@jnmc.edu",
        "dtstart": f"{dt}T120000",
        "dtend": f"{dt}T130000",
        "summary": f"ENT: {fac} // {top}",
        "location": "Anatomy Lecture Hall",
        "description": f"Subject: Oto-Rhino-Laryngology & HNS (ENT Theory)\nFaculty: {fac}\nTopic: {top}\nTime: 12:00 PM - 1:00 PM"
    })

# 4. OBG Theory
obg_raw = [
    ("20261007", "Dr. Manjunath Hukkeri", "OG 22.1 -Vaginal Discharge"),
    ("20261014", "Dr. Manjunath Hukkeri", "OG 9.2 -Abortions"),
    ("20261028", "Dr. Manjunath Hukkeri", "OG 28.1- Infertility"),
    ("20261104", "Dr. Manjunath Hukkeri", "OG 9.5 - Gestational Trophoblastic Disease"),
    ("20261111", "Dr. Manjunath Hukkeri", "OG 9.4 -Ectopic Pregnancy"),
    ("20261118", "Dr. Manjunath Hukkeri", "OG 11.1-Multiple Pregnancy 1"),
    ("20261125", "Dr. Manjunath Hukkeri", "OG 33.4 -VIA, VILI, PAP Smear, Colposcopy"),
    ("20261202", "Dr. Manjunath Hukkeri", "OG 14.2-Abnormal Labour 1"),
    ("20261209", "Dr. Manjunath Hukkeri", "OG 14.3 -Abnormal Labour 2"),
    ("20261216", "Dr. Manjunath Hukkeri", "OG 23.1 -Normal Puberty"),
    ("20261223", "Dr. Manjunath Hukkeri", "OG 25.1 -Primary Amenorrhea"),
    ("20270106", "Dr. Manjunath Hukkeri", "OG 27.3 -PID"),
    ("20270127", "Dr. Manjunath Hukkeri", "OG 24.1 -AUB"),
    ("20270203", "Dr. Manjunath Hukkeri", "OG 30.1 -PCOD"),
    ("20270210", "Dr. Manjunath Hukkeri", "OG 27.2 -Genital TB"),
    ("20270217", "Dr. Farzana Begaum", "OG 27.1-Infection of Genital Tract and STD"),
    ("20270224", "Dr. Farzana Begaum", "OG 13.4 -Preterm Labour"),
    ("20270303", "Dr. Farzana Begaum", "OG 13.4 -PROM"),
    ("20270310", "Dr. Farzana Begaum", "OG 16.1 -PPH 1"),
    ("20270317", "Dr. Farzana Begaum", "OG 16.1 -PPH 2")
]
for idx, (dt, fac, top) in enumerate(obg_raw, start=1):
    all_gen_events.append({
        "uid": f"jnmc-obg-ph3-1-{idx}-{dt}@jnmc.edu",
        "dtstart": f"{dt}T080000",
        "dtend": f"{dt}T090000",
        "summary": f"OBG: {fac} // {top}",
        "location": "Pathology Lecture Hall",
        "description": f"Subject: Obstetrics & Gynaecology (Theory)\nFaculty: {fac}\nTopic: {top}\nTime: 8:00 AM - 9:00 AM"
    })

# 5. Pediatrics
peds_raw = [
    ("20261007", "Faculty", "Revision"),
    ("20261014", "Dr. Supriya Patil", "PE 12.1, 12.2, 12.4, 12.5 Fat-soluble vitamins"),
    ("20261028", "Dr Shreya Rotti", "PE 7.1 to 7.8 Breast Feeding"),
    ("20261104", "Dr Reena", "PE 10.1 - 10.6 Protein Energy Malnutrition"),
    ("20261111", "Dr Mrunal Kelkar", "PE 11.1-11.4 Obesity in children"),
    ("20261125", "Dr Yashaswini", "PE 1.1-2.3 Growth and Development"),
    ("20261202", "Dr. Mahantesh Patil", "PE 15.1 Fluid and electrolytes in Children"),
    ("20261209", "Dr. Zeeshan Desai", "PE 14.1-14.3 Poisoning in children"),
    ("20270203", "Dr. Roopa Bellad", "PE 10.6 Adolescent Health"),
    ("20270210", "Dr Santosh", "PE 2.1-2.2 Failure to thrive"),
    ("20270217", "Dr Smruthi R", "PE 18.6-18.11, CM 10.5 UIP"),
    ("20270224", "Dr. S.M. Dhaded", "PE 19.1 Normal new born care Nomenclature & Classification in Neonatology"),
    ("20270303", "Dr. Manisha Bhandankar", "PE 19.3, 19.9 Thermoregulation in New-born"),
    ("20270317", "Dr. Ramchandra Bhat", "PE 19.8 Management of LBW newborns"),
    ("20270324", "Dr. Dnyanesh D K", "PE 28.2, 28.3 Childhood Asthma"),
    ("20270331", "Dr. Tanmaya Metgud", "PE 24.12, 24.14 Shock in children"),
    ("20270407", "Dr. Deepanjali G", "PE 23.4 Diarrhea in Children"),
    ("20270519", "Dr. Sujata Jali", "PE 31.1-31.4 TB in children & Adolescents"),
    ("20270526", "Dr. Smruthi R", "PE 29.1-29.5 Chromosomal Abnormalities"),
    ("20270609", "Dr. Vineeta G", "PE 31.10 Fever in children Viral Exanthemata's illness (Measles, Mumps, Rubella, Chickenpox)"),
    ("20270616", "Dr Shreya Patted", "PE 31.11 Diphtheria, Pertussis, Tetanus"),
    ("20270623", "Dr. Zeeshan", "PE 31.12 Enteric Fever")
]
for idx, (dt, fac, top) in enumerate(peds_raw, start=1):
    all_gen_events.append({
        "uid": f"jnmc-peds-ph3-1-{idx}-{dt}@jnmc.edu",
        "dtstart": f"{dt}T120000",
        "dtend": f"{dt}T130000",
        "summary": f"Pediatrics: {fac} // {top}",
        "location": "Pathology Lecture Hall",
        "description": f"Subject: Pediatrics (Theory)\nFaculty: {fac}\nTopic: {top}\nTime: 12:00 PM - 1:00 PM"
    })

# 6. Ophthalmology Theory
ophth_raw = [
    ("20261008", "Dr. Arpita G", "OP1.1 Anatomy of Eye & Physiology of Vision"),
    ("20261015", "Dr. Daisy V", "Refraction - OP1.2, OP1.4, OP1.5 Refractive errors, Refractive surgeries, Amblyopia"),
    ("20261022", "Dr. Rohini D K", "Lids - OP2.1 Lids & its Anomalies"),
    ("20261029", "Dr. Rohini D K", "Lacrimal Apparatus - OP 2.2 Congenital & Acquired dacryocystitis"),
    ("20261105", "Dr. Bhagyajyothi B K", "Orbit - OP2.6, OP2.3, OP2.4 Proptosis, Thyroid eye disease, Orbital cellulitis"),
    ("20261112", "Dr. Bhagyajyothi B K", "Orbit - OP2.5, OP2.7, OP2.8 Cavernous sinus thrombosis, Orbital Tumours"),
    ("20261119", "Dr. Samyakta S", "Conjunctiva - OP3.3, OP3.4 Trachoma, Allergic conjunctivitis, Vernal catarrh"),
    ("20261126", "Dr. S C Bubanale", "Cornea - OP4.1, OP4.2 Anatomy and Physiology of Cornea, Congenital anomalies & inflammations"),
    ("20261203", "Dr. S C Bubanale", "Cornea - OP4.3 Infective keratitis"),
    ("20261210", "Dr. Samyakta S", "Cornea - OP4.4, OP4.6, OP4.7 Corneal opacity, Corneal blindness, Keratoplasty"),
    ("20261217", "Dr. Daisy V", "OP4.5, OP10.4 Dry eyes, Vitamin A deficiency"),
    ("20270107", "Dr. Chethana W", "Uvea - OP6.1, OP6.2 Classification & Clinical features, investigations and treatment of Uveitis"),
    ("20270128", "Dr. Chethana W", "Uvea - OP6.4 Systemic conditions associated with Uveitis"),
    ("20270204", "Dr. Rekha R Mudhol", "Glaucoma - OP7.1, OP7.2 Congenital glaucoma, Primary open angle glaucoma"),
    ("20270211", "Dr. Rekha R Mudhol", "Glaucoma - OP7.3 Primary angle closure glaucoma"),
    ("20270218", "Dr. Farheen", "Glaucoma - OP 7.4 Secondary glaucoma"),
    ("20270225", "Dr. A L Tenagi", "Lens - OP8.1, OP8.2 Anatomy of lens & Senile cataract"),
    ("20270304", "Dr. A L Tenagi", "Lens - OP8.4 Cataract surgery"),
    ("20270311", "Dr. Mounesh P", "Retina - OP9.1 Anatomy of Normal Retina. Direct and indirect Ophthalmoscopy"),
    ("20270318", "Dr. Deepashri M", "Retina - OP 9.2 Diabetic Retinopathy"),
    ("20270325", "Dr. Deepashri M", "Retina - OP9.3 Vascular occlusions of retina"),
    ("20270401", "Dr. Mounesh P", "Retina - OP9.4 Hypertensive retinopathy & other retinal diseases"),
    ("20270408", "Dr. Zarafshan J", "Optic nerve - OP9.5 Diseases of the optic nerve"),
    ("20270429", "Dr. Farheen M", "Optic nerve - OP9.5 Diseases of the visual pathway"),
    ("20270506", "Dr. Smitha K. S.", "Strabismus - OP 10.1 Anatomy of Intraocular & Extraocular Muscles & Binocular single vision"),
    ("20270513", "Dr. Smitha K. S.", "Strabismus - OP10.2 Types & methods of diagnosis of Heterotropia/ Strabismus"),
    ("20270520", "Dr. Anjanabai O", "OP10.5 Enucleation, evisceration and exenteration"),
    ("20270527", "Dr. Anjanabai O", "OP10.6 Ocular injuries"),
    ("20270603", "Dr. Arpita G", "OP10.7 NPCB, Vision 2020"),
    ("20270610", "Dr. Zarafshan J", "Ocular Pharmacology")
]
for idx, (dt, fac, top) in enumerate(ophth_raw, start=1):
    all_gen_events.append({
        "uid": f"jnmc-ophth-ph3-1-{idx}-{dt}@jnmc.edu",
        "dtstart": f"{dt}T120000",
        "dtend": f"{dt}T130000",
        "summary": f"Ophthalmology: {fac} // {top}",
        "location": "",
        "description": f"Subject: Ophthalmology (Theory)\nFaculty: {fac}\nTopic: {top}\nTime: 12:00 PM - 1:00 PM"
    })

# 7. Community Medicine
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
        if not s_val.startswith("Community Medicine:"):
            s_val = f"Community Medicine: {s_val}"
        all_gen_events.append({
            "uid": uid_m.group(1).strip(),
            "dtstart": dtstart_m.group(1).strip(),
            "dtend": dtend_m.group(1).strip(),
            "summary": s_val,
            "location": "Pathology Lecture Hall",
            "description": desc
        })

# Write the single General Schedule ICS file
general_ics_path = os.path.join(DOWNLOADS_DIR, "MBBS_Phase_III_Schedule.ics")
write_master_ics(general_ics_path, "MBBS Phase III Schedule", "-//JNMC Belagavi//MBBS Phase III Schedule//EN", UNIFIED_COLOR, all_gen_events)

# Collect Batch B Additional Events
batch_b_events = []

# 1. Ophthalmology SDL & AETCOM (Batch B)
ophth_b_raw = [
    ("20261006", "OP1.2 Refractive errors", "Batch B-I: Dr. Chethana | Batch B-II: Dr. Arpita | Batch B-III: Dr. S C Bubanale"),
    ("20261027", "OP3.4 Allergic conjunctivitis & vernal catarrh", "Batch B-I: Dr. Deepashri | Batch B-II: Dr. Anjana | Batch B-III: Dr. A L Tenagi"),
    ("20261117", "OP3.5 Pterygium", "Batch B-I: Dr. Bhagyajyothi | Batch B-II: Dr. Mounesh | Batch B-III: Dr. Smitha K S"),
    ("20261201", "OP4.3 Corneal ulcer (infective Keratitis)", "Batch B-I: Dr. Samyakta | Batch B-II: Dr. Daisy | Batch B-III: Dr. Rekha R Mudhol"),
    ("20261215", "OP6.2 Iridocyclitis", "Batch B-I: Dr. Farheen | Batch B-II: Dr. Deepashri | Batch B-III: Dr. Rohini D K"),
    ("20270105", "OP7.2 Primary open angle glaucoma", "Batch B-I: Dr. Daisy | Batch B-II: Dr. Samyakta | Batch B-III: Dr. Zarafshan"),
    ("20270209", "OP8.2 Cataract", "Batch B-I: Dr. Anjana | Batch B-II: Dr. Farheen | Batch B-III: Dr. Rohini D K"),
    ("20270223", "AETCOM: 3.1 Doctor-Patient Communication (Intro & Small group)", "Batch B-I: Dr. Mounesh | Batch B-II: Dr. Chethana | Batch B-III: Dr. Deepashri"),
    ("20270316", "AETCOM: 3.1 Doctor-Patient Communication (Skill lab role play & Assessment)", "Batch B-I: Dr. Arpita | Batch B-II: Dr. Farheen | Batch B-III: Dr. Anjana")
]
for idx, (dt, top, staff) in enumerate(ophth_b_raw, start=1):
    batch_b_events.append({
        "uid": f"jnmc-ophth-batch-b-{idx}-{dt}@jnmc.edu",
        "dtstart": f"{dt}T140000",
        "dtend": f"{dt}T170000",
        "summary": f"Ophthal SDL/AETCOM (Batch B) // {top}",
        "location": "Dept. of Ophthalmology / Skill Lab",
        "description": f"Subject: Ophthalmology SDL & AETCOM (Batch B: Roll 101-202)\nTopic: {top}\nStaff Distribution:\n{staff}\nTime: 2:00 PM - 5:00 PM"
    })

# 2. FMT Batch B
fmt_b_raw = [
    ("20261013", "140000", "170000", "FMT: Dr. VVK, Dr. VB // MCCD (Batch-B)", "Dept. of FMT", "Medical Certificate of Cause of Death (MCCD) for Batch B (2 PM - 5 PM). Faculty: Dr. VVK, Dr. VB."),
    ("20261015", "140000", "170000", "FMT: Dr. PSJ // SGT: Skull Identification", "Dept. of FMT", "Small Group Teaching (SGT): Skull Identification. Faculty: Dr. PSJ."),
    ("20261016", "140000", "170000", "FMT: Dr. PSJ // SGT: Identification / Skeletal Remains", "Dept. of FMT", "Small Group Teaching (SGT): Identification & Skeletal Remains. Faculty: Dr. PSJ."),
    ("20261017", "120000", "130000", "FMT: Dr. VVK // Virginity and Defloration", "Dept. of FMT", "Lecture on Virginity and Defloration (12 PM - 1 PM). Faculty: Dr. VVK.")
]
for idx, (dt, tstart, tend, summ, loc, desc) in enumerate(fmt_b_raw, start=1):
    batch_b_events.append({
        "uid": f"jnmc-fmt-batch-b-{idx}-{dt}@jnmc.edu",
        "dtstart": f"{dt}T{tstart}",
        "dtend": f"{dt}T{tend}",
        "summary": summ,
        "location": loc,
        "description": f"Subject: Forensic Medicine & Toxicology (Batch B)\n{desc}"
    })

# Write the single Batch B Additional Schedule ICS file
batch_b_ics_path = os.path.join(DOWNLOADS_DIR, "MBBS_Phase_III_Batch_B_Additional.ics")
write_master_ics(batch_b_ics_path, "MBBS Phase III Batch B Additional", "-//JNMC Belagavi//MBBS Phase III Batch B//EN", UNIFIED_COLOR, batch_b_events)

print("Done generating merged ICS files.")
