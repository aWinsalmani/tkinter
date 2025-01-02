import tkinter as tk

window = tk.Tk()

canvas = tk.Canvas(window, width=800, height=400, background="lightblue")
canvas.pack()

# create net
canvas.create_line(400, 250, 400, 400, width=4)

score_text = canvas.create_text(400, 20, text="Player 1: 0    Player 2: 0", font=("Arial", 16))
# create players
player1 = canvas.create_rectangle(50, 340,
                                  80, 400, fill="red")
player2 = canvas.create_rectangle(720, 340,
                                  750, 400, fill="blue")

# create ball
ball = canvas.create_oval(400,150 ,430,180, fill="white")
player1_dy = 0
player2_dy = 0
#keys
keys_pressed = set()
# identify if key is pressed
def key_pressed(event):
    keys_pressed.add(event.keysym.lower())
# identify if key is released
def key_released(event):
    keys_pressed.discard(event.keysym.lower())
# move players
def move_players():
    global player1_dy, player2_dy #added
    gravity = 1 # changed
        # Player 1 controls
    if 'a' in keys_pressed:
        canvas.move(player1, -5, 0)
    if 'd' in keys_pressed:
        canvas.move(player1, 5, 0)
    if "w" in keys_pressed and on_ground(player1): #and on_ground(player1)
        player1_dy = -15 # changed

    # Player 2 controls
    if 'j' in keys_pressed:
        canvas.move(player2, -5, 0)
    if 'l' in keys_pressed:
        canvas.move(player2, 5, 0)
    if 'i' in keys_pressed and on_ground(player2): #and on_ground(player2)
        player2_dy = -15 # changed

    player1_dy += gravity
    player2_dy += gravity
    canvas.move(player1, 0 ,player1_dy)
    canvas.move(player2, 0 ,player2_dy)
    limitation(player1)
    limitation(player2)

def limitation(player):
    global player1_dy, player2_dy # added
    x1, y1, x2, y2 = canvas.coords(player)
    if y2 >= 400:
        if player == player1:
            player1_dy = 0 # changed
        else:
            player2_dy = 0 # changed
        canvas.coords(player,x1,340,x2,400) #added
    if player == player1 and x1 < 0:
        canvas.move(player, 5, 0)
    if player == player2 and x2 > 800:
        canvas.move(player, -5, 0)
    
    if player == player1 and x2>400:
        canvas.move(player1, -5, 0)
    if player == player2 and x1 < 400:
        canvas.move(player2, 5, 0)


ball_dx = -5
ball_dy = 5
collision_cooldown = {'player1':False, 'player2':False, 'net':False} # added for stucked

def move_ball():
    global ball_dy, ball_dx, last_scorer
    x1, y1, x2, y2 = canvas.coords(ball)
    px1, py1, px2, py2 = canvas.coords(player1)
    p2x1, p2y1, p2x2, p2y2 = canvas.coords(player2)

    if x1 <= 0 or x2 >= 800:
        ball_dx = -ball_dx

    if y1 <= 0 or y2 >=400:
        if y2>= 400:
            if x1<400:
                last_scorer = 1             
            else:
                last_scorer = 0
            score_point(last_scorer)
        ball_dy = -ball_dy

    if check_collision(ball, player1):
        ball_center = (x1 + x2) / 2
        player_center = (px1 + px2) / 2
        if ball_center < player_center:  # Hit left side
            ball_dx = -abs(ball_dx)  # Move left
        else:  # Hit right side
            ball_dx = abs(ball_dx)  # Move right
        ball_dy = -abs(ball_dy)
        ball_dx *= 1.01  # Slightly increase speed
        ball_dy *= 1.01

    # Ball collision with player2
    if check_collision(ball, player2):
        ball_center = (x1 + x2) / 2
        player_center = (p2x1 + p2x2) / 2
        if ball_center < player_center:  # Hit left side
            ball_dx = -abs(ball_dx)  # Move left
        else:  # Hit right side
            ball_dx = abs(ball_dx)  # Move right
        ball_dy = -abs(ball_dy)
        ball_dx *= 1.01  # Slightly increase speed
        ball_dy *= 1.01

    elif not check_collision(ball, player2):
        collision_cooldown["player2"] = False
    if x2 >= 398 and x1 <= 402 and y2 >= 400 - 150 and not collision_cooldown["net"]:
        ball_dx = -ball_dx
        collision_cooldown["net"] = True
    elif not (x2 >= 398 and x1 <= 402 and y2 >= 400 - 150):
        collision_cooldown["net"] = False
    canvas.move(ball, ball_dx, ball_dy)

def on_ground(player):
    x1, y1, x2, y2 = canvas.coords(player)
    return y2 >= 400 - 7

def check_collision(obj1, obj2):
    x1, y1, x2, y2 = canvas.coords(obj1)
    x3, y3, x4, y4 = canvas.coords(obj2)
    return x1 < x4 and x3 < x2 and y1 < y4 and y3 < y2
score = [0,0]
last_scorer = 1
def reset_ball():
    global ball_dx, ball_dy, last_scorer
    if last_scorer == 1:
        x = 50
    else:
        x = 800 - 80
    y = 400 - 60 - 15 * 2 - 10
    canvas.coords(ball, x, y, x + 15 * 2, y + 15 * 2)
    ball_dx = ball_dx * (-1 if last_scorer == 1 else 1)
    ball_dy = ball_dy

def score_point(player):
    global score, last_scorer, ball_dx, ball_dy
    score[player] += 1
    last_scorer = player
    canvas.itemconfig(score_text, text=f"Player 1: {score[0]}    Player 2: {score[1]}")
    canvas.create_text(400, 200, text="Goal!", fill="gold")
    window.after(1000, reset_after_goal)

def reset_after_goal():
    canvas.delete("all")
    # Redraw net
    canvas.create_line(400, 200, 400, 400, width=4)
    # Redraw players
    global player1, player2
    player1 = canvas.create_rectangle(50, 400 - 60, 50 + 30, 400, fill="red")
    player2 = canvas.create_rectangle(800 - 80, 400 - 60, 800 - 80 + 30, 400, fill="blue")
    # Redraw ball
    global ball, ball_dx, ball_dy
    ball = canvas.create_oval(0, 0, 15 * 2, 15 * 2, fill="white")
    reset_ball()
    # Redraw score
    global score_text
    score_text = canvas.create_text(800 / 2, 20, text=f"Player 1: {score[0]}    Player 2: {score[1]}", font=("Arial", 16))



def game():
    move_players()
    move_ball()
    window.after(20, game)

window.bind("<KeyPress>", key_pressed)
window.bind("<KeyRelease>", key_released)

game()

window.mainloop()
