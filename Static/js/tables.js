function highlightRows() {
  var table = document.getElementById('myTable');
  var rows = table.getElementsByTagName("tr");
  for(i = 1; i < rows.length; i++){
    var estimated = table.rows[i].cells[15].innerHTML;
    var actual = table.rows[i].cells[16].innerHTML;

    if (actual > estimated) {
      table.rows[i].style.backgroundColor = 'red';
      table.rows[i].style.color = 'white';
      }
  }
}
