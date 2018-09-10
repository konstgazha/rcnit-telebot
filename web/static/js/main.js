$(document).ready(function(){
  $('#header button').click(function() {
    var ind = $(this).text().trim();
    $('#phonebook').remove();
    if (window.tableAjax && ind in window.tableAjax) {
      $('#main').append($(window.tableAjax[ind]));
    } else {
      $.getJSON($SCRIPT_ROOT + '/_get_org_phonebook', {
        org: ind
      }, function(content) {
        window.content = content;
        $('#main').append(phonebook = $('<table>').attr('id', 'phonebook'));
        phonebook.append($('<thead>').append(tr = $('<tr>'))).append($('<tbody>'));
        phonebook = $('tbody');
        $.each(content.header, function(){
          tr.append($('<th>').text(this));
        });
        $.each(content.data, function(){
          var dep = this.dep;
          let attr = {'class': 'department', 'rowspan': this.emps.length}, firstRow = true;
          phonebook.append(tr = $('<tr>').attr('dep', dep).append($('<td>').attr(attr).append($('<span>').text(dep))));
          $.each(this.emps, function(){
            let emps = {
              'position': this.position,
              'full_name': this.full_name,
              'phone_number': this.phone_number,
              'internal_phone_number': this.internal_phone_number,
              'email': this.email
            };
            if (!firstRow) {
              tr = $('<tr>').attr('dep', dep);
              phonebook.append(tr);
            }
            for (let key in emps) {
              $(tr).append(function(){
                let span = $('<span>').text(emps[key] || '');
                if (key == 'email') {
                  span = emps[key] ? $('<a>').attr('href', 'mailto: '+emps[key]).text(emps[key]) : '';
                }
                return $('<td>').attr('class', key).append(span);
              });
            }
            firstRow = false;
          });
        });
        if (!window.tableAjax)
          window.tableAjax = {};
        window.tableAjax[ind] = phonebook.parent().clone();
      });
    }
  });
  $('#header button:first-child').trigger('click');
});
