import random
import sys
import pygame
import os

pygame.init()
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700

bottom_y = SCREEN_HEIGHT - 100

btn_size = (220,70)



#Importing assets section (memory go brr)
idle_boy = [
  pygame.image.load("boy1.png"),
  pygame.image.load("boy1_1.png"),
]
image_sprite = [
    pygame.image.load("boy2.png"),
    pygame.image.load("boy3.png"),
]
target_sprites = [
    pygame.transform.scale(pygame.image.load("itm1.png"), (40,40)),
    pygame.transform.scale(pygame.image.load("itm2.png"), (40,40)),
    pygame.transform.scale(pygame.image.load("itm3.png"), (40,40)),
]
current_target_sprite = random.randint(0, len(target_sprites)-1)
start_menu_sprites = [
  pygame.transform.scale(pygame.image.load("start_m.png"), (1200,700)),
  pygame.transform.scale(pygame.image.load("start_m1.png"), (1200,700)),
]

start_menu_index = 0
start_menu_timer = 0
speed_btn =pygame.transform.scale(
     pygame.image.load("speed.png"), btn_size
)

jump_btn = pygame.transform.scale(
    pygame.image.load("jump.png"), btn_size
)

multiplier_btn = pygame.transform.scale(
    pygame.image.load("rate.png"), btn_size
)
macondo = pygame.image.load("macondo.png")
heart_red = pygame.image.load("heart_r.png")
heart_grey = pygame.image.load("heaart_g.png")
retry_button = pygame.image.load("retry.png")
lvl_up_image = pygame.image.load("level_up.png")
lvl_up_image = pygame.transform.scale(lvl_up_image, (400,100))

banner_timer = 0
banner_duration = 1000
banner_flash_interval = 200

bg_1 = pygame.image.load("bg_1.png")
bg_2 = pygame.image.load("bg_2.png")

evil_img = pygame.image.load("evil.png")
evil_img = pygame.transform.scale(evil_img, (180,180))
Start_size = (200 , 60)
Start_hover_size = (250,80)
start_btn_original = pygame.image.load("start.png")
start_btn = pygame.transform.scale(start_btn_original,Start_size)


evils = []
last_evil_spawn = pygame.time.get_ticks()






heart_red = pygame.transform.scale(heart_red, (40,40))
heart_grey = pygame.transform.scale(heart_grey, (40,40))
retry_button = pygame.transform.scale(retry_button, (250, 80))
bg_1 = pygame.transform.scale(bg_1, (SCREEN_WIDTH, SCREEN_HEIGHT))
bg_2 = pygame.transform.scale(bg_2, (SCREEN_WIDTH, SCREEN_HEIGHT))
jump= pygame.mixer.Sound("Jump.wav")
collect= pygame.mixer.Sound("Collect.wav")
hurt = pygame.mixer.Sound("Hurt.wav")



