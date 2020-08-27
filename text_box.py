import pygame
import re
import utils as u


class TextBox:
    def __init__(self, w, h, x, y, font=None, original_text=None, game_over=False):
        """
        :param w: 文本框宽度
        :param h: 文本框高度
        :param x: 文本框坐标
        :param y: 文本框坐标
        :param font: 文本框中使用的字体
        :param original_text: 原文内容
        :param game_over: 游戏是否结束
        """
        self.width = w
        self.height = h
        self.x = x
        self.y = y
        self.text = ""  # 文本框内容
        self.original_text = original_text  # 原文内容
        self.count = 0  # 匹配单词数量
        self.color_index = 1  # 当前背景颜色索引
        self.__surface = pygame.Surface((w, h))

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

    # 改变背景颜色
    def change_bg_color(self, dest_surf):
        self.color_index += 1

    # 验证匹配单词
    def verify(self):
        self.count = 0
        result = self.text.split(' ')
        origin_words = []
        words = [word.split(' ') for word in self.original_text.splitlines()]
        for line in words:
            for word in line:
                origin_words.append(word)
        for i in range(0, len(result)):
            for current in range(0, len(origin_words)):
                if u.removePunctuation(origin_words[current]) == u.removePunctuation(result[i]) and result[i] not in [' ', '']:
                    self.count += 1
                    break

    # 按下键盘事件
    def key_down(self, event, dest_surf, game_over):

        unicode = event.unicode
        key = event.key

        # 游戏结束初始化 count text
        if game_over:
            if key == 13:
                self.count = 0
                self.text = ''
                return
            else:
                return

        # print(key)
        unuse_keys = [9, 13, 301, 303, 304, 310, 273, 274, 275, 276]  # 无用的按键集合
        if key in unuse_keys:
            return

        self.change_bg_color(dest_surf)

        # 删除键
        if key == 8:
            self.text = self.text[:-1]
            self.verify()
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

        self.verify()

    # 按键报错处理
    def safe_key_down(self, event, dest_surf, game_over):
        try:
            self.key_down(event, dest_surf, game_over)
        except:
            self.reset()

    # 异常的时候还原到初始状态
    def reset(self):
        self.text += ''
