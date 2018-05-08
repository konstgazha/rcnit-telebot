$('.header a').click(function(){
    $.getJSON($SCRIPT_ROOT + '/_get_org_phonebook', {
      org: $(this).text()
    }, function(data) {
      for (var i = data.length - 1; i >= 0; i--) {
          let dep = document.createElement("div");
          document.body.appendChild(dep);
          let emps = document.createElement("div");
          document.body.appendChild(emps);
          dep.innerHTML = data[i].dep;
          for (var j = data[i].emps.length - 1; j >= 0; j--) {
            emps.innerHTML += data[i].emps[j].name + ' ' +
                             data[i].emps[j].surname + ' ' +
                             data[i].emps[j].patronymic + '<br>';
          }
      }
      
    });
});
