from Classes.Base.Vector import Vector


class SpriteAnimator:
    def __init__(self, image,scaleFactor):
        self.image = image
        self.dimOriginal = Vector(self.image.get_width(), self.image.get_height()).multiply(scaleFactor)
        self.dimCamera = Vector(0, 0)


    def draw(self, canvas, cam, pos, numberColumns, numberRows, row, column, angle):
        ratio = cam.dimCanv.copy().divideVector(cam.dim)
        self.dimCamera = self.dimOriginal.copy().divideVector(Vector(numberColumns, numberRows)).multiplyVector(ratio)
        canLoc = pos.getP()

        imageCenter = Vector(
            (self.image.get_width() / numberColumns) * column - (self.image.get_width() / numberColumns) / 2,
            (self.image.get_height() / numberRows) * row - (self.image.get_height() / numberRows) / 2)

        imageDimention = Vector(self.image.get_width() / numberColumns, self.image.get_height() / numberRows)

        canvas.draw_image(self.image, imageCenter.getP(), imageDimention.getP(), canLoc, self.dimCamera.getP(), angle)
