const openFile = (event) => {
    document.querySelector('.error').classList.add('hide');
    var input = event.target;

    if (input.files[0].type == "image/jpeg" || input.files[0].type == "image/png") {
        var reader = new FileReader();
        reader.onload = function () {
            var dataURL = reader.result;
            var output = document.querySelector('.imgthumb');
            output.src = dataURL;
        };
        reader.readAsDataURL(input.files[0]);
        window.method = "upload";
        document.querySelector('.imgthumb').classList.remove('hide');
        document.querySelector('.btnbrowse').textContent = "Ganti Gambar";
        document.querySelector('.instruction').classList.add('hide');
        document.querySelector('.hitungbtn').classList.remove('hide');
        document.querySelector('#perbesaran').classList.remove('hide');
    } else {
        document.querySelector('.error').classList.remove('hide');
    }
};