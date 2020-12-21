baseurl = "http://localhost:5000/";

window.onload = () => {
    const backBtn = document.querySelector('.backbtn');
    if(backBtn){
        document.querySelector('.backbtn').addEventListener('click', () => {
            backClick();
        });
    }
}

const uploadImage = () => {
    const formData = new FormData();
    const files = document.querySelector('#fileupload').files;
    formData.append('file', files[0]);
    formData.append('perbesaran', document.querySelector('#perbesaran').value);
    showloading();
    fetch(baseurl + 'uploader', {
        method: 'POST',
        body: formData
    }).then((resp) => resp.json()
    ).then(data => {
        document.querySelector('.upload').classList.add('hide');
        document.querySelector('.output').classList.remove('hide');
        document.querySelector('.imgthumboutput').setAttribute('src', data.urledit);
        document.querySelector('.rb').textContent = data.normal;
        document.querySelector('.mk').textContent = data.mikrositik;
        document.querySelector('#touploader').addEventListener('click', () => {
            deleteFiles(data.filename);
            document.querySelector('.output').classList.add('hide');
            document.querySelector('.upload').classList.remove('hide');
            resetUploader();
        })
        hideloading();
    }).catch(error => {
        console.error(error);
    });

}

const hitung = () => {
    if(document.querySelector('#perbesaran').value === ""){
        shownotification("Pilih nilai perbesaran")
    }else{
        document.querySelector('.upload').classList.add('hide');
        document.querySelector('.output').classList.remove('hide');
        uploadImage();
    }
}

function deleteFiles(filename) {
    let formData = new FormData();
    formData.append('filename', filename);
    fetch(baseurl + 'deletegambar', {
        method: 'POST',
        body: formData
    });
}

function showloading(){
    const loadingWrapper = document.querySelector('.loading-wrapper');
    document.querySelector('.container').classList.add('hide');
    loadingWrapper.classList.remove('hide');
}

function hideloading(){
    const loadingWrapper = document.querySelector('.loading-wrapper');
    document.querySelector('.container').classList.remove('hide');
    loadingWrapper.classList.add('hide');
}

function shownotification(msg){
    notification = document.querySelector('.notification');
    notification.innerHTML = msg;
    notification.classList.remove('hide');
    setTimeout(() => {
        notification.classList.add('hide');
    }, 3000)
}

const resetUploader = () => {
    document.querySelector('#fileupload').value = "";
    document.querySelector('.imgthumb').classList.add('hide');
    document.querySelector('.hitungbtn').classList.add('hide');
    document.querySelector('.instruction').classList.remove('hide');
    document.querySelector('.btnbrowse').textContent = "Pilih Gambar";
    document.querySelector('#perbesaran').classList.add('hide');
}
