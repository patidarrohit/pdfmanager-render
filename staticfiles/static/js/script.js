// Function to add input group element for pdf merge page
function createNewInputGrp() {
  // First create a DIV element.
  var txtNewInputBox = document.createElement("div");
  var new_chq_no = parseInt($("#total_chq").val());

  //check if number of files to add is not more than 10.
  if (new_chq_no <= 10) {
    // Then add the content (a new input box) of the element.
    //txtNewInputBox.innerHTML = '<div id="ig-new" class="input-group mx-auto"> <input type="file" class="form-control my-2" id="inputGroupFile" name="inputGroup" accept=".pdf"> <input id="ig-del" type="button" class="btn btn-dark" value="x" onclick="removeInputGrp();"/> </div>';
    txtNewInputBox.innerHTML = '<div id="ig-new" class="input-group mx-auto"> <input type="file" class="form-control my-2" id="inputGroupFile" name="inputGroup' + new_chq_no + ' " accept=".pdf"> <input id="ig-del" type="button" class="btn btn-dark" value="x" onclick="removeInputGrp();"/> </div>';

    new_chq_no += 1;
    $("#total_chq").val(new_chq_no);

    // Finally put it where it is supposed to appear.
    document.getElementById("ig").append(txtNewInputBox);

    //jQuery function to send alert on size if file is more than 10 MB.
    $("input[type='file']").on("change", function () {
      if (this.files[0].size > 10485760) {
        alert("Please upload file less than 10MB. Thanks!!");
        $(this).val(null);
      }
    });
  } else {
    alert("You can maximum add 10 files.");
  }
}


// Function to remove input group element for pdf merge page
function removeInputGrp() {
    const ig = document.getElementById('ig-new');
  ig.remove();
}


// jQuery function to send alert on size if file is more than 10 MB.
$("input[type='file']").on("change", function () {
    if(this.files[0].size > 10485760) {
      alert("Please upload file less than 10MB. Thanks!!");
      $(this).val(null);
    }
   });


// jQuery function to send alert if no file is selected for merge.
// function file_check() {
//     if ($('#inputGroupFile')[0].files.length === 0) {
//         alert("No files are selected.")
//         return false;
//     } else{
//         return true;
//     }
//   } 


// Function to check if any checkbox is checked on pdf rotate show form.
function check_checkbox() 
{  
  if($("input[type='checkbox'").is(':checked')) {
    return true;
  } else {
    alert("Please select atleast one item from checklist.");
    return false;
  }
}

// Select all checkboxes on pdf rotate page.

function selectAll(source) {
    checkboxes = document.getElementsByName('check');
    for(let checkbox of checkboxes){
      checkbox.checked = source.checked;
    }
  }


$(document).ready(function() {
    $('#file-sub').bind("click",function() 
    { 
        if( document.getElementById("inputGroupFile").files.length == 0 ){
            alert("No files are selected. Please select atleast one file.");
          return false;
      } 

    }); 
});


// Navbar services submenu dropdown functionality
$(document).ready(function(){
    $('.submenu a.submenu-dtl').on("click", function(e){
      $(this).next('ul').toggle();
      e.stopPropagation();
      e.preventDefault();
    });
});


$(document).ready(function(){
    $(".check-split:last").hide()
});