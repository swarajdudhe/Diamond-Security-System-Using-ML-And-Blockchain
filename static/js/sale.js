// function uploadImage() {
//     const file = document.getElementById('fileInput').files[0];
//     if (file) {
//         // Here you can implement your upload logic
//         alert('Image uploaded successfully!');
//     } else {
//         alert('Please choose an image to upload.');
//     }
// }

// document.getElementById('fileInput').addEventListener('change', function() {
//     const file = this.files[0];
//     if (file) {
//         const reader = new FileReader();
//         reader.onload = function(e) {
//             const preview = document.getElementById('preview');
//             preview.innerHTML = '<img src="' + e.target.result + '" alt="Preview">';
//         }
//         reader.readAsDataURL(file);
//     }
// });


function uploadImage() {
    const file = document.getElementById('fileInput').files[0];
    if (file) {
        // Here you can implement your upload logic
        alert('Image uploaded successfully!');
    } else {
        alert('Please choose an image to upload.');
    }
}

document.getElementById('fileInput').addEventListener('change', function() {
    const file = this.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const preview = document.getElementById('preview');
            preview.innerHTML = '<img src="' + e.target.result + '" alt="Preview">';
        }
        reader.readAsDataURL(file);
    }
});

document.getElementById('chooseFileButton').addEventListener('click', function(event) {
    event.preventDefault(); // Prevent default action of the button click
    document.getElementById('fileInput').click(); // Trigger click event of file input
});
