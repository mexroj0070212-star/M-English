# -*- coding: utf-8 -*-
import random
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.core.window import Window

# Oyna o'lchamini kompyuterda telefon shakliga keltirish
Window.size = (360, 640)

LEVELS = {
    "Oson": [
        ("Apple", "Olma"), ("Book", "Kitob"), ("Cat", "Mushuk"), ("Dog", "It"),
        ("Sun", "Quyosh"), ("Water", "Suv"), ("Pen", "Ruchka"), ("Car", "Mashina"),
        ("Tree", "Daraxt"), ("House", "Uy"), ("City", "Shahar"), ("Door", "Eshik"),
        ("Window", "Oyna"), ("School", "Maktab"), ("Friend", "Do'st"), ("Time", "Vaqt"),
        ("Day", "Kun"), ("Night", "Tun"), ("Food", "Taom"), ("Milk", "Sut"),
        ("Sky", "Osmon"), ("Star", "Yulduz"), ("Moon", "Oy"), ("River", "Daryo"),
        ("Sea", "Dengiz"), ("Bird", "Qush"), ("Fish", "Baliq"), ("Flower", "Gul"),
        ("Chair", "Stul"), ("Table", "Stol")
    ],
    "O'rtacha": [
        ("Ability", "Qobiliyat"), ("Accept", "Qabul qilmoq"), ("Achieve", "Erishmoq"), ("Action", "Harakat"),
        ("Active", "Faol"), ("Add", "Qo'shmoq"), ("Address", "Manzil"), ("Admit", "Tan olmoq"),
        ("Advice", "Maslahat"), ("Affect", "Ta'sir qilmoq"), ("Agency", "Agentlik"), ("Agent", "Agent"),
        ("Agreement", "Kelishuv"), ("Ahead", "Oldinda"), ("Allow", "Ruxsat bermoq"), ("Almost", "Deyarli"),
        ("Already", "Allaqachon"), ("Although", "Garchi"), ("Always", "Doim"), ("Amount", "Miqdor"),
        ("Analysis", "Tahlil"), ("Ancient", "Qadimiy"), ("Animal", "Hayvon"), ("Another", "Boshqa"),
        ("Answer", "Javob"), ("Anything", "Har qanday narsa"), ("Appear", "Paydo bo'lmoq"), ("Apply", "Murojaat qilmoq"),
        ("Approach", "Yondashuv"), ("Area", "Hudud")
    ],
    "Qiyin": [
        ("Abandon", "Tark etmoq"), ("Abundant", "Mo'l-ko'l"), ("Accelerate", "Tezlashtirmoq"), ("Accumulate", "To'plamoq"),
        ("Ambiguous", "Noaniq"), ("Anomalous", "G'ayritabiiy"), ("Benevolent", "Mehribon"), ("Candid", "Samimiy"),
        ("Capricious", "O'zgaruvchan"), ("Cognitive", "Bilishga oid"), ("Colossal", "Bahaybat"), ("Comprehensive", "Har tomonlama"),
        ("Concise", "Qisqa va lo'nda"), ("Contradict", "Inkor etmoq"), ("Cryptic", "Sirli"), ("Debilitate", "Holsizlantirmoq"),
        ("Discrepancy", "Nomuvofiqlik"), ("Eradicate", "Yo'q qilmoq"), ("Furtive", "Yashirin"), ("Gargantuan", "Juda katta"),
        ("Haphazard", "Tartibsiz"), ("Immutable", "O'zgarmas"), ("Juxtapose", "Yonma-yon qo'ymoq"), ("Labyrinth", "Labirint"),
        ("Meticulous", "Pishiq-puxta"), ("Nefarious", "Yovuz"), ("Obsolete", "Eskirgan"), ("Paradox", "Paradoks"),
        ("Quintessential", "Asosiy"), ("Resilient", "Chidamli")
    ]
}

