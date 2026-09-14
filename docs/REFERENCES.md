# Джерела та походження

1. Z. Wang, A. C. Bovik, H. R. Sheikh, and E. P. Simoncelli, “Image Quality Assessment: From Error Visibility to Structural Similarity,” *IEEE Transactions on Image Processing*, 13(4), 2004, pp. 600–612. DOI: 10.1109/TIP.2003.819861.
2. A. Westfeld and A. Pfitzmann, “Attacks on Steganographic Systems,” *Information Hiding*, LNCS 1768, 2000 (conference held 1999), pp. 61–76. DOI: 10.1007/10719724_5.
3. J. Fridrich, M. Goljan, and R. Du, “Reliable Detection of LSB Steganography in Color and Grayscale Images,” *Proceedings of the 2001 Workshop on Multimedia and Security*, 2001, pp. 27–30.
4. S. Dumitrescu, X. Wu, and N. Memon, “On Steganalysis of Random LSB Embedding in Continuous-Tone Images,” *IEEE International Conference on Image Processing*, 2002.
5. J. Fridrich, M. Goljan, D. Hogea, and D. Soukal, “Quantitative Steganalysis of Digital Images: Estimating the Secret Message Length,” *Multimedia Systems*, 9, 2003, pp. 288–302. DOI: 10.1007/s00530-003-0100-9.

У запиті згадано початкову статтю Yarema та ін. 2026 року про модифіковану заміну LSB у SVG-зображеннях, але в репозиторії немає її точної назви, повного списку авторів або DOI. Тому тут не вигадують бібліографічний запис: для додавання потрібен оригінальний запис джерела. Так само адаптивне ранжування в цьому репозиторії розроблене для проєкту; жодну сучасну статтю не подано як безпосереднє джерело реалізації без перевіреного походження.

| Компонент репозиторію | Поняття | Походження | Джерело/примітка |
|---|---|---|---|
| Вбудовування LSB | заміна | усталене в літературі | Загальне поняття стеганографії. |
| SSIM | структурна подібність | усталене в літературі | Wang та ін. |
| Хі-квадрат Exp10 | статистика типу PoV | натхнене літературою | Поняття Westfeld–Pfitzmann; спрощена реалізація проєкту. |
| RS-групи Exp11 | RS-аналіз | натхнене літературою | Fridrich–Goljan–Du; обрізані від’ємні перевороти задокументовано. |
| Адаптивні оцінки | розміщення з урахуванням вмісту | натхнене літературою/специфічне для проєкту | Ранжування за дисперсією, Sobel і Лапласіаном; претензії на точну відповідність статті немає. |
| Інтерполяція Exp12 | оцінювання частки | розширення проєкту | Натхнене кількісним стегоаналізом; неканонічний оцінювач. |
| Регресія Exp14 | міжконтейнерне оцінювання | розширення проєкту | Експеримент Ridge/Random Forest. |
| Гібридні ознаки Exp15 | поєднання ознак | розширення проєкту | Експеримент Ridge/ElasticNet із негативним результатом. |
