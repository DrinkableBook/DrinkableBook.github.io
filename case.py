from datetime import datetime

class Case:
    def __init__(self, surgery_date=datetime.now(), start_time='0000', estimated_length=120,
                 inpatient=False, last_name='TestL', first_name='TestF', field='12345',
                 allergies=None, medicare=False, physician='TestPhy', surgeon='TestSur',
                 assistant_needed=True, diagnosis='', laparoscopic=True, anesthesia_type='TestAna',
                 procedure='', icd10='12345', cpt='12345', equipments=None, cardiac_comorbidity=False,
                 vascular_disease_comorbidity=False, hypertension_comorbidity=False,
                 endocrine_comorbidity=False, diabetes_comorbidity=False, respiratory_disease_comorbidity=False,
                 smoking_comorbidity=False, kidney_comorbidity=False, liver_comorbidity=False, 
                 birth_date=datetime(1989, 6, 4)):

        self.surgery_date = surgery_date if isinstance(surgery_date, datetime) else datetime.now()
        self.start_time = start_time
        self.estimated_length = estimated_length
        self.inpatient = inpatient
        self.last_name = last_name
        self.first_name = first_name
        self.field = field
        self.allergies = allergies if allergies else []
        self.medicare = medicare
        self.physician = physician
        self.surgeon = surgeon
        self.assistant_needed = assistant_needed
        self.diagnosis = diagnosis
        self.laparoscopic = laparoscopic
        self.anesthesia_type = anesthesia_type
        self.procedure = procedure
        self.icd10 = icd10
        self.cpt = cpt
        self.equipments = equipments if equipments else []
        potential_morbidities = ['Cardiac', 'Vascular Disease',
                            'Hypertension', 'Endocrine',
                            'Diabetes', 'Respiratory Disease',
                            'Smoking', 'Kidney', 'Liver']
        morbidity_determinants = [cardiac_comorbidity, vascular_disease_comorbidity,
                            hypertension_comorbidity, endocrine_comorbidity,
                            diabetes_comorbidity, respiratory_disease_comorbidity,
                            smoking_comorbidity, kidney_comorbidity, liver_comorbidity]
        self.comorbidities = [potential_morbidities[i] for i in range(len(morbidity_determinants))
                            if morbidity_determinants[i]]
        self.birth_date = birth_date if isinstance(birth_date, datetime) else datetime(1989, 6, 4)

    def display_case_details(self):
        detail = ''
        detail += f"Surgery Date: {self.surgery_date.strftime('%Y-%m-%d')}\n"
        detail += f"Start Time: {self.start_time}\n"
        detail += f"Estimated Length: {self.estimated_length} minutes\n"
        detail += f"Inpatient: {self.inpatient}\n"
        detail += f"Patient Name: {self.first_name} {self.last_name}\n"
        detail += f"Field: {self.field}\n"
        detail += f"Allergies: {', '.join(self.allergies) if self.allergies else 'None'}\n"
        detail += f"Medicare: {self.medicare}\n"
        detail += f"Physician: {self.physician}\n"
        detail += f"Surgeon: {self.surgeon}\n"
        detail += f"Assistant Needed: {self.assistant_needed}\n"
        detail += f"Diagnosis: {self.diagnosis}\n"
        detail += f"Laparoscopic: {self.laparoscopic}\n"
        detail += f"Anesthesia Type: {self.anesthesia_type}\n"
        detail += f"Procedure: {self.procedure}\n"
        detail += f"ICD-10 Code: {self.icd10}\n"
        detail += f"CPT Code: {self.cpt}\n"
        detail += f"Equipment: {', '.join(self.equipments) if self.equipments else 'None'}\n"
        detail += f"Comorbidities: {', '.join([str(comorbidity) for comorbidity in self.comorbidities])}\n"
        detail += f"Birth Date: {self.birth_date.strftime('%Y-%m-%d')}"
        return detail

