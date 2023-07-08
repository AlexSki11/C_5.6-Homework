
import random

class PosError(Exception):
    pass

class ShipError(PosError):
    def __str__(self):
        return "Слишком близко"

class PosRange(PosError):
    def __str__(self):
        return "Координаты были введены неверно, не хватило места на поле"

class PosAlso(PosError):
    def __str__(self):
        return "Нельзя вводить координаты 2-а раза"


class Pos:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Ship:
    def __init__(self, pos: Pos, w, h):
        self.start_pos = pos
        self.list_pos = []
        self.w = w
        self.h = h

        if w > h:
            for i in range(pos.x, pos.x+w):
                self.list_pos.append(Pos(i, pos.y))
        elif w < h:
            for i in range(pos.y, pos.y+h):
                self.list_pos.append(Pos(pos.x, i))
        else:
            self.list_pos.append(pos)

    def check_ship(self):
        return True if self.list_pos else False

    def __eq__(self, other):
        for pos in self.list_pos:
            for other_pos in other.list_pos:
                x = abs(pos.x - other_pos.x)
                y = abs(pos.y - other_pos.y)
                if x <= 1 and y <= 1:
                    if not(x == 1 and y == 1):
                        return True

        return False

    def __ne__(self, other):
        for pos in other.list_pos:
            if not pos in self.list_pos:
                return True

    def damage(self, pos):
        self.list_pos.remove(pos)


class Player:
    def __init__(self, w, h):

        self.w = w
        self.h = h
        self.list_ship = []
        self.list_hit = []
        self.table = [["O"] * w for _ in range(h)]
        self.table_hit = [["O"] * w for _ in range(h)]
        self.status_attack = ""
        self.verb = False



    def damage(self, pos):

        ship_check = Ship(pos, 1, 1)
        self.edit_table(pos)
        for n,ship in enumerate(self.list_ship):
            if not ship != ship_check:
                ship.damage(pos)
                self.list_ship[n] = ship
                self.status_attack = "Попал"
                if not ship.check_ship():
                    if self.verb:
                        self.edit_tableDestroid(ship)
                    self.list_ship.remove(ship)
                    self.status_attack = "Корабль уничтожен"
                    return
                return
        self.status_attack = "Мимо"



    def table_app(self):
        for ship in self.list_ship:
            for pos in ship.list_pos:

                self.table[pos.x][pos.y] = chr(9632)





    def edit_table(self, pos):
        if self.table[pos.x][pos.y] == chr(9632) or self.table[pos.x][pos.y] == "X":
            self.table[pos.x][pos.y] = "X"
            self.table_hit[pos.x][pos.y] = "X"
        else:
            self.table[pos.x][pos.y] = "T"
            self.table_hit[pos.x][pos.y] = "T"

    def edit_tableDestroid(self, ship:Ship):
        start_pos = ship.start_pos
        x = ship.start_pos.x
        y = ship.start_pos.y
        width = ship.w
        height = ship.h

        for w in range(0, width):
            if y - 1 != -1:
                self.edit_table(Pos(x + w, y - 1))

            if y + 1 < self.h:
                self.edit_table(Pos(x + w, y + 1))


        if x - 1 != -1:
            self.edit_table(Pos(x - 1, y))

        if x + width < self.w:
            self.edit_table(Pos(x+width, y))


        for h in range(0, height):
            if x - 1 != -1:
                self.edit_table(Pos(x - 1, y + h))

            if x + 1 < self.h:
                self.edit_table(Pos(x + 1, y + h))


        if y - 1 != -1:
            self.edit_table(Pos(x, y - 1))

        if y + height < self.h:
            self.edit_table(Pos(x, y + height))


    def add_ship(self, ship):
        for pos in ship.list_pos:
            self.check_pos(pos)
        self.check_ship(ship)
        self.list_ship.append(ship)
        self.table_app()

    def check_listShip(self):
        return False if self.list_ship else True

    def check_pos(self, pos):
        if (pos.x >= self.w or pos.y >= self.h or
                pos.x<0 or pos.y<0):
            raise PosRange
        if pos in self.list_hit:
            raise PosAlso

    def add_hit(self, pos):
        self.list_hit.append(pos)

    def check_ship(self, ship):
        if ship in self.list_ship:
            raise ShipError


