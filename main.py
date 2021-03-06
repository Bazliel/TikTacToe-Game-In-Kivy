from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.clock import Clock

Builder.load_file('design.kv')
Window.size = (770, 600)

class Game(Widget):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.turn = 'X'
        self.ids.curr_turn.text = 'Turn: X'

    def on_press(self, obj):
        if not len(obj.text):
            obj.text = self.turn
            self.game_logic()
            self.switch_turn()
            


    def switch_turn(self):
        if self.turn == 'X':
            self.turn = 'O'
            self.ids.curr_turn.text = 'Turn: O'
        else:
            self.turn = 'X'
            self.ids.curr_turn.text = 'Turn: X'
    
    def game_logic(self):
        ids = self.ids
        message = self.turn + ': Won!'
        big_list = [[ids.b3, ids.b5, ids.b7], [ids.b1, ids.b5, ids.b9],
                    [ids.b1, ids.b2, ids.b3], [ids.b4, ids.b5, ids.b6], [ids.b7, ids.b8, ids.b9],
                    [ids.b1, ids.b4, ids.b7], [ids.b2, ids.b5, ids.b8], [ids.b3, ids.b6, ids.b9]]
        
        for i in big_list:
            if self.inner_logic(i):
                Clock.schedule_once(lambda arg: self.bug_fix(message))
                break
        else:
            if self.not_empty(ids.b1, ids.b2, ids.b3, ids.b4, ids.b5, ids.b6, ids.b7, ids.b8, ids.b9):
                Clock.schedule_once(lambda arg: self.switcher("Draw Game!"), 0.3)

    def bug_fix(self, msg):
        self.switcher(msg)

    def inner_logic(self, ls):
        if ls[0].text == ls[1].text == ls[2].text and self.not_empty(ls[0], ls[1], ls[2]):
            return True
        else:
            return False
    
    def not_empty(self, *b):
        for i in b:
            if i.text == '':
                return False
        else:
            return True

    def switcher(self, msg):
        main.manager.current = 'gameover'
        main.manager.transition.direction = 'right'
        main.gameover.ids.label.text = msg
    
    def clear_all(self):
        ids = self.ids

        ids.b1.text = ''
        ids.b2.text = ''
        ids.b3.text = ''
        ids.b4.text = ''
        ids.b5.text = ''
        ids.b6.text = ''
        ids.b7.text = ''
        ids.b8.text = ''
        ids.b9.text = ''

        self.turn = 'X'
        self.ids.curr_turn.text = 'Turn: X'


class GameOver(Widget):
    def update_text(self, msg):
        self.ids.label.text = msg

    def switch_screen(self):
        main.manager.current = 'game'
        main.manager.transition.direction = 'left'
        main.game.clear_all()


class TicTac(App):
    def build(self):
        self.manager = ScreenManager()

        self.game = Game()
        screen = Screen(name='game')
        screen.add_widget(self.game)
        self.manager.add_widget(screen)

        self.gameover = GameOver()
        screen = Screen(name='gameover')
        screen.add_widget(self.gameover)
        self.manager.add_widget(screen)

        return self.manager


if __name__ == '__main__':
    main = TicTac()
    main.run()