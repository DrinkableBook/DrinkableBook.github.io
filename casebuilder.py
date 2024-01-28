import sys
import pdfminer
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdftypes import resolve1
from datetime import datetime

def process_case_data(case_data):
  processed_case_data = {}

  for key, value in case_data.items():
    if isinstance(value, str):
      if key in ['surgery_date', 'birth_date']:
        processed_case_data[key] = datetime.strptime(value, '%Y-%m-%d')
      elif key == 'start_time':
        processed_case_data[key] = datetime.strptime(value, '%H%M').time()
      elif key in ['estimated_length', 'icd10', 'cpt']:
        processed_case_data[key] = int(value)
      elif key in ['allergies', 'equipments']:
        processed_case_data[key] = value.split(', ') if value != 'None' else []
      else:
        processed_case_data[key] = value
    elif isinstance(value, pdfminer.psparser.PSLiteral):
      boolean_value = str(value) == "/'On'" or str(value) == "/'Yes'"
      processed_case_data[key] = boolean_value

  return processed_case_data

class CaseBuilder:
  def __init__(self, filename):
    self.filename = filename
    self.field_mappings = {
      'Date of Surgery': 'surgery_date',
      'Requested Time military': 'start_time',
      'Lengthmin': 'estimated_length',
      'I PInpatient': 'inpatient',
      'Last Name': 'last_name',
      'First Name': 'first_name',
      'Social Security': 'field',
      'Allergies': 'allergies',
      'MediCare': 'medicare',
      'Primary Care Physician': 'physician',
      'Surgeon': 'surgeon',
      'Request Assistant': 'assistant_needed',
      'Textfield': 'diagnosis',
      'Laparoscopic': 'laparoscopic',
      'Anesthesia Type': 'anesthesia_type',
      'Textfield0': 'procedure',
      'ICD10': 'icd10',
      'CPT Code': 'cpt',
      'Textfield1': 'equipments',
      'Cardiac': 'cardiac_comorbidity',
      'Vascular Disease': 'vascular_disease_comorbidity',
      'Hypertension': 'hypertension_comorbidity',
      'Endocrine': 'endocrine_comorbidity',
      'Diabetes': 'diabetes_comorbidity',
      'Respiratory Disease': 'respiratory_disease_comorbidity',
      'Smoker': 'smoking_comorbidity',
      'Kidney Disease': 'kidney_comorbidity',
      'Liver Disease': 'liver_comorbidity',
      'Date of Birth': 'birth_date'
    }
    self.fields = {}

  def parse_pdf(self):
    with open(self.filename, 'rb') as fp:
      print(type(fp))
      parser = PDFParser(fp)
      doc = PDFDocument(parser)
      raw_fields = resolve1(doc.catalog['AcroForm'])['Fields']

      for i in raw_fields:
        field = resolve1(i)
        name, value = field.get('T'), field.get('V')
        if name and value:
          name = name.decode('utf-8')
          value = value.decode('utf-8') if isinstance(value, bytes) else value
          self.fields[name] = value

  def build_case(self):
    useful_fields = {}
    for long_name, short_name in self.field_mappings.items():
      if long_name in self.fields:
        useful_fields[short_name] = self.fields[long_name]
    return process_case_data(useful_fields)

