$('#header button').click(function() {
    $.getJSON($SCRIPT_ROOT + '/_get_org_phonebook', {
      org: $(this).text()
    }, function(content) {
      var phonebook = document.getElementById('phonebook');
      if (phonebook !== null) {
        phonebook.remove();
      }
      phonebook = document.createElement("table");
      phonebook.setAttribute("id", "phonebook");
      document.getElementById("main").appendChild(phonebook);
      createTableHead(phonebook, content.header);
      for (var i = content.data.length - 1; i >= 0; i--) {
          let depAdded = false;
          let empNumber = content.data[i].emps.length;
          for (var j = empNumber - 1; j >= 0; j--) {
            let row = document.createElement("tr");
            if (depAdded != true) {
              appendDepartment(row, content.data[i].dep, empNumber);
              depAdded = true;
            }
            document.getElementById("phonebook").appendChild(row);
            let mailto = '<a href=mailto:"' + content.data[i].emps[j].email +'">' + content.data[i].emps[j].email + '</a>';
            appendTableCell(row, "full_name", content.data[i].emps[j].full_name);
            appendTableCell(row, "phone_number", content.data[i].emps[j].phone_number);
            appendTableCell(row, "internal_phone_number", content.data[i].emps[j].internal_phone_number);
            appendTableCell(row, "email", mailto);
            appendTableCell(row, "position", content.data[i].emps[j].position);
          }
      }
    });
    function createTableHead(table, header) {
      console.log('tada');  
      let thead = document.createElement("thead");
      let tr = document.createElement("tr");
      thead.appendChild(tr);
      table.appendChild(thead);
      for (var i = 0; i <= header.length - 1; i++) {
        let th = document.createElement("th");
        th.innerHTML = header[i];
        tr.appendChild(th);
      }
    }
    function appendTableCell(row, className, value) {
      let cell = document.createElement("td");
      cell.className = className;
      row.appendChild(cell);
      cell.innerHTML = value;
    }
    function appendDepartment(row, department, rowspan) {
      let dep = document.createElement("th");
      dep.className = "department";
      dep.setAttribute("rowspan", rowspan)//content.data[i].emps.length)
      //document.getElementById("phonebook").appendChild(dep);
      row.appendChild(dep);
      dep.innerHTML = department; //content.data[i].dep;
    }
});