class MobileVocabGame(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=15, spacing=10, **kwargs)

        self.level_names = ["Oson", "O'rtacha", "Qiyin"]
        self.current_level_idx = 0
        self.timer_event = None
        self.word_timer_event = None
        self.hints_left = 1

        # Sarlavha (M-English)
        self.lbl_title = Label(text="M-English", font_size='24sp', size_hint_y=0.08, bold=True, color=(0.2, 0.8, 1, 1))
        self.add_widget(self.lbl_title)

        # Rasm qo'shish (logo.png fayli shu skript yonida turishi kerak)
        self.img_logo = Image(source='logo.png', size_hint_y=0.22, allow_stretch=True)
        self.add_widget(self.img_logo)

        self.lbl_info = Label(text="", font_size='14sp', size_hint_y=0.08)
        self.add_widget(self.lbl_info)

        self.lbl_timer = Label(text="", font_size='16sp', size_hint_y=0.08, color=(1, 0.2, 0.2, 1), bold=True)
        self.add_widget(self.lbl_timer)

        # Yodlash sohasi
        self.lbl_study_words = Label(text="", font_size='18sp', size_hint_y=0.35, halign='center', valign='middle')
        self.lbl_study_words.bind(size=self.lbl_study_words.setter('text_size'))
        self.add_widget(self.lbl_study_words)

        # Test sohasi
        self.lbl_test_word = Label(text="", font_size='22sp', size_hint_y=0.15, bold=True, color=(0.2, 0.6, 1, 1))
        
        self.txt_input = TextInput(hint_text="Tarjimasini yozing...", font_size='18sp', multiline=False, size_hint_y=0.12)
        self.txt_input.bind(text=self.check_auto_answer)
        
        self.btn_hint = Button(text="💡 Yordam", font_size='16sp', size_hint_y=0.12, background_color=(0.9, 0.6, 0.1, 1))
        self.btn_hint.bind(on_press=self.use_hint)

        self.load_level_data()
        self.start_study_phase()

    def show_popup(self, title, message):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        lbl = Label(text=message, font_size='16sp', halign='center')
        lbl.bind(size=lbl.setter('text_size'))
        btn = Button(text="OK", size_hint_y=0.3, font_size='16sp')
        content.add_widget(lbl)
        content.add_widget(btn)

        popup = Popup(title=title, content=content, size_hint=(0.85, 0.4), auto_dismiss=False)
        btn.bind(on_press=popup.dismiss)
        popup.open()

    def load_level_data(self):
        current_name = self.level_names[self.current_level_idx]
        self.words = LEVELS[current_name]
        self.batch_size = 2        
        self.start_idx = 0
        self.current_word_idx = 0
        self.mission_word_count = 0  
        self.is_review_phase = False

    def reset_group_hints(self):
        if self.batch_size > 16:
            self.hints_left = 2
        else:
            self.hints_left = 1

    def start_study_phase(self):
        if self.word_timer_event:
            self.word_timer_event.cancel()

        if self.mission_word_count >= 30 or self.start_idx >= len(self.words):
            if not self.is_review_phase:
                self.show_popup("Takrorlash", "30 ta so'z tugadi! Endi ularni takrorlaymiz.")
                self.is_review_phase = True
                self.start_idx = max(0, self.start_idx - 30)
                self.batch_size = 30
                self.mission_word_count = 30
            else:
                if self.start_idx < len(self.words):
                    self.show_popup("Ajoyib!", "Keyingi 30 talik guruhga o'tamiz.")
                    self.is_review_phase = False
                    self.mission_word_count = 0
                    self.batch_size = 2
                else:
                    self.current_level_idx += 1
                    if self.current_level_idx < len(self.level_names):
                        next_lvl = self.level_names[self.current_level_idx]
                        self.show_popup("Tabriklaymiz!", f"Daraja tugadi! Keyingi bosqich: {next_lvl}")
                        self.load_level_data()
                    else:
                        self.show_popup("G'alaba!", "Barcha so'zlarni muvaffaqiyatli tugatdingiz!")
                        return

        self.reset_group_hints()

        if self.lbl_test_word in self.children:
            self.remove_widget(self.lbl_test_word)
            self.remove_widget(self.txt_input)
            self.remove_widget(self.btn_hint)

        if self.lbl_study_words not in self.children:
            self.add_widget(self.lbl_study_words)

        phase_text = "Takrorlash" if self.is_review_phase else f"Guruh: {self.batch_size} ta so'z"
        self.lbl_info.text = f"Daraja: {self.level_names[self.current_level_idx]} | {phase_text}"

        current_batch = self.words[self.start_idx : self.start_idx + self.batch_size]
        words_text = "\n".join([f"{eng} — {uz}" for eng, uz in current_batch])
        self.lbl_study_words.text = words_text

        self.time_left = 30
        if self.timer_event:
            self.timer_event.cancel()
        self.timer_event = Clock.schedule_interval(self.update_study_timer, 1)

    def update_study_timer(self, dt):
        if self.time_left > 0:
            self.lbl_timer.text = f"⏰ Yodlash vaqti: {self.time_left} soniya"
            self.time_left -= 1
        else:
            self.lbl_timer.text = "⏰ Vaqt tugadi! Sinov boshlandi!"
            self.timer_event.cancel()
            Clock.schedule_once(lambda dt: self.start_test_phase(), 1)

    def start_test_phase(self):
        if self.lbl_study_words in self.children:
            self.remove_widget(self.lbl_study_words)

        self.add_widget(self.lbl_test_word)
        self.add_widget(self.txt_input)
        self.add_widget(self.btn_hint)

        self.current_word_idx = 0
        self.load_next_test_word()

    def load_next_test_word(self):
        if self.word_timer_event:
            self.word_timer_event.cancel()

        if self.current_word_idx >= self.batch_size or (self.start_idx + self.current_word_idx) >= len(self.words):
            if not self.is_review_phase:
                self.start_idx += self.batch_size
                self.batch_size += 2
                self.mission_word_count += self.batch_size - 2
            
            self.start_study_phase()
            return

        eng, uz = self.words[self.start_idx + self.current_word_idx]
        self.test_direction = random.choice(['eng_to_uz', 'uz_to_eng'])

        if self.test_direction == 'eng_to_uz':
            self.lbl_test_word.text = f"Tarjimasi (O'zbekcha): {eng}"
            self.correct_answer = uz.lower()
        else:
            self.lbl_test_word.text = f"Tarjimasi (Inglizcha): {uz}"
            self.correct_answer = eng.lower()

        self.txt_input.text = ""

        self.word_time_left = 45
        self.word_timer_event = Clock.schedule_interval(self.update_word_timer, 1)

    def update_word_timer(self, dt):
        if self.word_time_left > 0:
            self.lbl_timer.text = f"⏰ Javob vaqti: {self.word_time_left} s"
            self.word_time_left -= 1
        else:
            self.word_timer_event.cancel()
            self.show_popup("Vaqt tugadi!", "45 soniya ichida yozmadingiz!\nGuruh boshidan boshlanadi.")
            self.current_word_idx = 0
            self.reset_group_hints()
            self.load_next_test_word()

    def check_auto_answer(self, instance, value):
        user_input = value.strip().lower()
        if hasattr(self, 'correct_answer') and user_input == self.correct_answer:
            if self.word_timer_event:
                self.word_timer_event.cancel()
            self.current_word_idx += 1
            self.load_next_test_word()

    def use_hint(self, instance):
        if self.hints_left > 0:
            self.hints_left -= 1
            # To'liq to'g'ri javobni ko'rsatish
            self.show_popup("Yordam", f"💡 To'g'ri javob: '{self.correct_answer.capitalize()}'\nQolgan yordamlar: {self.hints_left} ta")
        else:
            self.show_popup("Diqqat", "Bu guruh uchun barcha yordamlar ishlatib bo'lindi!")

class MainApp(App):
    def build(self):
        return MobileVocabGame()

if __name__ == '__main__':
    MainApp().run()