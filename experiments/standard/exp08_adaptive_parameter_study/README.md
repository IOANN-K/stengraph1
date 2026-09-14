# Експеримент 08

Дослідження параметрів адаптивного LSB.

## Контейнер

`data/images/exp07/03_texture_nature.png`

## Навантаження

`data/payload/text.txt`

## Глибина LSB

1 LSB.

## Метрики текстури

- local variance
- gradient magnitude
- Laplacian magnitude

## Розміри вікна

- 3x3
- 5x5
- 7x7
- 9x9

## Метрики

- decode success
- MSE
- PSNR
- SSIM
- SSIM loss
- changed pixels
- changed channels

## Мета

Визначити, яка метрика текстури та розмір околу забезпечують найкращу стратегію розміщення для адаптивного вбудовування 1-LSB.

Запустіть `python3 scripts/run_experiment.py`, потім `python3 scripts/plot_results.py`. Градієнт 7×7 був найкращим із SSIM 0.9999819816 на цьому одному текстурованому зображенні; це не універсальний оптимум. Оцінки є реалізаціями проєкту, натхненними літературою.
