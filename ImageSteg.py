from PIL import Image
import pandas as pd
import numpy as np


# Creating class to define the function encryption and Decryption of Message M in Carrier P
class ImageSteg:

    def __fillMSB(self, inp):
        """
        0b01100 -> [0,0,0,0,1,1,0,0]
        """
        # Splitting the function - In Data
        splitInput = inp.split("b")[-1]
        splitInput = '0' * (7 - len(splitInput)) + splitInput
        return [int(x) for x in splitInput]

    def __decrypt_pixels(self, pixels):
        """
        Given list of 7 pixel values -> Determine 0/1 -> Join 7 0/1s to form binary -> integer -> character
        """

        colorpixels = [str(x % 2) for x in pixels]
        binary_representation = "".join(colorpixels)
        return chr(int(binary_representation, 2))

    # Encrypting of the message M in carrier P
    def encrypting_text_in_image(self, image_path, message, target_path=""):
        """
        Read the image -> Flatten is a command used to -> encrypt images using LSB -> reshape and repack -> return image
        """
        print(image_path)
        print(message)
        imgOpen = np.array(Image.open(image_path))
        imgArray = imgOpen.flatten()
        # End of the message
        message += "<-END->"
        messageArray = [self.__fillMSB(bin(ord(charcter))) for charcter in message]

        index = 0
        for character in messageArray:
            for numbit in character:
                if numbit == 1:
                    if imgArray[index] == 0:
                        imgArray[index] = 1
                    else:
                        imgArray[index] = imgArray[index] if imgArray[index] % 2 == 1 else imgArray[index] - 1
                else:
                    if imgArray[index] == 255:
                        imgArray[index] = 254
                    else:
                        imgArray[index] = imgArray[index] if imgArray[index] % 2 == 0 else imgArray[index] + 1
                index += 1

        # savePath = target_path + "test" + "_encrypted.png"
        savePath = target_path + image_path.split(".")[0] + "_encrypted.png"
        print("save-path" + savePath)

        resultImage = Image.fromarray(np.reshape(imgArray, imgOpen.shape))
        resultImage.save(savePath)
        return

    def decrypting_text_in_image(self, image_path, target_path=""):
        """
        Read image -> Extract Text -> Return
        """
        imageToDecrypt = np.array(Image.open(image_path))
        imageArray = np.array(imageToDecrypt).flatten()

        decrypted_message = ""
        for value in range(7, len(imageArray), 7):
            decrypted_character = self.__decrypt_pixels(imageArray[value - 7:value])
            decrypted_message += decrypted_character

            if len(decrypted_message) > 10 and decrypted_message[-7:] == "<-END->":
                break

        return decrypted_message[:-7]
