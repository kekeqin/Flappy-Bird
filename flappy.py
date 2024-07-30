import pygame   # 导入pygame模块
import sys      # 导入sys模块
import random, os   # 导入random和os模块

# Constants  常量
W, H = 288, 512  # 设置窗口尺寸
FPS = 30   # 定义刷新率，即每秒更新的帧数

#Setup  设置
pygame.init()   # 初始化pygame模块
SCREEN = pygame.display.set_mode((W, H))   # 初始化游戏窗口，设置窗口大小为W,H
NAME = pygame.display.set_caption('Flappy Bird by k_k')  # 设置游戏名称
CLOCK = pygame.time.Clock()   # 创建时钟对象，用于控制游戏的帧率

#Materials  素材
IMAGES = {}   # 创建一个字典，用于存储所需的所有图像资源
for image in os.listdir('./assert'):   # 遍历目录中的所有图像文件
    name, extension = os.path.splitext(image)   # 文件名和后缀分开检索
    path = os.path.join('./assert', image)     # 获取图像文件的完整路径
    IMAGES[name] = pygame.image.load(path)   # 加载图像并存储到字典中

FLOOR_Y = H - IMAGES['floor'].get_height()   # 计算地板Y轴位置

AUDIO = {}           #  创建一个字典，用于存储所需的所有音频资源
for audio in os.listdir('./audio'):  # 遍历目录中的所有音频文件
    name,extension = os.path.splitext(audio) # 文件名和后缀分开检索
    path = os.path.join('./audio', audio)    # 获取音频文件的完整路径
    AUDIO[name] = pygame.mixer.Sound(path)   # 加载音频并存储到字典中


def main():  # 主函数
    while True:  # 游戏循环
        AUDIO['start'].play()    #  播放开始音乐
        IMAGES['bgpic'] = IMAGES[random.choice(['day', 'night'])]   #  随机选择黑夜白天背景图片
        color = random.choice(['red','yellow', 'blue'])   # 随机选取小鸟颜色
        # 根据颜色选择小鸟的图像
        IMAGES['birds'] = [IMAGES[color+'_up'], IMAGES[color+'_mid'], IMAGES[color+'_down']]
        pipe = IMAGES[random.choice(['green_pipe', 'red_pipe'])]    # 选取水管颜色
        # 根据颜色选择管道的颜色，并上下翻转管道。第二个参数是左右互换，第三个参数是上下互换方向
        IMAGES['pipes'] = [pipe, pygame.transform.flip(pipe, False, True)]  
        menu_window()  # 显示菜单窗口
        result = game_window()  # 运行游戏窗口
        end_window(result)   # 显示游戏结束窗口

