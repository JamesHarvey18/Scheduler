function highlightRows() {
  var table = document.getElementById('myTable');
  var rows = table.getElementsByTagName("tr");

  // Iterate through each row of the table and get variables from columns

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
      var row = table.rows[i]
      var edit = row.getElementsByTagName('a')[0];
      var del = row.getElementsByTagName('a')[1];
      console.log('edit ' + edit);
      console.log('delete ' + del);
      edit.style.color = 'white';
      del.style.color = 'white';
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
      table.rows[i].getElementsByTagName('a')[0].style.color = 'black';
      table.rows[i].getElementsByTagName('a')[1].style.color = 'black';
    }


  }
}
