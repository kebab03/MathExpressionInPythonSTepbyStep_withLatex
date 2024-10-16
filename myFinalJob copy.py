import os
os.environ['KIVY_NO_CONSOLELOG'] = '1'

import logging
logging.getLogger().setLevel(logging.ERROR)
logging.getLogger('matplotlib').setLevel(logging.ERROR)
logging.getLogger('PIL').setLevel(logging.ERROR)

import warnings
warnings.filterwarnings("ignore")

from kivy.logger import Logger
Logger.setLevel(logging.ERROR)

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from fractions import Fraction
import re
from math import gcd
import math
import matplotlib
matplotlib.set_loglevel("WARNING")
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from io import BytesIO
from kivy.core.image import Image as CoreImage
from kivy.uix.anchorlayout import AnchorLayout
from kivy.graphics import Color, Rectangle
from kivy.uix.floatlayout import FloatLayout
import operator

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Computer Modern Roman"],
})

def rgb(r,g,b):    
    return round(r / 255, 2), round(g / 255, 2), round(b / 255, 2), 1

class BackgroundLayout(AnchorLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(size=self._update_rect, pos=self._update_rect)

        with self.canvas.before:
            bgclr = rgb(250, 243, 182)
            Color(*bgclr)
            self.rect = Rectangle(size=self.size, pos=self.pos)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

class MainLayout(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(size=self._update_rect, pos=self._update_rect)

        with self.canvas.before:
            Color(* rgb(255, 69, 106)   )
            self.rect = Rectangle(size=self.size, pos=self.pos)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

class Copy7App(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.passi = []  # Inizializza passi come attributo della classe
        self.num = 0

    def build(self):
        self.main_layout = MainLayout()
        
        content_layout = BoxLayout(orientation='vertical', padding=10, spacing=10,
                    size_hint=(1, 1), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        
        input_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=100)
        
        self.label = Label(text="Inserisci un'espressione aritmetica (es. 2/3-9/7+(2/7+3/5)):", 
                        size_hint_y=None, height=40, font_size='18sp')
        input_layout.add_widget(self.label)

        self.entry = TextInput(size_hint_y=None, height=40)
        input_layout.add_widget(self.entry)

        content_layout.add_widget(input_layout)

        self.scroll_view = ScrollView(size_hint_y=0.7)
        self.steps_layout = GridLayout(cols=1, size_hint_y=None, spacing=10)
        self.steps_layout.bind(minimum_height=self.steps_layout.setter('height'))
        self.scroll_view.add_widget(self.steps_layout)
        content_layout.add_widget(self.scroll_view)

        button_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
        self.solve_button = Button(text="Risolvi")
        self.solve_button.bind(on_press=self.prepara_risoluzione)
        button_layout.add_widget(self.solve_button)

        self.next_button = Button(text="Prossimo Passo")
        self.next_button.bind(on_press=self.mostra_prossimo_passo)
        self.next_button.disabled = True
        button_layout.add_widget(self.next_button)

        content_layout.add_widget(button_layout)

        self.main_layout.add_widget(content_layout)

        self.passo_corrente = 0
        self.images = []

        return self.main_layout

    def prepara_risoluzione(self, instance):
        #espressione = self.entry.text
        txt = self.entry.text
        print(f"{' 124 len(txt)':<20} {len(txt)}")
        espressione = txt.replace(" ", "")
        print(f"{' 126 len(espressione)':<20} {len(espressione)}")
        #espressione = "[8+6-17]"
        # espressione = "[8+6-(15/3-2)]"
        #espressione = "(9+10)*4^2"
        # espressione = "[8/2+6-17]"
        #espressione = self.entry.text.strip()
        print("line 55")
        print(f"espressione  in prepara_risoluzione: {espressione}")
        if not espressione:
            self.passi = ["Inserisci un'espressione valida"]
        else:
            try:
                print(f"line 60   prepara_risoluzione espressione: {espressione}")
                passi = self.risolvi_espressione(espressione)
                print(f" line 62   prepara_risoluzione passi: {passi}")
            except Exception as e:
                self.passi = [f"Errore durante la risoluzione hg: {str(e)}"]
        self.passo_corrente = 0
        self.steps_layout.clear_widgets()
        self.images.clear()
        self.next_button.disabled = False
        self.mostra_prossimo_passo(instance)
    
    def replace_fractions(self,expression,i,lungh_sostituita):
        sta = False
        indx_partenza =i 
        lunEspress = len(expression)
        print(f"{"153 _expression_[-1]":<30}{expression[-1]}")
        print(f"{" i di partenza-----------***:=":<30} { i } ")
        print(f'{"18__len(expression)==***=:=":<30} {len(expression)}')
            # Aggiungiamo il controllo per evitare IndexError
        if (indx_partenza>= len(expression)) or  (indx_partenza>= len(expression)-1):
            print(f'{"return expression perk indx_partenza >= len(expression) :":<30} {expression}')            
            print(f'{"136 new expression:":<30} {expression}')
    # Sostituire moltiplicazione con \times
            expression = expression.replace('*', '\\times')
            print(f'{"139 new expression:":<30} {expression}') 
            return expression  # Esci dalla ricorsione se l'indice è fuori dal range
        print(f"{"167_expression_[indx_partenza+1]":<30}{expression[indx_partenza+1]}")
        if expression[indx_partenza] is not None:
            print(f"{"20_expression_[indx_partenza]":<30}{expression[indx_partenza]}")
        #if expression[indx_partenza] is not None:
            #print(f"{"20_expression_[indx_partenza]":<30}{expression[indx_partenza]}")
        while i < len(expression):
            print(f'{"partenza expression:":<30} {expression}')
            # Ignora le espressioni già convertite in \frac{...}{...}
            if expression[i:i+6] == r'\frac{':
                # Trova la fine della frazione
                frac_end = expression.find('}', expression.find('}', i + 6) + 1)
                i = frac_end + 1  # Salta oltre la frazione
                continue
            print(f"__32_expression[{i}] = {repr(expression[i])}")
            if expression[i] == '/':
                num = 0  # Cambiato da self.num a num locale
                print(f" {'i ':<30}{i}")
                left_expr = ""
                right_expr = ""
                # Controlla alla sinistra del '/'
                left_start = i - 1
                bolean = False
                while left_start >= 0 and expression[left_start] in '0123456789{([^}])':
                    print(f"{"187 expression[left_start]":<30}{expression[left_start]}")
                    print(f"{"190[left_start]":<30}{left_start}")
                    if left_start==indx_partenza:
                        if num >0 and indx_partenza >11:
                            # questa parte serve per tenere conto di prime cirefre(34) come 34/4
                            left_start=left_start+num
                            #left_start += num
                        else:
                            #left_start -= lungh_sostituita
                            # credo che avevo  fatto questo per prendere l'iniziale parentesi  di 
                            left_start=left_start-lungh_sostituita
                        print(f"{"439___[left_start]":<30}{left_start}")
                        print(f"{"440 e pression_[left_start]":<30}{expression[left_start]}")                
                    if expression[left_start] in '0123456789}])':
                        #break
                        #if expression[left_start] in '{([':
                        if expression[left_start] in '}])':  
                            print(f"{"445___[left_start]":<30}{left_start}")
                            print(f"{"446 -xpression_[left_start]":<30}{expression[left_start]}")                      
                            bolean =False
                            # Definire gli indici che vogliamo ignorare
                            start_ignore = indx_partenza-lungh_sostituita
                            end_ignore = indx_partenza
                            print(f"{" 4m_expression_[start_ignore-1]":<30}{expression[start_ignore-1]}")
                            print(f"{" 4m_expression_[start_ignore]":<30}{expression[start_ignore]}")
                            print(f"{" 4m_expression_[start_ignore+1]":<30}{expression[start_ignore+1]}") 
                            print(f"{"ignor4expression_[end_ignore]":<30}{expression[end_ignore]}")                             
                            # Costruire una stringa senza il contenuto tra start_ignore e end_ignore
                            filtered_txt = expression[:start_ignore] + " " * (end_ignore - start_ignore) + expression[end_ignore:]
                            print(f'{"66_len(filtered_txt)=====:=":<30} {len(filtered_txt)}')
                            # Trovare il primo indice della parentesi graffa aperta '{' ignorando la sezione specificata
                            parentes_index = filtered_txt.find("{")
                            print(f'{"461 type(parentes_index :":<38} {type(parentes_index)}')
                            if parentes_index>= start_ignore:
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
    # Sostituire la prima e l'ultima graffa
                print(f'{"txt 96 txt :":<38} {txt}')
                print(f'{"txt 97 txt :[0]":<38} {txt[0]}')
                print(f'{"txt 97 txt[-1] :":<38} {txt[-1]}')
                if txt[0] == "{" and txt[-1]== "}" :
                    modified_txt = r'\left\{' + txt[1:-1] + r'\right\}'
                    print(modified_txt)            
                    left_expr = modified_txt
                    print(f'{"txt 101 my new :":<38} {modified_txt}')                        
                print(f'{"lin 105  left_expr:":<30} {left_expr}')
                # Controlla alla destra del '/'
                right_end = i + 1
                # expression = r"46+{(9/2+2)+5}/4^2"
                while right_end < len(expression) and expression[right_end] in '0123456789{([^':
                    print(f"{"103 expression_[right_end]":<30}{expression[right_end]}")
                    # expression = r"[(9/2+4/7)-10]*4^3"
                    if expression[right_end] in '{([^':
                        print(f'{"106 right_end:":<30} {right_end}')
                        print(f"{"107 expression_[right_end]":<30}{expression[right_end]}")   
                        right_end += 1
                    elif expression[right_end] in '123456789^':
                        print(f"{"110 expression_[right_end]":<30}{expression[right_end]}")
                        print(f"{"111  len(expression) ":<30}{  len(expression) }")                                                         
                        if  right_end<  len(expression) :
                            right_end += 1
                        print(f'{"514 right_end:":<30} {right_end}')
                        print(f"{"515 expression_[right_end]":<30}{expression[right_end-1]}")
                    else:
                        right_end += 1
                        break 
                right_expr = expression[i + 1:right_end]  # Prendi l'espressione a destra
                print(f'{"right_expr:":<30} {right_expr}')
                # Sostituisci la porzione trovata con \frac{left}{right}
                fraction = r'\frac{' + left_expr + '}{' + right_expr + '}'
                print(f"{" fraction*******:=":<30} { fraction } ")
                print(f'{"289 len(fraction)=====:=":<30} {len(fraction)}')
                expression = expression[:left_start] + fraction + expression[right_end:]
                print(f'{"new expression:":<30} {expression}')
                indx=len(fraction)+i-1
                print(f"{" indx-----------***:=":<30} { indx } ")
                # Ripeti la sostituzione con l'espressione aggiornata
                lungh_sostituita = len(fraction)
                if lungh_sostituita>11:
                    # numd da sotrar per tenere primi n numeri
                    digDsor= lungh_sostituita-11
                    print(f'{"299 digDsor :":<30} {digDsor}')
                    indx-= digDsor# ho agiunto per tenere 45/87  i primi numeri
                    # indx-=2# ho agiunto per tenere 45/87  i primi numeri
                return self.replace_fractions(expression,indx, lungh_sostituita)  # Ricorsione sulla nuova espressione
            else:
                i += 1
        #print(f"__536_expression[{i}] = {repr(expression[i])}")
        print(f'{"136 new expression:":<30} {expression}')
        # Sostituire moltiplicazione con \times
        expression = expression.replace('*', '\\times')
        print(f'{"139 new expression:":<30} {expression}')
        ####     ho aggiunto if solo per [8/2+6-17]
        # se non va con altri pruoi eliminare
        if i== len(expression):            
            return expression
        return expression

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

    

    

    def espressione_to_latex(self, espressione):
        #print(f" line 280   espressione_to_latex espressione: {espressione}")
        latex = espressione.replace('*', r' \times ')
        #print(f" line 282 in espressione_to_latex dopo replace(*, r' \times '): {latex}")
        # Gestione corretta delle potenze
        def replace_power(match):
            base, exp = match.groups()
            print(f" line 286 in espressione_to_latex dopo match.groups(): {base}, {exp}")
            return f"{base}^{{{exp}}}"
        latex = re.sub(r'(\d+)\^(\d+)', replace_power, latex)
        #print(f" line 290   espressione_to_latex dopo sub(r'(d+)^(d+)', replace_power): {latex}")
        latex = re.sub(r'(\d+)/(\d+)', r'\\frac{\1}{\2}', latex)
        print(f" line 293   espressione_to_latex latex: {latex}")
        return latex

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
            if parte.startswith('+'):
                frazioni.append(self.parse_frazione(parte[1:]))
            elif parte.startswith('-'):
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
        
        """         for i, frazione in enumerate(frazioni):
            if i > 0:
                latex_expr += "+"
            latex_expr += r"\frac{" + str(frazione.numerator) + "}{" + str(frazione.denominator) + r"}*" + str(mcm)
        """
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
        
        self.passi.append(f"Espressione con denominatore comune semplificato: ${self.espressione_to_latex(latex_expr_semplificato)}$")
        
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
        
        
        self.passi.append(f"Espressione con Multi: ${self.espressione_to_latex(latex_expr_semplificatoMolt)}$")
        
        numeratori = [frazione.numerator * (mcm // frazione.denominator) for frazione in frazioni]
        somma_numeratori = sum(numeratori)
        risultato = Fraction(somma_numeratori, mcm)
        ###self.passi.append(f"Risultato finale 353: $\\frac{{{risultato.numerator}}}{{{risultato.denominator}}}$")
        print(f" line 354 in frisolvi_espressione risultato: {risultato}")
        print(f" line 355 in frisolvi_espressione type(risultato): {type(risultato)}")
        return risultato 
    #,self.passi

    def parse_expression(self, expr):
        expr = expr.replace("^", "**")
        expr = expr.replace(" ", "")
        if expr.count("(") != expr.count(")"):
            raise ValueError("Numero di parentesi non bilanciato")
        return expr

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
            expression = expression.replace(match.group(0), str(result), 1)
        
            self.passi.append(f"Dopo il calcolo delle potenze: ${self.espressione_to_latex(expression)}$")

        # Passaggio 2: Risolviamo moltiplicazioni
        mul_pattern = r'(-?\d+/\d+|\d+)\*(-?\d+/\d+|\d+)'
        while re.search(mul_pattern, expression):
            match = re.search(mul_pattern, expression)
            left = Fraction(match.group(1))
            right = Fraction(match.group(2))
            result = left * right
            self.passi.append(f"Moltiplicazione: ${self.espressione_to_latex(str(left))} \\times {self.espressione_to_latex(str(right))} = {self.espressione_to_latex(str(result))}$")
            print(f" line 351   calculate self.passi: {self.passi}")
            print(f" line 352   calculate match.group(0): {match.group(0)}")
            print(f" line 353   calculate match.group(1): {match.group(1)}")
            print(f" line 354   calculate match.group(2): {match.group(2)}")
            print(f" line 355   calculate result: {result}")
            print(f" line 356   calculate expression ************: {expression}")
            expression = expression.replace(match.group(0), str(result), 1)
            print(f" line 358   calculate expression ====: {expression}")
            self.passi.append(f"Dopo il calcolo delle moltiplicazioni: ${self.espressione_to_latex(expression)}$")
        moreExprs = re.findall(r'-?\d+/?\d*', expression)
        print(f'{" line 528  re.findall(r'-?\d+/?\d*', expression) ":<20}{re.findall(r'-?\d+/?\d*', expression)}')
        # Passaggio 3: Convertiamo tutto in frazioni e sommiamo
        fractions = [Fraction(term) for term in re.findall(r'-?\d+/?\d*', expression)]        
        while len(fractions) > 1:
            f1, f2 = fractions.pop(0), fractions.pop(0)
            #  lcm = abs(f1.denominator * f2.denominator) // math.gcd(f1.denominator, f2.denominator)
            print(f" line 364   f1 =: {f1}")  
            print(f" line 365   f2 *****=: {f2}")
            #self.passi.append(f"Caloliamo prima expression : ${self.espressione_to_latex(expression)}$")  
            #contenuto_parentesi_n    = str(f1) + "+" + str(f2)
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
            print(f'{"line 551  str(f1) := ":<25}{str(f1)}')
            print(f'{"line 552  str(f2) := ":<25}{str(f2)}')
            if f2 < 0:
                print(f" line 369   calculate result ======================================>=< 0: {result}")
                self.passi.append(f"Somma frazioni f2  mod: ${self.espressione_to_latex(str(f1))} - {self.espressione_to_latex(str(abs(f2)))} = {self.espressione_to_latex(str(result))}$")
            else:
                print(f" line 372   calculate result ======================================>= 0: {result}")
                
                self.passi.append(f"Somma frazioni f2  0 mod: ${self.espressione_to_latex(str(f1))} + {self.espressione_to_latex(str(f2))} = {self.espressione_to_latex(str(result))}$")
            # Sostituisci f1 e f2 con result nell'espressione
            expression = re.sub(r'(-?\d+/?\d*)\s*[+\-]\s*(-?\d+/?\d*)', str(result), expression, count=1)
            self.passi.append(f"Espressione dopo la sostituzione: ${self.espressione_to_latex(expression)}$")
            print(f"Espressione dopo la sostituzione: {expression}")
            fractions.insert(0, result)

        final_result = fractions[0]
        self.passi.append(f"Risultato finale ok: ${self.espressione_to_latex(str(final_result))}$")
        print(f"Risultato finale modd: ${self.espressione_to_latex(str(final_result))}$")    
        print(f"71  passi: {self.passi}")
        #self.genera_immagini_latex()
        
        return final_result
    #passi = []
    def risolvi_espressione(self, espressione):
        print(f" line 171   risolvi_espressione espressione: {espressione}")
        #expression = r"(9/2-2)*4^3"
        #expression_modifiedk = self.replace_fractions(expression,0,0)
        expression_modifiedk = self.replace_fractions(espressione,0,0)
        print(f'{"541 expression_modified:":<40} {expression_modifiedk}')
        self.passi = [f"Espre my cod iniziale7: ${ expression_modifiedk }$"]
        print(f" line 585 in risolvi_espressione espressione: {espressione}")
        
        #self.passi = [f"Espressione iniziale: ${self.espressione_to_latex(espressione)}$"]
        
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
                            match = re.search(pattern, espressione)
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
                                contenuto_parentesi = contenuto_parentesi[:match.start()-1] + str(risultato)
                                # contenuto_parentesi = contenuto_parentesi[:match.start()-1] + str(risultato) + espressione[match.end():]
                                print(f" line 458 in risolvi_espressione contenuto_parentesi: {contenuto_parentesi}")
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
                                self.passi.append(f"Moltiplicazione: ${self.espressione_to_latex(str(left))} \\times {self.espressione_to_latex(str(right))} = {self.espressione_to_latex(str(result))}$")
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
                            print(f" line 656 in risolvi_espressione espressione: {f"+{p}"}")
                            # sto facendo la sostituzione del segno + se il risultato è - negativo 
                            # forse fa lo setesso con 0 ma non lo so per questo aggiungo queste righe
                            x = espressione.find(p)

                            print(x)
                            
                            if espressione[x-1]== '+':
                                espressione = espressione.replace(f"+{p}", str(risultato_parentesi))
                            # cui finisc e la logica di sostitutire + se ri è ngtivo
                            if espressione[0]== '+':
                                espressione = espressione.replace(f"+{p}", str(risultato_parentesi))
                            else:
                                espressione = espressione.replace(f"{p}", str(risultato_parentesi))
                                
                            print(f" line 657 in risolvi_espressione espressione: {f"+{p}"}")
                            print(f" line 659 in risolvi_espressione espressione: {f"{p}"}")
                            
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
                #print(f'{"541 expression_modified:":<40} {expression_modifiedk}')
                self.passi.append(f"Espressione dopo la risoluzione delle parentesi {aperta}{chiusa}: ${ self.replace_fractions(espressione,0,0) }$")    
                    
                    
                #self.passi.append(f"Espressione dopo la risoluzione delle parentesi {aperta}{chiusa}: ${self.espressione_to_latex(espressione)}$")
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

    def genera_immagine_latex(self, formula):
        print(f" line 220   genera_immagine_latex formula: {formula}")
        fig, ax = plt.subplots(figsize=(8, 1))
        ax.axis('off')
        ax.text(0.5, 0.5, formula, fontsize=16, ha='center', va='center', wrap=True)
        plt.tight_layout()

        buf = BytesIO()
        print(f" line 232   genera_immagine_latex buf: {buf}")
        plt.savefig(buf, format='png', dpi=100, bbox_inches='tight', transparent=True)
        plt.close(fig)
        buf.seek(0)

        core_image = CoreImage(buf, ext='png')
        print(f" line 248   genera_immagine_latex core_image: {core_image}")
        larghezza_fissa = 700
        altezza_proporzionale = int(core_image.height * (larghezza_fissa / core_image.width))
        
        image_widget = Image(texture=core_image.texture, 
                            size_hint=(None, None),
                            size=(larghezza_fissa, altezza_proporzionale))
        
        background_layout = BackgroundLayout(anchor_x='center', size_hint_y=None, height=altezza_proporzionale + 20)
        background_layout.add_widget(image_widget)
        
        self.steps_layout.add_widget(background_layout)

if __name__ == "__main__":
    Copy7App().run()