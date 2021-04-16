import random
import os
from PIL import Image

DIR_TO_SAVE = 'copy'

# PAPER_SIZE = [210, 297]  # if A4 and it fills image completely
PAPER_SIZE = [190, 250]

COPY_OK_FILE_NAME = 'copy.png'
COPY_OK_SIZE = [60, 15]  # mm

SIGN_FILE_NAME = 'sign.png'
SIGN_SIZE = [20, 20]  # mm

SEAL_FILE_NAME = 'seal.png'
SEAL_SIZE = [40, 40]  # mm


class DoCopy:
    def __init__(self, in_name):
        self.img_name = in_name
        self.img = None
        self.px_in_mm = []
        self.save_name = self.img_name

    def perform(self):
        try:
            self._make_directory_save_name()
            self._open()
            self._make_img_black_and_white()
            self._put_additional_elements()
            self._save()
            print(f'Файл подписан и сохранен: {self.save_name}')
        except Exception as e:
            print(f'Не удалось обработать файл {self.img_name}\nОшибка: {str(e)}')

    @staticmethod
    def is_image(file_name: str) -> bool:
        image_formats = ['png', 'jpg', 'jpeg', 'tif', 'jpeg']
        extension = file_name.split('.')[-1]
        if extension in image_formats:
            return True
        return False

    @staticmethod
    def rand_loc(value, start, end):
        return value * (1 - (random.randint(start, end) / 100))

    def _open(self):
        self.img = Image.open(self.img_name)
        self._set_px_in_mm()

    def _save(self):
        self.img.save(self.save_name)

    def _make_img_black_and_white(self):
        self.img = self.img.convert('L')
        self.img = self.img.convert('RGB')

    def _paste_additional_img(self, image, x, y):
        self.img.paste(image, (round(x), round(y)), image)

    def _resize_additional_to_mm(self, img, size):
        return img.resize((round(size[0] * self.px_in_mm[0]), round(size[1] * self.px_in_mm[1])), Image.ANTIALIAS)

    def _prepare_additional_img(self, img_name, img_size):
        img = Image.open(img_name)
        img = self._resize_additional_to_mm(img, img_size)
        return img

    def _put_additional_elements(self):
        seal = self._prepare_additional_img(SEAL_FILE_NAME, SEAL_SIZE)
        seal_set_x = self.rand_loc(self.img.size[0] - seal.size[0], 20, 25)
        seal_set_y = self.rand_loc(self.img.size[1] - seal.size[1], 1, 3)
        self._paste_additional_img(seal, seal_set_x, seal_set_y)

        sign = self._prepare_additional_img(SIGN_FILE_NAME, SIGN_SIZE)
        sign_set_x = seal_set_x + seal.size[0] - self.rand_loc(sign.size[0], 50, 80)
        sign_set_y = seal_set_y + (seal.size[1] - sign.size[1]) / 2
        self._paste_additional_img(sign, sign_set_x, sign_set_y)

        copy = self._prepare_additional_img(COPY_OK_FILE_NAME, COPY_OK_SIZE)
        copy_set_x = seal_set_x - self.rand_loc(copy.size[0], 5, 10)
        copy_set_y = seal_set_y + (seal.size[1] - sign.size[1]) / 2 + self.rand_loc(copy.size[1], 10, 20)
        self._paste_additional_img(copy, copy_set_x, copy_set_y)

    def _set_px_in_mm(self):
        img_width, img_height = self.img.size
        px_in_mm_x = img_width / PAPER_SIZE[0]
        px_in_mm_y = img_height / PAPER_SIZE[1]
        self.px_in_mm = [px_in_mm_x, px_in_mm_y]

    def _make_directory_save_name(self):
        path = os.path.dirname(os.path.abspath(self.img_name))
        path = os.path.join(path, DIR_TO_SAVE)
        if not os.path.isdir(path):
            os.mkdir(path)
        self.save_name = path + '/' + os.path.basename(self.img_name)


def perform_file(file_name):
    copy = DoCopy(file_name)
    copy.perform()


def perform_dir(dir_name):
    for file in os.listdir(dir_name):
        file = os.path.join(dir_name, file)
        if DoCopy.is_image(file):
            perform_file(file)
        elif os.path.isdir(file):
            if not file.endswith('/copy'):
                perform_dir(file)


def main():
    file_name = input('Введите/перетащите файл/папку: ')
    while file_name.endswith(' '):
        file_name = file_name[:len(file_name) - 2]
    if os.path.isdir(file_name):
        perform_dir(file_name)
    elif os.path.isfile(file_name):
        perform_file(file_name)
    else:
        print('Не является ни файлом, ни папкой')


if __name__ == '__main__':
    main()
