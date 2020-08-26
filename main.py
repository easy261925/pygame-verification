import string
import pygame
import re


class TextBox:
    def __init__(self, w, h, x, y, font=None, current=None):
        """
        :param w:文本框宽度
        :param h:文本框高度
        :param x:文本框坐标
        :param y:文本框坐标
        :param font:文本框中使用的字体
        """
        self.width = w
        self.height = h
        self.x = x
        self.y = y
        self.text = ""  # 文本框内容
        self.current = current
        self.count = 0
        self.color_index = 1
        # 创建背景surface
        self.__surface = pygame.Surface((w, h))
        # 如果font为None,那么效果可能不太好，建议传入font，更好调节
        if font is None:
            self.font = pygame.font.SysFont(
                'Arial', 22)
        else:
            self.font = font

    def draw(self, dest_surf):
        # 创建文字surf
        text_surf = self.font.render(self.text, True, (255, 255, 255))
        # 绘制背景色
        dest_surf.blit(self.__surface, (self.x, self.y))
        # 绘制文字
        temp_text = []
        temp_text = re.findall(r'.{1,64}', self.text)
        if temp_text != []:
            for i in range(0, len(temp_text)):
                line = self.font.render(
                    temp_text[i], True, (255, 255, 255))
                dest_surf.blit(line, (self.x, self.y + i * 20),
                               (0, 0, self.width, self.height))
        else:
            dest_surf.blit(text_surf, (self.x, self.y),
                           (0, 0, self.width, self.height))

    def change_bg_color(self, dest_surf):
        self.color_index += 1

    def key_down(self, event, dest_surf):
        unicode = event.unicode
        key = event.key
        print(key)
        unuse_keys = [9, 301, 303, 304, 310, 273, 274, 275, 276]
        if key in unuse_keys:
            return

        self.change_bg_color(dest_surf)

        # 退位键
        if key == 8:
            self.text = self.text[:-1]
            return

        # 回车键
        if key == 13:
            self.count = 0
            result = self.text.split(' ')
            current = self.current
            for i in range(0, len(result)):
                if current.find(result[i]) != -1 and result[i] not in [' ', '']:
                    self.count += 1
            return

        # 空格
        if key == 32:
            self.text += ' '
            return

        if unicode != "":
            char = unicode
        else:
            char = chr(key)

        self.text += char

    def safe_key_down(self, event, dest_surf):
        try:
            self.key_down(event, dest_surf)
        except:
            self.reset()

    def reset(self):
        print('reset')
        # 异常的时候还原到初始状态
        self.text += ''


def main():
    # 英文文本框demo
    pygame.init()
    FPS = 30
    clock = pygame.time.Clock()
    minutes = 0
    seconds = 0
    milliseconds = 0

    sreen_size = width, height = 640, 480
    screen = pygame.display.set_mode(sreen_size)
    text = "This is a really long sentence with a couple of breaks.\nSometimes it will break even if there isn't a break " \
        "in the sentence, but that's because the text is too long to fit the screen.\nIt can look strange sometimes.\n" \
        "This function doesn't check if the text is too high to fit on the height of the surface though, so sometimes " \
        "text will disappear underneath the surface"
    font = pygame.font.SysFont('Arial', 22)
    # 创建文本框
    text_box = TextBox(width, 200, 0, 200, current=text)

    # 游戏主循环
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                # 调用文本框键盘按下事件
                text_box.safe_key_down(event, screen)
        pygame.time.delay(FPS)

        if milliseconds > 1000:
            seconds += 1
            milliseconds -= 1000
        if seconds > 60:
            print('TODO')

        milliseconds += clock.tick_busy_loop(60)

        colors = [(255, 0, 0), (0, 255, 0)]
        screen.fill(colors[text_box.color_index % 2])

        # 绘制文本框
        text_box.draw(screen)

        def blit_text(surface, text, pos, font, color=(0, 0, 255)):
            # 2D array where each row is a list of words.
            words = [word.split(' ') for word in text.splitlines()]
            space = font.size(' ')[0]  # The width of a space.
            max_width, max_height = surface.get_size()
            x, y = pos
            for line in words:
                for word in line:
                    word_surface = font.render(word, 0, color)
                    word_width, word_height = word_surface.get_size()
                    if x + word_width >= max_width:
                        x = pos[0]  # Reset the x.
                        y += word_height  # Start on new row.
                    surface.blit(word_surface, (x, y))
                    x += word_width + space
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.

        blit_text(screen, text, (20, 20), font)
        blit_text(screen, str(seconds) + ' s',
                  (600, 420), font)
        blit_text(screen, 'Your Counter Is ' +
                  str(text_box.count), (20, 420), font)

        pygame.display.flip()


if __name__ == '__main__':
    main()
