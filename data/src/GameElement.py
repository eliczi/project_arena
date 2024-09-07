
class GameElement:
    def __init__(self, game):
        self.game = game

    def get_blit_position(self) -> tuple[int, int]:
        if self.game.camera.camera_target:
            return self.game.camera.center_blit(self)
        else:
            return self.game.camera.blit_position(self) 