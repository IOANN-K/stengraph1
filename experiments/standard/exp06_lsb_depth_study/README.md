# Експеримент 06

Стандартизоване дослідження глибини LSB.

## Контейнер

`data/images/input2.png`

## Навантаження

`data/payload/text.txt`

## Глибини LSB

- 1
- 2
- 3
- 4

## Методи вбудовування

- sequential
- pseudorandom
- adaptive texture-based

## Метрики

- decode success
- MSE
- PSNR
- SSIM
- SSIM loss
- changed pixels
- changed channels
- maximum channel difference

## Мета

Виміряти компроміс між глибиною LSB, місткістю вбудовування та візуальним спотворенням за стандартизованих умов.

Запустіть `python3 scripts/run_experiment.py`, потім `python3 scripts/plot_results.py`. Спотворення зростало з глибиною; адаптивний метод зберігав найвищий SSIM, а максимальні різниці становили 1, 3, 7, 15. Один контейнер обмежує узагальнення. Заміна LSB усталена; адаптивне ранжування натхнене літературою.
