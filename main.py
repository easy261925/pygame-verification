import pygame
import text_box as t
import blit_text as b

# 原文内容集合
original_text = "This is a really long sentence with a couple of breaks.\nSometimes it will break even if there isn't a break " \
    "in the sentence, but that's because the text is too long to fit the screen.\nIt can look strange sometimes.\n" \
    "This function doesn't check if the text is too high to fit on the height of the dest_surf though, so sometimes " \
    "text will disappear underneath the dest_surf"


def main():
    pygame.init()
    sreen_size = width, height = 640, 480
    screen = pygame.display.set_mode(sreen_size)
    clock = pygame.time.Clock()

    game_over = False  # 游戏结束
    MAX_SECONDS = 60  # 游戏时间
    seconds = 0  # 计时器秒数
    milliseconds = 0  # 计时器毫秒数
    bg_colors = [(255, 0, 0), (0, 255, 0)]  # 背景颜色
    common_font = pygame.font.SysFont('Arial', 22)
    game_over_font = pygame.font.SysFont('Arial', 60)

    # 创建文本框
    text_box = t.TextBox(width, 200, 0, 200,
                         original_text=original_text, game_over=game_over)

    # 游戏主循环
    while True:

        # 计时器
        if game_over == False:
            if milliseconds > 1000:
                seconds += 1
                milliseconds -= 1000
            if seconds >= MAX_SECONDS:
                game_over = True

        milliseconds += clock.tick_busy_loop(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                # 调用文本框键盘按下事件
                text_box.safe_key_down(event, screen, game_over)
                # 游戏结束回车键
                if event.key == 13 and game_over:
                    game_over = False
                    seconds = 0
                    milliseconds = 0

        screen.fill(bg_colors[text_box.color_index % 2])  # 填充背景颜色

        # 显示输入文本框
        text_box.draw(screen)

        if game_over:
            b.blit_text(screen,
                        "GAME OVER",
                        (200, 220),
                        game_over_font, color=(255, 0, 0))
            b.blit_text(screen,
                        "Press Enter Restart",
                        (150, 320),
                        game_over_font, color=(255, 0, 0))

        # 显示原文
        b.blit_text(screen, original_text, (20, 20), common_font)

        # 计时器
        b.blit_text(screen, str(seconds) + ' s',
                    (600, 420), common_font)

        # 显示匹配数量
        b.blit_text(screen, 'YOUR COUNT IS ' +
                    str(text_box.count), (20, 420), common_font)

        pygame.display.flip()


if __name__ == '__main__':
    main()
