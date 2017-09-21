//These 3 functions are used to make sure file uploads are correct TYPE and SIZE
//Called by event listener added to file upload in template
//If all checks are passed, they call matching functions in s3_upload
//File extentsion and name are passed through

//WORKFLOW:     YOU ARE HERE
//template    -> JAVASRIPT  -> javascript -> view        -> javascript -> template     -> view               -> model
//file upload -> CHECK_FILES -> s3_upload -> s3_sign_put -> s3_upload  -> hidden_input -> employer/applicant -> save to db


function check_img(e){
    var file_list = e.target.files;
    for (var i = 0, file; file = file_list[i]; i++) {
        var sFileExtension = file.name.split(".").pop().toLowerCase();
        //param is sent through from template

        //sFileName = e.target.param + 'img-' + new Date().toJSON() + '.' sFileExtension;
        var sFileName = e.target.param + file.name

        var iFileSize = file.size;
        var iConvert = (file.size / 10485760).toFixed(2);
        if (iFileSize > 10485760) {
            txt = "File type : " + sFileExtension + "\n\n";
            txt += "Size: " + iConvert + " MB \n\n";
            txt += "Please make sure your file is less than 10 MB.\n\n";
            alert(txt);
        } else if ( (sFileExtension != "png")
            && (sFileExtension != "jpg")
            && (sFileExtension != "jpeg")
            && (sFileExtension != "tiff")
            && (sFileExtension != "tif")
            && (sFileExtension != "jp2")
            && (sFileExtension != "jif")
            && (sFileExtension != "gif")
            ){
            alert('The file you have uploaded is not of proper format.\nYou selected: ' + sFileExtension + '\nPlease try again.\nAcceptable types: jpg, jpeg, png, tiff, tif, jp2, jif, gif.');
        } else {
            //when all checks are passed, call s3 upload js function
            s3_upload_img(sFileExtension, sFileName, 1);
        }
    }
}

