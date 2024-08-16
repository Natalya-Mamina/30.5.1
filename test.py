import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



#driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))


@pytest.fixture(autouse=True)
def driver():
    driver = webdriver.Chrome()
    # Переходим на страницу авторизации
    driver.get('https://petfriends.skillfactory.ru/login')
    # element = WebDriverWait(driver, 10).until(
    #     EC.element_to_be_clickable((By.CLASS_NAME, 'nav-link'))  )
    yield driver

    driver.quit()



def test_show_all_pets(driver):
    # Вводим email
    driver.find_element(By.ID, 'email').send_keys('natakhol@mail.ru')
    # element = WebDriverWait(driver, 10).until(
    #     EC.element_to_be_clickable(By.CLASS_NAME, 'nav-link')

    # Вводим пароль
    driver.find_element(By.ID, 'pass').send_keys('happy2503$')
    # явное ожидание присутствия элемента в структуре документа.
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'btn-success'))
    )

    # Нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

    # Проверяем, что мы оказались на главной странице пользователя
    assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"

    driver.implicitly_wait(10)
    # переходим на страницу Мои питомцы
    driver.get('https://petfriends.skillfactory.ru/my_pets')

    # явное ожидание присутствия элемента в структуре документа.
    element_ = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, 'nav-link')))

    # находим фото, имена, породы и возраст моих питомцев
    images = driver.find_elements(By.XPATH, '//th/img')
    names = driver.find_elements(By.XPATH, '//td[1]')
    breeds = driver.find_elements(By.XPATH, '//td[2]')
    ages = driver.find_elements(By.XPATH, '//td[3]')

    # Общее количество моих питомцев
    all_my_pets = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table[1]/tbody/tr')

    # этот список image объектов , который имееют метод get_attribute('src') ,
    # благодаря которому можно посмотреть есть ли изображение питомца или нет.
    all_pets_images = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table[1]/tbody/tr/th/img')

    images_full = 0
    for i in range(len(all_my_pets)):
        # проверяем наличие фото у  питомца
        assert images[i].get_attribute('src') != ''
        # проверяем, что у всех питомцев есть имя, возраст и порода.
        assert names[i].text != ''
        assert breeds[i].text != ''
        assert ages[i].text != ''
        # подсчитываем количество питомцев с фото
        if images[i].get_attribute('src') != '':
            images_full = images_full + 1

        #проверяем, что в списке питомцев хотя бы у половины питомцев есть фото
    assert images_full >= len(all_my_pets) / 2
    #     # проверяем что список своих питомцев не пуст
    assert len(all_my_pets) > 0

     # проверяем, что у всех питомцев разные имена
    for i in range(len(all_my_pets)):
        for j in range(len(all_my_pets)):
            assert names[i] != names[j]
    #
    pets_info = []
    for i in range(len(all_my_pets)):
            # получаем информацию о питомце из списка всех своих питомцев
        pet_info = all_my_pets[i].text

            # избавляемся от лишних символов '\n×'
        pet_info = pet_info.split("\n")[0]

            # добавляем в список pets_info информацию рода: имя, тип, возраст,  по каждому питомцу
        pets_info.append(pet_info)


    # проверяем, что Количество строк таблицы соответствует количеству питомцев в блоке статистики пользователя
    assert len(all_my_pets) == len(pets_info)

    # проверяем, что в списке нет повторяющихся питомцев, то есть питомцев, у которых одинаковое имя, порода и возраст
    for i in range(len(pets_info)):
        for j in range(len(pets_info)):
            assert pets_info[i] != pets_info[j]
