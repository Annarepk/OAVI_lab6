from segmentation import binImg, segmentation, profiles, imgChar, characterProfiles

fontPath = "times_new_roman.ttf"
fontSize = 52
alphabet = "abcçdefgğhijklmnoöprsştuüvyz"
filename = "text.png"
binFilename = "textBin.bmp"
profFilename = "textProf.png"
folderLet = "letters"
folderProf = "profiles"

binImg(filename, binFilename)
hProf, vProf = profiles(binFilename, profFilename)
segmentation(binFilename, hProf, vProf)

for char in alphabet:
    imgChar(char, fontPath, fontSize, folderLet)
    print(f"The character '{char}' is saved in the folder {folderLet}...")
    filename = f"{folderLet}/{char}.bmp"
    characterProfiles(filename, char)

