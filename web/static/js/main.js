$(document).ready(function(){
  $('#header button').click(function() {
    var ind = $(this).text();
    if (window.tableAjax && ind in window.tableAjax) {
      $('#phonebook').html(window.tableAjax[ind].html());
    } else {
      $.getJSON($SCRIPT_ROOT + '/_get_org_phonebook', {
        org: ind
      }, function(content) {
        $('#phonebook').remove();
        $('#main').append(phonebook = $('<table>').attr('id', 'phonebook'));
        phonebook.append($('<thead>').append(tr = $('<tr>')));
        $.each(content.header, function(){
          tr.append($('<th>').text(this));
        });
        $.each(content.data, function(i){
          let attr = {'class': 'department', 'rowspan': this.emps.length+1+''};
          phonebook.append($('<tr>').append($('<th>').attr(attr).text(this.dep)));
          $.each(this.emps, function(){
            let emps = {
              'position': this.position,
              'full_name': this.full_name,
              'phone_number': this.phone_number,
              'internal_phone_number': this.internal_phone_number,
              'email': this.email
            }, tr = $('<tr>');
            for (let key in emps) {
              tr.append(function(){
                let td = $('<span>').text(emps[key] || '');
                if (key == 'email') {
                  td = emps[key] ? $('<a>').attr('href', 'mailto: '+emps[key]).text(emps[key]) : '';
                }
                return $('<td>').attr('class', key).append(td);
              });
            }
            phonebook.append(tr);
          });
        });
        if (!window.tableAjax)
          window.tableAjax = {};
        window.tableAjax[ind] = phonebook.clone();
      });
    }
  });
  $('#header button:first-child').trigger('click');
});