class Bot(Player):
    def __init__(self, w, h, list_hitPoint):
        super().__init__(w, h)
        self.list_ship = Bot.rand_ship(list_hitPoint, w, h)
        self.table_app()



    @staticmethod
    def rand_ship(list_hitPoint, w, h):
        list_ship = []
        while list_hitPoint:
            for n in list_hitPoint:


                r = random.randint(0, 1)
                if r == 1:
                    width = n
                    height = 1
                    x = random.randint(0, w - n)
                    y = random.randint(0, h - 1)
                else:
                    width = 1
                    height = n
                    x = random.randint(0, w - 1)
                    y = random.randint(0, h - n)

                pos = Pos(x, y)
                ship = Ship(pos, width, height)

                if not ship in list_ship:
                    list_ship.append(ship)
                    list_hitPoint.remove(n)

        return list_ship

    def hit(self):
        while(True):
            x = random.randint(0, self.w - 1)
            y = random.randint(0, self.h - 1)
            pos = Pos(x, y)
            if not (pos in self.list_hit):
                self.list_hit.append(pos)
                return pos



class GameEvent:
    EVENT_NONE = 0
    EVENT_APP = 1
    EVENT_HIT = 2
    EVENT_BOT_HIT = 3
    EVENT_RAND = 4


    def __init__(self, type, data):
        self.type = type
        self.data = data

    def get_type(self):
        return self.type

    def get_data(self):
        return self.data

class GameLogic:

    def __init__(self, w, h, list_hitPoint):
        self.w = w
        self.h = h
        self.player = Player(w,h)
        self.list_hitPoint = list_hitPoint.copy()
        self.bot = Bot(w, h, list_hitPoint)



    def event_process(self, event:GameEvent):

        if event.type == GameEvent.EVENT_APP:
            self.player.add_ship(event.data)
        elif event.type == GameEvent.EVENT_HIT:
            self.player.check_pos(event.data)
            self.player.add_hit(event.data)
            self.bot.damage(event.data)
        elif event.type == GameEvent.EVENT_BOT_HIT:
            data = self.bot.hit()
            self.player.damage(data)
        elif event.type == GameEvent.EVENT_RAND:
            list_ship = Bot.rand_ship(self.list_hitPoint, self.w, self.h)
            for ship in list_ship:
                self.player.add_ship(ship)


    def get_table(self):
        return self.player.table

    def get_tableHit(self):
        return self.bot.table_hit

    def player_win(self):
        return self.bot.check_listShip()

    def bot_win(self):
        return self.player.check_listShip()

    def get_statusAttack(self):
        return self.bot.status_attack

    def set_verb(self):
        if not self.bot.verb:
            self.bot.verb = True
        else:
            self.bot.verb = False

class ConsoleGUI:

    def __init__(self, logic:GameLogic):
        self.logic = logic


    def run(self):
        game_continue = True
        print("МОРСКОЙ БОЙ")



        self.phase_0()
        print(f"Расположите корабли на поле размером {self.logic.w}x{self.logic.h}")
        self.phase_1(self.choise_orientation())
        self.phase_2()





