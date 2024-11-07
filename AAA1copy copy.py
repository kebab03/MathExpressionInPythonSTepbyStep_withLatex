import os
os.environ['KIVY_NO_CONSOLELOG'] = '1'

import logging
logging.getLogger().setLevel(logging.ERROR)
logging.getLogger("matplotlib").setLevel(logging.ERROR)
logging.getLogger("PIL").setLevel(logging.ERROR)

from kivy.config import Config

# 0 being off 1 being on as in true / false
# you can use 0 or 1 && True or False
Config.set('graphics', 'resizable', True)
import warnings
warnings.filterwarnings("ignore")

from kivy.logger import Logger
Logger.setLevel(logging.ERROR)
from kivymd.app import MDApp  # Usa MDApp anziché App
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle
from kivymd.uix.button import MDFillRoundFlatButton
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.textfield import MDTextField

from kivy.core.window import Window
import matplotlib.pyplot as plt
from io import BytesIO
from kivy.core.image import Image as CoreImage
from kivy.uix.anchorlayout import AnchorLayout
from kivy.graphics import Color, Rectangle
from kivy.uix.floatlayout import FloatLayout
import operator
from kivy.metrics import dp  # Aggiungi questa riga
from kivy.core.window import Window  # Aggiungi questa riga
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
import re
from math import gcd
import math
from fractions import Fraction
import sqlite3
plt.rcParams.update({
    "text.usetex":False,
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial"],
})

def rgb(r,g,b):    
    return round(r / 255, 2), round(g / 255, 2), round(b / 255, 2), 1