def menu_window():  # 定义菜单函数
    
    floor_x = 0   # 赋值地板图像的x坐标为：0
    ready_x = (W - IMAGES['ready'].get_width())/2   # 计算ready的x轴坐标
    ready_y = (FLOOR_Y - IMAGES['ready'].get_height())/3  # 计算ready的y轴坐标
    flappy_x = (W - IMAGES['flappy'].get_width())/2    # 计算flappy的x轴坐标
    flappy_y = (ready_y - IMAGES['flappy'].get_height())/2   # 计算flappy的x轴坐标
    # 计算left_tap的x轴坐标
    left_tap_x = (W - IMAGES['left_tap'].get_width() * 1.1 -  
                  IMAGES['start'].get_width() -  IMAGES['right_tap'].get_width() * 1.1)/2
    # 计算left_tap的y轴坐标
    left_tap_y = (H - IMAGES['ready'].get_height() * 1.1 -  
                  IMAGES['point'].get_height() * 1.1)/2
    # 计算right_tap的x轴坐标
    right_tap_x = (W - IMAGES['left_tap'].get_width() * 1.1 -  
                   IMAGES['start'].get_width() -  IMAGES['right_tap'].get_width() * 1.1)/2 + IMAGES['left_tap'].get_width() * 1.1 + IMAGES['start'].get_width() * 1.1
    # 计算right_tap的y轴坐标
    right_tap_y = (H - IMAGES['ready'].get_height() * 1.1 -  
                   IMAGES['point'].get_height() * 1.1)/2
    
    point_x = (W - IMAGES['point'].get_width())/2 + 2   # 计算point的x轴坐标
     # 计算point的y轴坐标
    point_y = (H - IMAGES['ready'].get_height() * 1.1 -  
                   IMAGES['point'].get_height() * 1.1)/2 + IMAGES['start'].get_height() * 1.1
    
    start_x = (W - IMAGES['start'].get_width())/2 - 1   # 计算start的x轴坐标
    # 计算start的y轴坐标
    start_y = (H - IMAGES['ready'].get_height() * 1.1 -  
                   IMAGES['point'].get_height() * 1.1)/2 - 3
    
    bird_x = W * 0.2 # 小鸟的x轴坐标
    bird_y = (H - IMAGES['birds'][0].get_height())/2  # 小鸟的y轴坐标
    bird_y_vel = 1   # 定义小鸟的垂直速度
    bird_y_range = [bird_y - 8, bird_y + 8]   # 设置小鸟的垂直位置范围
    idx = 0   # 初始化小鸟动画的当前帧索引
    repeat = 5  #控制小鸟飞行画面流畅度
    # 设置小鸟动画的帧序列
    frames = [0] * repeat + [1] * repeat +[2] * repeat + [1] * repeat

    bird = Bird(W * 0.2, H * 0.4)  # 创建小鸟对象，并给出xy轴位置
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 关闭窗口，退出游戏
                sys.exit()
            # 按下空格键，退出菜单窗口，进入游戏
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return
        
        bird_y += bird_y_vel   # 更新小鸟的垂直位置
        if bird_y < bird_y_range[0] or bird_y > bird_y_range[1]:
            bird_y_vel  *= -1  # 改变小鸟的垂直速度

        idx += 1    # 改变帧索引
        idx %= len(frames) #限制idx避免无限增加，多于frames即重置

        SCREEN.blit(IMAGES['bgpic'],(0,0))  # 绘制背景
        SCREEN.blit(IMAGES['floor'],(floor_x,FLOOR_Y))   # 绘制地板
        SCREEN.blit(IMAGES['ready'], (ready_x, ready_y))   # 绘制ready图像
        SCREEN.blit(IMAGES['flappy'], (flappy_x, flappy_y))  # 绘制flappy图像
        SCREEN.blit(IMAGES['left_tap'], (left_tap_x, left_tap_y))  # 绘制left_tap图像
        SCREEN.blit(IMAGES['right_tap'], (right_tap_x, right_tap_y))   # 绘制right_tap图像
        SCREEN.blit(IMAGES['point'], (point_x, point_y))   # 绘制point图像
        SCREEN.blit(IMAGES['start'], (start_x, start_y))   # 绘制start图像
        SCREEN.blit(IMAGES['birds'][frames[idx]], (bird_x,bird_y))  # 绘制birds图像
        pygame.display.update()  # 更新屏幕显示
        CLOCK.tick(FPS)   #  控制帧率

