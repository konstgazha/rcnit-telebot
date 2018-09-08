;(function(){

  function ogbu() {

  }

  function search(text) {
    if (!text.trim()) {

      return;
    } else {
      let tr = $('tbody tr'), find = false, count = 1;
      jQuery.fn.reverse = [].reverse;
      tr.reverse().each(function(i){
        let th = $('th', this);
        if (th.length) {
          if (ogbu.search.result(th.text(), text)) {
            find = true;
          }
          $(this).nextAll('tr').each(function(){
            if (+$(this).attr('rowspan')) {
              return false;
            } else if ($(this).is(':visible')) {
              count++;
            } else if (find) {
              $(this).show();
              count++;
            }
          });
          if (count > 1) {
            $(this).show();
            th.attr('rowspan', count);
          } else if (count == 1) {
            $(this).hide();
          }
          find = false;
          count = 1;
        } else {
          $('td', this).each(function(){
            if (ogbu.search.result($(this).text(), text)) {
              find = true;
              ogbu.search.draw();
            }
          });
          if (find) {
            $(this).show();
          } else {
            $(this).hide();
          }
          find = false;
        }
      });
    }
  }

  function result(str, searchStr) {
    if (str.trim().toLowerCase().search(searchStr.trim().toLowerCase()) > -1) {
      return true;
    } else {
      return false;
    }
  }

  function draw() {
    console.log('Разукрасили в %cжелтый', 'color: gold;font-weight:bold;');
  }

  search.result = result;
  search.draw = draw;

  ogbu.search = search;

  window.ogbu = ogbu;
}());
