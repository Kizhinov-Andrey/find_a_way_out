import tkinter
import random


def create_extinguisher():
    global extinguisher, have_sth
    have_sth = True
    extinguisher_pos = another_pos()
    extinguisher = canvas.create_image(
        (extinguisher_pos[0], extinguisher_pos[1]), image=extinguisher_pic, anchor='nw')


def create_snowflake():
    global snowflake, have_sth
    have_sth = True
    snowflake_pos = another_pos()
    snowflake = canvas.create_image(
        (snowflake_pos[0], snowflake_pos[1]), image=snowflake_pic, anchor='nw')


def create_gun():
    global gun, have_sth
    have_sth = True
    gun_pos = another_pos()
    gun = canvas.create_image(
        (gun_pos[0], gun_pos[1]), image=gun_pic, anchor='nw')


def check_separately(cords):
    do = False
    change = []
    for e in cords:
        if cords.count(e) > 1:
            change.append(e)
            do = True
    if do:
        for enemy in enemies:
            if canvas.coords(enemy[0]) in change:
                direction = enemy[1](enemy[0])
                move_wrap(enemy[0], direction)
                break


def another_pos():
    obj_pos = (random.randint(1, n_x - 1) * step,
               random.randint(1, n_y - 1) * step)
    while obj_pos in cords:
        obj_pos = (random.randint(1, n_x - 1) * step,
                   random.randint(1, n_y - 1) * step)
    cords.append(obj_pos)
    return obj_pos


def move_enemy(enemy):
    player_pos = canvas.coords(player)
    enemy_pos = canvas.coords(enemy)
    diff = -1
    ans = -1
    perhaps = [(-step, 0), (step, 0), (0, -step), (0, step)]
    for i in range(4):
        c = False
        for el in fires + enemies + [exit]:
            if [enemy_pos[0] + perhaps[i][0], enemy_pos[1] + perhaps[i][1]] == canvas.coords(el):
                c = True
                break
        if c:
            continue
        check = abs(player_pos[0] - (enemy_pos[0] + perhaps[i][0])) + abs(
            player_pos[1] - (enemy_pos[1] + perhaps[i][1]))
        if diff >= 0 and check < diff:
            diff = check
            ans = i
        elif diff < 0:
            diff = check
            ans = i
    if ans == -1:
        return 0, 0
    return perhaps[ans]


def do_nothing(event):
    if event.keysym == 'space':
        prepare_and_start()
    else:
        pass


def move_wrap(obj, move):
    canvas.move(obj, move[0], move[1])
    x = canvas.coords(obj)[0]
    y = canvas.coords(obj)[1]
    if x == -step:
        x = n_x * step - step
    elif x == n_x * step:
        x = 0
    elif y == -step:
        y = n_y * step - step
    elif y == n_y * step:
        y = 0
    canvas.coords(obj, (x, y))


def check_move():
    global keys, have_sth, gun, m_e, snowflake, extinguisher
    if canvas.coords(player) == canvas.coords(exit):
        label.config(text="Победа!")
        master.bind("<KeyPress>", do_nothing)
    for f in fires:
        if canvas.coords(player) == canvas.coords(f):
            label.config(text="Ты проиграл!")
            master.bind("<KeyPress>", do_nothing)
    for e in enemies:
        if canvas.coords(player) == canvas.coords(e[0]):
            label.config(text="Ты проиграл!")
            master.bind("<KeyPress>", do_nothing)
    if gun:
        if canvas.coords(player) == canvas.coords(gun):
            canvas.delete(gun)
            canvas.delete(enemies[0][0])
            del enemies[0]
            keys = []
            have_sth = False
            gun = False
    if snowflake:
        if canvas.coords(player) == canvas.coords(snowflake):
            canvas.delete(snowflake)
            m_e = 3
            keys = []
            have_sth = False
            snowflake = False
    if extinguisher:
        if canvas.coords(player) == canvas.coords(extinguisher):
            canvas.delete(extinguisher)
            canvas.delete(fires[0])
            del fires[0]
            keys = []
            have_sth = False
            extinguisher = False


def key_pressed(event):
    global m_e
    needed_sym = False
    if event.keysym == 'Up' or event.keycode == 87:
        move_wrap(player, (0, -step))
        needed_sym = True
    elif event.keysym == 'Down' or event.keycode == 83:
        move_wrap(player, (0, step))
        needed_sym = True
    elif event.keysym == 'Left' or event.keycode == 65:
        move_wrap(player, (-step, 0))
        needed_sym = True
    elif event.keysym == 'Right' or event.keycode == 68:
        move_wrap(player, (step, 0))
        needed_sym = True
    elif event.keysym == 'space':
        prepare_and_start()
    if needed_sym:
        if not have_sth:
            keys.append(1)
        if len(keys) == bonus:
            fun = random.choice([create_gun, create_snowflake, create_extinguisher])
            do = False
            if fun == create_gun and not have_sth and enemies:
                fun()
            else:
                do = True
                fun = random.choice([create_snowflake, create_extinguisher])
            if do:
                if fun == create_snowflake and enemies and not have_sth:
                    fun()
                elif not have_sth:
                    create_extinguisher()

        enemies_cord = []
        if m_e <= 0:
            for enemy in enemies:
                direction = enemy[1](enemy[0])
                move_wrap(enemy[0], direction)
                enemies_cord.append(canvas.coords(enemy[0]))
            check_separately(enemies_cord)
            check_separately(enemies_cord)
        else:
            m_e -= 1
        check_move()


def prepare_and_start():
    global player, exit, fires, enemies, cords, have_sth, keys, gun, snowflake, m_e, extinguisher
    m_e = 0
    extinguisher = False
    gun = False
    snowflake = False
    have_sth = False
    keys = []
    canvas.delete("all")
    cords = []
    player_pos = another_pos()
    exit_pos = another_pos()
    player = canvas.create_image(
        (player_pos[0], player_pos[1]), image=player_pic, anchor='nw')
    exit = canvas.create_image(
        (exit_pos[0], exit_pos[1]), image=exit_pic, anchor='nw')
    n_fires = 6
    fires = []
    for i in range(n_fires):
        fire_pos = another_pos()
        fire = canvas.create_image(
            (fire_pos[0], fire_pos[1]), image=fire_pic, anchor='nw')
        fires.append(fire)
    n_enemies = 4
    enemies = []
    for i in range(n_enemies):
        enemy_pos = another_pos()
        enemy = canvas.create_image(enemy_pos, image=enemy_pic, anchor='nw')
        enemies.append((enemy, move_enemy))
    label.config(text="Найди выход!")
    master.bind("<KeyPress>", key_pressed)


step = 60
n_x = 10
n_y = 10
bonus = 5
master = tkinter.Tk()
player_pic = tkinter.PhotoImage(file="images/player.gif")
fire_pic = tkinter.PhotoImage(file="images/fire.gif")
exit_pic = tkinter.PhotoImage(file='images/exit.gif')
enemy_pic = tkinter.PhotoImage(file='images/enemy.gif')
gun_pic = tkinter.PhotoImage(file='images/gun.gif')
snowflake_pic = tkinter.PhotoImage(file='images/snowflake.gif')
extinguisher_pic = tkinter.PhotoImage(file='images/extinguisher.gif')
label = tkinter.Label(master, text="Найди выход")
label.pack()
canvas = tkinter.Canvas(master, bg='blue',
                        height=n_x * step, width=n_y * step)
canvas.pack()
restart = tkinter.Button(master, text="Начать заново",
                         command=prepare_and_start)
restart.pack()
prepare_and_start()
master.mainloop()
