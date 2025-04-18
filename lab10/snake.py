import pygame
import sys
import random
import psycopg2
from psycopg2 import sql
from ast import literal_eval

# Initialize pygame
pygame.init()
pygame.display.set_caption("Snake")

# Database connection function
def connect_to_db():
    try:
        conn = psycopg2.connect(
            dbname="snake",
            user="postgres",
            password="simple",
            host="localhost"
        )
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

# Initialize database tables
def initialize_db():
    conn = connect_to_db()
    if conn:
        try:
            with conn.cursor() as cur:
                # Create user table if not exists
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        user_id SERIAL PRIMARY KEY,
                        username VARCHAR(50) UNIQUE NOT NULL,
                        highest_level INTEGER DEFAULT 1,
                        total_score INTEGER DEFAULT 0,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Create user_score table if not exists
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS user_scores (
                        score_id SERIAL PRIMARY KEY,
                        user_id INTEGER REFERENCES users(user_id),
                        score INTEGER NOT NULL,
                        level INTEGER NOT NULL,
                        snake_body TEXT NOT NULL,
                        snake_direction VARCHAR(10) NOT NULL,
                        food_pos TEXT NOT NULL,
                        food_weight INTEGER NOT NULL,
                        saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                conn.commit()
        except Exception as e:
            print(f"Error initializing database: {e}")
        finally:
            conn.close()

# Call this at the start of your application
initialize_db()

# Game constants
WIDTH, HEIGHT = 500, 500
CELL_SIZE = 10
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Colors
black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)
white = (255, 255, 255)
blue = (100, 100, 255)

# Font
font = pygame.font.SysFont('Consolas', 20)

# User functions
def get_user_level(username):
    conn = connect_to_db()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT highest_level FROM users 
                    WHERE username = %s
                """, (username,))
                result = cur.fetchone()
                if result:
                    return result[0]
                else:
                    # Create new user
                    cur.execute("""
                        INSERT INTO users (username) 
                        VALUES (%s)
                        RETURNING highest_level
                    """, (username,))
                    conn.commit()
                    return 1
        except Exception as e:
            print(f"Error getting user level: {e}")
            return 1
        finally:
            conn.close()
    return 1

def get_user_id(username):
    conn = connect_to_db()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT user_id FROM users 
                    WHERE username = %s
                """, (username,))
                result = cur.fetchone()
                return result[0] if result else None
        except Exception as e:
            print(f"Error getting user ID: {e}")
            return None
        finally:
            conn.close()
    return None

def save_game_state(user_id, score, level, snake_body, direction, food):
    conn = connect_to_db()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO user_scores 
                    (user_id, score, level, snake_body, snake_direction, food_pos, food_weight)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (
                    user_id,
                    score,
                    level,
                    str(snake_body),
                    direction,
                    str(food['pos']),
                    food['weight']
                ))
                conn.commit()
                
                # Update user's highest level if needed
                cur.execute("""
                    UPDATE users
                    SET highest_level = GREATEST(highest_level, %s),
                        total_score = total_score + %s
                    WHERE user_id = %s
                """, (level, score, user_id))
                conn.commit()
                return True
        except Exception as e:
            print(f"Error saving game state: {e}")
            return False
        finally:
            conn.close()
    return False

# Level configurations
def get_level_settings(level):
    levels = {
        1: {'speed': 5, 'walls': []},
        2: {'speed': 7, 'walls': [[100, 100, 300, 20]]},
        3: {'speed': 10, 'walls': [[100, 100, 20, 300], [380, 100, 20, 300]]},
        4: {'speed': 12, 'walls': [[50, 50, 400, 20], [50, 430, 400, 20]]},
        5: {'speed': 15, 'walls': [[0, 0, WIDTH, 20], [0, HEIGHT-20, WIDTH, 20]]}
    }
    return levels.get(level, levels[1])

# Food generation
def generate_food(snake_body, walls):
    while True:
        food_x = random.randrange(0, WIDTH, CELL_SIZE)
        food_y = random.randrange(0, HEIGHT, CELL_SIZE)
        
        # Check if food position is not on snake or walls
        valid_position = True
        if [food_x, food_y] in snake_body:
            valid_position = False
        
        for wall in walls:
            wall_rect = pygame.Rect(wall[0], wall[1], wall[2], wall[3])
            if wall_rect.collidepoint(food_x, food_y):
                valid_position = False
                break
        
        if valid_position:
            food_weight = random.randint(1, 3)
            food_timer = pygame.time.get_ticks()
            return {'pos': [food_x, food_y], 'weight': food_weight, 'spawn_time': food_timer}

# Get username at game start
username = input("Enter your username: ").strip()
if not username:
    username = "Guest"

current_level = get_user_level(username)
level_settings = get_level_settings(current_level)
speed = level_settings['speed']
walls = level_settings['walls']
user_id = get_user_id(username)

# Initialize game state
snake_pos = [250, 250]
snake_body = [[250, 250], [240, 250], [230, 250]]
actual_direction = 'RIGHT'
future_direction = actual_direction
score = 0

