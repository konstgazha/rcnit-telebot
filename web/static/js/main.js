$('.header a').click(function() {
    $.getJSON($SCRIPT_ROOT + '/_get_org_phonebook', {
      org: $(this).text()
    }, function(data) {
      var phonebook = document.getElementById('phonebook');
      if (phonebook !== null) {
        phonebook.remove();
      }
      phonebook = document.createElement("table");
      phonebook.setAttribute("id", "phonebook");
      document.body.appendChild(phonebook);
      for (var i = data.length - 1; i >= 0; i--) {
          let dep = document.createElement("tr");
          dep.className = "departments";
          document.getElementById("phonebook").appendChild(dep);
          dep.innerHTML = data[i].dep;
          for (var j = data[i].emps.length - 1; j >= 0; j--) {
            let emp = document.createElement("tr");
            emp.className = "employees";
            document.getElementById("phonebook").appendChild(emp);
            appendTableCell(emp, "full_name", getEmployeeFullName(data[i].emps[j]));
            appendTableCell(emp, "position", data[i].emps[j].position);
            appendTableCell(emp, "phone_number", data[i].emps[j].phone_number);
          }
      }
    });
    function appendTableCell(row, className, value) {
      let cell = document.createElement("td");
      cell.className = className;
      row.appendChild(cell);
      cell.innerHTML = value;
    }
    function getEmployeeFullName(data) {
      var employee = data.name + ' ' +
                     data.surname + ' ' +
                     data.patronymic;
      return employee;
    }
});
