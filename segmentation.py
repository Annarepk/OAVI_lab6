from PIL import Image, ImageOps, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import numpy as np


def binImg(filename, resultFilename):
    with Image.open(filename) as img:
        img = img.convert('L')

        # Инвертируем цвета для поиска bbox
        invImg = ImageOps.invert(img)
        bbox = invImg.getbbox()

        if bbox:
            croppedImg = img.crop(bbox)
        else:
            croppedImg = img

        # Преобразуем в монохромный режим с порогом 128
        threshold = 128
        resImg = croppedImg.point(lambda p: 255 if p > threshold else 0, 'L')

        resImg.save(resultFilename)


def profiles(filename, profileFilename):
    with Image.open(filename) as img:
        width, height = img.size
        pix = img.load()

        profileX = [0] * height
        profileY = [0] * width

        for y in range(height):
            for x in range(width):
                # В монохромном изображении 0 - белый, 1 - черный
                profileX[y] += 255 - pix[x, y]
                profileY[x] += 255 - pix[x, y]
    plt.figure(figsize=(15, 6))

    plt.subplot(1, 2, 1)
    plt.barh(range(len(profileX)), profileX)
    plt.ylabel("X")
    plt.xlabel("Вес")
    plt.title(f"Профиль X")
    plt.yticks(range(0, len(profileX), max(1, len(profileX) // 10)))  # Подписи по X
    plt.xticks(range(0, max(profileX) + 1, max(1, (max(profileX) + 1) // 10)))  # Подписи по Y

    plt.subplot(1, 2, 2)
    plt.bar(range(len(profileY)), profileY)
    plt.xlabel("Y")
    plt.ylabel("Вес")
    plt.title("Горизонтальный профиль")
    plt.xticks(range(0, len(profileY), max(1, len(profileY) // 10)))
    plt.yticks(range(0, max(profileY) + 1, max(1, (max(profileY) + 1) // 10)))

    plt.title("Вертикальный профиль")
    plt.xlabel("Y")
    plt.ylabel("Вес")

    plt.tight_layout()
    plt.savefig(profileFilename)

    return profileX, profileY


def segmentation(filename, hProfile, vProfile):
    with Image.open(filename) as img:
        width, height = img.size
        # 1. Сегментация строк (горизонтальная)
        lineSeparators = []
        thresholdH = 70  # Порог для определения пробелов между строками.
        inLine = False
        startLine = 0

        for i, val in enumerate(hProfile):
            if val > thresholdH and not inLine:
                startLine = i
                inLine = True
            elif val <= thresholdH and inLine:
                lineSeparators.append((startLine, i))
                inLine = False
        if inLine:
            lineSeparators.append((startLine, height))  # Если строка до конца

        # 2. Сегментация символов в строке (вертикальная)
        charBoxes = []
        for y1, y2 in lineSeparators:
            charSeparators = []
            thresholdV = 500  # Порог для определения пробелов между символами.
            inChar = False
            startChar = 0

            for i, val in enumerate(vProfile):
                if val > thresholdV and not inChar:
                    startChar = i
                    inChar = True
                elif val <= thresholdV and inChar:
                    charSeparators.append((startChar, i))
                    inChar = False
            if inChar:
                charSeparators.append((startChar, width))  # Если символ до конца

            # Создаем прямоугольники для символов
            for x1, x2 in charSeparators:
                charBoxes.append((x1, y1, x2, y2))

    with Image.open(filename) as img:
        img = img.convert('RGB')
        draw = ImageDraw.Draw(img)
        for x1, y1, x2, y2 in charBoxes:
            draw.rectangle((x1, y1, x2, y2), outline="red")
        img.save("textSegm.png")  # Сохраняем изображение с выделенными символами
    return charBoxes


def imgChar(char, fontPath, fontSize, folder):
    font = ImageFont.truetype(fontPath, fontSize)

    tmpImg = Image.new("L", (1, 1), "white")
    tmpDraw = ImageDraw.Draw(tmpImg)
    left, top, right, bottom = tmpDraw.textbbox((0, 0), text=char, font=font)

    charWidth = int(right - left)
    charHeight = int(bottom - top)

    imgWidth = charWidth
    imgHeight = charHeight

    img = Image.new("L", (imgWidth, imgHeight), "white")
    d = ImageDraw.Draw(img)
    d.text((0 - left, 0 - top), char, font=font, fill="black")

    pix = np.array(img)
    coords = np.argwhere(pix < 255)
    if coords.size > 0:
        y0, x0 = coords.min(axis=0)
        y1, x1 = coords.max(axis=0) + 1
        imgCrop = img.crop((x0, y0, x1, y1))
    else:
        imgCrop = img

    filename = f"{folder}/{char}.bmp"
    imgCrop.save(filename)


def characterProfiles(filename, char):
    with Image.open(filename) as img:
        width, height = img.size
        pix = img.load()

        # Профили X и Y
        profileX = [0] * width
        profileY = [0] * height
        for x in range(width):
            for y in range(height):
                if pix[x, y] < 128:
                    profileX[x] += 1
                    profileY[y] += 1

        plt.figure(figsize=(10, 5))
        plt.subplot(1, 2, 1)
        plt.barh(range(len(profileX)), profileX)
        plt.ylabel("X")
        plt.xlabel("Вес")
        plt.title(f"Профиль X для '{char}'")
        plt.yticks(range(0, len(profileX), max(1, len(profileX) // 10)))  # Подписи по X
        plt.xticks(range(0, max(profileX) + 1, max(1, (max(profileX) + 1) // 10)))  # Подписи по Y

        plt.subplot(1, 2, 2)
        plt.bar(range(len(profileY)), profileY)
        plt.xlabel("Y")
        plt.ylabel("Вес")
        plt.title(f"Профиль Y для '{char}'")
        plt.xticks(range(0, len(profileY), max(1, len(profileY) // 10)))
        plt.yticks(range(0, max(profileY) + 1, max(1, (max(profileY) + 1) // 10)))

        plt.tight_layout()  # Предотвращает наложение подписей
        profileFilename = f"profiles/{char}Profile.png"
        plt.savefig(profileFilename)
        plt.close()

    return
