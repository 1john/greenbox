//These 3 functions are used to upload files to s3
//Called by matching function in check_files
//Bounce off s3_sign_put view
//Change hidden input in template to capture url of upload

//WORKFLOW:                    YOU ARE HREE
//template    -> javascript  -> JAVASCRIPT -> view        -> javascript -> template     -> view               -> model
//file upload -> check_Files -> S3_UPLOAD  -> s3_sign_put -> s3_upload  -> hidden_input -> employer/applicant -> save to db


function s3_upload_img(extension, file_in, try_in){
    var trynum = try_in;
    filename = file_in;
    var s3upload = new S3Upload({
        file_dom_selector: 'img_file',
        s3_sign_put_url: '/sign_s3_put/',
        s3_object_name: filename,
        onProgress: function(percent, message) {
            // $('#img_status').css('height', .01*percent*60 + 'px');
        },
        onFinishS3Put: function(url) {
            $("#img_url").val(url);
            console.log("img url : " + url)
            $('#img_preview').src(url)
            // $(".form-module").find("label.img-upload").css({"background-image": "url("+url+")", "background-position" : "center 40px"});
        },
        onError: function(status) {
            if(trynum < 1){ //amount of tries
                console.log("upload error #" + trynum + " of type " + status + ", retrying..");
                trynum++;
                s3_upload_img(extension, file_in, trynum);
            }
            else{
                console.log("upload error #" + trynum + ", giving up.");
                $('#img_status').html('Upload error: ' + status);
            }
        }
    });
}

