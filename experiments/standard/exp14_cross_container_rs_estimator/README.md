# Експеримент 14

Міжконтейнерне оцінювання частки вбудовування RS.

## Мета

Оцінити, чи можуть кілька RS-ознак оцінювати частку вбудовування LSB
для повністю невідомого контейнера зображення.

## Набір даних

Stego images generated in Experiment 13.

Containers:

- smooth light
- smooth dark
- textured nature
- mixed photograph
- graphics

Embedding rates:

- 15%
- 35%
- 60%
- 85%

Embedding methods:

- sequential
- pseudorandom
- adaptive

## Перевірка

Крос-валідація leave-one-container-out.

Для кожного фолду:

- чотири контейнери використовуються для навчання;
- один повний контейнер вилучається;
- вилучений контейнер ніколи не використовується під час підгонки моделі.

## Ознаки

RS statistics include:

- R_m
- S_m
- R_-m
- S_-m
- додатні й від’ємні RS-розриви
- gap ratio
- різниці R і S
- per-channel RS gaps

## Моделі

- Ridge regression
- Random Forest regression

## Метрики

- mean absolute error
- median absolute error
- maximum absolute error
- true vs estimated embedding rate

## Важливо

Експеримент перевіряє узагальнення між контейнерами, а не
запам’ятовування одного зображення-контейнера.

## Збережений результат та обмеження

MAE Ridge становила 5.765299 в. п. для sequential, 4.416240 в. п. для random і 7.115504 в. п. для adaptive. Random+Ridge був найсильнішою конфігурацією; Random Forest був гіршим для кожного методу. Кожен метод має лише 20 зразків (п’ять контейнерів × чотири частки), тобто на фолд припадає 16 навчальних і чотири тестові зразки. Це регресійне розширення, специфічне для проєкту, а не доказ загальної продуктивності поза цим набором даних.

Після встановлення пакета запустіть `python3 scripts/build_dataset.py`, потім `python3 scripts/run_experiment.py` і `python3 scripts/plot_results.py`. Результати — набір даних, прогнози, підсумкові метрики та графіки в `results/`.
