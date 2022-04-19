
  let category_add = document.querySelector('.modal .category_add')

  url_c = '/control/category_add/'
  category_add.addEventListener('click', ()=>{
    let category_title_uz = document.querySelector(".modal input[name='category_title_uz']");
    let category_title_ru = document.querySelector(".modal input[name='category_title_ru']");
    let category_priority = document.querySelector(".modal input[name='category_priority']");
    if (category_title_ru.value != '' && category_title_uz.value != '' && category_priority.value != '' ){
      fetch(url_c, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken
        },
        body: JSON.stringify({
            title_uz: category_title_uz.value,
            title_ru: category_title_ru.value,
            priority: category_priority.value
        })
        }).then(resp => resp.json()).then(
          data => {
            if (data.code == 200) {
              let select_option = document.querySelectorAll('.category_select')
              select_option[0].innerHTML += `<option value="${data.category.id}">${data.category.title_ru}</option>`
              select_option[1].innerHTML += `<option value="${data.category.id}">${data.category.title_ru}</option>`
              category_title_uz.value = ''
              category_title_ru.value = ''
              category_priority.value = 1
              let alert_box = document.querySelector('.alert_box')
              alert_box.innerHTML = `
              <div class="alert alert-dismissible fade show py-2 bg-success d-flex justify-content-between">
                <div class="d-flex align-items-center">
                  <div class="fs-3 text-white"><ion-icon name="checkmark-circle-sharp"></ion-icon>
                  </div>
                  <div class="ms-3">
                    <div class="text-white">Категория добавлено</div>
                  </div>
                </div>
              </div>
              `
            }
            else{
              let alert_box = document.querySelector('.alert_box')
              alert_box.innerHTML = `
              <div class="alert alert-dismissible fade show py-2 bg-danger d-flex justify-content-between">
                <div class="d-flex align-items-center">
                  <div class="fs-3 text-white"><ion-icon name="close-circle-sharp"></ion-icon>
                  </div>
                  <div class="ms-3">
                    <div class="text-white">${data.error}</div>
                  </div>
                </div>
              </div>
              `
            }
          }
        )
    } else {
      console.log("Error");
    }
  })

  
  let subcategory_add = document.querySelector('.modal .subcategory_add')

  url = '/control/subcategory_add/'
  subcategory_add.addEventListener('click', ()=>{
    let subcategory_category = document.querySelector(".modal select[name='subcategory_category']");
    let subcategory_title_uz = document.querySelector(".modal input[name='subcategory_title_uz']");
    let subcategory_title_ru = document.querySelector(".modal input[name='subcategory_title_ru']");
    let subcategory_priority = document.querySelector(".modal input[name='subcategory_priority']");
    if (subcategory_title_ru.value != '' && subcategory_title_uz.value != '' && subcategory_priority.value != '' ){
      fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken
        },
        body: JSON.stringify({
            category_id: subcategory_category.value, 
            title_uz: subcategory_title_uz.value,
            title_ru: subcategory_title_ru.value,
            priority: subcategory_priority.value
        })
        }).then(resp => resp.json()).then(
          data => {
              console.log(data);
            if (data.code == 200) {
              let select_option_subcategory = document.querySelector('.subcategory_select')
              select_option_subcategory.innerHTML += `<option value="${data.subcategory.id}">${data.subcategory.title_ru}</option>`
              subcategory_title_uz.value = ''
              subcategory_title_ru.value = ''
              subcategory_priority.value = 1
              let alert_box = document.querySelector('.alert_box_subcategory')
              alert_box.innerHTML = `
              <div class="alert alert-dismissible fade show py-2 bg-success d-flex justify-content-between">
                <div class="d-flex align-items-center">
                  <div class="fs-3 text-white"><ion-icon name="checkmark-circle-sharp"></ion-icon>
                  </div>
                  <div class="ms-3">
                    <div class="text-white">Подкатегория добавлено</div>
                  </div>
                </div>
              </div>
              `
            }
            else{
              let alert_box = document.querySelector('.alert_box_subcategory')
              alert_box.innerHTML = `
              <div class="alert alert-dismissible fade show py-2 bg-danger d-flex justify-content-between">
                <div class="d-flex align-items-center">
                  <div class="fs-3 text-white"><ion-icon name="close-circle-sharp"></ion-icon>
                  </div>
                  <div class="ms-3">
                    <div class="text-white">${data.error}</div>
                  </div>
                </div>
              </div>
              `
            }
          }
        )
    } else {
      console.log("Error");
    }
  })

  
  let discount_add = document.querySelector('.modal .discount_add')

  url_discount = '/control/discount_add/'
  discount_add.addEventListener('click', ()=>{
    let discount_title= document.querySelector(".modal input[name='discount_title']");
    let discount_unit = document.querySelector(".modal input[name='discount_unit']");
    if (discount_title.value != '' && discount_unit.value != '' ){
      fetch(url_discount, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken
        },
        body: JSON.stringify({
            title: discount_title.value,
            unit: discount_unit.value,
        })
        }).then(resp => resp.json()).then(
          data => {
            if (data.code == 200) {
              let select_option_subcategory = document.querySelector('.discount_select')
              select_option_subcategory.innerHTML += `<option value="${data.discount.id}">${data.discount.title}</option>`
              discount_title.value = ''
              discount_unit.value = ''
              let alert_box = document.querySelector('.alert_box_discount')
              alert_box.innerHTML = `
              <div class="alert alert-dismissible fade show py-2 bg-success d-flex justify-content-between">
                <div class="d-flex align-items-center">
                  <div class="fs-3 text-white"><ion-icon name="checkmark-circle-sharp"></ion-icon>
                  </div>
                  <div class="ms-3">
                    <div class="text-white">Скидка добавлено</div>
                  </div>
                </div>
              </div>
              `
            }
            else{
              let alert_box = document.querySelector('.alert_box_discount')
              alert_box.innerHTML = `
              <div class="alert alert-dismissible fade show py-2 bg-danger d-flex justify-content-between">
                <div class="d-flex align-items-center">
                  <div class="fs-3 text-white"><ion-icon name="close-circle-sharp"></ion-icon>
                  </div>
                  <div class="ms-3">
                    <div class="text-white">${data.error}</div>
                  </div>
                </div>
              </div>
              `
            }
          }
        )
    } else {
      console.log("Error");
    }
  })


