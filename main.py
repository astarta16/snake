import pygame
import random
import time

pygame.init()


WIDTH, HEIGHT = 800, 600

#კვადრატების პიქსელები
CELL_SIZE = 20
GRID_WIDTH, GRID_HEIGHT = WIDTH // CELL_SIZE, HEIGHT // CELL_SIZE

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GREY = (50, 50, 50)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

clock = pygame.time.Clock()
#ფონტის ტიპი da ფონტის ზომა
font = pygame.font.SysFont("arial", 35)


# ფიგურების გამოსახვა და უკანა ფონი
def draw_objects(snake, apple, elapsed_time):
    screen.fill(BLACK)
    
    #ხატავს ოთხკუთხედებს
    for x in range(0, WIDTH, CELL_SIZE):
        for y in range(0, HEIGHT, CELL_SIZE):
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, GREY, rect, 1) 
    
    #ხატავს გველს
    for segment in snake:
        pygame.draw.rect(screen, WHITE, (segment[0] * CELL_SIZE, segment[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        
    #ხატავს ვაშლს
    pygame.draw.rect(screen, RED, (apple[0] * CELL_SIZE, apple[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    
    #ტაიმერის ტექსი და ტაიმერი    
    timer_text = font.render(f"Time: {elapsed_time:.1f}s", True, WHITE)
    screen.blit(timer_text, (WIDTH - 150, 10))
    
    pygame.display.update()

# რენდომის პრინციპით გამოაქვს ვაშლი ეკრანზე
def generate_apple(snake):
    while True:
        apple = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        if apple not in snake:
            return apple

#გამოაქვს წარწერა გეიმ ოუვერი და ტაიმერის სრული დრო
def display_game_over(total_time):
    screen.fill(BLACK)
    game_over_text = font.render("Game Over", True, RED)
    time_text = font.render(f"Total Time: {total_time:.1f}s", True, WHITE)
    game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
    time_rect = time_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
    screen.blit(game_over_text, game_over_rect)
    screen.blit(time_text, time_rect)
    pygame.display.update()
    pygame.time.wait(2000)

#გამოსვლის ღილაკის გამოტანა
def display_exit_menu():
    menu = True
    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos 
                if exit_button.collidepoint(mouse_pos):
                    pygame.quit()
                    quit()
        screen.fill(BLACK)
        exit_text = font.render("Exit", True, WHITE)
        exit_button = pygame.draw.rect(screen, RED, (WIDTH // 2 - 50, HEIGHT // 2 - 25, 100, 50))
        screen.blit(exit_text, exit_text.get_rect(center=exit_button.center))
        pygame.display.update()

#სტარტის ღილაკი, სტარტზე დაჭერისას თამაშის დაწყება
def display_start_menu():
    menu = True
    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if start_button.collidepoint(mouse_pos):
                    menu = False
        
        screen.fill(BLACK)
        start_text = font.render("Start", True, WHITE)
        start_button = pygame.draw.rect(screen, GREEN, (WIDTH // 2 - 50, HEIGHT // 2 - 25, 100, 50))
        screen.blit(start_text, start_text.get_rect(center=start_button.center))
        pygame.display.update()

#თამაშის დაპაუზება და თამაშის გაგრძელება
def display_pause_menu():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if resume_button.collidepoint(mouse_pos):
                    paused = False
                elif exit_button.collidepoint(mouse_pos):
                    pygame.quit()
                    quit()

        screen.fill(BLACK)
        pause_text = font.render("Paused", True, WHITE)
        resume_text = font.render("Resume", True, WHITE)
        exit_text = font.render("Exit", True, WHITE)

        pause_rect = pause_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
        resume_button = pygame.draw.rect(screen, GREEN, (WIDTH // 2 - 75, HEIGHT // 2 - 25, 150, 50))  
        exit_button = pygame.draw.rect(screen, RED, (WIDTH // 2 - 50, HEIGHT // 2 + 35, 100, 50))

        screen.blit(pause_text, pause_rect)
        screen.blit(resume_text, resume_text.get_rect(center=resume_button.center)) 
        screen.blit(exit_text, exit_text.get_rect(center=exit_button.center))  
        
        pygame.display.update()

# მთავარი გამშვები ფუნქცია
def main():
    display_start_menu() 
    
    snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
    direction = (0, 0)
    apple = generate_apple(snake)
    running = True
    timer_started = False
    start_time = 0
    paused_time = 0
    
    while running:
        #დროის დათვლა
        elapsed_time = time.time() - start_time if timer_started else paused_time 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused_time = elapsed_time  
                    display_pause_menu()
                    start_time = time.time() - paused_time 
                elif event.key == pygame.K_UP and direction != (0, 1):
                    direction = (0, -1)
                    if not timer_started:
                        timer_started = True
                        start_time = time.time() 
                elif event.key == pygame.K_DOWN and direction != (0, -1):
                    direction = (0, 1)
                    if not timer_started:
                        timer_started = True
                        start_time = time.time()
                elif event.key == pygame.K_LEFT and direction != (1, 0):
                    direction = (-1, 0)
                    if not timer_started:
                        timer_started = True
                        start_time = time.time()
                elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                    direction = (1, 0)
                    if not timer_started:
                        timer_started = True
                        start_time = time.time()  
                        
        # გველის სიგრძის გაზრდა
        new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
        if new_head in snake[1:] or not (0 <= new_head[0] < GRID_WIDTH) or not (0 <= new_head[1] < GRID_HEIGHT):
            display_game_over(elapsed_time)
            running = False
            continue
        snake.insert(0, new_head)
        if new_head == apple:
            apple = generate_apple(snake)
        else:
            snake.pop()

        draw_objects(snake, apple, elapsed_time)
        clock.tick(8)

    pygame.quit()

if __name__ == "__main__":
    main()
