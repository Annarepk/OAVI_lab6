# OAVI_lab6
_Сегментация текста_

### Вариант 18

**Турецкие строчные буквы**

Была поставлена следующая задача:

1. Подготовить в Microsoft Word романтическую фразу с выбранным алфавитом
2. Сделать скриншот и сохранить в монохромный BMP-файл без белого фона
3. Реализовать алгоритм расчёта горизонтального и вертикального профиля изображения
4. Реализовать алгоритм сегментации символов в строке на основе профилей
5. Построить профили символов выбранного алфавита

***

## Функции

Основные функции находятся в файле `segmentation.py`.

### segmentation.py

- `binImg(filename: str, resultFilename: str) -> None`
    > Преобразует изображение в монохромное с обрезкой лишних полей
    >
    > _ПАРАМЕТРЫ:_  
    >    * **filename** - Путь к исходному изображению  
    >    * **resultFilename** - Путь для сохранения результата  

- `profiles(filename: str, profileFilename: str) -> tuple`
    > Вычисляет и визуализирует горизонтальный и вертикальный профили
    >
    > _ПАРАМЕТРЫ:_  
    >    * **filename** - Путь к изображению  
    >    * **profileFilename** - Путь для сохранения графиков  
    >
    > _ВОЗВРАЩАЕТ:_  
    >    * Кортеж (горизонтальный профиль, вертикальный профиль)

- `segmentation(filename: str, hProfile: list, vProfile: list) -> list`
    > Сегментирует текст на изображении на отдельные символы
    >
    > _ПАРАМЕТРЫ:_  
    >    * **filename** - Путь к изображению  
    >    * **hProfile** - Горизонтальный профиль  
    >    * **vProfile** - Вертикальный профиль  
    >
    > _ВОЗВРАЩАЕТ:_  
    >    * Список координат прямоугольников символов (x1, y1, x2, y2)

- `imgChar(char: str, fontPath: str, fontSize: int, folder: str) -> None`
    > Создает изображение символа с заданным шрифтом
    >
    > _ПАРАМЕТРЫ:_  
    >    * **char** - Символ для отрисовки  
    >    * **fontPath** - Путь к файлу шрифта (TTF)  
    >    * **fontSize** - Размер шрифта  
    >    * **folder** - Папка для сохранения  

- `characterProfiles(filename: str, char: str) -> None`
    > Строит профили X и Y для заданного символа
    >
    > _ПАРАМЕТРЫ:_  
    >    * **filename** - Путь к изображению символа  
    >    * **char** - Символ для подписей  

---

# Работа программы

## Входные данные
- Алфавит: `abcçdefgğhijklmnoöprsştuüvyz`
- Шрифт: Times New Roman, 52pt
- Пример входного изображения:

<img src="textBin.bmp" height="100">

## Результаты работы

### Профили текста
<img src="textProf.png" width="1000">

### Сегментированный текст
<img src="textSegm.png" height="100">

## Примеры профилей символов

<table>
  <tr>
    <td><img src="letters/f.bmp" height="100"></td>
    <td><img src="profiles/fProfile.png" height="300"></td>
  </tr>
  <tr>
    <td><img src="letters/ğ.bmp" height="100"></td>
    <td><img src="profiles/ğProfile.png" height="300"></td>
  </tr>
  <tr>
    <td><img src="letters/ö.bmp" height="100"></td>
    <td><img src="profiles/öProfile.png" height="300"></td>
  </tr>
  <tr>
    <td><img src="letters/ş.bmp" height="100"></td>
    <td><img src="profiles/şProfile.png" height="300"></td>
  </tr>
  <tr>
    <td><img src="letters/ü.bmp" height="100"></td>
    <td><img src="profiles/üProfile.png" height="300"></td>
  </tr>
</table>