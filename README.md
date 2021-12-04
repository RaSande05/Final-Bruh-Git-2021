<h4>Реализованная функциональность</h4>
<ul>
    <li>Идентификация заполненных мусорных баков на изображении/видеопотоке;</li>
    <li>Решение задачи коммивояжера с достаточным приближением для поиска оптимального пути вывоза мусора;</li>
    <li>Информирование бригад сборщиков мусора с помощью системы оповещения;</li>
</ul> 
<h4>Особенность проекта в следующем:</h4>
<ul>
    <li>Автоматическое дообучение и оптимизация модели за счет Noisy Student;</li>
    <li>Модель поиска оптимального маршрута с учетом расписания и времени работы бригады;</li>
    <li>Бот, отсылающий карту наиболее эффективного маршрута.</li>
</ul>
<h4>Основной стек технологий:</h4>
<ul>
    <li>Python, YOLOv5, OR tools, Telegram Bot</li>
 </ul>
 
 
 
 
 
<h2>Демо основной задачи по детекции заполенных мусорных баков</h2>

<p>Модель детекции заполенных мусорных баков по скриншотам с камер наблюдения доступна по адресу: https://colab.research.google.com/drive/1ptAYUXaojcyoIFN_yUTYdeGmmH4sw7mL#scrollTo=eD_IG46UosQx</p>
<p>Полученные веса модели находятся на гугл драйве https://drive.google.com/drive/folders/19uhqeUe1a20HmwMpbqJoCs1rPXgIw4Qw?usp=sharing </p>
<p>Данные для обучения лежат в папке dataset, но так же они могут быть загружены кодом, внутри модуля</p>
<p>Модуль поиска оптимального маршрута находится в папке optimization</p>
<p>Telegram-бот, реализующий ситсему оповещения, находится в папке rare_tg_bot  </p>


<h4>СРЕДА ЗАПУСКА</h4>
Модель детекции заполенных мусорных баков и модуль поиска оптимального маршрута являются .ipynb, которые запускаются в google colab


<h4>УСТАНОВКА</h4>
Запустите первые ячейки проекта на colab. Для запуска бота скачать папку rare-tg-bot, установить библиотеки из requirements.txt и запустить файл с названием path_bot.pay


<h2>Дополнительные задачи, решенные в рамках второй части кейса</h2>

<p>Базовая модель для детекции групп бездомных собак доступна по адресу: https://colab.research.google.com/drive/1HTHS8Ra_OCOY3livaOtVkAKiYVBkzSyR?usp=sharing</p>
<p>Изображения для теста лежат в папке homeless_animals</p>
<p>Базовая модель для детекции наркокурьеров доступна по адресу: https://colab.research.google.com/drive/1sRZrCS6ZBz1BA3t2fy1AWPLYexQyuyjX?usp=sharing</p>
<p>Изображения для теста лежат в папке narcos</p>
<p>Базовая модель для детекции свободных парковочных мест доступна по адресу: https://colab.research.google.com/drive/1wYecQ0cWdM4TW6kjJxVoMUjDWojmPsIY?usp=sharing</p>
<p>Полученные веса модели находятся на гугл драйве https://drive.google.com/drive/folders/1cgtRn0gYOUneUxNt8xFKR9BcqymoGJNH?usp=sharing </p>
<p>Данные для обучения лежат в папке parklot, но так же они могут быть загружены кодом, внутри модуля</p>


<h4>СРЕДА ЗАПУСКА</h4>
Все дополнительные задачи реализованы в виде отдельных .ipynb файлов, которые запускаются в google colab


<h4>УСТАНОВКА</h4>
Запустите ячейки проекта на colab





<h2>РАЗРАБОТЧИКИ</h2>

<h4>Распопов Александр,  аналитик/проджект :goberserk: </h4>

<h4>Васюрин Кирилл, Разработчик алгоритма оптимизации поиска пути :syringe: </h4>

<h4>Буш Александр, Разработчик Telegram бота :sunglasses: </h4>

<h4>Сова Глеб, CV-разработчик :muscle: </h4>