class BackgroundLayout(AnchorLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(size=self._update_rect, pos=self._update_rect)

        with self.canvas.before:
            bgclr = rgb(255, 238, 0)   ###  bei blocchi nel scroll
            Color(*bgclr) ####  color of the block  sfondo in scroll 
            self.rect = Rectangle(size=self.size, pos=self.pos)
            
            
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
# Layout principale con sfondo personalizzato
class MainLayout(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Aggiungi lo sfondo personalizzato
        with self.canvas.before:
            Color(* rgb(121, 101, 214)  ),#(0.8, 0.9, 0.9, 1)  # Colore di main  sfondo (RGB normalizzato)
            self.rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self._update_rect, pos=self._update_rect)

    # Aggiorna la dimensione e la posizione dello sfondo quando il layout cambia
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


# App principale che eredita da MDApp
class myApp(MDApp):
    def build(self):
        self.create_database()
        main_layout = MainLayout()
        largherzza =0.9 ##   dei piccoli blocchi 
        self.title_label = MDLabel(
            text="inserisci qui sotto",
            halign="center",
            theme_text_color="Primary",
            font_style="H6",
            pos_hint={"center_x": 0.5, "top": 1.45}
        )
        main_layout.add_widget(self.title_label)

        username_container = MDCard(
            size_hint=(None, None),
            size=(Window.width * 0.8, dp(50)),
            md_bg_color=(0, 0.9, 0.9, 1),
            padding=(dp(10), 0),
            pos_hint={"center_x": 0.5, "top": .9}
        )
        # Usa il parametro `height` come numero anziché stringa e imposta `size_hint_y`
        self.entry = TextInput(
            hint_text='inserisci qui Espressione 5+9',
            
            size_hint=(None, None),
            size=(Window.width * largherzza , dp(50)),
            font_size=24,
            pos_hint={"center_x": 0.5, "top": .9},
            # pos_hint={'center_x': 0.5, 'top': 0.45},
            background_color =   rgb(183, 255, 0),#(0, 0.9, 0.9, 1),  #   color of the input box
            foreground_color = rgb(8, 18, 82) #(1, 0.1, 0, 1)
        )

        #username_container.add_widget(self.entry)
        main_layout.add_widget(self.entry)
        # main_layout.add_widget(username_container)
        altezza_di_scrol = 0.7
        # Correzione per lo ScrollView e GridLayout
        self.scroll_view = ScrollView(size_hint=( largherzza, altezza_di_scrol), pos_hint={'center_x':0.5, 'top': 0.81})  ########  siz _hit  determina la size di ogni block 
        # nel scroll dei piccoli blochi 
        
        # spacing  spazio tra i piccoli blocchi nel scroll 
        self.steps_layout = GridLayout(cols=1, size_hint_y=None, height=dp(10), spacing=dp(5))  # Imposta un'altezza fissa  
        
        self.steps_layout.bind(minimum_height=self.steps_layout.setter('height'))  # Assicurati che l'altezza si adatti al contenuto
        self.scroll_view.add_widget(self.steps_layout)
        main_layout.add_widget(self.scroll_view)

        # Aggiungi il pulsante con sfondo riempito
        button = MDFillRoundFlatButton(
            text=" Risolvi",
            pos_hint={"center_x": 0.3, "center_y": 0.06},
            font_size = '40dp',
            size_hint=(0.3, 0.1)
        )
        main_layout.add_widget(button)

        button.bind(on_press=self.prepara_risoluzione)

        self.next_button = MDFillRoundFlatButton(
            text="Prossimo Passo",
            md_bg_color = "#D600CF",#"F86FFF",#"red",
            pos_hint={"center_x": 0.7, "center_y": 0.06},
            font_size = '30dp',
            size_hint=(0.3, 0.1)
        )
        self.next_button.bind(on_press=self.mostra_prossimo_passo)
        main_layout.add_widget(self.next_button)
        self.passo_corrente = 0
        self.images = []
        return main_layout
    
    
    
    
    
    def create_database(self):
        # Connessione al database SQLite e creazione della tabella
        self.conn = sqlite3.connect("counter.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Counter (
                id INTEGER PRIMARY KEY,
                value INTEGER NOT NULL
            )
        """)
        self.conn.commit()
    
    
    def load_counter(self):
        # Carica il valore del contatore dal database; se non esiste, lo imposta a 0
        self.cursor.execute("SELECT value FROM Counter WHERE id = 1")
        result = self.cursor.fetchone()
        if result:
            self.counter_text = str(result[0])
            return str(result[0])
        else:
            self.counter_text = "0"
            self.cursor.execute("INSERT INTO Counter (id, value) VALUES (1, 0)")
            self.conn.commit()

    def increment_counter(self):
        # Incrementa il contatore, aggiorna l'interfaccia e salva nel database
        current_value = int(self.counter_text) + 1
        self.counter_text = str(current_value)
        self.cursor.execute("UPDATE Counter SET value = ? WHERE id = 1", (current_value,))
        self.conn.commit()
    
    
    def valuta_espressione(self, espressione):
        print(f" line 168   valuta_espressione espressione: {espressione}")
        operatori = {'+': operator.add, '-': operator.sub, '*': operator.mul, '/': operator.truediv, '^': math.pow}
        
        # Separa i numeri e gli operatori, mantenendo i segni
        parti = re.findall(r'(-?\d+(/\d+)?|\^|\*|/|\+|-)', espressione)
        parti = [p[0] for p in parti]
        print(f" line 174   valuta_espressione parti: {parti}")
        
        # Gestisci le potenze
        i = 0
        while i < len(parti):
            if parti[i] == '^':
                print(f" line 180   potenze  valuta_espressione parti[i]: {parti[i]}")
                base = self.parse_frazione(parti[i-1])
                esponente = self.parse_frazione(parti[i+1])
                risultato = Fraction(operatori['^'](float(base), float(esponente)))
                parti[i-1:i+2] = [str(risultato)]
                i -= 1
            i += 1
        
        # Gestisci moltiplicazioni e divisioni
        i = 0
        while i < len(parti):
            if parti[i] in ['*', '/']:
                print(f" line 192   moltiplicazioni e divisioni  valuta_espressione parti[i]: {parti[i]}")
                a = self.parse_frazione(parti[i-1])
                b = self.parse_frazione(parti[i+1])
                risultato = operatori[parti[i]](a, b)
                parti[i-1:i+2] = [str(risultato)]
                i -= 1
            i += 1
        
        # Gestisci addizioni e sottrazioni
        risultato = self.parse_frazione(parti[0])
        for i in range(1, len(parti), 2):
            print(f" line 203   addizioni e sottrazioni  valuta_espressione parti[i]: {parti[i]}")
            operatore = parti[i]
            numero = self.parse_frazione(parti[i+1])
            risultato = operatori[operatore](risultato, numero)
        
        print(f" line 208   valuta_espressione risultato: {risultato}")
        return risultato    
    global pos_di_graf_da_sot  # Dichiarazione della variabile globale
    pos_di_graf_da_sot = []
    # **************************************************************************************************************************************************************
    def replace_fractions(self,expression,i,lungh_sostituita):
        ##**///************

        
        ##à*****************
        sta = False
        indx_partenza =i 
        lunEspress = len(expression)
        expression = expression.replace(" ", "")
        print(f"{'153 _expression_[-1] start':<30}{expression[-1]}")
            # Aggiungiamo il controllo per evitare IndexError
        if (indx_partenza>= len(expression)) or  (indx_partenza>= len(expression)-1):
            print(f"{'return expression perk indx_partenza >= len(expression) :':<30} {expression}")            
            print(f"{'136 new expression:':<30} {expression}")
        # Sstituire moltiplicazione con \times
            expression = expression.replace('*', "\\times")
            print(f"{'139 new expression:':<30} {expression}")
            return expression  # Esci dalla ricorsione se l'indice è fuori dal range
        print(f"{'167_expression_[indx_partenza+1]===':<30}{expression[indx_partenza+1]}")
        if expression[indx_partenza] is not None:
            print(f"{'20_expression_[indx_partenza]==':<30}{expression[indx_partenza]}")
        #if expression[indx_partenza] is not None:
            #print(f"{'20_expression_[indx_partenza]':<30}{expression[indx_partenza]}")
        fund_graf = None
        while i < len(expression):
            print(f"{'partenza expression:':<30} {expression}")
            # Ignora le espressioni già convertite in \frac{...}{...}
            #
            # il codice di sotto serve per ottenre  '{15/4-13/10} da '{15/4-13/10}/9/7'
            if expression[i] == r'{' :
                print(f" expression[i] =",expression[i])
                print(f" expression[i+1] =",expression[i+1])
                if "\\left" not in expression[i:] : 
                #and (expression.find('}',i+1)<expression.find('/', i+ 1)):
                    print(f"expression.find('',i+1) ",expression.find('}',i+1))
                    posizione_specifica = i                                                 # posizione_specifica   tiene  la pos
                                                                                            # di { 
                    print(f" expression.find(r' ',i+1)+1 ==",expression.find('}',i+1)+1)
                    if i< len(expression)-2  :
                        pos_di_ogg = expression.find('}',i+1)+1 # serve per trovare un oggetto  ,come * 
                        if pos_di_ogg< len(expression) :
                        #  era prima ora  forse non serve------------------ pos_di_graf_da_sot = expression[pos_di_ogg]
                            # °°°°°°°°°°°°°°° aggiunto per fare in modo che se ci sono piu un carattere * allora per 
                            # trovare l'indice di * della posizione
                            carattere = expression[pos_di_ogg]
                            conteggio_carattere = expression.count(carattere)
                            pos_di_graf_da_sot.append((expression[pos_di_ogg], conteggio_carattere))
                            # _______________________________________
                            print(f"291 pos_di_graf_da_sot = ",pos_di_graf_da_sot)
                    # Nuovo controllo per il contenuto a destra
                    contenuto_destra = expression[posizione_specifica+1:]
                    ha_numeri = any(c.isdigit() for c in contenuto_destra)
                    ha_operatori = any(op in contenuto_destra for op in '+-')
                    if ha_numeri and ha_operatori:
                        if expression.find('}',i+1)+1 == lunEspress:
                            if posizione_specifica < len(expression) and expression[posizione_specifica] == '{':
                                expression = expression[:posizione_specifica] + r'\left\{' + expression[posizione_specifica + 1:]
                            expression = expression[:expression.find('}',i+1)]+r'\right\}'
                        #if expression[0] == "{" and expression[-1]== "}" or expression[0] == "{" :
                        #    expression = expression.replace("{", "__LEFT_BRACE__").replace("}", "__RIGHT_BRACE__")
                        #     print(f"{'lin 149  __LEFT_BRACE__r:':<30} {expression}")
                        # print(f"expression.find('/',i+1) ",expression.find('/',i+1))
                # Trova la fine della frazione
                    if expression[0] == '{':
                        frac_end = expression.find('}', i + 1)
                        print(f" expression[frac_end-2:frac_end+3] :==  ",expression[frac_end-2:frac_end+3])
                        i = frac_end + 1  # Salta oltre la frazione
                        fund_graf= True  ################################### perche non lo so ma devo fare in modo  da far 
                        #partire da i  
                        continue
                    
            print(f"__32_expression[{i}] = {repr(expression[i])}")
            if expression[i] == '/' or expression[i] == ":":
                try:
                    if fund_graf :
                        print(f" expression[i:]==",expression[i:])
                        # Crea un pattern per cercare i simboli '-' o '+' dopo l'indice specificato
                        pattern = r'[-+]'  # Pattern per trovare '-' o '+'
                        # Cerca nel segmento dell'espressione a partire dall'indice iniziale
                        match = re.search(pattern, expression[i:])
                        if match:
                            # Restituisce l'indice globale del simbolo trovato
                            end = i + match.start()
                        else :
                            end = len(expression)
                        nu_of_div_sim = expression[i:end].count(r"/")
                        if nu_of_div_sim == 2:
                            left_expr = expression[i-frac_end-1:i] 
                            filtered_txt =  expression[i+1:]
                            modified_txt = r'\left\{' + left_expr[1:-1] + r'\right\}'
                            parts = filtered_txt.split('/')
                            numerator = modified_txt + '*' + parts[-1]
                            # Prendere gli intermedi come denominatore
                            denominator = '*'.join(parts[0])
                            fraction = r'\frac{' + numerator + '}{' + denominator + '}'
                            expression = fraction
                            print(f"Nuova espressione: {expression}")
                            return self.replace_fractions(expression,len(r'\left\{'+r'\frac{'),len(r'\left\{'+r'\frac{'))
                            # return replace_fractions(expression,len(r'\left\{'+r'\frac{'),0)
                            #return fraction
                except ZeroDivisionError:
                    print("Sorry ! You are dividing by zero ")
                pattern = r'^[0-9/:]+$'
                cleaned_input = expression.replace(" ", "")
                cleaned_input = cleaned_input.strip("-+")
                is_valid = bool(re.match(pattern, cleaned_input))
                print(is_valid)  # Output: True or False
                if is_valid and expression.count(r"/") > 1:
                    print("La stringa contiene solo '/'")
                    nu_of_div_sim = expression.count(r"/")
                    print(f" nu_of_div_sim =",nu_of_div_sim)
                    # _______________________________________________________________________________________
                    if nu_of_div_sim == 3:
                    # Logica per gestire il caso con tre simboli di divisione
                        parts = expression.split('/')
                        if len(parts) >= 3:
                            # Prendere il primo e l'ultimo come numeratore
                            numerator = parts[0] + '*' + parts[-1]
                            # Prendere gli intermedi come denominatore
                            denominator = '*'.join(parts[1:-1])
                            fraction = r'\frac{' + numerator + '}{' + denominator + '}'
                            expression = expression.replace('/'.join(parts), fraction, 1)
                            print(f"Nuova espressione: {expression}")
                    # _______________________________________________________________________________________
                else:
                    print("La stringa contiene altri caratteri oltre '/'")
                    num = 0  # Cambiato da self.num a num locale
                    print(f" {'i ':<30}{i}")
                    left_expr = ""
                    right_expr = ""
                    # Controlla alla sinistra del '/'
                    left_start = i - 1
                    bolean = False
                    while left_start >= 0 and expression[left_start] in '0123456789{([^}])':
                        print(f"{'187 expression[left_start]':<30}{expression[left_start]}")
                        print(f"{'190[left_start]':<30}{left_start}")
                        # -----------------------------------------------------------------------------------------
                        # first_brace = expression.find('}', start_ignore)  # Trova il primo '}'
                        # second_brace = expression.find('}', first_brace + 1)  # Trova il secondo '}'
                        # -----------------------------------------------------------------------------------------
                        if left_start==indx_partenza:
                            if num >0 and indx_partenza >11:
                                # questa parte serve per tenere conto di prime cirefre(34) come 34/4
                                if left_start+num>indx_partenza:
                                    left_start = indx_partenza
                                else:
                                    left_start=left_start+num
                                #left_start += num
                            else:
                                #left_start -= lungh_sostituita
                                # credo che avevo  fatto questo per prendere l'iniziale parentesi  di 
                                if expression.count(r"\frac{") >= 2:
                                    # rfind srve x fare all'indietrop
                                    # Supponiamo di voler cercare '}' partendo dalla posizione 15 e andando all'indietro
                                    #position = expression.rfind('}', 0, 15)
                                    #print(position)
                                    left_start=expression.rfind('(', 0,i)
                                    print(f"  left_start ===",left_start)
                                    sta = True
                                else :
                                    left_start=left_start-lungh_sostituita
                            print(f"{'439___[left_start]':<30}{left_start}")
                            print(f"{'440 e pression_[left_start]':<30}{expression[left_start]}")                
                        if expression[left_start] in '0123456789}])':
                            #break
                            #if expression[left_start] in '{([':
                            if expression[left_start] in '}])':  
                                print(f"{'445___[left_start]':<30}{left_start}")
                                print(f"{'446 -xpression_[left_start]':<30}{expression[left_start]}")                      
                                bolean =False
                                # Definire gli indici che vogliamo ignorare
                                if expression.count(r"\frac{") < 2:
                                    start_ignore = indx_partenza-lungh_sostituita
                                    end_ignore = indx_partenza
                                    print(f"{' 4m_expression_[start_ignore-1]':<30}{expression[start_ignore-1]}")
                                    print(f"{' 4m_expression_[start_ignore]':<30}{expression[start_ignore]}")
                                    print(f"{' 4m_expression_[start_ignore+1]':<30}{expression[start_ignore+1]}") 
                                    print(f"{'ignor4expression_[end_ignore]':<30}{expression[end_ignore]}")  
                                    # Costruire una stringa senza il contenuto tra start_ignore e end_ignore
                                    filtered_txt = expression[:start_ignore] + " " * (end_ignore - start_ignore) + expression[end_ignore:]
                                    print(f"{'66_len(filtered_txt)=====:=':<30} {len(filtered_txt)}")
                                    # Trovare il primo indice della parentesi graffa aperta '{' ignorando la sezione specificata
                                    # parentes_index = filtered_txt.find("{")
                                    parentes_index = min(
                                    [index for index in [
                                        filtered_txt.find("{"),
                                        filtered_txt.find("("),
                                        filtered_txt.find("[")
                                    ] if index != -1] or [len(filtered_txt)]
                                                        )
                                    left_expr = expression[indx_partenza+1:i] 
                                    print("left_expr:===============================::;;;==")
                                    print(left_expr)
                                    print(f"{'461 type(parentes_index :':<38} {type(parentes_index)}")
                                    if parentes_index>= start_ignore and left_expr is None:
                                        myParest =   end_ignore+ (parentes_index-start_ignore) 
                                        left_start = myParest-1
                                    else:
                                        if parentes_index == 0:
                                            left_start= parentes_index
                                            sta = True
                                        else:                                    
                                            left_start = parentes_index-1
                                    print(f"Indice della parentesi graffa aperta: {parentes_index}")                       
                                    x = expression.find("{")
                                    print(x)
                                else: 
                                    #################################################
                                    if r"\frac{" in expression:
                                    
                                        fractions = []  # Aggiunto per memorizzare le frazioni
                                        potenze = []
                                        positions = []  # Aggiunto per memorizzare le posizioni delle sostituzioni
                                        # Modifica del ciclo for per correggere l'errore di sintassi
                                        for i in range(expression.count(r"\frac{")):  # Cambiato per contare le occorrenze
                                            matches = re.findall(r'(\d+)\^(\d+)', expression)    
                                            for base, exponent in matches:
                                                # Sostituisce l'espressione originale con quella formattata
                                                expression = expression.replace(f"{base}^{exponent}", f"{base}^{{{exponent}}}") 
                                            minLen = len(expression)
                                            print (f" minLen = ",minLen)
                                            # Nuovo ciclo for per gestire la sostituzione dopo il primo for
                                            for match in re.finditer(r'\^', expression):
                                                start_brace = expression.find('{', match.end())
                                                end_brace = expression.find('}', start_brace)
                                                if start_brace != -1 and end_brace != -1:
                                                    # Sostituisci il contenuto tra { e }
                                                    potnz = expression[start_brace-1:end_brace+1]
                                                    potenze.append(potnz)
                                                    positions.append((start_brace-1, end_brace+1))  # Memorizza le posizioni
                                                    expression = expression[:start_brace-1] + " " * (end_brace - start_brace + 2) + expression[end_brace + 1:]
                                            try:
                                                start_ignore = expression.index(r"\frac{", i)  # Trova l'indice di inizio della frazione
                                                # Trova il secondo '}'
                                                first_brace = expression.find('}', start_ignore)  # Trova il primo '}'
                                                second_brace = expression.find('}', first_brace + 1)  # Trova il secondo '}'
                                                if second_brace != -1:  # Assicurati che il secondo '}' esista
                                                    end_ignore = second_brace
                                                    # Sostituisci il contenuto tra start_ignore e end_ignore
                                                    filtered_txt = expression[:start_ignore] + " " * (end_ignore - start_ignore + 1) + expression[end_ignore + 1:]
                                                    # Mantieni il carattere \ prima di frac
                                                    fract = expression[start_ignore:end_ignore+1]  # Non sostituire \frac
                                                    fractions.append(fract)  # Aggiunto per memorizzare la frazione nella lista
                                                    expression = filtered_txt  # Aggiorna l'espressione
                                                    i = start_ignore  # Aggiorna l'indice per continuare la ricerca
                                                else:
                                                    break 
                                            except ValueError:
                                                print("fine 24 ")
                                                break 
                                        print(f"{'lin 105  left_expr:':<30} {expression}")
                                        exprLen = len(expression)
                                        print (f" exprLen = ",exprLen)
                                        expression = expression.replace("{", "__LEFT_BRACE__").replace("}", "__RIGHT_BRACE__")
                                        print(f"{'lin 149  __LEFT_BRACE__r:':<30} {expression}")
                                        # Reinserisci le frazioni e le potenze nell'espressione
                                        for fract in fractions:
                                            expression = expression.replace(" " * len(fract), fract, 1)
                                        for i, pot in enumerate(potenze):
                                            start, end = positions.pop(0)  # Prendi la posizione della potenza
                                            try:
                                                if expression[0:0 + len("__LEFT_BRACE__")] == "__LEFT_BRACE__":  # Controlla se __LEFT_BRACE__ è all'indice 0
                                                    start += len("__LEFT_BRACE__")  # Aggiungi la lunghezza di __LEFT_BRACE__
                                                    end += len("__RIGHT_BRACE__")-2# Non fare nulla, mantenere le posizioni originali
                                                elif i > 0:  # Dalla seconda occorrenza in poi
                                                    start += len("__LEFT_BRACE__")  # Aggiungi la lunghezza di __LEFT_BRACE__
                                                    end += len("__RIGHT_BRACE__")-2   # Aggiungi la lunghezza di __RIGHT_BRACE__
                                            except IndexError:
                                                # Gestisci eventuali errori di indice
                                                print("Errore: indice non valido.")
                                            left = expression[:start]
                                            rigt =  expression[end:]
                                            expression = expression[:start] + pot + expression[end:]  # Reinserisci la potenza
                                        # Sostituisci { e } con marcatori temporanei
                                        # Esegui le sostituzioni di { e } solo dopo aver reinserito tutto
                                        filtered_txt = expression.replace("__LEFT_BRACE__", r'\left\{').replace("__RIGHT_BRACE__", r'\right\}') 
                                        # print(f"{'lin 105  left_expr:':<30} {expression}")
                                        print(f"{'lin 51  filtered_txt:':<30} {filtered_txt}")
                                        espressioneNv = filtered_txt.replace(" ", "")
                                    ###########################################################################################################
                            else:
                                num += 1  # Incrementa num locale
                                print(f"num 226 of digit: {num}")
                            if bolean:
                                if expression[left_start] in '{([+-':
                                    break
                        if expression[left_start] in '{([+-':
                                break
                        left_start -= 1
                    if  sta:
                        sta = False
                        left_start = 0
                    else:
                        left_start += 1  # Includi il primo carattere valido
                    ##  è aggiunto per tenere traccia di primi cifre che possono essere piu di 1 
                    if left_start < 0:
                        left_start = 0
                    ##
                    left_expr = expression[left_start:i]  # Prendi l'espressione a sinistra            
                    txt = left_expr
        # Sstituire     la prima e l'ultima graffa
                    if txt[0] == "{" and txt[-1]== "}" :
                            modified_txt = r'\left\{' + txt[1:-1] + r'\right\}'
                            print(modified_txt)            
                            left_expr = modified_txt
                            print(f"{'txt 101 my new :':<38} {modified_txt}")                        
                    print(f"{'lin 105  left_expr:':<30} {left_expr}")
                    """ if len(txt) >0:
                        if txt[0] == "{" and txt[-1]== "}" :
                            modified_txt = r'\left\{' + txt[1:-1] + r'\right\}'
                            print(modified_txt)            
                            left_expr = modified_txt
                            print(f"{'txt 101 my new :':<38} {modified_txt}")                        
                    print(f"{'lin 105  left_expr:':<30} {left_expr}") """
                    # Controlla alla destra del '/'
                    right_end = i + 1
                    # expression = r"46+{(9/2+2)+5}/4^2"
                    while right_end < len(expression) and expression[right_end] in '0123456789{([^':
                        print(f"{'103 expression_[right_end]':<30}{expression[right_end]}")
                        # expression = r"[(9/2+4/7)-10]*4^3"
                        if expression[right_end] in '{([^':
                            print(f"{'106 right_end:':<30} {right_end}")
                            print(f"{'107 expression_[right_end]':<30}{expression[right_end]}")   
                            right_end += 1
                        elif expression[right_end] in '0123456789^':   # mancava 0 per questo credo che avevo problemi con le frazioni che avevav 
                            #0  a denominatori  
                            print(f"{'110 expression_[right_end]':<30}{expression[right_end]}")
                            print(f"{'111  len(expression) ':<30}{  len(expression) }")                                                         
                            if  right_end<  len(expression) :
                                right_end += 1
                            print(f"{'514 right_end:':<30} {right_end}")
                            print(f"{'515 expression_[right_end]':<30}{expression[right_end-1]}")
                        else:
                            right_end += 1
                            break 
                    if expression[i+1] in '(': 
                        right_end =end_brace = expression.find(')', i) +1
                    right_expr = expression[i + 1:right_end]  # Prendi l'espressione a destra
                    print(f"{'right_expr:':<30} {right_expr}")
                    # Sostituisci la porzione trovata con \frac{left}{right}
                    fraction = r'\frac{' + left_expr + '}{' + right_expr + '}'
                    print(f"{' fraction*******:=':<30} { fraction } ")
                    #####   serve per avere gli esponenti 
                    matches = re.findall(r'(\d+)\^(\d+)', fraction)    
                    for base, exponent in matches:
                        # Sostituisce l'espressione originale con quella formattata
                        fraction = fraction.replace(f"{base}^{exponent}", f"{base}^{{{exponent}}}")                
                    #   cioè  da  "\frac{3^18}{3^16}"  ottengo  \frac{3^{18}}{3^{16}}
                    print(f"{' fraction*******:=':<30} { fraction } ")                
                    #####
                    print(f"{'289 len(fraction)=====:=':<30} {len(fraction)}")
                    expression = expression[:left_start] + fraction + expression[right_end:]
                    print(f"{'new expression:':<30} {expression}")
                    indx=i+len(fraction)-1
                    print(f"{' indx----partnza nuova-***:=':<30} { indx } ")
                    # Ripeti la sostituzione con l'espressione aggiornata
                    lungh_sostituita = len(fraction)
                    if lungh_sostituita > 11:
                        # Modifica per gestire correttamente le frazioni
                        digDsor = lungh_sostituita - 11
                        print(f"{'299 digDsor :':<30} {digDsor}")
                        indx -= digDsor  # Aggiornato per tenere conto delle frazioni
                    # Aggiunto per gestire correttamente le espressioni   come 4/5+8/9 e {4+(3^2+8/9)}
                    # altrimenti  dopo (3^2+8/9)  il risultato nella soluzione non avra {}
                    if indx < len(expression) and expression[indx] == '}' :
                        indx -= 1  # Riduci l'indice se ci sono parentesi graffe
                    return self.replace_fractions(expression, indx, lungh_sostituita)  # Ricorsione sulla nuova espressione
            else:
                i += 1
        #print(f"__536_expression[{i}] = {repr(expression[i])}")
        print(f"{'136 new expression:':<30} {expression}")
        # Sstituire moltiplicazione con \times
        ##########################################    ho modicato questo per    tenre conto di  {    ---   =  expression = expression.replace('*', '\\times')
        print(f"{'139 new expression:':<30} {expression}")
        print(f"{'633  len(expression):':<30} {len(expression)}")
        ###     ho aggiunto if solo per [8/2+6-17]
        # s non va con altri pruoi eliminare
        if i== len(expression):  
        #tx="{4+(3^2+8/9)}"
    #expresion" {4+(3^2+\frac{8}{9})}"
    ###  seve er avere { }  esterni  come {4+(3^2+8/9)} 
    # mentr prma avevo fatto per {4+(3+8/9)}/2^2
        # if r"\frac{" in expression:
        # if re.findall(r'\\frac{(\d+)', expression):
            if not re.findall(r'\\frac{(?!\\frac{)', expression):  
                fractions = []  # Aggiunto per memorizzare le frazioni
                potenze = []
                positions = []  # Aggiunto per memorizzare le posizioni delle sostituzioni
                # Modifica del ciclo for per correggere l'errore di sintassi
                for i in range(expression.count(r"\frac{")):  # Cambiato per contare le occorrenze
                    matches = re.findall(r'(\d+)\^(\d+)', expression)    
                    for base, exponent in matches:
                        # Sostituisce l'espressione originale con quella formattata
                        expression = expression.replace(f"{base}^{exponent}", f"{base}^{{{exponent}}}") 
                    minLen = len(expression)
                    print (f" minLen = ",minLen)
                    # Nuovo ciclo for per gestire la sostituzione dopo il primo for
                    for match in re.finditer(r'\^', expression):
                        start_brace = expression.find('{', match.end())
                        end_brace = expression.find('}', start_brace)
                        if start_brace != -1 and end_brace != -1:
                            # Sostituisci il contenuto tra { e }
                            potnz = expression[start_brace-1:end_brace+1]
                            potenze.append(potnz)
                            positions.append((start_brace-1, end_brace+1))  # Memorizza le posizioni
                            expression = expression[:start_brace-1] + " " * (end_brace - start_brace + 2) + expression[end_brace + 1:]
                    try:
                        start_ignore = expression.index(r"\frac{", i)  # Trova l'indice di inizio della frazione
                        # Trova il secondo '}'
                        first_brace = expression.find('}', start_ignore)  # Trova il primo '}'
                        second_brace = expression.find('}', first_brace + 1)  # Trova il secondo '}'
                        if second_brace != -1:  # Assicurati che il secondo '}' esista
                            end_ignore = second_brace
                            # Sostituisci il contenuto tra start_ignore e end_ignore
                            filtered_txt = expression[:start_ignore] + " " * (end_ignore - start_ignore + 1) + expression[end_ignore + 1:]
                            # Mantieni il carattere \ prima di frac
                            fract = expression[start_ignore:end_ignore+1]  # Non sostituire \frac
                            fractions.append(fract)  # Aggiunto per memorizzare la frazione nella lista
                            expression = filtered_txt  # Aggiorna l'espressione
                            i = start_ignore  # Aggiorna l'indice per continuare la ricerca
                        else:
                            break 
                    except ValueError:
                        print("fine 24 ")
                        break 
                print(f"{'lin 105  left_expr:':<30} {expression}")
                exprLen = len(expression)
                print (f" exprLen = ",exprLen)
                expression = expression.replace("{", "__LEFT_BRACE__").replace("}", "__RIGHT_BRACE__")
                print(f"{'lin 149  __LEFT_BRACE__r:':<30} {expression}")
                # Reinserisci le frazioni e le potenze nell'espressione
                for fract in fractions:
                    expression = expression.replace(" " * len(fract), fract, 1)
                for i, pot in enumerate(potenze):
                    start, end = positions.pop(0)  # Prendi la posizione della potenza
                    try:
                        if expression[0:0 + len("__LEFT_BRACE__")] == "__LEFT_BRACE__":  # Controlla se __LEFT_BRACE__ è all'indice 0
                            start += len("__LEFT_BRACE__")  # Aggiungi la lunghezza di __LEFT_BRACE__
                            end += len("__RIGHT_BRACE__")-2# Non fare nulla, mantenere le posizioni originali
                        elif i > 0:  # Dalla seconda occorrenza in poi
                            start += len("__LEFT_BRACE__")  # Aggiungi la lunghezza di __LEFT_BRACE__
                            end += len("__RIGHT_BRACE__")-2   # Aggiungi la lunghezza di __RIGHT_BRACE__
                    except IndexError:
                        # Gestisci eventuali errori di indice
                        print("Errore: indice non valido.")
                    left = expression[:start]
                    rigt =  expression[end:]
                    expression = expression[:start] + pot + expression[end:]  # Reinserisci la potenza
                # Sostituisci { e } con marcatori temporanei
                # Esegui le sostituzioni di { e } solo dopo aver reinserito tutto
                filtered_txt = expression.replace("__LEFT_BRACE__", r'\left\{').replace("__RIGHT_BRACE__", r'\right\}') 
                # print(f"{'lin 105  left_expr:':<30} {expression}")
                print(f"{'lin 51  filtered_txt:':<30} {filtered_txt}")
                espressioneNv = filtered_txt.replace(" ", "")
                espressioneNv = espressioneNv.replace('*', '\\times')
                return espressioneNv
        print ("417 expression §===",expression)
        if "/" in expression:
            if expression[0] == "{":
                print( f"--------------------=========================================-------------------------")
                print (f"734 pos_di_graf_da_sot ",pos_di_graf_da_sot)
                #expression = expression.replace("{", "__LEFT_BRACE__") 
                # expression = expression.replace("{", "__LEFT_BRACE__").replace("}", "__RIGHT_BRACE__")
                #expression = expression.replace("}", "__RIGHT_BRACE__")
                ######*/////////------------ inizio-----{(5/4-7/2)-[4/5+4/3*(1/3)*9/28-3/2]}*(10/21)------------------------///////
                ## tutto quello  c'è qui dentro tine econto di {}*  
                main = expression.find(pos_di_graf_da_sot[0][0], 1)
                print(f" expression[pos_di_ogg] = ", expression[  main-2: main +3 ])
                print(f" 711 pos_di_graf_da_sot   prima ",pos_di_graf_da_sot) 
                self.keep_last_element(pos_di_graf_da_sot)  # tiene conto di   {-9/4-[4/5+4/3*1/3*9/28-3/2]}*10/21 
                # cioè  pos_di_graf_da_sot ha dentro la * e il numero di * partendo da sistra , quello subit
                # dopo }
                symbol_to_find = pos_di_graf_da_sot[0][0]  # Simbolo da cercare (può essere cambiato in qualsiasi simbolo)
                position_to_find =pos_di_graf_da_sot[0][1]  # Posizione del simbolo che vuoi trovare (es. 3 per il terzo simbolo)
                symbol_indices = []  # Lista per memorizzare gli indici del simbolo
                #pos_di_graf_da_sot= []
                print(f"716 len(pos_di_graf_da_sot) = ", len(pos_di_graf_da_sot)  )
                # for j in range(len(pos_di_graf_da_sot)):
                #for j in range(len(pos_di_graf_da_sot) - 1, -1, -1):    
                #    pos_di_graf_da_sot.pop(j)
                #    print(f" pos_di_graf_da_sot = ",pos_di_graf_da_sot)
                #print(f" pos_di_graf_da_sot = ",pos_di_graf_da_sot)
                #pos_di_graf_da_sot = 
                ##############################
                ##self.keep_last_element(pos_di_graf_da_sot)
                print(pos_di_graf_da_sot)  # Output: [5]
                
                k = 0  # Inizializza l'indice
    
                # Loop per trovare gli indici del simbolo
                while True:
                    k = expression.find(symbol_to_find, k)  # Trova il simbolo a partire dall'indice i
                    if k == -1:  # Se non ci sono più simboli, esci dal ciclo
                        break
                    symbol_indices.append(k)  # Aggiungi l'indice trovato alla lista
                    k += 1  # Incrementa l'indice per continuare la ricerca

                # Controlla se ci sono abbastanza simboli
                if len(symbol_indices) >= position_to_find:
                    desired_symbol_index = symbol_indices[position_to_find - 1]  # Ottieni l'indice del simbolo desiderato
                    print(f"L'indice del {position_to_find}° simbolo '{symbol_to_find}' è: {desired_symbol_index}")
                else:
                    print(f"Ci sono meno di {position_to_find} simboli '{symbol_to_find}' nella stringa.")

                
                
                ######*/////////----------fine ----------------------------------------------///////
                # endf = expression.find(pos_di_graf_da_sot, 1)
                endf = desired_symbol_index #   serve per trovare la giusta posizione 
                expression =  "__LEFT_BRACE__" + expression[1:endf-1]+"__RIGHT_BRACE__"+ expression[endf:]
                self.replace_fractions(expression,0,0)
            else:
                self.replace_fractions(expression,0,0)
        filtered_txt = expression.replace("__LEFT_BRACE__", r'\left\{').replace("__RIGHT_BRACE__", r'\right\}') 
                # print(f"{'lin 105  left_expr:':<30} {expression}")
        print(f"{'lin 51  filtered_txt:':<30} {filtered_txt}")
        espressioneNv = filtered_txt.replace(" ", "")
        return espressioneNv

    def keep_last_element(self,lst):
        if lst:  # Controlla se la lista non è vuota
            lst[:] = [lst[-1]]  # Mantiene solo l'ultimo elemento
        return lst
    
    
    # **************************************************************************************************************************************************************
    
    
    def risolvi_espressione(self, espressione):
        print(f" line 171   risolvi_espressione espressione: {espressione}")
        #expression = r"(9/2-2)*4^3"
        #expression_modifiedk = self.replace_fractions(expression,0,0)
        expression_modifiedk = self.replace_fractions(espressione,0,0)
        
        ### inizio   qusto serve per fare in modo che {}  viene salato quindi ri chiamo per fare 
        # in mod che ance dentro  ho frac  , faccio cosi anche dopo la risol parentesi
        if "/" in expression_modifiedk:
            expression_modifiedk=self.replace_fractions(expression_modifiedk,0,0)
            print("-------------------------------------------------text---------------------")
            print(expression_modifiedk)
            print("-------------expression---------------------------------------------------------")
            print(expression_modifiedk)
        
        
        ### fine 
        print(f"{'541 expression_modified:':<40} {expression_modifiedk}")
        #########################self.title_label.text = expression_modifiedk
        self.passi = [f"Espre my cod iniziale7: ${ expression_modifiedk }$"]
        #######################################self.passi.append(f"Risolviamo : ${'[(\\frac{4}{3}+\\frac{7}{2})+5^2]-\left\{4+(3^2+\\frac{8}{9})\right\}'}$")
        print(f" line 585 in risolvi_espressione espressione: {espressione}")
        
        #self.passi = [f"Espressione iniziale: ${self.espressione_to_latex(espressione)}$"]
        # ***************************************************************************************************
        #serve    per calcolare  '-4/9/3/4' con moltiplicazioni 
        pattern = r'^[0-9/:]+$'
        cleaned_input = espressione.replace(" ", "")
        cleaned_input = cleaned_input.strip("-+")
        is_valid = bool(re.match(pattern, cleaned_input))
        print(is_valid)  # Output: True or False
        if is_valid:
            print("La stringa contiene solo '/'")
            nu_of_div_sim = espressione.count(r"/")
            print(f" nu_of_div_sim =",nu_of_div_sim)
            
                                
            # _______________________________________________________________________________________
            if nu_of_div_sim == 3:
            # Logica per gestire il caso con tre simboli di divisione
                parts = espressione.split('/')
                if len(parts) >= 3:
                    # Prendere il primo e l'ultimo come numeratore
                    numerator = str(int(parts[0])*int(parts[-1]))
                    # Prendere gli intermedi come denominatore
                    denominator = str(int(parts[1])*int(parts[-2]))
                    fraction = r'\frac{' + numerator + '}{' + denominator + '}'
                    expression = espressione.replace('/'.join(parts), fraction, 1)
                    print(f"Nuova espressione: {expression}")
                    espressione = numerator +'/'+denominator
                    print(f"Nuova espressione: {espressione}")
        
        
        
        # ***************************************************************************************************
        parentesi_ordine = [('(', ')'), ('[', ']'), ('{', '}')]
        
        for aperta, chiusa in parentesi_ordine:
            while aperta in espressione and chiusa in espressione:
                pattern = re.escape(aperta) + r'[^' + re.escape(aperta) + re.escape(chiusa) + r']+' + re.escape(chiusa)
                parentesi = re.findall(pattern, espressione)
                for p in parentesi:
                    contenuto_parentesi = p[1:-1]
                    
                    print(f" line 173   risolvi_espressione contenuto_parentesi: {contenuto_parentesi}")
                    print(f" line 374 in risolvi_espressione type(contenuto_parentesi): {type(contenuto_parentesi)}")
                    print(f"391 passi ",self.passi)
                    self.passi.append(f"Risolviamo la parentesi {aperta}{chiusa}: ${self.replace_fractions(contenuto_parentesi,0,0)}$")
                    print(f"393 passi dopo append: ",self.passi)
                    try:
                        # Risolvi le potenze
                        while "^" in contenuto_parentesi:
                            pattern = r'(-?\d+(/\d+)?)\^(-?\d+(/\d+)?)'
                            #############   ho modificato perche se   ho     [(4/3+7/2)+5^2]-{4+(3^2+8/9)}  
                            # allora  quando la vora sulla (3^2+8/9) trova   5^2 visto che lavora su intera espressione , per questo ora 
                        #    faccio lavorare solo su contenuto_parentesi
                            # match = re.search(pattern, espressione)
                            match = re.search(pattern, contenuto_parentesi)
                        
                            if match:
                                base, esponente = match.group(1), match.group(3)
                                risultato = self.valuta_espressione(f"{base}^{esponente}")
                                #risultato  = base ** esponente
                                self.passi.append(f"Calcoliamo la potenza: ${base}^{{{esponente}}} = {risultato}$")
                                # self.passi.append(f"Calcoliamo la potenza: ${base}^{{{exponent}}} = {risultato}$")
                                print(f" line 453 in risolvi_espressione match.start(): {match.start()}")
                                print(f" line 454 in risolvi_espressione match.end(): {match.end()}")
                                print(f" line 456 in risolvi_espressione contenuto_parentesi-1: {contenuto_parentesi[:match.start()-1]}")
                                print(f" line 457 in risolvi_espressione contenuto_parentesi[:match.start()]: {contenuto_parentesi[:match.start()]}")
                                if '^' in contenuto_parentesi[:match.start()-1]:
                                    # contenuto_parentesi = str(risultato)+contenuto_parentesi[match.start()-1:]
                                    # qui ho fatto una modicia perche ho deciso di prendere a lavorare 
                                    # su contenuto_parentesi in cerca di pozerazioni di ^ ..
                                    contenuto_parentesi = str(risultato)+contenuto_parentesi[match.end():]
                                else:
                                #  qui  hotolto -1 da   contenuto_parentesi[:match.start()-1] + str(risultato) 
                                # perche manca il segno + 
                                    contenuto_parentesi = contenuto_parentesi[:match.start()] + str(risultato)
                                # contenuto_parentesi = contenuto_parentesi[:match.start()-1] + str(risultato) + espressione[match.end():]
                                print(f" line 458 in risolvi_espressione contenuto_parentesi: {contenuto_parentesi}")
                                self.passi.append(f"Dopo il calcolo delle potenze: ${self.replace_fractions(contenuto_parentesi,0,0)}$")
                                #parsed_expr = self.parse_expression(contenuto_parentesi)
                                #risultato_finale = self.calculate(parsed_expr)
                                #print(f" line 466 in risolvi_espressione risultato_finale: {risultato_finale}")
                        # Passaggio 2: Risolviamo moltiplicazioni
                        mul_pattern = r'(-?\d+/\d+|\d+)\*(-?\d+/\d+|\d+)'
                        while re.search(mul_pattern, contenuto_parentesi):
                                match = re.search(mul_pattern, contenuto_parentesi)
                                left = Fraction(match.group(1))
                                right = Fraction(match.group(2))
                                result = left * right
                                self.passi.append(f"Moltiplicazione: ${self.replace_fractions(str(left),0,0)} \\times {self.replace_fractions(str(right),0,0 )} = {self.replace_fractions(str(result),0,0  )}$")
                                print(f" line 351   calculate self.passi: {self.passi}")
                                print(f" line 352   calculate match.group(0): {match.group(0)}")
                                print(f" line 353   calculate match.group(1): {match.group(1)}")
                                print(f" line 354   calculate match.group(2): {match.group(2)}")
                                print(f" line 355   calculate result: {result}")
                                print(f" line 356   calculate expression ************: {contenuto_parentesi}")
                                contenuto_parentesi = contenuto_parentesi.replace(match.group(0), str(result), 1)
                                print(f" line 358   calculate expression ====: {contenuto_parentesi}")
                                self.passi.append(f"Dopo il calcolo delle moltiplicazioni: ${self.replace_fractions(contenuto_parentesi,0,0)}$")
                                # self.passi.append(f"Dopo il calcolo delle moltiplicazioni: ${self.espressione_to_latex(contenuto_parentesi)}$")
                        # Risolvi moltiplicazioni e divisioni
                        #while '*' in espressione or '/' in espressione:
                        
                        #risultato_parentesi = self.valuta_espressione(contenuto_parentesi)
                        risultato_parentesi = self.frisolvi_espressione(contenuto_parentesi)
                        #risultato_parentesi,passi_parentesi = self.frisolvi_espressione(contenuto_parentesi)
                        print(f" line 174   risolvi_espressione risultato_parentesi: {risultato_parentesi}")
                        #self.passi.append(f"Risultato della parentesi: ${ risultato_parentesi }$")
                        self.passi.append(f"Risultato della parentesi: ${self.replace_fractions(str(risultato_parentesi),0,0)}$")
                        # self.passi.append(f"Risultato della parentesi: ${self.espressione_to_latex(str(risultato_parentesi))}$")
                        print(f" line 384 in risolvi_espressione p =: {p}")
                        if risultato_parentesi < 0:
                            # Sostituisci '+p' con il risultato negativo
                            print(f" line 655 in risolvi_espressione espressione: {espressione}")
                            #print(f" line 656 in risolvi_espressione espressione: {f"+{p}"}")
                            # sto facendo la sostituzione del segno + se il risultato è - negativo 
                            # forse fa lo setesso con 0 ma non lo so per questo aggiungo queste righe
                            x = espressione.find(p)

                            print(x)
                            print(f" line 902 in risolvi_espressione espressione[x-1]: { espressione[x-1]}")
                            print(f" line 903 in risolvi_espressione espressione[0]: { espressione[0]}")
                            if espressione[x-1]== '+':
                                espressione = espressione.replace(f"+{p}", str(risultato_parentesi))
                            # cui finisc e la logica di sostitutire + se ri è ngtivo
                            if espressione[0]== '+':
                                espressione = espressione.replace(f"+{p}", str(risultato_parentesi))
                            if espressione[x-1]== '-':
                                #espressione = espressione.replace(f"-{p}", str(risultato_parentesi))
                                espressione = espressione.replace(f"-{p}", "+"+str(abs(risultato_parentesi)))
                            else :
                                
                                espressione = espressione.replace(f"{p}", str(risultato_parentesi))
                                
                            print(f" line 657 in risolvi_espressione espressione: {f'+{p}'}")
                            print(f" line 659 in risolvi_espressione espressione: {f'{p}'}")
                            
                        else:
                            # Se il risultato non è negativo, procedi normalmente
                            espressione = espressione.replace(p, str(risultato_parentesi))
                            
                        print(f" line 385 in risolvi_espressione espressione: {espressione}")
                        print(f" line 386 in risolvi_espressione passi_parentesi: {type(espressione)}")
                    except Exception as e:
                        print(f"Errore nella valutazione: {e}")
                        self.passi.append(f"Errore nella valutazione: {e}")
                        return self.passi
                    
                #expression_modifiedk = self.replace_fractions(espressione,0,0)
                #print(f"{'541 expression_modified:':<40} {expression_modifiedk}")
                text_fr_grarffe = self.replace_fractions(espressione,0,0)
                
                
                ###/////////inizio ////////////// come fatto sopra se 
                if "/" in text_fr_grarffe:
                    text_fr_grarffe=self.replace_fractions(text_fr_grarffe,0,0)
            
                    print("-------------expression-------========----------:::--")
                    print(text_fr_grarffe)
                # @@@  fine 
                
                
                
                #print(f"{'indd ':<30} {ind}")
                print(f"{'text_fr_grarffe ':<30},{text_fr_grarffe}")
                self.passi.append(f"Espressione dopo la risoluzione delle parentesi {aperta}{chiusa}: ${ text_fr_grarffe }$")    
                    
                    
                #self.passi.append(f"Espressione dopo la risoluzione delle parentesi {aperta}{chiusa}: ${self.espressione_to_latex(espressione)}$")
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        
        """ pattern = r'^[0-9/:]+$'
        cleaned_input = espressione.replace(" ", "")
        cleaned_input = cleaned_input.strip("-+")
        is_valid = bool(re.match(pattern, cleaned_input))
        print(is_valid)  # Output: True or False
        if is_valid:
            print("La stringa contiene solo '/'")
            nu_of_div_sim = espressione.count(r"/")
            print(f" nu_of_div_sim =",nu_of_div_sim)
            
                                
            # _______________________________________________________________________________________
            if nu_of_div_sim == 3:
            # Logica per gestire il caso con tre simboli di divisione
                parts = espressione.split('/')
                if len(parts) >= 3:
                    # Prendere il primo e l'ultimo come numeratore
                    numerator = str(int(parts[0])*int(parts[-1]))
                    # Prendere gli intermedi come denominatore
                    denominator = str(int(parts[1])*int(parts[-2]))
                    fraction = r'\frac{' + numerator + '}{' + denominator + '}'
                    expression = espressione.replace('/'.join(parts), fraction, 1)
                    print(f"Nuova espressione: {expression}")
                    espressione = numerator +'/'+denominator
                    print(f"Nuova espressione: {espressione}")
    """
        
        
        
        
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        
        
        
        
        parsed_expr = self.parse_expression(espressione)
        risultato_finale = self.calculate(parsed_expr)
        # Risolvi moltiplicazioni
        
        #risultato_finale = valore_risultato if 'valore_risultato' in locals() else self.valuta_espressione(espressione)
        print(f" line 430 in risolvi_espressione risultato_finale: {risultato_finale}")
        #self.passi.append(f"Risultato finale mokd: ${risultato_finale}$")
        
        return self.passi

    def mostra_prossimo_passo(self, instance):
        print(f" line 437   mostra_prossimo_passo self.passi: {self.passi}")
        if self.passo_corrente < len(self.passi):
            passo = self.passi[self.passo_corrente]
            try:
                self.genera_immagine_latex(passo)
            except Exception as e:
                print(f"Errore durante la generazione dell'immagine: {e}")
            self.passo_corrente += 1
        else:
            self.next_button.disabled = True

    def prepara_risoluzione(self, instance):
        #txt = '{(5/4+7/2-1)-[4/5+4/3*(5-1/3)*9/28-3/2]}*(10/21+1/7+2/3)-3/20'
        #txt = "2/3/9/7"
        #txt = "{15/4-13/10}/9/7"
        #txt = "{(5/4+7/2 )-[ 4/3*(5-1/3)*9/28 ]}*(10/21+ 2/3)-3/20 "
        txt = self.entry.text
        espressione = txt.replace(" ", "")
        print (f"  self.load_counter()  value ==" ,self.load_counter())
        self.increment_counter()
        print (f"  self.load_counter()   value  Dopo increment ==" ,self.load_counter())
        print(f"Espressione in prepara_risoluzione: {espressione}")
        if not espressione:
            self.passi = ["Inserisci un'espressione valida"]
            #self.passi = [f"Risolviamo : ${'[(\\frac{4}{3}+\\frac{7}{2})+5^2]-\\left\{4+(3^2+\\frac{8}{9})\\right\}'}$"]
        else:
            try:
                if int(self.load_counter()) < 906:
                    passi = self.risolvi_espressione(espressione)
                    
                    print(f"Passi risoluzione: {passi}")
                else :
                    self.passi = ["hai superato il limite di 3 "]  
            except Exception as e:
                self.passi = [f"Errore durante la risoluzione: {str(e)}"]
        self.passo_corrente = 0
        self.steps_layout.clear_widgets()
        self.next_button.disabled = False
        self.mostra_prossimo_passo(instance)

    def genera_immagine_latex(self, formula):
        
        text_size_in_scrol= 24
        
        print(f" line 220   genera_immagine_latex formula: {formula}")
        fig, ax = plt.subplots(figsize=(10,1))
        ax.axis("off")
        #   qui sotto i valori 0.5, 0.5 determinano la posizioen del testo nel piccol blocco in scrol 
        #  qui il colore serve per il text 
        color_of_txt = rgb(13, 0, 255)
        ax.text(0.5, 0.5, formula, fontsize= text_size_in_scrol, ha='center', va='center', wrap=True, color= color_of_txt  )  # Modifica il colore qui
        # ax.text(0.5, 0.5, formula, fontsize= text_size_in_scrol, ha='center', va='center', wrap=True, color='red')  # Modifica il colore qui
        plt.tight_layout()

        buf = BytesIO()
        print(f" line 232   genera_immagine_latex buf: {buf}")
        plt.savefig(buf, format='png', dpi=100, bbox_inches='tight', transparent=True)
        plt.close(fig)
        buf.seek(0)

        core_image = CoreImage(buf, ext="png")
        print(f" line 248   genera_immagine_latex core_image: {core_image}")
        larghezza_fissa = 700
        altezza_proporzionale = int(core_image.height * (larghezza_fissa / core_image.width))
        
        image_widget = Image(texture=core_image.texture, 
                            size_hint=(None, None),
                            size=(larghezza_fissa, altezza_proporzionale))
        
        background_layout = BackgroundLayout(anchor_x='center', size_hint_y=None, height=altezza_proporzionale + 20)
        background_layout.add_widget(image_widget)
        
        self.steps_layout.add_widget(background_layout)
        
    def parse_expression(self, expr):
        expr = expr.replace("^", "**")
        expr = expr.replace(" ", "")
        if expr.count("(") != expr.count(")"):
            raise ValueError("Numero di parentesi non bilanciato")
        return expr
    def parse_frazione(self, s):
        #print(f" line 145   parse_frazione s: {s}")
        s = s.strip()
        #print(f" line 147   parse_frazione s: {s}")
        # Rimuovi i comandi LaTeX
        s = re.sub(r'\\large\{|\}', '', s)
        #print(f" line 149   parse_frazione s: {s}")
        s = s.replace('\\frac', '')
        #print(f" line 151   parse_frazione s: {s}")
        if '/' in s:
            #print(f" line 154   parse_frazione s: {s}")
            num, denom = map(int, s.split('/'))
            #print(f" line 156   parse_frazione num: {num}")
            #print(f" line 157   parse_frazione denom: {denom}")
            return Fraction(num, denom)
        elif s.lstrip('+-').isdigit():
            #print(f" line 160   parse_frazione s: {s}")
            return Fraction(int(s), 1)
        else:
            #print(f" line 163   parse_frazione s: {s}")
            # Gestisci il caso in cui la stringa sia un'espressione
            return self.valuta_espressione(s)
        
    def calcola_mcm(self, numeri):
        print(f" line 297   calcola_mcm numeri: {numeri}")
        def mcm_due_numeri(a, b):
            return abs(a * b) // gcd(a, b)
        risultato = numeri[0]
        for i in range(1, len(numeri)):
            risultato = mcm_due_numeri(risultato, numeri[i])
        print(f" line 304   calcola_mcm risultato: {risultato}")
        return risultato    
    
    
    def frisolvi_espressione(self, espressione):
        print(f" line 307   frisolvi_espressione espressione: {espressione}")
        parti = re.findall(r'([+-]?\s*\d+(?:/\d+)?)', espressione)
        print(f" line 310   frisolvi_espressione parti: {parti}")
        if not parti:
            return ["Risultato: $0$"]
        
        frazioni = []
        for parte in parti:
            print(f" line 315   frisolvi_espressione parte: {parte}")
            parte = parte.strip()
            print(f" line 317   frisolvi_espressione parte dopo strip: {parte}")
            if parte.startswith("+"):
                frazioni.append(self.parse_frazione(parte[1:]))
            elif parte.startswith("-"):
                frazioni.append(-self.parse_frazione(parte[1:]))
            else:
                frazioni.append(self.parse_frazione(parte))
        
        if not frazioni:
            return ["Risultato: $0$"]
        
        print(f" line 316   frisolvi_espressione frazioni: {frazioni}")
        mcm = self.calcola_mcm([frazione.denominator for frazione in frazioni])
        
        print(f" line 324   frisolvi_espressione mcm: {mcm}")
        self.passi.append(f"MCM dei denominatori: {mcm}")
        self.passi.append("Moltiplichiamo ogni numeratore per il MCM e manteniamo invariato il denominatore:")
        print(f" line 327   frisolvi_espressione passi: {self.passi}")
        latex_expr = r"\frac{"

        for i, frazione in enumerate(frazioni):
            if i > 0:
                print(f" line 333   frisolvi_espressione i: {i}")
                print(f" line 334   frisolvi_espressione frazione: {frazione}")
                print(f" line 335   frisolvi_espressione latex_expr: {latex_expr}")
                latex_expr += "+" if frazione >= 0 else ""
                print(f" line 337   frisolvi_espressione latex_expr: {latex_expr}")
            segno = '-' if frazione < 0 else ''
            latex_expr += f"{segno}\\frac{{{abs(frazione.numerator)}}}{{{frazione.denominator}}}*{mcm}"
            
            print(f" line 192   frisolvi_espressione latex_expr: {latex_expr}")    
        
        
        latex_expr += "}{" + str(mcm) + "}"
        print(f" line 341   frisolvi_espressione latex_expr: {latex_expr}")
        self.passi.append(f"Espressione con denominatore comune: ${self.replace_fractions(latex_expr,0,0)}$")
        # self.passi.append(f"Espressione con denominatore comune: ${self.espressione_to_latex(latex_expr)}$")
        
    
        
        latex_expr_semplificato = r"\frac{"
        for i, frazione in enumerate(frazioni):
            if i > 0:
                print(f" line 294   frisolvi_espressione i: {i}")
                print(f" line 295   frisolvi_espressione frazione: {frazione}")
                print(f" line 296   frisolvi_espressione latex_expr_semplificato: {latex_expr_semplificato}")
                latex_expr_semplificato += "+" if frazione >= 0 else ""
                print(f" line 298   frisolvi_espressione latex_expr_semplificato: {latex_expr_semplificato}")
            segno = '-' if frazione < 0 else ''
            print(f" line 298   frisolvi_espressione segno: {segno}")   
            print(f" line 299   frisolvi_espressione str(frazione.numerator): {str(frazione.numerator)}")
            print(f" line 300   frisolvi_espressione str(mcm//frazione.denominator): {str(mcm//frazione.denominator)}") 
            print(f" line 301   frisolvi_espressione latex_expr_semplificato: {latex_expr_semplificato}")
            latex_expr_semplificato += str(frazione.numerator) + r"*" + str(mcm//frazione.denominator)
            print(f" line 303   frisolvi_espressione latex_expr_semplificato: {latex_expr_semplificato}")
        latex_expr_semplificato += "}{" + str(mcm) + "}"
        #latex_expr_semplificato += "}{" + str(mcm) + "}"
        
        self.passi.append(f"Espressione con denominatore comune semplificato: ${self.replace_fractions(latex_expr_semplificato,0,0)}$")
        
        latex_expr_semplificatoMolt = r"\frac{"
        for i, frazione in enumerate(frazioni):
            if i > 0:
                print(f" line 294   frisolvi_espressione i: {i}")
                print(f" line 295   frisolvi_espressione frazione: {frazione}")
                print(f" line 296   frisolvi_espressione latex_expr_semplificato: {latex_expr_semplificatoMolt}")
                latex_expr_semplificatoMolt += "+" if frazione >= 0 else ""
                print(f" line 298   frisolvi_espressione latex_expr_semplificato: {latex_expr_semplificatoMolt}")
            segno = '-' if frazione < 0 else ''
            print(f" line 298   frisolvi_espressione segno: {segno}")   
            print(f" line 299   frisolvi_espressione str(frazione.numerator): {str(frazione.numerator)}")
            print(f" line 300   frisolvi_espressione str(mcm//frazione.denominator): {str(mcm//frazione.denominator)}") 
            print(f" line 301   frisolvi_espressione latex_expr_semplificato: {latex_expr_semplificatoMolt}")
            latex_expr_semplificatoMolt += str((frazione.numerator)*(mcm//frazione.denominator))
            print(f" line 303   frisolvi_espressione latex_expr_semplificato: {latex_expr_semplificatoMolt}")
        latex_expr_semplificatoMolt += "}{" + str(mcm) + "}"
        
        
        self.passi.append(f"Espressione con Multi: ${self.replace_fractions(latex_expr_semplificatoMolt, 0,0 )}$")
        
        numeratori = [frazione.numerator * (mcm // frazione.denominator) for frazione in frazioni]
        somma_numeratori = sum(numeratori)
        risultato = Fraction(somma_numeratori, mcm)
        ###self.passi.append(f"Risultato finale 353: $\\frac{{{risultato.numerator}}}{{{risultato.denominator}}}$")
        print(f" line 354 in frisolvi_espressione risultato: {risultato}")
        print(f" line 355 in frisolvi_espressione type(risultato): {type(risultato)}")
        return risultato



    def calculate(self, expression):
        #self.passi = []
        #self.passi.append(f"Espressione originale: ${self.espressione_to_latex(expression)}$")
        
        # Passaggio 1: Risolviamo le potenze
        power_pattern = r'(\d+)\*\*(\d+)'
        while re.search(power_pattern, expression):
            match = re.search(power_pattern, expression)
            base = int(match.group(1))
            exponent = int(match.group(2))
            result = base ** exponent
            self.passi.append(f"Calcolo potenza: ${base}^{{{exponent}}} = {result}$")
            
            print(f" line 547   calculate match.group(0): {match.group(0)}")
            print(f" line 548   calculate match.group(1): {match.group(1)}")
            print(f" line 549   result: { result }")
            
            expression = expression.replace(match.group(0), str(result), 1)
            
        ####   è aggiunto per  fare in modo che il latex viene fatto cone ^  altrimenti trovhe che 2^3= diventa 2x x3 invece con questa riga 
            #ottengo 2^3    solo che dopo   nella MOltiplicazioen 2^3  diventa 3x2 .  quindi in avanti faremo qualcosa
            # per sistemare questo 
            print(f"{'line 551  expression prima) := ':<25}{expression}")
            expressionPotena = expression.replace("**","^")
            #####
            print(f"{'line 554  expression  Dopo := ':<25}{  expressionPotena }")
            self.passi.append(f"Dopo il calcolo delle potenze: ${self.replace_fractions(expressionPotena,0,0)}$")
            # self.passi.append(f"Dopo il calcolo delle potenze: ${self.espressione_to_latex(expression)}$")
            
            #  agiiungo per tornare alla potenza  altrimenti   diventa una moltiplicazione 
            #expression = expression.replace("^", "**")

        # Passaggio 2: Risolviamo moltiplicazioni
        mul_pattern = r'(-?\d+/\d+|\d+)\*(-?\d+/\d+|\d+)'
        while re.search(mul_pattern, expression):
            match = re.search(mul_pattern, expression)
            left = Fraction(match.group(1))
            right = Fraction(match.group(2))
            result = left * right
            self.passi.append(f"Moltiplicazione: ${self.replace_fractions(str(left),0,0)}\\times {self.replace_fractions(str(right),0,0)} = {self.replace_fractions(str(result),0,0)}$")
            print(f" line 351   calculate self.passi: {self.passi}")
            print(f" line 352   calculate match.group(0): {match.group(0)}")
            print(f" line 353   calculate match.group(1): {match.group(1)}")
            print(f" line 354   calculate match.group(2): {match.group(2)}")
            print(f" line 355   calculate result: {result}")
            print(f" line 356   calculate expression ************: {expression}")
            expression = expression.replace(match.group(0), str(result), 1)
            print(f" line 358   calculate expression ====: {expression}")
            self.passi.append(f"Dopo il calcolo delle moltiplicazioni: ${self.replace_fractions(expression,0,0   )}$")
        moreExprs = re.findall(r'-?\d+/?\d*', expression)
        
        # Passaggio 3: Convertiamo tutto in frazioni e sommiamo
        fractions = [Fraction(term) for term in re.findall(r'-?\d+/?\d*', expression)]        
        while len(fractions) > 1:
            f1, f2 = fractions.pop(0), fractions.pop(0)
            #  lcm = abs(f1.denominator * f2.denominator) // math.gcd(f1.denominator, f2.denominator)
            print(f" line 364   f1 =: {f1}")  
            print(f" line 365   f2 *****=: {f2}")
            #self.passi.append(f"Caloliamo prima expression : ${self.espressione_to_latex(expression)}$")  
            #contenuto_parentesi_n    = str(f1) + "+" + str(f2)
            
            ################################per 
            # sitemare  2/8/7/9   che  è un risultato di un calcolo 
            pattern = r'^[0-9/:]+$'
            cleaned_input = expression.replace(" ", "")
            cleaned_input = cleaned_input.strip("-+")
            is_valid = bool(re.match(pattern, cleaned_input))
            print(is_valid)  # Output: True or False
            if is_valid:
                print("La stringa contiene solo '/'")
                nu_of_div_sim = expression.count(r"/")
                print(f" nu_of_div_sim =",nu_of_div_sim)


                # _______________________________________________________________________________________
                if nu_of_div_sim == 3:
                # Logica per gestire il caso con tre simboli di divisione
                    parts = expression.split('/')
                    if len(parts) >= 3:
                        # Prendere il primo e l'ultimo come numeratore
                        numerator = str(int(parts[0])*int(parts[-1]))
                        # Prendere gli intermedi come denominatore
                        denominator = str(int(parts[1])*int(parts[-2]))
                        fraction = r'\frac{' + numerator + '}{' + denominator + '}'
                        expression = expression.replace('/'.join(parts), fraction, 1)
                        print(f" 1237 Nuova espressione: {expression}")
                        expression = numerator +'/'+denominator
                        print(f"1239 Nuova espressione: {expression}")
                self.passi.append(f"Risultato di ribalta : ${self.replace_fractions(expression,0,0)}$") 
                print(f"1240 Nuova espressione: {expression}")
                return 987
            
            
            
            ################################per 
            
            
            
            
            
            contenuto_parentesi_n = str(f1)
            if f2 < 0:
                contenuto_parentesi_n += str(f2)  # Aggiungi direttamente se f2 è negativo
            else:
                contenuto_parentesi_n += "+" + str(f2)  # Aggiungi il segno più se f2 è positivo
            #self.passi.append(f"Caloliamo prima  : ${self.espressione_to_latex(contenuto_parentesi_n)}$")     
            self.passi.append(f"Caloliamo prima  : ${self.replace_fractions(contenuto_parentesi_n,0,0)}$")     
            #self.passi.append(f"Calc le prime due frazioni  = : ${self.espressione_to_latex(contenuto_parentesi_n)}$")
            print(f" line 377   calculate contenuto_parentesi_n: {contenuto_parentesi_n}")
            result = self.frisolvi_espressione(contenuto_parentesi_n)
            # Aggiungi un controllo per gestire correttamente i segni
            print(f"{'line 551  str(f1) := ':<25}{str(f1)}")
            print(f"{'line 552  str(f2) := ':<25}{str(f2)}")
            if f2 < 0:
                print(f" line 369   calculate result ======================================>=< 0: {result}")
                self.passi.append(f"Somma frazioni f2  mod: ${self.replace_fractions(str(f1),0 ,0 )} - {self.replace_fractions(str(abs(f2)),0,0 )} = {self.replace_fractions(str(result),0,0 )}$")
            else:
                print(f" line 372   calculate result ======================================>= 0: {result}")
                
                self.passi.append(f"Somma frazioni f2  0 mod: ${self.replace_fractions(str(f1),0 ,0 ) } + {self.replace_fractions(str(abs(f2)),0,0 ) } = {self.replace_fractions(str(result),0,0 ) }$")
            # Sostituisci f1 e f2 con result nell'espressione
            expression = re.sub(r'(-?\d+/?\d*)\s*[+\-]\s*(-?\d+/?\d*)', str(result), expression, count=1)
            self.passi.append(f"Espressione dopo la sostituzione: ${self.replace_fractions(expression,0,0 )}$")
            print(f"Espressione dopo la sostituzione: {expression}")
            fractions.insert(0, result)

        final_result = fractions[0]
        print(f"1278 final_result  tyop",type( final_result))
        self.passi.append(f"Risultato finale ok: ${self.replace_fractions(str(final_result),0,0 )}$")
        print(f"Risultato finale modd: ${self.replace_fractions(str(final_result),0,0   )}$")    
        print(f"71  passi: {self.passi}")
        #self.genera_immagini_latex()
        
        return final_result


# Avvia l'applicazione
if __name__ == "__main__":
    myApp().run()
