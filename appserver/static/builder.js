function s2ab(s) {
  var buf = new ArrayBuffer(s.length);
  var view = new Uint8Array(buf);
  for (var i=0; i!=s.length; ++i) view[i] = s.charCodeAt(i) & 0xFF;
  return buf;
}

function objectifyForm (formArray) {
  // serialize data function

  var returnArray = {}
  for (var i = 0; i < formArray.length; i++) {
    if (formArray[i]['type'] == 'submit') {
      continue
    }
    returnArray[formArray[i]['name']] = formArray[i]['value']
  }
  return returnArray
}

require([
  'underscore',
  'jquery',
  'splunkjs/mvc',
  'splunkjs/mvc/tableview',
  'splunkjs/mvc/simplexml/ready!'
], function (_, $, mvc, TableView) {
  var service = mvc.createService()

  // $('#merge_document').on('click', function () {
  //   console.log('clicked merge document!')
  // })

  var theForm = $('#the_form')

  theForm.submit(function (event) {
    event.preventDefault()

    var tasks = $('#tasks table').tableToJSON()
    var issues = $('#issues table').tableToJSON()
    var recommendations = $('#recommendations table').tableToJSON()
    var schedule = $('#schedule table').tableToJSON()
    var contacts = $('#contacts table').tableToJSON()

    var data = {}

    $(".report").each(function(item, index) {
      data[this.id] = this.innerHTML
    })

    data["merge_rows"] = []
    data["merge_rows"].push({"task_dates": tasks })
    data["merge_rows"].push({"issue_status": issues })
    data["merge_rows"].push({"recommendation_item": recommendations })
    data["merge_rows"].push({"project_week": schedule })
    data["merge_rows"].push({"contact_name": contacts })
    data["merge_rows"] = JSON.stringify(data["merge_rows"])

    service.post('/services/merge_document', data, function (err, response) {
      if (err) {
        console.log('error: ', err)
      } else if (response.status === 200) {
        console.log('response 200 ')

        var blob = new Blob([s2ab(atob(response.data))], {
          type: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        });

        var link=document.createElement('a');
        link.href=window.URL.createObjectURL(blob);

        link.download="output.docx";
        link.click();

      }
    })
  })

})
