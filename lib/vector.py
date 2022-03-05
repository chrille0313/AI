from func import Vector2, Particle, Colors, draw_arrow


class VectorPointer:
    def __init__(self, x, y, color=Colors.white, sprite=None):
        self.pos = Vector2(x, y)
        self.vector = Vector2(x, y)
        self.sprite = sprite
        self.color = color

    def update(self, affectors, affectorClass, affectFunction):
        self.vector = Vector2(0, 0)
        p = affectorClass(self.pos.x, self.pos.y)

        for affector in affectors:
            self.vector += affectFunction(p, affector)

    def draw(self):
        draw_arrow(self.pos, self.pos + self.vector.normalize() * 10, 3)
        # draw_line(self.pos, self.pos + self.vector.normalize() * 10)


class VectorField:
    def __init__(self, sizeX, sizeY, density):
        self.size = Vector2(sizeX, sizeY)
        self.density = density

        self.vectors = [VectorPointer(x * density, y * density, Particle) for y in range(int(sizeY/density)) for x in range(int(sizeX/density))]

    def draw(self):
        for vector in self.vectors:
            vector.draw()
