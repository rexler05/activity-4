function closeAlert(element) {
    element.parentElement.style.opacity = '0';
    setTimeout(function(){
        element.parentElement.style.display = 'none';
    }, 600);
}