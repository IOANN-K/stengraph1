# Експеримент 03

Порівняння вбудовування необробленого та стиснутого навантаження.

## Контейнер

`data/images/input2.png`

## Навантаження

`data/payload/text.txt`

## Стискання

Перед вбудовуванням навантаження стискається zlib рівня 9.

Порівнюються два варіанти:

- raw payload
- zlib-compressed payload

## Методи вбудовування

- sequential 1-LSB
- pseudorandom 1-LSB
- adaptive texture-based 1-LSB

## Перевірка

Після вилучення стиснуті навантаження розпаковуються та порівнюються
побайтно з початковим `text.txt`.

Також перевіряється SHA-256.

## Метрики

- embedded payload size
- compression ratio
- compression saving
- MSE
- PSNR
- SSIM
- SSIM loss
- changed pixels
- changed channels
- maximum channel difference

## Мета

Визначити, чи зменшує стискання навантаження перед стеганографічним вбудовуванням
спотворення зображення зі збереженням повного відновлення навантаження.

Запустіть `python3 scripts/run_experiment.py`, потім `python3 scripts/plot_results.py`. Збережений розмір навантаження зменшився зі 148 574 B до 53 408 B (64,05%), що покращило якість для всіх методів. Результати специфічні для навантаження; zlib є стандартним, а це порівняння конвеєра специфічне для проєкту.
