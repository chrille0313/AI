from lib.func import *


class App:
    def __init__(self, windowW, windowH, fps):
        pygame.init()

        self.windowSize = self.windowW, self.windowH = windowW, windowH
        self.window = pygame.display.set_mode(self.windowSize)
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.running = True

        self.vectorField = VectorField(windowW, windowH, 20, Particle)

        self.particles = []

        self.particles.append(Particle(windowW/2, windowH/2, 10))
        self.particles.append(Particle(windowW / 2, windowH, 10, shouldSimulate=False))

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def draw(self):
        self.window.fill(Colors.black)

        # self.vectorField.draw()

        for particle in self.particles:
            particle.draw()

        pygame.display.update()

    def main_loop(self):
        while self.running:
            self.events()

            for particle1 in self.particles:
                for particle2 in self.particles:
                    if particle1 != particle2:
                        if particle1.shouldSimulate:
                            particle1.velocity += affect(particle1, particle2)
                        if particle2.shouldSimulate:
                            particle2.velocity += affect(particle2, particle1)

            for particle in self.particles:
                particle.simulate()

            # for vector in self.vectorField.vectors:
                # vector.update(self.particles, Particle, affect)

            self.draw()
            self.clock.tick(self.fps)


if __name__ == '__main__':
    app = App(1280, 720, 0)
    app.main_loop()
