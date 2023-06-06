# -*- coding: utf-8 -*- 
import pygame
import sys
import random
import time


class Game():
	def __init__(self):
		self.background_color = (0, 255, 204)
		self.block_color_1 = (255, 255, 255)
		self.block_color_2 = (204, 255, 255)
		self.red = (255, 0, 0)
		self.black = (0, 0, 0)
		self.block_size = 20
		self.block_margin = 1
		self.screen_size = [400, 500]
		self.fps = 5 # количество кадров в секунду
		self.fps_update = pygame.time.Clock()
		self.columns = int(self.screen_size[0] / self.block_size) - 2
		self.rows = int(self.screen_size[1] / self.block_size) - 4
		self.screen = pygame.display.set_mode(self.screen_size)
		self.scores = 0
		pygame.display.set_caption("Snake")
		pygame.init()

	def game_update(self):
		pygame.display.flip() # отражаем все изменения
		self.fps_update.tick(self.fps)

	def screen_fill(self):
		self.screen.fill(self.background_color)

	def render_block(self, column, row, color):
		pygame.draw.rect(self.screen, color, 
			[(self.block_size / 2) + column * self.block_size + self.block_margin * (column + 1), 
			self.block_size + self.block_size + row * self.block_size + self.block_margin * (row + 1), 
			self.block_size, self.block_size])
	
	def render_table(self):
		for column in range(game.columns):
			for row in range(game.rows):
				if (row + column) % 2 == 0:
					color = game.block_color_1
				else:
					color = game.block_color_2
				
				self.render_block(column, row, color)
	
	def game_over(self):
		text_font = pygame.font.SysFont('monaco', 32)
		go_surf = text_font.render('Game over', True, pygame.Color(self.red))
		go_rect = go_surf.get_rect()
		go_rect.midtop = (self.screen_size[0] / 2, self.screen_size[1] / 2)
		self.screen.blit(go_surf, go_rect)
		pygame.display.flip()
		time.sleep(3)
		pygame.quit()
		sys.exit()
    
	def show_score(self):
		text_font = pygame.font.SysFont('monaco', 24)
		s_surf = text_font.render('Score: {0}'.format(self.scores), True, pygame.Color(self.black))
		s_rect = s_surf.get_rect()
		s_rect.midtop = (85, 15)
		self.screen.blit(s_surf, s_rect)

	def score(self):
		self.scores += 1


class Snake(Game):
	def __init__(self):
		super().__init__()
		self.snake_color = (0, 255, 0)
		self.snake_block = [[10, 20], [11, 20], [12, 20]]
		self.direction = None
		self.change_to = self.direction

	def validate_direction_and_change(self):
		"""Изменияем направление движения змеи"""
		if any((self.change_to == "RIGHT" and not self.direction == "LEFT",
				self.change_to == "LEFT" and not self.direction == "RIGHT",
				self.change_to == "UP" and not self.direction == "DOWN",
				self.change_to == "DOWN" and not self.direction == "UP")):
				self.direction = self.change_to

	# отслеживаем нажатия
	def event_key(self):
		for event in pygame.event.get():
			if event.type == pygame.constants.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					self.change_to = 'LEFT'              
				if event.key == pygame.K_RIGHT:
					self.change_to = 'RIGHT'
				if event.key == pygame.K_UP:
					self.change_to = 'UP'        
				if event.key == pygame.K_DOWN:
   					self.change_to = 'DOWN'
					   
		return self.change_to

	#движение хвоста змейки
	def do_going(self):
		if self.direction == 'LEFT':     
			self.going_hv()
			self.snake_block[0][0] -= 1
			if self.snake_block[0][0] < 0:
				self.snake_block[0][0] = self.columns
		if self.direction == 'RIGHT':        
			self.going_hv()
			self.snake_block[0][0] += 1
			if self.snake_block[0][0] > self.columns:
				self.snake_block[0][0] = 0        
		if self.direction == 'UP':       
			self.going_hv()
			self.snake_block[0][1] -= 1
			if self.snake_block[0][1] < 0:
				self.snake_block[0][1] = self.rows
		if self.direction == 'DOWN':     
			self.going_hv()
			self.snake_block[0][1] += 1
			if self.snake_block[0][1] > self.rows:
				self.snake_block[0][1] = 0

	def going_hv(self):
		x = 2
		y = len(self.snake_block)
		for i in reversed(self.snake_block[1:]):
			#каждый кубик (элемент хвоста) получает координаты стоящего перед ним (ближе к голове змейки)
			i[0], i[1] = self.snake_block[y - x][0], self.snake_block[y - x][1]
			x += 1

	def track_for_tail(self):
		for segment in self.snake_block[1:]:
			if segment == self.snake_block[0]:
				self.game_over()
	
	def draw_snake(self):
		for elem in self.snake_block:
			self.render_block(elem[0], elem[1], self.snake_color) # рисуем змейку


class Food(Game):
	def __init__(self):
		"""Инит еды"""
		super().__init__()
		self.food_color = (250, 0, 0)
		self.food_pos = [random.randrange(1, self.columns), random.randrange(1, self.rows)]

	def food_pos_random(self):
		self.food_pos = [random.randrange(1, self.columns), random.randrange(1, self.rows)]
	
	def food_eat(self, snake, food, score):
		if snake[0][0] == food[0] and snake[0][1] == food[1]:
			snake.insert(0, list(food))
			self.food_pos_random()
			score()

	def draw_food(self):
		self.render_block(self.food_pos[0], self.food_pos[1], self.food_color)
