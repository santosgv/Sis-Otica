function myFunction() {
  // Declare variables
  var input, filter, table, tr, td, i, j, txtValue;
  input = document.getElementById("myInput");
  filter = input.value.toUpperCase();
  table = document.getElementById("myTable");
  tr = table.getElementsByTagName("tr");

  // Loop through all table rows
  for (i = 0; i < tr.length; i++) {
    var rowVisible = false;
    // Loop through all table columns in each row
    for (j = 0; j < tr[i].getElementsByTagName("td").length; j++) {
      td = tr[i].getElementsByTagName("td")[j];
      if (td) {
        txtValue = td.textContent || td.innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
          rowVisible = true;
          break; // Se encontrar um valor correspondente, não é necessário continuar verificando as outras colunas
        }
      }
    }
    // Show or hide the row based on whether any column contains the search text
    if (rowVisible) {
      tr[i].style.display = "";
    } else {
      tr[i].style.display = "none";
    }
  }
}