speed_btn_rect = speed_btn.get_rect(center = (SCREEN_WIDTH//4, bottom_y))
jump_btn_rect =jump_btn.get_rect(center= (SCREEN_WIDTH//2, bottom_y))
multiplier_btn_rect = multiplier_btn.get_rect(center= (3 *SCREEN_WIDTH//4, bottom_y))



value = 0
moving = False
animation_timer = 0
#fonts go hard :isob:

splash_font = pygame.font.Font("Pixel.ttf", 50)
font = pygame.font.Font("Pixel.ttf", 36)
pause_font = pygame.font.Font("Pixel.ttf", 64)
game_over_font = pygame.font.Font("Pixel.ttf", 80)
small_font = pygame.font.Font("Pixel.ttf", 14)



screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
display_buffer = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True
dt = 0

radius = 40
player_pos = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
move_speed = 0
acceleration = 1400
base_maxspeed = 800
maxspeed = 800
friction = 2000
health = 3

y_velocity = 0
gravity = 0.8
jump_strength = 20
base_jump_strength= 20
is_jumping = False

target_x = random.randint(50, SCREEN_WIDTH - 50)
target_y = random.randint(50, SCREEN_HEIGHT - 50)
target_size = 40
target_y_velocity = 0
target_gravity = 0.2
score = 0
current_level = 1
playing_track = None  # Keeps track of what song is currently loaded

shake_timer = 0
shake_intensity = 0


in_start = True
in_shop = False
is_new_highscore  = False
highscore_message_until = 0

current_level = 1
upgrades = {"speed":1, "jump":1, "spawn":1}
total_coins = 0

def load_highscore():
  if os.path.exists("highscore.txt"):
    try:
      with open("highscore.txt", "r") as file:
        return int(file.read())
    except ValueError:
      return 0
    return 0




def save_highscore(new_high_score):
    with open("highscore.txt", "w") as file:
      file.write(str(new_high_score))

def load_points():
  if os.path.exists("points.txt"):
    try:
      with open("points.txt","r") as file:
        return int(file.read())
    except ValueError:
      return 0
  return 0

def save_points(amount):
  with open("points.txt", "w")as file:
    file.write(str(amount))

def load_upgrades():
  if os.path.exists("upgrades.txt"):
    try:
      with open("upgrades.txt","r") as file:
        lines = file.readlines
        return{
          "speed": int(lines[0].strip()),
          "jump": int(lines[1].strip()),
          "spawn": int(lines[2].strip()),
        }
    except Exception:
      return{"speed": 1, "jump":1, "spawn":1}
    return{"speed": 1, "jump":1, "spawn":1}

def save_upgrades():
  with open("upgrades.txt", "w") as file:
    file.write(f"{upgrades['speed']}\n{upgrades['jump']}\n{upgrades['spawn']}")

high_score = load_highscore()
total_coins = load_points()
upgrades=load_upgrades()

def get_upgrade_cost(level):
  return int(15 * (1.5 **(level-1)))

def apply_upgrades():
  global maxspeed, jump_strength
  maxspeed = base_maxspeed + (upgrades["speed"]-1)*26.6 #The max speed can be 1040 compared to the 800 base speed (idk if this is baldanced buuuut...)
  jump_strength = base_jump_strength+(upgrades["jump"]-1)*0.555 #Same thing here max move speed is 25 compared to 20

def spawn_single_target():
  return{
    "x": random.randint(50, SCREEN_WIDTH-50),
    "y": 50,
    "y_vel": 0,
    "sprite_idx": random.randint(0, len(target_sprites)-1) #used for storing which item image is spawned
  }



def reset_game():
  global score, health, player_pos, move_speed, y_velocity, is_jumping
  global target_x, target_y, target_y_velocity, game_over
  global evil, last_evil_spawn, in_start, value, animation_timer
  global current_target_sprite, is_new_highscore, highscore_message_until
  score=0
  health=3
  player_pos= pygame.Vector2(SCREEN_WIDTH/2,SCREEN_HEIGHT/2)
  move_speed=0
  y_velocity=0
  is_jumping = False
  target_count = 1 + (upgrades["spawn"]-1)//4
  active_targets = [spawn_single_target() for _ in range(target_count)]
  evils.clear
 
  last_evil_spawn = pygame.time.get_ticks()
  game_over=False
  in_start = False
  in_start = False
  in_shop = False
  is_new_highscore = False
  current_level = 1
  start_menu_index=0
  start_menu_timer=0
  current_level = 1
  playing_track = None  # keeps track of what song is currently loaded
  banner_timer = 0
  
def return_to_main_menu():
  global in_start, game_over, in_shop, playing_track
  in_start = True
  game_over = False
  in_shop = False
  playing_track=None


def trigger_shake(duration_frames, intensity):
  global shake_timer, shake_intensity
  shake_timer = duration_frames
  shake_intensity = intensity


paused = False
game_over = False




def shows_splash_screen(splash_duration):
  start_time = pygame.time.get_ticks()
  waiting = True

  while waiting:
    current_time = pygame.time.get_ticks()
    if current_time - start_time >= splash_duration:
      waiting = False

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
      if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
        waiting = False

    screen.fill("black")
    text_surface = splash_font.render(
        "Built for Macondo 2026", True, (255, 0, 0)
    )
    text_rect = text_surface.get_rect(
        center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    )

    display_buffer.fill("black")
    display_buffer.blit(text_surface, text_rect)
    screen.blit(display_buffer, (0, 0))

    pygame.display.flip()
    clock.tick(60)


shows_splash_screen(3000)

pygame.mixer.music.load("start_m.mp3")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(loops=-1, start=0.0)
playing_track = "start_m.mp3"

while running:
  start_btn_rect = start_btn.get_rect(
    center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2+50)
  )
  shop_btn_rect = pygame.Rect(
    SCREEN_WIDTH//2+20, SCREEN_HEIGHT//2 +20, 200,60
  )
  retry_rect = retry_button.get_rect(
      center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT//2 + 50)
  )
  menu_rect = pygame.Rect(
    SCREEN_WIDTH // 2 + 20, SCREEN_HEIGHT//2 +50, 200,60
  )
  if not paused and not game_over:
    current_time = pygame.time.get_ticks()

  render_offset = [0, 0]

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    if event.type == pygame.KEYDOWN:
      if (
            event.key in (pygame.K_p, pygame.K_ESCAPE)
            and not game_over
      ):
        paused = not paused
    if event.type == pygame.MOUSEBUTTONDOWN:
      if in_start and not in_shop:
        if start_btn_rect.collidepoint(event.pos):
          reset_game()
        elif shop_btn_rect.collidepoint(event.pos):
          in_shop = True

      elif in_shop:
        back_btn_rect = pygame.Rect(50,50,140,50)
        if back_btn_rect.collidepoint(event.pos):
          in_shop=False

        speed_btn = pygame.Rect(SCREEN_WIDTH//2 +150, 200, 160, 50)
        jump_btn = pygame.Rect(SCREEN_WIDTH//2 + 150, 310, 160, 50)
        multiplier_btn = pygame.Rect(SCREEN_WIDTH//2+150,420,160,50)

        if speed_btn_rect.collidepoint(event.pos) and upgrades["speed"] < 10:
          cost = get_upgrade_cost(upgrades["speed"])
          if total_coins >= cost:
            total_coins -= cost
            upgrades["speed"]+=1
            save_points(total_coins)
            save_upgrades()

        elif jump_btn_rect.collidepoint(event.pos) and upgrades["jump"] < 10:
          cost = get_upgrade_cost(upgrades["jump"])
          if total_coins >= cost:
            total_coins -= cost
            save_points(total_coins)
            save_upgrades()

        elif multiplier_btn_rect.collidepoint(event.pos) and upgrades["spawn"] < 10:
          cost = get_upgrade_cost(upgrades["spawn"])
          if total_coins >= cost:
            total_coins -= cost
            save_points(total_coins)
            save_upgrades()
      elif game_over:
        if retry_rect.collidepoint(event.pos):
          reset_game()
        elif menu_rect.collidepoint(event.pos):
          return_to_main_menu

  if in_shop:
    display_buffer.fill((20,20,35))
    shop_title= font.render( "UPGRADES SHOP", True, (255,215,0)) #Gold because macondo
    coins_surf = font.render(f"Coins: {total_coins}", True, (255,255,255))
    display_buffer.blit(shop_title, (SCREEN_WIDTH//2-130,40))
    display_buffer.blit(coins_surf, (SCREEN_WIDTH-250,40))
    

    back_btn = pygame.Rect(50,50,140,50)
    pygame.draw.rect(display_buffer, (180,50,50), back_btn, border_radius=10)
    display_buffer.blit(font.render("BACK",True,(255,255,255)), (75,57))

    categories = [
      ("Speed", "speed", 200),
      ("Jump Power", "jump", 310),
      ("Item Spawn", "item", 420),
    ]

    for label,key,y_pos in categories:
      lvl = upgrades[key]
      cost = get_upgrade_cost(lvl)

      txt = font.render(f"{label} (Lvl {lvl}/10)", True,(255,255,255))
      display_buffer.blit(txt, (150, y_pos +10))

      buy_btn = pygame.Rect(SCREEN_WIDTH//2+150, y_pos, 160,50)

      if lvl >=10:
        pygame.draw.rect(display_buffer, (80,80,80), buy_btn, border_radius=8)
        btn_txt = small_font.render("MAXED", True, (128, 0, 32))
        display_buffer.blit(btn_txt,(buy_btn.x + 40, buy_btn.y+13))
      else:
        btn_color =((40,180,40) if total_coins >= cost else (100,100,100))
        pygame.draw.rect(display_buffer, btn_color, buy_btn, border_radius=8 )
        btn_text = small_font.render(f"Buy: {cost}C", True,(255,255,255))
        display_buffer.blit(btn_txt, (buy_btn.x + 20, buy_btn.y +13))

    screen.blit(display_buffer, (0,0))
    pygame.display.flip()
    dt = clock.tick(60)/1000
    continue



  

    


    start_menu_timer += 1
    if start_menu_timer >=20:
      start_menu_index=(start_menu_index+1) % len(start_menu_sprites)
      start_menu_timer=0
    current_start_bg= start_menu_sprites[start_menu_index]
    display_buffer.blit(current_start_bg, (0,0))

    mouse_pos = pygame.mouse.get_pos()
    if start_btn_rect.collidepoint(mouse_pos):
      hover_btn = pygame.transform.scale(
        start_btn_original, Start_hover_size
      )
      hover_rect = hover_btn.get_rect(center=start_btn_rect.center)
      display_buffer.blit(hover_btn, hover_rect)
    else:
      display_buffer.blit(start_btn, start_btn_rect)

    menu_highscore_surf = font.render(
      f"High Score: {high_score}", True, (255,255,255)

    )
    menu_highscore_rect = menu_highscore_surf.get_rect(
      center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 120)
    )
    display_buffer.blit(menu_highscore_surf, menu_highscore_rect)
    screen.blit(display_buffer, (0,0))
    pygame.display.flip()
    dt = clock.tick(60) / 1000
    continue

  if current_time - last_evil_spawn >= 3000:
    
    spawn_x = random.randint(200, SCREEN_WIDTH -100)
    spawn_y = random.randint(150,300)
    evils.append({"x": spawn_x, "y": spawn_y, "y_vel": -8})
    last_evil_spawn = current_time

  if paused or game_over:
    pygame.mixer.music.pause()
  else:
    pygame.mixer.music.unpause()
  
  display_buffer.fill("purple")
  if current_level == 1:
    display_buffer.blit(bg_1, (0, 0))
  elif current_level == 2:
    display_buffer.blit(bg_2, (0,0))
  
  

  if not paused and not game_over:
    current_track = f"bg_{current_level}.mp3"
    if playing_track != current_track:
      pygame.mixer.music.load(current_track)
      pygame.mixer.music.set_volume(0.3)
      pygame.mixer.music.play(loops=-1, start=0.0)
      playing_track = current_track
    
      
    
    keys = pygame.key.get_pressed()

    image = image_sprite[value]
    image = pygame.transform.scale(image, (65, 70))
    player_half_height = image.get_height() // 2

    if (
        keys[pygame.K_SPACE]
        and not is_jumping
        and player_pos.y >= (SCREEN_HEIGHT - player_half_height - 2) #Makes the player jump by changeing
    ):
      y_velocity = -jump_strength
      jump.set_volume(0.5)
      jump.play()
      is_jumping = True

    y_velocity += gravity
    player_pos.y += y_velocity

    target_y_velocity += target_gravity
    target_y += target_y_velocity

    if keys[pygame.K_a] and player_pos.x > radius:
      move_speed -= acceleration * dt
      moving = True
    if keys[pygame.K_d] and player_pos.x < SCREEN_WIDTH - radius:
      move_speed += acceleration * dt
      moving = True

    if not keys[pygame.K_a] and not keys[pygame.K_d]:
      moving = False
      if move_speed > 0:
        move_speed = max(0, move_speed - friction * dt)
      elif move_speed < 0:
        move_speed = min(0, move_speed + friction * dt)

    move_speed = max(-maxspeed, min(move_speed, maxspeed))
    player_pos.x += move_speed * dt
    
    if moving:
      animation_timer += 1
      if animation_timer >= 12:
        value = (value + 1) % len(image_sprite)
        animation_timer = 0

    image_rect = image.get_rect(center=(int(player_pos.x), int(player_pos.y)))
    player_rect = image_rect

    if player_rect.left < 0:
      player_pos.x = player_rect.width // 2
      move_speed = max(0, move_speed)
    elif player_rect.right > SCREEN_WIDTH:
      player_pos.x = SCREEN_WIDTH - (player_rect.width // 2)
      move_speed = min(0, move_speed)

    if player_rect.bottom >= SCREEN_HEIGHT:
      player_pos.y = SCREEN_HEIGHT - player_half_height
      y_velocity = 0
      is_jumping = False
    elif player_rect.top <= 0:
      player_pos.y = player_half_height
      y_velocity = max(y_velocity, 0)

    if target_y + target_size >= SCREEN_HEIGHT:
    
      trigger_shake(10, 4)

      target_x = random.randint(50, SCREEN_WIDTH - 50)
      target_y = 50
      target_y_velocity = 0
      
      current_target_sprite = random.randint(0, len(target_sprites)-1)

      if health <= 0:
        health=0
        game_over=True
    elif target_y <= 0:
      target_y=0
      target_y_velocity = max(target_y_velocity, 0)
    
    

    target_rect = pygame.Rect(target_x, target_y, target_size, target_size)

    if player_rect.colliderect(target_rect):
      trigger_shake(15,5)
      collect.set_volume(0.5)
      collect.play()
      score += 1
      new_level = current_level
      if score>=20:
        new_level=2

      if new_level >current_level:
        current_level = new_level
        banner_timer = pygame.time.get_ticks()
      
      if score > high_score:
        high_score = score
        save_highscore(high_score) #Calling the save_highscore function to save current highscore to highscore.txt
        is_new_highscore = True


      
      target_y_velocity = 0
      target_x = random.randint(50, SCREEN_WIDTH - 50)
      target_y = 50

    for evil in evils[:]:
      evil["y_vel"] += 0.4
      evil["y"] += evil["y_vel"]

      evil_rect = pygame.Rect(evil["x"], evil["y"], 80,80)

      if player_rect.colliderect(evil_rect):
        hurt.set_volume(0.5)
        hurt.play()
        trigger_shake(12, 6)
        health -= 1
        evils.remove(evil)
        if health <= 0:
          health =0
          game_over=True
      elif evil["y"] >= SCREEN_HEIGHT:
        evils.remove(evil)



    

    if shake_timer > 0:
      render_offset[0] = random.randint(-shake_intensity, shake_intensity)
      render_offset[1] = random.randint(-shake_intensity, shake_intensity)
      shake_timer -= 1

  image = pygame.transform.scale(image_sprite[value], (65, 70))
  image_rect = image.get_rect(center=(int(player_pos.x), int(player_pos.y)))
  display_buffer.blit(image, image_rect)

  display_buffer.blit(
    target_sprites[current_target_sprite], (target_x,target_y)
  )

  for evil in evils:
    display_buffer.blit(evil_img, (evil["x"], evil["y"]))

  score_surface = font.render(f"Score: {score}", True, (0, 0, 0))
  for i in range(3):
    heart_x = SCREEN_WIDTH - 160 + (i *45)
    heart_y=20
    if i<health:
      display_buffer.blit(heart_red, (heart_x, heart_y))
    else:
      display_buffer.blit(heart_grey,(heart_x,heart_y))


  display_buffer.blit(score_surface, (20, 20))

  if banner_timer > 0:
    elapsed = pygame.time.get_ticks() - banner_timer
    if elapsed <= banner_duration:
      if (elapsed//banner_flash_interval) % 2 == 0:
        banner_rect = lvl_up_image.get_rect(center=(SCREEN_WIDTH//2, 180))
        display_buffer.blit(lvl_up_image,banner_rect)
    else:
      banner_timer = 0 
    
  


  

  screen.blit(display_buffer, render_offset)

  if paused and not game_over:
    
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 128))
    screen.blit(overlay, (0, 0))

    pause_surface = pause_font.render("GAME PAUSED", True, (255, 255, 255))
    inst_surface = font.render("Press P or ESC to resume", True, (255, 255, 255))

    screen.blit(
        pause_surface,
        (
            SCREEN_WIDTH // 2 - pause_surface.get_width() // 2,
            SCREEN_HEIGHT // 2 - 50,
        ),
    )
    screen.blit(
        inst_surface,
        (
            SCREEN_WIDTH // 2 - inst_surface.get_width() // 2,
            SCREEN_HEIGHT // 2 + 10,
        ),
    )

  if game_over:
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))

    game_over_surface = game_over_font.render("GAME OVER", True, (255, 50, 50))
    final_score_surface = font.render(f"Final Score: {score}", True, (255,255,255))
    

    screen.blit(
      game_over_surface,
      (
        SCREEN_WIDTH // 2 - game_over_surface.get_width() // 2,
        SCREEN_HEIGHT // 2 - 120,
      ),
    )
    screen.blit(
      final_score_surface,
      (
        SCREEN_WIDTH // 2 - final_score_surface.get_width() // 2,
        SCREEN_HEIGHT // 2 - 40,
      ),
    )
    if is_new_highscore:
      new_highscore_surf = font.render("NEW HIGH SCORE", True, (255, 215, 0))
      screen.blit(
        new_highscore_surf,
        (SCREEN_WIDTH//2 - new_highscore_surf.get_width()//2, SCREEN_HEIGHT// 2 +100),

      )
    else:
      gameover_highscore_surf = font.render(f"CURRENT HIGHSCORE: {high_score}", True, (200,200,200))
      screen.blit(
        gameover_highscore_surf,
        (SCREEN_WIDTH//2 - gameover_highscore_surf.get_width() // 2, SCREEN_HEIGHT//2+100),
      )
    screen.blit(retry_button, retry_rect)
  pygame.display.flip()
  dt = clock.tick(60) / 1000

pygame.quit()