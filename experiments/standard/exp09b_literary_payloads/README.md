# Експеримент 09B

Дослідження літературних навантажень для стеганографії зображень 1-LSB.

## Контейнер

`data/images/input2.png`

## Навантаження

- alice.txt
- jekyll_hyde.txt
- frankenstein.txt
- sherlock_holmes.txt
- moby_dick.txt
- war_and_peace.txt

## Методи вбудовування

- sequential
- pseudorandom
- adaptive texture-based

## Глибина LSB

1 LSB.

## Можливі стани навантаження

- EMPTY_PAYLOAD
- CAPACITY_EXCEEDED
- EMBEDDED

## Метрики

- payload size
- capacity used
- decode success
- MSE
- PSNR
- SSIM
- SSIM loss
- changed pixels
- changed channels

## Мета

Оцінити, як реальні літературні тексти різного розміру впливають на якість зображення
і чи вміщуються вони у вибраний PNG-контейнер.

Запустіть `python3 scripts/run_experiment.py`, потім `python3 scripts/plot_results.py`. Moby-Dick умістився за 78,0737%; War and Peace перевищив місткість за 148,0367%. Тексти відрізняються розміром і вмістом, тому цей результат ілюстративний, а не контрольований за ентропією.
