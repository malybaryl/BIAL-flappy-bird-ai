# FlappyAI

## Screenshots [EN] / Zrzuty Ekranu [PL]

![](/screenshots/Screenshot_0.png)
![](/screenshots/Screenshot_2.png)
![](/screenshots/Screenshot_1.png)

## English

### Project Overview
FlappyAI is a NEAT-based implementation of the classic Flappy Bird game, where neural networks evolve to master gameplay through reinforcement-style fitness evaluation. Agents learn to navigate pipes by adjusting jump timing based on sensory inputs.

### Key Features
- **Neuroevolution with NEAT**: Adaptive topology and weight mutation for evolving effective controllers.  
- **Custom Sensory Inputs**: Distance to upcoming pipes, vertical position, and relative gap height.  
- **Fitness Strategy**: Survival reward, incremental scoring bonus, and collision penalty.  
- **Modular Architecture**: Clean separation of game logic, AI loop, and asset management.  

### Installation
1. Clone the repository:  
   ```bash
   git clone https://github.com/your-username/FlappyAI.git
   cd FlappyAI
   ```
2. Create a virtual environment and install dependencies:  
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Configure NEAT parameters in `AI/config/config.txt` as needed.

### Usage
- **Manual Mode:** 
/config/config.py -> AI = False  
  ```bash
  python main.py
  ```
- **AI Training Mode:**  
/config/config.py -> AI = True
  ```bash
  python main.py
  ```

### Repository Structure
```plaintext
FlappyAI/
├── AI/
│   ├── config/
│   │   └── config.txt
│   └── scripts/
│       └── Head.py
├── config/
│   ├── config.py
│   └── constants.py
├── scripts/
│   ├── Assets.py
│   ├── Background.py
│   ├── GUI.py
│   ├── Pipe.py
│   └── PipeManager.py
├── main.py
└── requirements.txt
```

### Credits
Course project for **BIAL – Biologically Inspired Artificial Intelligence** at Silesian University of Technology, Faculty of Automatic Control, Electronics and Computer Science, Computer Science program.

---

## Polski

### Opis Projektu
FlappyAI to implementacja gry Flappy Bird oparta na algorytmie NEAT, w której sieci neuronowe uczą się sterować ptakiem poprzez ewolucję topologii i wag.

### Kluczowe Funkcje
- **Neuroewolucja z NEAT**: Adaptacja struktury i wag sieci w celu optymalizacji sterowania.  
- **Dostosowane Wejścia Sensoryczne**: Odległość do rur, pozycja pionowa i relatywne położenie szczeliny.  
- **Strategia Fitness**: Nagroda za przetrwanie, bonus za zdobywanie punktów, kara za kolizję.  
- **Modułowa Architektura**: Rozdział logiki gry, pętli AI i zarządzania zasobami.  

### Instalacja
1. Sklonuj repozytorium:  
   ```bash
   git clone https://github.com/your-username/FlappyAI.git
   cd FlappyAI
   ```
2. Utwórz wirtualne środowisko i zainstaluj zależności:  
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Skonfiguruj parametry NEAT w `AI/config/config.txt` według potrzeb.

### Użytkowanie
- **Tryb Manualny:**  
/config/config.py -> AI = False 
  ```bash
  python main.py
  ```
- **Tryb AI (trenowanie):** 
  
  /config/config.py -> AI = True
  ```bash
  python main.py 
  ```

### Struktura Repozytorium
```plaintext
FlappyAI/
├── AI/
│   ├── config/
│   │   └── config.txt
│   └── scripts/
│       └── Head.py
├── config/
│   ├── config.py
│   └── constants.py
├── scripts/
│   ├── Assets.py
│   ├── Background.py
│   ├── GUI.py
│   ├── Pipe.py
│   └── PipeManager.py
├── main.py
└── requirements.txt
```

### Podziękowania
Projekt wykonany na zaliczenie przedmiotu **BIAL – Biologically Inspired Artificial Intelligence** na Politechnice Śląskiej w Katowicach, Wydział Automatyki, Elektroniki i Informatyki, kierunek Informatyka.
