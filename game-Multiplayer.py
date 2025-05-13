import pygame
import random
import cv2
from utils.multi_hand_tracker import HandTracker
from utils.utils import clamp, map_range, smooth_value

# Game Settings
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 120
BALL_SIZE = 20
PADDLE_SPEED = 10
BALL_SPEED_X = 6
BALL_SPEED_Y = 6
SPEED_INCREMENT = 0.5

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)

    def move(self, y):
        self.rect.y = clamp(y, 0, WINDOW_HEIGHT - PADDLE_HEIGHT)

    def draw(self, surface):
        pygame.draw.rect(surface, WHITE, self.rect)

class Ball:
    def __init__(self):
        self.rect = pygame.Rect(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, BALL_SIZE, BALL_SIZE)
        self.dx = BALL_SPEED_X
        self.dy = BALL_SPEED_Y
        self.speed_x = BALL_SPEED_X
        self.speed_y = BALL_SPEED_Y

    def move(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

        if self.rect.top <= 0 or self.rect.bottom >= WINDOW_HEIGHT:
            self.dy *= -1
            self.rect.y = clamp(self.rect.y, 0, WINDOW_HEIGHT - BALL_SIZE)

    def check_collision(self, paddle1, paddle2):
        if self.rect.colliderect(paddle1.rect) or self.rect.colliderect(paddle2.rect):
            self.dx *= -1
            # Increase difficulty
            self.dx += SPEED_INCREMENT if self.dx > 0 else -SPEED_INCREMENT
            self.dy += SPEED_INCREMENT if self.dy > 0 else -SPEED_INCREMENT

    def draw(self, surface, paddle1, paddle2):
        color = RED if self.rect.colliderect(paddle1.rect) or self.rect.colliderect(paddle2.rect) else WHITE
        center_x = self.rect.centerx
        center_y = self.rect.centery
        radius = BALL_SIZE // 2  # Radius is half the ball size
        pygame.draw.circle(surface, color, (center_x, center_y), radius)

    def reset(self):
        self.rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        self.dx = random.choice([self.speed_x, -self.speed_x])
        self.dy = random.choice([self.speed_y, -self.speed_y])

class Game:
    def __init__(self):
        pygame.init()
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

        self.hand_tracker = HandTracker(max_num_hands=2)  # Track up to two hands
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            raise RuntimeError("Could not open webcam")

    def update_paddle(self, new_y, paddle):
        paddle.move(new_y)

    def update_opponent_paddle(self, ball_y):
        target_y = ball_y - PADDLE_HEIGHT // 2 
        current_y = self.opponent.rect.y
        new_y = current_y + 0.2 * (target_y - current_y)  # Lower smoothing factor
        self.opponent.move(new_y)

    def update_score(self):
        if self.ball.rect.left <= 0:
            self.opponent_score += 1
            self.ball.reset()
        elif self.ball.rect.right >= WINDOW_WIDTH:
            self.player_score += 1
            self.ball.reset()

    def draw_score(self):
        score_text = self.font.render(f"{self.player_score} : {self.opponent_score}", True, WHITE)
        self.screen.blit(score_text, (WINDOW_WIDTH // 2 - score_text.get_width() // 2, 20))

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            ret, frame = self.cap.read()
            frame = cv2.flip(frame, 1)  # Flip horizontally
            if not ret:
                print("Failed to grab frame")
                self.running = False
                break

            original_height, original_width = frame.shape[:2]
            
            hand_positions, frame = self.hand_tracker.get_hand_positions(frame)

            # AFTER tracking, resize for display
            frame = cv2.resize(frame, (WINDOW_WIDTH, WINDOW_HEIGHT))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))

            self.opponent_controlled_by_hand = False  # Reset before scanning hands

            if hand_positions:
                # Ensure that the hands detected are mapped to paddles
                # if len(hand_positions) >= 1:
                #     finger_x, finger_y = hand_positions[0]
                #     try:
                #         finger_x = float(finger_x)
                #         finger_y = float(finger_y)
                #     except ValueError:
                #         continue
                #     scaled_x = int(map_range(finger_x, 0, original_width, 0, WINDOW_WIDTH))
                #     scaled_y = int(map_range(finger_y, 0, original_height, 0, WINDOW_HEIGHT))
                #     previous_y = getattr(self, 'previous_y', scaled_y)
                #     smoothed_y = smooth_value(scaled_y, previous_y, smoothing_factor=0.6)
                #     self.previous_y = smoothed_y

                #     self.update_paddle(smoothed_y - PADDLE_HEIGHT // 2, self.player)

                #     pygame.draw.circle(self.screen, (0, 255, 0), (scaled_x, int(smoothed_y)), 10)

                # if len(hand_positions) > 1:
                #     finger_x, finger_y = hand_positions[1]
                #     try:
                #         finger_x = float(finger_x)
                #         finger_y = float(finger_y)
                #     except ValueError:
                #         continue
                #     scaled_x = int(map_range(finger_x, 0, original_width, 0, WINDOW_WIDTH))

                #     scaled_y = int(map_range(finger_y, 0, original_height, 0, WINDOW_HEIGHT))
                #     previous_y2 = getattr(self, 'previous_y2', scaled_y)
                #     smoothed_y2 = smooth_value(scaled_y, previous_y2, smoothing_factor=0.6)
                #     self.previous_y2 = smoothed_y2

                #     self.update_paddle(smoothed_y2 - PADDLE_HEIGHT // 2, self.opponent)

                #     pygame.draw.circle(self.screen, (0, 255, 0), (scaled_x, int(smoothed_y)), 10)
                 for hand_x, hand_y in hand_positions:
                    try:
                        hand_x = float(hand_x)
                        hand_y = float(hand_y)
                    except ValueError:
                        continue

                    scaled_x = int(map_range(hand_x, 0, original_width, 0, WINDOW_WIDTH))
                    scaled_y = int(map_range(hand_y, 0, original_height, 0, WINDOW_HEIGHT))

                    # Determine if the hand is on the left or right half of the frame
                    if hand_x < original_width / 2:
                        # LEFT half → control player paddle
                        previous_y = getattr(self, 'previous_y', scaled_y)
                        smoothed_y = smooth_value(scaled_y, previous_y, smoothing_factor=0.6)
                        self.previous_y = smoothed_y

                        self.update_paddle(smoothed_y - PADDLE_HEIGHT // 2, self.player)

                        pygame.draw.circle(self.screen, (0, 255, 0), (scaled_x, int(smoothed_y)), 10)
                    else:
                        # RIGHT half → control opponent paddle
                        self.opponent_controlled_by_hand = True  # User takes over
                        previous_y2 = getattr(self, 'previous_y2', scaled_y)
                        smoothed_y2 = smooth_value(scaled_y, previous_y2, smoothing_factor=0.6)
                        self.previous_y2 = smoothed_y2

                        self.update_paddle(smoothed_y2 - PADDLE_HEIGHT // 2, self.opponent)

                        pygame.draw.circle(self.screen, (0, 255, 0), (scaled_x, int(smoothed_y2)), 10)
            self.update_opponent_paddle(self.ball.rect.centery)
            self.ball.move()
            self.ball.check_collision(self.player, self.opponent)
            self.update_score()

            self.screen.blit(frame_surface, (0, 0))  # Webcam feed as background

            self.player.draw(self.screen)
            self.opponent.draw(self.screen)
            self.ball.draw(self.screen, self.player, self.opponent)
            self.draw_score()

            pygame.display.flip()
            self.clock.tick(60)

        self.cap.release()
        cv2.destroyAllWindows()
        pygame.quit()

    def close(self):
        self.hand_tracker.release()

if __name__ == "__main__":
    game = Game()
    game.run()