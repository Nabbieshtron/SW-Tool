from PIL import ImageGrab
from PIL import Image
from pytesseract import pytesseract
import pygame


def get_image():
    """Makes a full screenshot"""
    return ImageGrab.grab(all_screens=False)


def crop_image(image, pos_x, pos_y, width, height):
    return image.crop((pos_x, pos_y, width, height))


def crop_multiple_image(image, rect_list):
    """Crop multiple images from single given image and return the list of cropped images"""
    return [image.crop(rect) for rect in rect_list]


def get_total_image_size(image: list):
    total_size = [0, 0]
    for img in image:
        total_size[1] += img.size[1]
        total_size[0] = max(total_size[0], img.size[0])
    return total_size


def resize_image(image, size: tuple[int, float]):
    return image.resize(size)


def resize_multiple_images(image: list, size: list[int, float]):
    return [resize_image(img, sz) for img, sz in zip(image, size)]


def stich_multiple_image(image, image_list):
    current_height = 0
    for img in image_list:
        image.paste(img, (0, current_height))
        current_height += img.size[1]
    return image


def convert_pil_to_surface(pil_image):
    return pygame.image.fromstring(pil_image.tobytes(), pil_image.size, pil_image.mode)


def convert_pils_to_surfaces(pil_image: list):
    return [convert_pil_to_surface(image) for image in pil_image]


def convert_surface_to_pil(surface):
    pil_string_image = pygame.image.tostring(surface, "RGBA", False)
    return Image.frombytes("RGBA", surface.get_size(), pil_string_image)


def get_image_text(image):
    """Returns a text of image object"""
    return pytesseract.image_to_string(image)
