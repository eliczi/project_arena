import pygame


def perfect_outline(image, loc, surface):
    mask = pygame.mask.from_surface(image)
    mask_surf = mask.to_surface()
    mask_surf.set_colorkey((0, 0, 0))
    surface.blit(mask_surf, (loc[0] - 4, loc[1]))
    surface.blit(mask_surf, (loc[0] + 4, loc[1]))
    surface.blit(mask_surf, (loc[0], loc[1] - 4))
    surface.blit(mask_surf, (loc[0], loc[1] + 4))


def wait(game, time, amount):
    if pygame.time.get_ticks() - time > amount / game.time.game_speed:
        time = pygame.time.get_ticks()
        return True


def get_mask_rect(surf, top=0, left=0):
    """Returns minimal bounding rectangle of an image"""
    surf_mask = pygame.mask.from_surface(surf)
    rect_list = surf_mask.get_bounding_rects()
    if rect_list:
        surf_mask_rect = rect_list[0].unionall(rect_list)
        surf_mask_rect.move_ip(top, left)
        return surf_mask_rect