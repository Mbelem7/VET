const btnaddm = document.getElementById("agregar-mascota"),
      btnaddp = document.getElementById("agregar-propietario"),
      formMas = document.querySelector(".mascotas"),
      formPro = document.querySelector(".propietario");

btnaddm.addEventListener("click", e=>{
  formMas.classList.add("hide");
  formPro.classList.remove("hide");
})


btnaddp.addEventListener("click", e=>{
  formPro.classList.add("hide");
  formMas.classList.remove("hide");
})




