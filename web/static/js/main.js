$('.header a').click(function(){
    $.getJSON($SCRIPT_ROOT + '/_get_org_phonebook', {
      org: $(this).text()
    }, function(data) {
      let deps = []
      for (var i = data.length - 1; i >= 0; i--) {
          deps += data[i].dep + ' ';
      }
      document.getElementById("phonebook").innerHTML = deps;
    });
});
