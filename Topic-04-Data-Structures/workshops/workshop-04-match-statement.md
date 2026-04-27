# Workshop 4: Match Statement
```bash
Section: Topic-04-Data-Structures - Workshop 4
Level: Beginner
Estimated Time: ~35 minutes
Prerequisites: Tutorial 4 (Match Statement)
```

---

## Workshop Objectives

By the end of this workshop you will be able to:

- Replace if-elif chains with match statements
- Use `_` as a default case and named variables to capture values
- Combine multiple values in one case using `|`
- Add guards to cases for extra conditions
- Write functions that use match with type hints

---

## Workshop Structure

1. Warm-Up - Reading Code
2. Exercise 1: Basic Match
3. Exercise 2: Default Case
4. Exercise 3: Matching Multiple Values
5. Exercise 4: Guards
6. Exercise 5: Match vs If-Elif
7. Exercise 6: Functions with Match
8. Challenge Exercise

---

## Setup

Create a new file called `workshop_match.py`. Make sure you are running Python 3.10 or later. Check with:

```bash
python --version
```

---

## 1. Warm-Up - Reading Code

Read the code below and answer the questions before running it.

```python
score = 85

match score // 10:
    case 10 | 9:
        result = "A - Excellent"
    case 8:
        result = "B - Good"
    case 7:
        result = "C - Fair"
    case 6:
        result = "D - Poor"
    case _:
        result = "F - Fail"

print(result)

day = "saturday"

match day:
    case "monday" | "tuesday" | "wednesday" | "thursday" | "friday":
        print("Weekday")
    case "saturday" | "sunday":
        print("Weekend")
    case _:
        print("Unknown day")

temperature = 15

match temperature:
    case t if t > 30:
        print("Hot")
    case t if t > 20:
        print("Warm")
    case t if t > 10:
        print("Cool")
    case _:
        print("Cold")
```

Questions - write your answers as comments first:

- What does `score // 10` evaluate to?
- What is printed for `result`?
- What is printed for `day`?
- What is printed for `temperature`?
- Why does the temperature block use `t` instead of `_`?

Run the code and check your predictions.

---

## 2. Exercise 1: Basic Match

#### Task 1.1 - Match Numbers

Write a match statement for a variable `number`. Print `"One"`, `"Two"`, or `"Three"` for values 1, 2, 3.

```python
number = 2

## TODO: match number and print the word
```

Expected output:
```bash
Two
```

---

#### Task 1.2 - Match Strings

Write a match statement for a variable `color`. Print `"Stop"` for `"red"`, `"Wait"` for `"yellow"`, `"Go"` for `"green"`.

```python
color = "green"

## TODO: match color and print the action
```

Expected output:
```bash
Go
```

---

#### Task 1.3 - Match Booleans

Write a match statement for `is_admin`. Print `"Full access"` for `True` and `"Limited access"` for `False`.

```python
is_admin = False

## TODO: match is_admin
```

Expected output:
```bash
Limited access
```

---

#### Task 1.4 - Days of the Week

Write a match statement for `day_number` (1 = Monday, 2 = Tuesday, 3 = Wednesday). Print the day name.

```python
day_number = 3

## TODO: match day_number and print the day name
```

Expected output:
```bash
Wednesday
```

---

## 3. Exercise 2: Default Case

#### Task 2.1 - Status Code Handler

Write a match statement for `status_code`. Handle `200` ("OK"), `404` ("Not Found"), `500` ("Server Error"). Use `_` for everything else.

```python
status_code = 403

## TODO: match status_code
```

Expected output:
```bash
Something else
```

---

#### Task 2.2 - Capture the Unknown Value

Rewrite Task 2.1 but use a named variable instead of `_` so you can print the unknown code in the message.

```python
status_code = 403

## TODO: match status_code, capture unknown into a variable
```

Expected output:
```bash
Unknown status: 403
```

---

#### Task 2.3 - Fruit Classifier

Write a match statement for `fruit`. Handle `"apple"` ("Red fruit"), `"banana"` ("Yellow fruit"), `"lime"` ("Green fruit"). Use a default for anything else.

```python
fruit = "mango"

## TODO: match fruit
```

Expected output:
```bash
Unknown fruit
```

---

#### Task 2.4 - Predict the Output

