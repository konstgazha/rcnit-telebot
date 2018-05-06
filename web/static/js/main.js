$('.header a').click(function(){
    $.getJSON($SCRIPT_ROOT + '/_get_org_phonebook', {
      org: $(this).text()
    }, function(data) {
      data = JSON.parse($(this).attr(data.result));
      document.getElementById("phonebook").innerHTML = data;
    });
});
