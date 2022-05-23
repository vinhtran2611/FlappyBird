from Barrier_Factory import *
import matplotlib.pyplot as plt
import numpy as np

class Game:
    def __init__(self):
        self.barrier_factory = Barrier_Factory()
        self.game_runing = True  # whole game, to configure quit command
        self.game_pausing = True  # bird jumping -> true. Instruction screen -> false
        
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.screen.set_alpha(None)
        self.clock = pg.time.Clock()

        pg.init()

    def new(self):
        self.barrier_factory.index = 0  # reset the factory so that a set of tube remain unchanged

        # SORT bird_list based on its fitness,
        # from highest to lowest fitness
        self.birds.sort(key=lambda x: x.ANN.fitness, reverse=True)

        # region Calculate average fitness (used for visualize growth rate)
        fitness_ave = 0
        for bird in self.birds:
            fitness_ave += bird.ANN.fitness
        fitness_ave = fitness_ave / POPULATION
        # endregion)

        self.average_fitness_list.append(round(fitness_ave))
        self.best_fitness_list.append(self.birds[0].ANN.fitness)
        self.scores.append(self.score)

        # region Collect data
        print(f'Generation: {self.generation}')
        print(f'Average fitness: {self.average_fitness_list}')
        print(f'Best fitness: {self.best_fitness_list}')
        print(f'Scores: {self.scores}')
        index_max = np.argmax(self.scores)
        print(f'Max Score: {self.scores[index_max]} at {index_max}')
        print('==============================================================')
        # endregion

        self.generation += 1
        self.barrier_factory.count = 0

        self.birds = ANN.create_new_generation(self.birds)

        # region Barrier Factory generator
        self.tubeTop, self.tubeBottom = self.barrier_factory.generate("Tube")
        self.ground = self.barrier_factory.generate("Ground")
        self.sky = self.barrier_factory.generate("Sky")
        # endregion

        # region Add sprites to group of sprite
        self.all_birds = pg.sprite.Group()
        self.all_barrier = pg.sprite.Group()
        self.all_sprites = pg.sprite.Group()

        self.all_birds.add(self.birds)

        self.all_barrier.add(self.ground)
        self.all_barrier.add(self.sky)
        self.all_barrier.add(self.tubeBottom)
        self.all_barrier.add(self.tubeTop)

        self.all_sprites.add(self.all_birds)
        self.all_sprites.add(self.all_barrier)
        # endregion

    def update(self):
        self.score = self.barrier_factory.index 

        if len(self.all_birds) != 0:  # update best score:
            self.display_text("Best score: " + str(self.score), 10, 10, 20, BLACK)

        # increase score if bird pass through a tube
        if self.tubeBottom.rect.x + TUBE_WIDTH + BIRD_SIZE[0] <= WIDTH_GAME / 2:
            self.tubeTop, self.tubeBottom = self.barrier_factory.generate("Tube")

            self.all_barrier.add(self.tubeBottom)
            self.all_barrier.add(self.tubeTop)
            self.all_sprites.add(self.all_barrier)

        # feed forward NN of each bird
        for bird in self.all_birds:
            bird.sensor.detect(bird, self.tubeTop, self.tubeBottom)
            output_NN = bird.ANN.L_model_forward(np.array(  [[bird.sensor.dist_vertical],
                                                            [bird.sensor.dist_horizontal],
                                                            [TUBE_WIDTH],
                                                            [bird.rect.x],
                                                            [bird.rect.y]]))

            bird.p = output_NN[0][0]
            if output_NN > THRESHOLD:
                bird.flap()

        self.all_sprites.update()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:  # If user clicked close
                self.game_runing = False  # Flag that we are done so we exit this loop

                # raise SystemExit
            if event.type == pg.MOUSEBUTTONDOWN:
                # 1 is the left mouse button, 2 is middle, 3 is right.
                if event.button == 1:
                    # `event.pos` is the mouse position.
                    if self.pause_button.collidepoint(event.pos):
                        # Increment the number.
                        self.game_pausing = not self.game_pausing
            if event.type == pg.MOUSEBUTTONDOWN:
                # 1 is the left mouse button, 2 is middle, 3 is right.
                if event.button == 1:
                    # `event.pos` is the mouse position.
                    if self.statistic_button.collidepoint(event.pos):
                        # Increment the number.
                        self.statistic()
            if event.type == pg.MOUSEBUTTONDOWN:
                # 1 is the left mouse button, 2 is middle, 3 is right.
                if event.button == 1:
                    # `event.pos` is the mouse position.
                    if self.restart_button.collidepoint(event.pos):
                        # Increment the number.
                        self.start_screen()
                    
            if event.type == pg.MOUSEBUTTONDOWN:
                # 1 is the left mouse button, 2 is middle, 3 is right.
                if event.button == 1:
                    # `event.pos` is the mouse position.
                    if self.end_button.collidepoint(event.pos):
                        # Increment the number.
                        for i in range(0, POPULATION):  # check collision
                            if self.birds[i].live:
                                self.birds[i].live = 0
                                self.all_birds.remove(self.birds[i])
                                self.all_sprites.remove(self.birds[i])
                        

        for i in range(0, POPULATION):  # check collision
            birdCollide = pg.sprite.spritecollide(self.birds[i], self.all_barrier, False)
            if birdCollide:
                self.birds[i].live = 0
                self.all_birds.remove(self.birds[i])
                self.all_sprites.remove(self.birds[i])

        if len(self.all_birds) == 0:  # dead birds are removed from group of bird sprite (all_bird)
            self.new()
    
   
    def draw(self):
        self.screen.blit(Background, [0, 0])

        for bird in self.all_birds:  # Use blit instead of draw to have better speed
            self.screen.blit(bird.image, [bird.rect.x, bird.rect.y])

        for barrier in self.all_barrier:
            self.screen.blit(barrier.image, [barrier.rect.x, barrier.rect.y])

        pg.draw.rect(self.screen, GRAY, pg.Rect(400, 0, WIDTH - WIDTH_GAME, 600))   
          
        if len(self.all_birds) != 0:  # update best score:
            self.display_text("Generation: " + str(self.generation), START_POS, 0, 20, BLACK)
            self.display_text("Bird alive: " + str(len(self.all_birds)), START_POS, 30, 20, BLACK)
            self.display_text("Best score: " + str(self.score), START_POS, 50, 20, BLACK)
            index_max = np.argmax(self.scores)
            self.display_text("Max score: " + str(self.scores[index_max]) + ' at generation ' +str(index_max), START_POS, 70, 20, BLACK)

        # Create button
        self.pause_button = self.creat_button('Pause', 450, 50, 100, 50, 35)
        self.end_button = self.creat_button('End', 450, 150, 100, 50, 35)
        self.statistic_button = self.creat_button('Statistic', 600, 50, 150, 50, 35)
        self.restart_button = self.creat_button('Restart', 600, 150, 150, 50, 35)

        # Settings
        self.display_text("POPULATION: " + str(POPULATION), 450, 250, 20, WHITE)
        self.display_text("LAYER DIMS: " + str(LAYER_DIMS), 450, 300, 20, WHITE)
        self.display_text("ELITE_PRECENTAGE: " + str(ELITE_PRECENTAGE), 450, 350, 20, WHITE)
        self.display_text("GRAVITY: " + str(GRAVITY), 450, 400, 20, WHITE)
        self.display_text("JUMP_VELOCITY: " + str(JUMP_VELOCITY), 450, 450, 20, WHITE)
        if GRAVITY_TUBE < 0:
            self.display_text("GRAVITY_TUBE (HARD): " + str(GRAVITY_TUBE), 450, 500, 20, WHITE)
        elif GRAVITY_TUBE == 0:
            self.display_text("GRAVITY_TUBE (EASY):" + str(GRAVITY_TUBE), 450, 500, 20, WHITE)
        self.display_text("TUBE_VELOCITY: " + str(TUBE_VELOCITY), 450, 550, 20, WHITE)


        if self.birds[0].live == 1:  # draw two line from bird with data from bird.sensor
            pg.draw.line(self.screen, BLACK,
                         (self.birds[0].rect.center[0], self.birds[0].rect.center[1]), (
                             self.birds[0].rect.center[0] + self.birds[0].sensor.dist_horizontal,
                             self.birds[0].rect.center[1]))
            pg.draw.line(self.screen, BLACK,
                         (self.birds[0].rect.center[0], self.birds[0].rect.center[1]), (
                             self.birds[0].rect.center[0],
                             self.birds[0].rect.center[1] + self.birds[0].sensor.dist_vertical))

        pg.display.flip()
        

    def run(self):
        self.start_screen()
        while self.game_runing and self.generation <= NUM_GENNERATION:
            self.clock.tick(FPS)
            self.events()
            if self.game_pausing == False:
                self.update()
                self.draw()

    def start_screen(self):
        self.game_pausing = True
        while self.game_pausing:
            self.display_text("Flappy Bird", WIDTH / 5, HEIGHT / 5, 30, WHITE)
            self.display_text("Press S to Start...", WIDTH / 5, HEIGHT / 3, 30, WHITE)
            pg.display.flip()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    raise SystemExit  # Exit game

                if event.type == pg.KEYDOWN and event.key == pg.K_s:  # press S to start game
                    self.game_pausing = False

                    self.score = 0  # best score
                    self.birds = [Bird() for i in range(POPULATION)]  # all bird in a population

                    self.generation = 0
                    self.average_fitness = 0
                    self.average_fitness_list = []
                    self.best_fitness_list = []
                    self.scores = []
                    
                    self.new()

    def display_text(self, message, x, y, size, color):
        font = pg.font.SysFont("Comic Sans Ms", size)
        text = font.render(message, False, color)
        self.screen.blit(text, (x, y))

    def creat_button(self, message, x, y, w, h, size, color = BLACK):
        button = pg.Rect(x, y, w, h)
        pg.draw.rect(self.screen, color, button)
        self.display_text(message, x, y, size, color = WHITE)
        return button

    def statistic(self):
        fig, ax = plt.subplots(1,2)
        ax[0].plot(range(self.generation), self.average_fitness_list, label = 'avg')
        ax[1].plot(range(self.generation), self.best_fitness_list, label = 'best')

        ax[0].legend(loc = 2)
        ax[1].legend(loc = 2)
        plt.show()

def main():
    g = Game()
    g.run()

if __name__ == "__main__":
    main()
