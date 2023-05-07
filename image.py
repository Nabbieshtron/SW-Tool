from PIL import ImageGrab as PilIg
from PIL import Image as PilI
from PIL import ImageOps as PilIo


class Image:
    def __init__(self):
        self.window_rect = None
        self.rect = None
        # One image of data
        self.img = None
        # Multiple images of data
        self.imgs = None
        # Tesseract image for extraction
        self.tese_img = None

    def resize_multiple_images(self, image: list, size: list[int, float]):
        return [img.resize(sz) for img, sz in zip(image, size)]

    def update(self):
        # Get full_screenshot
        self.img = PilIg.grab(all_screens=False)
        # Croping image
        self.img = self.img.crop(
            (
                self.window_rect.left + 110,
                self.window_rect.top + 10,
                self.window_rect.w - 10,
                self.window_rect.h - 10,
            )
        )

        # Get the list of cropped images (should be 4 images)
        self.imgs = [self.img.crop(rect.rect) for rect in self.rects.values()]

        # Resize images for blit
        self.imgs = [
            img.resize(rect.default_rect.size)
            for rect, img in zip(self.rects.values(), self.imgs)
        ]

        # Stiching images to minimize performance time
        self.tese_img = self.stich_images()

        # If needed later make a function
        # x, y = image.size
        # ratio = (x / y) * 2
        # image = image.resize((round(x * ratio), round(y * ratio)))
        self.tese_img = PilIo.invert(self.tese_img)

    def get_total_image_size(self):
        total_size = [0, 0]
        for img in self.imgs:
            total_size[1] += img.size[1]
            total_size[0] = max(total_size[0], img.size[0])
        return total_size

    def stich_images(self):
        # New image surface to paste old images
        new_img = PilI.new("RGB", self.get_total_image_size(), (37, 24, 15))
        # Stiching process
        current_height = 0
        for img in self.imgs:
            new_img.paste(img, (0, current_height))
            current_height += img.size[1]
        return new_img

    # def convert_pil_to_surface(self, pil_image):
    #     return pygame.image.fromstring(
    #         pil_image.tobytes(), pil_image.size, pil_image.mode
    #     )

    # def convert_pils_to_surfaces(self, pil_image: list):
    #     return [self.convert_pil_to_surface(image) for image in pil_image]

    # def convert_surface_to_pil(surface):
    #     pil_string_image = pygame.image.tostring(surface, "RGBA", False)
    #     return Image.frombytes("RGBA", surface.get_size(), pil_string_image)
