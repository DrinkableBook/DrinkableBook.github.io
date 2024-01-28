$(document).ready(function() {
  $("#datepicker").datepicker({
      minDate : 0,
      dateFormat: "mm/dd/yy",
      onSelect: function(dateText) {
          $("#selectedDate").text(dateText);
      }
  });
  $('#procedure_name').select2({});
  $('#field').select2({});
  $('#start_time').select2({});
  $('#end_time').select2({});
});

var proce_data = ['Partial ostectomy, fifth metatarsal head', 'Neurectomy, intrinsic musculature of foot', 'Lapidus bunionectomy', 'Bunionectomy with distal osteotomy', 'Arthroplasty, knee, hinge prothesis', 'Extracapsular cataract removal', 'Hysterectomy, surgical', 'Cervical biopsy', 'Vasectomy', 'Cryosurgery of the prostate gland', 'Cystourethroscopy', 'Liposuction', 'Rhinoplasty', 'Digital amputation, metatarsophalangeal joint', 'AV fistula', 'Sleeve gastrectomy', 'Laparoscopic cholecystectomy', 'Hallux rigidus correction with cheilectomy', 'Arthroscopy, knee, surgical', 'Tonsillectomy', 'Septoplasty', 'Removal of benign skin lesion', 'Adjacent tissue transfer, eyelids, nose, ears, lip', 'Tympanostomy, general anesthesia', 'Myringotomy, general anesthesia', 'Arthroplasty, hip', 'Plantar fasciotomy', 'Correction, hammertoe', 'Carpal tunnel release, open', 'Fasciotomy, palmar, open', 'ORIF, phalangeal shaft fracture', 'Flexor tendon repair'];

var selectProcedure = document.getElementById('procedure_name');

for (var i = 0; i < proce_data.length; i++){
  var option = document.createElement('option');
  option.value = proce_data[i];
  option.text = proce_data[i];
  selectProcedure.appendChild(option);
}

var field_data = ['Podiatry', 'Orthopedics', 'Ophthalmology', 'OBGYN', 'Urology', 'Plastic', 'Vascular', 'General', 'ENT', 'Pediatrics'];

var selectField = document.getElementById('field');

for (var i= 0; i < field_data.length; i++) {
  var option = document.createElement('option');
  option.value = field_data[i];
  option.text = field_data[i];
  selectField.appendChild(option);
}

const selectStartTime = document.getElementById("start_time");
const selectEndTime = document.getElementById("end_time");

function populateTimeSelect(selectElement) {
    for (let hour = 0; hour < 24; hour++) {
        for (let minute = 0; minute < 60; minute += 15) {
            const timeString = `${String(hour).padStart(2, '0')}:${String(minute).padStart(2, '0')}`;
            const option = new Option(timeString, timeString);
            selectElement.appendChild(option);
        }
    }
}

populateTimeSelect(selectStartTime);
populateTimeSelect(selectEndTime);

