import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
from scheduler import Schedule
from casebuilder import CaseBuilder
from case import Case
from scheduler_ai import predict_time

app = Flask(__name__, '/static')


def format_time(case):
  surgery_date, start_time, original_length = str(case.surgery_date), case.start_time, case.estimated_length
  
  estimated_length = int(predict_time(int(case.cpt), int(original_length), case.field, case.procedure))

  est_diff = abs(estimated_length - original_length)

  date_str = surgery_date.split()[0]
  start_hour, start_minute = divmod(start_time.hour * 60 + start_time.minute, 60)
  end_hour, end_minute = divmod(start_hour * 60 + start_minute + estimated_length, 60)
  start_time_str = f"{date_str}T{start_hour:02d}:{start_minute:02d}:00-08:00"
  end_time_str = f"{date_str}T{end_hour:02d}:{end_minute:02d}:00-08:00"
  return start_time_str, end_time_str, est_diff


def convert_to_google_datetime(date_str, start_time_str, end_time_str):
  date = datetime.strptime(date_str, "%m/%d/%Y")
  start_time = date.replace(hour=int(start_time_str.split(':')[0]),
                            minute=int(start_time_str.split(':')[1]))
  end_time = date.replace(hour=int(end_time_str.split(':')[0]),
                          minute=int(end_time_str.split(':')[1]))
  return start_time.strftime(
      "%Y-%m-%dT%H:%M:%S%z") + "-08:00", end_time.strftime(
          "%Y-%m-%dT%H:%M:%S%z") + "-08:00"


def add_new_operation(rm, pn, fd, cpt, diag, icd, phy, dt, st, et):
  stt, edt = convert_to_google_datetime(dt, st, et)
  scheduler.add_medical_event(calendar_name=rm,
                              procedure_name=pn,
                              field=fd,
                              cpt_code=cpt,
                              diagnosis=diag,
                              icd10_code=icd,
                              physician=phy,
                              start_time=stt,
                              end_time=edt)


@app.route('/')
def home():
  return render_template('main.html')

UPLOAD_FOLDER = r'/Users/Xingjian/Desktop/ORACLE/temp_data'
ALLOWED_EXTENSIONS = {'pdf'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/pdfupload', methods=['GET', 'POST'])
def pdfupload():
  if request.method == 'POST':
    pdf = request.files
    o_r = request.form.get('or')

    file = request.files['pdf']
    filename = file.filename
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))

    # We do the pdf -> google calendar tricks here.
    case_builder = CaseBuilder('temp_data/form.pdf')
    case_builder.parse_pdf()
    case_data = case_builder.build_case()

    case = Case(**case_data)
    description = case.display_case_details()

    scheduler = Schedule()
    start_time, end_time, est_diff = format_time(case)

    scheduler.add_medical_event(
      o_r,
      case.procedure,
      case.field,
      case.cpt,
      case.diagnosis,
      case.icd10,
      case.surgeon,
      start_time,
      end_time,
      case.equipments,
      case.comorbidities,
      case.anesthesia_type,
      description,
      est_diff
    )

    result = [o_r,
        case.procedure,
        case.field,
        case.cpt,
        case.diagnosis,
        case.icd10,
        case.surgeon,
        start_time,
        end_time,
        case.equipments,
        case.comorbidities,
        case.anesthesia_type,
        description,
        est_diff
    ]


    return redirect(url_for('success'))
  return render_template('pdfupload.html')

@app.route('/pdfresults', methods=['GET', 'POST'])
def pdfresults(result):
  if request.method == 'POST':
    scheduler = Schedule()
    scheduler.add_medical_event(*result)
    return redirect(url_for('/success'))
  return render_template('pdfresults.html', result)


@app.route('/manual', methods=['GET', 'POST'])
def manual():
  if request.method == 'POST':
    procedure_name = request.form.get('procedure_name')
    field = request.form.get('field')
    o_r = request.form.get('or')
    diagnosis = request.form.get('diagnosis')
    icd10_code = request.form.get('icd10_code')
    physician = request.form.get('physician')
    date = request.form.get('date')
    start_time = request.form.get('start_time')
    end_time = request.form.get('end_time')
    # We add the new operation here.
    add_new_operation(o_r, procedure_name, field, '12323', diagnosis, icd10_code, physician, date, start_time, end_time)
    
    return redirect(url_for('success'))
  return render_template('manual.html')

@app.route('/success')
def success():
  return render_template('success.html')

if __name__ == '__main__':
  scheduler = Schedule()
  app.run(host='0.0.0.0', debug=True, port=8080)