def game_window():   # 定义游戏函数
    score = 0   # 初始化分数
    AUDIO['flap'].play()   # 播放flap音频
    floor_gap = IMAGES['floor'].get_width() - W  # # 计算地板与窗口宽度的差值
    floor_x = 0  # 赋值地板图像的x坐标为：0
    
    bird = Bird(W * 0.1, H * 0.4)  # 创建小鸟对象，给出小鸟的xy轴位置

    distance = 180   # 设置每对管道间的距离
    n_pairs = 4   # 设置初始生成的管道对数
    pipe_gap = 120   # 设置管道之间的垂直距离
    pipe_group = pygame.sprite.Group()  # 创建一个精灵组，用于存储管道
    for i in range(n_pairs):
        pipe_y = random.randint(int(H*0.3), int(H*0.7))   # 随机生成管道的y坐标
        # 创建向上管道，第一个参数是x坐标，第二个是y坐标，第三个参数是方向参数True为上管道
        pipe_up = Pipe(W + i * distance, pipe_y, True)    
        # 创建向下管道，第一个参数是x坐标，第二个是y坐标，第三个参数是方向参数False为下管道
        pipe_down = Pipe(W + i * distance, pipe_y - pipe_gap, False)   
        pipe_group.add(pipe_up)  # 将上管道加入到精灵组
        pipe_group.add(pipe_down)  # 将下管道加入到精灵组

    while True:  # 游戏主循环
        flap = False   # 初始化小鸟拍翅膀状态
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()   # 点击关闭窗口，退出游戏
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    flap = True
                    AUDIO['flap'].play()   # 按下空格键，则设置拍翅膀标志，并播放拍翅膀的声音
                    
        floor_x -= 4  # 向左移动地板
        if floor_x <= - floor_gap:
            floor_x = 0   # 地板图像移动到屏幕外，重置位置
        
        bird.update(flap)   # 更新小鸟状态
        # 检查管道精灵组中的第一个上管道和下管道
        first_pipe_up = pipe_group.sprites()[0]
        first_pipe_down = pipe_group.sprites()[1]
        if first_pipe_up.rect.right < 0:
            # 如果第一个上管道已经完全移出屏幕，则生成新的管道对
            pipe_y = random.randint(int(H * 0.3), int(H * 0.7))
            new_pipe_up = Pipe(first_pipe_up.rect.x + n_pairs * distance, pipe_y, True)
            new_pipe_down = Pipe(first_pipe_up.rect.x + n_pairs * distance, pipe_y - pipe_gap, False)
            pipe_group.add(new_pipe_up)   # 将新上管道添加到精灵组
            pipe_group.add(new_pipe_down)  # 将新下管道添加到精灵组
            first_pipe_up.kill()    # 从精灵组中移除旧上管道
            first_pipe_down.kill()  # 从精灵组中移除旧下管道

        pipe_group.update()   # 更新管道精灵组的状态
        # 检查小鸟是否死亡
        if bird.rect.y > FLOOR_Y or bird.rect.y < 0 or pygame.sprite.spritecollideany(bird, pipe_group):
            bird.dying = True  # 设置小鸟死亡标志
            AUDIO['hit'].play()  # 播放碰撞声音
            AUDIO['die'].play()  # 播放死亡声音
            result = {'bird': bird, 'pipe_group':pipe_group, 'score': score}   # 存储游戏结果
            return result    # 返回游戏结果
        # 检查小鸟是否通过管道
        if bird.rect.left + first_pipe_up.x_vel < first_pipe_up.rect.centerx < bird.rect.left:
            AUDIO['score'].play()  # 播放得分声音
            score += 1   # 增加分数

    
        SCREEN.blit(IMAGES['bgpic'],(0,0))  # 绘制背景
        pipe_group.draw(SCREEN)   # 绘制管道
        SCREEN.blit(IMAGES['floor'],(floor_x,FLOOR_Y))  # 绘制地板
        show_score(score)  # 显示分数
        SCREEN.blit(bird.image, bird.rect)  # 绘制小鸟
        pygame.display.update()   # 更新游戏状态
        CLOCK.tick(FPS)  # 设置游戏帧率

def end_window(result):
    # 计算游戏结束图片在窗口中的位置
    gameover_x = (W - IMAGES['gameover'].get_width())/2
    gameover_y = (FLOOR_Y - IMAGES['gameover'].get_height())/3
    # 计算按键提示图片在窗口中的位置
    key_x = (W - IMAGES['key'].get_width())/2
    key_y = (FLOOR_Y - IMAGES['gameover'].get_height())/2 + 10
    # 获取结果字典中的鸟和管道组对象
    bird = result['bird']
    pipe_group = result['pipe_group']

    while True:  # 进入一个无限循环，直到按下空格键
        if bird.dying:  # 如果鸟对象的dying属性为True，则调用go_die方法处理鸟的死亡动画
            bird.go_die()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()   # 点击关闭窗口，退出游戏
            
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    return  # 如果按下空格键，则退出循环，返回主游戏
            
        SCREEN.blit(IMAGES['bgpic'], (0,0))   # 绘制背景
        pipe_group.draw(SCREEN)   # 绘制管道组
        SCREEN.blit(IMAGES['floor'], (0,FLOOR_Y))  # 绘制地板
        SCREEN.blit(IMAGES['gameover'], (gameover_x, gameover_y))  # 绘制游戏结束图片
        SCREEN.blit(IMAGES['key'], (key_x, key_y))  # 绘制按键提示图片
        show_score(result['score'])  # 显示分数
        SCREEN.blit(bird.image, bird.rect)   # 绘制小鸟的图像
        pygame.display.update()  # 更新屏幕显示
        CLOCK.tick(FPS)   # 控制游戏帧率

def show_score(score):         
    score_str = str(score)  # 将分数转换为字符串
    n = len(score_str)  # 获取分数字符串的长度
    w = IMAGES['0'].get_width() * 1.1  # 计算每个数字图片的宽度，并乘以1.1作为间距
    x = (W - n * w) / 2   # 计算数字图片在屏幕上的水平起始位置
    y = H * 0.1   # 计算数字图片在屏幕上的垂直起始位置
    for number in score_str:   # 遍历分数字符串中的每个数字
        SCREEN.blit(IMAGES[number], (x, y))   # 将每个数字的图片绘制到屏幕上
        x += w  # 更新x坐标，为下一个数字图片绘制位置做准备



