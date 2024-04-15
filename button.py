import pygame.font

class Button():

    def __init__(self, ai_settings, screen, msg):
        '''Initialize button attributes'''
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # Set dimensions and properties of button
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        #Buid the button's rect object and center it
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        self.msg = msg
        self.play_img = self.prep_msg('Play')
        self.resume_img = self.prep_msg('Resume')
        #The button message needs to be prepped only once
        #self.prep_msg(msg)
    
    def prep_msg(self, msg):
        '''Turn msg into a rendered image and center text on the button'''
        msg_image = self.font.render(msg, True, self.text_color,
                                          self.button_color)
        msg_image_rect = msg_image.get_rect()
        msg_image_rect.center = self.rect.center
        return (msg_image, msg_image_rect)
    
    def draw_button(self):
        # Draw blank button and then draw message
        (image, image_rect) = self.play_img if(self.msg == 'Play') else self.resume_img
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(image, image_rect)