# Можно было-бы воспользоваться str
    def print_table(self, table):
        print("   |", end="")

        for i in range(len(table)):
            print(f" {i} |", end="")

        print()

        for y in range(len(table)):
            print(f" {y} |", end=" ")
            for x in range(len(table)):
                print(table[x][y], end=" | ")
            print()
        print()

    def phase_0(self):
        print("Включить помощь?")
        print("Показывать соседние клетки рядом с подбитыми кораблями")
        print("Эти клетки не будут считаться как задетые")
        print("1 - Да")
        print("2 - Нет")
        i = input(":")
        while i != "1" and i != "2":
            print("Ошибка! Повторите")
            i = input(": ")

        if i == "1":
            self.logic.set_verb()




    def phase_1(self,x):
        if x == "4":
            self.add_ship_rand()
            return
        print("Фаза 1, размещение юнитов")
        print("Пример ввода координат")
        print(":0 3")
        print(":5 0")
        print("Корабли должны быть друг от друга на растоянии 1 клетки")
        print("Но могут быть соседями по диагонали")

        if x == "1":
            self.add_ship_w()
        elif x == "2":
            self.add_ship_h()
        elif x == "3":
            self.add_ship()

    def phase_2(self):
        print("Фаза 2")
        print("Соперник готов")
        print("Введите координаты атаки")
        print("Пример")
        print(":0 0")
        print(":3 5")
        print("Нельзя стрелять 2-а раза в одно и тоже место")
        game_continue = True
        while game_continue:
            self.attack()

            if self.logic.player_win():
                text = "Player WIN!"
                game_continue = False  # break
            self.attack_bot()
            if self.logic.bot_win():
                text = "BOT WIN!!! My apologize"
                game_continue = False
            self.print_table(self.logic.get_table())
            self.print_table(self.logic.get_tableHit())
            print(self.logic.get_statusAttack())

        print(text)

    def choise_orientation(self):
        print("Выберите 1 вариант")
        print("1 - Все корабли будут горизонтально")
        print("2 - Вертикально")
        print("3 - Для каждого выберу сам")
        print("4 - Случайно")
        x = ""
        while (x != "1" and x != "2" and x != "3" and x!= "4"):
            x = input(":")

        return x

    def add_ship(self):
        for count in self.logic.list_hitPoint:
            print(f"Корабль размером {count}")
            if count != 1:
                print("Выберите ориентацию")
                print("1 - горизонтальная")
                print("2 - вертикальная")
            i = ""
            while True:
                try:
                    while (i != "1" and i != "2" and count != 1):
                        i = input(":")
                    print(f"Введите координаты")
                    x, y = list(map(int, input(":").split()))
                    pos = Pos(x, y)
                    if i == "1":
                        ship = Ship(pos, w=count, h=1)
                        event = GameEvent(GameEvent.EVENT_APP, ship)
                        self.logic.event_process(event)
                        self.print_table(self.logic.get_table())
                        break
                    else:
                        ship = Ship(pos, w=1, h=count)

                        event = GameEvent(GameEvent.EVENT_APP, ship)
                        self.logic.event_process(event)
                        self.print_table(self.logic.get_table())
                        break
                except ShipError as e:
                    print(e)
                    continue
                except ValueError:
                    print("Неверно повторите ввод")
                    print("Пример:3 2")
                    continue


    def add_ship_w(self):
        for w in self.logic.list_hitPoint:
            print(f"Введите координаты для корабля размером {w}")
            while True:
                try:
                    x, y = list(map(int, input(":").split()))
                    pos = Pos(x, y)
                    ship = Ship(pos, w=w, h=1)
                    event = GameEvent(GameEvent.EVENT_APP, ship)
                    self.logic.event_process(event)
                    self.print_table(self.logic.get_table())
                except ShipError as e:
                    print(e)
                    continue
                except PosError as e:
                    print(e)
                    continue
                except ValueError:
                    print("Неверно повторите ввод")
                    print("Пример:3 2")
                    continue

    def add_ship_h(self):
        for h in self.logic.list_hitPoint:
            print(f"Введите координаты для корабля размером {h}")
            while True:
                try:
                    x, y = list(map(int, input(":").split()))
                    pos = Pos(x, y)
                    ship = Ship(pos, w=1, h=h)
                    event = GameEvent(GameEvent.EVENT_APP, ship)
                    self.logic.event_process(event)
                    self.print_table(self.logic.get_table())
                    break
                except ShipError as e:
                    print(e)
                    continue
                except PosError as e:
                    print(e)
                    continue
                except ValueError:
                    print("Неверно повторите ввод")
                    print("Пример:3 2")
                    continue

    def add_ship_rand(self):
        event = GameEvent(GameEvent.EVENT_RAND, data = None)
        self.logic.event_process(event)
        self.print_table(self.logic.get_table())

    def attack(self):

        while True:
            try:
                x, y = list(map(int, input(":").split()))
                event = GameEvent(GameEvent.EVENT_HIT, data=Pos(x, y))
                self.logic.event_process(event)
                break
            except PosAlso as e:
                print(e)
                continue
            except PosError as e:
                print(e)
                continue
            except ValueError:
                print("Ошибка, повторите ввод")
                continue



    def attack_bot(self):
        event = GameEvent(GameEvent.EVENT_BOT_HIT, data = None)
        self.logic.event_process(event)

def main():
    list_hitPoint = [3, 2, 2, 1, 1, 1, 1]
    w = 6
    h = 6

    logic = GameLogic(w, h, list_hitPoint)

    GUI = ConsoleGUI(logic)
    GUI.run()

if __name__ == "__main__":
    main()


