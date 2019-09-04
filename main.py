from PIL import Image, ImageOps, ImageChops
import os


class ImageEditor(object):
    def __init__(self, save_result_on_file=True):
        self.file_manager = FileManager()
        self.save_result_on_file = save_result_on_file

    @staticmethod
    def get_value_at(image, x, y):
        """ Get RGB value at current position. """
        return image.load()[x, y]

    def grey_scale(self, image, file_name="greyscale.jpg"):
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
        if self.save_result_on_file:
            self.file_manager.save_image(result_image, file_name)
            print("Greyscale operation done: saved to file " + file_name)
        return result_image

    # automatic
    def weighted_grey_scale(self, image, file_name="weighted_greyscale.jpg"):
        """ Gets as grey scale version of the original image. """
        result_image = ImageOps.grayscale(image)
        if self.save_result_on_file:
            self.file_manager.save_image(result_image, file_name)
            print("Weighted greyscale operation done: saved to file " + file_name)
        return result_image

    # automatic
    def negative(self, image, file_name="threshold.jpg"):
        """ Gets as negative version of the original image. """
        result_image = ImageOps.invert(image)
        if self.save_result_on_file:
            self.file_manager.save_image(result_image, file_name)
            print("Negative operation done: saved to file " + file_name)
        return result_image

    def threshold(self, image, threshold=128, file_name="threshold.jpg"):
        """ All pixes above this greyscale threshold are inverted. """
        result_image = Image.eval(image, lambda p: 255 if p >= threshold else 0)
        if self.save_result_on_file:
            self.file_manager.save_image(result_image, file_name)
            print("Threshold operation done: saved to file " + file_name)
        return result_image

    # automatic
    def addition(self, first_image, second_image, file_name="addition.jpg"):
        result_image = ImageChops.add(first_image, second_image, 2)
        if self.save_result_on_file:
            self.file_manager.save_image(result_image, file_name)
            print("Addition operation done: saved to file " + file_name)
        return result_image

    # automatic
    def weighted_addition(self, first_image, second_image, alpha=0.7,
                          file_name="weighted_addition.jpg"):
        result_image = Image.blend(first_image, second_image, alpha)
        if self.save_result_on_file:
            self.file_manager.save_image(result_image, file_name)
            print("Weighted addition operation done: saved to file " + file_name)
        return result_image

    # automatic
    def subtraction(self, first_image, second_image, file_name="subtraction.jpg"):
        result_image = ImageChops.subtract(first_image, second_image, 2)
        if self.save_result_on_file:
            self.file_manager.save_image(result_image, file_name)
            print("Subtraction operation done: saved to file " + file_name)
        return result_image

    def weighted_subtraction(self, first_image, second_image, weight=0.7,
                             file_name="weighted_subtraction.jpg"):
        first_image_data = first_image.getdata()
        second_image_data = second_image.getdata()
        resulting_image_data = []

        for i in range(0, len(first_image_data)):
            resulting_pixel = self._weighted_subtract_pixel(first_image_data[i], second_image_data[i], weight)
            resulting_image_data.append(tuple(resulting_pixel))
        result_image = Image.new(first_image.mode, first_image.size)
        result_image.putdata(tuple(resulting_image_data))
        if self.save_result_on_file:
            self.file_manager.save_image(result_image, file_name)
            print("Weighted subtraction done: saved to file " + file_name)
        return result_image

    @staticmethod
    def _weighted_subtract_pixel(first_pixel, second_pixel, weight):
        resulting_pixel = [0, 0, 0]
        for i in range(0, 3):
            resulting_pixel[i] = round((first_pixel[i] * weight) - (second_pixel[i] * (1-weight)))
        return resulting_pixel

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

    def split_color(self, image, color='r', file_name="split_color.jpg"):
        result_image = self._modify_all_pixels_of_a_color(image, color)
        if self.save_result_on_file:
            self.file_manager.save_image(result_image, file_name)
            print("Split operation done on " + color + " color: saved to file " + file_name)
        return result_image

    def increment_color(self, image, color='r', color_modifier=0.5,
                        file_name="increment_color.jpg"):
        result_image = self._modify_all_pixels_of_a_color(image, color, color_modifier, 1)
        if self.save_result_on_file:
            self.file_manager.save_image(result_image, file_name)
            print("Increment operation done on " + color + " color: saved to file " + file_name)
        return result_image

    def histogram(self, image):
        raise NotImplementedError

    def convolution(self, image, file_name="convolution.jpg"):
        raise NotImplemented

    def dilatation(self, image, element, file_name="dilatation.jpg"):
        image_matrix = StructuralElement.image_array_to_matrix(image.getdata(),
                                                               image.width,
                                                               image.height)
        # começar com imagem toda preta!
        for i in range(1, image.width-3):
            for j in range(1, image.height-3):
                current_pixel = image_matrix[i][j]
                if current_pixel > 0:
                    for a in range(-1, 2):
                        for b in range(-1, 2):
                            image_matrix[i+a][j+b] = element.kernel[a+1][b+1]
        result_image = Image.new(image.mode, image.size)
        result_image.putdata(tuple(StructuralElement.image_matrix_to_array(image_matrix)))
        if self.save_result_on_file:
            self.file_manager.save_image(result_image, file_name)
            print("Dilatation subtraction done: saved to file " + file_name)
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


class StructuralElement(object):
    def __init__(self, kernel_type=None):
        self.kernel = []
        if kernel_type is None:
            self.kernel = [[0, 0, 0],
                           [255, 255, 255],
                           [0, 0, 0]]

    def get_hot_spot(self):
        return self.kernel[1][1]

    def get_offset(self):
        return round(len(self.kernel) // 2)

    @staticmethod
    def image_array_to_matrix(image_data, image_width, image_height):
        matrix = []
        for i in range(0, image_width):
            column = []
            for j in range(image_height*i, image_height*(i+1)):
                column.append(image_data[j])
            matrix.append(column)
        return matrix

    @staticmethod
    def get_all_black_image_matrix():
        raise NotImplemented

    @staticmethod
    def image_matrix_to_array(image_matrix):
        image_array = []
        for row in image_matrix:
            image_array += row
        return image_array


if __name__ == '__main__':
    fm = FileManager()
    tulip = fm.get_copy("tulips.jpg")
    hydra = fm.get_copy("hydrangeas.jpg")
    bw = fm.get_copy("blackwhite.jpg")
    image_editor = ImageEditor()

    result = image_editor.dilatation(bw, StructuralElement())

    result.show()
