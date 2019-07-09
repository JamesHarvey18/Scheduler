function highlightRows() {
  var table = document.getElementById('myTable');
  var rows = table.getElementsByTagName("tr");
  for(i = 1; i < rows.length; i++){
    var estimated = table.rows[i].cells[13].innerHTML;
    var actual = table.rows[i].cells[14].innerHTML;
    var qty = table.rows[i].cells[4].innerHTML;
    var qty_comp = table.rows[i].cells[5].innerHTML;

    // If the row has the actual time going over est. time, highlight red

    if (actual > estimated) {
      table.rows[i].style.backgroundColor = 'red';
      table.rows[i].style.color = 'white';
      table.rows[i].style.fontWeight = '900';
    }

    // If the row has a completed qty. less than req., highlight yellow

    if (qty > qty_comp) {
      table.rows[i].style.backgroundColor = 'yellow';
      table.rows[i].style.color = 'black';
      table.rows[i].style.fontWeight = '900';
    }

    // If the row has a completed quantity less than req. and is over time, highlight orange

    if (qty > qty_comp && actual > estimated) {
      table.rows[i].style.backgroundColor = 'orange';
      table.rows[i].style.color = 'black';
      table.rows[i].style.fontWeight = '900';
    }


  }
}
