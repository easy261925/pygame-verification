def blit_text(dest_surf, text, pos, font, color=(0, 0, 255)):
    words = [word.split(' ') for word in text.splitlines()]
    space = font.size(' ')[0]
    max_width, max_height = dest_surf.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]
                y += word_height
            dest_surf.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]
        y += word_height
