function highlightRows() {
  var table = document.getElementById('myTable');
  var rows = table.getElementsByTagName("tr");

  // Iterate through each row of the table and get variables from columns

  for(i = 1; i < rows.length; i++){
    var due_date = Date.parse(table.rows[i].cells[10].innerHTML);
    var current_date = Date.now();
    var estimated = parseFloat(table.rows[i].cells[15].innerHTML);
    var actual = parseFloat(table.rows[i].cells[16].innerHTML);
    var qty = parseInt(table.rows[i].cells[5].innerHTML);
    var qty_comp = parseInt(table.rows[i].cells[6].innerHTML);

    // If the due date is two days away, highlight due date red
    if (current_date + 172800000 >= due_date) {
      table.rows[i].cells[10].style.backgroundColor = '#f54242';
      table.rows[i].cells[10].style.color = 'white';
      table.rows[i].cells[10].style.fontWeight = '600';
    }

    // If the row has the actual time going over est. time, highlight act. time cell red
    if (actual > estimated) {
      table.rows[i].cells[16].style.backgroundColor = '#f54242';
      table.rows[i].cells[16].style.color = 'white';
      table.rows[i].cells[16].style.fontWeight = '600';
      table.rows[i].cells[15].style.backgroundColor = '#f54242';
      table.rows[i].cells[15].style.color = 'white';
      table.rows[i].cells[15].style.fontWeight = '600';
    }

    // If the row has a completed qty. less than req., highlight qcp cell yellow
    if (qty > qty_comp) {
      table.rows[i].cells[6].style.backgroundColor = '#f54242';
      table.rows[i].cells[6].style.color = 'white';
      table.rows[i].cells[6].style.fontWeight = '900';
    }

    link = table.rows[i].cells[18].innerHTML;
    table.rows[i].cells[18].innerHTML = '<a href="' + link + '">PDF</a>';
  }
}

function changeDeleteToTrashIcon() {
  var table = document.getElementById('myTable');
  var rows = table.getElementsByTagName("tr");

  table.getElementsByTagName('th')[20].innerHTML = '<i class="fas fa-trash-alt"></i>';
  table.getElementsByTagName('th')[19].innerHTML = '<i class="fas fa-edit"></i>';

  for(i = 1; i < rows.length; i++) {
    table.rows[i].getElementsByTagName('a')[1].innerHTML = '<i class="fas fa-edit"></i>';
    table.rows[i].getElementsByTagName('a')[2].innerHTML = '<i class="fas fa-trash-alt"></i>';
  }
}
