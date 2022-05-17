
document.onreadystatechange = () => {
if (document.readyState === "complete"){
document.querySelector("#loader").style.display = 'none';
document.querySelector("#root").style.display = 'block';
}
}