Read the code below. Write your prediction as a comment, then run it.

```python
command = "restart"

match command:
    case "start":
        print("Starting...")
    case "stop":
        print("Stopping...")
    case other:
        print(f"Unknown command: {other}")
```

- What prints?
- What is the value of `other`?
- What would happen if you replaced `other` with `_` and tried to print it?

---

## 4. Exercise 3: Matching Multiple Values

#### Task 3.1 - Weekday or Weekend

Write a match statement for `day`. Use `|` to group Monday–Friday as `"Weekday"` and Saturday–Sunday as `"Weekend"`.

```python
day = "tuesday"

## TODO: match day using |
```

Expected output:
```bash
Weekday
```

---

#### Task 3.2 - Vowel or Consonant

Write a match statement for `letter`. Print `"Vowel"` if it is `a`, `e`, `i`, `o`, or `u`. Print `"Consonant"` otherwise.

```python
letter = "e"

## TODO: match letter using |
```

Expected output:
```bash
Vowel
```

---

#### Task 3.3 - Grade Bands

Write a match statement that uses `score // 10` and `|` to group scores:
```bash
- 10 or 9 → `"A"`
- 8 → `"B"`
- 7 → `"C"`
- 6 → `"D"`
- anything else → `"F"`
```
#### Do it
```python
score = 92

## TODO: match score // 10
```

Expected output:
```bash
A
```

---

#### Task 3.4 - Season Classifier

Write a match statement for `month` 
(1–12). Group months into seasons:
```bash
- 12, 1, 2 → `"Winter"`
- 3, 4, 5 → `"Spring"`
- 6, 7, 8 → `"Summer"`
- 9, 10, 11 → `"Autumn"`
```

#### Do It!
```python
month = 4

## TODO: match month using |
```

Expected output:
```bash
Spring
```

---

## 5. Exercise 4: Guards

#### Task 4.1 - Temperature Classifier

Write a match statement for `temperature` using guards:

- above 30 → `"Hot"`
- above 20 → `"Warm"`
- above 10 → `"Cool"`
- otherwise → `"Cold"`

```python
temperature = 22

## TODO: match temperature with guards
```

Expected output:
```bash
Warm
```

---

#### Task 4.2 - Age Classifier

Write a match statement for `age` using guards:
```bash
- under 13 → `"Child"`
- under 18 → `"Teen"`
- under 65 → `"Adult"`
- otherwise → `"Senior"`
```

#### Do It!
```python
age = 17

## TODO: match age with guards
```

Expected output:
```bash
Teen
```

---

#### Task 4.3 - Weather and Temperature

Write a match statement for `weather` with a guard on temperature:

- `"sunny"` and temp above 20 → `"Go swimming"`
- `"sunny"` (any temp) → `"Go for a walk"`
- `"rainy"` → `"Stay indoors"`
- `"cloudy"` → `"Visit a museum"`
- default → `"Check the forecast"`

```python
weather = "sunny"
temp = 15

## TODO: match weather with guard on temp
```

Expected output:
```bash
Go for a walk
```

---

#### Task 4.4 - Predict the Output

Read the code below. Write your prediction as a comment, then run it.

```python
value = 7

match value:
    case v if v > 10:
        print("Big")
    case v if v > 5:
        print("Medium")
    case _:
        print("Small")
```

- What prints?
- What would print if `value = 3`?
- What would print if `value = 15`?

---

## 6. Exercise 5: Match vs If-Elif

#### Task 5.1 - Rewrite If-Elif as Match

Rewrite the code below using a match statement.

```python
day = "friday"

if day == "monday":
    print("Start of work week")
elif day == "friday":
    print("End of work week")
elif day == "saturday" or day == "sunday":
    print("Weekend")
else:
    print("Midweek")
```

```python
## TODO: rewrite using match
```

---

#### Task 5.2 - Rewrite Match as If-Elif

Rewrite the code below using if-elif.

```python
match status_code:
    case 200:
        print("OK")
    case 404:
        print("Not Found")
    case 500:
        print("Server Error")
    case _:
        print("Unknown")
```

```python
## TODO: rewrite using if-elif
```

---

#### Task 5.3 - Choose the Right Tool

For each situation below, write a comment saying whether you would use `match` or `if-elif` and why.

