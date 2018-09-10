;(function(){

  function ogbu() {

  }

  function search(text) {
    let arr = [null, false];
    let tr = $('tbody tr');
    tr.each(function(i){
      var dep = $(this).attr('dep');
      if (!arr[0]) {
        arr[0] = dep;
      } else if (arr[0] != dep || i == tr.length-1) {
        let depList = '[dep="'+arr[0]+'"]';
        if (ogbu.search.result(arr[0], text)) {
          $(depList).show();
        }
        depList = $(depList+':visible');
        let attr = {'class': 'department', 'rowspan': depList.length};
        $('[dep="'+arr[0]+'"] .department').remove();
        $(depList[0]).prepend($('<td>').attr(attr).text(arr[0]));
        arr[0] = null;
      }
      $('td', this).each(function(){
        if (ogbu.search.result($(this).text(), text)) {
          arr[1] = true;
          ogbu.search.draw();
        } else {
          ogbu.search.drawClear();
        }
      });
      if (arr[1]) {
        $(this).show();
        arr[1] = false;
      } else {
        $(this).hide();
      }
    });
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

  function drawClear() {
    console.log('Убираем выделение');
  }

  search.result = result;
  search.draw = draw;
  search.drawClear = drawClear;

  ogbu.search = search;

  window.ogbu = ogbu;
}());
