## Team Matcher Documentation

## 1. Project Overview
**Team Matcher** is a web-based tool designed to automate and optimize the formation of student groups. By leveraging a Genetic Algorithm, the application processes complex student data, such as availability, skills, and diversity metrics, to generate balanced, diverse teams.

* **Goal:** Replace inefficient and time-consuming manual grouping with an optimized data-driven approach.
* **Core Technology:** Django (Web Framework), PyGAD (Genetic Algorithm), NumPy (Data Processing).

---

## 2. Key Features

* **Student app:** Student side app to handle student data input and storage.
* **Teacher Dashboard:**
    * CSV Upload & Validation.
    * Historical tracking of past team generations.
    * Downloadable CSV output of results.
    * Results visualization.

* **Admin Dashboard:**
    * Student profile visualization.
    * Task modification.
    * CSV generations.
    * Team name template customization.

* **Automated Matching Engine:** Uses evolutionary computation to find the best fit for teams based on multiple conflicting constraints.
* **Smart Scheduling:** Calculates time slot overlaps to ensure every team has at least one valid meeting time.
* **Flexible Constraints:**
    * **Team Size:** User-defined Minimum and Maximum team sizes.
    * **Weights:** Adjustable priority sliders (e.g., prioritize "Availability" over "Skill Mix").

* **Modern UI:** Responsive, dark-mode interface built with Bootstrap 5.

---

## 3. How It Works (The Algorithm)

The core logic resides in the Genetic Algorithm (GA), which mimics natural selection to evolve a solution.

### 3.1. Data Encoding (Pre-processing)
Before processing, raw student data is converted into a numerical matrix:
1.  **Availability:** One-hot encoded into a 21-slot binary vector (7 days × 3 slots).
2.  **Categorical Data:** Mapped to integers (e.g., Business=1, CS=2).
3.  **Continuous Data:** Integer conversion if necessary.

### B. The Optimization Cycle
1.  **Initialization:** A population of random team assignments is generated.
2.  **Evaluation (Fitness Function):** Each schedule is scored based on:
    * **Intersection:** Shared time availability and task preferences between team members.
    * **Diversity:** Mix of heterogeneous criteria ( e.g. skills/gender/backgrounds).
    * **Homogeneity:** Alignment of commitment levels.
    * **Penalties:** 
        * Penalizarion of lack of leaders.
        * Penalization of min/max constraint violations.
        * Penalization of large deviation from average team size.
3.  **Evolution:** The best schedules crossover and randomly mutate to produce better schedules.
4.  **Convergence:** The process repeats for ~200 generations until an optimal solution is found.

---

## 4. Technical Architecture

### Tech Stack
* **Backend:** Python 3.12, Django 5.0
* **Algorithm:** PyGAD, NumPy
* **Frontend:** HTML5, Bootstrap 5, Jinja2 Templates
* **Database:** SQLite

## 5. Installation & Set-up

    git clone [https://github.com/yourusername/team-matcher.git](https://github.com/yourusername/team-matcher.git)
    cd team-matcher

    python -m venv .venv

    # on linux:
    source venv/bin/activate  
    # on Windows: 
    venv\Scripts\activate
    
    pip install -r requirements.txt

    python manage.py makemigrations
    python manage.py migrate
    python manage.py createsuperuser
    python manage.py runserver