```python
## Situation 1: check if x > 0 and y > 0 at the same time
## Situation 2: map a menu number (1–5) to an action string
## Situation 3: check if a score is between 50 and 60
## Situation 4: map a day name to "Weekday" or "Weekend"
## Situation 5: check if a user is logged in AND has admin rights
```

---

## 7. Exercise 6: Functions with Match

#### Task 6.1 - Menu Handler

Complete the function below.

```python
def process_menu_choice(choice: int) -> str:
    """Return the action string for a menu option (1–4)."""
    match choice:
        case 1:
            return "View profile"
        ## TODO: case 2 → "Edit settings"
        ## TODO: case 3 → "Show help"
        ## TODO: case 4 → "Exit"
        ## TODO: default → "Invalid choice"

print(process_menu_choice(2))    ## Edit settings
print(process_menu_choice(3))    ## Show help
print(process_menu_choice(99))   ## Invalid choice
```

---

#### Task 6.2 - Simple Calculator

Write a function that uses match on `op` to perform the operation.

```python
def simple_calculator(a: int, b: int, op: str) -> float:
    """Perform a basic arithmetic operation."""
    ## TODO: match op
    ## "add"      → a + b
    ## "subtract" → a - b
    ## "multiply" → a * b
    ## "divide"   → a / b  (assume b != 0)
    ## default    → 0.0
    pass

print(simple_calculator(10, 3, "add"))        ## 13
print(simple_calculator(10, 3, "subtract"))   ## 7
print(simple_calculator(10, 3, "multiply"))   ## 30
print(simple_calculator(10, 3, "divide"))     ## 3.333...
print(simple_calculator(10, 3, "power"))      ## 0.0
```

---

#### Task 6.3 - Speed Classifier

Write a function using match with guards.

```python
def classify_speed(speed: int) -> str:
    """Classify a speed value into a category."""
    ## TODO: match speed with guards
    ## speed <= 0  → "Stationary"
    ## speed <= 30 → "Slow"
    ## speed <= 90 → "Normal"
    ## otherwise   → "Fast"
    pass

print(classify_speed(0))    ## Stationary
print(classify_speed(20))   ## Slow
print(classify_speed(60))   ## Normal
print(classify_speed(120))  ## Fast
```

---

#### Task 6.4 - BMI Classifier

Write a function using match with guards. Recall: $BMI < 18.5$ is underweight, $BMI < 25$ is normal, $BMI < 30$ is overweight, otherwise obese.

```python
def classify_bmi(bmi: float) -> str:
    """Return a BMI category string."""
    ## TODO: match bmi with guards
    pass

print(classify_bmi(17.0))   ## Underweight
print(classify_bmi(22.5))   ## Normal
print(classify_bmi(27.0))   ## Overweight
print(classify_bmi(35.0))   ## Obese
```

---

## 8. Challenge Exercise

#### Task - HTTP Response Handler

Write a function that takes a status code and returns a full response message. Then write a second function that processes a list of codes and prints a summary.

```python
def http_response(code: int) -> str:
    """Return a descriptive message for an HTTP status code."""
    ## TODO: use match with | to group codes
    ## 200 | 201 | 204 → "Success: ..."
    ## 301 | 302       → "Redirect: ..."
    ## 400             → "Bad Request"
    ## 401             → "Unauthorized"
    ## 403             → "Forbidden"
    ## 404             → "Not Found"
    ## 500 | 502 | 503 → "Server Error: ..."
    ## default         → f"Unknown code: {code}"
    pass


def process_responses(codes: list[int]) -> None:
    """Print a response message for each code in the list."""
    ## TODO: loop and print http_response for each code
    pass


codes = [200, 301, 404, 500, 403, 201, 999]
process_responses(codes)
```

Expected output:
Success: 200
Redirect: 301
Not Found
Server Error: 500
Forbidden
Success: 201
Unknown code: 999


---

## Key Takeaways

- `match` checks cases top to bottom - only the first match runs
- `_` is the wildcard default and must always be last
- use a named variable instead of `_` when you need the unmatched value in the message
- `|` combines multiple values into one case cleanly
- guards (`case x if condition`) add extra logic without nesting
- `match` shines when mapping one value to many fixed options
- for complex boolean logic or range checks, if-elif is still the right tool
- requires Python 3.10 or later - check with `python --version`