food = generate_food(snake_body, walls)
paused = False
game_over = False

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if not paused and not game_over:
                if event.key == pygame.K_w and actual_direction != 'DOWN':
                    future_direction = 'UP'
                elif event.key == pygame.K_s and actual_direction != 'UP':
                    future_direction = 'DOWN'
                elif event.key == pygame.K_d and actual_direction != 'LEFT':
                    future_direction = 'RIGHT'
                elif event.key == pygame.K_a and actual_direction != 'RIGHT':
                    future_direction = 'LEFT'
            if event.key == pygame.K_ESCAPE:  # Pause with ESC key
                paused = not paused
                if paused and not game_over:
                    # Save game when pausing
                    success = save_game_state(
                        user_id,
                        score,
                        current_level,
                        snake_body,
                        actual_direction,
                        food
                    )
                    if success:
                        print("Game saved successfully!")
                    else:
                        print("Failed to save game")
            elif event.key == pygame.K_r and game_over:  # Restart with R key
                # Reset game state
                snake_pos = [250, 250]
                snake_body = [[250, 250], [240, 250], [230, 250]]
                actual_direction = 'RIGHT'
                future_direction = actual_direction
                score = 0
                current_level = get_user_level(username)
                level_settings = get_level_settings(current_level)
                speed = level_settings['speed']
                walls = level_settings['walls']
                food = generate_food(snake_body, walls)
                game_over = False
    
    if paused or game_over:
        # Show pause or game over message
        screen.fill(black)
        if paused:
            pause_text = font.render("PAUSED - Press ESC to continue", True, white)
            screen.blit(pause_text, (WIDTH//2 - 150, HEIGHT//2))
        elif game_over:
            game_over_text = font.render("GAME OVER - Press R to restart", True, white)
            score_text = font.render(f"Final Score: {score}", True, white)
            screen.blit(game_over_text, (WIDTH//2 - 150, HEIGHT//2 - 20))
            screen.blit(score_text, (WIDTH//2 - 80, HEIGHT//2 + 20))
        
        pygame.display.flip()
        clock.tick(5)  # Low tick rate while paused/game over
        continue
    
    # Update direction
    actual_direction = future_direction
    
    # Movement
    if actual_direction == 'UP':
        snake_pos[1] -= CELL_SIZE
    elif actual_direction == 'DOWN':
        snake_pos[1] += CELL_SIZE
    elif actual_direction == 'LEFT':
        snake_pos[0] -= CELL_SIZE
    elif actual_direction == 'RIGHT':
        snake_pos[0] += CELL_SIZE
    
    # Wall teleport (only for level 1)
    if current_level == 1:
        if snake_pos[0] < 0:
            snake_pos[0] = WIDTH - CELL_SIZE
        elif snake_pos[0] >= WIDTH:
            snake_pos[0] = 0
        elif snake_pos[1] < 0:
            snake_pos[1] = HEIGHT - CELL_SIZE
        elif snake_pos[1] >= HEIGHT:
            snake_pos[1] = 0
    
    # Snake growth
    snake_body.insert(0, list(snake_pos))
    
    # Check if food is eaten
    if snake_pos == food['pos']:
        score += food['weight']
        # Check for level up (every 5 points)
        if score // 5 + 1 > current_level and current_level < 5:
            current_level += 1
            level_settings = get_level_settings(current_level)
            speed = level_settings['speed']
            walls = level_settings['walls']
        food = generate_food(snake_body, walls)
    else:
        snake_body.pop()
    
    # Remove food if more than 5 seconds passed
    if pygame.time.get_ticks() - food['spawn_time'] > 5000:
        food = generate_food(snake_body, walls)
    
    # Check collision with walls (for levels > 1)
    if current_level > 1:
        for wall in walls:
            wall_rect = pygame.Rect(wall[0], wall[1], wall[2], wall[3])
            snake_rect = pygame.Rect(snake_pos[0], snake_pos[1], CELL_SIZE, CELL_SIZE)
            if snake_rect.colliderect(wall_rect):
                game_over = True
    
    # Check collision with itself
    if snake_pos in snake_body[1:]:
        game_over = True
    
    # Check out of bounds for levels > 1
    if current_level > 1 and (snake_pos[0] < 0 or snake_pos[0] >= WIDTH or 
                              snake_pos[1] < 0 or snake_pos[1] >= HEIGHT):
        game_over = True
    
    # Rendering
    screen.fill(black)
    
    # Draw walls
    for wall in walls:
        pygame.draw.rect(screen, blue, pygame.Rect(wall[0], wall[1], wall[2], wall[3]))
    
    # Draw snake
    for block in snake_body:
        pygame.draw.rect(screen, green, pygame.Rect(block[0], block[1], CELL_SIZE, CELL_SIZE))
    
    # Draw food with color based on weight
    food_colors = {3: (255, 100, 100), 2: (255, 50, 50), 1: (200, 0, 0)}
    pygame.draw.rect(screen, food_colors[food['weight']], 
                    pygame.Rect(food['pos'][0], food['pos'][1], CELL_SIZE, CELL_SIZE))
    
    # Score and level counters
    score_text = font.render(f'Score: {score}  Level: {current_level}', True, white)
    screen.blit(score_text, (10, 10))
    
    pygame.display.flip()
    clock.tick(speed)

# Clean exit
pygame.quit()
sys.exit()