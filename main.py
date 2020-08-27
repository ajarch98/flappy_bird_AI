import pygame
import random
import os
import time


class FlappyBird:
    """Class representing the entire game."""

    def __init__(self):
        """Initialize class."""
        pygame.font.init()
        self.WIN_WIDTH = 600
        self.WIN_HEIGHT = 650
        self.FLOOR = 600
        self.START_FONT = pygame.font.SysFont("comicsans", 50)
        self.END_FONT = pygame.font.SysFont("comicsans", 70)
        self.DRAW_LINES = False

        self.WIN = pygame.display.set_mode((self.WIN_WIDTH, self.WIN_HEIGHT))
        pygame.display.set_caption("Flappy Bird")

        self.pipe_img = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")).convert_alpha())
        self.bg_img = pygame.transform.scale(pygame.image.load(os.path.join("imgs", "bg.png")).convert_alpha(), (600, 900))
        self.base_image = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")).convert_alpha())
        self.bird_images = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", f"bird{i}.png"))) for i in range(1, 4)]

        self.gen = 0

        self.game_over = False

        self.base = Base(self.base_image, self.FLOOR)
        self.bird = Bird(self.bird_images)
        self.pipes = [Pipe(self.pipe_img, 700)]
        self.score = 0

        self.clock = pygame.time.Clock()

        self.run = True

    def draw_window(self, win, bird, pipes, base, score):
        """
        Draw window for main game loop.

        :param win: a pygame window surface
        :Bird bird: an object of class Bird
        :iterable pipes: iterable containing objects of class Pipe
        :Base base: an object of class Base
        :int score: score of the game
        """
        win.blit(self.bg_img, (0, 0))
        base.draw(win)
        for pipe in pipes:
            pipe.draw(win)

        # score
        score_label = self.START_FONT.render(f"Score: {str(score)}", 1, (255, 255, 255))
        win.blit(score_label, (self.WIN_WIDTH - score_label.get_width() - 15, 10))

        # bird
        bird.draw(win)

        pygame.display.update()

    def draw_game_over_screen(self):
        """
        Draw game_over screen.

        :return bool: return boolean based on user input.
            If boolean is True, continue should be called
            in the main while loop in def play().
        """

        self.WIN.fill((0, 0, 0))
        pygame.display.update()

        game_over_text = self.END_FONT.render("GAME OVER", True, (255, 255, 255))

        text_rect = game_over_text.get_rect()
        text_x = int(self.WIN.get_width() / 2 - text_rect.width / 2)
        text_y = int(self.WIN.get_height() / 2 - text_rect.height / 2)
        self.WIN.blit(game_over_text, [text_x, text_y])

        # TODO: reduce font size and add score to game_over screen
        text = f"PRESS SPACE TO QUIT OR ANY KEY TO CONTINUE"
        retry_text = self.START_FONT.render(text, True, (255, 255, 255))
        retry_rect = retry_text.get_rect()
        retry_x = int(self.WIN.get_width() / 2 - retry_rect.width / 2)
        retry_y = int(text_x + 20)
        self.WIN.blit(retry_text, [retry_x, retry_y])

        pygame.display.update()

        pygame.event.clear()
        event = pygame.event.wait()

        # for event in pygame_events:
        if event.type == pygame.KEYDOWN and\
                event.key == pygame.K_SPACE or\
                event.type == pygame.QUIT:
            self.run = False
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            self.__init__()
            return True
        else:
            return True

    def play(self):
        """Play FlappyBird game."""
        while self.run:
            self.clock.tick(30)

            pygame_events = pygame.event.get()

            if self.game_over is True:
                continue_flag = self.draw_game_over_screen()
                if continue_flag is True:
                    continue

            for event in pygame_events:
                if event.type == pygame.QUIT:
                    self.run = False
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN and\
                        event.key == pygame.K_SPACE:
                    # pygame.quit()
                    self.bird.jump()

            self.base.move()

            pipes_to_remove = []
            add_pipe = False
            for pipe in self.pipes:
                pipe.move()

                # TODO: Fix collision detection
                if pipe.collide(self.bird, self.WIN):
                    self.game_over = True

                if pipe.x + pipe.pipe_top.get_width() < 0:
                    pipes_to_remove.append(pipe)

                if not pipe.passed and pipe.x < self.bird.x:
                    pipe.passed = True
                    add_pipe = True

            if add_pipe:
                self.score += 1
                self.pipes.append(Pipe(self.pipe_img, 800))

            for pipe in pipes_to_remove:
                self.pipes.remove(pipe)

            self.draw_window(self.WIN, self.bird, self.pipes, self.base, self.score)


class Bird():
    """Bird class representing flappy bird."""

    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5

    def __init__(self, IMGS, x=230, y=350):
        """
        Initialize the object.

        :iterable IMGS: iterable containing pygame.Surface instances storing
            bird images
        :int x: starting position on x-axis
        :int y: starting position on y-axis
        """
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.IMGS = IMGS
        self.img = self.IMGS[0]

    def jump(self):
        """Make the bird jump."""
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y

    def draw(self, win):
        """Draw the bird."""
        # TODO: edit code to display different bird images during flight
        win.blit(self.img, (self.x, self.y))

    def get_mask(self):
        """
        Return mask for current image of bird.

        :return: pygame.Mask object
        """
        return pygame.mask.from_surface(self.img)


class Base:
    """Represents the moving floor of the game."""

    VEL = 5

    def __init__(self, IMG, y):
        """
        Initialize object.

        :param y: int
        """
        self.IMG = IMG
        self.WIDTH = IMG.get_width()

        self.y = y

        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        """Move floor to simulate side-scrolling."""
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):
        """
        Draw the floor.

        :param win: the pygame window
        """
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))


class Pipe:
    """Class representing a Pipe object."""

    GAP = 200
    VEL = 5

    def __init__(self, img, x):
        """
        Initialize pipe object.

        :pygame.Surface img: pygame transformed pipe image.
        :int x: location of pipe on the x-axis.
        """
        self.x = x
        self.height = 0

        self.top = 0
        self.bottom = 0

        self.pipe_bottom = img
        self.pipe_top = pygame.transform.flip(img, False, True)

        self.passed = False

        self.set_height()

    def set_height(self):
        """Set the height of the pipe from the top of the screen."""
        self.height = random.randrange(50, 450)
        self.top = self.height - self.pipe_top.get_height()
        self.bottom = self.height + self.GAP

    def draw(self, win):
        """
        Draw the top and bottom of the pipe.

        :pygame.Surface win: instance of pygame window/surface.
        """
        win.blit(self.pipe_top, (self.x, self.top))
        win.blit(self.pipe_bottom, (self.x, self.bottom))

    def move(self):
        """Move the pipe according to velocity."""
        self.x -= self.VEL

    def collide(self,  bird, win):
        """
        Check if a bird has collided with a pipe.

        :Bird bird: object of class Bird
        :pygame.Surface win: object of class pygame.Surface

        :return Bool: return True if collision is detected,
            else return False
        """
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.pipe_top)
        bottom_mask = pygame.mask.from_surface(self.pipe_bottom)

        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        top_point = bird_mask.overlap(top_mask, top_offset)
        bottom_point = bird_mask.overlap(bottom_mask, bottom_offset)

        if top_point or bottom_point:
            return True
        return False


if __name__ == "__main__":
    game = FlappyBird()
    game.play()
