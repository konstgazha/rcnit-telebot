;(function(){

  jQuery.expr[":"].Contains = jQuery.expr.createPseudo(function(arg) {
    return function( elem ) {
      return jQuery(elem).text().toLowerCase().indexOf(arg.toLowerCase()) >= 0;
    };
  });

  function ogbu() {

  }

  function search(str) {
    let elems = $('tr:Contains("'+str+'")').show();
    $('tbody tr:not(:Contains("'+str+'"))').hide();
    $('.department').remove();
    ogbu.eachFind(elems, str);
  }

  function eachFind(e, s) {
    let dep;
    ogbu.clearMark($('.mark').parent());
    e.each(function(){
      let tempDep = $(this).attr('dep');
      if (dep != tempDep) {
        let attr = {
          'class': 'department',
          'rowspan': $('[dep="'+tempDep+'"]:visible').length
        };
        $(this).prepend($('<td>').attr(attr).append($('<span>').text(tempDep)));
        dep = tempDep;
      }
      ogbu.createMark($('span:Contains("'+s+'")', this), s);
    });
  }

  function createMark(e, text) {
    e.each(function(){
      let t = $(this).text();
      let str = t.substr(t.toLowerCase().indexOf(text.toLowerCase()), text.length);
      $(this).html($(this).text().replace(str, '<span class="mark">'+str+'</span>'));
    });
  }

  function clearMark(e) {
    e.each(function(){
      $(this).html($(this).text());
    });
  }

  ogbu.search = search;
  ogbu.eachFind = eachFind;
  ogbu.createMark = createMark;
  ogbu.clearMark = clearMark;

  window.ogbu = ogbu;
}());
