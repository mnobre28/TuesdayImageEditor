from PIL import Image, ImageOps, ImageChops
import os
        # original_pixels = list(image.getdata())
        # resulting_pixels = []
        # for px in original_pixels:
        #     current_pixel = []
        #     for value in px:
        #         current_pixel.append(round(value*0.3))
        #     resulting_pixels.append(tuple(current_pixel))
        # result_image = Image.new(image.mode, image.size)
        # result_image.putdata(tuple(resulting_pixels))


class ImageEditor(object):
    def __init__(self):
        self.file_manager = FileManager()

    @staticmethod
    def get_value_at(image, x, y):
        """ Get RGB value at current position. """
        return image.load()[x, y]

    def grey_scale(self, image, save_result_on_file=True, file_name="greyscale.jpg"):
        """ Gets as grey scale version of the original image. """
        original_pixels = list(image.getdata())
        resulting_pixels = []
        for px in original_pixels:
            current_pixel = []
            for value in px:
                current_pixel.append(round(value*0.3))
            resulting_pixels.append(tuple(current_pixel))
        result_image = Image.new(image.mode, image.size)
        result_image.putdata(tuple(resulting_pixels))
        result_image = result_image.convert('L')
        if save_result_on_file:
            self.file_manager.save_image(result_image, file_name)
            print("Greyscale operation done: saved to file " + file_name)
        return result_image

    def weighted_grey_scale(self, image, save_result_on_file=True, file_name="weighted_greyscale.jpg"):
        """ Gets as grey scale version of the original image. """
        result_image = ImageOps.grayscale(image)
        if save_result_on_file:
            self.file_manager.save_image(result_image, file_name)
            print("Weighted greyscale operation done: saved to file " + file_name)
        return result_image

    def negative(self, image, save_result_on_file=True, file_name="threshold.jpg"):
        """ Gets as negative version of the original image. """
        result_image = ImageOps.invert(image)
        if save_result_on_file:
            self.file_manager.save_image(result_image, file_name)
            print("Negative operation done: saved to file " + file_name)
        return result_image

    def threshold(self, image, threshold=128, save_result_on_file=True, file_name="threshold.jpg"):
        """ All pixes above this greyscale threshold are inverted. """
        result_image = Image.eval(image, lambda p: 255 if p >= threshold else 0)
        if save_result_on_file:
            self.file_manager.save_image(result_image, file_name)
            print("Threshold operation done: saved to file " + file_name)
        return result_image

    def addition(self, first_image, second_image, save_result_on_file=True, file_name="addition.jpg"):
        result_image = ImageChops.add(first_image, second_image, 2)
        if save_result_on_file:
            self.file_manager.save_image(result_image, file_name)
            print("Addition operation done: saved to file " + file_name)
        return result_image

    def weighted_addition(self, first_image, second_image, alpha=0.7, save_result_on_file=True,
                          file_name="weighted_addition.jpg"):
        result_image = Image.blend(first_image, second_image, alpha)
        if save_result_on_file:
            self.file_manager.save_image(result_image, file_name)
            print("Weighted addition operation done: saved to file " + file_name)
        return result_image

    def subtraction(self, first_image, second_image, save_result_on_file=True, file_name="subtraction.jpg"):
        result_image = ImageChops.subtract(first_image, second_image, 2)
        if save_result_on_file:
            self.file_manager.save_image(result_image, file_name)
            print("Subtraction operation done: saved to file " + file_name)
        return result_image

    def weighted_subtraction(self, first_image, second_image, save_result_on_file=True,
                             file_name="weighted_subtraction.jpg"):
        raise NotImplementedError

    def split_color(self, image, color='r', save_result_on_file=True, file_name="split_color.jpg"):
        result_image = self._modify_all_pixels_of_a_color(image, color)
        if save_result_on_file:
            self.file_manager.save_image(result_image, file_name)
            print("Split operation done on " + color + " color: saved to file " + file_name)
        return result_image

    def increment_color(self, image, color='r', color_modifier=0.5, save_result_on_file=True,
                        file_name="increment_color.jpg"):
        result_image = self._modify_all_pixels_of_a_color(image, color, color_modifier, 1)
        if save_result_on_file:
            self.file_manager.save_image(result_image, file_name)
            print("Increment operation done on " + color + " color: saved to file " + file_name)
        return result_image

    def histogram(self, image):
        raise NotImplementedError

    @staticmethod
    def _modify_all_pixels_of_a_color(image, color='r', color_modifier=1.0, others_modifier=0.0):
        image_data = image.getdata()
        if color == 'b':
            modified_pixels = [(round(d[0]*others_modifier), 
                                round(d[1]*others_modifier), 
                                round(d[2]*color_modifier)) for d in image_data]
        elif color == 'g':
            modified_pixels = [(round(d[0]*others_modifier), 
                                round(d[1]*color_modifier), 
                                round(d[2]*others_modifier)) for d in image_data]
        else:
            modified_pixels = [(round(d[0]*color_modifier), 
                                round(d[1]*others_modifier), 
                                round(d[2]*others_modifier)) for d in image_data]
        result_image = Image.new(image.mode, image.size)
        result_image.putdata(modified_pixels)
        return result_image


class FileManager(object):
    def __init__(self):
        self.originals = os.path.join(os.getcwd(), "original_images")
        self.results = os.path.join(os.getcwd(), "result_images")

    def get_copy(self, image_name):
        try:
            original = Image.open(os.path.join(self.originals, image_name))
            return original.copy()
        except Exception as e:
            print(e)

    def load_image(self, image_name):
        try:
            return Image.open(os.path.join(self.originals, image_name))
        except Exception as e:
            print(e)

    def save_image(self, image_to_save, new_image_name):
        try:
            image_to_save.save(os.path.join(self.results, new_image_name))
        except Exception as e:
            print(e)


if __name__ == '__main__':
    fm = FileManager()
    img = fm.get_copy("tulips.jpg")
    si = fm.get_copy("hydrangeas.jpg")
    image_editor = ImageEditor()
    result = image_editor.increment_color(img, 'g', 2)

    result.show()
