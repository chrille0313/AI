from lib.func import *


class App:
    def __init__(self, windowW, windowH):
        pygame.init()

        self.windowSize = self.windowW, self.windowH = windowW, windowH
        self.window = pygame.display.set_mode(self.windowSize)

        self.vectorField = VectorField(windowW, windowH, 20)

        self.particles = []

        for i in range(4):
            self.particles.append(
                Particle(random.randint(0, windowW), random.randint(0, windowH), 10 if i % 2 != 0 else -10))

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

    def draw(self):
        self.window.fill(Colors.black)

        self.vectorField.draw()

        for particle in self.particles:
            particle.draw()

        pygame.display.update()

    def main_loop(self):
        while True:
            self.events()

            for particle1 in self.particles:
                for particle2 in self.particles:
                    if particle1 != particle2:
                        particle1.velocity += affect(particle1, particle2)
                        particle2.velocity += affect(particle2, particle1)

            for particle in self.particles:
                particle.simulate()

            for vector in self.vectorField.vectors:
                vector.update(self.particles, Particle, affect)

            self.draw()


if __name__ == '__main__':
    app = App(1280, 720)
    app.main_loop()
