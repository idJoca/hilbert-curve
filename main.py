import pygame
from numpy import interp, asfarray
from utils import Point2D, Step, Path, Trace
from PIL import Image
from sys import argv


class Main():
    _continue_flag = True
    _load_image_flag = False
    _image_pixels_color_array = None
    BACKGROUND_COLOR = (220, 220, 220)

    def __init__(self, width,
                 height,
                 order, render_steps, fps=30):
        pygame.init()
        if (width == 0 or height == 0):
            self.set_fullscreen()
            self.fullscreen = True
        else:
            self.canvas = pygame.display.set_mode(
                (width, height), pygame.RESIZABLE)
            self.fullscreen = False
        self.canvas.fill(self.BACKGROUND_COLOR)
        # Sets the width and height
        screen_details = pygame.display.Info()
        self.width = screen_details.current_w
        self.height = screen_details.current_h
        self.fps = fps
        self.order = order
        self.number_of_lines = ((2 ** (order - 1)) ** 2) * 4
        self.render_steps = render_steps
        self.number_of_iterations = 0
        self.color = pygame.Color(0, 0, 0, 0)
        self.count = 0
        self.clock = pygame.time.Clock()

    def set_fullscreen(self):
        self.canvas = pygame.display \
                            .set_mode(
                                (0, 0),
                                pygame.FULLSCREEN)
        screen_details = self.canvas.get_size()
        self.width = screen_details[0]
        self.height = screen_details[1]

    def loadImage(self, image_path, save_name):
        image = Image.open(image_path).resize((self.width, self.height))
        self._image_pixels_color_array = asfarray(image)
        self.save_name = "{}_hilbert_{}_{}x{}.png".format(
            save_name, self.order, self.width, self.height)
        self._load_image_flag = True

    def draw_line(self, _from: Point2D, to: Point2D):
        if (_from.is_empty()):
            return
        if self._load_image_flag is False:
            self.color.hsva = (
                interp(self.count, [0, self.number_of_lines], [0, 360]), 100, 100)
        else:
            self.color = tuple(
                self._image_pixels_color_array[int(to.y)][int(to.x)])
        pygame.draw.line(
            self.canvas, self.color, _from.to_tuple(), to.to_tuple(), 2)
        self.count += 1

    def draw_shape(self, previous, first, second, third, fourth):
        points = [previous, first, second, third, fourth]
        for index in range(1, len(points)):
            if not isinstance(points[index], Point2D):
                raise ValueError(
                    'Expected the value to be a instace of Point2D')
            self.draw_line(points[index - 1], points[index])

        return fourth

    def trace_path_by_direction(self, center: Point2D, offset: Point2D, direction: Step):
        if not isinstance(direction, Step):
            raise ValueError('Expected \'direction\' to be a instance of Step')
        if not isinstance(center, Point2D):
            raise ValueError('Expected \'center\' to be a instance of Point2D')
        if not isinstance(offset, Point2D):
            raise ValueError('Expected \'offset\' to be a instance of Point2D')

        this_offset = offset / 2
        if direction.step is Step.CONST_DIRECTION_A:
            first = Point2D(center.x - this_offset.x,
                            center.y + this_offset.y)
            second = Point2D(center.x - this_offset.x,
                             center.y - this_offset.y)
            third = Point2D(center.x + this_offset.x,
                            center.y - this_offset.y)
            fourth = Point2D(center.x + this_offset.x,
                             center.y + this_offset.y)
            path = Path(
                Step(Step.CONST_DIRECTION_D),
                Step(Step.CONST_DIRECTION_A),
                Step(Step.CONST_DIRECTION_A),
                Step(Step.CONST_DIRECTION_B),
            )
        elif direction.step is Step.CONST_DIRECTION_B:
            first = Point2D(center.x + this_offset.x,
                            center.y - this_offset.y)
            second = Point2D(center.x - this_offset.x,
                             center.y - this_offset.y)
            third = Point2D(center.x - this_offset.x,
                            center.y + this_offset.y)
            fourth = Point2D(center.x + this_offset.x,
                             center.y + this_offset.y)
            path = Path(
                Step(Step.CONST_DIRECTION_C),
                Step(Step.CONST_DIRECTION_B),
                Step(Step.CONST_DIRECTION_B),
                Step(Step.CONST_DIRECTION_A),
            )
        elif direction.step is Step.CONST_DIRECTION_C:
            first = Point2D(center.x + this_offset.x,
                            center.y - this_offset.y)
            second = Point2D(center.x + this_offset.x,
                             center.y + this_offset.y)
            third = Point2D(center.x - this_offset.x,
                            center.y + this_offset.y)
            fourth = Point2D(center.x - this_offset.x,
                             center.y - this_offset.y)
            path = Path(
                Step(Step.CONST_DIRECTION_B),
                Step(Step.CONST_DIRECTION_C),
                Step(Step.CONST_DIRECTION_C),
                Step(Step.CONST_DIRECTION_D),
            )
        elif direction.step is Step.CONST_DIRECTION_D:
            first = Point2D(center.x - this_offset.x,
                            center.y + this_offset.y)
            second = Point2D(center.x + this_offset.x,
                             center.y + this_offset.y)
            third = Point2D(center.x + this_offset.x,
                            center.y - this_offset.y)
            fourth = Point2D(center.x - this_offset.x,
                             center.y - this_offset.y)
            path = Path(
                Step(Step.CONST_DIRECTION_A),
                Step(Step.CONST_DIRECTION_D),
                Step(Step.CONST_DIRECTION_D),
                Step(Step.CONST_DIRECTION_C),
            )
        else:
            raise ValueError(
                'Expected the attribute \'step\' in the parameter \'direction\' to be valid')

        return Trace(first, second, third, fourth, path)

    def hilbert(self, center: Point2D, current_order: int, previous: Point2D, direction: Step):
        if self._continue_flag is False:
            return
        if (self.number_of_iterations >= self.render_steps):
            self.number_of_iterations = 0
            pygame.display.flip()
            self.clock.tick(self.fps)
            self.handle_events()
        else:
            self.number_of_iterations += 1

        number_of_sides = 2 ** (current_order - 1)
        x_offset = self.width / (number_of_sides * 2)
        y_offset = self.height / (number_of_sides * 2)
        offset = Point2D(x_offset, y_offset)

        if (current_order is self.order):
            trace = self.trace_path_by_direction(
                center, offset, direction)

            return self.draw_shape(previous, trace.first, trace.second, trace.third, trace.fourth)
        else:
            trace = self.trace_path_by_direction(
                center, offset, direction)

            first_point = self.hilbert(
                trace.first, current_order + 1, previous, trace.path.get(0))
            second_point = self.hilbert(
                trace.second, current_order + 1, first_point, trace.path.get(1))
            third_point = self.hilbert(
                trace.third, current_order + 1, second_point, trace.path.get(2))
            fourth_point = self.hilbert(
                trace.fourth, current_order + 1, third_point, trace.path.get(3))

            return fourth_point

    def loop(self):
        center = Point2D(self.width / 2, self.height / 2)
        offset = Point2D(0, 0)
        self.hilbert(center, 1, offset, Step(Step.CONST_DIRECTION_D))
        if self._load_image_flag is True:
            pygame.image.save(self.canvas, self.save_name)
        while self._continue_flag is True:
            # self.canvas.fill(self.BACKGROUND_COLOR)
            pygame.display.flip()
            self.handle_events()
            pass

    def handle_events(self):
        for event in pygame.event.get():
            # Quit the program if the use close the windows
            if (event.type == pygame.QUIT):
                pygame.quit()
                self._continue_flag = False
            # Or press ESCAPE
            if (event.type == pygame.KEYDOWN):
                if (event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    self._continue_flag = False
                if (event.key == pygame.K_F11):
                    if (self.fullscreen is False):
                        self.fullscreen = True
                        pygame.display.quit()
                        pygame.display.init()
                        self.set_fullscreen()
                    else:
                        self.fullscreen = False
                        self.canvas = pygame.display.set_mode((self.width, self.height),
                                                              pygame.RESIZABLE)
            if (event.type == pygame.VIDEORESIZE):
                self.width, self.height = event.size
                if (not self.fullscreen):
                    self.canvas = pygame.display.set_mode((self.width, self.height),
                                                          pygame.RESIZABLE)


if __name__ == "__main__":
    main = Main(1024, 1024, 9, 100, 0)
    main.loadImage(argv[1], argv[2])
    main.loop()