class Bird():  # 定义小鸟类
    def __init__(self, x, y):  # 使用init构造方法
        # 初始化鸟的动画帧索引列表，包含5帧静止，5帧上升，5帧下降，5帧静止
        self.frames = [0] * 5 + [1] * 5 + [2] * 5 + [1] * 5
        self.idx = 0   # 初始化当前动画帧索引
        self.images = IMAGES['birds']   # 获取鸟的图像列表
        self.image = self.images[self.frames[self.idx]]   # 获取当前动画帧的图像
        self.rect = self.image.get_rect()    # 获取图像的矩形区域
        self.rect.x = x    # 设置鸟的初始位置
        self.rect.y = y
        self.y_vel = -10   # 初始化鸟的垂直速度
        self.max_y_vel = 10  # 设置鸟的最大垂直速度
        self.gravity = 1   # 设置鸟的重力加速度
        self.rotate = 45   # 设置鸟的旋转角度
        self.max_rotate = -20  # 设置鸟的最大旋转角度
        self.rotate_vel = -3   # 设置鸟的旋转速度
        self.y_vel_after_flap = -10   # 设置鸟拍打翅膀后的垂直速度
        self.rotate_after_flap = 45   # 设置鸟拍打翅膀后的旋转角度
        self.dying = False    # 初始化鸟的死亡状态为False
    
    def update(self, flap = False):
        # 如果用户拍打翅膀，则更新鸟的垂直速度和旋转角度
        if flap:
            self.y_vel = self.y_vel_after_flap
            self.rotate = self.rotate_after_flap
        # 更新鸟的垂直速度，同时确保不超过最大垂直速度
        self.y_vel = min(self.y_vel + self.gravity, self.max_y_vel)
        self.rect.y += self.y_vel  # 更新鸟的垂直位置
        # 更新鸟的旋转角度，同时确保不超过最大旋转角度
        self.rotate = max(self.rotate + self.rotate_vel, self.max_rotate)

        self.idx += 1   # # 获取当前动画帧的图像
        self.idx %= len(self.frames)   # 确保索引值在有效范围内循环
        self.image = self.images[self.frames[self.idx]]  # 获取当前动画帧的图像
        self.image = pygame.transform.rotate(self.image, self.rotate)  # 根据旋转角度旋转图像

    def go_die(self):
        # 如果鸟的垂直位置低于地面，则执行死亡动画
        if self.rect.y < FLOOR_Y:
            # 更新鸟的垂直位置
            self.rect.y += self.max_y_vel
            self.rotate = -90   # 设置鸟的旋转角度为-90度，模拟死亡后的倒地效果
            self.image = self.images[self.frames[self.idx]]    # 获取当前动画帧的图像
            self.image = pygame.transform.rotate(self.image, self.rotate)  # 根据旋转角度旋转图像
        else:
            self.dying = False  # 如果鸟的垂直位置高于或等于地面，则重置死亡状态为False

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, upwards=True):
        '''
        初始化管道类。
        :param x: 管道的x坐标，即在屏幕上的水平位置。
        :param y: 管道的y坐标，即在屏幕上的垂直位置。
        :param upwards: 布尔值，指示管道是向上（True）还是向下（False）。
        '''
        # 调用父类（Sprite类）的构造函数，初始化精灵
        pygame.sprite.Sprite.__init__(self)
        if upwards:  # 根据管道的方向选择图像
            # 如果是上管道，使用IMAGES字典中索引为0的图像（通常是上管道的图像）
            self.image = IMAGES['pipes'][0]
            # 获取图像的矩形区域，用于碰撞检测和定位
            self.rect = self.image.get_rect()
            self.rect.x = x   # 设置管道的初始位置
            self.rect.top = y  # 如果是上管道，设置矩形区域的顶部为指定的y坐标
        else:
            # 如果是下管道，使用IMAGES字典中索引为1的图像（通常是下管道的图像）
            self.image = IMAGES['pipes'][1]
            self.rect = self.image.get_rect()  # 获取图像的矩形区域，用于碰撞检测和定位
            self.rect.x = x    # 设置管道的初始位置
            self.rect.bottom = y   # 如果是下管道，设置矩形区域的底部为指定的y坐标
        self.x_vel = -4  # 设置管道的水平速度，向左移动
            

    def update(self):
        """
        更新管道的位置。
        每次调用此方法时，管道会根据其水平速度向左移动。
        """
        self.rect.x += self.x_vel

main()   # 启动游戏，运行main()函数


