$('.header a').click(function() {
    $.getJSON($SCRIPT_ROOT + '/_get_org_phonebook', {
      org: $(this).text()
    }, function(content) {
      var phonebook = document.getElementById('phonebook');
      if (phonebook !== null) {
        phonebook.remove();
      }
      phonebook = document.createElement("table");
      phonebook.setAttribute("id", "phonebook");
      document.body.appendChild(phonebook);
      createTableHead(phonebook, content.header);
      for (var i = content.data.length - 1; i >= 0; i--) {
          let dep = document.createElement("tr");
          dep.className = "departments";
          document.getElementById("phonebook").appendChild(dep);
          dep.innerHTML = content.data[i].dep;
          for (var j = content.data[i].emps.length - 1; j >= 0; j--) {
            let emp = document.createElement("tr");
            emp.className = "employees";
            document.getElementById("phonebook").appendChild(emp);
            appendTableCell(emp, "full_name", content.data[i].emps[j].full_name);
            appendTableCell(emp, "position", content.data[i].emps[j].position);
            appendTableCell(emp, "phone_number", content.data[i].emps[j].phone_number);
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
});
