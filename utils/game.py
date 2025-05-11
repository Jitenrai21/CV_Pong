import pygame
import sys, os
import random

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import clamp

# Game Settings
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 120  # Increased for easier hits
BALL_SIZE = 20
PADDLE_SPEED = 10
BALL_SPEED_X = 4
BALL_SPEED_Y = 4
SPEED_INCREMENT = 0.5  # Speed increase after each paddle hit

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)  # For visual debugging


class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)

    def move(self, y):
        """Move paddle, ensuring it stays within bounds."""
        self.rect.y = clamp(y, 0, WINDOW_HEIGHT - PADDLE_HEIGHT)

    def draw(self, surface):
        pygame.draw.rect(surface, WHITE, self.rect)


class Ball:
    def __init__(self):
        self.rect = pygame.Rect(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, BALL_SIZE, BALL_SIZE)
        self.dx = BALL_SPEED_X
        self.dy = BALL_SPEED_Y
        self.speed_x = BALL_SPEED_X  # Track base speed for resets
        self.speed_y = BALL_SPEED_Y

    def move(self):
        """Move the ball, updating its position."""
        self.rect.x += self.dx
        self.rect.y += self.dy

        # Bounce off top/bottom
        if self.rect.top <= 0 or self.rect.bottom >= WINDOW_HEIGHT:
            self.dy *= -1
            self.rect.y = clamp(self.rect.y, 0, WINDOW_HEIGHT - BALL_SIZE)

    def check_collision(self, paddle1, paddle2):
        if self.rect.colliderect(paddle1.rect) or self.rect.colliderect(paddle2.rect):
            self.dx *= -1

    def draw(self, surface, paddle1, paddle2):
        """Draw the ball, red on collision for debugging."""
        color = RED if self.rect.colliderect(paddle1.rect) or self.rect.colliderect(paddle2.rect) else WHITE
        pygame.draw.rect(surface, color, self.rect)

    def reset(self):
        """Reset ball to center with randomized direction."""
        self.rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        self.dx = random.choice([self.speed_x, -self.speed_x])
        self.dy = random.choice([self.speed_y, -self.speed_y])


class Game:
    def __init__(self):
        try:
            pygame.init()
        except pygame.error as e:
            raise RuntimeError(f"Failed to initialize Pygame: {e}")
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("CV Pong")
        self.clock = pygame.time.Clock()
        self.running = True

        self.player = Paddle(20, WINDOW_HEIGHT // 2 - PADDLE_HEIGHT // 2)
        self.opponent = Paddle(WINDOW_WIDTH - 30 - PADDLE_WIDTH, WINDOW_HEIGHT // 2 - PADDLE_HEIGHT // 2)
        self.ball = Ball()

        self.font = pygame.font.SysFont(None, 36)
        self.player_score = 0
        self.opponent_score = 0

    def update_paddle(self, new_y):
        """Update the player's paddle position."""
        self.player.move(new_y)

    def update_opponent_paddle(self, ball_y):
        """Update the opponent's paddle position with smoothing."""
        target_y = ball_y - PADDLE_HEIGHT // 2
        current_y = self.opponent.rect.y
        # Smooth movement (70% towards target per frame)
        new_y = current_y + 0.7 * (target_y - current_y)
        self.opponent.move(new_y)

    def update_score(self):
        """Update scores and reset ball if it goes out of bounds."""
        if self.ball.rect.left <= 0:
            self.opponent_score += 1
            self.ball.reset()
        elif self.ball.rect.right >= WINDOW_WIDTH:
            self.player_score += 1
            self.ball.reset()

    def draw_score(self):
        """Draw the current score."""
        score_text = self.font.render(f"{self.player_score} : {self.opponent_score}", True, WHITE)
        self.screen.blit(score_text, (WINDOW_WIDTH // 2 - score_text.get_width() // 2, 20))

    def run(self, get_hand_y=None):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Update paddles
            if get_hand_y is not None:
                self.update_paddle(get_hand_y())
            else:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_UP]:
                    self.update_paddle(self.player.rect.y - PADDLE_SPEED)
                if keys[pygame.K_DOWN]:
                    self.update_paddle(self.player.rect.y + PADDLE_SPEED)

            self.update_opponent_paddle(self.ball.rect.centery)

            # Move ball and check collisions
            self.ball.move()
            self.ball.check_collision(self.player, self.opponent)
            self.update_score()

            # Drawing
            self.screen.fill(BLACK)
            self.player.draw(self.screen)
            self.opponent.draw(self.screen)
            self.ball.draw(self.screen, self.player, self.opponent)
            self.draw_score()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()