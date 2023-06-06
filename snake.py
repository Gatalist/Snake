# -*- coding: utf-8 -*- 
from models import Game, Snake, Food


game = Game()
snake = Snake()
food = Food()


while True:
	snake.change_to = snake.event_key()
	snake.validate_direction_and_change()
	snake.do_going()

	game.screen_fill() # закраска экрана
	game.render_table() # рисуем table
	
	snake.draw_snake() # рисуем змейку
	snake.track_for_tail()

	food.food_eat(snake.snake_block, food.food_pos, game.score)
	game.show_score()
	
	food.draw_food() # рисуем еду
	game.game_update()
