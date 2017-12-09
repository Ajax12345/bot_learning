import pygame
import pygame.gfxdraw
import numpy
import random
import classifiers.naive_bayes as naive_bayes
import classifiers.knn as knn

ball = pygame.Surface((100, 100), pygame.SRCALPHA)
pygame.gfxdraw.aacircle(ball, 50, 50, 40, (255, 0, 0))
pygame.gfxdraw.filled_circle(ball, 50, 50, 40, (255, 0, 0))
class Ball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = ball
        self.rect = self.image.get_rect(center=(150, 200))
        self.rect.x = 900
        self.rect.y = 400

class Test(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([100, 30])
        self.image.fill((131,139,139))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 100
class Floor(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([1100, 50])
        self.image.fill((131,139,139))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 500

class Body(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([100, 50])
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
class Bot:
    def __init__(self):
        self.image = pygame.image.load("/Users/jamespetullo/Desktop/maxresdefault.jpg")
        self.screen = pygame.display.set_mode((1100, 900))
        self.done = False
        self.converter = {"naive_bayes":naive_bayes.NaiveBayes, "knn":knn.KNN}
        self.floor = Floor()
        self.group = pygame.sprite.Group()
        self.group.add(self.floor)
        self.the_ball = Ball()
        self.output_converter = {b:a for a, b in {1:"successful", 0:"unsuccessful"}.items()}
        self.body1 = Body(300, 410)
        self.body2 = Body(410, 410)
        self.body3 = Body(520, 410)
        self.update_vals = [0, 0, 0]
        self.successful = True
        self.frequiency_results = {"naive_bayes":[0, 0], "knn":[0, 0]}
        self.updated = [False, False, False]
        self.t = Test()
        self.t1 = pygame.sprite.Group()
        self.t1.add(self.t)
        self.weights = [-1*random.randint(5, 70) for i in range(3)]
        self.bot = pygame.sprite.Group()
        for sprite in [self.body1, self.body2, self.body3]:
            self.bot.add(sprite)
        self.obsticle = pygame.sprite.Group()
        self.obsticle.add(self.the_ball)
        self.ranges = {0:range(300, 402), 1:range(410, 512), 2:range(520, 621)}
        self.outputed_info = False
        self.test_count = 0
        self.run_tests()
    def roll_ball(self):
        self.the_ball.rect.x -= 10
        if self.the_ball.rect.x <= 0:
            self.the_ball.rect.x = 900

    def update_weights(self, predict = False, classifier="naive_bayes"):
        if not predict:
            for i, sprite in enumerate([self.body1, self.body2, self.body3]):
                if self.the_ball.rect.x in self.ranges[i]:


                    if not self.updated[i]:

                        sprite.rect.y += self.weights[i]
                        self.updated[i] = True
                else:
                    if sprite.rect.y < 410:
                        sprite.rect.y += 10
                    self.updated[i] = False

                if self.the_ball.rect.x > 800:
                    self.outputed_info = False

                if any(pygame.sprite.collide_rect(self.the_ball, sprite) for sprite in [self.body1, self.body2, self.body3]):
                    self.successful = False
                    self.outputed_info = True


                    with open('results_from_tests.txt', 'a') as f:
                        f.write('0 '+' '.join(map(str, self.weights))+'\n')

                    break

                if self.the_ball.rect.x <= 200:
                    if not self.outputed_info:
                        if self.successful:

                            self.outputed_info = True

                            with open('results_from_tests.txt', 'a') as f:
                                f.write('1 '+' '.join(map(str, self.weights))+'\n')

                            self.successful = False
                        else:
                            self.successful = True
                    break
            self.updated = [False, False, False]
            self.weights = [-1*random.randint(30, 70) for i in range(3)]
        else:
            self.weights = [-1*random.randint(30, 70) for i in range(3)]
            current_count = 0
            while True:
                self.weights = [-1*random.randint(30, 70) for i in range(3)]
                new_val = self.converter[classifier](*self.weights, top_results=1, filename='results_from_tests.txt').output
                if self.output_converter[new_val]:
                    current_count = 0
                    self.frequiency_results[classifier] = [i+1 for i in self.frequiency_results[classifier]]
                    break

                if current_count > 20:
                    self.frequiency_results[classifier] = [self.frequiency_results[classifier][0]-1, self.frequiency_results[classifier][-1]+1]
                    current_count = 0
                    break
                current_count += 1

            for i, sprite in enumerate([self.body1, self.body2, self.body3]):
                if self.the_ball.rect.x in self.ranges[i]:


                    if not self.updated[i]:

                        sprite.rect.y += self.weights[i]
                        self.updated[i] = True
                else:
                    if sprite.rect.y < 410:
                        sprite.rect.y += 10
                    self.updated[i] = False

            self.updated = [False, False, False]


    def run_tests(self):
        while not self.done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True


            self.obsticle.update()
            self.bot.update()
            self.group.update()
            self.roll_ball()
            self.t1.update()

            if self.test_count > 700:
                print "running classifier"
                self.update_weights(predict = True)
            else:

                self.update_weights()

            self.update_weights()
            self.screen.blit(self.image, (0, 0))
            self.obsticle.draw(self.screen)
            self.bot.draw(self.screen)

            self.group.draw(self.screen)
            self.test_count += 1
            pygame.display.flip()


if __name__ == "__main__":
     b = Bot()
