function highlightRows() {
  var table = document.getElementById('myTable');
  var rows = table.getElementsByTagName("tr");

  // Iterate through each row of the table and get variables from columns

  for(i = 1; i < rows.length; i++){
    var estimated = parseFloat(table.rows[i].cells[15].innerHTML);
    var actual = parseFloat(table.rows[i].cells[16].innerHTML);
    var qty = parseInt(table.rows[i].cells[5].innerHTML);
    var qty_comp = parseInt(table.rows[i].cells[6].innerHTML);

    // If the row has the actual time going over est. time, highlight red

    if (actual > estimated) {
      table.rows[i].style.backgroundColor = '#f54242';
      table.rows[i].style.color = 'white';
      table.rows[i].style.fontWeight = '900';
      var row = table.rows[i];
      var edit = row.getElementsByTagName('a')[0];
      var del = row.getElementsByTagName('a')[1];
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

function changeDeleteToTrashIcon() {
  var table = document.getElementById('myTable');
  var rows = table.getElementsByTagName("tr");

  table.getElementsByTagName('th')[19].innerHTML = '<i class="fas fa-trash-alt"></i>';
  table.getElementsByTagName('th')[18].innerHTML = '<i class="fas fa-edit"></i>';

  for(i = 1; i < rows.length; i++) {
    table.rows[i].getElementsByTagName('a')[0].innerHTML = '<i class="fas fa-edit"></i>';
    table.rows[i].getElementsByTagName('a')[1].innerHTML = '<i class="fas fa-trash-alt"></i>';
  }
}
